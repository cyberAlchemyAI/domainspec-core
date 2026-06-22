# Refresh Report — intent-engine development artifacts

Invoke mode: **refresh**. Mutation mode: **applied** (operator instruction "refresh development artifacts"
= explicit approval for the upstream edit, per the no-silent-mutation gate). DomainSpec modeling applied:
**yes** ([../MODEL.md](../MODEL.md)) — the dominant signal class was type/semantic mismatch, which a typed
model resolves.

## Source signals (typed)
All deltas trace to the plan-validation refine run
`development/refinement-runs/2026-06-17-intent-engine-plan-validation/RESULT.md` (gaps G1–G12), itself
backed by 3 critic receipts. Signal type: **validation-finding**.

## Typed delta ledger

| # | Signal (gap) | Delta type | Target artifact + section | Change applied |
|---|---|---|---|---|
| D1 | G1 (pattern/scale net-new) | scope-cut | design DD1; layering L0; plan L0.1; work-pack SWU-1 | Remove `pattern`/`scale` from v1 DSL; v1 grammar = `voice gendyn <effect>*` + `seed`. Defer rhythm/pitch to a named future sub-project. |
| D2 | G2 (flagship unmeasurable) | scope-honesty + sequencing | design DD5; layering Floor-dep; plan + work-pack | v1 success criterion states what IS/ISN'T shown on GENDYN; pull the cheap **F3 moment-centroid before L1** so "darkness" aims honestly on the stochastic voice; roughness stays an explicit proxy with a stated limit. |
| D3 | G3 (search scope / no strangeness cost) | type-fix | MODEL; plan L1.1; design intelligence-table | Tune/search is **GENDYN-only**; targets map to the 3 real feature keys; `strangeness` cost defined concretely (`weighted([(1,high(dissonance_minor2)),(0.5,high(harmonicity_match))])`). |
| D4 | G4 (billing inversion) | label-fix | MODEL I2; design intelligence-table; layering L2; work-pack SWU-5 | Rename L2 to "transliterate intent → code"; state the intelligence is the L1 search, not authoring. |
| D5 | G5 (author seam / invented fields) | invariant | MODEL I3; plan L2.3 | Every Program field is sourced; `seed` explicit; no pattern/seed invention → closes LLM-reentry seam; add a test. |
| D6 | G6 (Spectralize-v2 coupling) | sequencing | layering Floor-dep; plan L1.1; design DD3 | Freeze stochastic objective/vocabulary/lexicon **values** until v2; `fit.py` = thin adapter over studio-core features. |
| D7 | G7 (steering on rails) | scope-add | plan L3; work-pack new SWU-7b | Add first-class "human hand-edits the shown DSL → re-parse → re-render" task. |
| D8 | G8 (parser is a menu) | label-fix | MODEL Intent; plan L2.2 | Demote "intent parser" → "governed vocabulary resolver"; v1 explicitly closed-vocabulary; open intent = deferred LLM. |
| D9 | G9 (no target values) | type-fix | MODEL FeatureTarget; plan L2.1 | Vocabulary entries carry concrete `value`s (or baseline-relative rule), matching the real `FeatureTarget`. |
| D10 | G10 (Reading-A only) | validation-add | plan validation table; work-pack | Add one Reading-B test (analyzer-independence on the additive control) so green ≠ false confidence. |
| D11 | G11 (F3-vs-F4 model-free gate) | dependency-flag | MODEL OM2; design open-gaps | Surface the owner decision before the "no model" prose ships. |
| D12 | G12 (paths/determinism scoping) | hygiene | plan L0.2 + validation; work-pack SWU-0 | Import via PYTHONPATH to `build/`; determinism scoped to render (not DE-across-BLAS); drop "eyeball" acceptance. |

## No-op check
The artifacts did NOT already represent these deltas (the un-refreshed plan still bills pattern/scale as
reuse and the stochastic voice as adequately mitigated). So refresh is **not** a no-op. New artifact:
`MODEL.md`. Edited: design.md, implementation-layering.md, plan.md, WORK-PACK.md.

## Next route
`task-session` on the refreshed, re-scoped work-pack; pull the Spectralize-v2 F3-centroid task earlier.

---

# Round 2 — corrective refresh (post-verification)

Source signals: the verification run
`refinement-runs/2026-06-19-intent-engine-plan-verification/RESULT.md` (fixes F1–F6), backed by 2 reviewer
receipts. Signal type: **verification-finding**. Mutation mode: **applied** (operator: "yes do the invoke
refresh"). These fix honesty defects the Round-1 refresh itself introduced (asymmetric over-claim on the
*easy* feature, darkness).

| # | Signal | Delta type | Targets | Change applied |
|---|---|---|---|---|
| F1 | centroid mischaracterized as "peak-pick 6.1%"; "<0.05" asserted as known | correctness + honesty | MODEL Feature/MeterReadout; design DD5/open-gaps; layering L-pre/floor; plan L-pre + validation; work-pack SWU-A | `moment_centroid` = moment over the **full magnitude spectrum bypassing `P`**, **multitaper required**; "<0.05 on GENDYN" reframed as a **hypothesis SWU-A measures**, not a result. |
| F2 | "darkness aims for real" conflates analyzer-independence with felt-faithfulness | honesty (symmetric) | MODEL I5; design success-criterion/example; layering floor; work-pack rollup | Darkness reading = **analyzer-independent (Reading-B)**; **felt-match = O1, open** — same proxy/O1 honesty as strangeness, applied to both features. |
| F3 | `dissonance` vs `dissonance_minor2` namespace mismatch | type-fix | MODEL FeatureTarget/Feature; plan L1.1 | `fit` maps `dissonance → dissonance_minor2` (the live key); documented. |
| F4 | `dur_s` default mismatch (Spec 0.5 vs search 0.4) | correctness | MODEL RenderCtx (new); plan L0.2/L1.1 | Frozen `RenderCtx{dur_s, sr, SpectralizeParams}` pinned in `program.py`, shared by tune + render, asserted in tests. |
| F5 | SWU-A mutates studio-core; ownership/boundary unstated | governance | plan L-pre; work-pack SWU-A | SWU-A marked an **upstream studio-core change** (own commit/review), distinct from deferred Spectralize-v2. |
| F6 | MODEL Tune arrow elides SearchResult+make_walk; MeterReadout key count; Reading-B stimulus; OM2 scope | minors | MODEL Tune/Feature/MeterReadout; layering Reading-B; design open-gaps | `search → SearchResult` then `make_walk`; Reading-B test on **GENDYN** (additive = baseline); OM2 scoped to deferred v2 roughness (v1 centroid+Sethares is pure signal math). |

**Standing lesson saved:** apply proxy/O1 honesty symmetrically to every feature, not only the hard one.
**No-op check:** not a no-op — all six were present defects; applied across MODEL + 4 artifacts.
