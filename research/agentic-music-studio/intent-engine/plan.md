# Implementation Plan — intent-engine (refreshed)

> **Refreshed** per [development/REFRESH-REPORT.md](./development/REFRESH-REPORT.md); anchored to
> [MODEL.md](./MODEL.md). Complexity: medium. v1 = single-voice timbre on GENDYN.

Companions: [design.md](./design.md), [implementation-layering.md](./implementation-layering.md),
[WORK-PACK.md](./WORK-PACK.md). Substrate: Python, reusing `../build/studio_core/` via
`PYTHONPATH=../build` (or `pip install -e ../build`) — G12.

## Validation strategy (per slice)
| Slice | Validation | Reading | Evidence |
|---|---|---|---|
| L-pre | re-run O8 grid on `moment_centroid` (GENDYN); **target** drift < 0.05 (hypothesis to measure, F1) | **B (analyzer-independence; felt-match = O1, separate)** | `o8_v2_centroid.json` |
| L0 | round-trip + render bit-identical (render step only, not DE) | A | `tests/test_dsl.py` |
| L1 | declared `dark` → searched centroid lower vs baseline; reproducible (pinned scipy) | A + the L-pre B | `tests/test_tune.py` |
| L2 | intent → Program whose FeatureTargets == resolved Effects' targets (4 named) | — | `tests/test_authoring.py` |
| L3 | critique → reproducible revised Program; hand-edit → re-render | A | `tests/test_steer.py` |

---

## L-pre — F3 moment-centroid (new; pull forward) — upstream studio-core change (F5)
> NB (F1): studio-core's *existing* `spectral_centroid` is already a moment — but over the **peak-picked
> `P`**; the O8 wobble (6.1%) is the peak-pick. `moment_centroid` is a moment over the **full magnitude
> spectrum, bypassing `P`**. This is an **upstream `studio_core` change** (its own commit/review), distinct
> from the deferred Spectralize-v2 roughness re-anchor.

### Task Lpre.1 — `moment_centroid(signal, sr)` in studio-core (ALGORITHMIC)
- **Inputs:** the realized signal. **Output:** centroid (Hz) = energy-weighted mean over ALL bins of a
  **multitaper (Thomson/DPSS) magnitude spectrum** — no peak-pick. Multitaper is **required**, not optional
  (it's the variance fix the Spectralize refine identified; a bare single-STFT moment is unvalidated on GENDYN).
- **Rules:** `centroid = Σ f_k·|X(f_k)| / Σ|X(f_k)|` over the DPSS-averaged spectrum (`scipy.signal.windows.dpss`).
- **Validation (Reading B) — HYPOTHESIS, not a known result:** re-run the O8 perturbation grid using
  `moment_centroid` on GENDYN; **target** drift median < 0.05. The only measured GENDYN number today is the
  6.1% peak-pick path — SWU-A's job is to *measure* whether the moment path actually clears EPS. If it does
  not, that is a banked finding (escalate to add reassignment/longer averaging), not a silent pass.

---

## L0 — the code-language runs (single voice)
### Task L0.1 — `dsl.py` grammar + parser (ALGORITHMIC) — G1
- **Grammar (v1, minimal):** `voice gendyn <effect>*` ; `seed <int>`. **No `pattern`, no `scale`.**
  Effects resolve via the vocabulary (unknown effect = error naming it).
- **Output:** `Program {voice_engine, effects, seed}` → re-parses to an `IntentSpec`.
- **Edge cases:** unknown effect → error; missing seed → default + warn.
- **Validation:** parse→unparse round-trip stable; golden-AST test.

### Task L0.2 — `compile.py` Program → IntentSpec → render (G12, M4, F4)
- **Inputs:** `Program`. **Output:** `IntentSpec(engine=GENDYN, targets, seed)` carrying the **frozen
  `RenderCtx{dur_s, sr, SpectralizeParams}`** (F4); render via studio-core.
- **Rules:** effects → their `FeatureTarget`s (MODEL); engine = GENDYN; seed threaded; RenderCtx attached.
  **`IntentSpec` is pre-tune; the concrete tuned `GendynWalk` is produced by L1.** A pre-L1 render uses an
  **untuned default `GendynWalk`** — it makes *a* sound (proves the language runs), not the tuned target (m1).
- **Validation:** render of a fixed `GendynWalk` is bit-identical on replay (render step only — DE/search
  reproducibility is asserted "within tol under pinned scipy", not bit-identical across BLAS, G12/M3).

---

## L1 — targets engineered, not guessed (the thesis — I2)
### Task L1.1 — `tune/fit.py` (ALGORITHMIC) — thin adapter over studio-core `search` (G3/G6)
- **Inputs:** an `IntentSpec` with `FeatureTarget`s + the **frozen render context** (F4). **Output:** a
  `RealizedSpec` (concrete `GendynWalk`).
- **Frozen render context (F4):** `fit` and the L0 render MUST share one `RenderCtx{dur_s, sr,
  SpectralizeParams}` (studio-core defaults disagree — `Spec.dur_s=0.5` vs `search` `dur_s=0.4`), or the
  meter readout won't match what `search` optimized. Pin it in `program.py`; assert equality in tests.
- **Namespace map (F3):** the objective/meter key is `dissonance_minor2`; studio-core `Spec.FeatureTarget.feature`
  doc-token is `'dissonance'`. `fit` maps `dissonance → dissonance_minor2` explicitly (the live key).
- **Ordered rules:** build a studio-core `Objective` per target using ONLY the three real readout keys:
  - `dark` → `low("spectral_centroid", value)` where centroid is the **L-pre `moment_centroid`** (full-spectrum, F1), not the partial-mean
  - `violin` → `low("harmonicity_match", value)`
  - `strangeness` → minimize `-weighted([(1.0, high("dissonance_minor2")), (0.5, high("harmonicity_match"))])`
  then run `search` over the GENDYN 3-D theta → it returns a **`SearchResult`**; rebuild the walk via
  `make_walk(res.theta, seed)` and write that `GendynWalk` into the `RealizedSpec` (F6).
- **Edge cases:** flat objective (already satisfied) → keep init + flag; infeasible → best + flag.
- **Failure modes:** strangeness/dissonance result on GENDYN is tagged **proxy** (Reading-B unresolved);
  never asserted as felt (G2/I5). `fit` touches studio-core features only through an adapter so a v2
  re-anchor doesn't rewrite this module (G6).
- **Validation:** `dark` lowers `moment_centroid` vs a 12-sample random-init baseline; reproducible within
  tol under pinned scipy (DE is not bit-identical across BLAS).

---

## L2 — intent transliterated to code (NOT generation — G4/G8)
### Task L2.1 — `intent/vocabulary.py` — Effects → FeatureTargets WITH VALUES (G9)
- Each Effect entry carries a concrete target: `darkness→low(spectral_centroid, value=<low band, e.g. 0.6×baseline>)`,
  `violin→low(harmonicity_match, 0.15)`, `strangeness→the proxy objective above (status: proxy)`,
  `stochastic→engine=GENDYN`. Values are baseline-relative where absolute Hz is unstable. Extensible via the contrastive gate (governance, not a layer — O6).

### Task L2.2 — `intent/parse.py` — closed-vocabulary **resolver** (G8)
- **Inputs:** intent text. **Output:** resolved `[Effect]` → `IntentSpec`.
- **Rules (v1 rule-based, model-free):** match known vocabulary words/phrases; **unknown adjective → ask
  or flag "not in vocabulary"** (it is a resolver, not an open-vocabulary parser; open intent = deferred LLM).
- **Edge cases:** conflicting effects (dark+bright) → surface the conflict; no known words → flag.
- **Validation:** "dark violin stochastic synth, bring strangeness" → IntentSpec with the 4 named targets.

### Task L2.3 — `codegen/author.py` — Effects → Program (transliteration; G5)
- **Inputs:** `IntentSpec`. **Output:** DSL text + parsed `Program`.
- **Rules:** template the `voice gendyn <effects>` + `seed` lines. **Every Program field is sourced
  (I3): `seed` explicit (from spec or a stated default), effects from the resolver — nothing invented.**
  Deterministic; zero generative intelligence (the engineering is L1).
- **Validation:** emitted source re-parses to an equivalent Program; a test asserts no field originates
  outside the IntentSpec (closes the LLM-reentry seam).

---

## L3 — the human directs
### Task L3.1 — `steer/session.py` — render + meter + show code
- Render → print `MeterReadout` (real values + proxy tags) AND the DSL source. Snapshot test.
### Task L3.2 — `steer/revise.py` (ALGORITHMIC) — closed critique → typed Edit (G-critique)
- **Inputs:** Program + a critique from a **tiny closed table** (`more bite`→strangeness target up;
  `too muddy`/`darker`→centroid down; `brighter`→centroid up), each with a fixed step delta, each tagged proxy/grounded.
- **Output:** revised Program (re-tuned via L1). Unknown critique → ask one clarifying question (no guess).
- **Validation:** "more bite" → strangeness target up → re-tune → measurably higher `dissonance_minor2`, reproducible.
### Task L3.3 — `steer/edit.py` — human hand-edits the code (NEW; G7)
- **Inputs:** the human's edited DSL text. **Output:** re-parsed Program → re-render.
- **Rules:** the shown DSL is a first-class editable input; a hand-edit round-trips parse→compile→render.
- **Validation:** edit `seed` or an effect in the text → re-parse → render reflects it, reproducible.

## Handoffs
- Execution → `task-session` per [WORK-PACK.md](./WORK-PACK.md) (L-pre → L0 → L1 → L2 → L3).
- Spectralize-v2 (full roughness re-anchor) → `invoke design`; **L-pre (centroid) is pulled in here**.
- Open-vocabulary intent/critique + rhythm/pitch → explicitly deferred (not v1 gaps).

## Unresolved gaps
- Invoke gaps: none blocking.
- Target gaps: L-pre EPS confirmation on GENDYN; OM2 (F3-vs-F4 model-free call, G11) before the "no model" prose; concrete target values tuned against the additive sanity case.
