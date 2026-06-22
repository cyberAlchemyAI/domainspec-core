# Refine Result — intent-engine plan + specs verification

**Verdict: the refresh HELD — with residue. Ready-with-minor-fixes after a small corrective patch.**
Two tensioned reviewers (regression/fidelity + fresh-eyes attacker) checked the refreshed artifacts
against studio-core's real code.

## What held (confirmed)
- **All 12 deltas (G1–G12) landed.** 9 fully RESOLVED; 3 (G2/G10/G11) correctly *scoped* — v1 honestly
  cannot measure the stochastic flagship until Spectralize-v2, and the refresh surfaces that limit rather
  than faking a fix. **No regressions.**
- **The single-voice re-scope is faithful to the code** — studio-core genuinely has no Pattern/Scale, so
  cutting rhythm/pitch is honest, not a dodge.
- **MODEL.md is faithful** on the load-bearing types (3 readout keys, `dissonance_minor2`=`dissonance(P,16/15)`,
  GENDYN-3D-theta search, `Spec.l0: GendynWalk`, `FeatureTarget.value` required, gate shape).
- The strangeness-as-proxy labeling discipline is exemplary.

## What the verification caught (residual fixes, ranked)

| # | Sev | Finding | Fix |
|---|---|---|---|
| **F1** | CRITICAL | The artifacts call the existing centroid a "peak-pick (6.1% drift)". It's *already* a moment — the instability is the **peak-pick of `P`**. And "<0.05 on GENDYN" is asserted as known, but only the peak-pick path (6.1%) was ever measured. | Correct the description: L-pre `moment_centroid` computes the moment over the **full magnitude spectrum, bypassing `P`**, and is **multitaper-hardened** (per the Spectralize refine). Make multitaper **required**, and mark "<0.05 on GENDYN" as a **hypothesis SWU-A measures**, not a known result. |
| **F2** | CRITICAL | "darkness aims **for real**" conflates analyzer-independence (Reading-B) with felt/timbre faithfulness (O1, still open) — the exact asymmetric over-claim the schema-stress review warned against, re-committed for the easy feature. | Reword everywhere: "darkness becomes **analyzer-independent** (Reading-B clean) — the number is a property of the sound, not the STFT settings; whether it matches *felt* darkness is O1, open." Apply the same proxy honesty darkness that strangeness already gets. |
| **F3** | MAJOR | Namespace mismatch (both reviewers): `spec.py:FeatureTarget.feature` token `'dissonance'` vs the objective/meter key `'dissonance_minor2'`. | `fit.py` maps between them; document the live key is `dissonance_minor2`; note studio-core's stale docstring. |
| **F4** | MAJOR | `dur_s` default mismatch (Spec 0.5 vs search 0.4) → the meter readout won't match what search optimized. | Pin a **frozen render context** (dur_s, sr, SpectralizeParams) in `program.py`/IntentSpec, shared by L1 fit and L0 render; assert equality. |
| **F5** | MAJOR | SWU-A mutates `../build/studio_core/` (an engine with its own lifecycle); ownership/submodule boundary + relation to deferred Spectralize-v2 unstated. | Mark SWU-A an **upstream studio-core change** (own commit/review), distinct from the deferred full v2. |
| **F6** | MINOR | MODEL `Tune` arrow elides `SearchResult`→`make_walk`; OM2 (F4 model-free) only bites deferred roughness not v1's clean centroid+Sethares path; Reading-B stimulus should be GENDYN (additive is the baseline); pre-L1 renders are untuned defaults. | Small wording/scoping corrections in MODEL/plan/layering. |

## Honest note (radical candor)
F1/F2 are honesty defects **introduced in the prior refresh** — fixing the 12 gaps, I re-committed the
"overclaim the easy feature" sin on darkness while being scrupulous about strangeness. The verification
fresh-eyes lens is exactly what caught it. Worth saving as a standing check: *apply proxy/O1 honesty
symmetrically to every feature, not just the hard one.*

## Recommended next route
`invoke refresh` to apply F1–F6 (typed deltas over the 5 artifacts) → then `task-session` in gate order
(SWU-0 → SWU-A …). The Spectralize-v2 full-roughness re-anchor remains a separate `invoke design`.
