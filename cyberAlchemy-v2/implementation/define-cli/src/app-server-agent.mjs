import {spawn} from "node:child_process";
import {readFileSync} from "node:fs";
import {resolve} from "node:path";
import {createInterface} from "node:readline";

const APPLICATION_CONTEXT_KEY = "cyberalchemy.define.conversation";

function bounded(promise, label, milliseconds) {
  return new Promise((resolveValue, reject) => {
    const timer = setTimeout(() => reject(new Error(`define-agent.${label}-timeout`)), milliseconds);
    promise.then(
      (value) => { clearTimeout(timer); resolveValue(value); },
      (error) => { clearTimeout(timer); reject(error); },
    );
  });
}

function validateTurn(value) {
  const phases = new Set(["discover", "scope-review", "options-ready", "option-discussion"]);
  if (!value || typeof value !== "object" || Array.isArray(value)) throw new Error("define-agent.invalid-turn-object");
  if (value.schema_version !== "cav2.define-conversation-turn/v1") throw new Error("define-agent.invalid-turn-version");
  if (!phases.has(value.phase) || typeof value.message !== "string" || !value.message.trim()) throw new Error("define-agent.invalid-turn-message");
  if (value.phase === "discover" && (typeof value.question !== "string" || !value.question.trim())) throw new Error("define-agent.discovery-question-required");
  if (typeof value.scope_ready !== "boolean" || !value.scope || typeof value.scope !== "object") throw new Error("define-agent.invalid-turn-scope");
  if (!Array.isArray(value.options) || value.options.length > 12) throw new Error("define-agent.invalid-turn-options");
  const optionIds = new Set();
  const optionTerms = new Set();
  for (const option of value.options) {
    if (!option || typeof option !== "object" || !String(option.option_id ?? "").trim() || !String(option.term ?? "").trim()) {
      throw new Error("define-agent.invalid-option");
    }
    const optionId = String(option.option_id).trim();
    const optionTerm = String(option.term).trim().toLowerCase();
    if (optionIds.has(optionId) || optionTerms.has(optionTerm)) throw new Error("define-agent.duplicate-option");
    optionIds.add(optionId);
    optionTerms.add(optionTerm);
  }
  return value;
}

function agentText(completed, deltas) {
  const items = completed?.turn?.items ?? [];
  const messages = items.filter((item) => item?.type === "agentMessage" && typeof item.text === "string");
  if (messages.length > 0) return messages[messages.length - 1].text;
  return deltas;
}

export function createAppServerDefineAgent(options = {}) {
  const repositoryRoot = resolve(options.repository_root);
  const packageRoot = resolve(import.meta.dirname, "..");
  const wrapperRoot = resolve(packageRoot, "../agent-reasoning-engine/packages/codex-app-server-wrapper");
  const proxyPath = options.proxy_path ?? resolve(wrapperRoot, "bin/are-codex-app-server.mjs");
  const profilePath = options.profile_path ?? resolve(wrapperRoot, "profiles/repository-v1.json");
  const outputSchema = JSON.parse(readFileSync(resolve(packageRoot, "schemas/define-conversation-turn.schema.json"), "utf8"));
  const child = (options.spawn_impl ?? spawn)(process.execPath, [proxyPath, "--config", profilePath, "--repository-root", repositoryRoot], {stdio: ["pipe", "pipe", "pipe"]});
  const pending = new Map();
  const completed = new Map();
  const completionWaiters = new Map();
  const deltas = new Map();
  let sequence = 0;
  let threadId = null;
  let stderr = "";
  let closed = false;
  let closeError = null;
  let startPromise = null;

  child.stderr.on("data", (chunk) => { stderr = `${stderr}${chunk}`.slice(-16384); });
  createInterface({input: child.stdout, crlfDelay: Infinity}).on("line", (line) => {
    let message;
    try { message = JSON.parse(line); } catch { return; }
    if (message.method === "item/agentMessage/delta") {
      const turnId = message.params?.turnId;
      if (turnId) deltas.set(turnId, `${deltas.get(turnId) ?? ""}${message.params?.delta ?? ""}`);
    }
    if (message.method === "turn/completed") {
      const turnId = message.params?.turn?.id;
      if (turnId) {
        completed.set(turnId, message.params);
        completionWaiters.get(turnId)?.resolve(message.params);
        completionWaiters.delete(turnId);
      }
    }
    if (message.method?.endsWith("/requestApproval") && Object.hasOwn(message, "id")) {
      const result = message.method === "item/permissions/requestApproval" ? {permissions: {}} : {decision: "decline"};
      child.stdin.write(`${JSON.stringify({jsonrpc: "2.0", id: message.id, result})}\n`);
      return;
    }
    if (Object.hasOwn(message, "id") && pending.has(String(message.id))) {
      const waiter = pending.get(String(message.id));
      pending.delete(String(message.id));
      if (message.error) waiter.reject(new Error(`define-agent.${waiter.method}:${JSON.stringify(message.error)}`));
      else waiter.resolve(message.result);
    }
  });
  function markClosed(error) {
    if (closeError) return;
    closed = true;
    closeError = error;
    for (const waiter of pending.values()) waiter.reject(error);
    pending.clear();
    for (const waiter of completionWaiters.values()) waiter.reject(error);
    completionWaiters.clear();
  }

  child.on("error", (error) => {
    markClosed(new Error(`define-agent.app-server-spawn-failed:${error.message}`));
  });
  child.on("exit", (code, signal) => {
    markClosed(new Error(`define-agent.app-server-exited:${signal ?? code}${stderr ? `:${stderr.trim()}` : ""}`));
  });

  function request(method, params) {
    if (closed) return Promise.reject(closeError ?? new Error("define-agent.closed"));
    const id = ++sequence;
    child.stdin.write(`${JSON.stringify({jsonrpc: "2.0", id, method, params})}\n`);
    return new Promise((resolveValue, reject) => pending.set(String(id), {resolve: resolveValue, reject, method}));
  }

  function waitForCompletion(turnId) {
    if (completed.has(turnId)) return Promise.resolve(completed.get(turnId));
    if (closed) return Promise.reject(closeError ?? new Error("define-agent.closed"));
    return new Promise((resolveValue, reject) => completionWaiters.set(turnId, {resolve: resolveValue, reject}));
  }

  function start() {
    startPromise ??= (async () => {
      await bounded(request("initialize", {
        clientInfo: {name: "cyberalchemy-define-cli", version: "0.2.0-candidate"},
        capabilities: {experimentalApi: true},
      }), "initialize", 180000);
      const params = {cwd: repositoryRoot, ephemeral: true, approvalPolicy: "never", sandbox: "read-only"};
      if (options.model) params.model = options.model;
      const started = await bounded(request("thread/start", params), "thread-start", 240000);
      threadId = started.thread.id;
    })();
    return startPromise;
  }

  async function respond(payload) {
    if (!threadId) await start();
    const applicationContext = {
      schema_version: "cav2.define-conversation-request/v1",
      instructions: [
        "Act as a collaborative Define facilitator.",
        "Begin from broad domain, subject, context, or project language and respond naturally before narrowing.",
        "Ask at most one focused question per discovery turn.",
        "Put that focused question in the question field; keep it separate from the reflective message. Use null outside discovery.",
        "Do not treat an inference as confirmed; propose a scope and wait for explicit confirmation.",
        "Conversational agreement does not confirm scope. Mark scope_ready true when the scope can be shown, but the terminal controller owns the separate confirmation step.",
        "After scope confirmation, identify a small bounded set of meaning options for one-by-one review.",
        "Candidate meanings are proposals only. Never claim a source, owner, permission, or canonical status that was not supplied.",
        "Do not use tools. Return only the JSON object required by the output schema.",
      ],
      conversation: payload,
    };
    const started = await bounded(request("turn/start", {
      threadId,
      input: [{type: "text", text: "Define the supplied conversational context."}],
      additionalContext: {
        [APPLICATION_CONTEXT_KEY]: {kind: "application", value: JSON.stringify(applicationContext)},
      },
      outputSchema,
      approvalPolicy: "never",
      sandboxPolicy: {type: "readOnly", networkAccess: false},
    }), "turn-start", 180000);
    const turnId = started.turn.id;
    const completion = await bounded(waitForCompletion(turnId), "turn-completed", 300000);
    if (completion?.turn?.status !== "completed") {
      const detail = completion?.turn?.error ?? completion?.turn?.failure ?? null;
      throw new Error(`define-agent.turn-${completion?.turn?.status ?? "unknown"}:${JSON.stringify(detail)}`);
    }
    const text = agentText(completion, deltas.get(turnId) ?? "");
    let value;
    try { value = JSON.parse(text); } catch { throw new Error("define-agent.non-json-response"); }
    return validateTurn(value);
  }

  async function close() {
    if (closed) return;
    closed = true;
    closeError = new Error("define-agent.closed");
    child.stdin.end();
    child.kill("SIGTERM");
  }

  return Object.freeze({respond, close, inspect: () => ({thread_id: threadId, stderr, closed, close_error: closeError?.message ?? null, authority_effect: "none"})});
}
