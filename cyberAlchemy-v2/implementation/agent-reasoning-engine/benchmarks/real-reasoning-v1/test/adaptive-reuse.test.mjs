import assert from "node:assert/strict";
import test from "node:test";

import {ARM_IDS, runAdaptiveReuseBenchmark} from "../src/adaptive-reuse.mjs";
import {loadBenchmark} from "../src/corpus.mjs";
import {packageRoot} from "../src/common.mjs";

test("adaptive reuse round improves intent and preservation while eliminating stale reuse", async () => {
  const result = await runAdaptiveReuseBenchmark(loadBenchmark(packageRoot), {warm_iterations: 0, timing_iterations: 2, enforce_performance: false});
  assert.equal(result.status, "PASS", JSON.stringify(result.summary.checks));
  assert.equal(result.cases.length, 8);
  assert.equal(result.cases.every((entry) => entry.arms.length === 4), true);
  assert.equal(result.metrics.by_arm[ARM_IDS[1]].critical_fact_preservation_rate > result.metrics.by_arm[ARM_IDS[0]].critical_fact_preservation_rate, true);
  assert.equal(result.metrics.by_arm[ARM_IDS[2]].intent_fidelity_rate > result.metrics.by_arm[ARM_IDS[1]].intent_fidelity_rate, true);
  assert.equal(result.metrics.by_arm[ARM_IDS[2]].stale_reuse_incidents > 0, true);
  assert.equal(result.metrics.by_arm[ARM_IDS[3]].stale_reuse_incidents, 0);
  assert.equal(result.metrics.by_arm[ARM_IDS[3]].cache_hit_posture, "unobserved");
  assert.equal(result.authority_effect, "none");
});

test("adaptive refresh distinguishes selected dependency drift from unrelated source drift", async () => {
  const left = await runAdaptiveReuseBenchmark(loadBenchmark(packageRoot), {warm_iterations: 0, timing_iterations: 1, enforce_performance: false});
  const right = await runAdaptiveReuseBenchmark(loadBenchmark(packageRoot), {warm_iterations: 0, timing_iterations: 1, enforce_performance: false});
  assert.deepEqual(left.cases, right.cases);
  const selectedDrift = left.cases.filter((entry) => entry.refresh_disposition === "successor-required");
  assert.equal(selectedDrift.length, 5);
  assert.equal(selectedDrift.every((entry) => entry.arms[3].exact_prefix_reuse === false), true);
  const unrelated = left.cases.find((entry) => entry.change_kind === "unrelated-source");
  assert.equal(unrelated.refresh_disposition, "reuse-current");
  assert.equal(unrelated.unrelated_source_drift_count, 1);
  assert.equal(unrelated.arms[3].exact_prefix_reuse, true);
});
