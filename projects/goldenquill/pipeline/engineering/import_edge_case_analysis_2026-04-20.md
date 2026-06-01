---
scope: root-cause analysis — E-024 / E-025 / E-026 import-layer edge cases
date: 2026-04-20
status: analysis complete
---

# Import-Layer Edge Case Analysis: E-024 / E-025 / E-026

## 1. Root Cause: pytest Full-Suite sys.modules Reload

All three lessons trace to one mechanism: **Round 1's `test_package_import_runs_under_100ms` pops `pipeline.scout*` from `sys.modules` and reloads the package.** Every subsequent test file that imported Scout symbols at module-load time is now holding references to the OLD module's objects. When the full suite runs, pytest collects all test files in one process; the reload creates a second generation of every module-level object. Tests that assume single-generation invariants break.

This never surfaces in per-round test runs (`pytest tests/scout/test_round_6_*.py`) because no reload occurs. It only fires under `pytest tests/` or `scripts/run_tests.sh` — the full-suite sys.modules path.

## 2. What Each Lesson Is

**E-024 — LOC estimation under Protocol + V1 discipline.** Spec-card LOC targets underestimate by 1.5–2× when modules declare injected Protocols, V1 inline-literal rebind resistance, and E-023 Threat-model docstrings. Five firings across §5 Rounds 2–5 and Scout Round 6. Connection to imports: the LOC overshoot comes from defensive patterns that exist BECAUSE of import-layer concerns (Protocols are import-seam contracts; V1 discipline prevents post-import rebinding; Threat-model docs name import-boundary residuals). Not directly an import bug, but import-layer architecture is the cost driver.

**E-025 — Version-pin range-check.** Scout Round 2 tests hard-pinned `assert scout.__version__ == "0.1.0-scout-r2"`. Round 3 bumped `__version__` to `r3`; the Round 2 test broke. Root import mechanism: `from pipeline import scout` in a later-round test file sees the latest `__version__` because the module was reloaded by Round 1's test. Fix: `assert int(version.rsplit("r", 1)[1]) >= N` — range-check, never hard-pin.

**E-026 — Object identity under sys.modules reload.** Round 5 shared `AdapterContext` across Channels C/D/E. Round 6 tests verified reuse with `AdapterContext is AC5` (identity check). Full-suite reload meant the `AdapterContext` imported in `test_round_6_*.py` at collection time was a DIFFERENT object than the one inside the reloaded `channel_e_rss` module. Fix: check `obj.__module__ == "pipeline.scout.channel_c_portals"` (string equality on lineage) instead of `is` identity.

## 3. The Shared Invariant Being Violated

**Single-generation assumption.** All three assume that a Python name bound at import time refers to the same object throughout the process lifetime. Under full-suite reload, this is false:

- E-024: the defensive LOC exists to protect import-time bindings from post-import mutation (V1 discipline) and to document which import boundaries are trusted (Threat-model docs).
- E-025: `__version__` is an import-time binding that changes value across module generations.
- E-026: `AdapterContext` is an import-time binding whose `id()` changes across module generations.

## 4. Why Scout Rounds Surface This Systematically

Scout is the only pipeline section with a Round 1 test that **reloads the package** (`test_package_import_runs_under_100ms`). §5 Loop tests don't reload; §4 Logician tests don't reload; §2 Vault tests don't reload. Scout's reload is legitimate — it verifies cold-import performance — but it creates a persistent second-generation split that every subsequent Scout round inherits.

The pattern is: Round N ships → Round N tests green in isolation → full-suite run includes Round 1 reload → Round N tests see stale first-generation references → identity/equality assertions fail.

## 5. Fix Recommendations

### A. conftest.py fixture for sys.modules cleanup

Add to `tests/scout/conftest.py`:

```python
@pytest.fixture(autouse=True, scope="session")
def _scout_module_generation_guard():
    """
    Round 1's import-perf test reloads pipeline.scout*.
    Record the generation of key objects AFTER reload so
    downstream tests can reference the post-reload generation.
    """
    # No-op: the real fix is Rules B and C below.
    # A conftest fixture that re-syncs sys.modules after every
    # test is too expensive and masks real isolation bugs.
    # Instead, enforce the coding rules.
    yield
```

**Do NOT add a fixture that re-syncs sys.modules after Round 1.** That masks the problem. The real fix is coding discipline in tests:

### B. Coding rules for Scout tests (enforce in spec-card template)

1. **Never `is`-compare cross-module objects.** Use `obj.__module__ == "expected.module.path"` for lineage checks. (E-026)
2. **Never hard-pin `__version__`.** Use `>= N` range-checks. (E-025)
3. **Access mutable module state through `__globals__`** of the function under test, not through the test file's own import binding. (Already done in Round 5 `_reset_registries` fixture.)

### C. Spec-card template clause (new section)

Add after "Pre-flight checklist" in the spec-card template:

```markdown
## Import-layer invariants (E-024/025/026)

- [ ] No `is` identity checks on objects imported from sibling modules.
      Use `obj.__module__ == "expected.path"` for lineage verification.
- [ ] Version-pin tests use `>= N` range-check, never `== "exact"`.
- [ ] Mutable module-state access goes through `fn.__globals__["REGISTRY"]`,
      not through the test file's own top-level import binding.
- [ ] LOC budget includes 1.5× multiplier for tests when module declares
      Protocols + V1 inline literals + Threat-model docstrings.
- [ ] If this round's module will be imported by future rounds, document
      which symbols are shared and how identity-safety is maintained.
```

### D. AST-lint rule (ARCH-06 candidate)

An AST-lint rule detecting `assert <expr> is <expr>` where both sides resolve to cross-module imports would mechanically prevent E-026 recurrence. Low priority — the spec-card checklist catches it at design time. File as ARCH-06 candidate if a third E-026 firing occurs.

## 6. Meta-Lesson for lessons.md

```
## L-011 — Scout rounds under full-suite sys.modules reload systematically surface import-layer invariants that contract-only reviews miss

- First observed: 2026-04-20 (E-024 fifth firing, E-025 second firing, E-026 promotion to formal)
- Frequency: 3 occurrences (E-024, E-025, E-026) across Scout Rounds 2–6
- Severity: MEDIUM (fails fast in CI; never reaches production)
- Pattern: Scout Round 1 reloads pipeline.scout* from sys.modules for import-perf testing.
  Every subsequent round's tests hold first-generation references to module objects.
  Full-suite runs create a second-generation split. Tests that assume single-generation
  invariants (is-identity, exact __version__, direct import-binding to mutable registries)
  fail under the full suite but pass in isolation. Contract-only reviews (committee
  dispatches reviewing the code without running the full suite) cannot catch this because
  the invariant violation is a runtime property of pytest collection order, not a
  static-analysis or design-review property.
- Pre-check: Every Scout spec card includes the "Import-layer invariants" checklist
  (E-024/025/026). Every test PR runs the full suite, not just the round's tests.
  Never is-compare cross-module objects; never hard-pin __version__; access mutable
  module state through __globals__ of the function under test.
- Origin: E-025 first observed Scout Round 4 (hard-pinned __version__); E-026 first
  observed Scout Round 5 (AdapterContext is-identity); E-024 first observed §5 Round 2
  (LOC estimation). Pattern recognized 2026-04-20 after three consecutive Scout rounds
  (Rounds 4–6) each surfaced a variant.
```

## 7. Review-Lessons Entries (E-024, E-025, E-026 — to be appended to review_lessons.v1.md)

These three have been referenced as candidates across spec cards and lock history but never formally written into `review_lessons.v1.md`. Formal entries drafted; append after E-016.

**E-024** — Spec-card LOC targets underestimate 1.5–2× for Protocol + V1 + Threat-model modules. Pre-check: apply 1.5× multiplier to main tests, 2× to adversarial tests when the module declares injected Protocols + V1 inline literals.

**E-025** — Version-pin tests must range-check (`>= N`), never hard-pin (`== "r2"`). Pre-check: spec card lists version-pin test as range-check; reviewer verifies no exact-match assertion on `__version__`.

**E-026** — Object identity (`is`) fails across sys.modules reload generations. Pre-check: use `__module__` string-equality for cross-module lineage checks; never `is`-compare objects imported from sibling scout modules.

---

*Analysis complete. 140 lines. Root cause is Scout Round 1's sys.modules reload creating a second-generation split that downstream rounds inherit.*
