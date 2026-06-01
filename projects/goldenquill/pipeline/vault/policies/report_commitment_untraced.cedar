// pipeline/vault/policies/report_commitment_untraced.cedar
// §14 Report Generator v1 LOCKED 2026-05-10 §14.9.1
// SKELETON — NOT YET SIGNED. Awaits §14 v1 Code-phase Slice 2 wiring +
// M15 signed-commit before this file is load-bearing at boot.
//
// Blueprint authority:
//   - section_14_report_generator.md §14.9.1 (F-REPORT-COMMITMENT-UNTRACED)
//   - section_14_report_generator.md §14.5.0 (GrantReportBundle.bundle_state
//     transition gate)
//   - section_04_v2_x_amendment.md §5.2 (HORIZON → ACTIVE flip at §14 v1 LOCK)
//
// Lifecycle note (mirrors operational_subkinds.cedar + compound_commit.cedar):
//   This file is a CODE-side Cedar policy. The Python evaluator at
//   pipeline/logician/gates/f_report_commitment_untraced.py::check_commitment_untraced
//   is authoritative at v0.2; this .cedar file is the human-auditable
//   surface that pairs with it. Any drift between this file and the
//   Python predicate body is the audit-finding surface.
//
// Denies surface as:
//   F-REPORT-COMMITMENT-UNTRACED.<sub_tag> per §14.9.1.
//
// Cedar is default-deny. The forbid rules below model the Python
// predicate's fail-closed branches.

// Rule 1 — refuse_finalize_with_untraced_claims
// Refuses writing a FINALIZED bundle when any claim in the draft has no
// entry in claim_evidence_map.yaml OR when any source has drifted.
forbid (
  principal == ReportGenerator::"finalize_action",
  action == Vault::"write_finalized_report",
  resource is GrantReportBundle
) when {
  resource has bundle_state &&
  resource.bundle_state == "DRAFT_PENDING_OPERATOR_SIGN" &&
  resource has has_untraced_claim &&
  resource.has_untraced_claim == true
};

// Rule 2 — refuse_finalize_with_drifted_source
// Refuses finalization when any per-claim source content hash drifted
// between Scribe author time and pre-finalize check time (RT-1b closure).
forbid (
  principal == ReportGenerator::"finalize_action",
  action == Vault::"write_finalized_report",
  resource is GrantReportBundle
) when {
  resource has bundle_state &&
  resource.bundle_state == "DRAFT_PENDING_OPERATOR_SIGN" &&
  resource has has_source_content_drift &&
  resource.has_source_content_drift == true
};

// Rule 3 — refuse_finalize_with_post_sign_mutation
// RT-8b closure — refuses finalization when the draft_<v>.md file was
// modified after the operator signed the claim_evidence_map.
forbid (
  principal == ReportGenerator::"finalize_action",
  action == Vault::"write_finalized_report",
  resource is GrantReportBundle
) when {
  resource has has_draft_post_sign_mutation &&
  resource.has_draft_post_sign_mutation == true
};

// Rule 4 — refuse_finalize_with_unflagged_paraphrase
// RT-C2-10 closure — refuses finalization when a narrative claim is
// neither verbatim-substantiated nor flagged as operator-approved
// paraphrase.
forbid (
  principal == ReportGenerator::"finalize_action",
  action == Vault::"write_finalized_report",
  resource is GrantReportBundle
) when {
  resource has has_narrative_paraphrase_unflagged &&
  resource.has_narrative_paraphrase_unflagged == true
};
