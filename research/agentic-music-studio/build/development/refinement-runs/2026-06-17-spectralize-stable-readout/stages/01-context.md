# Stage 1 — Context Builder (evidence baseline)

**Constraint carried in (memory_residue overlay):** O8 = conditional FAIL. On GENDYN, `Spectralize`
features drift centroid 6.1% median / 17.9% max, dissonance 8.8% / 17.5% under analyzer-param
perturbation; additive-voice control drifts 0.29%. Root cause: peak-picking a single STFT snapshot of a
noisy/inharmonic signal. Hard rule: no learned/generative models (C7/C8).

**Source pack:** `../../../experiments/o8_report.md`, `../../schema-stress/findings.md` (the L0·Lσ·L1·L2
model), `../../design.md` (studio-core).

**What "stable" must mean here:** reproducible AND analyzer-independent (Reading B), not just frozen-param
determinism (Reading A). Coverage: complete. No blocked context.
