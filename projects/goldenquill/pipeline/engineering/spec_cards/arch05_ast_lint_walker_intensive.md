# Spec card — pipeline.linting.ast_lint (ARCH-05: §7.16 walker-intensive pair — R6 + R7)

**STATUS:** SELF-LOCKED

## Blueprint anchors

- `pipeline/blueprint/v0.1/section_03_scout.md` §7.16 AST-NO-INDIRECT-VAULT-READ + AST-PREFLIGHT-DOMINATES-FD-REQUEST, including refinements A-v3-03, A-v4-03, B-v5-02 (R6) and A-v3-07, A-v4-02, B-v5-01, B-v5-03 (R7).
- `pipeline/blueprint/v0.1/section_04_logician.md` §7.6 (R3 bridging case — `pathlib.Path("orgs/").open()` and `builtins.open("orgs/")` fall under R6's alias-walker).

**Module:** `pipeline/linting/ast_lint.py` (row-append; no refactor of ARCH-04 infrastructure).
**Round:** ARCH-05 (§7.16 walker-intensive closure).
**Predecessor LOCK:** ARCH-04 2026-04-20 (R1–R5 shipped, `Rule.check` callable = extension point).

## What this round adds

Two rules. Both require whole-module flow-sensitive walking that ARCH-04's single-AST-walk per-rule check cannot express. They row-append to `DEFAULT_RULES` and each ships its own `_check_*` function that internally holds an alias map / CFG-dominance analysis over the module.

### R6 — AST-NO-INDIRECT-VAULT-READ

Closes the alias/attribute-chain/dynamic-import bypass class that ARCH-04's R1/R3/R5 intentionally admitted. Nine `test_adv_*` tests in `tests/linting/test_ast_lint.py` already enumerate the class with named examples:

- `test_adv_r3_open_via_pathlib_not_caught` — `Path("orgs/...").open()`
- `test_adv_r3_open_rebound_to_local_name_not_caught` — `o = open; o("orgs/...")`
- `test_adv_r3_builtins_open_attribute_form_not_caught` — `builtins.open("orgs/...")`
- `test_adv_r4_dynamic_attribute_name_not_caught` — `attr = "operator_decision"; setattr(x, attr, v)`
- `test_adv_r5_getattr_builtins_eval_not_caught` — `getattr(__builtins__, "eval")(s)`
- `test_adv_r5_eval_rebound_to_local_name_not_caught` — `e = eval; e(s)`
- `test_adv_r5_builtins_eval_attribute_form_not_caught` — `builtins.eval(s)`
- `test_adv_r1_dynamic_import_via_importlib_not_caught` — `importlib.import_module("anthropic")`
- `test_adv_r2_attribute_access_via_package_import_not_caught` — `import pipeline.logician as L; L.cedar_eval.evaluate(...)`

R6's landing flips each of these from `assert vs == []` to `assert vs != []` (with appropriate reason-tag).

**Algorithm sketch:**

1. Build a per-module alias map: name → concrete callable/class/module (follow simple `x = expr` bindings where `expr` is `ast.Name`, `ast.Attribute`, or `ast.Call` returning a well-known constructor).
2. Resolve `ast.Attribute` chains against the alias map to their canonical root.
3. Resolve string-first-arg `importlib.import_module("anthropic")` / `__import__("anthropic")` against the R1 provider ban set.
4. Resolve `ast.Call(func=Attribute(ast.Name("builtins"), "open"))` / `Attribute(ast.Name("pathlib").Path, "open")` to the canonical `open` matcher.
5. Resolve `getattr(obj, const_str)` to the attribute-name-to-predicate mapping for R4 + R5 classes.

**B-v5-02 termination guard:** alias-walker must terminate on bounded-arity cycles (e.g. `a = b; b = a`). Fixed-point computation with epoch counter + iteration-cap raise `AliasWalkerNonTerminationError` for cycles longer than the cap (default 32). Tests include an `test_adv_r6_alias_cycle_non_termination_bounded` probe.

**Reason-tag vocabulary** (E-008 byte-match):
- `logician_indirect_vault_read_via_alias`
- `logician_indirect_llm_client_via_alias`
- `scout_indirect_operator_decision_write_via_alias`
- `scout_indirect_dynamic_code_via_alias`

### R7 — AST-PREFLIGHT-DOMINATES-FD-REQUEST

Enforces that every `fd_broker.request(...)` call in `pipeline/loop/**` and `pipeline/scout/**` is CFG-dominated by a preflight predicate resolved at module scope. Closes the bypass where a caller issues an `fd_broker.request` without having executed the §2 Vault preflight check on the same code path.

**Algorithm sketch:**

1. Build a control-flow graph per function body (blocks + successor edges).
2. Identify each `fd_broker.request(...)` call node as a "sink."
3. Walk backwards along the CFG from every sink; require that every path includes a call to a preflight predicate whose module-level `Final[bool]` sentinel has been tested True.
4. Cross-module resolution (B-v5-03): if the preflight sentinel is defined in a sibling module, resolve via `from <mod> import <name>` + type-annotation `Final[bool]` + literal-init `= True` / `= False`. No runtime resolution — static pattern match only.
5. If any sink is not dominated, emit a violation at the sink's line with reason-tag `loop_fd_request_not_preflight_dominated` (or `scout_...` analog).

**A-v4-02 `Final[bool]` literal-init discipline:** R7 refuses to treat a sentinel as preflight-evidence unless the sentinel is `typing.Final[bool]` with a `True`/`False` literal initializer at module scope. Computed initializers (e.g. `SENTINEL: Final[bool] = os.getenv("X") == "1"`) fail R7 with reason-tag `fd_request_preflight_sentinel_non_literal`.

**B-v5-01 short-circuit-op handling:** `if preflight and other:` — R7 treats `preflight` as a dominator when it appears on the `and`-short-circuit path; `if preflight or fallback:` — R7 does NOT treat it as dominator (fallback path reaches sink without preflight).

**Reason-tag vocabulary:**
- `loop_fd_request_not_preflight_dominated`
- `scout_fd_request_not_preflight_dominated`
- `fd_request_preflight_sentinel_non_literal`
- `fd_request_preflight_short_circuit_or_bypass`

## Public API delta

```python
# pipeline/linting/ast_lint.py — ARCH-05 additions
__all__ += [
    "AST_NO_INDIRECT_VAULT_READ",       # R6
    "AST_PREFLIGHT_DOMINATES_FD_REQUEST",  # R7
    "AliasWalkerNonTerminationError",   # R6 termination-guard failure class
]
DEFAULT_RULES += [
    AST_NO_INDIRECT_VAULT_READ,
    AST_PREFLIGHT_DOMINATES_FD_REQUEST,
]
```

No change to `Rule`, `Violation`, `lint_tree`, or any ARCH-04 rule. ARCH-04's 9 `test_adv_*` documentation tests flip from `assert vs == []` to `assert vs != []` with the appropriate reason-tag — the tests become regression guards for R6's coverage.

## Corpus additions

`tests/corpus/ast_lint/v1/fail/pipeline/`:
- `logician/r6_path_alias.py` — `Path("orgs/...").open()`
- `logician/r6_builtins_open.py` — `builtins.open("orgs/...")`
- `logician/r6_rebound_open.py` — `o = open; o("orgs/...")`
- `logician/r6_importlib_anthropic.py` — `importlib.import_module("anthropic")`
- `scout/r6_getattr_eval.py` — `getattr(__builtins__, "eval")(s)`
- `scout/r6_dynamic_setattr.py` — `setattr(item, "operator_decision", v)`
- `loop/r7_fd_request_no_preflight.py`
- `loop/r7_fd_request_or_fallback.py`
- `loop/r7_fd_request_non_literal_sentinel.py`

Plus `pass/pipeline/loop/r7_fd_request_preflight_dominated.py` demonstrating the happy path.

## Failure-code tests (red-first)

Each of the nine `test_adv_*` tests in ARCH-04's suite flips. Plus at minimum:
- R6: `test_r6_catches_path_alias`, `test_r6_catches_builtins_open`, `test_r6_catches_rebound_name`, `test_r6_catches_importlib_anthropic`, `test_r6_catches_getattr_builtins_eval`, `test_r6_catches_dynamic_setattr_operator_decision`, `test_r6_termination_guard_cycle`.
- R7: `test_r7_catches_missing_preflight`, `test_r7_admits_preflight_dominator`, `test_r7_catches_or_fallback`, `test_r7_catches_non_literal_sentinel`, `test_r7_cross_module_sentinel_resolution`, `test_r7_short_circuit_and_admits`.

## Scope boundaries

**In scope:**
- Single-pass alias tracking within a module (forward flow, no call-graph across module boundaries except the preflight-sentinel resolution for R7 B-v5-03).
- Attribute-chain resolution to depth 4 (covers `builtins.open`, `pathlib.Path(x).open`, `importlib.import_module`, `object.__setattr__`).
- String-literal first-argument resolution for `importlib.import_module`, `__import__`, `getattr`, `setattr`.
- CFG construction over structured control flow (`if`, `for`, `while`, `try`, `with`, comprehensions). Lambda bodies count as nested scopes with their own CFG.

**Out of scope (deferred to ARCH-06 if ever needed):**
- Cross-module alias tracking (alias defined in module A, used in module B). R6 is per-module.
- Dynamic code-path via `exec` / `eval` — already banned under R5, so this is moot.
- Call-graph-sensitive preflight (preflight called by a helper). R7 requires the preflight literally appear in the caller's CFG.

## Engineering-process futureproofing

- Public-API additions enumerated in `__all__` (§4.1).
- `BLUEPRINT_DEPS` extended to add `section_03_scout.md` §7.16 refinement anchors (A-v3-03, A-v4-03, B-v5-02, A-v3-07, A-v4-02, B-v5-01, B-v5-03). Hash recomputed as `sha3_512[:16]` per §4.6.
- Drift guard `test_blueprint_deps_hashes_match_live_blueprints` continues to cover both blueprints — edits to §3 Scout or §4 Logician without pin bump fail the suite.
- Regression discipline (§4.9): all ARCH-04 property tests (`test_logician_tree_has_zero_violations`, `test_scout_tree_has_zero_violations`, `test_full_tree_passes_default_rules`) continue to pass — `DEFAULT_RULES` is additive.
- Type hints (§4.10): every public entry type-annotated including the new error class.
- Docstring blueprint anchors (§4.11): each new rule's `description` cites §7.16 refinement IDs.
- Round-lesson commitment (§4.12): author commits E-NNN post-committee.

## Done definition

1. R6 + R7 implemented; all nine ARCH-04 `test_adv_*` tests flipped to assert violations; new `test_r6_*` and `test_r7_*` tests red-first then green.
2. Live-tree property tests remain green (`pipeline/logician/` zero violations, `pipeline/scout/` zero violations, full `pipeline/` zero violations). If any live module now violates R6 or R7, that is a real finding that must be fixed in the same round or filed as a separate task.
3. Coverage on `pipeline/linting/ast_lint.py` ≥ 95% (currently 99%; the alias walker + CFG walker will add ~400 LOC, so coverage target holds only with exhaustive adversarial tests).
4. `scripts/run_lint.sh` unchanged; continues to exit 0/1/2.
5. Code Thesis Committee dispatch: 5 cross-family reviewers per `router.yaml`, all-pass, retry cap 1. Given the alias-bypass class is now IN scope, gpt_oss's findings from ARCH-04 retry-1 must be CAUGHT by R6; reviewer will verify.
6. `pipeline/validation/architecture_v0.1_findings_from_section_03/ARCH-05.md` filed with closure narrative.
7. `E-NNN` engineering lesson added.
8. `pipeline/engineering/lock_history.v1.jsonl` telemetry line appended with `rules_shipped: ["R6","R7"]`.
9. `daily_logs/<date>.md` updated.
10. §0.5 paired-commit amendment lands (row-append extending ARCH-04's aggregate or adding a new aggregate for the walker-intensive tier).
11. Next staged: §3 Scout build (task #3) if not already dispatched; §5 Orchestrator build (task #4) if not already dispatched.

## Open questions for operator (do NOT block Midas dispatch — flag at Midas §12a)

- **Q1:** Should R6's alias walker also resolve the `pathlib.Path(x).open()` form where `x` is a variable rather than a literal? (Default answer: no — resolving variable-content requires symbolic execution, which is out-of-scope-for-v0.2. The `Path("orgs/...")` literal case is what matters.)
- **Q2:** Should R7 admit a `try/except` block containing preflight as a dominator? (Default answer: yes, treating `try: preflight(); sink()` as a dominated path because the sink is not reached if preflight raises; document this explicitly in `description`.)

---

*Spec card v1 — 2026-04-20 — filed as pre-staged ARCH-05 deliverable by the ARCH-04 author. Dispatch readiness: blocked only on operator go-ahead + Midas v2.1 invocation.*
