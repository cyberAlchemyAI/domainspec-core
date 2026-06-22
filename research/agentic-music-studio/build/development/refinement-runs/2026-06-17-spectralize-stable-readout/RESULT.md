# Refine Result — A taxonomy of stable Signal→P methods, and the recommended fix for O8

**Plain summary.** Our problem (O8): reading a random/wiggly sound's timbre wobbles 6–9% depending on
the measuring tool's settings, because we *peak-pick partials from one spectrum snapshot* — the worst
corner for noisy sound. The research says the fix has **two independent knobs**: (1) **stop peak-picking**
— measure from the whole spectrum or from an ear-model instead; and (2) **average the spectrum** so a
random signal stops jittering (multitaper). Do both and the wobble goes away, model-free. The one real
cost: "roughness without partials" isn't the exact same recipe as before — but for random GENDYN sounds
(which have no clean partials anyway) it's arguably *more* honest.

---

## The taxonomy (two axes)

There is no single "best method" — methods live on two axes that **compose**:

**Axis A — how you represent the timbre** (the instability lives in the peak-picking step):
```
discrete partials  →  sines+noise  →  whole-spectrum  →  ear-model/excitation  →  recipe-derived
 (current, broken)     (SMS, F1)      (moments, F3)        (auditory, F4)          (synthesis-coupled, F5)
   needs peak-pick    tracks+noise    NO peak-pick          NO peak-pick            NO analyzer at all
```

**Axis B — how you estimate the spectrum** (sits *under* any representation in Axis A):
```
single snapshot  →  averaged (Welch)  →  multitaper (Thomson)  →  reassigned  →  Monte-Carlo over seeds
 (current, wobbly)    lower variance       best variance/sample     sharper        integrates seed variance
```

Our current method is the **worst corner of both**: discrete-partials × single-snapshot. Every fix is a
move rightward on one or both axes.

## Scored comparison (tournament)

| Family | Axis-A cell | Axis-B cell | C1 model-free | C2 stable | C3 perceptual | C4 cost | C5 GENDYN | Σ |
|---|---|---|:--:|:--:|:--:|:--:|:--:|:--:|
| **F1** SMS sines+noise | sines+noise | reassigned | 3 | 2 | 3 | 3 | 3 | **14** |
| **F2** Welch/multitaper | (estimator) | multitaper | 3 | 3 | 2 | 3 | 3 | **14** |
| **F3** whole-spectrum moments | whole-spectrum | moment | 2 | 3 | 2 | 3 | 3 | **13** |
| **F4** auditory roughness | ear-model | envelope-fluct | 1–2 | 3 | 3 | 2 | 3 | **12–13** |
| **F5** synthesis-coupled | recipe-derived | analytic/MC | 3 | 3 | 1 | 3 | 2 | **12** |

Totals are close *because the axes are orthogonal* — the right move is to combine, not to pick one.

## Recommendation — `Spectralize`-v2 (stratified, two-knob)

**For "darkness" (centroid):** switch to a **whole-spectrum moment** (F3) — centroid over the full
magnitude spectrum, no peak-picking. Near-deterministic on GENDYN, cheap, faithful for brightness. Clean
win, removes the instability at its source for this feature.

**For "roughness / dissonance" (the operator's "dissonance scale"):** use a **peak-free critical-band
roughness** — either the auditory-model envelope-fluctuation form (F4, Daniel–Weber lineage; most
perceptually grounded) or the ERB-convolution form (F3). No partial set, so no flicker; validated on
noisy/inharmonic input.

**Under both, harden the estimator with multitaper** (F2, Thomson/DPSS via `scipy.signal.windows.dpss`)
instead of a single STFT — the textbook variance fix. Crucially, multitaper averages *within one heard
realization*, so it lowers variance **without** erasing the per-take grit that defines the GENDYN
percept (the fatal flaw of F5's seed-averaging — keep F5 as analogy/future, not the primary fix).

**Keep the existing partial method for additive/`PartialSet` voices** — it's already stable there
(0.29% drift); the closed floor holds where a real partial set exists.

### Why this resolves O8
The wobble came from (a) peak-picking a (b) single snapshot of a noisy signal. The recommendation
removes (a) for both features and fixes (b) with multitaper — attacking both causes, staying model-free
(modulo the C1 nuance below).

### The one trade-off to name (residue)
Roughness-without-partials is a **deliberate semantic substitution**, not a drop-in: it departs from the
exact Plomp–Levelt-over-*partials* definition the "dissonance scale" was first written against. For
random GENDYN timbres — where discrete partials are arguably ill-posed — the critical-band form is
*more* appropriate, but it must be re-anchored and (eventually) checked against listeners (ties to O1).

### Governance decision this surfaces (C1 nuance)
The auditory-model roughness (F4) embeds a **fixed psychoacoustic model** (ERB filter shapes, the 70 Hz
weighting, asper calibration) — **no ML/training**, but many empirically-tuned constants. Whether that
counts as "model-free" under the project's no-models principle is a one-line owner call:
- "no *learned* models" → F4 is fine (recommended path).
- "no embedded perceptual assumptions, pure signal math only" → prefer F3's moment-centroid +
  ERB-convolution roughness and treat the auditory model as out of bounds.

---

## Non-executed plan (feeds `invoke design` for Spectralize-v2)

1. **Decision gate (owner, one line):** is a fixed psychoacoustic model "model-free"? (picks F4 vs F3 for roughness).
2. **L0/Lσ-v2 design:** new interfaces — `multitaper_spectrum(signal, NW, K)` (estimator), `centroid_moment(spectrum)` (representation), `band_roughness(signal | spectrum)` (peak-free). Keep the partial path for additive voices behind the `EngineSpec` boundary.
3. **Re-run O8** on v2: target centroid drift < EPS (0.05) on GENDYN — the same experiment, now expected to pass.
4. **Re-anchor the "dissonance scale"** to the chosen roughness; document the semantic substitution.
5. **Then** the O1 listener study can run on stable stimuli (its blocking precondition lifts).

**Recommended next route:** `invoke design` → Spectralize-v2 (carry this RESULT as the define/research
input) → `task-session` to implement → re-run O8 → unblock O1 via `research-evidence-harness`.

## Sources (by family)
F1: Serra&Smith CMJ 1990; McAulay–Quatieri IEEE TASSP 1986; Auger–Flandrin 1995. ·
F2: Welch 1967; Thomson Proc.IEEE 1982; Percival&Walden 1993. ·
F3: Peeters CUIDADO 2004; MPEG-7 ISO/IEC 15938-4; Plomp–Levelt 1965 ERB-convolution. ·
F4: Daniel&Weber Acustica 1997; Zwicker–Fastl *Psychoacoustics*; Glasberg&Moore 1990; Leman SIM 2000. ·
F5: Wiener–Khinchin / aging-WK; analysis-by-synthesis (Risset; SMS). ·
Full URLs in `stages/04-research-survey.md` and the subagent receipts.
