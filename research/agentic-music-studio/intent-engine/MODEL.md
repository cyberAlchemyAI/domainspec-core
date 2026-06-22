# Domain Model — intent-engine (v1)

DomainSpec-style typed model. Authored during `invoke refresh` because the plan-validation found the
critical gaps were **type/semantic mismatches with studio-core's real API** (G1, G3, G9, M4) — a typed
model is the tool that catches those. Every type below is checked against the real
[../build/studio_core/](../build/studio_core/) code. This model is the anchor the revised design/plan
are kept consistent with.

> **v1 scope (frozen here):** a **single-voice timbre engine on GENDYN**. No rhythm/`pattern`, no
> pitch/`scale` (studio-core has neither — those are a separate future sub-project). The human gives
> intent → the agent transliterates it to inspectable code → deterministic search tunes the GENDYN
> voice to hit measurable targets → render → human hears, reads the code, steers.

## Concepts (typed nouns)

| Concept | Type (v1) | Backed by real studio-core? | Notes |
|---|---|---|---|
| **Intent** | `str` (natural language, **closed vocabulary** v1) | — | What the human says/types. Open-vocabulary intent is the deferred LLM front-end's job, not v1. |
| **Effect** | `name + Binding` (a label, NOT a primitive — O6) | `l2_effects/gate.py` `SensationLabel` | Resolves to FeatureTargets. e.g. `darkness`, `strangeness`. Governed by the contrastive gate. |
| **Feature** | the three **readout keys** `{spectral_centroid, harmonicity_match, dissonance_minor2}` (not a code enum) | `objective.py:features_of` + `meter.py:report_features` | Exactly the three keys the real readout emits. `dissonance_minor2` is the **readout key** for the function `dissonance(P, 16/15)` (F6). No others in v1 (G3). |
| **FeatureTarget** | `(feature: Feature, op: {low,high,band}, value: float)` | `spec.py:FeatureTarget` (**requires `value`**) | Value is mandatory (G9). ⚠ **Namespace (F3):** `spec.py`'s `feature` doc-token for dissonance is `'dissonance'`, but the live readout/objective key is `'dissonance_minor2'` — `fit` maps between them. |
| **RenderCtx** | `(dur_s, sr, SpectralizeParams)` — **frozen, shared** by L1 tune + L0 render (F4) | studio-core defaults *disagree* (`Spec.dur_s=0.5` vs `search` `dur_s=0.4`) | Pinned in `program.py`; tune and render MUST share it or the meter won't match what search optimized. |
| **IntentSpec** | `(engine=GENDYN, targets: list[FeatureTarget], seed: int)` | pre-tune; not yet a studio-core `Spec` | The intent as targets, before search picks parameters. |
| **Program** | DSL text (human-readable code) | — (new `dsl.py`) | v1 grammar: `voice gendyn <effect>*` + `seed <int>`. Re-parses to an IntentSpec. **No pattern/scale.** |
| **Objective** | cost `fn(feats)->float` from FeatureTargets | `l2_effects/objective.py` `low/high/weighted` | `strangeness` cost = `weighted([(1.0, high("dissonance_minor2")), (0.5, high("harmonicity_match"))])` then minimized as `-value` (resolves G3/C3). |
| **Tune** | `search(objective) -> SearchResult`; `fit` rebuilds the walk via `make_walk(res.theta, seed)` (F6) | `objective.py:search` (**GENDYN 3-D theta only**) | Search tunes GENDYN only — the honest substrate; additive voices are render-only (G3/C2). **This is where the engineering/intelligence lives.** |
| **RealizedSpec** | studio-core `Spec{l0: GendynWalk, ...}` | `spec.py:Spec`, `realize` | The tuned, concrete, single-voice spec. `realize` → signal, deterministic. |
| **Realization** | `np.ndarray` (audio) | `spec.realize` / `gendyn.render` | Bit-identical given `(RealizedSpec, seed)` — Reading-A. |
| **MeterReadout** | `dict` (6 keys incl. `spectral_centroid_hz`, `dissonance_minor2`, `f0_hz`, `n_partials`, `note`) | `l3_evidence/meter.py:report_features` | The reverse channel (#10). Centroid becomes **analyzer-independent** once `moment_centroid` lands (Reading-B); **felt-match stays O1**. Roughness Reading-B stays UNRESOLVED until Spectralize-v2 (G2/G10/F2). |
| **Critique** | closed lexicon `str` → Edit | — (new `revise.py`) | v1 = tiny closed table; open-vocabulary critique deferred (resolves G-critique). |
| **Edit** | `(feature: Feature, direction, delta: float)` | typed mutation | A diffable change to a FeatureTarget. Never a silent multi-target guess. |

## Relationships (the pipeline as typed arrows)

```
Intent ──parse(rule-based resolver, v1)──▶ [Effect] ──resolve──▶ [FeatureTarget]
   │                                                                    │
   │                                                        author (transliterate)
   ▼                                                                    ▼
 (closed vocab)                                                      Program (DSL text, human-readable)
                                                                        │ compile
                                                                        ▼
                                                                    IntentSpec
                                                                        │ tune = search()  ◀── the intelligence
                                                                        ▼
                                                                  RealizedSpec (GendynWalk)
                                                                        │ realize
                                                                        ▼
                                                                    Realization (audio)
                                                                        │ analyze
                                                                        ▼
   Critique ──map──▶ Edit ──apply──▶ Program ◀┄┄┄┄┄ human reads code + hears + MeterReadout (steer loop)
```

## Invariants (governance)
- **I1 — no model in the sound path.** Only `parse` may (later, optionally) use an LLM; everything from
  `author` rightward is deterministic. v1 `parse` is rule-based → v1 is end-to-end model-free.
- **I2 — the intelligence is `Tune` (search), not `author`.** `author` is deterministic transliteration;
  the thesis is earned by the objective search (resolves the G4 billing inversion).
- **I3 — every Program field is sourced.** `seed` explicit; `voice`/`effects` from Intent; **no field is
  invented** (no pattern/seed guessing) → closes the LLM-reentry seam (G5).
- **I4 — Feature ∈ the three real keys; FeatureTarget carries a value.** No target references a feature
  the engine can't compute, and none is value-less (G3, G9).
- **I5 — analyzer-independence ≠ felt-faithfulness; apply the honesty symmetrically (F2).** After
  `moment_centroid` (L-pre), the centroid "darkness" reading is **analyzer-independent** on GENDYN
  (Reading-B clean) but whether it matches *felt* darkness is **O1, open** — never claim "darkness for
  real". Roughness/"strangeness" is a proxy AND not yet analyzer-independent until Spectralize-v2. Both
  features carry the proxy/O1 caveat; neither is asserted as a felt result (G2/G10).

## Open model questions (carried)
- OM1 — when Spectralize-v2 re-anchors dissonance/roughness semantics, `dissonance_minor2` and the
  `strangeness` Objective change *meaning*; freeze their values until then, treat `Tune`'s Objective
  construction as a thin adapter over studio-core features (G6).
- OM2 — "is a fixed psychoacoustic model model-free?" (F3 vs F4) decides whether I1 holds for the v2
  roughness; resolve before the "no model" prose ships (G11).
