// pipeline/vault/policies/report_out_of_scope_drift.cedar
// §14 Report Generator v1 LOCKED 2026-05-10 §14.9.3
// SKELETON — NOT YET SIGNED. Awaits §14 v1 Code-phase Slice 2 wiring +
// M15 signed-commit before this file is load-bearing at boot.
//
// Blueprint authority:
//   - section_14_report_generator.md §14.9.3 (F-REPORT-OUT-OF-SCOPE-DRIFT)
//   - section_14_report_generator.md §14.6.4 + §14.6.5 (photo + beneficiary
//     consent_tier gates)
//   - §15 v1 F-ARCHIVIST-* three-layer-detection precedent
//
// Lifecycle note:
//   Python evaluator at pipeline/logician/gates/f_report_out_of_scope_drift.py
//   is authoritative; this .cedar file is the human-auditable surface.
//
// Denies surface as:
//   F-REPORT-OUT-OF-SCOPE-DRIFT.<sub_tag> per §14.9.3.

// Rule 1 — refuse_write_finalized_with_scope_drift
// Refuses writing a FINALIZED bundle when any claim's scope-tag set is
// NOT a subset of the union of PROMOTED commitments' scope-tag sets.
forbid (
  principal == ReportGenerator::"finalize_action",
  action == Vault::"write_finalized_report",
  resource is GrantReportBundle
) when {
  resource has has_scope_tag_not_in_promoted_set &&
  resource.has_scope_tag_not_in_promoted_set == true
};

// Rule 2 — refuse_cross_org_claim
// Law 3 structural enforcement — refuses any claim source path that
// resolves under a different org_slug subtree (RT-4b cross-org leak
// closure; mirrors §15 v1 F-ARCHIVIST-CROSS-ORG-LEAK).
forbid (
  principal == ReportGenerator::"finalize_action",
  action == Vault::"write_finalized_report",
  resource is GrantReportBundle
) when {
  resource has has_cross_org_claim &&
  resource.has_cross_org_claim == true
};

// Rule 3 — refuse_cross_grant_claim
// Refuses claim source paths that resolve under a different grant_id.
forbid (
  principal == ReportGenerator::"finalize_action",
  action == Vault::"write_finalized_report",
  resource is GrantReportBundle
) when {
  resource has has_cross_grant_claim &&
  resource.has_cross_grant_claim == true
};

// Rule 4 — refuse_cross_period_without_sp0
// Refuses claim source paths in different period_n without SP0 flag
// `accept_signed_prior_period_claim_evidence_map: true`.
forbid (
  principal == ReportGenerator::"finalize_action",
  action == Vault::"write_finalized_report",
  resource is GrantReportBundle
) when {
  resource has has_cross_period_without_sp0 &&
  resource.has_cross_period_without_sp0 == true
};

// Rule 5 — refuse_beneficiary_consent_tier_violation
// RT-6a / RT-6c / RT-C2-03: refuses claim text including beneficiary
// detail above the beneficiary's consent_tier (no-narrative /
// metrics-only inclusion in narrative-style sub-sections).
forbid (
  principal == ReportGenerator::"finalize_action",
  action == Vault::"write_finalized_report",
  resource is GrantReportBundle
) when {
  resource has has_beneficiary_consent_tier_violation &&
  resource.has_beneficiary_consent_tier_violation == true
};

// Rule 6 — refuse_photo_consent_tier_violation
// §14.6.4 + RT-7a: refuses photos with consent_tier internal_only in
// photo_gallery; refuses cross-section references to internal_only OR
// funder_only photo_ids outside photo_gallery.
forbid (
  principal == ReportGenerator::"finalize_action",
  action == Vault::"write_finalized_report",
  resource is GrantReportBundle
) when {
  resource has has_photo_consent_tier_violation &&
  resource.has_photo_consent_tier_violation == true
};

// Rule 7 — refuse_beneficiary_aggregate_identifying_unapproved
// RT-6a: refuses aggregate counts ≤2 without per-aggregate operator
// Ed25519 signature.
forbid (
  principal == ReportGenerator::"finalize_action",
  action == Vault::"write_finalized_report",
  resource is GrantReportBundle
) when {
  resource has has_beneficiary_aggregate_identifying_unapproved &&
  resource.has_beneficiary_aggregate_identifying_unapproved == true
};

// Rule 8 — refuse_beneficiary_privacy_leak
// RT-C2-03: refuses narrative text mentioning a beneficiary by name
// when that beneficiary's consent_tier disallows narrative inclusion.
forbid (
  principal == ReportGenerator::"finalize_action",
  action == Vault::"write_finalized_report",
  resource is GrantReportBundle
) when {
  resource has has_beneficiary_privacy_leak &&
  resource.has_beneficiary_privacy_leak == true
};
