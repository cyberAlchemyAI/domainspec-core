# Spec card — pipeline.loop (RunState schema v2 → v3)

**STATUS:** PRE-STAGED 2026-05-10
**Round:** v7 RunState schema bump — closes blueprint/code drift surfaced by 2026-05-10 review (finding #6).
**Canonical home:** `pipeline/loop/types.py` (+ `pipeline/loop/run_pipeline.py` consumer paths)

**Framework:** per `pipeline/templates/component_analysis_template.md` (Five Laws, Four Rules, failure-mode taxonomy, standard interface pattern — not restated).

---

## 1. Blueprint anchors

- `pipeline/blueprint/v0.1/section_05_v7_amendment.md` line 44 — *"schema_version: int  # v7: bumped to 3 (red_team_verdict_ref + council_split_decision + signoff_pending_council_split)"*
- `pipeline/blueprint/v0.1/section_05_v7_amendment.md` line 70 — *"`_assert_runstate_schema_current(rs)` predicate … updated to require `schema_version == 3`; resume of a v6 RunState (`schema_version=2`) trips F-PIPE-22.runstate_schema_downgrade"*
- `pipeline/blueprint/v0.1/section_05_pipeline.md` lines 419–438 — current `RUNSTATE_SCHEMA_VERSION = 2` + `RUNSTATE_SCHEMA_VERSION_LEGACY_REJECTED = frozenset({1})` + inline-literal asserts (rebind-resistance pattern).
- `pipeline/blueprint/v0.1/section_05_pipeline.md` lines 1125–1128 — module-load `assert RUNSTATE_SCHEMA_VERSION == 2` (must bump to `3`).
- §10.6 (Red Team) — council-split inclusive-at-threshold; the v7 RunState additions exist to *persist* the council-split decision.

**Spec-card version:** v1
**Blueprint hash-at-card:** recompute on open (v7 amendment LOCKED 2026-04-19).

---

## 2. Current state (drift)

`pipeline/loop/types.py`:
- Line 495: `if self.schema_version != 2:` (POST-init validator)
- Line 504: `if RUNSTATE_SCHEMA_VERSION != 2:` (module-load rebind assert)

Blueprint says version should be 3. Code is still on 2. The `council_split_decision` and `red_team_verdict_ref` fields exist in the dataclass (run_pipeline.py:872 reads `run_state.council_split_decision`) but the schema-version constant was never bumped.

---

## 3. Scope

### 3.1 In scope (this round)

- Bump `RUNSTATE_SCHEMA_VERSION` from `2` → `3` at the canonical constant site.
- Update both inline-literal compares (POST-init validator + module-load assert) to `3`.
- Extend `RUNSTATE_SCHEMA_VERSION_LEGACY_REJECTED` from `frozenset({1})` to `frozenset({1, 2})`.
- Update the module-load `RUNSTATE_SCHEMA_VERSION_LEGACY_REJECTED == frozenset({1, 2})` rebind assert.
- Mirror the same bumps in any duplicate inline-literals (search `\b2\b` near `schema_version` in `pipeline/loop/`).
- Confirm `red_team_verdict_ref`, `council_split_decision`, and the `signoff_pending_council_split` phase string are already declared on `RunState`; if not, add as required fields per §44.
- Update `_assert_runstate_schema_current(rs)` (per blueprint §3.2.1) — must raise `F-PIPE-22.runstate_schema_downgrade` for `schema_version != 3`.

### 3.2 Out of scope

- Silent migration of v2 → v3 state on disk. Per blueprint line 70, resume of a v2 RunState **fails closed** with `F-PIPE-22`; operator runs an explicit migration tool. Migration tool is a separate spec card (not staged here).
- Schema-version compatibility window. v0.1 is single-version strict — no forward compat.
- v6 → v7 envelope schema (§1) — separate constant, separate spec.

---

## 4. Failure codes touched

- `F-PIPE-22.runstate_schema_downgrade` — already declared (blueprint §6). This card extends its trigger set: now fires on observed `schema_version ∈ {1, 2}` at resume_run. Reason-tag wording: `"observed schema_version={N} ∉ {3} (current); legacy_rejected={1, 2}"`.
- No new failure codes minted.

---

## 5. Test surface

### 5.1 Property tests
- `RunState(schema_version=3, …)` constructs cleanly (positive).
- `RunState(schema_version=2, …)` raises `F-PIPE-22` at POST-init (negative).
- `RunState(schema_version=1, …)` raises `F-PIPE-22` at POST-init (negative).
- `RunState(schema_version=4, …)` raises `F-PIPE-22` at POST-init (forward-incompat).
- Module-load rebind: `monkeypatch.setattr(types, "RUNSTATE_SCHEMA_VERSION", 99)` → re-importing the module trips the inline-literal assert.

### 5.2 Failure-code tests
- One test per legacy-rejected version (1, 2) confirming `F-PIPE-22.runstate_schema_downgrade` with the exact reason-tag.
- One test confirming `_assert_runstate_schema_current(rs)` raises when invoked on a v2 RunState (resume path).

### 5.3 Corpus tests
- Add `tests/corpus/runstate/v3/baseline.json` — minimal v3 RunState dict, asserts round-trip.
- Preserve `tests/corpus/runstate/v2/baseline.json` (if exists) as a NEGATIVE fixture — used by the F-PIPE-22 resume test.

### 5.4 Drift detection
- `BLUEPRINT_DEPS` on `types.py`: bump `hash_source_version` to `v7_amendment` and recompute the hash. Add `sections_implemented: ["§3.2.1 v7 schema bump"]`.

---

## 6. Done definition

- `pytest pipeline/loop/tests/` green.
- Full suite (`./scripts/run_tests.sh`) green — except environment-gated sovereignty tests (macOS sandbox / Keychain) which are pre-existing.
- `RUNSTATE_SCHEMA_VERSION == 3` everywhere it appears (grep clean).
- `LEGACY_REJECTED == frozenset({1, 2})` everywhere it appears.
- `_assert_runstate_schema_current` raises `F-PIPE-22` on `schema_version != 3`.
- LOC delta ±25% of naive floor.

---

## 7. Risks / open questions

- **Q1.** Does `_assert_runstate_schema_current` already exist, or is it a v5-vintage addition still pending implementation? If missing, this card needs to add the predicate AND the call site at the top of `resume_run` (§4.1). Worth a 30-second grep before the executor starts.
- **Q2.** Are there any test fixtures in `tests/corpus/runstate/` currently pinned to `schema_version=2`? They become NEGATIVE fixtures under this card; that may break tests that import them as POSITIVE. Sweep needed.
- **Q3.** Does `RunState` already carry `red_team_verdict_ref` as a field? If not, this card grows by one field-addition + tests. Confirm before estimating LOC.

---

## 8. Suggested executor

Codex (Claude Code) authoring → cross-family two-audit committee per L-005 (Editor / Judge / Red Team committee per `pipeline/engineering/engineering_process_v0.1.md` §6).
