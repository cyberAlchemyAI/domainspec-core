import {
  canonicalBytes,
  sealRecord,
  sha256Bytes,
} from "./canonical-json.mjs";
import { EVALUATOR_ID, SCHEMA_VERSION } from "./reducer.mjs";

function observationIds(observations, posture) {
  return observations
    .filter((observation) => observation.posture === posture)
    .map((observation) => observation.observation_id)
    .sort();
}

export function assembleReasoningReceipt(request, semantic) {
  const receipt = sealRecord({
    record_type: "ReasoningReceipt",
    schema_version: SCHEMA_VERSION,
    run_id: request.run_id,
    created_at: request.created_at,
    producer: EVALUATOR_ID,
    mode: request.mode,
    evaluator_id: EVALUATOR_ID,
    input_digests: {
      authority_snapshot: request.authority_snapshot.digest,
      catalog: request.catalog.digest,
      challenge_closure: request.challenge_closure.digest,
      effort_profile: request.effort_profile.digest,
      entry_gate: request.entry_gate.digest,
      frame: request.frame.digest,
      observations: request.observations
        .map((observation) => observation.digest)
        .sort(),
      runtime_journal_cut: request.runtime_journal_cut.digest,
      technique_plan: request.technique_plan.digest,
    },
    applicability_decision: semantic.applicability_decision,
    admitted_observation_ids: observationIds(request.observations, "admitted"),
    rejected_observation_ids: observationIds(request.observations, "rejected"),
    unresolved_observation_ids: observationIds(request.observations, "unresolved"),
    executed_challenge_records: [
      ...request.challenge_closure.required_lanes.map((lane) => lane.lane_id),
    ].sort(),
    executed_technique_records: [
      ...(request.technique_plan.selected_techniques ?? []),
    ].sort(),
    derivation: semantic.derivation,
    terminal_outcome: semantic.outcome,
    unresolved_residue: semantic.residue,
    entry_gate_decision_digest: request.entry_gate.digest,
    claim_ceiling:
      "A recommendation under captured inputs only; not premise truth, proof, approval, promotion, confidence, authority, or permission.",
  });
  const bytes = canonicalBytes(receipt);
  return {
    receipt,
    bytes,
    exact_bytes_digest: sha256Bytes(bytes),
  };
}
