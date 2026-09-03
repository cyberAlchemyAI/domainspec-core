import assert from "node:assert/strict";
import test from "node:test";

import {loadBenchmark} from "../src/corpus.mjs";
import {packageRoot} from "../src/common.mjs";
import {compareCandidate, diagnoseImprovement, runImprovementLoop} from "../src/improvement-loop.mjs";

function evidence(overrides = {}) {
  const routeAccuracy = overrides.route_accuracy ?? 0.90;
  const recall = overrides.definition_recall ?? 0.70;
  const precision = overrides.context_precision ?? 0.20;
  const contextPass = overrides.context_pass ?? false;
  return {
    sampling_mode: "fast",
    core: {
      summary: {route_accuracy: routeAccuracy, definition_recall: recall, context_precision: precision, false_direct_ambiguities: overrides.false_direct ?? 0, determinism_mismatches: overrides.determinism ?? 0},
      metrics: {route: {p95_ms: overrides.route_p95 ?? 1}, request_selection: {p95_ms: 2}, preflight: {p95_ms: 20}},
      cases: {routing: [], context: [{scenario_id: "CONTEXT-006", passed: contextPass}, {scenario_id: "CONTEXT-010", passed: contextPass}]}
    },
    integration: {cases: {lifecycle: [{scenario_id: "L", passed: overrides.lifecycle ?? true}], failure_safety: [{scenario_id: "F", passed: overrides.failure ?? true}]}}
  };
}

test("candidate comparison keeps a targeted improvement with intact safety", () => {
  const benchmark = loadBenchmark(packageRoot);
  const comparison = compareCandidate(benchmark.profile, "objective-disambiguation", evidence(), evidence({context_pass: true, definition_recall: 0.72}));
  assert.equal(comparison.keep, true, JSON.stringify(comparison));
});

test("candidate comparison rejects safety regression even when target improves", () => {
  const benchmark = loadBenchmark(packageRoot);
  const comparison = compareCandidate(benchmark.profile, "objective-disambiguation", evidence(), evidence({context_pass: true, definition_recall: 0.72, failure: false}));
  assert.equal(comparison.keep, false);
  assert.ok(comparison.reason_codes.includes("improvement.safety-regression"));
});

test("fast diagnosis binds evidence and recommends only an unmet target", async () => {
  const result = await diagnoseImprovement(loadBenchmark(packageRoot), {fast: true});
  assert.equal(result.status, "DIAGNOSED");
  const unmet = result.findings.filter((finding) => finding.meets_target === false);
  if (unmet.length === 0) assert.equal(result.recommended_target, null);
  else {
    assert.equal(typeof result.recommended_target, "string");
    assert.ok(unmet.some((finding) => finding.target_id === result.recommended_target));
  }
  assert.equal(result.sampling_mode, "fast");
  assert.ok(result.evidence.core);
});

test("stability loop requires two consecutive KEEP results", async () => {
  const benchmark = loadBenchmark(packageRoot);
  const statuses = ["KEEP", "KEEP"];
  const result = await runImprovementLoop(benchmark, {iteration_id: "baseline"}, "objective-disambiguation", {max_attempts: 5, evaluator: async () => ({iteration_id: `attempt:${statuses.length}`, status: statuses.shift(), comparison: {}})});
  assert.equal(result.status, "STABLE");
  assert.equal(result.attempts.length, 2);
  assert.equal(result.achieved_pass_streak, 2);
});

test("stability loop stops on the first rejected candidate", async () => {
  const benchmark = loadBenchmark(packageRoot);
  let calls = 0;
  const result = await runImprovementLoop(benchmark, {iteration_id: "baseline"}, "objective-disambiguation", {max_attempts: 5, evaluator: async () => { calls += 1; return {iteration_id: "rejected", status: "REJECT", comparison: {}}; }});
  assert.equal(result.status, "REJECT");
  assert.equal(calls, 1);
});
