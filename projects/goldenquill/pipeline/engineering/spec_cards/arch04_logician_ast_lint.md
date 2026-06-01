# Spec card — pipeline.linting.ast_lint (ARCH-04 closure: §4 Logician AST-lint)

**STATUS:** LOCKED

**Blueprint anchors:**
- `pipeline/blueprint/v0.1/section_04_logician.md` §3.1 (line 844), §4.2.3 (line 414), §10 (line 1377, 1385, 1620)
- Analogous pattern: `pipeline/blueprint/v0.1/section_03_scout.md` §7.16 (AST-NO-INDIRECT-VAULT-READ et al.)
**Blueprint hash-at-card:** `<to-fill-at-implementation-time>` — Midas runs `python scripts/check_blueprint_drift.py` to compute the 16-char SHA3-512 prefix of `section_04_logician.md` v2 and pastes it here before locking.
**Spec-card version:** v1
**Round:** ARCH-04 (new infrastructure + §4 closure)
**Futureproofing scope:** §4.1 public-API boundary; §4.9 regression discipline; §4.10 type hints; §4.11 docstring blueprint anchors; §4.12 engineering lessons accumulation

---

## Summary

Ship the first cross-section AST-lint harness. Enforce five rules total:
- **§4 Logician (ARCH-04 closure) — three rules:** (R1) ban LLM-client SDK imports under `pipeline/logician/**`, (R2) ban `from pipeline.logician ...` imports under `pipeline/loop/**` (prospective — §5 not yet built), (R3) ban `open()` calls on `orgs/` or `vault_shared/` paths under `pipeline/logician/**`.
- **§3 Scout (§7.16 simple pair) — two rules:** (R4) ban `setattr(item, "operator_decision", …)` and direct attribute-store equivalents outside `review_stage.py`, (R5) ban `eval`/`exec`/`compile` under `pipeline/scout/**`.

Each violation fail-closed with a named reason-tag. Landing this closes ARCH-04 candidate, replaces manual lock-time audits with mechanical enforcement, and establishes the infrastructure for ARCH-05 (the walker-intensive §7.16 rules — AST-NO-INDIRECT-VAULT-READ, AST-PREFLIGHT-DOMINATES-FD-REQUEST — which row-append to `DEFAULT_RULES` without refactor).

## Design decisions (E1-resolved 2026-04-20)

1. **Scope — INCLUDE R3.** All three rules (R1 LLM-client import ban, R2 loop-internal-import ban, R3 `open()` on vault paths ban) ship in this round. R3 closes a Law 3 Org-Isolation bypass vector that would otherwise rely on manual lock-time audits. Same harness, same committee round, same telemetry line — splitting would double overhead.
2. **Location — `pipeline/linting/ast_lint.py` + `tests/linting/` + `scripts/run_lint.sh`.** Dual invocation: (a) property tests in `tests/linting/test_ast_lint.py` run as part of the regular `pytest` suite (cost: ~1-2s walking `pipeline/`); (b) standalone shell entry `scripts/run_lint.sh` for dev-time on-demand runs. Both call the same `lint_tree()` — no divergence. Shell script is a thin wrapper; updates to `DEFAULT_RULES` automatically reflect in both invocation paths.
3. **Section 3 §7.16 coverage — SPLIT.** This round ships TWO of the four §7.16 rules as row-appends to `DEFAULT_RULES`:
   - **AST-NO-SETATTR-OPERATOR-DECISION** (simple attribute-store check) — rejects `setattr(item, "operator_decision", …)` and equivalents outside `review_stage.py::record_operator_decision`.
   - **AST-NO-EVAL-IN-SCOUT** (simple call-name check) — rejects `eval`, `exec`, `compile` anywhere under `pipeline/scout/**`.

   DEFERRED to a dedicated ARCH-05 round (walker-intensive, would blow the round-batching 40 KiB cap):
   - AST-NO-INDIRECT-VAULT-READ — full alias tracker with fixed-point resolution + B-v5-02 termination guard.
   - AST-PREFLIGHT-DOMINATES-FD-REQUEST — CFG-dominance walker with cross-module `Final[bool]` resolution (A-v4-02, B-v5-01, B-v5-03 refinements).

   ARCH-05 uses this round's infrastructure — `Rule`/`Violation` types, `lint_tree` walker. No refactor needed; the §4 public-API boundary (§4.1 futureproofing) already designed for extensibility.
4. **ARCH-04 promotion — Committee all-pass suffices.** Pattern is blueprint-precedent (§7.16 already specs AST rules). Implementation matches spec. Code Thesis Committee 5-cross-family is exactly designed for this review depth. No dedicated Thesis round. ARCH-04 closure filed at `pipeline/validation/architecture_v0.1_findings_from_section_04/ARCH-04.md` with the closure narrative (what shipped, what deferred to ARCH-05, final lint surface). §0.5 paired-commit row lands with the lock.

## Public API (goes in `__all__`)

```python
# pipeline/linting/ast_lint.py
__all__ = [
    # Futureproofing pin (§4.6)
    "BLUEPRINT_DEPS",
    # Public dataclasses
    "Rule",
    "Violation",
    # Harness entry
    "lint_tree",
    # §4 rules (ARCH-04)
    "LOGICIAN_IMPORT_BAN",            # R1
    "LOOP_LOGICIAN_BAN",              # R2
    "LOGICIAN_OPEN_BAN",              # R3
    # §7.16 rules (simple — land in this round)
    "SCOUT_NO_SETATTR_OPERATOR_DECISION",  # §7.16 simple
    "SCOUT_NO_EVAL",                       # §7.16 simple
    # Default set
    "DEFAULT_RULES",                  # list[Rule] — all five above
]
```

- `Rule` — frozen dataclass: `name: str`, `target_glob: str`, `check: Callable[[ast.Module, Path], list[Violation]]`, `reason_tag: str`, `blueprint_anchor: str`.
- `Violation` — frozen dataclass: `rule_name: str`, `file: Path`, `line: int`, `col: int`, `message: str`, `reason_tag: str`.
- `lint_tree(root: Path, rules: list[Rule]) -> list[Violation]` — walks `root`, filters files by each rule's `target_glob`, applies check, returns flat list of violations. Empty list = pass.
- Rule constants (`LOGICIAN_IMPORT_BAN`, `LOOP_LOGICIAN_BAN`, `LOGICIAN_OPEN_BAN`) so callers can compose subsets.

## Data structures

Both dataclasses frozen + kw_only per blueprint §0.5 discipline. `Rule.check` receives a parsed `ast.Module` plus the file path; returns 0..N `Violation`. No mutation of the AST.

## Algorithms

**R1 — LOGICIAN_IMPORT_BAN.** For each `.py` file under `pipeline/logician/**`: `ast.parse` → walk `Import` and `ImportFrom` nodes → reject if module name is in the ban set `{"anthropic", "openai", "groq", "google.generativeai", "ollama"}` OR starts with any of those plus `.` (submodule imports). Reason-tag: `logician_imports_llm_client`.

**R2 — LOOP_LOGICIAN_BAN.** For each `.py` file under `pipeline/loop/**` (prospective; no matching files in v0.1 current tree): `ast.parse` → walk `ImportFrom` nodes → reject if `module` starts with `pipeline.logician.` (internal module access). `from pipeline.logician import ...` (the `__init__.py` public surface) is ALLOWED — the rule is specifically about internal-module bypass of the public API, analogous to §4.1 public-API boundary. Reason-tag: `loop_imports_logician_internal`.

**R3 — LOGICIAN_OPEN_BAN.** For each `.py` file under `pipeline/logician/**`: `ast.parse` → walk `Call` nodes where `func` resolves to the builtin `open` (direct name-reference; does NOT track aliases per §4 v2 threat model which is trusted-operator) → if first arg is an `ast.Constant` string AND starts with `orgs/` or `vault_shared/`, reject. Non-literal first args are admitted (out of scope for static analysis under trusted-operator). Reason-tag: `logician_opens_vault_path`. Blueprint note: Section 3 §7.16 has richer alias-tracking; §4 explicitly defers that per blueprint line 1385 ("analogous to Section 3's AST-NO-INDIRECT-VAULT-READ" — pattern, not full implementation).

**R4 (§7.16 simple) — SCOUT_NO_SETATTR_OPERATOR_DECISION.** For each `.py` file under `pipeline/scout/**` EXCEPT `pipeline/scout/review_stage.py`: `ast.parse` → walk `Call` nodes matching `setattr(x, "operator_decision", …)` OR `object.__setattr__(x, "operator_decision", …)` → also walk `Attribute` store nodes (`ast.Attribute` with `ctx=ast.Store`) whose `attr == "operator_decision"` → reject. Reason-tag: `scout_setattr_operator_decision_outside_review_stage`. Complements the existing `no auto-file` rule which only looks at `Assign` nodes.

**R5 (§7.16 simple) — SCOUT_NO_EVAL.** For each `.py` file under `pipeline/scout/**`: `ast.parse` → walk `Call` nodes where `func` is an `ast.Name` with `id in {"eval", "exec", "compile"}` → reject. No exceptions; the Scout package never generates or executes runtime code. Reason-tag: `scout_dynamic_code_execution`.

**Deferred to ARCH-05** (not implemented in this round): R6 AST-NO-INDIRECT-VAULT-READ (alias-walker intensive); R7 AST-PREFLIGHT-DOMINATES-FD-REQUEST (CFG-dominance walker with cross-module `Final[bool]` resolution). Both specified in Section 3 blueprint §7.16 with extensive refinements (A-v3-03, A-v4-03, B-v5-02 for R6; A-v3-07, A-v4-02, B-v5-01, B-v5-03 for R7). ARCH-05 will extend `DEFAULT_RULES` by row-append — no infrastructure refactor required because `Rule`'s `check` callable is the extension point.

## Failure codes

Not Logician `F-*` codes. AST-lint violations surface as test failures with named reason-tags (above). Property tests assert zero violations across the tree.

## Test surface

### Property tests
- `test_logician_tree_has_zero_violations` — runs `lint_tree(Path("pipeline/logician"), DEFAULT_RULES)` against the live tree, asserts empty violations list. Green today = Logician currently clean (matches blueprint §4.10 claim). Ongoing regression guard.
- `test_loop_tree_has_zero_violations` — runs against `pipeline/loop/` when it exists; skipped if directory missing.
- `test_scout_tree_has_zero_violations` — runs `lint_tree(Path("pipeline/scout"), [SCOUT_NO_SETATTR_OPERATOR_DECISION, SCOUT_NO_EVAL])`. Green today for existing `pipeline/scout/scan_golden_quill.py` surface.
- `test_full_tree_passes_default_rules` — runs `lint_tree(Path("pipeline"), DEFAULT_RULES)` against the live monorepo. Asserts empty violations. Single-call entry for the pytest regression guard.

### Failure-code tests (red-first)
- R1: `test_r1_detects_anthropic_import`, `test_r1_detects_submodule_import` (`from openai.types import X`), `test_r1_catches_all_five_providers` (parametrized over `{anthropic, openai, groq, google.generativeai, ollama}`).
- R2: `test_r2_rejects_internal_module_import_from_loop`, `test_r2_admits_public_api_import_from_loop` (`from pipeline.logician import LogicianGateRunner` does NOT fire).
- R3: `test_r3_rejects_open_on_orgs_path`, `test_r3_rejects_open_on_vault_shared_path`, `test_r3_admits_non_literal_open` (`open(var)` with var a parameter), `test_r3_admits_open_on_other_paths` (`open("/tmp/cache")`).
- R4: `test_r4_rejects_setattr_operator_decision_outside_review_stage`, `test_r4_rejects_object_setattr_form`, `test_r4_rejects_direct_attribute_store` (`item.operator_decision = x`), `test_r4_admits_setattr_inside_review_stage_module` (the carve-out works).
- R5: `test_r5_rejects_eval`, `test_r5_rejects_exec`, `test_r5_rejects_compile`, `test_r5_admits_these_outside_scout` (rule is scout-scoped, not universal).

### Adversarial tests (`test_adv_*`)
- `test_adv_r1_alias_import_still_caught_via_module_name` — `import anthropic as a` still fires (walker uses `alias.name`, not local rebinding).
- `test_adv_r1_conditional_import_inside_try` — `try: import openai\nexcept: ...` still fires (static scan, not runtime reachability).
- `test_adv_r2_dotted_submodule_access_still_caught` — `from pipeline.logician.cedar_eval import thing` fires.
- `test_adv_r3_open_via_pathlib` — `Path("orgs/x").open()` does NOT fire under v0.1 trusted-operator scope (documented limitation; blueprint §4 v2 explicit).
- `test_adv_r4_dynamic_attribute_name_not_caught` — `attr_name = "operator_decision"; setattr(item, attr_name, ...)` does NOT fire under v0.1 trusted-operator scope (static string literal only; documented limitation).
- `test_adv_r5_getattr_builtins_eval_not_caught` — `getattr(__builtins__, "eval")("...")` does NOT fire (static-name check; documented limitation, aligns with Section 3 §7.16 v0.1 scope).

### Corpus tests
- `tests/corpus/ast_lint/v1/pass/` — fixture files that must produce zero violations.
- `tests/corpus/ast_lint/v1/fail/` — fixture files paired with expected-violation manifests.

## Futureproofing commitments

- Public-API surface declared in `__all__`; internal helpers (AST walk primitives) stay module-private.
- Schema version: N/A (no on-disk artifacts produced).
- Crypto-agile types: N/A.
- BLUEPRINT_DEPS populated:
  ```python
  BLUEPRINT_DEPS = {
      "section_04_logician.md": {
          "sections_implemented": ["§3.1", "§4.2.3", "§4.10", "§10 ARCH-04"],
          "hash_at_lock": "<16-char-prefix>",
          "hash_source_version": "v2",
      },
      "section_03_scout.md": {
          "sections_implemented": ["§7.16 (pattern reference only — rules filed ARCH-05 or separate card)"],
          "hash_at_lock": "<16-char-prefix>",
          "hash_source_version": "<current>",
      },
  }
  ```
- Regression discipline: fixture files in the corpus are preserved; future rule additions are ADDITIVE — existing pass corpus must keep passing.
- Extensibility: `Rule` is a dataclass with a callable check — adding §7.16 Scout rules later is a row-append, not a refactor.

## Done definition

1. All five rules (R1-R5) implemented, property tests green on the live tree (zero violations in `pipeline/logician/` and `pipeline/scout/`).
2. All failure-code tests red before fix, green after.
3. All adversarial tests exercise the documented threat model; none passes vacuously.
4. Coverage on `pipeline/linting/ast_lint.py` ≥ 95%.
5. `scripts/run_lint.sh` exists, runs `lint_tree(Path("pipeline"), DEFAULT_RULES)`, exits 0 on empty-violations / 1 on any-violation with violation listing on stderr. Documented in `provisioning_manifest_v0.1.md` §10.1 Code quality (D-01 drift resolved 2026-04-20: v1 card had `§4 (dev-workflow commands)` which is actually "LLM providers / API keys" — corrected here).
6. Code Thesis Committee dispatch: 5 cross-family reviewers per `router.yaml` `code_*` rows, all-pass, retry cap 1.
7. `pipeline/validation/architecture_v0.1_findings_from_section_04/ARCH-04.md` filed with closure narrative: what shipped (R1-R5), what's deferred to ARCH-05 (R6 AST-NO-INDIRECT-VAULT-READ, R7 AST-PREFLIGHT-DOMINATES-FD-REQUEST), why deferral chosen (walker complexity, round-batching cap), infrastructure reuse pattern.
8. `E-NNN` engineering lesson added: "AST-lint rules that live in blueprint text but not in code are promises not guardrails — land the harness alongside any blueprint rule-spec." Pre-check: any future blueprint-LOCKED AST rule gets a companion implementation task filed in the same round, not as a future promise.
9. `pipeline/engineering/lock_history.v1.jsonl` telemetry line appended with `rules_shipped: ["R1","R2","R3","R4","R5"]` + `rules_deferred: ["R6","R7"]`.
10. `daily_logs/2026-04-20.md` updated.
11. ARCH-05 task already created (task #11) — contains the two walker-intensive rules. This round's infrastructure is explicitly designed to receive them as row-appends.
12. Task #2 LOCKs. Downstream unblocks: task #3 (§3 Scout build — Scout modules are now lint-guarded), task #4 (§5 Orchestrator build — `pipeline/loop/` directory will be lint-guarded from day one).
13. Next staged (per §14 proactive pre-staging): ARCH-05 spec card for walker-intensive §7.16 rules OR §3 Scout spec card, whichever operator designates as the next Midas frontier.

---

*Spec card v2 — 2026-04-20 — E1 resolved via operator delegation ("do what is necessary to create the most stable secure efficient useful intelligent powerful magnificent tool"); ready for Midas dispatch.*

*Spec card v2.1 — 2026-04-20 — Committee-retry remediation: `BLUEPRINT_DEPS` added to `__all__` (gemini_r5 LOW-2); Done row 5 pointer corrected §4 → §10.1 (D-01); Done row Notes: alias-bypass scope for R2/R3/R5 formally documented as ARCH-05 R6 territory via three new `test_adv_*` tests (gpt_oss HIGH-1..3 reclassified as documented-scope per spec card E1 + trusted-operator envelope).*
