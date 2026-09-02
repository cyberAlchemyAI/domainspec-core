import {EventEmitter} from "node:events";
import {spawn} from "node:child_process";
import {createInterface} from "node:readline";

export class AppServerRpcError extends Error {
  constructor(code, message, details = null) {
    super(message);
    this.name = "AppServerRpcError";
    this.code = code;
    this.details = details;
  }
}

export function spawnAppServerRpcTransport(options = {}) {
  const child = (options.spawn_impl ?? spawn)(options.command, options.args ?? [], {stdio: ["pipe", "pipe", "pipe"], env: options.env ?? process.env});
  const failure = new EventEmitter();
  let stderr = "";
  let closing = false;
  let failed = false;
  child.stderr.on("data", (chunk) => { stderr = `${stderr}${chunk}`.slice(-16384); });
  child.on("error", (error) => {
    if (closing || failed) return;
    failed = true;
    failure.emit("failure", new AppServerRpcError("rpc.transport-spawn-failed", `App-server transport failed to start: ${error.message}`, {cause: error.message}));
  });
  child.on("exit", (code, signal) => {
    if (closing || failed) return;
    failed = true;
    failure.emit("failure", new AppServerRpcError("rpc.transport-exited", `App-server transport exited: ${signal ?? code}${stderr ? `: ${stderr.trim()}` : ""}`, {code, signal, stderr}));
  });
  async function close() {
    if (closing) return;
    closing = true;
    child.stdin.end();
    if (child.exitCode === null) child.kill("SIGTERM");
  }
  return Object.freeze({
    kind: "spawned-stdio",
    input: child.stdin,
    output: child.stdout,
    failure,
    ready: Promise.resolve({kind: "spawned-stdio", authority_effect: "none"}),
    close,
    inspect: () => ({kind: "spawned-stdio", closing, failed, stderr, exit_code: child.exitCode, authority_effect: "none"}),
  });
}

function defaultApproval(message) {
  if (message.method === "item/permissions/requestApproval") return {permissions: {}};
  return {decision: "decline"};
}

function agentText(completed, deltas) {
  const items = completed?.turn?.items ?? [];
  const messages = items.filter((item) => item?.type === "agentMessage" && typeof item.text === "string");
  return messages.length > 0 ? messages[messages.length - 1].text : deltas;
}

export function createAppServerRpcClient(options = {}) {
  const transport = options.transport;
  if (!transport?.input || !transport?.output || !transport?.ready) throw new TypeError("An app-server RPC transport is required.");
  const requestTimeout = options.request_timeout_ms ?? 180000;
  const completionTimeout = options.completion_timeout_ms ?? 300000;
  const maxNotifications = options.max_notifications ?? 512;
  const pending = new Map();
  const notifications = [];
  const waiters = new Set();
  const deltas = new Map();
  const events = new EventEmitter();
  let sequence = 0;
  let closed = false;
  let failure = null;

  function failAll(error) {
    if (failure) return;
    failure = error instanceof Error ? error : new AppServerRpcError("rpc.transport-failed", String(error));
    closed = true;
    for (const entry of pending.values()) {
      clearTimeout(entry.timer);
      entry.reject(failure);
    }
    pending.clear();
    for (const waiter of waiters) {
      clearTimeout(waiter.timer);
      waiter.reject(failure);
    }
    waiters.clear();
    events.emit("failure", failure);
  }

  function send(value) {
    if (closed) throw failure ?? new AppServerRpcError("rpc.closed", "App-server RPC client is closed.");
    transport.input.write(`${JSON.stringify(value)}\n`);
  }

  function rememberNotification(message) {
    notifications.push(message);
    if (notifications.length > maxNotifications) notifications.splice(0, notifications.length - maxNotifications);
    for (const waiter of [...waiters]) {
      let matched = false;
      try { matched = waiter.predicate(message); } catch (error) {
        clearTimeout(waiter.timer);
        waiters.delete(waiter);
        waiter.reject(error);
        continue;
      }
      if (!matched) continue;
      clearTimeout(waiter.timer);
      waiters.delete(waiter);
      waiter.resolve(message);
    }
    events.emit("notification", message);
  }

  async function handleMessage(message) {
    if (Object.hasOwn(message, "id") && !message.method) {
      const entry = pending.get(String(message.id));
      if (!entry) return;
      clearTimeout(entry.timer);
      pending.delete(String(message.id));
      if (message.error) entry.reject(new AppServerRpcError("rpc.response-error", `${entry.method}: ${message.error.message ?? "JSON-RPC error"}`, message.error));
      else entry.resolve(message.result);
      return;
    }
    if (message.method === "item/agentMessage/delta") {
      const turnId = message.params?.turnId;
      if (turnId) deltas.set(turnId, `${deltas.get(turnId) ?? ""}${message.params?.delta ?? ""}`);
    }
    if (message.method?.endsWith("/requestApproval") && Object.hasOwn(message, "id")) {
      const result = await (options.approval_handler?.(message) ?? defaultApproval(message));
      send({jsonrpc: "2.0", id: message.id, result});
      return;
    }
    rememberNotification(message);
  }

  const lines = createInterface({input: transport.output, crlfDelay: Infinity});
  let ordered = Promise.resolve();
  lines.on("line", (line) => {
    ordered = ordered.then(async () => {
      let message;
      try { message = JSON.parse(line); } catch {
        throw new AppServerRpcError("rpc.invalid-json", "App-server transport emitted invalid JSON.", {line: line.slice(0, 1024)});
      }
      await handleMessage(message);
    }).catch(failAll);
  });
  lines.on("error", failAll);
  transport.failure?.on("failure", failAll);

  async function request(method, params, requestOptions = {}) {
    await transport.ready;
    if (closed) throw failure ?? new AppServerRpcError("rpc.closed", "App-server RPC client is closed.");
    const id = `are-rpc-${++sequence}`;
    const timeoutMs = requestOptions.timeout_ms ?? requestTimeout;
    return new Promise((resolveValue, reject) => {
      const timer = setTimeout(() => {
        pending.delete(id);
        reject(new AppServerRpcError("rpc.request-timeout", `${method} timed out after ${timeoutMs} ms.`, {method, timeout_ms: timeoutMs}));
      }, timeoutMs);
      pending.set(id, {method, resolve: resolveValue, reject, timer});
      try { send({jsonrpc: "2.0", id, method, params}); } catch (error) {
        clearTimeout(timer);
        pending.delete(id);
        reject(error);
      }
    });
  }

  function waitForNotification(predicate, waitOptions = {}) {
    const existing = notifications.find(predicate);
    if (existing) return Promise.resolve(existing);
    if (closed) return Promise.reject(failure ?? new AppServerRpcError("rpc.closed", "App-server RPC client is closed."));
    const timeoutMs = waitOptions.timeout_ms ?? completionTimeout;
    return new Promise((resolveValue, reject) => {
      const waiter = {predicate, resolve: resolveValue, reject, timer: null};
      waiter.timer = setTimeout(() => {
        waiters.delete(waiter);
        reject(new AppServerRpcError("rpc.notification-timeout", `App-server notification timed out after ${timeoutMs} ms.`, {timeout_ms: timeoutMs}));
      }, timeoutMs);
      waiters.add(waiter);
    });
  }

  async function initialize(params) {
    return request("initialize", params);
  }

  async function startThread(params) {
    return request("thread/start", params, {timeout_ms: options.thread_start_timeout_ms ?? 240000});
  }

  async function runTurn(params) {
    const started = await request("turn/start", params);
    const turnId = started?.turn?.id;
    if (!turnId) throw new AppServerRpcError("rpc.turn-id-missing", "turn/start did not return a turn identity.");
    const notification = await waitForNotification(
      (message) => message.method === "turn/completed" && message.params?.turn?.id === turnId,
      {timeout_ms: options.completion_timeout_ms ?? completionTimeout},
    );
    return {started, completed: notification.params, text: agentText(notification.params, deltas.get(turnId) ?? "")};
  }

  async function close() {
    if (closed) return;
    const error = new AppServerRpcError("rpc.closed", "App-server RPC client was closed.");
    failAll(error);
    lines.close();
    await transport.close?.();
  }

  return Object.freeze({
    request,
    initialize,
    startThread,
    runTurn,
    waitForNotification,
    close,
    events,
    inspect: () => ({closed, failure: failure?.message ?? null, pending_requests: pending.size, notification_waiters: waiters.size, transport: transport.inspect?.() ?? null, authority_effect: "none"}),
  });
}
