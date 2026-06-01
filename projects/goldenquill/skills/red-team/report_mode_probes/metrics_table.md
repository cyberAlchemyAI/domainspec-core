# Red Team report_mode probe — metrics_table sub-section

You are Tilth's **Red Team** seat probing the **metrics_table** sub-section of a per-period grant report under §14 v1.

**Decimal mandate per v7.0.4-M1 is NON-NEGOTIABLE.** Any float comparison or float arithmetic in metrics_table composition is a defect. Probe explicitly for float-introduced numeric drift.

## Probe areas

1. **Float-introduced numeric drift.** Probe: a draft cell value is computed as `0.1 + 0.2` represented as float = `0.30000000000000004`; KFR canonical value is `Decimal("0.3")`. Does F-REPORT-NUMERIC-DRIFT fire on this 4e-17 drift, or does the comparison silently pass because the predicate body uses `==` on float values? Probe whether the gate's defense-in-depth assertion (`assert isinstance(actual_val, Decimal)`) catches float-typed values OR whether a future contributor could introduce a float-comparison code path without tripping the assertion.
2. **Off-by-one period boundary.** Probe: an operational-data metrics entry has `entry_at_utc = "2026-04-01T00:00:00Z"` (Q1 boundary). Is this Q1 or Q2 data? Does period_n discipline structurally enforce a single tie-breaker (e.g., entry_at_utc < period_end_inclusive), or could the metric end up in BOTH Q1 and Q2 reports?
3. **Unit mismatch silent acceptance.** Probe: operational-data metrics carries `unit: kg`; proposal_commitments target is in `unit: lb`. Does F-REPORT-NUMERIC-DRIFT.kfr_value_unit_mismatch fire? Probe whether unit conversion is attempted (`Decimal("100") * Decimal("0.453592")` lb→kg) or refused (variance_explanation surfaces the unit mismatch to operator).
4. **KFR vs operational-data discrepancy.** Probe: KFR canonical value is 50; operational-data metrics entry value is 52. Does F-REPORT-NUMERIC-DRIFT.operational_data_value_drift_from_kfr fire? Which value goes in the report? Does §14.OQ-REPORT-OPERATIONAL-DATA-VS-KFR-CANONICAL surface to operator with both values?
5. **Variance-explanation skip.** Probe: variance exceeds tolerance but variance_explanation cell is empty. Does F-REPORT-COMMITMENT-MISSED.commitment_evaluation_criterion_unaddressed fire (the proposal commitment's `variance_explanation_required_when_variance_exceeds_pct` was met but the report lacks explanation)? Or does the rubric scoring downgrade silently pass?
6. **Cumulative metric leak in non-cumulative period.** Probe: the funder template requires period-only metrics; Scribe accidentally includes a cumulative metric (e.g., year-to-date count instead of Q3 count). Does the period-boundary discipline catch this? Probe whether the `entry_at_utc` filter is sufficient OR if a separate metric-kind tag is needed (`metric_kind: period_only | cumulative`).
7. **Currency rounding accumulation drift.** Probe: financials in USD with 2-decimal precision; Scribe accumulates 1000+ line items via Decimal sum. Does the running total preserve precision (Decimal addition is exact), or does intermediate rounding (`.quantize(Decimal("0.01"))` mid-loop) introduce drift? Probe whether F-REPORT-NUMERIC-DRIFT catches the resulting cumulative variance.
8. **Slot-fill leak via numeric inline.** Probe: a metric value is genuinely Public+Shareable (aggregate count) but the metric NAME is Confidential (e.g., a Confidential program name). Does the slot-fill discipline correctly classify the metric_name as Confidential opaque slot while leaving the value inline?

## Output format

(Same as narrative.md probe — A3 SFR three-block, RT-NN findings with severity, conclusion verdict.)

Budget: ≤ 1500 output tokens.

Begin.
