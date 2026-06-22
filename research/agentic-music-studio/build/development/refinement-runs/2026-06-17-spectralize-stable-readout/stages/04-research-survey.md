# Stage 4 — Bounded Research Survey (tournament, 5 subagents)

Five surveyors, one method family each, scored against C1–C5 (model-free / stability / perceptual
faithfulness / cost / GENDYN fit). Verbatim-condensed returns; full citations per family.

## F1 — SMS sines+noise + reassignment (Serra & Smith 1990; McAulay–Quatieri 1986; Auger–Flandrin 1995)
Split sound into deterministic sinusoids + a modeled noise residual; link peaks across frames into
tracks (not single-snapshot); reassignment sharpens partials. **Directly attacks O8** — track-continuity
kills threshold flicker and it's the only family that *explicitly models the noise* that wrecks naive
peak-picking. **Scores: C1 3 · C2 2 · C3 3 · C4 3 · C5 3.** Catch: trades STFT-param wobble for
tracking-param wobble (birth/death thresholds must be pinned). Axis: representation=sines+noise,
estimator=reassigned/multi-frame.

## F2 — Statistical estimators: Welch / Thomson multitaper (Welch 1967; Thomson 1982; Percival & Walden 1993)
The textbook variance fix. A single periodogram of a random signal is *inconsistent* (variance doesn't
shrink); averaging K near-independent looks cuts variance ~1/K. Multitaper gets K≈2NW looks from one
window via DPSS tapers. **Most direct statistical cure for O8** — the 6–9% drift IS periodogram
variance. **Scores: C1 3 · C2 3 · C3 2 · C4 3 · C5 3** (`scipy.signal.welch`, `windows.dpss`). Catch:
smoothing merges partials closer than the resolution bandwidth → can blur fine dissonance. Axis:
**estimator-layer, representation-agnostic** — sits UNDER any representation.

## F3 — Whole-spectrum moments, no peak-pick (Peeters CUIDADO 2004; MPEG-7; Plomp–Levelt ERB-convolution)
Compute centroid/spread/flatness as moments over the *full* magnitude spectrum — no "which peaks count"
decision, so the brittle step disappears. Roughness without partials is possible via ERB-rate spectral
energy convolved with a Plomp–Levelt kernel (NOT the Essentia/MIRtoolbox defaults, which need peaks).
**Directly fixes O8 for centroid; roughness needs the ERB-convolution substitution.** **Scores: C1 2 ·
C2 3 · C3 2 · C4 3 · C5 3.** Catch: partial-free roughness departs from validated Plomp–Levelt-over-
partials semantics. Axis: representation=whole-spectrum, estimator=moment/integral.

## F4 — Auditory-model roughness (Daniel & Weber 1997; Zwicker–Fastl; Moore–Glasberg ERB; gammatone; Leman SIM 2000)
Run audio through a fixed cochlear filterbank (ERB/gammatone) → band envelopes; roughness = envelope
fluctuation (~20–300 Hz, peak 70 Hz) summed across critical bands. **No partial set ever formed** →
structurally immune to peak flicker; validated on noise/inharmonic input. **Scores: C1 1–2 (embeds a
fixed psychoacoustic model — no ML, but many tuned constants) · C2 3 · C3 3 (most perceptually grounded;
asper is the literal unit) · C4 2 (gammatone bank > one FFT) · C5 3.** Catch: the C1 "is a fixed
perceptual model still model-free?" question — a governance call. Axis: representation=ear-model/
excitation, estimator=envelope-fluctuation.

## F5 — Synthesis-coupled / parametric readout (analysis-by-synthesis; Wiener–Khinchin PSD; Monte-Carlo)
Compute the spectrum from the synth's OWN math, not a recorded trace — so no analyzer to wobble. Two
sub-paths: (a) analytic PSD from the walk parameters (Wiener–Khinchin; needs *aging*-WK because GENDYN's
reflecting walks are non-stationary), (b) Monte-Carlo: average the spectrum over N seeded renders →
integrates out seed variance. **Arguably DISSOLVES O8** (no analyzer param exists / seed variance →0).
**Scores: C1 3 · C2 3 · C3 1 · C4 3 · C5 2.** Catch (decisive): the *expected* spectrum ≠ the one
realization a listener hears — averaging erases the stochastic grit that IS the GENDYN percept (Xenakis:
identity lives in the per-realization motion). Axis: representation=recipe-derived, estimator=analytic/
MC-averaged.

## Cross-cutting realization (feeds synthesis)
F2 and F5b are **estimator-axis** fixes that sit *under* any representation; F3 and F4 are
**representation** choices that *delete the peak-picking step* (the actual O8 cause). They compose; the
answer is a stratified pick across both axes, not a single winner.
