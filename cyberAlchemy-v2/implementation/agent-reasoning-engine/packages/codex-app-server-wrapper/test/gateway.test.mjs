import assert from "node:assert/strict";
import {EventEmitter, once} from "node:events";
import {mkdtempSync} from "node:fs";
import {createConnection} from "node:net";
import {resolve} from "node:path";
import {PassThrough} from "node:stream";
import test from "node:test";

import {
  connectGatewayRpcTransport,
  createPersistentGateway,
  GATEWAY_CONNECT_SCHEMA,
  resolveBackendCommand,
  runGatewayClientProxy,
} from "../index.mjs";

function fakeChild() {
  const child = new EventEmitter();
  child.stdin = new PassThrough();
  child.stdout = new PassThrough();
  child.stderr = new PassThrough();
  child.killed = false;
  child.kill = () => { child.killed = true; child.emit("exit", 0, "SIGTERM"); };
  return child;
}

function passThroughWrapper() {
  return {
    processClientMessage: async (message) => ({to_server: [message], to_client: []}),
    processServerMessage: async (message) => ({to_server: [], to_client: [message]}),
  };
}

function nextJsonLine(stream, timeout = 2000, label = "JSON line") {
  return new Promise((resolveLine, reject) => {
    let buffer = "";
    const timer = setTimeout(() => reject(new Error(`timed out waiting for ${label}`)), timeout);
    function onData(chunk) {
      buffer += chunk.toString("utf8");
      const index = buffer.indexOf("\n");
      if (index < 0) return;
      clearTimeout(timer);
      stream.off("data", onData);
      resolveLine(JSON.parse(buffer.slice(0, index)));
    }
    stream.on("data", onData);
  });
}

function collectJsonLines(stream) {
  let buffer = "";
  const queue = [];
  const waiters = [];
  stream.on("data", (chunk) => {
    buffer += chunk.toString("utf8");
    let index;
    while ((index = buffer.indexOf("\n")) >= 0) {
      const value = JSON.parse(buffer.slice(0, index));
      buffer = buffer.slice(index + 1);
      const waiter = waiters.shift();
      if (waiter) waiter(value);
      else queue.push(value);
    }
  });
  return {next: (label = "collected JSON line") => queue.length ? Promise.resolve(queue.shift()) : new Promise((resolveValue, reject) => {
    const timer = setTimeout(() => reject(new Error(`timed out waiting for ${label}`)), 2000);
    waiters.push((value) => { clearTimeout(timer); resolveValue(value); });
  })};
}

async function waitFor(predicate, label) {
  const deadline = Date.now() + 2000;
  while (Date.now() < deadline) {
    if (predicate()) return;
    await new Promise((resolveWait) => setTimeout(resolveWait, 10));
  }
  throw new Error(`timed out waiting for ${label}`);
}

async function connectGateway(path, consumerId, lane) {
  const socket = createConnection(path);
  await once(socket, "connect");
  const receipt = nextJsonLine(socket, 2000, `${consumerId} handshake`);
  socket.write(`${JSON.stringify({schema_version: GATEWAY_CONNECT_SCHEMA, consumer_id: consumerId, lane})}\n`);
  return {socket, receipt: await receipt};
}

function fixture(options = {}) {
  const directory = mkdtempSync("/tmp/are-gateway-test-");
  const listenPath = resolve(directory, "gateway.sock");
  const children = [];
  const gateway = createPersistentGateway({
    listen_path: listenPath,
    runtime_epoch_id: "are-gateway-runtime:test",
    backend: options.backend ?? {mode: "direct-stdio"},
    max_clients: options.max_clients ?? 4,
    max_buffered_messages_per_client: options.max_buffered_messages_per_client ?? 4,
    reconnect: options.reconnect ?? true,
    authorize_client: options.authorize_client,
    wrapper_factory: passThroughWrapper,
    spawn_impl: (command, args) => {
      const child = fakeChild();
      child.command = command;
      child.args = args;
      children.push(child);
      return child;
    },
  });
  return {gateway, listenPath, children};
}

test("backend resolution distinguishes direct stdio from the official daemon proxy", () => {
  assert.deepEqual(resolveBackendCommand({mode: "direct-stdio"}).args, ["app-server", "--stdio"]);
  assert.deepEqual(resolveBackendCommand({mode: "daemon-proxy", socket_path: "/tmp/codex.sock"}).args, ["app-server", "proxy", "--sock", "/tmp/codex.sock"]);
  assert.equal(resolveBackendCommand({mode: "websocket", url: "ws://127.0.0.1:4500"}).url, "ws://127.0.0.1:4500");
  assert.throws(() => resolveBackendCommand({mode: "invented"}), /Unsupported/);
});

test("gateway preserves one consumer session and buffered output across reconnect", async (context) => {
  const {gateway, listenPath, children} = fixture();
  await gateway.start();
  context.after(() => gateway.close());
  const first = await connectGateway(listenPath, "codex:plan", "plan-bound");
  assert.equal(first.receipt.ok, true);
  assert.equal(first.receipt.resumed, false);
  assert.equal(children.length, 1);
  const upstream = nextJsonLine(children[0].stdin, 2000, "first upstream request");
  first.socket.write(`${JSON.stringify({jsonrpc: "2.0", id: 1, method: "initialize", params: {}})}\n`);
  assert.equal((await upstream).method, "initialize");
  first.socket.destroy();
  await once(first.socket, "close");
  await waitFor(() => gateway.inspect().sessions[0]?.attached === false, "gateway detach");
  children[0].stdout.write(`${JSON.stringify({id: 1, result: {ready: true}})}\n`);
  await waitFor(() => gateway.inspect().sessions[0]?.buffered_messages === 1, "detached response buffer");
  const secondSocket = createConnection(listenPath);
  const secondLines = collectJsonLines(secondSocket);
  await once(secondSocket, "connect");
  secondSocket.write(`${JSON.stringify({schema_version: GATEWAY_CONNECT_SCHEMA, consumer_id: "codex:plan", lane: "plan-bound"})}\n`);
  const receipt = await secondLines.next("reconnect handshake");
  assert.equal(receipt.resumed, true);
  const replayed = await secondLines.next("buffered replay");
  assert.equal(replayed.result.ready, true);
  assert.equal(children.length, 1);
  secondSocket.destroy();
});

test("gateway isolates consumers and rejects lane substitution", async (context) => {
  const {gateway, listenPath, children} = fixture();
  await gateway.start();
  context.after(() => gateway.close());
  const plan = await connectGateway(listenPath, "codex:plan", "plan-bound");
  const human = await connectGateway(listenPath, "codex:human-chat", "interaction-bound");
  assert.equal(plan.receipt.ok, true);
  assert.equal(human.receipt.ok, true);
  assert.equal(children.length, 2);
  plan.socket.destroy();
  await once(plan.socket, "close");
  const mismatch = await connectGateway(listenPath, "codex:plan", "interaction-bound");
  assert.equal(mismatch.receipt.ok, false);
  assert.equal(mismatch.receipt.reason, "gateway.consumer-lane-mismatch");
  human.socket.destroy();
  mismatch.socket.destroy();
});

test("gateway rejects concurrent attachment and unauthorized consumers", async (context) => {
  const {gateway, listenPath} = fixture({authorize_client: ({consumer_id}) => consumer_id === "allowed"});
  await gateway.start();
  context.after(() => gateway.close());
  const first = await connectGateway(listenPath, "allowed", "plan-bound");
  const duplicate = await connectGateway(listenPath, "allowed", "plan-bound");
  const denied = await connectGateway(listenPath, "denied", "plan-bound");
  assert.equal(first.receipt.ok, true);
  assert.equal(duplicate.receipt.reason, "gateway.consumer-already-attached");
  assert.equal(denied.receipt.reason, "gateway.client-not-authorized");
  first.socket.destroy();
  duplicate.socket.destroy();
  denied.socket.destroy();
});

test("detached buffer overflow closes only the affected session", async (context) => {
  const {gateway, listenPath, children} = fixture({max_buffered_messages_per_client: 1});
  await gateway.start();
  context.after(() => gateway.close());
  const connection = await connectGateway(listenPath, "codex:plan", "plan-bound");
  connection.socket.destroy();
  await once(connection.socket, "close");
  await new Promise((resolveWait) => setTimeout(resolveWait, 20));
  children[0].stdout.write(`${JSON.stringify({method: "one"})}\n${JSON.stringify({method: "two"})}\n`);
  await new Promise((resolveWait) => setTimeout(resolveWait, 30));
  assert.equal(children[0].killed, true);
  assert.equal(gateway.inspect().sessions.length, 0);
});

test("disabled reconnect closes consumer state on disconnect", async (context) => {
  const {gateway, listenPath, children} = fixture({reconnect: false});
  await gateway.start();
  context.after(() => gateway.close());
  const first = await connectGateway(listenPath, "codex:plan", "plan-bound");
  first.socket.destroy();
  await once(first.socket, "close");
  await waitFor(() => gateway.inspect().sessions.length === 0, "non-reconnectable session close");
  const second = await connectGateway(listenPath, "codex:plan", "plan-bound");
  assert.equal(second.receipt.resumed, false);
  assert.equal(children.length, 2);
  second.socket.destroy();
});

test("upstream exit is visible and closes only its consumer session", async (context) => {
  const {gateway, listenPath, children} = fixture();
  await gateway.start();
  context.after(() => gateway.close());
  const connection = await connectGateway(listenPath, "codex:plan", "plan-bound");
  const errorLine = nextJsonLine(connection.socket, 2000, "upstream exit error");
  children[0].emit("exit", 17, null);
  const error = await errorLine;
  assert.equal(error.error.code, -32090);
  await waitFor(() => gateway.inspect().sessions.length === 0, "failed upstream cleanup");
});

test("stdio client adapter consumes the gateway handshake and forwards only app-server bytes", async (context) => {
  const {gateway, listenPath, children} = fixture();
  await gateway.start();
  context.after(() => gateway.close());
  const input = new PassThrough();
  const output = new PassThrough();
  const error = new PassThrough();
  const socket = runGatewayClientProxy({socket_path: listenPath, consumer_id: "codex:human-chat", lane: "interaction-bound", client_input: input, client_output: output, client_error: error});
  context.after(() => socket.destroy());
  await once(socket, "connect");
  await new Promise((resolveWait) => setTimeout(resolveWait, 20));
  const upstream = nextJsonLine(children[0].stdin);
  input.write(`${JSON.stringify({jsonrpc: "2.0", id: 9, method: "initialize", params: {}})}\n`);
  assert.equal((await upstream).id, 9);
  const downstream = nextJsonLine(output);
  children[0].stdout.write(`${JSON.stringify({id: 9, result: {ready: true}})}\n`);
  assert.equal((await downstream).result.ready, true);
});

test("programmatic RPC transport consumes the gateway handshake and exposes app-server bytes", async (context) => {
  const {gateway, listenPath, children} = fixture();
  await gateway.start();
  context.after(() => gateway.close());
  const transport = connectGatewayRpcTransport({socket_path: listenPath, consumer_id: "codex:human-chat", lane: "interaction-bound"});
  context.after(() => transport.close());
  const receipt = await transport.ready;
  assert.equal(receipt.ok, true);
  assert.equal(receipt.consumer_id, "codex:human-chat");
  const upstream = nextJsonLine(children[0].stdin);
  transport.input.write(`${JSON.stringify({jsonrpc: "2.0", id: 17, method: "initialize", params: {}})}\n`);
  assert.equal((await upstream).id, 17);
  const downstream = nextJsonLine(transport.output);
  children[0].stdout.write(`${JSON.stringify({jsonrpc: "2.0", id: 17, result: {ready: true}})}\n`);
  assert.deepEqual((await downstream).result, {ready: true});
});
