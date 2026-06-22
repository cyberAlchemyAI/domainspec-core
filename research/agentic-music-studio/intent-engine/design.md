# Design — intent-to-code engine (Invoke `design`, refreshed)

> **Refreshed** from the plan-validation findings (G1–G12) — see
> [development/REFRESH-REPORT.md](./development/REFRESH-REPORT.md). Anchored to the typed
> [MODEL.md](./MODEL.md). v1 re-scoped to a **single-voice timbre engine on GENDYN**.

Target artifact: **intent-engine** — turns **human intent into agent-transliterated, deterministic,
inspectable code**, which deterministic search then tunes to hit measurable targets, then renders music.
The human **directs and judges** (reads, hears, hand-edits, steers). **No model is ever in the sound
path**; a model may sit only at intent-parsing (deferred in v1 → v1 is end-to-end model-free).

Owner/cycle: agentic-music-studio → intent-engine. Builds on [../build/](../build/) (studio-core).

> **The alignment.** TidalCycles already turns hand-written code into music. This project adds the layer
> above: the human says *"dark violin stochastic synth, bring strangeness"* and the agent **writes the
> code** to realize it — but the real work is **deterministic engineering (objective search against
> measurements)**, not generation. v1 proves this on the GENDYN voice the operator actually named.

## Where the intelligence lives (corrected — G4/I2)

| Step | Who | Model? | Output |
|---|---|---|---|
| Intent → Effects | rule-based **vocabulary resolver** (v1; LLM is a deferred upgrade) | no (v1) | resolved Effects (closed vocabulary) |
| Effects → Program (code) | **deterministic transliteration** (`author`) | no | DSL text — *no intelligence here; it's a template fill* |
| **Tune the GENDYN voice to hit targets** | **deterministic objective search** (`fit` → studio-core `search`) | **no** | concrete `GendynWalk` — **this is the engineering; the thesis is earned here** |
| Program → audio | the engine | no | music (reproducible) |

"The agent writes the code" = resolver + transliteration **+** the search that makes the code actually
hit the named targets. The human reads/edits every line. **No LLM emits audio.**

## v1 scope (frozen by MODEL.md)
- **Single voice, GENDYN engine.** No `pattern` (rhythm) and no `scale` (pitch) — studio-core has neither;
  they are a **named future sub-project** (sequencer + scale module), not v1 reuse (G1).
- **Honest success criterion (G2/F2):** v1 demonstrates, on the **stochastic GENDYN voice the operator
  named**: intent → agent-written code → a **darkness reading that is analyzer-independent** (Reading-B
  clean via the F3 moment-centroid — the number is a property of the *sound*, not the STFT settings;
  whether it matches *felt* darkness is **O1, still open**) → human reads/edits the code, hears it, steers.
  **Roughness/"strangeness" is shown as an explicit proxy** (measurable only to ±9% until Spectralize-v2)
  — surfaced, never asserted as a felt result. The same proxy/O1 honesty applies to *both* features (F2).

## Recorded decisions (refreshed)

| # | Decision | Choice | Note |
|---|---|---|---|
| DD1 | v1 code-language | **Single-voice timbre DSL** (`voice gendyn <effect>*` + `seed` + targets) compiling to studio-core | pattern/scale CUT from v1 (G1); real TidalCycles backend later behind `EngineSpec` |
| DD2 | Where the LLM sits | **Intent-parse only, and deferred** → v1 is rule-based, fully model-free | open-vocabulary intent = the deferred LLM's job (G8) |
| DD3 | How targets get hit | **GENDYN objective search** (studio-core `search`, 3-D theta); `fit` = thin adapter over studio-core features | search is GENDYN-only (G3); adapter shields the v2 re-anchor (G6) |
| DD4 | Human-steering | read code + hear + meter → critique (closed lexicon) **AND hand-edit the code** → re-render | hand-edit is first-class (G7) |
| DD5 | Floor dependency | **Pull the F3 moment-centroid fix in before L1** so the darkness reading is *analyzer-independent* on GENDYN (Reading-B; felt-match still O1, F2); roughness stays a stated proxy | resolves the "demo on additive only" dodge (G2). NB: the *existing* `spectral_centroid` is already a moment over the **peak-picked** `P` — the wobble is the peak-pick; F3 = a moment over the **full magnitude spectrum, bypassing `P`, multitaper-hardened** (F1) |
| DD6 | Modeling | **DomainSpec typed model** ([MODEL.md](./MODEL.md)) is the anchor; types checked vs studio-core's real API | catches the G1/G3/G9 mismatch class |

## Architecture (v1, single-voice)

```
intent_engine/
  intent/   vocabulary.py (Effect -> FeatureTarget incl. concrete values)  parse.py (closed-vocab resolver)
  codegen/  dsl.py (voice+seed grammar; NO pattern/scale)  author.py (Effects -> Program)  compile.py (Program -> IntentSpec)
  tune/     fit.py (IntentSpec -> RealizedSpec via studio-core search; thin adapter)
  steer/    session.py (render + meter + show code)  revise.py (closed critique -> Edit)  edit.py (human hand-edit -> re-parse)
  program.py  the Program + IntentSpec + seed (diffable, versioned)
```

## Operator example, end-to-end (v1, honest)
"dark violin stochastic synth, bring strangeness" → resolver emits Effects {darkness, violin-ness,
stochastic→GENDYN, strangeness(proxy)} → each resolves to a `FeatureTarget` with a concrete value
(MODEL) → `author` transliterates a 2-line Program (`voice gendyn dark violin strange` / `seed 0x5EED`) →
`fit` searches the GENDYN theta to hit low-centroid (analyzer-independent via F3) + harmonicity-match;
strangeness tuned as the proxy objective → render → human hears it, **sees "centroid 225 Hz
(analyzer-independent; felt=O1); strangeness 0.63 (proxy — judge it)"** and the 2-line code, says "more
bite" → typed Edit raises the strangeness target → re-tune. Two lines of authored code, reproducible, no
model made the sound.

## Glossary consistency
All types defined in [MODEL.md](./MODEL.md), checked against studio-core. No canonical promotion (local-only).

## Open gaps → plan
- F3 moment-centroid (full-spectrum, multitaper-hardened) must land first; its "<EPS drift on GENDYN" is a
  **hypothesis SWU-A measures**, not a known result (F1).
- OM2 (F3-vs-F4 "fixed model = model-free?") gates only the **deferred Spectralize-v2 roughness** — v1's
  centroid (F3) + Sethares dissonance are pure signal math, so v1's "no model" claim already holds (F6/m3).
- Open-vocabulary intent + critique, rhythm/pitch — all explicitly deferred, not v1 gaps.
