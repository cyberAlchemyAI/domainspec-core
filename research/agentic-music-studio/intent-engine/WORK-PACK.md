# WORK-PACK — intent-engine (refreshed)

> **Refreshed** per [development/REFRESH-REPORT.md](./development/REFRESH-REPORT.md); anchored to
> [MODEL.md](./MODEL.md). v1 = single-voice timbre on GENDYN. Next owner: `task-session`.

Package root: `research/agentic-music-studio/intent-engine/intent_engine/`; reuses `../build/studio_core/`
via `PYTHONPATH=../build`.

## SWU manifest (re-scoped)
| SWU | Parent task | Layer | Demonstrates | Depends on |
|---|---|---|---|---|
| SWU-0 | Scaffold + import studio-core (PYTHONPATH) + pytest | — | — | studio-core |
| SWU-A | `moment_centroid` in studio-core + **re-run O8 on GENDYN** | L-pre | **darkness aims honestly on the flagship voice** | SWU-0 |
| SWU-1 | DSL grammar + parser (voice+seed only, no pattern/scale) | L0 | code-language exists | SWU-0 |
| SWU-2 | Compile Program → IntentSpec + render | L0 | **a hand-written program makes music, deterministically** | SWU-1 |
| SWU-3 | `tune/fit.py` — GENDYN search fills targets (thin adapter) | L1 | **targets engineered, not guessed (the thesis)** | SWU-2, SWU-A |
| SWU-4 | `vocabulary.py` (values) + `parse.py` (closed-vocab resolver) | L2 | intent → IntentSpec, model-free | SWU-3 |
| SWU-5 | `author.py` — Effects → Program (transliteration, sourced fields) | L2 | **intent → agent-written code** (no invented fields) | SWU-4 |
| SWU-6 | `steer/session.py` — render + meter (real+proxy) + show code | L3 | the reverse channel (#10) | SWU-5 |
| SWU-7 | `steer/revise.py` — closed critique → typed Edit | L3 | menu-steering | SWU-6 |
| SWU-7b | `steer/edit.py` — **human hand-edits code → re-render** (NEW) | L3 | **the human directs by writing, not just nudging (G7)** | SWU-6 |

**Gate order:** SWU-0 → **SWU-A (L-pre gate: centroid drift < 0.05 on GENDYN)** → SWU-1,2 → SWU-3 → SWU-4,5 → SWU-6,7,7b.

## SWU details (write scope · acceptance · verify)

### SWU-0 — scaffold
- **Scope:** `intent_engine/__init__.py`, `tests/`, `conftest.py` adding `../build` to `sys.path`.
- **Accept:** `import studio_core` resolves; pytest runs. **Verify:** `PYTHONPATH=../build python -m pytest -q`.

### SWU-A — F3 moment-centroid + O8 re-run — *Lpre.1* — **honesty gate** — **UPSTREAM studio-core change (F5)**
- **Scope:** add a **full-spectrum, multitaper** `moment_centroid(signal, sr)` to
  `../build/studio_core/l1_features/features.py` (its **own studio-core commit/review** — distinct from the
  deferred Spectralize-v2 roughness re-anchor); `experiments/o8_v2_centroid.py`.
- **Accept (HYPOTHESIS to measure, not assumed — F1):** re-run the O8 grid on `moment_centroid` over GENDYN;
  **target** drift median < 0.05 (Reading-B = analyzer-independence; **felt-match is O1, separate**). The
  6.1% figure is the *peak-pick* path; if the moment path doesn't clear EPS, bank the finding + escalate
  (reassignment / longer averaging) — not a silent pass.
- **Verify:** `python experiments/o8_v2_centroid.py` → drift report with measured number + PASS/FAIL vs 0.05.

### SWU-1 — DSL parser (voice+seed) — *L0.1*
- **Scope:** `codegen/dsl.py`, `tests/test_dsl.py`. **Accept:** parse `voice gendyn dark violin` + `seed 0x5EED` → Program; round-trip; unknown effect errors; **`pattern`/`scale` tokens rejected as not-in-v1.** **Verify:** `pytest tests/test_dsl.py -q`.

### SWU-2 — compile + render — *L0.2*
- **Scope:** `codegen/compile.py`, `program.py`, `tests/test_dsl.py`. **Accept:** render bit-identical on replay (render step). **Verify:** `pytest tests/test_dsl.py -q`.

### SWU-3 — tune/fit — *L1.1* — **thesis demo**
- **Scope:** `tune/fit.py`, `tests/test_tune.py`. **Accept:** `dark` lowers centroid vs baseline (using moment-centroid), reproducible; strangeness result tagged `proxy`. **Verify:** `pytest tests/test_tune.py -q`.

### SWU-4 — vocabulary + resolver — *L2.1/L2.2*
- **Scope:** `intent/vocabulary.py` (with concrete values), `intent/parse.py`, `tests/test_authoring.py`. **Accept:** the operator sentence → IntentSpec with the 4 named `FeatureTarget`s (each with a value); unknown adjective flagged. **Verify:** `pytest tests/test_authoring.py -q`.

### SWU-5 — author — *L2.3* — **headline (honestly labeled)**
- **Scope:** `codegen/author.py`, `tests/test_authoring.py`. **Accept:** IntentSpec → DSL text that re-parses to an equivalent Program; **test asserts no Program field originates outside the IntentSpec (G5/I3).** **Verify:** `pytest tests/test_authoring.py -q`.

### SWU-6 — steer session — *L3.1*
- **Scope:** `steer/session.py`, `tests/test_steer.py`. **Accept:** prints MeterReadout (real values + proxy tags) AND the DSL source. Snapshot test. **Verify:** `pytest tests/test_steer.py -q`.

### SWU-7 — revise (closed critique) — *L3.2*
- **Scope:** `steer/revise.py`, `tests/test_steer.py`. **Accept:** "more bite" → strangeness target up → re-tune → higher `dissonance_minor2`, reproducible; unknown critique asks one question. **Verify:** `pytest tests/test_steer.py -q`.

### SWU-7b — human hand-edit — *L3.3* — **the write-side of direction (G7)**
- **Scope:** `steer/edit.py`, `tests/test_steer.py`. **Accept:** human edits the DSL text (seed or effect) → re-parse → render reflects it, reproducible. **Verify:** `pytest tests/test_steer.py -q`.

## Validation rollup
End-to-end (GENDYN voice, model-free): intent → resolver → author writes code → fit tunes (darkness reading
**analyzer-independent** via moment-centroid; strangeness proxy) → render → meter+code shown → "more bite"
OR hand-edit → revised reproducible Program. **Honest (F2):** on the flagship voice, darkness is
*analyzer-independent* (a property of the sound, not the STFT) but its *felt-match is O1, open*; strangeness
is a labeled proxy until Spectralize-v2 — the same honesty for both features. The Reading-B test (on GENDYN)
guards against false-green; it does not establish felt-faithfulness.

## Next route
`task-session` in gate order. Spectralize-v2 full roughness re-anchor → separate `invoke design`.
