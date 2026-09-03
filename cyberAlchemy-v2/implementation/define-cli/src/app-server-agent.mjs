import {readFileSync} from "node:fs";
import {resolve} from "node:path";

import {
  connectGatewayRpcTransport,
  createAppServerRpcClient,
  spawnAppServerRpcTransport,
} from "../../agent-reasoning-engine/packages/codex-app-server-wrapper/index.mjs";

const APPLICATION_CONTEXT_KEY = "cyberalchemy.define.conversation";

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

function defaultGatewaySocket() {
  const runtimeRoot = process.env.XDG_RUNTIME_DIR || `/run/user/${typeof process.getuid === "function" ? process.getuid() : 1000}`;
  return resolve(runtimeRoot, "are-codex/gateway.sock");
}

export function createAppServerDefineAgent(options = {}) {
  const repositoryRoot = resolve(options.repository_root);
  const packageRoot = resolve(import.meta.dirname, "..");
  const wrapperRoot = resolve(packageRoot, "../agent-reasoning-engine/packages/codex-app-server-wrapper");
  const proxyPath = options.proxy_path ?? resolve(wrapperRoot, "bin/are-codex-app-server.mjs");
  const profilePath = options.profile_path ?? resolve(wrapperRoot, "profiles/repository-v1.json");
  const outputSchema = JSON.parse(readFileSync(resolve(packageRoot, "schemas/define-conversation-turn.schema.json"), "utf8"));
  const transportMode = options.transport_mode ?? (options.spawn_impl ? "direct" : "gateway");
  const gatewaySocket = resolve(options.gateway_socket ?? defaultGatewaySocket());
  const consumerId = options.consumer_id ?? "codex:human-chat";
  let transport = null;
  let client = options.rpc_client ?? null;
  let threadId = null;
  let closed = false;
  let startPromise = null;

  async function createTransport() {
    if (typeof options.transport_factory === "function") {
      return options.transport_factory({transport_mode: transportMode, gateway_socket: gatewaySocket, consumer_id: consumerId});
    }
    if (transportMode === "gateway") {
      return connectGatewayRpcTransport({
        socket_path: gatewaySocket,
        consumer_id: consumerId,
        lane: "interaction-bound",
        connect_impl: options.connect_impl,
      });
    }
    if (transportMode === "direct") {
      return spawnAppServerRpcTransport({
        command: process.execPath,
        args: [proxyPath, "--config", profilePath, "--repository-root", repositoryRoot],
        spawn_impl: options.spawn_impl,
      });
    }
    throw new Error(`define-agent.unsupported-transport:${transportMode}`);
  }

  function start() {
    startPromise ??= (async () => {
      if (closed) throw new Error("define-agent.closed");
      if (!client) {
        transport = await createTransport();
        client = createAppServerRpcClient({transport});
      }
      await client.initialize({
        clientInfo: {name: "cyberalchemy-define-cli", version: "0.2.0-candidate"},
        capabilities: {experimentalApi: true},
      });
      const params = {cwd: repositoryRoot, ephemeral: true, approvalPolicy: "never", sandbox: "read-only"};
      if (options.model) params.model = options.model;
      const started = await client.startThread(params);
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
    const result = await client.runTurn({
      threadId,
      input: [{type: "text", text: "Define the supplied conversational context."}],
      additionalContext: {
        [APPLICATION_CONTEXT_KEY]: {kind: "application", value: JSON.stringify(applicationContext)},
      },
      outputSchema,
      approvalPolicy: "never",
      sandboxPolicy: {type: "readOnly", networkAccess: false},
    });
    const completion = result.completed;
    if (completion?.turn?.status !== "completed") {
      const detail = completion?.turn?.error ?? completion?.turn?.failure ?? null;
      throw new Error(`define-agent.turn-${completion?.turn?.status ?? "unknown"}:${JSON.stringify(detail)}`);
    }
    let value;
    try { value = JSON.parse(result.text); } catch { throw new Error("define-agent.non-json-response"); }
    return validateTurn(value);
  }

  async function close() {
    if (closed) return;
    closed = true;
    await client?.close?.();
  }

  return Object.freeze({
    respond,
    close,
    inspect: () => ({
      thread_id: threadId,
      closed,
      transport_mode: transportMode,
      gateway_socket: transportMode === "gateway" ? gatewaySocket : null,
      rpc: client?.inspect?.() ?? null,
      authority_effect: "none",
    }),
  });
}
