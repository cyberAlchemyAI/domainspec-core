// pipeline/vault/policies/report_commitment_missed.cedar
// §14 Report Generator v1 LOCKED 2026-05-10 §14.9.2
// SKELETON — NOT YET SIGNED. Awaits §14 v1 Code-phase Slice 2 wiring +
// M15 signed-commit before this file is load-bearing at boot.
//
// Blueprint authority:
//   - section_14_report_generator.md §14.9.2 (F-REPORT-COMMITMENT-MISSED)
//   - section_14_report_generator.md §14.4.1 (PROPOSAL_COMMITMENT_STATUS_PROMOTED filter)
//
// Lifecycle note:
//   Python evaluator at pipeline/logician/gates/f_report_commitment_missed.py
//   is authoritative; this .cedar file is the human-auditable surface.
//
// Denies surface as:
//   F-REPORT-COMMITMENT-MISSED.<sub_tag> per §14.9.2.

// Rule 1 — refuse_dispatch_with_empty_promoted_set
// PRE pre-track-dispatch: refuses if proposal_commitments.yaml carries
// zero rows with status == "PROMOTED".
forbid (
  principal == ReportGenerator::"dispatch_action",
  action == ReportGenerator::"dispatch_track",
  resource is ReportGeneratorRunInput
) when {
  resource has promoted_commitment_count &&
  resource.promoted_commitment_count == 0
};

// Rule 2 — refuse_judge_score_with_missed_required_subsection
// POST judge-equivalent: refuses if a PROMOTED commitment's
// required_sub_sections is NOT a subset of sub_sections_authored
// (RT-2b fail-closed).
forbid (
  principal == ReportGenerator::"judge_action",
  action == ReportGenerator::"score_bundle",
  resource is GrantReportBundle
) when {
  resource has has_commitment_required_subsection_missing &&
  resource.has_commitment_required_subsection_missing == true
};

// Rule 3 — refuse_judge_score_with_unaddressed_criterion
// POST judge-equivalent: refuses if a PROMOTED commitment's
// evaluation_criteria has an unaddressed field (RT-2b).
forbid (
  principal == ReportGenerator::"judge_action",
  action == ReportGenerator::"score_bundle",
  resource is GrantReportBundle
) when {
  resource has has_evaluation_criterion_unaddressed &&
  resource.has_evaluation_criterion_unaddressed == true
};

// Rule 4 — refuse_waiver_unsigned
// PRE pre-track-dispatch: refuses if any operator-claimed not-due-yet
// waiver is missing OR the Ed25519 signature does not verify (RT-2b).
forbid (
  principal == ReportGenerator::"dispatch_action",
  action == ReportGenerator::"dispatch_track",
  resource is ReportGeneratorRunInput
) when {
  resource has has_unsigned_commitment_waiver &&
  resource.has_unsigned_commitment_waiver == true
};

// Rule 5 — refuse_waiver_cap_exceeded
// PRE pre-track-dispatch: refuses if waivers would suppress all
// commitments (vacuous reports forbidden).
forbid (
  principal == ReportGenerator::"dispatch_action",
  action == ReportGenerator::"dispatch_track",
  resource is ReportGeneratorRunInput
) when {
  resource has commitment_waiver_cap_exceeded &&
  resource.commitment_waiver_cap_exceeded == true
};

// Rule 6 — refuse_invalid_commitment_id_format
// PRE pre-track-dispatch: refuses if any commitment_id violates the
// ^[A-Z0-9_-]+$ safe-identifier regex (RT-C2-02 closure; path-traversal
// mitigation).
forbid (
  principal == ReportGenerator::"dispatch_action",
  action == ReportGenerator::"dispatch_track",
  resource is ReportGeneratorRunInput
) when {
  resource has has_commitment_id_invalid_format &&
  resource.has_commitment_id_invalid_format == true
};
