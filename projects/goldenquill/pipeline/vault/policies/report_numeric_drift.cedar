// pipeline/vault/policies/report_numeric_drift.cedar
// §14 Report Generator v1 LOCKED 2026-05-10 §14.9.4
// SKELETON — NOT YET SIGNED. Awaits §14 v1 Code-phase Slice 2 wiring +
// M15 signed-commit before this file is load-bearing at boot.
//
// Blueprint authority:
//   - section_14_report_generator.md §14.9.4 (F-REPORT-NUMERIC-DRIFT)
//   - architecture v7.0.4-M1 §2 Decimal mandate (canonical rounding mode
//     ROUND_HALF_UP; no float arithmetic in numeric paths)
//   - §14.6.2 metrics_table composer (per-cell drift)
//   - §14.6.3 financial_summary composer (per-line variance)
//
// Lifecycle note:
//   Python evaluator at pipeline/logician/gates/f_report_numeric_drift.py
//   is authoritative; this .cedar file is the human-auditable surface.
//   The Decimal-mandate runtime defense lives in the Python predicate
//   body (assert isinstance(value, Decimal)); Cedar adds the write-path
//   forbid.
//
// Denies surface as:
//   F-REPORT-NUMERIC-DRIFT.<sub_tag> per §14.9.4.

// Rule 1 — refuse_write_finalized_with_value_drift
// Refuses writing a FINALIZED bundle when any numeric claim differs
// from the KFR-derived expected value beyond per-field tolerance.
forbid (
  principal == ReportGenerator::"finalize_action",
  action == Vault::"write_finalized_report",
  resource is GrantReportBundle
) when {
  resource has has_kfr_value_mismatch_above_tolerance &&
  resource.has_kfr_value_mismatch_above_tolerance == true
};

forbid (
  principal == ReportGenerator::"finalize_action",
  action == Vault::"write_finalized_report",
  resource is GrantReportBundle
) when {
  resource has has_kfr_value_mismatch_below_tolerance &&
  resource.has_kfr_value_mismatch_below_tolerance == true
};

// Rule 2 — refuse_write_finalized_with_unit_mismatch
// Composes with §13 F-DATACOLLECTOR-KFR-DRIFT.unit_mismatch — refuses
// finalization when claim and KFR carry different units (kg vs lb etc).
forbid (
  principal == ReportGenerator::"finalize_action",
  action == Vault::"write_finalized_report",
  resource is GrantReportBundle
) when {
  resource has has_kfr_value_unit_mismatch &&
  resource.has_kfr_value_unit_mismatch == true
};

// Rule 3 — refuse_write_finalized_with_float_defect
// Defense-in-depth — Cedar layer's enforcement of the Decimal mandate;
// surfaces when the Python predicate detected a float in a numeric
// arithmetic path (R-REPORT-DECIMAL-MANDATE AST-lint is the compile-
// time layer; this is the runtime backstop).
forbid (
  principal == ReportGenerator::"finalize_action",
  action == Vault::"write_finalized_report",
  resource is GrantReportBundle
) when {
  resource has has_float_comparison_detected &&
  resource.has_float_comparison_detected == true
};

// Rule 4 — refuse_write_finalized_with_operational_data_drift_from_kfr
// Refuses finalization when operational-data sub-kind value differs
// from KFR canonical (composes with F-LOGICIAN-FACT-DRIFT family per
// v7.0.4); operator must reconcile before sign-off.
forbid (
  principal == ReportGenerator::"finalize_action",
  action == Vault::"write_finalized_report",
  resource is GrantReportBundle
) when {
  resource has has_operational_data_value_drift_from_kfr &&
  resource.has_operational_data_value_drift_from_kfr == true
};
