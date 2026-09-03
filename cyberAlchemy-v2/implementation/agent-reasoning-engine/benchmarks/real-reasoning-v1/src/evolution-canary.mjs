import {readFileSync} from "node:fs";

import {loadBenchmark} from "./corpus.mjs";
import {packageRoot} from "./common.mjs";
import {createFixtureResearchProvider, runBenchmarkEvolutionCycle} from "./evolution-bridge.mjs";

function evidence(precision) {
  return {
    sampling_mode: "fixture",
    core: {
      result_id: `fixture:core:${precision}`,
      summary: {route_accuracy: 0.99, definition_recall: 0.97, context_precision: precision, false_direct_ambiguities: 0, determinism_mismatches: 0},
      metrics: {route: {p95_ms: 1}, request_selection: {p95_ms: 2}, preflight: {p95_ms: 20}},
      cases: {routing: [], context: []},
    },
    integration: {cases: {lifecycle: [{passed: true}], failure_safety: [{passed: true}]}},
  };
}

function diagnosis() {
  return {
    schema_version: "are.reasoning-improvement-iteration/v1",
    iteration_id: "fixture:diagnosis:context-precision",
    evidence_digest: "d".repeat(64),
    status: "DIAGNOSED",
    findings: [{target_id: "context-precision", priority: 1, metric: "context_precision", value: 0.72, threshold: 0.8, meets_target: false, failed_cases: ["fixture:precision"], mutation_allowlist: ["packages/context-basis-runtime"],}],
  };
}

export async function runFixtureEvolutionCanary() {
  const evolutionProfile = JSON.parse(readFileSync(new URL("../../../packages/evolution-runtime/profiles/default-v1.json", import.meta.url), "utf8"));
  evolutionProfile.research.enabled = true;
  const provider = createFixtureResearchProvider(new URL("../fixtures/evolution/context-precision-research.json", import.meta.url));
  return runBenchmarkEvolutionCycle(loadBenchmark(packageRoot), {
    evolution_profile: evolutionProfile,
    diagnosis: diagnosis(),
    research_providers: [provider],
    reproduce: async ({technique}) => ({
      technique_ref: technique.record_id,
      environment_ref: "node:26.8.1-fixture",
      protocol_ref: "fixture:context-precision-reproduction-v1",
      expected_observations: technique.expected_observations,
      actual_observations: ["fixture context precision increased"],
      outcome: "reproduced",
    }),
    build_variant: async ({technique, reproduction}) => ({
      baseline_ref: "serving:fixture-baseline",
      source_tree_digest: "a".repeat(64),
      build_environment_ref: "node:26.8.1-fixture",
      technique_refs: [technique.record_id],
      reproduction_refs: [reproduction.record_id],
      changed_paths: ["packages/context-basis-runtime/index.mjs"],
    }),
    baseline_evidence: evidence(0.72),
    candidate_evidence: evidence(0.84),
    manifest_ref: "benchmark:real-reasoning-v1:fixture",
    environment_ref: "node:26.8.1-fixture",
    holdout_passed: true,
    keep_streak: evolutionProfile.upgrade.required_keep_streak,
  });
}

export function projectCanaryResult(result) {
  return {
    schema_version: "are.evolution-canary-result/v1",
    status: result.status,
    target_ref: result.target?.record_id ?? null,
    research_result_refs: result.research?.results?.map((item) => item.record_id) ?? [],
    technique_ref: result.technique?.record_id ?? null,
    reproduction_ref: result.reproduction?.record_id ?? null,
    variant_ref: result.variant?.record_id ?? null,
    comparison_ref: result.comparison?.record_id ?? null,
    comparison_outcome: result.comparison?.outcome ?? null,
    upgrade_decision_ref: result.decision?.record_id ?? null,
    upgrade_disposition: result.decision?.disposition ?? null,
    evolution_epoch_digest: result.sealed?.epoch?.epoch_digest ?? null,
    authority_effect: "none",
  };
}

