import {evaluateContinuation} from "../../request-decision-router/index.mjs";
import {canonicalizeJson, digestValue, fail, freezeResult, isRecord, nonEmptyString, uniqueStrings} from "./canonical.mjs";
import {isVerifiedReasoningReceiptConstraints} from "./reasoning-receipt-constraints.mjs";

function normalizePlanProposal(proposal) {
  const reasons = [];
  if (!isRecord(proposal)) return {posture: "rejected", rejection_reasons: ["proposal.expected-object"]};
  if (!nonEmptyString(proposal.proposal_id)) reasons.push("proposal.id-required");
  if (!nonEmptyString(proposal.declared_plan_digest)) reasons.push("proposal.plan-digest-required");
  if (!nonEmptyString(proposal.action_ref)) reasons.push("proposal.action-ref-required");
  if (!nonEmptyString(proposal.route_id)) reasons.push("proposal.route-required");
  if (!Array.isArray(proposal.effect_classes) || proposal.effect_classes.length === 0) reasons.push("proposal.effect-classes-required");
  if (typeof proposal.reversible !== "boolean") reasons.push("proposal.reversibility-required");
  if (!isRecord(proposal.next_turn) || !isRecord(proposal.next_turn.params)) reasons.push("proposal.next-turn-required");
  const hasSemanticDependency = Object.hasOwn(proposal, "semantic_dependency") && proposal.semantic_dependency !== null;
  if (hasSemanticDependency && !isRecord(proposal.semantic_dependency)) reasons.push("proposal.semantic-dependency-invalid");
  if (isRecord(proposal.semantic_dependency) && proposal.semantic_dependency.required !== true) reasons.push("proposal.semantic-dependency-required-invalid");
  if (isRecord(proposal.semantic_dependency) && proposal.semantic_dependency.binding_id !== undefined && !nonEmptyString(proposal.semantic_dependency.binding_id)) reasons.push("proposal.semantic-binding-id-invalid");
  if (isRecord(proposal.semantic_dependency) && proposal.semantic_dependency.conclusion_domain !== undefined && !nonEmptyString(proposal.semantic_dependency.conclusion_domain)) reasons.push("proposal.semantic-conclusion-domain-invalid");
  const material = canonicalizeJson({
    proposal_id: proposal.proposal_id ?? null,
    source_lane: "plan_bound",
    declared_plan_digest: proposal.declared_plan_digest ?? null,
    action_ref: proposal.action_ref ?? null,
    route_id: proposal.route_id ?? null,
    objective_kind: nonEmptyString(proposal.objective_kind) ? proposal.objective_kind.trim() : null,
    effect_classes: uniqueStrings(proposal.effect_classes),
    reversible: proposal.reversible === true,
    owner_gate_ref: nonEmptyString(proposal.owner_gate_ref) ? proposal.owner_gate_ref.trim() : null,
    evidence_refs: uniqueStrings(proposal.evidence_refs),
    semantic_dependency: isRecord(proposal.semantic_dependency) ? {
      required: proposal.semantic_dependency.required === true,
      binding_id: nonEmptyString(proposal.semantic_dependency.binding_id) ? proposal.semantic_dependency.binding_id.trim() : null,
      conclusion_domain: nonEmptyString(proposal.semantic_dependency.conclusion_domain) ? proposal.semantic_dependency.conclusion_domain.trim() : null,
    } : null,
    next_turn: proposal.next_turn ?? null,
    posture: reasons.length === 0 ? "candidate" : "rejected",
    rejection_reasons: reasons,
    authority_effect: "none",
  });
  return {...material, proposal_digest: digestValue(material)};
}

function normalizeInteractionProposal(proposal) {
  const reasons = [];
  if (!isRecord(proposal)) return {posture: "rejected", rejection_reasons: ["proposal.expected-object"]};
  if (!nonEmptyString(proposal.proposal_id)) reasons.push("proposal.id-required");
  if (!nonEmptyString(proposal.attributed_to)) reasons.push("proposal.attribution-required");
  if (!nonEmptyString(proposal.proposal_text)) reasons.push("proposal.text-required");
  if (!Array.isArray(proposal.evidence_refs) || proposal.evidence_refs.length === 0) reasons.push("proposal.evidence-required");
  const material = canonicalizeJson({
    proposal_id: proposal.proposal_id ?? null,
    source_lane: "interaction_bound",
    attributed_to: proposal.attributed_to ?? null,
    proposal_text: proposal.proposal_text ?? null,
    effect_classes: uniqueStrings(proposal.effect_classes?.length ? proposal.effect_classes : ["unknown-interaction-effect"]),
    reversible: typeof proposal.reversible === "boolean" ? proposal.reversible : false,
    owner_gate_ref: nonEmptyString(proposal.owner_gate_ref) ? proposal.owner_gate_ref.trim() : "Human owner of the exact interaction proposal",
    evidence_refs: uniqueStrings(proposal.evidence_refs),
    human_decision_digest: nonEmptyString(proposal.human_decision_digest) ? proposal.human_decision_digest.trim() : null,
    posture: reasons.length === 0 ? "candidate" : "rejected",
    rejection_reasons: reasons,
    authority_effect: "none",
  });
  return {...material, proposal_digest: digestValue(material)};
}

export function normalizeContinuationProposals(input) {
  if (!isRecord(input)) return fail("continuation-normalization", ["continuation.input-required"]);
  const plan = (Array.isArray(input.plan_bound) ? input.plan_bound : []).map(normalizePlanProposal).sort((a, b) => String(a.proposal_id).localeCompare(String(b.proposal_id)));
  const interaction = (Array.isArray(input.interaction_bound) ? input.interaction_bound : []).map(normalizeInteractionProposal).sort((a, b) => String(a.proposal_id).localeCompare(String(b.proposal_id)));
  return freezeResult({ok: true, plan_bound: plan, interaction_bound: interaction, digest: digestValue({plan, interaction}), authority_effect: "none"});
}

export function evaluateDualLaneContinuation(input, decisionProfile) {
  if (!isRecord(input) || !isRecord(input.completion)) return fail("continuation", ["continuation.completion-required"]);
  const normalized = normalizeContinuationProposals({plan_bound: input.plan_bound, interaction_bound: input.interaction_bound});
  if (!normalized.ok) return normalized;
  if (input.semantic_constraints !== undefined && !isVerifiedReasoningReceiptConstraints(input.semantic_constraints)) {
    return fail("continuation", ["continuation.semantic-constraints-unverified"]);
  }
  const semanticConstraints = input.semantic_constraints ?? null;
  const constraintsByProposal = new Map((semanticConstraints?.proposal_constraints ?? []).map((constraint) => [constraint.proposal_id, constraint]));
  const rejectedInteraction = normalized.interaction_bound.filter((proposal) => proposal.posture === "rejected");
  const validInteraction = normalized.interaction_bound.filter((proposal) => proposal.posture !== "rejected");
  const planOptions = normalized.plan_bound.map((proposal) => {
    const constraint = constraintsByProposal.get(proposal.proposal_id) ?? null;
    const constraintDigestMismatch = constraint && constraint.proposal_digest !== proposal.proposal_digest;
    const missingConstraint = semanticConstraints && proposal.semantic_dependency && !constraint;
    const semanticIneligible = constraint?.constraint_kind === "ineligible" || constraintDigestMismatch || missingConstraint;
    return {
      option_id: proposal.proposal_id,
      route_id: proposal.route_id,
      effect_classes: proposal.effect_classes,
      reversible: proposal.reversible,
      owner_gate_ref: proposal.owner_gate_ref,
      structurally_admissible: proposal.posture !== "rejected" && !semanticIneligible,
      rejection_reasons: [
        ...proposal.rejection_reasons,
        ...(constraint?.constraint_kind === "ineligible" ? constraint.reason_codes : []),
        ...(constraintDigestMismatch ? ["continuation.semantic-proposal-digest-mismatch"] : []),
        ...(missingConstraint ? ["continuation.semantic-constraint-missing"] : []),
      ],
    };
  });
  const engineDecision = evaluateContinuation({completion: input.completion, options: planOptions}, decisionProfile);
  let kind = engineDecision.kind;
  let reasons = [...engineDecision.reason_codes];
  let selectedProposal = normalized.plan_bound.find((proposal) => proposal.proposal_id === engineDecision.selected_option_id) ?? null;
  let ownerGateRefs = [...engineDecision.owner_gate_refs];
  const admissibleOptionIds = new Set(engineDecision.options.filter((option) => option.posture === "admissible").map((option) => option.option_id));
  const semanticGates = normalized.plan_bound
    .filter((proposal) => admissibleOptionIds.has(proposal.proposal_id) && constraintsByProposal.get(proposal.proposal_id)?.constraint_kind === "gate")
    .map((proposal) => constraintsByProposal.get(proposal.proposal_id));
  if (rejectedInteraction.length > 0) {
    kind = "block";
    reasons = ["continuation.interaction-proposal-invalid"];
    selectedProposal = null;
  } else if (validInteraction.length > 0) {
    kind = "gate";
    reasons = ["continuation.interaction-bound-human-decision-required"];
    selectedProposal = null;
    ownerGateRefs = [...new Set([...ownerGateRefs, ...validInteraction.map((proposal) => proposal.owner_gate_ref)])].sort();
  } else if (semanticGates.length > 0) {
    kind = "gate";
    reasons = ["continuation.semantic-owner-gate-required"];
    selectedProposal = null;
    ownerGateRefs = [...new Set([...ownerGateRefs, ...semanticGates.map((constraint) => constraint.owner_gate_ref).filter(Boolean)])].sort();
  }
  const material = canonicalizeJson({
    schema_version: "are.codex-dual-lane-continuation-directive/v1",
    directive_kind: kind,
    completion_digest: engineDecision.completion_digest,
    decision_profile_digest: engineDecision.decision_profile_digest,
    selected_proposal_id: selectedProposal?.proposal_id ?? null,
    candidate_proposal_ids: [...normalized.plan_bound, ...normalized.interaction_bound].map((proposal) => proposal.proposal_id).filter(Boolean).sort(),
    owner_gate_refs: ownerGateRefs,
    reason_codes: reasons,
    plan_bound: normalized.plan_bound,
    interaction_bound: normalized.interaction_bound,
    reasoning_receipt_constraints: semanticConstraints,
    engine_decision_digest: engineDecision.decision_digest,
    authority_effect: "none",
  });
  return freezeResult({ok: true, value: {...material, decision_digest: digestValue(material)}, selected_proposal: selectedProposal, engine_decision: engineDecision, authority_effect: "none"});
}
