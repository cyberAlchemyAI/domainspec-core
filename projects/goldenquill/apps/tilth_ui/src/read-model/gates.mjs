const HARD = "HARD";

function isCommitted(item) {
  return item && item.commit_state === "COMMITTED" && item.classification && item.classification !== "CLASSIFICATION_REQUIRED";
}

function unavailableEvidenceIds(data) {
  return new Set((data.quarantine_items || []).map((item) => item.evidence_id));
}

function sourceExists(data) {
  const explicitSource = (data.source_documents || []).some((doc) => doc.source_type === "RFA_NOFO" && doc.hash);
  return Boolean(explicitSource || data.opportunity?.ingested_nofo_hash || data.opportunity?.nofo_url);
}

function activeSamEvidenceExists(data) {
  const quarantined = unavailableEvidenceIds(data);
  return (data.evidence_items || []).some((item) => {
    if (quarantined.has(item.evidence_id)) return false;
    return isCommitted(item) && ["SAM_UEI_ACTIVE", "ACTIVE_SAM_UEI"].includes(item.evidence_kind);
  });
}

function budgetWithinMax(data) {
  const max = Number(data.budget?.max_request);
  const requested = Number(data.budget?.requested_total);
  if (!Number.isFinite(max) || max <= 0) return { known: false, pass: false };
  if (!Number.isFinite(requested)) return { known: false, pass: false };
  return { known: true, pass: requested <= max };
}

function linkedEvidenceState(data) {
  const linkedIds = new Set((data.draft_sections || []).flatMap((section) => section.evidence_links || []));
  const itemsById = new Map((data.evidence_items || []).map((item) => [item.evidence_id, item]));
  const quarantined = unavailableEvidenceIds(data);
  const linked = [...linkedIds].map((id) => itemsById.get(id)).filter(Boolean);
  const uncommitted = linked.filter((item) => !isCommitted(item));
  const quarantinedLinked = [...linkedIds].filter((id) => quarantined.has(id));
  return { linkedIds, linked, uncommitted, quarantinedLinked };
}

function postureSafe(data) {
  const mode = data.posture?.mode;
  const allowed = new Set(["FRONTIER_ELIGIBLE", "SPLIT_CONTEXT_HYBRID", "LOCAL_ONLY_SOVEREIGN", "Frontier-Eligible", "Split-Context Hybrid", "Local-Only / Sovereign"]);
  if (!mode || !allowed.has(mode)) return { pass: false, reason: "Deployment posture is missing or outside the three-value vocabulary." };
  if (data.posture?.changed_mid_cycle) return { pass: false, reason: "Posture changed mid-cycle; unsafe routing must be revalidated before work continues." };
  return { pass: true, reason: "Posture is visible and no mid-cycle unsafe routing change is recorded." };
}

function makeGate({ gate_id, description, verdict, evidence_ref = null, source_excerpt = "", remediation = null, blocks_scribe = false }) {
  return {
    gate_id,
    gate_class: HARD,
    description,
    verdict,
    evidence_ref,
    source_excerpt,
    remediation,
    blocks_scribe,
  };
}

function untestedFrom(gate) {
  return {
    ...gate,
    verdict: "UNTESTED_DUE_TO_BLOCK",
    evidence_ref: null,
    source_excerpt: "Cascade halted before this hard gate could be evaluated.",
    remediation: "Resolve the earlier fail-closed hard gate, then rerun the cascade.",
    blocks_scribe: false,
  };
}

export function evaluateGateCascade(data) {
  const budget = budgetWithinMax(data);
  const evidenceState = linkedEvidenceState(data);
  const posture = postureSafe(data);
  const gatePlan = [
    () => makeGate({
      gate_id: "E-101",
      description: "RFA/NOFO source document exists for this cycle.",
      verdict: sourceExists(data) ? "PASS" : "FAIL_CLOSED",
      evidence_ref: data.opportunity?.ingested_nofo_hash || data.source_documents?.[0]?.hash || null,
      source_excerpt: sourceExists(data) ? "Source document/hash present in local projection." : "No RFA/NOFO source hash or URL is present.",
      remediation: sourceExists(data) ? null : "Register the source RFA/NOFO before drafting or scoring.",
      blocks_scribe: !sourceExists(data),
    }),
    () => makeGate({
      gate_id: "E-102",
      description: "Active SAM/UEI evidence exists and is committed.",
      verdict: activeSamEvidenceExists(data) ? "PASS" : "FAIL_CLOSED",
      evidence_ref: activeSamEvidenceExists(data) ? "SAM_UEI_ACTIVE" : null,
      source_excerpt: activeSamEvidenceExists(data) ? "Committed SAM/UEI evidence is available." : "Active SAM/UEI evidence is UNKNOWN.",
      remediation: activeSamEvidenceExists(data) ? null : "Upload or refresh active SAM.gov/UEI evidence.",
      blocks_scribe: !activeSamEvidenceExists(data),
    }),
    () => makeGate({
      gate_id: "B-201",
      description: "Budget request is at or below funder maximum when maximum is available.",
      verdict: budget.pass ? "PASS" : "FAIL_CLOSED",
      evidence_ref: budget.known ? "budget.requested_total" : null,
      source_excerpt: budget.known ? `Requested ${data.budget.requested_total}; max ${data.budget.max_request}.` : "Budget maximum or requested total is UNKNOWN.",
      remediation: budget.pass ? null : budget.known ? "Reduce requested total or register corrected funder maximum evidence." : "Register budget request and funder maximum before drafting.",
      blocks_scribe: !budget.pass,
    }),
    () => makeGate({
      gate_id: "E-103",
      description: "Evidence classification is committed before evidence can support claims.",
      verdict: evidenceState.uncommitted.length ? "FAIL_CLOSED" : "PASS",
      evidence_ref: evidenceState.uncommitted.map((item) => item.evidence_id).join(", ") || "linked_evidence",
      source_excerpt: evidenceState.uncommitted.length ? "Linked evidence includes uncommitted or unclassified material." : "All linked evidence is committed.",
      remediation: evidenceState.uncommitted.length ? "Resolve classification/ontology state before linked evidence can support drafting." : null,
      blocks_scribe: Boolean(evidenceState.uncommitted.length),
    }),
    () => makeGate({
      gate_id: "E-104",
      description: "Quarantined evidence is unavailable to Scout, Scribe, and Judge.",
      verdict: evidenceState.quarantinedLinked.length ? "FAIL_CLOSED" : "PASS",
      evidence_ref: evidenceState.quarantinedLinked.join(", ") || "quarantine",
      source_excerpt: evidenceState.quarantinedLinked.length ? "A draft-linked evidence item is quarantined." : "No draft-linked evidence is quarantined.",
      remediation: evidenceState.quarantinedLinked.length ? "Release evidence from quarantine through operator mapping or unlink the claim." : null,
      blocks_scribe: Boolean(evidenceState.quarantinedLinked.length),
    }),
    () => makeGate({
      gate_id: "P-501",
      description: "Deployment posture is visible and blocks unsafe routing.",
      verdict: posture.pass ? "PASS" : "FAIL_CLOSED",
      evidence_ref: "posture.mode",
      source_excerpt: posture.reason,
      remediation: posture.pass ? null : "Reconfirm posture and rerun affected work before any council seat can proceed.",
      blocks_scribe: !posture.pass,
    }),
  ];

  const gates = [];
  let halted = false;
  for (const plan of gatePlan) {
    const gate = plan();
    if (halted) {
      gates.push(untestedFrom(gate));
      continue;
    }
    gates.push(gate);
    if (gate.gate_class === HARD && gate.verdict !== "PASS") {
      halted = true;
    }
  }

  const failed = gates.find((gate) => gate.verdict === "FAIL_CLOSED");
  return {
    projection_type: "GateProjection",
    cycle_id: data.cycle?.cycle_id,
    cascade_state: failed ? "GATE_FAILED_CLOSED" : "GATE_PASSED",
    hard_gate_failed: Boolean(failed),
    halted_at_gate_id: failed?.gate_id || null,
    gates,
  };
}

export function usableEvidenceItems(data) {
  const quarantined = unavailableEvidenceIds(data);
  return (data.evidence_items || []).filter((item) => isCommitted(item) && !quarantined.has(item.evidence_id));
}
