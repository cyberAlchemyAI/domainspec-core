# O1 — Pre-Registered Criterion (FROZEN before any live run)

**Question:** Does the dissonance/inharmonicity *objective* predict perceived **"strangeness"**?
**Status:** criterion FROZEN at authoring; **live run handed off** to `research-evidence-harness`
(design DD6). This file is the pre-registration; it must not be edited after the first live datum.

## Hypothesis
The strangeness proxy `strangeness_value = 1.0·dissonance + 0.5·(harmonicity match-distance)` (over the
L1 floor) positively rank-correlates with listener-rated strangeness.

## Pre-registered success / failure criterion (fixed BEFORE running)
- **SURVIVES** iff Spearman ρ(objective_value, mean_rating) ≥ **0.40** with **p < 0.05**, at **n ≥ 20**
  raters over **≥ 8** stimuli spanning the objective range, blinded presentation order.
- **FALSIFIED** iff ρ < 0.40 or p ≥ 0.05 under the same design.
- **INVALID** iff the design cannot be run as specified (insufficient raters, broken blinding, or — see
  caveat — the underlying floor is unstable for the stimulus timbres).

## Design (built; harness validated on synthetic ratings — see `dryrun_report.json`)
- Stimuli: GENDYN voices at graded objective targets via `build_battery` (deterministic, seeded, blinded).
- Rating: per-stimulus "how strange does this sound?" 1–7 Likert; aggregate mean per stimulus.
- Scoring: `score_correlation` → Spearman ρ + p (`scipy.stats.spearmanr`).

## Hard caveat (O8 dependency — blocking)
The proxy rests on the L1 perceptual floor, whose **stability on stochastic timbres is currently
UNRESOLVED (O8 = conditional FAIL)**. If stimuli are GENDYN voices, their objective values drift 6–9%
under analyzer-param choice — which would inject measurement noise into the independent variable. **This
study should not run on stochastic stimuli until O8 is resolved** (use additive-voice stimuli, where the
floor is stable to 0.29%, OR resolve O8 first). Recorded as a precondition, not a result.

## Handoff
Live run owner: `research-evidence-harness` (run schema, rater logistics, scoring) gated by `experiment`
(this frozen criterion). Do not render SURVIVED/FALSIFIED here.
