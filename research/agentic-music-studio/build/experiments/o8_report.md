# O8 — Banked Finding (L0 STOP-GATE)

**Question:** Is `Spectralize: Signal→P` reproducible **and stable** on stochastic (GENDYN) timbres?
**Verdict: CONDITIONAL FAIL.** Reproducible under frozen params (Reading A ✓); **not** analyzer-
independent (Reading B ✗). This fires the L0 stop-gate per [../implementation-layering.md](../implementation-layering.md).

Run: `experiments/o8_spectralize_stability.py` → `o8_report.json`. EPS (pass threshold) = 0.05 relative drift.

## Results

| Test | Result | Numbers |
|---|---|---|
| **T1 — re-render identity** | **PASS** | same `(walk, seed)` → identical signal → identical features |
| **T3 — param-perturbation (O8)** | **FAIL** | centroid drift **median 6.1% / max 17.9%**; dissonance drift **median 8.8% / max 17.5%** (grid over n_fft∈{512,1024,2048}, hop∈{128,256,512}, threshold∈{−50,−40,−30} dB) |
| **Control — additive voice** | (reference) | centroid drift **median 0.29%** — a clean PartialSet voice is ~20–30× more stable |

## Interpretation

Popper's review prediction is **empirically confirmed**. On a GENDYN timbre the partial set `P` is an
artifact of the analyzer parameters: holding the spec and seed fixed and changing only the STFT
window/hop/peak-threshold moves the perceptual features 6–9% (median), far above EPS. The additive-voice
control proves this is **not** a bug in the feature code — on a voice with a real partial set the floor
is rock-solid (0.29%). The instability is intrinsic to extracting discrete partials from an emergent,
inharmonic, noisy spectrum.

Two readings of "reproducible", and they diverge exactly here:
- **Reading A — frozen-params reproducibility:** PASS. With `SpectralizeParams` version-pinned, `P` (hence
  every feature) is a deterministic function of `(Spec, seed)`. The witness replays bit-identically.
- **Reading B — analyzer-independence (a feature is a property of the *timbre*):** FAIL on GENDYN. The
  feature value is partly a property of the chosen analyzer, not the sound.

## Consequence (why this is a stop-gate, not a FLAG)

The closed perceptual floor (L1) was justified as "primitive iff a pure estimator two runs reproduce
identically." On stochastic timbres that holds only in the weak Reading-A sense — which is just L0's
seed-determinism relabeled. Under Reading B the floor **degrades to signal-only** for exactly the timbre
class the operator's flagship example ("dark violin **stochastic** synth") lives in. Promoting L1 as a
*timbre-faithful* governing floor on stochastic voices is therefore **not evidence-supported as built**.

## The decision this forces (see task-session Decision Gate)

Which reproducibility standard governs the closed floor? Reading-A-is-enough (accept a modelling caveat,
proceed) vs Reading-B-required (re-architect Lσ, restrict the floor to additive voices, or demote
perceptual features to proxies). This is a modelling/governance choice for the owner, not derivable from
more measurement.

## Repair paths surfaced (not yet built)
1. **Synthesis-coupled readout** — derive `P` from the GENDYN polygon/short-time model directly rather than
   re-analyzing the output (makes `P` a property of the spec, dissolving Reading B).
2. **Restrict the closed floor to additive/`PartialSet` voices**; treat GENDYN features as explicit proxies.
3. **Accept Reading A + pin Lσ**; document every feature as analyzer-relative (governance caveat).
4. **Tighten Lσ** (longer stability filter / median-of-renders) and re-measure drift vs EPS.
