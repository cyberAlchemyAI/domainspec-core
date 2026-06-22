# Stage 4 — Verification review (2 tensioned reviewers)

## Reviewer 1 — regression/fidelity (verdict: held-with-residue)
All 12 deltas present in the refreshed artifacts; **9 RESOLVED, 3 correctly scoped** (G2/G10/G11 — v1
honestly can't measure the stochastic flagship until Spectralize-v2, so the refresh *surfaces* the limit
rather than faking a fix). **No regressions.** MODEL.md faithful on the load-bearing types (3 readout keys;
`dissonance_minor2` = `dissonance(P,16/15)`; `search` = GENDYN 3-D theta; `Spec.l0: GendynWalk`;
`FeatureTarget.value` required; `SensationLabel`/gate). Two real MODEL residue items: (a) `search` returns a
`SearchResult`, not a `GendynWalk` directly (needs `make_walk(res.theta, seed)`); (b) **namespace mismatch**:
`spec.py:FeatureTarget.feature` token is `'dissonance'` but the objective/meter key is `'dissonance_minor2'`
— `fit.py` must reconcile.

## Reviewer 2 — fresh-eyes attacker (verdict: needs-rework, narrowly)
The **re-scope is clean and faithful** — studio-core genuinely has no Pattern/Scale, so cutting rhythm/pitch
is honest, and the proxy-labeling on strangeness is exemplary. But it caught a **reintroduced asymmetric
over-claim on darkness**:
- **C1 (CRITICAL):** the artifacts call the existing centroid a "peak-pick (6.1% drift)" — but `spectral_centroid`
  is *already* a moment; the instability is in the **peak-pick of `P`** (`spectralize`). The real F3 fix must
  compute the moment over the **full magnitude spectrum, bypassing `P`**, and (per the Spectralize refine) be
  **multitaper-hardened**. The plan makes multitaper "optional" and states "<0.05 on GENDYN" as if known — but
  nobody has measured a bare moment-centroid on GENDYN; the only number (6.1%) is the peak-pick path.
- **C2 (CRITICAL):** "darkness aims for real" conflates **Reading-B (analyzer-independence)** with
  **timbre-faithfulness**. Passing the O8 grid shows the number stops depending on STFT params — NOT that it
  matches felt darkness (that's O1, still open). Same asymmetric-honesty error the schema-stress review warned
  about, reintroduced for centroid.
- **M2:** SWU-A mutates `../build/studio_core/` — submodule/ownership boundary + own commit/review unstated,
  and its relation to deferred Spectralize-v2 unclear.
- **M3:** `dur_s` default mismatch (Spec 0.5 vs search 0.4) — pin a frozen render context (dur_s, sr,
  SpectralizeParams) shared by L1 fit and L0 render, or the meter won't match what search optimized.
- minor: pre-L1 renders are untuned defaults (state it); OM2 only bites the deferred F4 roughness, not v1's
  clean centroid+Sethares path; Reading-B test stimulus should be GENDYN (load-bearing), additive is the baseline.

## Convergence
Both independently flagged the **dissonance vs dissonance_minor2 namespace mismatch** (act on it). Both confirm
the re-scope/typing is faithful. Reviewer 2's C1/C2 are the high-value catch the regression lens missed: the
refresh fixed the 12 gaps but re-committed the over-claim sin on the *easy* feature (darkness).
