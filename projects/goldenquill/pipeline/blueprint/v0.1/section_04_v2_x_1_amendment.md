---
title: Blueprint §4 Logician — Amendment v2.x.1 (Tilth-RT-07 PARTIAL closure — R-ARCHIVIST-NO-CANONICAL-MUTATE low-level-rename enumeration extension)
filed: 2026-05-10
operator: Josh Inklovich
amendment_status: LOCKED 2026-05-10 — narrow-corrective amendment mirroring v7.0.4-M1 precedent (lock_history row 190). L-005 strict two-cycle CLOSED with FULL live cross-family rigor (Editor=Llama-3.3-70B/Groq + Judge=Gemini-2.5-Pro/Google + Red Team=GPT-OSS-120B/Groq via openclaw bridge). Cycle 1 surfaced 22 findings (6 Editor + 1 Judge DC + 15 Red Team) → Cycle 1 fold-ins applied to module + tests + amendment text per row-170 transparent-disposition pattern. Cycle 2 verification: Editor READY_TO_LOCK (6/6 CLOSED) + Judge READY_TO_LOCK 100/100 (+2 from 98/100; all five fold-ins CLOSED) + Red Team REQUIRES_MINOR_FIXES blocking=false (RT-C2-01 LOW FOLDED-IN at LOCK with explicit text-level mechanism + RT-C2-02/03 NO-ACTION). Compound-LOCK paired-commit with §0.5 v16 amendment (Tilth-RT-07 marker row + R-ARCHIVIST-NO-CANONICAL-MUTATE enforcement-infrastructure primitive row). Ninth substantive v0.1+v0.2 round to LOCK at FULL live cross-family rigor (after WS-D v7.0.5 + WS-F §12 + WS-E §11 + WS-H §2 v7.2 + WS-G §5 v8 + WS-K §15 + WS-C-M1 v7.0.4-M1 + WS-L §4 v2.x + WS-I §13 precedents). Tilth-RT-07 structurally closed.
parent_lock: pipeline/blueprint/v0.1/section_04_v2_x_amendment.md  (§4 v2.x LOCKED 2026-05-10 row 193)
parent_lock_row: 193
predecessor_disposition_packet: pipeline/planning/section_04_v2_x_1_tilth_rt_07_backlog_2026-05-10.md  (BACKLOG_QUEUED 2026-05-10 — seed text for this amendment)
parent_disposition_row: 195
companion_lock: pipeline/blueprint/v0.1/section_15_archivist.md  (§15 v1 SPEC LOCKED 2026-05-10 row 191; §15.9.3 + §15.13.1 line 694 host the R-ARCHIVIST-NO-CANONICAL-MUTATE rule the predicate body of which this amendment extends)
amendment_class: narrow-corrective
precedent_pattern: v7.0.4-M1 corrective amendment (lock_history row 190) — both extend an already-LOCKed predicate body with new forbidden-call enumerations without modifying the parent amendment's LOCKed text in-place.
threat_severity_at_v0_1_v0_2: LOW — bounded by v7 LOCKED A4 (operator-trusted preflight); residual exploit is contributor-discipline-shaped, not adversarial under the single-operator Beta deployment threat model. Promotion to MED would require multi-contributor or v2 multi-tenant context.
purpose: Close Tilth-RT-07 PARTIAL via AST-lint enumeration extension. The §4 v2.x amendment text already enumerates `subprocess` + `os.system` + `os.popen` + `os.exec*` + `os.spawn*` + `pexpect.*` at §15.13.1 line 694; this amendment adds the five low-level rename primitives that were the residual gap (Tilth-RT-07 PARTIAL).
companion_code_landed:
  - "pipeline/linting/r_archivist_no_canonical_mutate.py (NEW — R-ARCHIVIST-NO-CANONICAL-MUTATE Rule constant + _check_archivist_no_canonical_mutate predicate body + FORBIDDEN_PRIMITIVES table; Cycle-1 RT-09 fold-in adds os.renames; Cycle-1 RT-14 fold-in wraps re-export in types.MappingProxyType; Cycle-1 DC-01 fold-in adds static-analysis-limitations docstring section)"
  - "pipeline/linting/ast_lint.py (UPDATED — _section_04_v2_x_1_rules() lazy-import block extends DEFAULT_RULES with ARCHIVIST_NO_CANONICAL_MUTATE)"
companion_tests_landed:
  - "tests/linting/test_r_archivist_no_canonical_mutate.py (UPDATED — acceptance test stub per disposition packet §3.2 + shutil.copy-family fan-out + os.link/symlink fan-out + alias resolution + scope discipline + clean-module + multi-primitive + FORBIDDEN_PRIMITIVES table coverage + live-tree regression guard + Cycle-1 RT-09 os.renames parametrize + Cycle-1 RT-14 test_forbidden_primitives_table_is_immutable + Cycle-1 RT-15 test_rule_fires_in_dead_code; 23 tests at Cycle 1 close; parametrized across 10 concrete call shapes)"
  - "tests/linting/test_ast_lint.py (UPDATED — test_default_rules_list_is_the_eight_published_constants extended to include ARCHIVIST_NO_CANONICAL_MUTATE)"
done_definition_at_cycle_1_closures_applied:
  - "Six sub-tags landed in predicate body (verified via FORBIDDEN_PRIMITIVES table inspection): low_level_rename_replace + low_level_rename_rename + low_level_rename_renames (Cycle-1 RT-09) + low_level_rename_shutil_move + low_level_rename_shutil_copy + low_level_rename_os_link."
  - "Acceptance test green (23 tests passing as of Cycle-1 close: 6 §3.2 + RT-09 parametrized acceptance + shutil.copy family fan-out + os.link family fan-out + 3 alias-resolution variants + scope discipline + clean-module + multi-primitive + table-covers-six-sub-tags + table-includes-ten-call-shapes + table_is_immutable + rule_fires_in_dead_code + live-tree regression guard)."
  - "Full lint test suite green at Cycle 1 close: 136 tests passing (was 133 pre-Cycle-1; +3 from RT-09 + RT-14 + RT-15 fold-ins)."
  - "Existing R-ARCHIVIST tests under tests/seats/archivist/ still green (rule is additive; pytest-layer skeleton tests at §15.13.1 are untouched)."
  - "ast_lint clean against the live Archivist seat tree (the shipping seat module does not import os or shutil)."
  - "Cycle 1 fold-ins applied to amendment text (this file §0 + §2 + §4 + §7 + §8 + §9 + §11 NEW); BOUNDED + DEFERRED + REJECTED dispositions registered at §11."
  - "audit_v1_synthesis.md authored at pipeline/validation/v4_v2_x_1_thesis_2026-05-10/."
  - "Daily-log entry + session-metrics row written at session close."
cowork_thesis_dispatch_status: BOTH CYCLES COMPLETE. Cycle 1: Editor + Judge + Red Team dispatched at 2026-05-10T22:47Z..22:52Z. Cycle 2 (verification): Editor + Judge + Red Team dispatched at 2026-05-10T23:01Z..23:01Z. All dispatches via mcp__Control_your_Mac__osascript → openclaw infer model run --gateway with timeout of 600 seconds. L-005 strict two-cycle CLOSED; cross-family rigor matches WS-L §4 v2.x LOCK posture (Editor=Llama-3.3-70B/Groq + Judge=Gemini-2.5-Pro/Google + Red Team=GPT-OSS-120B/Groq).
ws_dispatch: §4 v2.x.1 corrective dispatch (separate session) — modeled on v7.0.4-M1 narrow-corrective-amendment cadence (lock_history row 190).
session_metrics: pipeline/metrics/session_log.jsonl
---

# Amendment v2.x.1 — Tilth-RT-07 PARTIAL closure (R-ARCHIVIST-NO-CANONICAL-MUTATE)

## §0. Amendment intent + scope

This narrow-corrective amendment **extends** (does **not** replace) the R-ARCHIVIST-NO-CANONICAL-MUTATE predicate body landed at §4 v2.x LOCK (rows 193/194) with six low-level rename primitives (originally five per disposition packet §3.1 + `os.renames` per Cycle-1 RT-09 fold-in). The amendment does NOT modify §4 v2.x text in place; instead, per the v7.0.4-M1 precedent (lock_history row 190), the parent text remains historical and this amendment is the authoritative on-disk source for the extension.

**Composition with the existing §15.13.1 / §15.9.3 enumeration.** The Cycle-1 Editor finding E-01 surfaced reading-surface ambiguity here. To be explicit: the existing §4 v2.x §15.13.1 line 694 R-ARCHIVIST-NO-CANONICAL-MUTATE enumeration covers `subprocess` + `os.system` + `os.popen` + `os.exec*` + `os.spawn*` + `pexpect.*` + foreign-file-write-helper imports + unsafe `yaml.load` + FFI imports + dynamic-import primitives. This amendment **adds** six rename-primitive sub-tags under the same `F-ARCHIVIST-AUTO-APPLY-ATTEMPTED` failure code via a **new dedicated module** at `pipeline/linting/r_archivist_no_canonical_mutate.py`. Both the existing §15.13.1 enumeration and the new module fire under `pipeline/orchestrator/seats/archivist/**` and emit the shared `F-ARCHIVIST-AUTO-APPLY-ATTEMPTED` failure-code attribution in their diagnostic `Violation.message` bodies. The new module is registered into `pipeline.linting.ast_lint.DEFAULT_RULES` via a lazy-import block (`_section_04_v2_x_1_rules()`) mirroring the WS-L Slice 4 `_wsl_slice4_rules()` decomposition pattern (one rule per file for reading-surface coherence + minimal blast radius).

**What landed at §4 v2.x.** §15.9.3 + §15.13.1 line 694 host the existing R-ARCHIVIST-NO-CANONICAL-MUTATE enumeration:

- Direct write-intent calls (`kfr_write_intent` / `funder_intel_write_intent` / `match_db_write_intent` / `lessons_json_write_intent` / `benchmarks_write_intent`)
- Subprocess of canonical-write CLI (`subprocess.*` / `os.system` / `os.popen` / `os.exec*` / `os.spawn*` / `pexpect.*` containing `tilth` or the five canonical-write sub-commands)
- Foreign file-write helper imports (per RT-02 closure; foreign-package allowlist + dynamic-import ban)
- Raw write to non-allowed prefix
- Unsafe `yaml.load` (per RT-09 closure)
- FFI module imports (per Cycle 2 RT-01 PARTIAL + NF-05 closure)
- Dynamic-import primitives `importlib.import_module(...)` / `__import__(...)` (per Cycle 2 RT-02 PARTIAL + RT-08 PARTIAL closure)

**Tilth-RT-07 PARTIAL gap.** The existing enumeration does not cover **low-level rename primitives** that contributors could use to perform canonical-substrate writes by writing a tempfile inside an allowed-prefix path and then atomically renaming it over a forbidden canonical path. Under v7 LOCKED A1+A4 single-client + operator-trusted-preflight envelope this is contributor-discipline-shaped (the operator is the only contributor; the gap is not adversarial). Bounded promotion to MED severity would require multi-contributor or v2 multi-tenant context.

**What this amendment lands.** Six sub-tags ride under failure code `F-ARCHIVIST-AUTO-APPLY-ATTEMPTED` (the existing §15.9.3 owner), mapping ten concrete call shapes:

| Primitive (concrete Call.func shape)                                          | Sub-tag                                |
| ----------------------------------------------------------------------------- | -------------------------------------- |
| `os.replace(...)`                                                             | `.low_level_rename_replace`            |
| `os.rename(...)`                                                              | `.low_level_rename_rename`             |
| `os.renames(...)` *(Cycle-1 RT-09 fold-in)*                                   | `.low_level_rename_renames`            |
| `shutil.move(...)`                                                            | `.low_level_rename_shutil_move`        |
| `shutil.copy(...)` / `shutil.copy2(...)` / `shutil.copyfile(...)` / `shutil.copytree(...)` | `.low_level_rename_shutil_copy`        |
| `os.link(...)` / `os.symlink(...)`                                            | `.low_level_rename_os_link`            |

Sub-tag count = 6 (5 per disposition packet §3.1 + 1 from Cycle-1 RT-09 fold-in); concrete call-shape coverage = 10; failure code count = 1 (`F-ARCHIVIST-AUTO-APPLY-ATTEMPTED`).

## §1. Target glob + scope discipline

Target glob: `pipeline/orchestrator/seats/archivist/**/*.py` — narrowly scoped to the Archivist seat package, mirroring §15.9.3's existing AST-lint scope. The rule does NOT fire on modules outside the Archivist seat tree (the same primitives in `pipeline/orchestrator/seats/intake/` or `pipeline/logician/gates/` continue to be admissible; canonical-substrate write boundaries for those seats are enforced via their own §11 / §4 v2.x gates).

The narrow scope mirrors the existing R-ARCHIVIST-NO-CANONICAL-MUTATE convention. Cross-section drift (e.g., importing an `os.replace`-using helper from a foreign package) is already a §15.9.3 violation under the existing foreign-file-write-helper-import rule (RT-02 closure); this amendment does not extend that scope.

## §2. Predicate body (in pipeline/linting/r_archivist_no_canonical_mutate.py)

The predicate body lives in a new dedicated module `pipeline/linting/r_archivist_no_canonical_mutate.py`, mirroring the WS-L Slice 4 corrective-rule decomposition (one rule per file) for reading-surface coherence and minimal blast radius. The module is lazy-imported into `pipeline.linting.ast_lint.DEFAULT_RULES` via the `_section_04_v2_x_1_rules()` block, mirroring the existing `_wsl_slice4_rules()` lazy-import pattern (necessary to avoid the `Rule`/`Violation` circular-import that surfaces when `ast_lint` is invoked as `python -m pipeline.linting.ast_lint`).

The predicate body walks `ast.Call` nodes; for each call, it resolves the callable identity via a small `_resolve_callable_to_module_attr` helper that handles two shapes:

1. `ast.Attribute(value=ast.Name('os'), attr='replace')` — the canonical `os.replace(...)` call shape. The bare-name binding (`os`) resolves to its canonical module via a per-module imports table (`import os` / `import os as o` / `from os import replace`).
2. `ast.Name('replace')` — happens when the function was imported via `from os import replace`. The imports table maps the local name to `"os.replace"` and the resolver splits on the last dot to produce the `(module, attr)` pair.

Each forbidden `(module, attr)` pair maps to a sub-tag via the `FORBIDDEN_PRIMITIVES` dict (ten concrete keys → six sub-tag values). On a hit, the rule yields a `Violation` with:

- `rule_name = "R-ARCHIVIST-NO-CANONICAL-MUTATE"`
- `reason_tag = "archivist_auto_apply_attempted.<sub_tag>"` (the leading dot is preserved so the disposition-packet acceptance assertion `".low_level_rename_replace" in result.sub_tags` matches the wire representation)
- `message` body contains `F-ARCHIVIST-AUTO-APPLY-ATTEMPTED` — the failure-code attribution travels with the diagnostic regardless of how the reason_tag is read

The rule emits one `Violation` per offending `Call` node; a module with six distinct forbidden primitives produces six `Violation` rows.

### §2.1 Static-analysis limitations (intentionally out-of-scope under v7 A1+A4)

Cycle-1 closures (Judge DC-01 LOW + Red Team RT-01/02/03/04/06 HIGH/MED dynamic-call evasion class) make the rule's structural boundary explicit. The resolver handles direct `ast.Attribute` + bound `ast.Name` shapes; it does **NOT** track:

- `getattr(os, 'replace')(...)` — dynamic attribute lookup;
- `os.__dict__['replace'](...)` — subscript on module dict;
- `_x = os.replace; _x(...)` — local-name reassignment of imported callable (no data-flow pass);
- `sys.modules['os'].replace(...)` — indirect module reference via subscript;
- `from os import *` — wildcard imports (the `*` name is never entered into the imports table);
- `pathlib.Path(src).rename(dst)` / `Path(src).replace(dst)` / `Path(src).symlink_to(dst)` / `Path(src).hardlink_to(dst)` — Path-method equivalents of the forbidden primitives (resolver does not walk through constructor `Call` returns).

These shapes are bounded under **v7 LOCKED A1 (single-client) + A4 (operator-trusted preflight)** per §8 below + §11 deferred dispositions register. The amendment's threat model is **contributor-hygiene compile-time defense, not adversarial proof under a multi-tenant or untrusted-contributor envelope**. v2 multi-tenant promotion to MED severity lands via Section O.5 (architecture's "Section O.5" v2-hardening targets — not the numeric §0.5 Interface Index).

### §2.2 Dot-handling + wire-form convention (Cycle-1 E-06 closure)

The `FORBIDDEN_PRIMITIVES` table's **values** are bare sub-tag names (no leading dot): `"low_level_rename_replace"`. The rule's **emitter** prepends `"archivist_auto_apply_attempted."` to produce the wire-form `reason_tag = "archivist_auto_apply_attempted.low_level_rename_replace"`. The disposition packet's acceptance assertion (`".low_level_rename_replace" in result.sub_tags`) matches because the dot is preserved at emit time. Downstream tooling that reads `reason_tag` for sub-tag membership should rely on the dot-prefixed substring match — the wire form is stable across the §4 v2.x.1 → §15 v1.x runtime-guard boundary.

### §2.3 Immutable public table (Cycle-1 RT-14 closure)

The module exports `FORBIDDEN_PRIMITIVES` as a `types.MappingProxyType` view over the internal `_FORBIDDEN_PRIMITIVES` dict. Downstream consumers cannot accidentally (or maliciously) silence the rule by reassigning entries in the public view — `FORBIDDEN_PRIMITIVES["new"] = ...` raises `TypeError` deterministically. The internal mutable source of truth (`_FORBIDDEN_PRIMITIVES`) remains module-private. Acceptance test `test_forbidden_primitives_table_is_immutable` asserts this contract at the test surface.

## §3. Acceptance test (in tests/linting/test_r_archivist_no_canonical_mutate.py)

The acceptance test surface mirrors the disposition packet §3.2 stub adapted to the actual `lint_tree`-based API (the stub's `ast_lint_archivist_seat_source` / `make_module_with` helpers do not exist on disk; this amendment uses `lint_tree` + a `_write` fixture helper per the `tests/linting/test_ast_lint.py` convention).

- `test_r_archivist_no_canonical_mutate_enumerates_low_level_rename_primitives` (the §3.2 disposition stub realized) — parametrized across the six primitives (5 per §3.2 + `os.renames` per Cycle-1 RT-09 fold-in) with `pytest.param(... id=...)` for readable per-primitive test IDs; asserts exactly-one violation per synthetic module + sub-tag presence in `reason_tag` + failure-code presence in `message`.
- `test_shutil_copy_family_all_map_to_shutil_copy_sub_tag` — verifies `copy / copy2 / copyfile / copytree` collapse to a single sub-tag.
- `test_os_link_family_all_map_to_os_link_sub_tag` — verifies `link / symlink` collapse to a single sub-tag.
- `test_rule_resolves_module_import_aliases` — `import os as o; o.replace(...)` still fires.
- `test_rule_resolves_from_import_aliases` — `from os import replace; replace(...)` still fires.
- `test_rule_resolves_from_import_with_asname` — `from shutil import move as m; m(...)` still fires.
- `test_rule_does_not_fire_outside_archivist_seat` — modules under `seats/intake/` are unaffected.
- `test_clean_archivist_module_passes` — a module that uses none of the forbidden primitives produces zero violations.
- `test_multiple_primitive_calls_emit_one_violation_each` — a module with six distinct forbidden primitive calls (Cycle-1 RT-09 fold-in extends from five → six) produces six violations with all six distinct sub-tags.
- `test_forbidden_primitives_table_covers_six_sub_tags` — table introspection asserts the sub-tag closure equals the post-Cycle-1 six-element set (§3.1 five + RT-09 `low_level_rename_renames`).
- `test_forbidden_primitives_table_includes_all_ten_call_shapes` — table introspection asserts the call-shape closure is the post-Cycle-1 ten-element set (§3.1 nine + RT-09 `("os", "renames")`).
- `test_forbidden_primitives_table_is_immutable` *(Cycle-1 RT-14 closure)* — asserts the `MappingProxyType`-wrapped public view refuses `__setitem__` / `clear` / `del` with `TypeError`.
- `test_rule_fires_in_dead_code` *(Cycle-1 RT-15 closure)* — asserts `if False:` forbidden primitive still fires (AST-lint is structural, not flow-sensitive — confirms expected behavior).
- `test_live_archivist_seat_tree_passes_default_rules` — live-tree regression guard against the shipping Archivist seat package (the v0.2 SPEC LOCK skeleton does not use any forbidden primitive; this test prevents future drift).

## §4. Runtime-guard wrapper extension note (§15.9.3 line 521 — for §15 v1.x first ship)

Per disposition packet §3.3 and Tilth-RT-07 PARTIAL acceptance criterion §4.4: the runtime guard wrapper layer at §15.9.3 line 521 (currently wraps `open()` + `pathlib.Path.write_text` / `pathlib.Path.write_bytes` with the allowed-prefix-set check) MUST be extended at §15 v1.x first ship to also wrap:

- `os.replace`
- `os.rename`
- `shutil.move`

**Single source of truth (Cycle-1 E-02 + RT-12 closure — operationally specific).** The forbidden-call set lives in `pipeline/linting/r_archivist_no_canonical_mutate.py:_FORBIDDEN_PRIMITIVES` (internal mutable source) exported as `FORBIDDEN_PRIMITIVES` (public `MappingProxyType` view). When the §15 v1.x amendment realizes the runtime guard wrapper extension, the wrapper set MUST be derived from (or test-equivalent to) `FORBIDDEN_PRIMITIVES`. Drift between the two layers (AST-lint forbidden-call set ≠ runtime-guard wrapper set) is itself a structural defect.

**Named drift test (binding contract for v1.x amendment author):**

- **Test file path:** `tests/seats/archivist/test_runtime_guard_wrapper_drift.py`
- **Test function:** `test_runtime_guard_wrapper_set_mirrors_forbidden_primitives_keys`
- **Assertion form:** `assert set(runtime_wrapper_forbidden_keys) == set(FORBIDDEN_PRIMITIVES.keys())`, where `runtime_wrapper_forbidden_keys` is the v1.x runtime-guard wrapper's public surface that the §15 v1.x author introduces.
- **Owner:** the v1.x amendment author (whoever LOCKs §15 v1.x first).
- **Fires:** at pytest collection time during the v1.x LOCK suite; v1.x LOCK ceremony **MUST NOT** complete with this test red or absent.

This is a **named, location-binding contract**, not a soft commitment — the path + function name + assertion form are normative. Drift detected mid-v1.x is itself a `F-INDEX-STALE`-class defect.

**Test-file existence at §4 v2.x.1 LOCK (Cycle-2 RT-C2-01 closure).** The drift test file does **NOT** exist on disk at §4 v2.x.1 LOCK — this is intentional. The §15 v1.x amendment + the runtime-guard wrapper that the test pairs with are v1.x deliverables; the runtime guard's wrapping surface (`runtime_wrapper_forbidden_keys`) is defined by the v1.x author, not by this amendment. Creating the file as a v0.2 skeleton stub would either (a) raise `NotImplementedError` deterministically at pytest collection time and force §4 v2.x.1 LOCK to ship with a known-red test in the suite, or (b) assert against a non-existent wrapper surface and falsely turn green. Neither preserves the contract. The contract is a **forward-binding requirement on v1.x**: at v1.x LOCK ceremony the file must exist, the function name must match, the assertion form must hold, and v1.x amendment frontmatter must cross-reference back to this §4 v2.x.1 §4 binding contract. Mirrors the §15 v1 v0.2 SPEC-ONLY discipline pattern where v1.x deliverables are named at v0.2 SPEC LOCK without being implemented at v0.2 LOCK time.

**Why `shutil.copy*` and `os.link / os.symlink` are AST-lint-only at v0.2 / v0.1.** The four `shutil.copy*` primitives and the two link primitives are file-creation rather than file-overwrite primitives; the residual exploit (copy-then-overwrite via subsequent write) is already caught by the existing §15.9.3 runtime open-shim against canonical-substrate paths. AST-lint enumeration captures the contributor-discipline boundary at compile time; runtime-guard wrapping of the link primitives is a **defense-in-depth note** at §15 v1.x first ship — see the v1.x amendment-realization checklist below for the SMART form (Cycle-1 E-03 + RT-11 tightening).

**v1.x amendment-realization checklist row (cross-reference back to this amendment) — SMART form (Cycle-1 E-03 + RT-11 closure):**

```
[ ] §15.9.3 line 521 runtime guard wrapper extended to os.replace + os.rename + shutil.move
    (acceptance: wrapper accepts these three primitives + raises FileSystemError-or-equivalent
     when destination resolves to a forbidden canonical path).
[ ] Drift test added at tests/seats/archivist/test_runtime_guard_wrapper_drift.py
    (function: test_runtime_guard_wrapper_set_mirrors_forbidden_primitives_keys;
     assertion: set(runtime_wrapper_forbidden_keys) == set(FORBIDDEN_PRIMITIVES.keys())).
[ ] shutil.copy* / os.link / os.symlink wrapping decision recorded in §15 v1.x amendment text:
    EITHER (a) wrap them (recommended; matches FORBIDDEN_PRIMITIVES surface) and update the
    drift test to require keys-equality across all ten call shapes, OR (b) document the
    OPTIONAL-by-cost-analysis decision with a structured operator-discipline-cost calculation
    (which contributor patterns the operator must catch by visual review) — flag-cleared by
    explicit operator sign-off at v1.x LOCK ceremony.  No "OPTIONAL" status survives v1.x LOCK
    without a written cost analysis.
[ ] Cross-reference back to pipeline/blueprint/v0.1/section_04_v2_x_1_amendment.md §4 in the
    §15 v1.x amendment frontmatter.
```

## §5. Failure-code table

| Code                            | Tier | Module                                                   | Severity | Cycle             |
| ------------------------------- | ---- | -------------------------------------------------------- | -------- | ----------------- |
| `F-ARCHIVIST-AUTO-APPLY-ATTEMPTED` (sub-tag `.low_level_rename_*` — five sub-tags) | PRE-write (AST-lint at build time) | `pipeline/linting/r_archivist_no_canonical_mutate.py` | HIGH (inherits §15.9.3 severity) | §4 v2.x.1 Tilth-RT-07 PARTIAL closure 2026-05-10 |

No new top-level failure-code row is registered (sub-tags only). The §15.9.3 owner remains the authoritative failure-code owner. The §0.5 row count is UNCHANGED at the §4 v2.x amendment's range (305-348 inclusive of §4 v2.x slices 1-4; this amendment is sub-tag scoped and does not row-append).

## §6. PRE-gate row addition

| Order  | Check ID                                | Fires at                                               | Failure code                       | Bypass |
| ------ | --------------------------------------- | ------------------------------------------------------ | ---------------------------------- | ------ |
| PRE-(n/a — AST-lint at build time) | R-ARCHIVIST-NO-CANONICAL-MUTATE (low-level-rename extension) | every `ast.Call` in `pipeline/orchestrator/seats/archivist/**/*.py` against a forbidden primitive | `F-ARCHIVIST-AUTO-APPLY-ATTEMPTED.low_level_rename_<flavor>` | M13 (audited; HIGH-severity admin-risk) |

AST-lint runs at build time as part of `scripts/run_lint.sh`; failure of the rule fails the build (the build never reaches a runnable state). M13 bypass requires the standard `--bypass-flagcheck` operator gesture audited per §4 v2.x §4.16 dispatcher contract.

## §7. Verification + dispatch posture

**Code-phase verification (this session — Cycle 1 close):**

- 10 concrete primitive call shapes verified via .venv/bin/python3 (3.14) pytest at `tests/linting/test_r_archivist_no_canonical_mutate.py` — 23 tests passing (6 §3.2 + RT-09 parametrized acceptance + 4 shutil.copy fan-out + 2 os.link fan-out + 3 alias-resolution + scope-discipline + clean-module + multi-primitive + table-covers-six + table-includes-ten + table-is-immutable + dead-code + live-tree-regression).
- Alias resolution verified across three shapes: `import os as o`, `from os import replace`, `from shutil import move as m`.
- Multi-primitive emission verified: a module with six distinct forbidden calls produces six distinct sub-tags.
- Clean-module assertion verified: a module using only `pathlib.Path.write_bytes` produces zero violations.
- Out-of-scope discipline verified: `seats/intake/`-pathed modules do not fire.
- Live-tree regression guard verified: the shipping Archivist seat module passes `DEFAULT_RULES` clean (no `os` / `shutil` imports in the v0.2 SPEC LOCK skeleton).
- Immutable table verified: `FORBIDDEN_PRIMITIVES[k] = v` raises `TypeError` deterministically (RT-14 fold-in).
- Dead-code structural-walk verified: `if False: os.replace(src, dst)` still triggers the rule (RT-15 fold-in).
- Full lint test suite green: 136 tests passing (was 133 pre-Cycle-1; +3 from os.renames parametrize + immutability + dead-code).
- `scripts/run_lint.sh pipeline/orchestrator/seats/archivist/` exit 0.

**Cowork Thesis dispatch (next session):**

L-005 two-cycle cadence applies; cross-family rigor matches WS-L §4 v2.x LOCK posture per the parent amendment's `cross_family_posture: LIVE FULL CROSS-FAMILY` row. Editor / Judge / Red Team dispatched via the openclaw gateway per `pipeline/validation/v7_0_5_thesis_2026-05-09/dispatch_audit_v{1,2}.sh` template. Audit scope:

- Predicate correctness vs. disposition packet §3.1 sub-tag mapping.
- Test coverage vs. §3.2 acceptance criterion (the parametrized test is the load-bearing acceptance row).
- Scope discipline (rule fires only under `pipeline/orchestrator/seats/archivist/**`; out-of-scope modules unaffected).
- Single-source-of-truth discipline (FORBIDDEN_PRIMITIVES drives both layers; v1.x amendment-realization checklist row at §4 is the contract).
- Threat-model boundary preservation (v7 LOCKED A1+A4 single-client + operator-trusted preflight; promotion to MED bounded to v2 multi-tenant per Section O.5).
- No semantic delta vs. §15.9.3 line 521 / §15.13.1 line 694 (the existing pytest-layer skeleton tests remain green and authoritative for their respective scopes).

## §8. Threat-model boundaries (interim posture; Cycle-1 E-04 + RT-13 closure — explicit progression)

The amendment's stated severity is **LOW at v0.1+v0.2** because the threat model is **contributor-hygiene compile-time defense under v7 LOCKED A1 (single-client) + A4 (operator-trusted preflight)**, not adversarial proof under a multi-contributor or multi-tenant envelope. The rule's resolver is intentionally conservative per §2.1; the dynamic-call evasion classes documented at §2.1 are bounded by A4 and routed to Section O.5 v2 multi-tenant per the row-170 transparent-disposition pattern. Promotion to HIGH severity at v0.1+v0.2 would reject the parent disposition packet (row 195) and the §8 amendment text in equal measure — both are evidence of the bounded threat-model claim, not contradictions of it.

**Three-stage progression:**

- **v0.1 + v0.2 single-operator Beta deployment** (current — see §16 v0.1 Beta gate cleared at WS-L LOCK row 193/194): bounded by v7 LOCKED A4 (operator-trusted preflight). Operator is the only contributor; contributor-discipline gap is not adversarial-exploitable. AST-lint enumeration extension is contributor-hygiene, not adversarial-defense. The dynamic-call evasion classes at §2.1 + the Path-equivalent and low-level-file-handle gaps at §11 are bounded under this envelope — they are NOT v0.1+v0.2 fail-closed gates.

- **v1.x first-ship** (next horizon): bounded by v7 LOCKED A1 (single-client) + A4 (operator-trusted). Same boundary applies — the gap remains contributor-discipline-shaped. The runtime-guard wrapper extension at §4 of this amendment is the v1.x first-ship layer that elevates the gap from "build-time-only" to "build-time + runtime" for `os.replace` / `os.rename` / `shutil.move` (defense-in-depth). The `shutil.copy*` / `os.link` / `os.symlink` wrapping decision is a v1.x amendment-realization checklist item with explicit operator-discipline-cost analysis required before OPTIONAL retirement per §4.

- **v2 multi-tenant** (Section O.5 horizon — architecture's v2-hardening targets section, NOT the numeric §0.5 Interface Index): the gap promotes to MED severity (multi-contributor + multi-tenant context can exploit). The bounded findings at §11 (RT-01/02/03/04/06 dynamic-call evasion + RT-07/08 Path-equivalents + RT-10 low-level file-handle primitives) all promote to v2-active hardening targets. Section O.5 v2 multi-tenant amendment author must verify §4 v2.x.1 LOCK + §11 deferred-dispositions register + the §15 v1.x runtime-guard wrapper presence before declaring §15 hardened for v2 deployment.

**Why severity stays LOW at v0.1+v0.2 even with the §2.1 / §11 documented gaps.** Promoting the severity would imply the rule must close all evasion classes to be useful. That conflates two things: a *security guarantee against an adversarial contributor* (which the rule does not claim to provide at v0.1+v0.2 under A4) versus a *contributor-discipline compile-time check that catches accidental misuse of rename primitives* (which the rule does provide). The first is v2 multi-tenant scope; the second is the rule's actual brief. The §2.1 + §11 documentation is **evidence of bounded scope**, not evidence of unmitigated risk.

## §9. Acceptance criterion (closes Tilth-RT-07; Cycle-1 E-05 closure — criteria operationally distinct)

§4 v2.x.1 LOCK ceremony asserts each criterion independently:

1. **On-disk table assertion.** The six sub-tags (`low_level_rename_replace`, `low_level_rename_rename`, `low_level_rename_renames` *(Cycle-1 RT-09 fold-in)*, `low_level_rename_shutil_move`, `low_level_rename_shutil_copy`, `low_level_rename_os_link`) are registered in the `R-ARCHIVIST-NO-CANONICAL-MUTATE` predicate body via the `_FORBIDDEN_PRIMITIVES` table in `pipeline/linting/r_archivist_no_canonical_mutate.py`. Verification = test introspection at `test_forbidden_primitives_table_covers_six_sub_tags` + `test_forbidden_primitives_table_includes_all_ten_call_shapes`.
2. **Acceptance-test execution.** The acceptance test `test_r_archivist_no_canonical_mutate_enumerates_low_level_rename_primitives` (parametrized across six primitives: §3.2 five + RT-09 `os.renames`) is green in the §4 LOCK suite. Verification = full lint test suite pytest run at Cycle-2 close.
3. **Amendment text enumeration.** The §4 v2.x.1 amendment text enumerates the six low-level rename primitives explicitly, with the sub-tag mapping shown verbatim (§0 table above + Appendix A). This is distinct from criterion #1 (which is the on-disk table) — criterion #3 is the **reading-surface contract** for future v1.x amendment authors and downstream consumers who read the amendment without inspecting the code. Drift between criterion #1 (table) and criterion #3 (text) is itself a §4 v2.x.1 defect; Appendix A naming the module file as canonical resolves the tie.
4. **v1.x amendment-realization checklist binding.** The runtime-guard wrapper extension note for `os.replace` / `os.rename` / `shutil.move` is recorded at §4 of this amendment with the named drift test (`tests/seats/archivist/test_runtime_guard_wrapper_drift.py::test_runtime_guard_wrapper_set_mirrors_forbidden_primitives_keys`) bound to it. Cross-reference back from §15 v1.x amendment frontmatter binds the contract; v1.x LOCK ceremony must not complete with the drift test red or absent.
5. **Cycle-1 fold-in completeness.** The Cycle-1 fold-ins (RT-09 `os.renames` enumeration + RT-14 `MappingProxyType` immutability + RT-15 dead-code structural-walk) are all landed in module + tests + this amendment text. Verification = tests + diff against Cycle-1 synthesis at `pipeline/validation/v4_v2_x_1_thesis_2026-05-10/audit_v1_synthesis.md`.

## §10. Cross-references

- Parent §4 v2.x LOCK: `pipeline/blueprint/v0.1/section_04_v2_x_amendment.md` (rows 193/194; LOCKED 2026-05-10).
- Disposition packet (predecessor seed): `pipeline/planning/section_04_v2_x_1_tilth_rt_07_backlog_2026-05-10.md` (BACKLOG_QUEUED 2026-05-10; row 195).
- Companion §15 LOCK (predicate-body home for the AST-lint rule's spec): `pipeline/blueprint/v0.1/section_15_archivist.md` §15.9.3 + §15.13.1 line 694 (rows 191/192).
- Narrow-corrective precedent pattern: `pipeline/architecture/v0.1/architecture_v7_0_4_M1_amendment.md` (lock_history row 190).
- WS-L dispatch handoff (closed): `pipeline/planning/v0_2_dispatch_plan_2026-05-09.md` §WS-L (post-LOCK note pointing to the §4 v2.x.1 backlog file remains accurate; this amendment is the realization of that backlog).
- Audit trail (Cycle 1 + Cycle 2): `pipeline/validation/v4_v2_x_1_thesis_2026-05-10/` — common header + per-seat prompts + per-seat raw + extracted markdown + synthesis files.
- Lock history row (when LOCKed via Cowork Thesis): TBD at LOCK ceremony.

## §11. Bounded findings + deferred dispositions (Cycle-1 row-170 transparent pattern)

Per the row-170 transparent disposition pattern (v7.0.4-M1 row 190 + WS-D v7.0.5 row 179 + WS-B v7.0.7 row 180 + §15 v1 rows 191/192 + WS-L §4 v2.x rows 193/194 + WS-I §13 rows 196/197 precedents): Cycle 1 surfaced findings that are NOT fold-in edits at this LOCK. Each is registered transparently with its disposition + destination.

### §11.1 BOUNDED-by-v7-A1+A4 (dynamic-call evasion class — Section O.5 v2 promotion path)

These findings document **dynamic-call evasion** classes that the AST-lint resolver intentionally does NOT track under v7 LOCKED A1 (single-client) + A4 (operator-trusted preflight). They are bounded at v0.1+v0.2; promotion to MED severity lands at v2 multi-tenant via Section O.5.

| Cycle-1 ID | Severity at LOCK | Probe | Disposition |
|---|---|---|---|
| RT-01 | BOUNDED-LOW | `getattr(os, 'replace')(src, dst)` — dynamic attribute lookup | Documented at §2.1; bounded by A4; v2 Section O.5 multi-tenant promotion path. |
| RT-02 | BOUNDED-LOW | `os.__dict__['replace'](src, dst)` — subscript on module dict | Same class as RT-01; bounded by A4. |
| RT-03 | BOUNDED-LOW | `_x = os.replace; _x(src, dst)` — local-name reassignment | Same class as RT-01; AST-lint is not flow-sensitive per §2.1. |
| RT-04 | BOUNDED-LOW + NF-DD-04 | `from os import *; replace(src, dst)` — wildcard import | Same class as RT-01; NEW defense-in-depth note (NF-DD-04) for §15 v1.x amendment author: consider adding a separate R-ARCHIVIST-NO-WILDCARD-IMPORT rule or extending an existing import-discipline rule. |
| RT-06 | BOUNDED-LOW | `sys.modules['os'].replace(src, dst)` — indirect module reference | Same class as RT-01; resolver does not walk subscripts. |

### §11.2 DEFERRED to follow-on amendment

| Cycle-1 ID | Severity at LOCK | Probe | Routing |
|---|---|---|---|
| RT-07 | DEFERRED-MED + NF-DD-05 | `pathlib.Path(src).rename(dst)` / `Path(src).replace(dst)` — Path-method equivalents of the forbidden primitives | Requires resolver work for Path-method analysis (resolver must walk through constructor `Call` returns to recognize the result as a Path). Routed to a follow-on §4 v2.x.2 corrective amendment OR a new disposition packet that opens the Path-equivalents scope. Bounded interim under A4. |
| RT-08 | DEFERRED-MED + NF-DD-05 | `pathlib.Path(src).symlink_to(dst)` / `Path(src).hardlink_to(dst)` — Path-method link equivalents | Same routing as RT-07. |
| RT-10 | DEFERRED-LOW | `os.open(tmp, ...)` + `os.fdopen(fd, 'w').write(data)` + `os.replace(tmp, dst)` — low-level file-handle primitives bypass open-shim chain | File-handle primitives are out-of-scope for §4 v2.x.1's rename-enumeration brief. Routed to §15 v1.x runtime-guard expansion (the `os.replace` final step is already caught by this amendment; the bypass chain's `os.open` is a separate enumeration class that requires its own disposition). Bounded interim under A4. |

### §11.3 REJECTED-with-rationale

| Cycle-1 ID | Severity claimed | Probe | Rejection rationale |
|---|---|---|---|
| RT-13 | LOW (Red Team) | "Threat-model claim of LOW severity assumes the rule covers all rename pathways." | Premise contradicted by §8 amendment text + parent disposition packet §2.1. The threat-model rating is LOW *because* the amendment is bounded by A1+A4 and is contributor-hygiene compile-time defense, not adversarial proof. The §2.1 + §11 explicit documentation of bounded scope is evidence of correct severity claim, not evidence of unmitigated risk. Promoting to HIGH would reject the parent disposition's authority. Row-170 precedent applies: when a Red Team finding's premise contradicts the LOCKED text/disposition, the finding is REJECTED with rationale, not folded into the LOCK. (Mirrors WS-L §4 v2.x Cycle-2 RT-04/RT-05 REJECTED-with-rationale dispositions and WS-I §13 Cycle-2 RT-C2-04 disposition.) |

### §11.4 NO-OP (Red Team explicitly says "no gap here")

| Cycle-1 ID | Severity claimed | Probe | Disposition |
|---|---|---|---|
| RT-05 | MED (Red Team) | `import os as o; import shutil as s; o.replace(s.copy(src, tmp), dst)` — nested call | Red Team's analysis correctly concludes the rule emits two violations (one per `Call` node visited). No gap; no action. |

### §11.5 Cycle-2 verification dispositions

Cycle-2 dispatch (Editor + Judge + Red Team via openclaw bridge 2026-05-10T23:01Z) results:

- **Editor**: READY_TO_LOCK (all six E-NN findings CLOSED; no new findings).
- **Judge**: READY_TO_LOCK 100/100 (+2 from Cycle-1 98/100; all five fold-ins CLOSED).
- **Red Team**: REQUIRES_MINOR_FIXES blocking=`false` — "Compatible with LOCK at this Cycle-2 close per row-170 transparent-disposition pattern." One LOW probe surfaced (RT-C2-01); RT-C2-02 + RT-C2-03 NO-ACTION.

| Cycle-2 ID | Severity | Probe | Disposition |
|---|---|---|---|
| RT-C2-01 | LOW | Drift-test file `tests/seats/archivist/test_runtime_guard_wrapper_drift.py` not yet on disk at §4 v2.x.1 LOCK | FOLDED-IN at LOCK — explicit text-level fix at §4 above ("Test-file existence at §4 v2.x.1 LOCK") clarifies that the file is a forward-binding v1.x deliverable, not a §4 v2.x.1 LOCK precondition. Mirrors §15 v1 v0.2 SPEC-ONLY discipline pattern. |
| RT-C2-02 | LOW | Module variable `FORBIDDEN_PRIMITIVES` could be reassigned at runtime via `importlib.import_module().FORBIDDEN_PRIMITIVES = {}` | NO-ACTION (already-acknowledged per §2.1 + §11.1 RT-01/02/03 dynamic-call evasion class; bounded by v7 A4 operator-trusted-preflight). Red Team's own framing: "No action — limitation already acknowledged." |
| RT-C2-03 | LOW | Sub-tag count consistency across code/text/test | NO-ACTION (Red Team verified: no mismatch detected; all three sources list six sub-tags + ten call shapes). |

---

## Appendix A — Forbidden-primitive table (single source of truth)

The on-disk single source of truth lives in `pipeline/linting/r_archivist_no_canonical_mutate.py:_FORBIDDEN_PRIMITIVES`. Reproduced here for reading-surface coherence with the disposition packet §3.1 — drift between the file and this table is itself a §4 v2.x.1 defect and the file is canonical.

```python
_FORBIDDEN_PRIMITIVES: dict[tuple[str, str], str] = {
    ("os", "replace"):  "low_level_rename_replace",
    ("os", "rename"):   "low_level_rename_rename",
    # os.renames is the recursive-rename wrapper; same shape as os.rename
    # for atomic-substrate purposes (Cycle-1 RT-09 fold-in).
    ("os", "renames"):  "low_level_rename_renames",
    ("shutil", "move"): "low_level_rename_shutil_move",
    # shutil.copy family — all four primitives collapse to a single sub-tag.
    ("shutil", "copy"):     "low_level_rename_shutil_copy",
    ("shutil", "copy2"):    "low_level_rename_shutil_copy",
    ("shutil", "copyfile"): "low_level_rename_shutil_copy",
    ("shutil", "copytree"): "low_level_rename_shutil_copy",
    # os.link / os.symlink — same sub-tag per disposition packet.
    ("os", "link"):    "low_level_rename_os_link",
    ("os", "symlink"): "low_level_rename_os_link",
}

# Cycle-1 RT-14 fold-in: the exported public view is wrapped in
# types.MappingProxyType to make the table immutable at runtime.
FORBIDDEN_PRIMITIVES: Mapping[tuple[str, str], str] = MappingProxyType(
    _FORBIDDEN_PRIMITIVES
)
```
