# RUN-MANIFEST — 2026-06-17-spectralize-stable-readout

- **Target:** studio-core `Spectralize` (Lσ) — resolve O8.
- **Preset:** standard · **Research:** bounded-research (operator-confirmed) · **Status:** pass
- **Owner:** refine · **Subagent strategy:** recommended → authorized → 5 surveyors, all joined.
- **Source mutation:** none (`studio_core/` untouched; recommendation feeds `invoke design`).

## Canonical 10-stage loop

| # | Stage | Owner | Artifact | Receipt | Status |
|---|---|---|---|---|---|
| 1 | Context Builder | context-builder | `stages/01-context.md` | parent | pass |
| 2 | Invoke Define | invoke | `stages/02-define.md` | parent | pass |
| 3 | Interrogation (refine-review) | interrogation | `stages/03-review.md` | parent | pass |
| 4 | Research decision (bounded) | refine | `stages/04-research-survey.md` | 5 subagent returns | pass |
| 5 | Distill | distill | `stages/05-distill.md` | parent | pass |
| 6 | Invoke Redefine/Design | invoke | `RESULT.md` (recommendation) | parent | pass |
| 7 | Interrogation (refine-design-review) | interrogation | `stages/07-design-review.md` | parent | pass |
| 8 | Distill Repair | distill | `stages/08-repair.md` | parent | pass |
| 9 | Invoke Plan | invoke | `RESULT.md` (non-executed plan) | parent | pass |
| 10 | Final interrogation + synthesis | refine | `RESULT.md` | parent | pass |

## Subagent receipts (research stage)
5 surveyors (SMS, multitaper, whole-spectrum, auditory, synthesis-coupled), join policy all-join — all
returned structured C1–C5 scores + citations; condensed in `stages/04-research-survey.md`. No open agents.

## Result
`RESULT.md` — two-axis taxonomy + recommended stratified `Spectralize`-v2 (whole-spectrum moment centroid
+ peak-free critical-band roughness, over a multitaper estimator). One owner decision surfaced (fixed
perceptual model = model-free?). Next route: `invoke design` → `task-session` → re-run O8 → unblock O1.
