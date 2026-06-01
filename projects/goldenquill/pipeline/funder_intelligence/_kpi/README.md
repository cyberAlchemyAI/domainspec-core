# _kpi/

**STATUS: DORMANT** as of 2026-05-16 per operator scope correction. The four KPI axes (win-rate uplift / time-to-funder-ready-draft / reviewer-rating delta / cost-per-win) all measure grant-drafting outcomes; no grant drafting active right now. Dashboard reactivates when grant drafting reactivates and Pillar 4 calibration produces signal.

When reactivated, the spec below applies.

---

Four-axis composite KPI dashboard per planning doc §6. Quarterly publish.

## Schema

`quarterly.jsonl` (JSON-Lines, one entry per quarter):

```json
{
  "quarter": "2026-Q3",
  "axis_a_win_rate_uplift_pct": 0.0,
  "axis_a_denominator": 0,
  "axis_b_time_to_draft_median_hrs": 0.0,
  "axis_b_baseline_median_hrs": 0.0,
  "axis_c_reviewer_rating_delta_sd": 0.0,
  "axis_c_n_pairs": 0,
  "axis_d_cost_per_win_pct_of_award": 0.0,
  "axis_d_baseline_pct": 0.0,
  "trending_up": ["a", "b", "c"],
  "trending_down_or_flat": ["d"],
  "verdict_3_of_4_passing": true,
  "notes": "free-text"
}
```

## Axes

| Axis | Definition | Baseline | Target at +6 months |
|------|-----------|----------|---------------------|
| (a) Win-rate uplift | % submitted that get funded | Operator's current 3-of-N (denominator NEEDED at project start) | +25-50% lift |
| (b) Time-to-funder-ready-draft | Operator-hours from "apply to X" to draft ready for final review | 20-40+ hrs today | <8 hrs |
| (c) Reviewer-rating delta on blinded comparison | Synthetic panel 5-dim rubric mean rating, deep-card minus shallow | 0 (baseline = same) | ≥1.0 SD higher |
| (d) Cost-per-win as % of award | Total operator-hours-equivalent + compute cost ÷ wins per quarter, as fraction of award | NEEDED at project start | <30% |

## Decision logic at +6 months (week 26)

- 3 of 4 axes trending up vs Wave-1+2 baseline → methodology validated → proceed scale-out.
- 2 of 4 → framework partial revision (which axes failed? targeted fix dispatched).
- ≤1 of 4 → framework full revision (return to planning doc §1 decisions).

## Baselines pending

Axis (a) denominator + axis (d) baseline both `NEEDED` at project start — operator-confirmed numbers go here at Phase-1 week-1.
