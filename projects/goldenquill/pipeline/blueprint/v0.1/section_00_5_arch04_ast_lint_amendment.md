---
title: Blueprint §0.5 Interface Index — Amendment for ARCH-04 AST-lint harness (1 paired-commit row)
filed: 2026-04-20
operator: Josh
amendment_status: DRAFT — paired commit with pipeline/linting/ast_lint.py LOCK 2026-04-20; awaiting next §0.5 Thesis-round merge
parent_lock: pipeline/blueprint/v0.1/section_00_5_interface_index_locked.md  (§0.5 v4 LOCKED 2026-04-19, 99 rows)
supersedes_relationship: row-append only. No existing v4 row modified.
companion_code: pipeline/linting/ast_lint.py (sha3_512[:16]=342f3232f72be045, 525 LOC, 99% coverage, 61 tests)
companion_narrative: pipeline/validation/architecture_v0.1_findings_from_section_04/ARCH-04.md
scope_source: pipeline/engineering/spec_cards/arch04_logician_ast_lint.md (v2.1, E1 resolved)
parent_wins_discipline: the added row points at §4 Logician v2.1 (existing LOCKED blueprint reference) and §3 Scout v0.1 §7.16 (simple-pair carve-out).
row_count: 1
aggregate_granularity: one row at harness-lock-version granularity per §0.5.8 aggregation precedent ("Logician allowlist rows aggregated at Section-4-lock-version granularity"). Individual R1-R5 rules not exploded into separate rows — rule set enumerated in the `description` field. ARCH-05 will row-append R6/R7 at the same granularity.
---

# Amendment intent

§0.5 paired-commit discipline: every load-bearing primitive introduced by a blueprint-or-implementation section lands as an index row in the same commit. ARCH-04 introduces the deterministic AST-lint harness `pipeline.linting.ast_lint` as the enforcement layer for three §4 Logician invariants (no-LLM-client, no-vault-open, no-loop-internal-import) + the §7.16 Scout simple pair (no-setattr-operator_decision-outside-review_stage, no-eval). The harness is cross-cutting infrastructure that multiple future blueprint sections cite.

# Proposed 1 new §0.5 row

Row schema per §0.5 v4: `primitive_id`, `defined_at`, `parent_lock_version`, `parent_lock_commit_hash`, `primitive_kind`, `description`, `introduced_in_index_version`, `stability_tier`.

## Group — Enforcement infrastructure (1 row)

| # | primitive_id | defined_at | parent_lock | kind | stability |
|---|---|---|---|---|---|
| 100 | `linting_ast_lint_harness_v1` | `pipeline/linting/ast_lint.py` (sha3_512[:16]=`342f3232f72be045`); blueprint anchors `section_04_logician.md` §3.1 + §7.4 + §7.6 + §10 and `section_03_scout.md` §7.16 (simple pair) | §4 v2.1 + §3 v0.1 | enforcement-infrastructure | Tier 1 (stable — deterministic AST walk, no I/O beyond reading .py files) |

**Description:** Deterministic AST-lint harness exposing `Rule`, `Violation`, `lint_tree(root, rules)`, and five `DEFAULT_RULES`:

1. **R1 LOGICIAN_IMPORT_BAN** — no LLM-client SDK imports under `pipeline/logician/**` (banned set: `anthropic`, `openai`, `groq`, `google.generativeai`, `ollama`). Reason-tag: `logician_imports_llm_client`. Anchors §4 v2.1 §3.1 + §7.4.
2. **R2 LOOP_LOGICIAN_BAN** — no `from pipeline.logician.<submodule> import …` or `import pipeline.logician.<submodule>` under `pipeline/loop/**`. Public-API imports (`from pipeline.logician import X`) allowed. Reason-tag: `loop_imports_logician_internal`. Anchors §4 v2.1 §4.1 public-API boundary.
3. **R3 LOGICIAN_OPEN_BAN** — no `open("orgs/...")` or `open("vault_shared/...")` under `pipeline/logician/**`. Literal-prefix only; alias/attribute/dynamic-call forms deferred to ARCH-05 R6 per v0.1 trusted-operator envelope. Reason-tag: `logician_opens_vault_path`. Anchors §4 v2.1 §7.6.
4. **R4 SCOUT_NO_SETATTR_OPERATOR_DECISION** — no `setattr(x, "operator_decision", …)`, `object.__setattr__(x, "operator_decision", …)`, or `x.operator_decision = …`/`+= …` under `pipeline/scout/**` except `review_stage.py`. Reason-tag: `scout_setattr_operator_decision_outside_review_stage`. Anchors §3 v0.1 §7.16 simple pair.
5. **R5 SCOUT_NO_EVAL** — no `eval(…)`, `exec(…)`, `compile(…)` by static name under `pipeline/scout/**`. Attribute/getattr forms deferred to ARCH-05 R6. Reason-tag: `scout_dynamic_code_execution`. Anchors §3 v0.1 §7.16 simple pair.

`BLUEPRINT_DEPS` pinned to `sha3_512[:16]` of the two source blueprint files; drift-guard test fails when either blueprint is edited without bumping the pin. CLI wrapper `scripts/run_lint.sh` exits 0/1/2. Extension point: new rules row-append to `DEFAULT_RULES` via `Rule(check=…)` callable — no walker refactor required. ARCH-05 adds R6 (alias walker + B-v5-02 termination guard) and R7 (CFG-dominance + `Final[bool]` literal-init + B-v5-03 cross-module resolution) under this infrastructure.

# Commit-time F-INDEX-STALE discipline

This amendment must land in the same commit as `pipeline/linting/ast_lint.py`. The `lock_history.v1.jsonl` telemetry entry for ARCH-04 carries `blueprint_hash_at_lock_prefix_logician` = `e0507e6daaa18676` and `blueprint_hash_at_lock_prefix_scout` = `0a82d955f95b0fca`. These prefixes are also recorded in `BLUEPRINT_DEPS` at module scope, enforced by `test_blueprint_deps_hashes_match_live_blueprints`.

# Merge path

At next §0.5 Thesis-round audit, merge this 1-row amendment into `section_00_5_interface_index_locked.md` as v5 (or v6 if GPP v5 amendment lands first). Row count would advance 99 → 100 (or to 100+N depending on parallel pending amendments).
