# Implementation Layering — intent-engine (refreshed)

> **Refreshed** per [development/REFRESH-REPORT.md](./development/REFRESH-REPORT.md); anchored to
> [MODEL.md](./MODEL.md). v1 = single-voice timbre on GENDYN; pattern/scale deferred.

Layers ordered by value/cost; each is a **demonstrable capability** reusing studio-core. Promotion gate =
"a human can do X end-to-end."

| Layer | Minimum working unit (demo) | Value | Cost | Promotion gate | Reuses |
|---|---|---|---|---|---|
| **L-pre — F3 moment-centroid** (pulled forward, G2/DD5/F1) | centroid as a moment over the **full magnitude spectrum** (bypassing the peak-picked `P`), **multitaper-hardened** | **Gating** — without it the darkness reading isn't analyzer-independent on the flagship voice | Low–med (full-spectrum moment + multitaper; from the Spectralize refine) | **hypothesis to measure:** re-run the O8 grid on `moment_centroid` → drift < 0.05 on GENDYN (not yet known — the 6.1% figure is the *peak-pick* path) | studio-core spectralize/features |
| **L0 — code-language runs** | a hand-written 2-line `Program` (`voice gendyn …` + `seed`) compiles + renders deterministically | Highest | Low (thin DSL; NO pattern/scale) | Program round-trips parse→compile→render, bit-identical on replay | studio-core engine + spec |
| **L1 — targets engineered, not guessed** | `fit` searches the GENDYN voice to hit a `dark` (centroid) target via studio-core `search` | High — **the thesis is earned here (I2)** | Med (thin adapter over `search`) | declared target → searched feature within tol, reproducible; strangeness tagged proxy | `objective.py:search` (GENDYN) |
| **L2 — intent transliterated to code** | "dark violin stochastic synth, bring strangeness" → a valid Program (closed-vocabulary resolver + template) | High — the operator-facing payoff | Med (vocabulary with concrete values) | intent → Program whose targets = the resolved Effects' FeatureTargets | the Effect vocabulary (gate, not a layer — O6) |
| **L3 — the human directs** | hear + meter + **read the code**; "more bite" → typed Edit → re-tune; **AND hand-edit the code → re-render** | High — symbiosis payoff | Med | a critique AND a hand-edit each produce a reproducible revised Program | studio-core meter (#10) |

## Boundary rationale (refreshed)
- **L-pre is new and first** — "darkness aims honestly on GENDYN" is the cheapest way to make the flagship
  demo truthful (G2); it's one estimator borrowed from the Spectralize refine, no need to wait for full v2.
- **L0 is genuinely thin now** — with pattern/scale cut, L0 is a 2-construct grammar over the existing
  single-voice engine (G1 resolved). Cost honestly Low.
- **L1 before L2** — prove the search hits targets before the agent writes programs whose trust depends on it.
- **L3 adds the write-side of direction** — hand-editing the code is first-class, not just menu-nudging (G7).

## Floor dependency (refreshed, honest — G2/G6/G10/F1/F2)
- **Centroid/"darkness":** once L-pre lands, the reading is **analyzer-independent** on GENDYN (Reading-B
  clean — a property of the sound, not the STFT settings). Whether it matches *felt* darkness is **O1,
  open** — the same honesty applied to strangeness (F2). It is NOT yet "real" in the felt sense.
- **Roughness/"strangeness":** an **explicit proxy** (measurable to ±9% on GENDYN until Spectralize-v2
  re-anchors it). The steer loop surfaces it as "proxy — judge it", never asserts the felt effect.
- **Coupling freeze (G6):** stochastic objective/vocabulary/lexicon **values** are frozen until v2; `fit`
  is a thin adapter so the v2 re-anchor is a studio-core change, not an intent-engine rewrite.
- **Reading-B (G10/F6):** the suite's load-bearing analyzer-independence check runs on the **GENDYN** voice
  (the additive voice is the stable *reference baseline*), so a green "reproducible" never masquerades as
  "timbre-faithful".

## Per-layer slices → [plan.md](./plan.md); SWUs → [WORK-PACK.md](./WORK-PACK.md).
