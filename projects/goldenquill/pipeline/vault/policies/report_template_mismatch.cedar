// pipeline/vault/policies/report_template_mismatch.cedar
// §14 Report Generator v1 LOCKED 2026-05-10 §14.9.5
// SKELETON — NOT YET SIGNED. Awaits §14 v1 Code-phase Slice 2 wiring +
// M15 signed-commit before this file is load-bearing at boot.
//
// Blueprint authority:
//   - section_14_report_generator.md §14.9.5 (F-REPORT-TEMPLATE-MISMATCH)
//   - section_14_report_generator.md §14.4.2 (ReportingTemplateContract)
//   - architecture v7.0.5 (Funder Intelligence DB)
//   - architecture v7.0.7 §6.1 (router-template-update signature pattern;
//     SN-LLC Ed25519 binding to lock_history)
//
// Lifecycle note:
//   Python evaluator at pipeline/logician/gates/f_report_template_mismatch.py
//   is authoritative; this .cedar file is the human-auditable surface.
//
// Denies surface as:
//   F-REPORT-TEMPLATE-MISMATCH.<sub_tag> per §14.9.5.

// Rule 1 — refuse_dispatch_with_workspace_template_drift
// PRE pre-track-dispatch: refuses when the operator-captured
// reporting_template.yaml content hash differs from the workspace-shared
// published_reporting_template.yaml content hash for the funder.
forbid (
  principal == ReportGenerator::"dispatch_action",
  action == ReportGenerator::"dispatch_track",
  resource is ReportGeneratorRunInput
) when {
  resource has has_workspace_published_template_drift &&
  resource.has_workspace_published_template_drift == true
};

// Rule 2 — refuse_dispatch_first_wave_template_absent
// RT-5a closure: FAIL-CLOSED for SN-LLC first-wave funders when the
// workspace-published template is missing OR the
// sn_llc_first_wave.signed.yaml marker is missing/tampered.
forbid (
  principal == ReportGenerator::"dispatch_action",
  action == ReportGenerator::"dispatch_track",
  resource is ReportGeneratorRunInput
) when {
  resource has has_workspace_published_template_absent_first_wave &&
  resource.has_workspace_published_template_absent_first_wave == true
};

// Rule 3 — refuse_dispatch_first_wave_marker_tampered
// RT-C2-04 closure: refuses dispatch when the first-wave marker hash
// does not bind to the lock_history immutable record OR the marker
// signature does not verify.
forbid (
  principal == ReportGenerator::"dispatch_action",
  action == ReportGenerator::"dispatch_track",
  resource is ReportGeneratorRunInput
) when {
  resource has has_workspace_published_template_marker_tampered &&
  resource.has_workspace_published_template_marker_tampered == true
};

// Rule 4 — refuse_dispatch_schema_required_subsections_unrecognized
// PRE pre-track-dispatch: refuses when required_sub_sections contains
// any value outside the v0.2 closed set.
forbid (
  principal == ReportGenerator::"dispatch_action",
  action == ReportGenerator::"dispatch_track",
  resource is ReportGeneratorRunInput
) when {
  resource has has_schema_required_sub_sections_unrecognized &&
  resource.has_schema_required_sub_sections_unrecognized == true
};

// Rule 5 — refuse_dispatch_schema_required_fields_unspecified
forbid (
  principal == ReportGenerator::"dispatch_action",
  action == ReportGenerator::"dispatch_track",
  resource is ReportGeneratorRunInput
) when {
  resource has has_schema_required_fields_unspecified &&
  resource.has_schema_required_fields_unspecified == true
};

// Rule 6 — refuse_dispatch_period_cadence_invalid
// PRE pre-track-dispatch: refuses when required_period_cadence is not
// in {monthly, quarterly, semi_annual, annual}.
forbid (
  principal == ReportGenerator::"dispatch_action",
  action == ReportGenerator::"dispatch_track",
  resource is ReportGeneratorRunInput
) when {
  resource has has_period_cadence_invalid &&
  resource.has_period_cadence_invalid == true
};

// Rule 7 — refuse_dispatch_template_signature_invalid
// PRE pre-track-dispatch: refuses when the operator-captured template
// carries an Ed25519 signature that does not verify against the
// operator's pinned public key.
forbid (
  principal == ReportGenerator::"dispatch_action",
  action == ReportGenerator::"dispatch_track",
  resource is ReportGeneratorRunInput
) when {
  resource has has_template_signature_invalid &&
  resource.has_template_signature_invalid == true
};

// Rule 8 — refuse_dispatch_operator_key_version_mismatch
// RT-5b TOFU rotation: refuses when the template's operator_key_version
// doesn't match the pinned key OR an auditable predecessor.
forbid (
  principal == ReportGenerator::"dispatch_action",
  action == ReportGenerator::"dispatch_track",
  resource is ReportGeneratorRunInput
) when {
  resource has has_operator_key_version_mismatch &&
  resource.has_operator_key_version_mismatch == true
};
