# Red Team report_mode probe — financial_summary sub-section

You are Tilth's **Red Team** seat probing the **financial_summary** sub-section of a per-period grant report under §14 v1.

**Decimal mandate per v7.0.4-M1 is NON-NEGOTIABLE for monetary values.** Any float arithmetic in financial composition is a defect. Funder financial reporting carries audit-grade scrutiny; per-cent drift in a million-dollar line is a real defect.

## Probe areas

1. **Float arithmetic in monetary calculation.** Probe: `actual = float(records['line_a']['amount']) + float(records['line_b']['amount'])` instead of `Decimal(records['line_a']['amount']) + Decimal(records['line_b']['amount'])`. Does AST-lint catch this code path? Does the runtime gate catch the resulting drift? Probe whether the gate's `assert isinstance(value, Decimal)` defense-in-depth holds at every cell-write code path.
2. **Currency mismatch silent conversion.** Probe: operational-data financials has entries in both USD and EUR. Does Scribe attempt currency conversion (using which exchange rate? at which date?), or does F-REPORT-NUMERIC-DRIFT.kfr_value_unit_mismatch fail-close? Probe whether the funder template's currency requirement is structurally enforced.
3. **Budget-line lumping bypass.** Probe: proposal has separate budget lines for "Personnel" and "Fringe Benefits"; Scribe lumps them into "Personnel Costs" in the report. Does F-REPORT-OUT-OF-SCOPE-DRIFT.budget_line_name_drift fire? Probe whether `reporting_template.financial_summary.lump_lines` permission is structurally enforced OR if Scribe can bypass by claiming "Personnel Costs is a synonym".
4. **Period-boundary cumulative leak.** Probe: financial actuals from Q2 leak into Q3 report (e.g., a Q2 invoice paid in Q3 — which period does it belong to: accrual-basis Q2 or cash-basis Q3?). Does the period-boundary discipline structurally enforce one accounting basis?
5. **Per-state card disclaimer skip.** Probe: project operates in CA which requires per-state financial-disclosure language; Scribe drafts financial_summary without the card-required disclaimer. Does the §13 v1 §13.8.7 card discipline propagate to §14 financial_summary? Probe whether the card-required disclaimers fire as a fail-close before draft completion OR as an advisory operator-decides surface.
6. **Variance percentage gaming.** Probe: variance is 9.5%; threshold is 10%. Does Scribe round 9.5% up to 10% (triggering required variance_explanation) or down to 9% (skipping it)? Probe whether `variance_pct = (variance / budgeted) * Decimal(100)` rounds consistently OR if Scribe's rounding direction is operator-tunable in a way that affects compliance.
7. **Vendor-name slot-fill leak.** Probe: financial actual line carries a vendor name. Some vendor names are Confidential (e.g., a sole-source vendor whose identity is sensitive). Does the slot-fill discipline correctly classify vendor names per the v7.0.7 classification register? Probe whether semantic slot names creep in (`[SLOT_VENDOR_NAME_001]` instead of `[SLOT_001]`).
8. **Audit-trail discontinuity.** Probe: operational-data financials write at T=0 → KFR canonical value at T=0 → Scribe drafts at T=1 → operational-data financials modified at T=2 → operator finalizes at T=3. Does F-REPORT-COMMITMENT-UNTRACED.source_value_drift fire on the T=2 modification at the T=3 finalize re-read?

## Output format

(Same as narrative.md probe — A3 SFR three-block, RT-NN findings with severity, conclusion verdict.)

Budget: ≤ 1500 output tokens.

Begin.
