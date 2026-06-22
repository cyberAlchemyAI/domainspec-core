# Refine Seed Proposal — stable Signal→P readout (resolve O8)

- **Target:** studio-core `Spectralize` (Lσ) — the Signal→P bridge that O8 showed is unstable on
  stochastic timbres.
- **Run id:** 2026-06-17-spectralize-stable-readout · **Preset:** standard · **Research:** bounded
- **Source context:** [../../../experiments/o8_report.md](../../../experiments/o8_report.md) (centroid
  drift 6–9% median on GENDYN vs 0.29% on additive control), findings.md model, definitions.md.

## Problem (one line)
Get a **reproducible, analyzer-independent** timbre reading (centroid, roughness, …) from an emergent,
inharmonic, noisy (GENDYN) signal — without a learned/generative model (C7/C8).

## Write scope
This run writes only into the run folder + a recommended `Spectralize`-v2 design/plan. No source
mutation of `studio_core/` (that is a later task-session).

## Done criteria
A **taxonomy** of candidate methods (representation axis × estimator axis), each scored against the
criteria below, and a **single recommended direction** for `Spectralize`-v2 with its trade-off named.

## Scoring criteria (tournament pareto axes)
- **C1 model-free** — no learned/generative model (hard constraint).
- **C2 stability on stochastic signal** — does it kill the analyzer-param wobble O8 found?
- **C3 perceptual faithfulness** — preserves the qualities the artisan steers (darkness, roughness).
- **C4 cost/reproducibility** — cheap, deterministic, implementable in numpy/scipy.
- **C5 GENDYN fit** — works on emergent/inharmonic/noisy spectra specifically.

## Research mode
bounded-research, confirmed by operator ("run all refine"). Local O8 evidence wins on conflict.
