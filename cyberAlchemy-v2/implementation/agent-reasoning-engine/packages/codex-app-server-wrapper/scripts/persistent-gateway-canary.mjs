import {execFileSync, spawn} from "node:child_process";
import {mkdtempSync} from "node:fs";
import {createConnection, createServer} from "node:net";
import {resolve} from "node:path";

import {
  createCodexAppServerWrapper,
  createPersistentGateway,
  GATEWAY_CONNECT_SCHEMA,
  loadRepositoryProfile,
  protocolBindingCheck,
} from "../index.mjs";

const packageRoot = resolve(import.meta.dirname, "..");
const repositoryRoot = resolve(packageRoot, "../../../../..");
const profilePath = resolve(packageRoot, "profiles/repository-v1.json");
const temporaryRoot = mkdtempSync("/tmp/are-persistent-canary-");
const gatewaySocket = resolve(temporaryRoot, "are-gateway.sock");

async function availablePort() {
  const server = createServer();
  await new Promise((resolveListen, reject) => {
    server.once("error", reject);
    server.listen(0, "127.0.0.1", resolveListen);
  });
  const port = server.address().port;
  await new Promise((resolveClose) => server.close(resolveClose));
  return port;
}

async function waitForPort(port) {
  const deadline = Date.now() + 15000;
  while (Date.now() < deadline) {
    const connected = await new Promise((resolveResult) => {
      const socket = createConnection({host: "127.0.0.1", port});
      socket.once("connect", () => { socket.destroy(); resolveResult(true); });
      socket.once("error", () => resolveResult(false));
    });
    if (connected) return;
    await new Promise((resolveWait) => setTimeout(resolveWait, 50));
  }
  throw new Error("upstream-websocket-listener:timeout");
}

function bounded(promise, label, milliseconds = 300000) {
  return new Promise((resolveValue, reject) => {
    const timer = setTimeout(() => reject(new Error(`${label}:timeout`)), milliseconds);
    promise.then((value) => { clearTimeout(timer); resolveValue(value); }, (error) => { clearTimeout(timer); reject(error); });
  });
}

async function waitFor(predicate, label, milliseconds = 15000) {
  const deadline = Date.now() + milliseconds;
  while (Date.now() < deadline) {
    if (predicate()) return;
    await new Promise((resolveWait) => setTimeout(resolveWait, 50));
  }
  throw new Error(`${label}:timeout`);
}

async function connectClient(consumerId, lane) {
  const socket = createConnection(gatewaySocket);
  const messages = [];
  const waiters = [];
  const pending = new Map();
  let sequence = 0;
  let buffer = "";
  socket.on("data", (chunk) => {
    buffer += chunk.toString("utf8");
    let index;
    while ((index = buffer.indexOf("\n")) >= 0) {
      const message = JSON.parse(buffer.slice(0, index));
      buffer = buffer.slice(index + 1);
      messages.push(message);
      for (const waiter of [...waiters]) {
        if (!waiter.predicate(message)) continue;
        waiters.splice(waiters.indexOf(waiter), 1);
        waiter.resolve(message);
      }
      if (message.method?.endsWith("/requestApproval")) {
        const result = message.method === "item/permissions/requestApproval" ? {permissions: {}} : {decision: "decline"};
        socket.write(`${JSON.stringify({jsonrpc: "2.0", id: message.id, result})}\n`);
      }
      if (Object.hasOwn(message, "id") && pending.has(String(message.id))) {
        const request = pending.get(String(message.id));
        pending.delete(String(message.id));
        if (message.error) request.reject(new Error(`${request.method}:${JSON.stringify(message.error)}`));
        else request.resolve(message.result);
      }
    }
  });
  await bounded(new Promise((resolveConnect, reject) => {
    socket.once("connect", resolveConnect);
    socket.once("error", reject);
  }), `${consumerId}:connect`, 15000);
  socket.write(`${JSON.stringify({schema_version: GATEWAY_CONNECT_SCHEMA, consumer_id: consumerId, lane})}\n`);
  const receipt = await bounded(waitMessage((message) => message.schema_version === "are.codex-gateway-connected/v1"), `${consumerId}:handshake`, 15000);

  function request(method, params) {
    const id = ++sequence;
    socket.write(`${JSON.stringify({jsonrpc: "2.0", id, method, params})}\n`);
    return new Promise((resolveValue, reject) => pending.set(String(id), {resolve: resolveValue, reject, method}));
  }

  function waitMessage(predicate) {
    const existing = messages.find(predicate);
    if (existing) return Promise.resolve(existing);
    return new Promise((resolveValue) => waiters.push({predicate, resolve: resolveValue}));
  }

  return {socket, receipt, request, waitMessage, messages};
}

async function runTurn(client, threadId, text, label) {
  const started = await bounded(client.request("turn/start", {
    threadId,
    input: [{type: "text", text}],
    approvalPolicy: "never",
    sandboxPolicy: {type: "readOnly", networkAccess: false},
  }), `${label}:turn-start`);
  const turnId = started.turn.id;
  await bounded(client.waitMessage((message) => message.method === "turn/completed" && message.params?.turn?.id === turnId), `${label}:turn-completed`);
  await bounded(client.waitMessage((message) => message.method === "cyberalchemy/decision" && message.params?.directive_kind === "complete" && message.params?.completion_digest), `${label}:decision`);
  return turnId;
}

function contextView(gateway, consumerId) {
  const session = gateway.inspect().sessions.find((item) => item.consumer_id === consumerId);
  return session?.wrapper_state?.current_context_epochs?.[0]?.view_id ?? null;
}

let observedVersion = "unavailable";
try { observedVersion = execFileSync("codex", ["--version"], {encoding: "utf8"}).trim(); } catch {}
const loaded = loadRepositoryProfile(profilePath, repositoryRoot);
if (!loaded.ok) throw new Error(`repository-profile:${loaded.reason_codes.join(",")}`);
const binding = protocolBindingCheck(loaded.value.protocol_binding, observedVersion);
let upstream = null;
let gateway = null;
let upstreamStderr = "";
let gatewayStderr = "";
let output;

try {
  if (!binding.ok) throw new Error(`protocol-binding:${binding.reason_codes.join(",")}`);
  const upstreamPort = await availablePort();
  const upstreamUrl = `ws://127.0.0.1:${upstreamPort}`;
  upstream = spawn("codex", ["app-server", "--listen", upstreamUrl], {stdio: ["ignore", "ignore", "pipe"]});
  upstream.stderr.on("data", (chunk) => { upstreamStderr += chunk; });
  await waitForPort(upstreamPort);
  const allowed = new Map(loaded.value.gateway.allowed_clients.map((client) => [client.consumer_id, client]));
  gateway = createPersistentGateway({
    listen_path: gatewaySocket,
    backend: {mode: "websocket", url: upstreamUrl},
    max_clients: loaded.value.gateway.max_clients,
    max_buffered_messages_per_client: loaded.value.gateway.max_buffered_messages_per_client,
    reconnect: true,
    authorize_client: ({consumer_id, lane}) => allowed.get(consumer_id)?.lane === lane,
    on_backend_stderr: (chunk) => { gatewayStderr += chunk; },
    wrapper_factory: ({consumer_id, lane}) => {
      const profile = structuredClone(loaded.value);
      profile.turn_bindings.default = {
        ...profile.turn_bindings.default,
        lane,
        consumer_ref: consumer_id,
        ...(lane === "plan-bound" ? {window_ref: allowed.get(consumer_id).window_ref, request_id: allowed.get(consumer_id).request_id} : {}),
      };
      return createCodexAppServerWrapper({
        loaded_profile: profile,
        decision_profile: loaded.decision_profile,
        definition_catalog: loaded.definition_catalog,
        ontology_snapshot: loaded.ontology_snapshot,
        source_snapshot: loaded.source_snapshot,
        context_source_provider: loaded.context_source_provider,
        semantic_profile: loaded.semantic_profile,
      });
    },
  });
  await gateway.start();

  const plan = await connectClient("codex:plan", "plan-bound");
  await bounded(plan.request("initialize", {clientInfo: {name: "are-persistent-plan-canary", version: "0.1.0"}, capabilities: {experimentalApi: true}}), "plan:initialize");
  const planThread = await bounded(plan.request("thread/start", {cwd: "/tmp", ephemeral: true, model: "gpt-5.6-sol", approvalPolicy: "never", sandbox: "read-only"}), "plan:thread-start");
  const stablePlanPrompt = "Research Context Envelope provenance and answer in one sentence. Do not use tools.";
  const planTurn1 = await runTurn(plan, planThread.thread.id, stablePlanPrompt, "plan:first");
  const planView1 = contextView(gateway, "codex:plan");
  plan.socket.destroy();
  await waitFor(() => gateway.inspect().sessions.find((item) => item.consumer_id === "codex:plan")?.attached === false, "plan-detach");
  const resumedPlan = await connectClient("codex:plan", "plan-bound");
  const planTurn2 = await runTurn(resumedPlan, planThread.thread.id, stablePlanPrompt, "plan:second");
  const planView2 = contextView(gateway, "codex:plan");

  const human = await connectClient("codex:human-chat", "interaction-bound");
  await bounded(human.request("initialize", {clientInfo: {name: "are-persistent-human-canary", version: "0.1.0"}, capabilities: {experimentalApi: true}}), "human:initialize");
  const humanThread = await bounded(human.request("thread/start", {cwd: "/tmp", ephemeral: true, model: "gpt-5.6-sol", approvalPolicy: "never", sandbox: "read-only"}), "human:thread-start");
  const humanTurn1 = await runTurn(human, humanThread.thread.id, "Research Context Envelope provenance and answer in one sentence. Do not use tools.", "human:first");
  const humanView1 = contextView(gateway, "codex:human-chat");
  const humanTurn2 = await runTurn(human, humanThread.thread.id, "Research Context Envelope freshness and answer in one sentence. Do not use tools.", "human:second");
  const humanView2 = contextView(gateway, "codex:human-chat");

  const effectRequests = [...plan.messages, ...resumedPlan.messages, ...human.messages].filter((message) => message.method?.endsWith("/requestApproval")).length;
  const semanticNotifications = [...plan.messages, ...resumedPlan.messages, ...human.messages].filter((message) => message.method === "cyberalchemy/semantic").length;
  const passed = plan.receipt.resumed === false
    && resumedPlan.receipt.resumed === true
    && planView1 === planView2
    && humanView1 !== humanView2
    && effectRequests === 0
    && semanticNotifications === 0;
  output = {
    schema_version: "are.codex-persistent-gateway-live-canary/v1",
    status: passed ? "PASS" : "FAIL",
    observed_codex_version: observedVersion,
    protocol_binding: "matched",
    backend_mode: "websocket-isolated-canary",
    plan_bound: {thread_id: planThread.thread.id, turn_ids: [planTurn1, planTurn2], reconnected: resumedPlan.receipt.resumed, context_view_identity_reused: planView1 === planView2},
    interaction_bound: {thread_id: humanThread.thread.id, turn_ids: [humanTurn1, humanTurn2], context_view_identity_succeeded: humanView1 !== humanView2},
    consumer_sessions: gateway.inspect().sessions.length,
    effect_requests: effectRequests,
    semantic_notifications: semanticNotifications,
    authority_effect: "none",
    claim_limit: "Controlled ephemeral local persistent-gateway canary only; no Desktop integration, daemon installation, admission, conformance, publication, deployment, or external-effect authority.",
  };
  resumedPlan.socket.destroy();
  human.socket.destroy();
} catch (error) {
  output = {schema_version: "are.codex-persistent-gateway-live-canary/v1", status: "FAIL", error: error.message, observed_codex_version: observedVersion, authority_effect: "none"};
} finally {
  if (gateway) await gateway.close();
  if (upstream) upstream.kill("SIGTERM");
}

output.stderr = [...gatewayStderr.split("\n"), ...upstreamStderr.split("\n")].filter(Boolean).slice(-20);
process.stdout.write(`${JSON.stringify(output, null, 2)}\n`);
process.exitCode = output.status === "PASS" ? 0 : 1;
