import {randomUUID} from "node:crypto";
import {chmodSync, existsSync, lstatSync, unlinkSync} from "node:fs";
import {createServer} from "node:net";

import {spawnCodexBackend} from "./backend.mjs";
import {freezeResult, isRecord, nonEmptyString} from "./canonical.mjs";
import {jsonLine, jsonRpcError, parseJsonLine} from "./protocol.mjs";

export const GATEWAY_CONNECT_SCHEMA = "are.codex-gateway-connect/v1";
export const GATEWAY_CONNECTED_SCHEMA = "are.codex-gateway-connected/v1";
const LANES = new Set(["plan-bound", "interaction-bound"]);

function send(stream, value) {
  if (stream && !stream.destroyed) stream.write(jsonLine(value));
}

function validateHandshake(value) {
  if (!isRecord(value) || value.schema_version !== GATEWAY_CONNECT_SCHEMA || !nonEmptyString(value.consumer_id) || !LANES.has(value.lane)) {
    return {ok: false, reason: "gateway.handshake-invalid"};
  }
  if (value.consumer_id.length > 256) return {ok: false, reason: "gateway.consumer-id-too-long"};
  return {ok: true, value: {consumer_id: value.consumer_id, lane: value.lane}};
}

function removeSocketPath(path) {
  if (!existsSync(path)) return;
  const stat = lstatSync(path);
  if (!stat.isSocket()) throw new Error(`Gateway listen path exists and is not a socket: ${path}`);
  unlinkSync(path);
}

function createLineReader(stream, onLine, onOverflow, initial = "") {
  let buffer = initial;
  const onData = (chunk) => {
    buffer += chunk.toString("utf8");
    if (buffer.length > 1024 * 1024) {
      onOverflow();
      return;
    }
    let index;
    while ((index = buffer.indexOf("\n")) >= 0) {
      const line = buffer.slice(0, index);
      buffer = buffer.slice(index + 1);
      if (line.trim()) onLine(line);
    }
  };
  stream.on("data", onData);
  return () => stream.off("data", onData);
}

function createSession({metadata, wrapper, backend, spawnImpl, WebSocketImpl, maxBufferedMessages, reconnectEnabled, onBackendStderr, onClosed}) {
  const child = spawnCodexBackend(backend, spawnImpl, WebSocketImpl);
  let client = null;
  let detachReader = null;
  let clientChain = Promise.resolve();
  let serverChain = Promise.resolve();
  let closed = false;
  let closeReason = null;
  const buffered = [];
  let reconnectCount = 0;

  function emitClient(value) {
    const encoded = jsonLine(value);
    if (client && !client.destroyed) {
      client.write(encoded);
      return;
    }
    buffered.push(encoded);
    if (buffered.length > maxBufferedMessages) stop("gateway.detached-buffer-overflow");
  }

  function processClientLine(line) {
    clientChain = clientChain.then(async () => {
      const parsed = parseJsonLine(line);
      if (!parsed.ok) {
        emitClient(jsonRpcError(null, -32700, "Parse error", parsed));
        return;
      }
      const actions = await wrapper.processClientMessage(parsed.value);
      for (const message of actions.to_server) send(child.stdin, message);
      for (const message of actions.to_client) emitClient(message);
    }).catch((error) => emitClient(jsonRpcError(null, -32603, "Gateway client-path failure", {message: error.message})));
  }

  const detachServerReader = createLineReader(child.stdout, (line) => {
    serverChain = serverChain.then(async () => {
      const parsed = parseJsonLine(line);
      if (!parsed.ok) {
        emitClient(jsonRpcError(null, -32700, "App-server parse error", parsed));
        return;
      }
      const actions = await wrapper.processServerMessage(parsed.value);
      for (const message of actions.to_server) send(child.stdin, message);
      for (const message of actions.to_client) emitClient(message);
    }).catch((error) => emitClient(jsonRpcError(null, -32603, "Gateway server-path failure", {message: error.message})));
  }, () => stop("gateway.upstream-line-too-large"));

  child.stderr.on("data", (chunk) => onBackendStderr(chunk, metadata));
  child.on("exit", (code, signal) => {
    if (closed) return;
    emitClient(jsonRpcError(null, -32090, "Codex app-server backend exited", {code, signal, authority_effect: "none"}));
    stop("gateway.upstream-exited", false, false);
  });
  child.on("error", (error) => {
    if (closed) return;
    emitClient(jsonRpcError(null, -32091, "Codex app-server backend failed", {message: error.message, authority_effect: "none"}));
    stop("gateway.upstream-failed", false, false);
  });

  function attach(socket) {
    if (closed) return {ok: false, reason: closeReason ?? "gateway.session-closed"};
    if (client && !client.destroyed) return {ok: false, reason: "gateway.consumer-already-attached"};
    client = socket;
    reconnectCount += 1;
    detachReader = createLineReader(socket, processClientLine, () => stop("gateway.client-line-too-large"));
    const detach = () => {
      if (client !== socket) return;
      detachReader?.();
      detachReader = null;
      client = null;
      if (!reconnectEnabled) stop("gateway.client-disconnected");
    };
    socket.once("close", detach);
    socket.once("error", detach);
    return {ok: true};
  }

  function flushBuffered() {
    if (!client || client.destroyed) return;
    for (const encoded of buffered.splice(0)) client.write(encoded);
  }

  function stop(reason = "gateway.closed", killChild = true, destroyClient = true) {
    if (closed) return;
    closed = true;
    closeReason = reason;
    detachReader?.();
    detachServerReader();
    if (client && !client.destroyed) {
      if (destroyClient) client.destroy();
      else client.end();
    }
    client = null;
    if (killChild && typeof child.kill === "function") child.kill("SIGTERM");
    onClosed(metadata.consumer_id, api);
  }

  const api = Object.freeze({
    attach,
    flushBuffered,
    stop,
    metadata: freezeResult(metadata),
    child,
    inspect: () => freezeResult({
      consumer_id: metadata.consumer_id,
      lane: metadata.lane,
      attached: Boolean(client && !client.destroyed),
      buffered_messages: buffered.length,
      reconnect_count: reconnectCount,
      closed,
      close_reason: closeReason,
      wrapper_state: typeof wrapper.inspectState === "function" ? wrapper.inspectState() : null,
      authority_effect: "none",
    }),
  });
  return api;
}

export function createPersistentGateway(options = {}) {
  if (!nonEmptyString(options.listen_path)) throw new TypeError("A Unix gateway listen_path is required.");
  if (typeof options.wrapper_factory !== "function") throw new TypeError("A wrapper_factory is required.");
  const maxClients = options.max_clients ?? 8;
  const maxBufferedMessages = options.max_buffered_messages_per_client ?? 256;
  if (!Number.isSafeInteger(maxClients) || maxClients < 1) throw new TypeError("max_clients must be a positive safe integer.");
  if (!Number.isSafeInteger(maxBufferedMessages) || maxBufferedMessages < 1) throw new TypeError("max_buffered_messages_per_client must be a positive safe integer.");
  const runtimeEpochId = options.runtime_epoch_id ?? `are-gateway-runtime:${randomUUID()}`;
  const reconnectEnabled = options.reconnect !== false;
  const sessions = new Map();
  const authorizeClient = options.authorize_client ?? (() => true);
  const server = createServer();
  let started = false;

  function closeSession(consumerId, session) {
    if (sessions.get(consumerId) === session) sessions.delete(consumerId);
  }

  server.on("connection", (socket) => {
    let buffer = "";
    const onData = (chunk) => {
      buffer += chunk.toString("utf8");
      if (buffer.length > 16384) {
        send(socket, {schema_version: GATEWAY_CONNECTED_SCHEMA, ok: false, reason: "gateway.handshake-too-large", authority_effect: "none"});
        socket.end();
        return;
      }
      const index = buffer.indexOf("\n");
      if (index < 0) return;
      socket.off("data", onData);
      const line = buffer.slice(0, index);
      const remainder = buffer.slice(index + 1);
      let parsed;
      try { parsed = JSON.parse(line); } catch { parsed = null; }
      const handshake = validateHandshake(parsed);
      if (!handshake.ok || authorizeClient(handshake.value ?? parsed) !== true) {
        send(socket, {schema_version: GATEWAY_CONNECTED_SCHEMA, ok: false, reason: handshake.ok ? "gateway.client-not-authorized" : handshake.reason, authority_effect: "none"});
        socket.end();
        return;
      }
      const metadata = handshake.value;
      let session = sessions.get(metadata.consumer_id);
      if (session && session.metadata.lane !== metadata.lane) {
        send(socket, {schema_version: GATEWAY_CONNECTED_SCHEMA, ok: false, reason: "gateway.consumer-lane-mismatch", authority_effect: "none"});
        socket.end();
        return;
      }
      if (!session) {
        if (sessions.size >= maxClients) {
          send(socket, {schema_version: GATEWAY_CONNECTED_SCHEMA, ok: false, reason: "gateway.max-clients-reached", authority_effect: "none"});
          socket.end();
          return;
        }
        try {
          const wrapper = options.wrapper_factory(metadata);
          session = createSession({
            metadata,
            wrapper,
            backend: options.backend ?? {},
            spawnImpl: options.spawn_impl,
            WebSocketImpl: options.websocket_impl,
            maxBufferedMessages,
            reconnectEnabled,
            onBackendStderr: options.on_backend_stderr ?? (() => {}),
            onClosed: closeSession,
          });
        } catch (error) {
          send(socket, {schema_version: GATEWAY_CONNECTED_SCHEMA, ok: false, reason: "gateway.session-start-failed", detail: error.message, authority_effect: "none"});
          socket.end();
          return;
        }
        sessions.set(metadata.consumer_id, session);
      }
      const attached = session.attach(socket);
      if (!attached.ok) {
        send(socket, {schema_version: GATEWAY_CONNECTED_SCHEMA, ok: false, reason: attached.reason, authority_effect: "none"});
        socket.end();
        return;
      }
      send(socket, {schema_version: GATEWAY_CONNECTED_SCHEMA, ok: true, consumer_id: metadata.consumer_id, lane: metadata.lane, runtime_epoch_id: runtimeEpochId, resumed: session.inspect().reconnect_count > 1, authority_effect: "none"});
      setImmediate(() => session.flushBuffered());
      if (remainder) socket.emit("data", Buffer.from(remainder));
    };
    socket.on("data", onData);
  });

  async function start() {
    if (started) return api;
    removeSocketPath(options.listen_path);
    await new Promise((resolveStart, reject) => {
      server.once("error", reject);
      server.listen(options.listen_path, () => {
        server.off("error", reject);
        resolveStart();
      });
    });
    chmodSync(options.listen_path, 0o600);
    started = true;
    return api;
  }

  async function close() {
    for (const session of [...sessions.values()]) session.stop("gateway.shutdown");
    if (started) await new Promise((resolveClose) => server.close(resolveClose));
    started = false;
    removeSocketPath(options.listen_path);
  }

  const api = Object.freeze({
    start,
    close,
    server,
    inspect: () => freezeResult({
      schema_version: "are.codex-persistent-gateway-state/v1",
      runtime_epoch_id: runtimeEpochId,
      listen_path: options.listen_path,
      started,
      sessions: [...sessions.values()].map((session) => session.inspect()).sort((a, b) => a.consumer_id.localeCompare(b.consumer_id)),
      authority_effect: "none",
    }),
  });
  return api;
}
