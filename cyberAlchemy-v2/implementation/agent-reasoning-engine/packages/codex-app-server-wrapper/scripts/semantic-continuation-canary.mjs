import {execFileSync} from "node:child_process";
import {dirname, resolve} from "node:path";
import {createInterface} from "node:readline";
import {PassThrough} from "node:stream";
import {fileURLToPath} from "node:url";

import {
  createCodexAppServerWrapper,
  loadRepositoryProfile,
  protocolBindingCheck,
  runStdioProxy,
} from "../index.mjs";
import {composeSemanticLifecycle, loadSemanticInputProfile} from "../../semantic-input-runtime/index.mjs";
import {digestValue} from "../../semantic-judgment-evaluator/index.mjs";

const packageRoot = resolve(dirname(fileURLToPath(import.meta.url)), "..");
const repositoryRoot = resolve(packageRoot, "../../../../..");
const profilePath = resolve(packageRoot, "profiles/repository-v1.json");
const semanticProfilePath = resolve(packageRoot, "test/fixtures/semantic/profile.json");
const SCENARIOS = ["recommended", "insufficient", "owner-escalation", "tampered", "disabled", "interaction-precedence"];

function semanticInput() {
  const value = {purchase_age_days: 12, purchase_amount: 75, receipt_present: true, fraud_hold: false, final_sale: false};
  const sourceDigest = digestValue(value);
  return {
    owner_ref: "commerce-policy-owner@local",
    created_at: "2026-07-23T12:00:00.000Z",
    as_of: "2026-07-23T12:05:00.000Z",
    observation_sources: [{source_ref: "fixture://wrapper/refund-case", value, digest: sourceDigest}],
    observation_candidates: Object.entries(value).map(([field, fieldValue], index) => ({
      schema_version: "are.observation-candidate/v1",
      candidate_id: `canary:candidate:${String(index + 1).padStart(2, "0")}`,
      field,
      value: fieldValue,
      issuer_ref: "commerce-policy-owner@local",
      source_ref: "fixture://wrapper/refund-case",
      source_digest: sourceDigest,
      validator_ref: "wrapper-fixture-validator@1",
      temporal_scope: {observed_at: "2026-07-23T12:05:00.000Z"},
      proposed_posture: "admitted",
    })),
    challenge_state: {required_lanes: [{lane_id: "owner-policy-challenge", status: "closed", attempt_count: 1}]},
  };
}

function planProposal(threadId, scenario) {
  return {
    proposal_id: `canary:${scenario}:successor`,
    declared_plan_digest: `canary-plan:${scenario}`,
    action_ref: "validate-canary-result",
    route_id: "CA2-ROUTE-VALIDATE",
    objective_kind: "validate",
    effect_classes: ["non-effectful-validate"],
    reversible: true,
    evidence_refs: [`canary:${scenario}`],
    semantic_dependency: {required: true, binding_id: "semantic-domain:wrapper-refund-test@1"},
    next_turn: {params: {threadId, input: [{type: "text", text: "Validate in one sentence that this is a bounded non-authorizing canary result. Do not use tools."}]}},
  };
}

function expected(scenario) {
  if (scenario === "recommended") return {semantic: "RecommendedUnderSnapshot", directive: "direct", successors: 1};
  if (scenario === "insufficient") return {semantic: "Deferred.Insufficient", directive: "block", successors: 0};
  if (scenario === "owner-escalation") return {semantic: "EscalateOwner", directive: "gate", successors: 0};
  if (scenario === "tampered") return {semantic: null, semantic_disposition: "block", directive: "block", successors: 0};
  if (scenario === "disabled") return {semantic_notifications: 0, directive: "direct", successors: 1};
  return {semantic: "RecommendedUnderSnapshot", directive: "gate", successors: 0};
}

function bounded(waiters, predicate, label, milliseconds = 300000) {
  const existing = waiters.messages.find(predicate);
  if (existing) return Promise.resolve(existing);
  return new Promise((resolvePromise, reject) => {
    const timer = setTimeout(() => reject(new Error(`${label}:timeout`)), milliseconds);
    waiters.pending.push({
      predicate,
      resolve: (value) => { clearTimeout(timer); resolvePromise(value); },
    });
  });
}

async function runScenario(scenario, loaded, semanticProfile, observedVersion) {
  const profile = structuredClone(loaded.value);
  profile.semantic_evaluation = {enabled: scenario !== "disabled", trigger: "turn/completed"};
  let primaryTurnId = null;
  let evaluatorCalls = 0;
  const provider = () => {
    const input = semanticInput();
    if (scenario === "insufficient") input.observation_candidates = input.observation_candidates.filter((candidate) => candidate.field !== "receipt_present");
    if (scenario === "owner-escalation") input.challenge_state.material_disputes = [{dispute_id: "canary-owner", status: "open"}];
    return input;
  };
  const lifecycle = (input) => {
    evaluatorCalls += 1;
    const result = composeSemanticLifecycle(input);
    if (scenario !== "tampered" || !result.ok) return result;
    const reasoningReceipt = {...result.reasoning_receipt, terminal_outcome: "Deferred.Insufficient"};
    return {...result, reasoning_receipt: reasoningReceipt, reasoning_receipt_exact_bytes_digest: digestValue(reasoningReceipt)};
  };
  const wrapper = createCodexAppServerWrapper({
    loaded_profile: profile,
    decision_profile: loaded.decision_profile,
    definition_catalog: loaded.definition_catalog,
    ontology_snapshot: loaded.ontology_snapshot,
    source_snapshot: loaded.source_snapshot,
    context_source_provider: loaded.context_source_provider,
    semantic_profile: scenario === "disabled" ? null : semanticProfile,
    semantic_input_provider: provider,
    semantic_lifecycle: lifecycle,
    continuation_provider: ({message}) => {
      if (message.params?.turn?.id !== primaryTurnId) return {plan_bound: [], interaction_bound: []};
      const proposal = planProposal(message.params.threadId, scenario);
      if (scenario === "interaction-precedence") {
        return {plan_bound: [proposal], interaction_bound: [{proposal_id: "canary:interaction", attributed_to: "human:canary", proposal_text: "Review before continuing.", evidence_refs: ["canary:interaction"]}]};
      }
      return {plan_bound: [proposal], interaction_bound: []};
    },
  });

  const clientInput = new PassThrough();
  const clientOutput = new PassThrough();
  const clientError = new PassThrough();
  const child = runStdioProxy({wrapper, client_input: clientInput, client_output: clientOutput, client_error: clientError});
  const waiters = {messages: [], pending: []};
  const pendingRequests = new Map();
  let sequence = 0;
  let stderr = "";
  clientError.on("data", (chunk) => { stderr += chunk; });
  createInterface({input: clientOutput, crlfDelay: Infinity}).on("line", (line) => {
    const message = JSON.parse(line);
    waiters.messages.push(message);
    for (const waiter of [...waiters.pending]) {
      if (!waiter.predicate(message)) continue;
      waiters.pending.splice(waiters.pending.indexOf(waiter), 1);
      waiter.resolve(message);
    }
    if (message.method?.endsWith("/requestApproval")) {
      const denial = message.method === "item/permissions/requestApproval" ? {permissions: {}} : {decision: "decline"};
      clientInput.write(`${JSON.stringify({jsonrpc: "2.0", id: message.id, result: denial})}\n`);
    }
    if (Object.hasOwn(message, "id") && pendingRequests.has(String(message.id))) {
      const pending = pendingRequests.get(String(message.id));
      pendingRequests.delete(String(message.id));
      if (message.error) pending.reject(new Error(`${pending.method}:${JSON.stringify(message.error)}`));
      else pending.resolve(message.result);
    }
  });

  function request(method, params) {
    const id = ++sequence;
    clientInput.write(`${JSON.stringify({jsonrpc: "2.0", id, method, params})}\n`);
    return new Promise((resolvePromise, reject) => pendingRequests.set(String(id), {resolve: resolvePromise, reject, method}));
  }

  let result;
  try {
    await request("initialize", {clientInfo: {name: `are-semantic-canary-${scenario}`, version: "0.1.0"}, capabilities: {experimentalApi: true}});
    const started = await request("thread/start", {cwd: "/tmp", ephemeral: true, model: "gpt-5.6-sol", approvalPolicy: "never", sandbox: "read-only"});
    const turn = await request("turn/start", {
      threadId: started.thread.id,
      input: [{type: "text", text: "Research whether this exact refund case is eligible. Answer in one sentence and do not use tools."}],
      approvalPolicy: "never",
      sandboxPolicy: {type: "readOnly", networkAccess: false},
    });
    primaryTurnId = turn.turn.id;
    await bounded(waiters, (message) => message.method === "turn/completed" && message.params?.turn?.id === primaryTurnId, `${scenario}:primary-completion`);
    const semantic = scenario === "disabled" ? null : await bounded(waiters, (message) => message.method === "cyberalchemy/semantic", `${scenario}:semantic`);
    const directive = await bounded(waiters, (message) => message.method === "cyberalchemy/decision" && message.params?.completion_digest, `${scenario}:directive`);
    let successorTurns = 0;
    if (directive.params.directive_kind === "direct") {
      await bounded(waiters, (message) => message.method === "cyberalchemy/successor" && message.params?.kind === "started", `${scenario}:successor-started`);
      const successorResponse = await bounded(waiters, (message) => message.method === "cyberalchemy/successor" && message.params?.kind === "turn-start-response", `${scenario}:successor-response`);
      const successorTurnId = successorResponse.params.response?.result?.turn?.id;
      if (successorTurnId) {
        await bounded(waiters, (message) => message.method === "turn/completed" && message.params?.turn?.id === successorTurnId, `${scenario}:successor-completion`);
        successorTurns = 1;
      }
    }
    const exp = expected(scenario);
    const semanticNotifications = waiters.messages.filter((message) => message.method === "cyberalchemy/semantic").length;
    const effectRequests = waiters.messages.filter((message) => message.method?.endsWith("/requestApproval")).length;
    const pass = directive.params.directive_kind === exp.directive
      && successorTurns === exp.successors
      && effectRequests === 0
      && (exp.semantic_notifications === undefined || semanticNotifications === exp.semantic_notifications)
      && (exp.semantic_disposition === undefined || semantic?.params?.disposition === exp.semantic_disposition)
      && (exp.semantic === undefined || semantic?.params?.semantic_outcome === exp.semantic);
    const journalCutDigests = waiters.messages.filter((message) => message.method === "cyberalchemy/semantic").map((message) => message.params?.reasoning_receipt_binding?.runtime_journal_cut_digest).filter(Boolean);
    result = {
      scenario,
      status: pass ? "PASS" : "FAIL",
      observed_codex_version: observedVersion,
      thread_id: started.thread.id,
      primary_turn_id: primaryTurnId,
      semantic_disposition: semantic?.params?.disposition ?? "disabled",
      semantic_outcome: semantic?.params?.semantic_outcome ?? null,
      reasoning_receipt_digest: semantic?.params?.reasoning_receipt_digest ?? null,
      journal_cut_digest: journalCutDigests[0] ?? null,
      directive_kind: directive.params.directive_kind,
      reason_codes: directive.params.reason_codes,
      successor_turns: successorTurns,
      evaluator_calls: evaluatorCalls,
      effect_requests: effectRequests,
      authority_effect: "none",
    };
  } catch (error) {
    result = {scenario, status: "FAIL", error: error.message, observed_codex_version: observedVersion, authority_effect: "none"};
  } finally {
    child.kill("SIGKILL");
    clientInput.end();
  }
  result.stderr = stderr.split("\n").filter(Boolean).slice(-10);
  return result;
}

const loaded = loadRepositoryProfile(profilePath, repositoryRoot);
if (!loaded.ok) throw new Error(`repository-profile:${loaded.reason_codes.join(",")}`);
const semanticLoaded = loadSemanticInputProfile(semanticProfilePath, repositoryRoot);
if (!semanticLoaded.ok) throw new Error(`semantic-profile:${semanticLoaded.reason_codes.join(",")}`);
let observedVersion = "unavailable";
try {
  observedVersion = execFileSync("codex", ["--version"], {encoding: "utf8"}).trim();
} catch {
  observedVersion = "unavailable";
}
const binding = protocolBindingCheck(loaded.value.protocol_binding, observedVersion);
let results = [];
if (binding.ok) {
  for (const scenario of SCENARIOS) results.push(await runScenario(scenario, loaded, semanticLoaded.value, observedVersion));
}
const output = {
  schema_version: "are.codex-semantic-continuation-live-canary/v1",
  status: binding.ok && results.every((item) => item.status === "PASS") ? "PASS" : "FAIL",
  observed_codex_version: observedVersion,
  protocol_binding: binding.ok ? "matched" : "blocked-version-drift",
  scenarios: results,
  authority_effect: "none",
  claim_limit: "Controlled ephemeral local canary only; no acceptance, admission, conformance, publication, deployment, or external-effect authority.",
};
process.stdout.write(`${JSON.stringify(output, null, 2)}\n`);
process.exitCode = output.status === "PASS" ? 0 : 1;
