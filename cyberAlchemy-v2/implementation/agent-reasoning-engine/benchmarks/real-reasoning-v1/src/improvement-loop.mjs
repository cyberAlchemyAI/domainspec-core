import {readFileSync} from "node:fs";
import {resolve} from "node:path";

import {runCoreBenchmark} from "./core.mjs";
import {runIntegrationBenchmark} from "./integration.mjs";
import {ratio, repositoryRoot, sha256} from "./common.mjs";

function allCases(evidence) {
  return [
    ...(evidence.core.cases.routing ?? []),
    ...(evidence.core.cases.context ?? []),
    ...(evidence.integration.cases.lifecycle ?? []),
    ...(evidence.integration.cases.failure_safety ?? []),
  ];
}

function caseRate(evidence, ids) {
  const selected = allCases(evidence).filter((entry) => ids.includes(entry.scenario_id));
  return ratio(selected.filter((entry) => entry.passed).length, selected.length);
}

export function scoreVector(evidence) {
  const failure = evidence.integration.cases.failure_safety ?? [];
  const lifecycle = evidence.integration.cases.lifecycle ?? [];
  return {
    safety: {
      failure_safety_rate: ratio(failure.filter((entry) => entry.passed).length, failure.length),
      lifecycle_rate: ratio(lifecycle.filter((entry) => entry.passed).length, lifecycle.length),
      false_direct_ambiguities: evidence.core.summary.false_direct_ambiguities,
      determinism_mismatches: evidence.core.summary.determinism_mismatches,
      authority_violations: 0
    },
    quality: {
      route_accuracy: evidence.core.summary.route_accuracy,
      definition_recall: evidence.core.summary.definition_recall,
      context_precision: evidence.core.summary.context_precision
    },
    performance: {
      route_p95_ms: evidence.core.metrics.route.p95_ms,
      request_selection_p95_ms: evidence.core.metrics.request_selection.p95_ms,
      preflight_p95_ms: evidence.core.metrics.preflight.p95_ms
    }
  };
}

export function targetValue(evidence, target) {
  if (target.metric === "case_pass_rate") return caseRate(evidence, target.case_ids);
  if (Object.hasOwn(evidence.core.summary, target.metric)) return evidence.core.summary[target.metric];
  if (target.metric === "route_p95_ms") return evidence.core.metrics.route.p95_ms;
  throw new Error(`Unsupported improvement metric: ${target.metric}`);
}

export async function collectImprovementEvidence(benchmark, options = {}) {
  const fast = options.fast === true;
  const sampling = benchmark.profile.improvement_loop.fast_sampling;
  const coreOptions = fast ? {...sampling, enforce_performance: false} : {};
  const core = await runCoreBenchmark(benchmark, coreOptions);
  const integration = await runIntegrationBenchmark(benchmark);
  return {sampling_mode: fast ? "fast" : "full", core, integration};
}

export function diagnoseEvidence(benchmark, evidence) {
  const targets = benchmark.profile.improvement_loop.targets;
  return Object.entries(targets).map(([targetId, target]) => {
    const value = targetValue(evidence, target);
    const failedCases = allCases(evidence).filter((entry) => target.case_ids.includes(entry.scenario_id) && !entry.passed).map((entry) => entry.scenario_id);
    const threshold = target.metric === "route_accuracy" ? benchmark.profile.thresholds.route_accuracy
      : target.metric === "context_precision" ? benchmark.profile.thresholds.context_precision
      : target.metric === "route_p95_ms" ? benchmark.profile.thresholds.route_p95_ms
      : 1;
    const meetsTarget = target.direction === "lower" ? value <= threshold : value >= threshold;
    return {target_id: targetId, priority: target.priority, metric: target.metric, value, threshold, meets_target: meetsTarget, failed_cases: failedCases, classification: targetId === "routing-accuracy" ? "mixed-engine-and-oracle-review" : "candidate-engine-defect", mutation_allowlist: target.mutation_allowlist};
  }).sort((a, b) => Number(a.meets_target) - Number(b.meets_target) || a.priority - b.priority);
}

function safetyComparison(baseline, candidate) {
  return {
    failure_safety: candidate.safety.failure_safety_rate === 1 && candidate.safety.failure_safety_rate >= baseline.safety.failure_safety_rate,
    lifecycle: candidate.safety.lifecycle_rate === 1 && candidate.safety.lifecycle_rate >= baseline.safety.lifecycle_rate,
    ambiguity: candidate.safety.false_direct_ambiguities <= baseline.safety.false_direct_ambiguities && candidate.safety.false_direct_ambiguities === 0,
    determinism: candidate.safety.determinism_mismatches <= baseline.safety.determinism_mismatches && candidate.safety.determinism_mismatches === 0,
    authority: candidate.safety.authority_violations <= baseline.safety.authority_violations && candidate.safety.authority_violations === 0
  };
}

export function compareCandidate(profile, targetId, baselineEvidence, candidateEvidence) {
  const loop = profile.improvement_loop;
  const target = loop.targets[targetId];
  if (!target) throw new Error(`Unknown target: ${targetId}`);
  if (baselineEvidence.sampling_mode !== candidateEvidence.sampling_mode) return {keep: false, reason_codes: ["improvement.sampling-mode-mismatch"]};
  const baseline = scoreVector(baselineEvidence);
  const candidate = scoreVector(candidateEvidence);
  const safety = safetyComparison(baseline, candidate);
  const baselineTarget = targetValue(baselineEvidence, target);
  const candidateTarget = targetValue(candidateEvidence, target);
  const delta = target.direction === "lower" ? baselineTarget - candidateTarget : candidateTarget - baselineTarget;
  const threshold = target.metric === "route_accuracy" ? profile.thresholds.route_accuracy
    : target.metric === "context_precision" ? profile.thresholds.context_precision
    : target.metric === "route_p95_ms" ? profile.thresholds.route_p95_ms
    : 1;
  const targetAlreadyMet = target.direction === "lower" ? baselineTarget <= threshold : baselineTarget >= threshold;
  const targetImproved = delta >= loop.minimum_quality_delta || (targetAlreadyMet && delta >= 0);
  const qualityChecks = Object.fromEntries(Object.entries(candidate.quality).map(([metric, value]) => [metric, metric === target.metric || value >= baseline.quality[metric] - loop.non_target_quality_tolerance]));
  const performanceChecks = Object.fromEntries(Object.entries(candidate.performance).map(([metric, value]) => [metric, candidateEvidence.sampling_mode === "fast" || metric === target.metric || value <= baseline.performance[metric] * (1 + loop.latency_regression_ratio)]));
  const reasonCodes = [];
  if (!Object.values(safety).every(Boolean)) reasonCodes.push("improvement.safety-regression");
  if (!targetImproved) reasonCodes.push("improvement.target-not-improved");
  if (!Object.values(qualityChecks).every(Boolean)) reasonCodes.push("improvement.non-target-quality-regression");
  if (!Object.values(performanceChecks).every(Boolean)) reasonCodes.push("improvement.latency-regression");
  return {keep: reasonCodes.length === 0, reason_codes: reasonCodes, target: {target_id: targetId, metric: target.metric, direction: target.direction, baseline: baselineTarget, candidate: candidateTarget, delta}, safety_checks: safety, quality_checks: qualityChecks, performance_checks: performanceChecks, baseline_score: baseline, candidate_score: candidate};
}

function mutationSnapshot(target) {
  return target.mutation_allowlist.map((path) => {
    const absolute = resolve(repositoryRoot, path);
    if (!absolute.startsWith(`${repositoryRoot}/`)) throw new Error(`Mutation path escapes repository: ${path}`);
    try { return {path, sha256: sha256(readFileSync(absolute))}; }
    catch { return {path, sha256: null, unreadable: true}; }
  });
}

function iteration(mode, targetId, status, fields = {}) {
  const identity = {mode, target_id: targetId, created_at: new Date().toISOString(), evidence_digest: sha256(fields.evidence ?? fields.comparison ?? fields)};
  return {schema_version: "are.reasoning-improvement-iteration/v1", iteration_id: `are-improvement:${sha256(identity)}`, ...identity, status, ...fields, authority_effect: "none", claim_limit: "Candidate improvement evidence only; no source mutation, acceptance, conformance, publication, deployment, or effect authority."};
}

export async function diagnoseImprovement(benchmark, options = {}) {
  const evidence = await collectImprovementEvidence(benchmark, options);
  const findings = diagnoseEvidence(benchmark, evidence);
  return iteration("diagnose", null, "DIAGNOSED", {sampling_mode: evidence.sampling_mode, score_vector: scoreVector(evidence), findings, recommended_target: findings.find((entry) => !entry.meets_target)?.target_id ?? null, evidence});
}

export async function prepareIteration(benchmark, targetId, options = {}) {
  const diagnosis = options.baseline ?? await diagnoseImprovement(benchmark, options);
  const selected = targetId ?? diagnosis.recommended_target;
  const target = benchmark.profile.improvement_loop.targets[selected];
  if (!target) return iteration("iterate", selected ?? null, "BLOCKED", {reason_codes: ["improvement.target-required"]});
  return iteration("iterate", selected, "READY_FOR_CHANGE", {sampling_mode: diagnosis.sampling_mode, baseline_iteration_id: diagnosis.iteration_id, baseline_digest: sha256(diagnosis), score_vector: diagnosis.score_vector, evidence: diagnosis.evidence, source_snapshot_before: mutationSnapshot(target), target: {...target, target_id: selected}, next_command: `node bin/improve.mjs --mode verify-candidate --target ${selected} --baseline <this-report>`});
}

export async function verifyCandidate(benchmark, baselineReport, targetId, options = {}) {
  if (!baselineReport?.evidence || !baselineReport?.score_vector) return iteration("verify-candidate", targetId, "BLOCKED", {reason_codes: ["improvement.baseline-evidence-required"]});
  if (!benchmark.profile.improvement_loop.targets[targetId]) return iteration("verify-candidate", targetId ?? null, "BLOCKED", {reason_codes: ["improvement.target-required"]});
  const evidence = await collectImprovementEvidence(benchmark, {fast: baselineReport.sampling_mode === "fast"});
  const comparison = compareCandidate(benchmark.profile, targetId, baselineReport.evidence, evidence);
  const target = benchmark.profile.improvement_loop.targets[targetId];
  const currentSnapshot = mutationSnapshot(target);
  const changed = currentSnapshot.filter((entry, index) => entry.sha256 !== baselineReport.source_snapshot_before?.[index]?.sha256).map((entry) => entry.path);
  if (baselineReport.source_snapshot_before && changed.length === 0) {
    comparison.keep = false;
    if (!comparison.reason_codes.includes("improvement.no-allowlisted-source-change")) comparison.reason_codes.push("improvement.no-allowlisted-source-change");
  }
  return iteration("verify-candidate", targetId, comparison.keep ? "KEEP" : "REJECT", {sampling_mode: evidence.sampling_mode, baseline_iteration_id: baselineReport.iteration_id, baseline_digest: sha256(baselineReport), source_snapshot_before: baselineReport.source_snapshot_before ?? null, source_snapshot_after: currentSnapshot, changed_allowlisted_paths: changed, comparison, score_vector: scoreVector(evidence), evidence, next_action: comparison.keep ? "repeat-for-stability" : "revise-or-discard-candidate"});
}

export async function runImprovementLoop(benchmark, baselineReport, targetId, options = {}) {
  const required = benchmark.profile.improvement_loop.required_pass_streak;
  const maximum = options.max_attempts ?? benchmark.profile.improvement_loop.max_attempts;
  const evaluator = options.evaluator ?? ((...args) => verifyCandidate(...args));
  const attempts = [];
  let streak = 0;
  for (let number = 1; number <= maximum && streak < required; number += 1) {
    const result = await evaluator(benchmark, baselineReport, targetId, options);
    attempts.push({attempt: number, iteration_id: result.iteration_id, status: result.status, comparison: result.comparison ?? null});
    streak = result.status === "KEEP" ? streak + 1 : 0;
    if (result.status !== "KEEP") break;
  }
  return iteration("loop", targetId, streak >= required ? "STABLE" : "REJECT", {baseline_iteration_id: baselineReport?.iteration_id ?? null, required_pass_streak: required, achieved_pass_streak: streak, max_attempts: maximum, attempts, next_action: streak >= required ? "run-live-holdout" : "revise-or-discard-candidate"});
}

export function loadImprovementReport(path) {
  const report = JSON.parse(readFileSync(path, "utf8"));
  if (report.schema_version !== "are.reasoning-improvement-iteration/v1") throw new Error("Unsupported improvement baseline");
  return report;
}
