import {
  canonicalJson,
  canonicalizeJson,
  deepFreeze,
  sha256HexText,
} from "../intent-route-resolver/index.mjs";
import {
  createReasoningStateLedger,
  replayReasoningStateEpoch,
  sealReasoningStateEpoch,
} from "../reasoning-state-runtime/index.mjs";

export {createVariantWorkspaceFactory} from "./src/variant-workspace.mjs";
export {applyUpgradeDecision, createServingVersionStore} from "./src/upgrade-controller.mjs";
export {createEvolutionScheduler} from "./src/scheduler.mjs";

export const EVOLUTION_PROFILE_SCHEMA = "are.evolution-profile/v1";
export const IMPROVEMENT_SIGNAL_SCHEMA = "are.improvement-signal/v1";
export const IMPROVEMENT_TARGET_SCHEMA = "are.improvement-target/v1";
export const RESEARCH_RESULT_SCHEMA = "are.research-result/v1";
export const TECHNIQUE_CANDIDATE_SCHEMA = "are.technique-candidate/v1";
export const REPRODUCTION_TRIAL_SCHEMA = "are.reproduction-trial/v1";
export const ENGINE_VARIANT_SCHEMA = "are.engine-variant/v1";
export const VARIANT_COMPARISON_SCHEMA = "are.variant-comparison/v1";
export const UPGRADE_DECISION_SCHEMA = "are.upgrade-decision/v1";
export const EVOLUTION_CYCLE_SCHEMA = "are.evolution-cycle/v1";

const RECORD_PREFIX = new Map([
  [IMPROVEMENT_SIGNAL_SCHEMA, "improvement-signal"],
  [IMPROVEMENT_TARGET_SCHEMA, "improvement-target"],
  [RESEARCH_RESULT_SCHEMA, "research-result"],
  [TECHNIQUE_CANDIDATE_SCHEMA, "technique-candidate"],
  [REPRODUCTION_TRIAL_SCHEMA, "reproduction-trial"],
  [ENGINE_VARIANT_SCHEMA, "engine-variant"],
  [VARIANT_COMPARISON_SCHEMA, "variant-comparison"],
  [UPGRADE_DECISION_SCHEMA, "upgrade-decision"],
  [EVOLUTION_CYCLE_SCHEMA, "evolution-cycle"],
]);

function object(value) {
  return value !== null && typeof value === "object" && !Array.isArray(value);
}

function text(value) {
  return typeof value === "string" && value.trim().length > 0;
}

function finite(value) {
  return typeof value === "number" && Number.isFinite(value);
}

function freeze(value) {
  return deepFreeze(canonicalizeJson(value));
}

function digest(value) {
  return sha256HexText(canonicalJson(canonicalizeJson(value)));
}

function uniqueText(values) {
  return [...new Set((Array.isArray(values) ? values : []).filter(text).map((value) => value.trim()))].sort();
}

function fail(stage, reasonCodes, residue = []) {
  return freeze({
    schema_version: "are.evolution-failure/v1",
    ok: false,
    stage,
    reason_codes: uniqueText(reasonCodes),
    residue: Array.isArray(residue) ? residue : [],
    authority_effect: "none",
  });
}

function seal(schemaVersion, fields) {
  const prefix = RECORD_PREFIX.get(schemaVersion);
  if (!prefix) throw new TypeError(`Unsupported evolution record schema: ${schemaVersion}`);
  const material = canonicalizeJson({schema_version: schemaVersion, ...fields, authority_effect: "none"});
  const recordDigest = digest(material);
  return freeze({...material, record_id: `${prefix}:${recordDigest}`, record_digest: recordDigest});
}

function recordMaterial(record) {
  const {record_id: _id, record_digest: _digest, ...material} = record;
  return material;
}

export function verifyEvolutionRecord(record, expectedSchema = null) {
  const reasons = [];
  if (!object(record) || !RECORD_PREFIX.has(record.schema_version)) reasons.push("evolution.record-schema-invalid");
  if (expectedSchema !== null && record?.schema_version !== expectedSchema) reasons.push("evolution.record-schema-mismatch");
  const prefix = RECORD_PREFIX.get(record?.schema_version);
  if (prefix) {
    const expectedDigest = digest(recordMaterial(record));
    if (record.record_digest !== expectedDigest) reasons.push("evolution.record-digest-invalid");
    if (record.record_id !== `${prefix}:${expectedDigest}`) reasons.push("evolution.record-id-invalid");
  }
  if (record?.authority_effect !== "none") reasons.push("evolution.record-authority-invalid");
  return reasons.length > 0 ? fail("record-verification", reasons) : freeze({ok: true, value: record, authority_effect: "none"});
}

export function verifyEvolutionProfile(profile) {
  const reasons = [];
  if (!object(profile) || profile.schema_version !== EVOLUTION_PROFILE_SCHEMA) reasons.push("evolution.profile-schema-invalid");
  if (!text(profile?.profile_id)) reasons.push("evolution.profile-id-required");
  if (!object(profile?.research) || typeof profile.research.enabled !== "boolean" || !Number.isSafeInteger(profile.research.maximum_results_per_provider) || profile.research.maximum_results_per_provider < 1) reasons.push("evolution.profile-research-invalid");
  if (!object(profile?.target_selection) || !Number.isSafeInteger(profile.target_selection.minimum_signal_count) || profile.target_selection.minimum_signal_count < 1) reasons.push("evolution.profile-target-selection-invalid");
  if (!object(profile?.upgrade) || !["recommend-only", "controlled-local"].includes(profile.upgrade.mode) || !Number.isSafeInteger(profile.upgrade.required_keep_streak) || profile.upgrade.required_keep_streak < 1) reasons.push("evolution.profile-upgrade-invalid");
  if (profile?.authority_effect !== "none") reasons.push("evolution.profile-authority-invalid");
  return reasons.length > 0 ? fail("profile-verification", reasons) : freeze({ok: true, value: profile, authority_effect: "none"});
}

export function createImprovementSignal(input) {
  if (!object(input) || !text(input.kind) || !text(input.source_result_ref) || !text(input.scope)) throw new TypeError("Improvement signal requires kind, source_result_ref, and scope.");
  if (!finite(input.observed_value) && !text(input.observed_value)) throw new TypeError("Improvement signal requires a finite numeric or non-empty textual observed_value.");
  return seal(IMPROVEMENT_SIGNAL_SCHEMA, {
    kind: input.kind.trim(),
    source_result_ref: input.source_result_ref.trim(),
    scope: input.scope.trim(),
    observed_value: input.observed_value,
    expected_value: input.expected_value ?? null,
    metric: text(input.metric) ? input.metric.trim() : null,
    occurred_at: text(input.occurred_at) ? input.occurred_at.trim() : null,
    provenance_refs: uniqueText(input.provenance_refs),
    confidence: finite(input.confidence) ? input.confidence : null,
  });
}

export function createImprovementTarget(input) {
  if (!object(input) || !text(input.target_key) || !text(input.metric) || !["higher", "lower"].includes(input.direction) || !finite(input.threshold)) throw new TypeError("Improvement target requires target_key, metric, direction, and finite threshold.");
  const signalRefs = uniqueText(input.signal_refs);
  if (signalRefs.length === 0) throw new TypeError("Improvement target requires at least one signal_ref.");
  return seal(IMPROVEMENT_TARGET_SCHEMA, {
    target_key: input.target_key.trim(),
    signal_refs: signalRefs,
    metric: input.metric.trim(),
    direction: input.direction,
    baseline_ref: text(input.baseline_ref) ? input.baseline_ref.trim() : null,
    baseline_value: finite(input.baseline_value) ? input.baseline_value : null,
    threshold: input.threshold,
    priority: Number.isSafeInteger(input.priority) ? input.priority : 100,
    protected_metrics: canonicalizeJson(object(input.protected_metrics) ? input.protected_metrics : {}),
    test_sets: uniqueText(input.test_sets),
    mutation_allowlist: uniqueText(input.mutation_allowlist),
    invalidation_rules: uniqueText(input.invalidation_rules),
  });
}

export function createResearchResult(input) {
  if (!object(input) || !text(input.target_ref) || !text(input.provider_id) || !text(input.source_ref) || !text(input.source_version) || !text(input.mechanism)) throw new TypeError("Research result requires target, provider, source, version, and mechanism.");
  return seal(RESEARCH_RESULT_SCHEMA, {
    target_ref: input.target_ref.trim(),
    provider_id: input.provider_id.trim(),
    source_ref: input.source_ref.trim(),
    source_version: input.source_version.trim(),
    retrieved_at: text(input.retrieved_at) ? input.retrieved_at.trim() : null,
    mechanism: input.mechanism.trim(),
    evidence: uniqueText(input.evidence),
    counterevidence: uniqueText(input.counterevidence),
    limitations: uniqueText(input.limitations),
    fit_hypothesis: text(input.fit_hypothesis) ? input.fit_hypothesis.trim() : null,
  });
}

export function createTechniqueCandidate(input) {
  if (!object(input) || !text(input.target_ref) || !text(input.research_result_ref) || !text(input.mechanism) || !text(input.integration_point)) throw new TypeError("Technique candidate requires target, research result, mechanism, and integration point.");
  return seal(TECHNIQUE_CANDIDATE_SCHEMA, {
    target_ref: input.target_ref.trim(),
    research_result_ref: input.research_result_ref.trim(),
    mechanism: input.mechanism.trim(),
    integration_point: input.integration_point.trim(),
    required_dependencies: uniqueText(input.required_dependencies),
    expected_observations: uniqueText(input.expected_observations),
    limitations: uniqueText(input.limitations),
  });
}

export function createReproductionTrial(input) {
  if (!object(input) || !text(input.technique_ref) || !text(input.environment_ref) || !text(input.protocol_ref) || !["reproduced", "partially-reproduced", "not-reproduced", "not-evaluable"].includes(input.outcome)) throw new TypeError("Reproduction trial requires technique, environment, protocol, and a supported outcome.");
  return seal(REPRODUCTION_TRIAL_SCHEMA, {
    technique_ref: input.technique_ref.trim(),
    environment_ref: input.environment_ref.trim(),
    protocol_ref: input.protocol_ref.trim(),
    dependency_versions: canonicalizeJson(object(input.dependency_versions) ? input.dependency_versions : {}),
    expected_observations: uniqueText(input.expected_observations),
    actual_observations: uniqueText(input.actual_observations),
    deviations: uniqueText(input.deviations),
    outcome: input.outcome,
  });
}

export function createEngineVariant(input) {
  if (!object(input) || !text(input.baseline_ref) || !text(input.source_tree_digest) || !text(input.build_environment_ref)) throw new TypeError("Engine variant requires baseline, source tree digest, and build environment.");
  const techniqueRefs = uniqueText(input.technique_refs);
  const reproductionRefs = uniqueText(input.reproduction_refs);
  if (techniqueRefs.length === 0 || reproductionRefs.length === 0) throw new TypeError("Engine variant requires technique and reproduction references.");
  return seal(ENGINE_VARIANT_SCHEMA, {
    baseline_ref: input.baseline_ref.trim(),
    source_tree_digest: input.source_tree_digest.trim(),
    build_environment_ref: input.build_environment_ref.trim(),
    interface_version: text(input.interface_version) ? input.interface_version.trim() : "are-evolution/v1",
    technique_refs: techniqueRefs,
    reproduction_refs: reproductionRefs,
    changed_paths: uniqueText(input.changed_paths),
    change_digest: text(input.change_digest) ? input.change_digest.trim() : digest(uniqueText(input.changed_paths)),
  });
}

function metricsPass(direction, candidate, baseline, minimumDelta) {
  return direction === "lower" ? baseline - candidate >= minimumDelta : candidate - baseline >= minimumDelta;
}

export function createVariantComparison(input) {
  if (!object(input) || !text(input.variant_ref) || !text(input.baseline_ref) || !text(input.target_ref) || !text(input.manifest_ref) || !text(input.environment_ref)) throw new TypeError("Variant comparison requires variant, baseline, target, manifest, and environment references.");
  if (!object(input.fitness) || !["higher", "lower"].includes(input.fitness.direction) || !finite(input.fitness.minimum_delta)) throw new TypeError("Variant comparison requires a valid fitness rule.");
  if (!object(input.baseline_metrics) || !object(input.candidate_metrics)) throw new TypeError("Variant comparison requires baseline and candidate metrics.");
  const metric = input.fitness.target_metric;
  const baseline = input.baseline_metrics[metric];
  const candidate = input.candidate_metrics[metric];
  if (!text(metric) || !finite(baseline) || !finite(candidate)) throw new TypeError("Variant comparison target metric is missing from the metric vectors.");
  const reasons = [];
  if (!metricsPass(input.fitness.direction, candidate, baseline, input.fitness.minimum_delta)) reasons.push("fitness.target-not-improved");
  for (const [name, tolerance] of Object.entries(input.fitness.protected_quality ?? {})) {
    if (!finite(tolerance) || !finite(input.baseline_metrics[name]) || !finite(input.candidate_metrics[name]) || input.candidate_metrics[name] < input.baseline_metrics[name] - tolerance) reasons.push(`fitness.quality-regression:${name}`);
  }
  for (const [name, ratio] of Object.entries(input.fitness.maximum_regression_ratio ?? {})) {
    if (!finite(ratio) || !finite(input.baseline_metrics[name]) || !finite(input.candidate_metrics[name]) || input.candidate_metrics[name] > input.baseline_metrics[name] * (1 + ratio)) reasons.push(`fitness.performance-regression:${name}`);
  }
  if (input.safety_passed !== true) reasons.push("fitness.safety-failed");
  if (input.determinism_passed !== true) reasons.push("fitness.determinism-failed");
  if (input.holdout_passed !== true) reasons.push("fitness.holdout-failed");
  return seal(VARIANT_COMPARISON_SCHEMA, {
    variant_ref: input.variant_ref.trim(),
    baseline_ref: input.baseline_ref.trim(),
    target_ref: input.target_ref.trim(),
    manifest_ref: input.manifest_ref.trim(),
    environment_ref: input.environment_ref.trim(),
    baseline_metrics: canonicalizeJson(input.baseline_metrics),
    candidate_metrics: canonicalizeJson(input.candidate_metrics),
    fitness: canonicalizeJson(input.fitness),
    safety_passed: input.safety_passed === true,
    determinism_passed: input.determinism_passed === true,
    holdout_passed: input.holdout_passed === true,
    run_refs: uniqueText(input.run_refs),
    outcome: reasons.length === 0 ? "KEEP" : "REJECT",
    reason_codes: reasons.sort(),
  });
}

export function createUpgradeDecision(input) {
  if (!object(input) || !text(input.current_version_ref) || !text(input.candidate_version_ref) || !text(input.comparison_ref) || !["recommend-only", "controlled-local"].includes(input.mode)) throw new TypeError("Upgrade decision requires versions, comparison, and mode.");
  const eligible = input.comparison_outcome === "KEEP" && input.required_keep_streak_met === true && input.reproduction_passed === true && input.holdout_passed === true;
  const disposition = !eligible ? "retain-current" : input.mode === "recommend-only" ? "recommend-candidate" : input.activation_enabled === true ? "activate-candidate" : "block";
  return seal(UPGRADE_DECISION_SCHEMA, {
    current_version_ref: input.current_version_ref.trim(),
    candidate_version_ref: input.candidate_version_ref.trim(),
    comparison_ref: input.comparison_ref.trim(),
    mode: input.mode,
    required_keep_streak_met: input.required_keep_streak_met === true,
    reproduction_passed: input.reproduction_passed === true,
    holdout_passed: input.holdout_passed === true,
    activation_enabled: input.activation_enabled === true,
    disposition,
    predecessor_ref: input.current_version_ref.trim(),
    rollback_target_ref: input.current_version_ref.trim(),
    canary_policy_ref: text(input.canary_policy_ref) ? input.canary_policy_ref.trim() : null,
    reason_codes: !eligible ? ["upgrade.fitness-incomplete"] : disposition === "block" ? ["upgrade.activation-disabled"] : [],
  });
}

function targetMetricForSignal(signal, targetProfile) {
  return targetProfile.signal_kinds.includes(signal.kind) && (targetProfile.scope === undefined || targetProfile.scope === signal.scope);
}

export function selectImprovementTarget(signals, targetProfiles, options = {}) {
  if (!Array.isArray(signals) || !Array.isArray(targetProfiles)) return fail("target-selection", ["evolution.target-selection-input-invalid"]);
  const minimum = Number.isSafeInteger(options.minimum_signal_count) ? options.minimum_signal_count : 1;
  const candidates = [];
  for (const profile of targetProfiles) {
    if (!object(profile) || !text(profile.target_key) || !Array.isArray(profile.signal_kinds) || !text(profile.metric) || !["higher", "lower"].includes(profile.direction) || !finite(profile.threshold)) continue;
    const matching = signals.filter((signal) => verifyEvolutionRecord(signal, IMPROVEMENT_SIGNAL_SCHEMA).ok && targetMetricForSignal(signal, profile));
    if (matching.length < minimum) continue;
    candidates.push(createImprovementTarget({...profile, signal_refs: matching.map((signal) => signal.record_id)}));
  }
  candidates.sort((left, right) => left.priority - right.priority || left.target_key.localeCompare(right.target_key) || left.record_id.localeCompare(right.record_id));
  return freeze({ok: true, disposition: candidates.length === 0 ? "no-target" : "selected", target: candidates[0] ?? null, candidates, authority_effect: "none"});
}

export async function runResearchScout(target, providers, options = {}) {
  if (!verifyEvolutionRecord(target, IMPROVEMENT_TARGET_SCHEMA).ok) return fail("research-scout", ["evolution.target-invalid"]);
  if (options.enabled !== true) return freeze({ok: true, disposition: "disabled", results: [], provider_calls: 0, authority_effect: "none"});
  if (!Array.isArray(providers) || providers.length === 0) return freeze({ok: true, disposition: "no-providers", results: [], provider_calls: 0, authority_effect: "none"});
  const maximum = Number.isSafeInteger(options.maximum_results_per_provider) ? options.maximum_results_per_provider : 20;
  const ordered = [...providers].sort((left, right) => String(left.id).localeCompare(String(right.id)));
  const results = [];
  let providerCalls = 0;
  for (const provider of ordered) {
    if (!text(provider?.id) || typeof provider.search !== "function") return fail("research-scout", ["evolution.research-provider-invalid"]);
    providerCalls += 1;
    const rows = await provider.search(freeze({target, authority_effect: "none"}));
    if (!Array.isArray(rows)) return fail("research-scout", ["evolution.research-provider-result-invalid"]);
    for (const row of rows.slice(0, maximum)) results.push(createResearchResult({...row, target_ref: target.record_id, provider_id: provider.id}));
  }
  const unique = [...new Map(results.map((result) => [result.record_id, result])).values()].sort((left, right) => left.record_id.localeCompare(right.record_id));
  return freeze({ok: true, disposition: "completed", results: unique, provider_calls: providerCalls, authority_effect: "none"});
}

export function createEvolutionRuntime({profile, ledger = null, target_profiles = []} = {}) {
  const verified = verifyEvolutionProfile(profile);
  if (!verified.ok) throw new TypeError(`Invalid evolution profile: ${verified.reason_codes.join(",")}`);
  const stateLedger = ledger ?? createReasoningStateLedger({ledger_id: `are-evolution:${profile.profile_id}`});
  const records = new Map();

  function append(record) {
    const checked = verifyEvolutionRecord(record);
    if (!checked.ok) return checked;
    const event = stateLedger.append({
      event_kind: `evolution.${record.schema_version.split(".")[1]}`,
      idempotency_key: record.record_id,
      content: record,
      provenance_refs: uniqueText(record.provenance_refs),
    });
    if (!event.ok) return fail("evolution-append", event.reason_codes, event.residue);
    records.set(record.record_id, record);
    return freeze({ok: true, disposition: event.disposition, record, event: event.event, authority_effect: "none"});
  }

  function snapshot() {
    return freeze([...records.values()].sort((left, right) => left.record_id.localeCompare(right.record_id)));
  }

  function selectTarget() {
    const signals = snapshot().filter((record) => record.schema_version === IMPROVEMENT_SIGNAL_SCHEMA);
    const selected = selectImprovementTarget(signals, target_profiles, profile.target_selection);
    if (selected.ok && selected.target) append(selected.target);
    return selected;
  }

  function sealCycle(frontier = {}) {
    const epoch = sealReasoningStateEpoch(stateLedger, {consumer_ref: "are-evolution-runtime", frontier});
    if (!epoch.ok) return fail("cycle-seal", epoch.reason_codes, epoch.residue);
    const cycle = seal(EVOLUTION_CYCLE_SCHEMA, {profile_id: profile.profile_id, epoch_id: epoch.value.epoch_id, epoch_digest: epoch.value.epoch_digest, frontier: canonicalizeJson(frontier)});
    records.set(cycle.record_id, cycle);
    return freeze({ok: true, cycle, epoch: epoch.value, authority_effect: "none"});
  }

  function replay(cycle) {
    const checked = verifyEvolutionRecord(cycle, EVOLUTION_CYCLE_SCHEMA);
    if (!checked.ok) return checked;
    const replayed = replayReasoningStateEpoch(stateLedger, {schema_version: "are.reasoning-state-epoch/v1", ledger_id: stateLedger.inspect().ledger_id, consumer_ref: "are-evolution-runtime", request_ref: null, event_digests: stateLedger.snapshot().map((event) => event.event_digest), event_set_digest: digest(stateLedger.snapshot().map((event) => event.event_digest)), selected_dependencies: [], context_envelope_digest: null, frontier: cycle.frontier, authority_effect: "none", epoch_id: cycle.epoch_id, epoch_digest: cycle.epoch_digest});
    return replayed;
  }

  return Object.freeze({
    append,
    appendSignal: (input) => append(createImprovementSignal(input)),
    appendResearchResult: (input) => append(createResearchResult(input)),
    appendTechnique: (input) => append(createTechniqueCandidate(input)),
    appendReproduction: (input) => append(createReproductionTrial(input)),
    appendVariant: (input) => append(createEngineVariant(input)),
    appendComparison: (input) => append(createVariantComparison(input)),
    appendUpgradeDecision: (input) => append(createUpgradeDecision({...input, mode: input.mode ?? profile.upgrade.mode})),
    selectTarget,
    snapshot,
    sealCycle,
    replay,
    inspect: () => freeze({profile_id: profile.profile_id, record_count: records.size, ledger: stateLedger.inspect(), authority_effect: "none"}),
    ledger: stateLedger,
  });
}
