import {EventEmitter} from "node:events";
import {createConnection} from "node:net";
import {PassThrough} from "node:stream";

import {GATEWAY_CONNECT_SCHEMA, GATEWAY_CONNECTED_SCHEMA} from "./gateway.mjs";

export function connectGatewayRpcTransport(options = {}) {
  const connectImpl = options.connect_impl ?? createConnection;
  const socket = connectImpl(options.socket_path);
  const output = new PassThrough();
  const failure = new EventEmitter();
  let buffer = "";
  let connected = false;
  let closing = false;
  let failed = false;
  let receipt = null;
  let resolveReady;
  let rejectReady;
  const ready = new Promise((resolveValue, reject) => {
    resolveReady = resolveValue;
    rejectReady = reject;
  });

  function fail(code, detail) {
    if (closing || failed) return;
    failed = true;
    const error = new Error(`${code}${detail ? `:${detail}` : ""}`);
    error.code = code;
    if (!connected) rejectReady(error);
    else failure.emit("failure", error);
    if (!socket.destroyed) socket.destroy();
  }

  socket.on("connect", () => {
    socket.write(`${JSON.stringify({schema_version: GATEWAY_CONNECT_SCHEMA, consumer_id: options.consumer_id, lane: options.lane})}\n`);
  });
  const onHandshakeData = (chunk) => {
    buffer += chunk.toString("utf8");
    if (buffer.length > 16384) return fail("gateway.handshake-too-large");
    const index = buffer.indexOf("\n");
    if (index < 0) return;
    socket.off("data", onHandshakeData);
    try { receipt = JSON.parse(buffer.slice(0, index)); } catch { receipt = null; }
    if (!receipt || receipt.schema_version !== GATEWAY_CONNECTED_SCHEMA || receipt.ok !== true) {
      return fail(receipt?.reason ?? "gateway.invalid-connect-receipt", receipt?.detail);
    }
    connected = true;
    const remainder = buffer.slice(index + 1);
    if (remainder) output.write(remainder);
    socket.on("data", (data) => output.write(data));
    resolveReady(receipt);
  };
  socket.on("data", onHandshakeData);
  socket.on("error", (error) => {
    if (!closing) fail("gateway.connection-failed", error.message);
  });
  socket.on("close", () => {
    output.end();
    if (!closing) fail("gateway.connection-closed");
  });

  async function close() {
    if (closing) return;
    closing = true;
    if (!socket.destroyed) socket.end();
  }

  return Object.freeze({
    kind: "persistent-gateway",
    input: socket,
    output,
    failure,
    ready,
    close,
    inspect: () => ({kind: "persistent-gateway", connected, closing, failed, receipt, authority_effect: "none"}),
  });
}

export function runGatewayClientProxy(options = {}) {
  const clientInput = options.client_input ?? process.stdin;
  const clientOutput = options.client_output ?? process.stdout;
  const clientError = options.client_error ?? process.stderr;
  const connectImpl = options.connect_impl ?? createConnection;
  const socket = connectImpl(options.socket_path);
  clientInput.pause?.();
  let buffer = "";
  let connected = false;

  socket.on("connect", () => {
    socket.write(`${JSON.stringify({schema_version: GATEWAY_CONNECT_SCHEMA, consumer_id: options.consumer_id, lane: options.lane})}\n`);
  });
  const onData = (chunk) => {
    buffer += chunk.toString("utf8");
    const index = buffer.indexOf("\n");
    if (index < 0) return;
    socket.off("data", onData);
    let receipt;
    try { receipt = JSON.parse(buffer.slice(0, index)); } catch { receipt = null; }
    if (!receipt || receipt.schema_version !== GATEWAY_CONNECTED_SCHEMA || receipt.ok !== true) {
      clientError.write(`${JSON.stringify(receipt ?? {reason: "gateway.invalid-connect-receipt"})}\n`);
      socket.destroy();
      return;
    }
    connected = true;
    const remainder = buffer.slice(index + 1);
    if (remainder) clientOutput.write(remainder);
    socket.on("data", (data) => clientOutput.write(data));
    clientInput.on("data", (data) => socket.write(data));
    clientInput.on("end", () => socket.end());
    clientInput.resume?.();
  };
  socket.on("data", onData);
  socket.on("error", (error) => clientError.write(`ARE gateway connection failed: ${error.message}\n`));
  socket.on("close", () => {
    if (!connected) clientInput.pause?.();
  });
  return socket;
}
