// Cedar policy file — F-PACKET-* family (§16 Reflection Packet)
//
// Owner: §16 Reflection Packet (seat_owner: "reflection_packet")
// v0.1 hook compound LOCK: §16 v1 + §4 v2.x.y + §0.5 v22 (2026-05-15 row 216-218)
// v0.2 first wave compound LOCK: §16 v1.1 + §2 v7.x + §4 v2.x.y.1 + §15 v2.x +
//                                §0.5 v23 (2026-05-15 row 219-223)
//
// **OQ-2 RESOLVED minimal scope at v0.2 first wave**:
//   - Rule 19 (F-PACKET-COVERAGE-INCOMPLETE META-gate): ENFORCING.
//   - Rules 1-18 (BINDING predicates): remain at placeholder. The 18
//     Logician deterministic Python predicates at
//     `pipeline/logician/gates/f_packet_*.py` are LIVE at v0.2 first wave
//     and are the load-bearing enforcement layer. Cedar full enforcement
//     defers to v1.x consumer runtime amendment per §16 v1.1 §16.v1.1.4.
//   - This is defense-in-depth alongside Logician; not redundancy.
//     Compounding the failure surface without compounding value would
//     have been the alternative (rejected at OQ-2 default).
//
// Path B naming discipline: F-PACKET-* gates the artifact; F-REFLECTION-*
// gates the producer behavior; F-ARCHIVIST-* gates the substrate write;
// F-WPFA-* gates the sibling artifact. NO cross-family imports — enforced
// at module-import time by AST-lint (§4 v2.x.y §6).
//
// Mirrors pattern from `pipeline/vault/policies/operational_subkinds.cedar`
// and `pipeline/vault/policies/report_*.cedar`.

// ────────────────────────────────────────────────────────────────────────
// Rule 1 — F-PACKET-INSTANCE-LEAK (DORMANT at v0.1 hook)
// ────────────────────────────────────────────────────────────────────────
// PRE-emission: forbid instance-level identifiers in pattern_summary /
// proposed_rule fields. Three-layer detection (NFKC + NER + regex) per
// §15.9.2 RT-07 precedent. Body lives at v0.2 first wave; this Cedar
// rule placeholder is the explicit reservation.
forbid (
  principal,
  action == Action::"reflection-packet-emit",
  resource
) when {
  // v0.1 hook DORMANT — predicate body NotImplementedError;
  // forbid context.f_packet_instance_leak_v0_1_dormant_marker
  context.f_packet_instance_leak_v0_1_dormant_marker == true
};

// ────────────────────────────────────────────────────────────────────────
// Rule 2 — F-PACKET-CROSS-ORG-LEAK (DORMANT)
// ────────────────────────────────────────────────────────────────────────
// PRE-emission + PRE-load: path slug match + span_id org_slug match.
// Mirrors `check_f_wpfa_cross_org_leak` byte-for-byte at v0.2.
forbid (
  principal,
  action,
  resource
) when {
  action == Action::"reflection-packet-emit" &&
  context.f_packet_cross_org_leak_v0_1_dormant_marker == true
};

// ────────────────────────────────────────────────────────────────────────
// Rule 3 — F-PACKET-FABRICATION (DORMANT)
// ────────────────────────────────────────────────────────────────────────
forbid (
  principal,
  action == Action::"reflection-packet-emit",
  resource
) when {
  context.f_packet_fabrication_v0_1_dormant_marker == true
};

// ────────────────────────────────────────────────────────────────────────
// Rule 4 — F-PACKET-CLASS-SLOT-LEAK (DORMANT)
// ────────────────────────────────────────────────────────────────────────
forbid (
  principal,
  action == Action::"reflection-packet-emit",
  resource
) when {
  context.f_packet_class_slot_leak_v0_1_dormant_marker == true
};

// ────────────────────────────────────────────────────────────────────────
// Rule 5 — F-PACKET-CLASS-MISLABEL (DORMANT)
// ────────────────────────────────────────────────────────────────────────
forbid (
  principal,
  action == Action::"reflection-packet-emit",
  resource
) when {
  context.f_packet_class_mislabel_v0_1_dormant_marker == true
};

// ────────────────────────────────────────────────────────────────────────
// Rule 6 — F-PACKET-EVAL-ONLY-GROUNDED (DORMANT)
// ────────────────────────────────────────────────────────────────────────
forbid (
  principal,
  action == Action::"reflection-packet-emit",
  resource
) when {
  context.f_packet_eval_only_grounded_v0_1_dormant_marker == true
};

// ────────────────────────────────────────────────────────────────────────
// Rule 7 — F-PACKET-PREMATURE-GENERALIZATION (DORMANT)
// ────────────────────────────────────────────────────────────────────────
forbid (
  principal,
  action == Action::"reflection-packet-emit",
  resource
) when {
  context.f_packet_premature_generalization_v0_1_dormant_marker == true
};

// ────────────────────────────────────────────────────────────────────────
// Rule 8 — F-PACKET-SPAN-PROVENANCE-MISSING (DORMANT)
// ────────────────────────────────────────────────────────────────────────
// RESOLVES §17 v1 §6.5 forward-reference at the compound triple LOCK.
forbid (
  principal,
  action == Action::"reflection-packet-emit",
  resource
) when {
  context.f_packet_span_provenance_missing_v0_1_dormant_marker == true
};

// ────────────────────────────────────────────────────────────────────────
// Rule 9 — F-PACKET-RETRIEVAL-CORRUPTION (DORMANT)
// ────────────────────────────────────────────────────────────────────────
forbid (
  principal,
  action == Action::"reflection-packet-load",
  resource
) when {
  context.f_packet_retrieval_corruption_v0_1_dormant_marker == true
};

// ────────────────────────────────────────────────────────────────────────
// Rule 10 — F-PACKET-MEMORY-INJECTION (DORMANT)
// ────────────────────────────────────────────────────────────────────────
forbid (
  principal,
  action == Action::"reflection-packet-emit",
  resource
) when {
  context.f_packet_memory_injection_v0_1_dormant_marker == true
};

// ────────────────────────────────────────────────────────────────────────
// Rule 11 — F-PACKET-SCHEMA-DRIFT (DORMANT; advisory-only at v0.1 hook)
// ────────────────────────────────────────────────────────────────────────
forbid (
  principal,
  action == Action::"reflection-packet-load",
  resource
) when {
  context.f_packet_schema_drift_v0_1_dormant_marker == true
};

// ────────────────────────────────────────────────────────────────────────
// Rule 12 — F-PACKET-CADENCE-VIOLATION (DORMANT)
// ────────────────────────────────────────────────────────────────────────
forbid (
  principal,
  action == Action::"reflection-packet-emit",
  resource
) when {
  context.f_packet_cadence_violation_v0_1_dormant_marker == true
};

// ────────────────────────────────────────────────────────────────────────
// Rule 13 — F-PACKET-SIGNATURE-INVALID (DORMANT)
// ────────────────────────────────────────────────────────────────────────
forbid (
  principal,
  action == Action::"reflection-packet-load",
  resource
) when {
  context.f_packet_signature_invalid_v0_1_dormant_marker == true
};

// ────────────────────────────────────────────────────────────────────────
// Rule 14 — F-PACKET-OPERATOR-SIGNATURE-MISSING (DORMANT)
// ────────────────────────────────────────────────────────────────────────
forbid (
  principal,
  action == Action::"reflection-packet-load",
  resource
) when {
  context.f_packet_operator_signature_missing_v0_1_dormant_marker == true
};

// ────────────────────────────────────────────────────────────────────────
// Rule 15 — F-PACKET-OPERATOR-SIGNATURE-INVALID (DORMANT)
// ────────────────────────────────────────────────────────────────────────
forbid (
  principal,
  action == Action::"reflection-packet-load",
  resource
) when {
  context.f_packet_operator_signature_invalid_v0_1_dormant_marker == true
};

// ────────────────────────────────────────────────────────────────────────
// Rule 16 — F-PACKET-CYCLE-ID-UNRESOLVABLE (DORMANT)
// ────────────────────────────────────────────────────────────────────────
forbid (
  principal,
  action == Action::"reflection-packet-emit",
  resource
) when {
  context.f_packet_cycle_id_unresolvable_v0_1_dormant_marker == true
};

// ────────────────────────────────────────────────────────────────────────
// Rule 17 — F-PACKET-OUTCOME-EVIDENCE-MISSING (DORMANT)
// ────────────────────────────────────────────────────────────────────────
forbid (
  principal,
  action,
  resource
) when {
  (action == Action::"reflection-packet-emit" ||
   action == Action::"reflection-packet-load") &&
  context.f_packet_outcome_evidence_missing_v0_1_dormant_marker == true
};

// ────────────────────────────────────────────────────────────────────────
// Rule 18 — F-PACKET-PRODUCER-UNAUTHORIZED (DORMANT)
// ────────────────────────────────────────────────────────────────────────
forbid (
  principal,
  action == Action::"reflection-packet-emit",
  resource
) when {
  context.f_packet_producer_unauthorized_v0_1_dormant_marker == true
};

// ────────────────────────────────────────────────────────────────────────
// Rule 19 — F-PACKET-COVERAGE-INCOMPLETE (LIVE — META PRE-cycle)
// ────────────────────────────────────────────────────────────────────────
// META-gate dormant-binding lever. Activates at v0.2 first wave deployment
// to verify all 18 BINDING bodies are realized. At v0.1 hook the predicate
// signature is registered; the deterministic Python body at
// `pipeline/logician/gates/f_packet_coverage_incomplete.py` is the LIVE
// implementation (Python is the authoritative enforcement; Cedar rule
// here is documentary).
forbid (
  principal,
  action == Action::"reflection-packet-deploy",
  resource
) when {
  context.f_packet_coverage_incomplete_missing_bodies != []
};
