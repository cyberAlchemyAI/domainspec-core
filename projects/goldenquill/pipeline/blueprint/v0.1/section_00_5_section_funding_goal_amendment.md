---
title: §0.5 Blueprint Interface Index — Funding Goal paired-commit amendment (v20 — LOCKED 2026-05-11)
filed: 2026-05-11
operator: Josh
status: LOCKED 2026-05-11 — compound paired-commit (sibling 4/4) with §2 v7.5 + §3 v6 + §4 v2.x.4 at the same `lock_timestamp_utc` per §6.17 Option-B. L-005 strict two-cycle CLOSED with FULL LIVE CROSS-FAMILY rigor (audit trail at `pipeline/validation/funding_goal_thesis_2026-05-11/{audit_v{1,2}_*.md, cycle_{1,2}_disposition.md}`). Eleventh substantive v0.1+v0.2 round to LOCK at FULL live cross-family rigor.
parent_locks:
  - pipeline/blueprint/v0.1/section_00_5_interface_index_locked.md                                 # §0.5 v5 LOCKED 2026-04-19 — 101 master rows
  - pipeline/blueprint/v0.1/section_00_5_section_06_operating_envelope_amendment.md                # §0.5 v6 LOCKED 2026-04-21 — rows 102-117
  - pipeline/blueprint/v0.1/section_00_5_section_07_scribe_amendment.md                            # §0.5 v7 LOCKED 2026-04-21 — rows 118-158
  - pipeline/blueprint/v0.1/section_00_5_section_10_red_team_amendment.md                          # §0.5 v8 LOCKED 2026-05-02 — rows 159-211
  - pipeline/blueprint/v0.1/section_00_5_section_12_uploader_amendment.md                          # §0.5 v9 LOCKED 2026-05-10 — rows 212-232
  - pipeline/blueprint/v0.1/section_00_5_section_11_intake_amendment.md                            # §0.5 v10 LOCKED 2026-05-10 — rows 233-256
  - pipeline/blueprint/v0.1/section_00_5_section_02_v7_2_operational_amendment.md                  # §0.5 v11 LOCKED 2026-05-10 — rows 257-278
  - pipeline/blueprint/v0.1/section_00_5_section_05_v8_amendment.md                                # §0.5 v12 LOCKED 2026-05-10 — rows 279-290
  - pipeline/blueprint/v0.1/section_00_5_section_15_archivist_amendment.md                         # §0.5 v13 LOCKED 2026-05-10 — rows 291-304
  - pipeline/blueprint/v0.1/section_00_5_section_04_v2_x_amendment.md                              # §0.5 v14 LOCKED 2026-05-10 — rows 305-348
  - pipeline/blueprint/v0.1/section_00_5_section_13_data_collector_amendment.md                    # §0.5 v15 LOCKED 2026-05-10 — rows 349-376
  - pipeline/blueprint/v0.1/section_00_5_section_04_v2_x_1_amendment.md                            # §0.5 v16 LOCKED 2026-05-10 — rows 377-378
  - pipeline/blueprint/v0.1/section_00_5_section_14_report_generator_amendment.md                  # §0.5 v17 LOCKED 2026-05-10 — rows 379-395
  - pipeline/blueprint/v0.1/section_00_5_section_15_reflection_amendment.md                        # §0.5 v18 LOCKED 2026-05-10 — rows 396-413
  - pipeline/blueprint/v0.1/section_00_5_section_17_wpfa_amendment.md                              # §0.5 v19 LOCKED 2026-05-11 — rows 414-445; vocabulary extension `ast-lint` kind landed
  - pipeline/blueprint/v0.1/section_02_v7_5_funding_goal_amendment.md                              # §2 v7.5 (paired-commit sibling 1/4)
  - pipeline/blueprint/v0.1/section_03_v6_funding_goal_amendment.md                                # §3 v6 (paired-commit sibling 2/4; bundles §6.x prompt-compilation goals-block per OQ-2)
  - pipeline/blueprint/v0.1/section_04_v2_x_4_funding_goal_amendment.md                            # §4 v2.x.4 (paired-commit sibling 3/4)
companion_blueprint_amendment: pipeline/blueprint/v0.1/section_02_v7_5_funding_goal_amendment.md  # paired-commit per §6.17 Option-B
compound_lock_with: section_02_v7_5_funding_goal_amendment.md v7.5 + section_03_v6_funding_goal_amendment.md v6 + section_04_v2_x_4_funding_goal_amendment.md v2.x.4
parent_wins_discipline: each row's parent_lock_version + parent_lock_commit_hash point at §2 v7.5, §3 v6, or §4 v2.x.4; resolves to actual commit hash at LOCK ceremony.
row_delta: prior runtime-live total at §0.5 v19 LOCK 2026-05-11 = 445 rows. **§0.5 v20 amendment claims rows 446-470 (25 rows: 1 marker + 5 schema + 9 interface-contract + 8 failure-code + 3 ast-lint).** Plus two extra ast-lint rows (469, 470) per Cycle 2 RT-C2-04 + RT-C2-10 closures. New runtime-live total at this LOCK = 470.
kind_of_amendment: row-append with seat_owner attribute extension per RT-19. NO new vocabulary kind — every row's `primitive_kind` resolves against the v5 + v6 + v19 closed vocabulary (marker / schema / interface-contract / failure-code / pre-gate-check / post-gate-check / ast-lint).
seat_owner_attribute: every row in this amendment carries `seat_owner: "funding_goal"` per RT-19. F-INDEX-STALE PRE-gate at compound commit verifies seat_owner consistency across all 25 rows; deviation triggers F-INDEX-STALE with sub-tag `.seat_owner_mismatch` per RT-C2-09.
dependency_order: §2 v7.5 + §3 v6 + §4 v2.x.4 + this §0.5 amendment land as a single compound paired-commit at the same `lock_timestamp_utc`. F-INDEX-STALE PRE-gate fires at commit time per §6.2 order 3; all 25 new rows must be present in the index or the compound commit fails closed.
f_index_stale_preflight: F-INDEX-STALE PRE-gate fires at commit time; all 25 new rows must be present in the index AND every row must carry seat_owner: "funding_goal" or the commit fails closed.
cross_family_posture: LIVE FULL CROSS-FAMILY (no Section E carve-out) per WS-D v7.0.5 LOCK precedent. ELEVENTH v0.1+v0.2 round to LOCK at this rigor level (after WS-D v7.0.5 + WS-F §12 v1 + WS-E §11 v1 + WS-H §2 v7.2 + WS-G §5 v8 + WS-K §15 + WS-C-M1 v7.0.4-M1 + WS-L §4 v2.x + WS-I §13 v1 + WS-J §14 v1 + WS-Reflection v0.1 hook + WS-WPFA precedents).
---

# Amendment intent

This amendment lands paired with §2 v7.5 + §3 v6 + §4 v2.x.4 LOCK per §6.17 Option-B compound-commit pattern. It registers Funding Goal-owned primitives (one section-anchor marker + five schema rows + nine interface-contract rows + eight failure-code rows + three ast-lint rows = 25 rows) into the Index. Every row carries `seat_owner: "funding_goal"` per Cycle 2 RT-19 closure; F-INDEX-STALE PRE-gate verifies consistency at commit.

The §17 WPFA amendment (§0.5 v19 LOCKED 2026-05-11 with rows 414-445 across 32 rows + `ast-lint` vocabulary extension) is the most-recent precedent. Funding Goal compound LOCK adds 25 rows (446-470).

The master `section_00_5_interface_index_locked.md` remains LOCKED v5 on-disk; this amendment file is runtime-live at compound LOCK with §2 v7.5 + §3 v6 + §4 v2.x.4. Future master re-author folds all v6-v20 amendment files into the master.

# Amendment §A — row append (rows 446-470)

All rows enter §0.5 at `stability_tier = "STABLE"` at compound v1 LOCK (no PARENT_UNLOCKED transit since §2 v7.5 + §3 v6 + §4 v2.x.4 LOCK in the same compound transaction).

**Marker (row 446) — §2 v7.5 section anchor:**

| Row | primitive_id | defined_at | parent_lock_version | parent_lock_commit_hash | kind | seat_owner | stability_tier |
|---|---|---|---|---|---|---|---|
| 446 | `blueprint.section_anchor.s02_v7_5_funding_goal.v1` | `pipeline/blueprint/v0.1/section_02_v7_5_funding_goal_amendment.md` | §2 v7.5 | `<resolved_at_commit>` | marker | funding_goal | STABLE |

**Schemas (rows 447-451):**

| Row | primitive_id | defined_at | kind | seat_owner | Parent |
|---|---|---|---|---|---|
| 447 | `vault.sub_kinds.funding_goal.v1` | `section_02_v7_5_funding_goal_amendment.md#§2.11.8` | schema | funding_goal | `FundingGoal` frozen kw_only |
| 448 | `vault.sub_kinds.funding_goal.goal_blocker.v1` | `section_02_v7_5_funding_goal_amendment.md#§2.11.8` | schema | funding_goal | `GoalBlocker` frozen kw_only |
| 449 | `vault.sub_kinds.funding_goal.canonical_codec.v1` | `pipeline/vault/sub_kinds/funding_goals.py:to_canonical_bytes,from_canonical_bytes` | interface-contract | funding_goal | canonical-JSON round-trip codec (LIVE at v0.2) |
| 450 | `vault.sub_kinds.funding_goal.resolve_live.v1` | `pipeline/vault/sub_kinds/funding_goals.py:resolve_live` | interface-contract | funding_goal | thin status-resolution helper per OQ-5 (LIVE at v0.2); atomic ledger-lookup + status-write within fcntl.flock(LOCK_EX) per RT-C2-05 |
| 451 | `vault.sub_kinds.registry.funding_goal_descriptor.v1` | `section_02_v7_5_funding_goal_amendment.md#§2.12` | interface-contract | funding_goal | `SUB_KIND_REGISTRY["funding_goal"]` row |

**Cedar policy interface-contracts (rows 452-454):**

| Row | primitive_id | defined_at | kind | seat_owner | Parent |
|---|---|---|---|---|---|
| 452 | `vault.policy.operational_subkinds.cedar.goal_status_transition.v1` | `pipeline/vault/policies/operational_subkinds.cedar` | interface-contract | funding_goal | Cedar rule `goal_status_transition` per §2.16 |
| 453 | `vault.policy.operational_subkinds.cedar.goal_priority_mutation_audited.v1` | `pipeline/vault/policies/operational_subkinds.cedar` | interface-contract | funding_goal | Cedar rule `goal_priority_mutation_audited` per §2.16 |
| 454 | `vault.policy.operational_subkinds.cedar.goal_taxonomy_closed.v1` | `pipeline/vault/policies/operational_subkinds.cedar` | interface-contract | funding_goal | Cedar rule `goal_taxonomy_closed` per §2.16 |

**Allowlist + layout (rows 455-456):**

| Row | primitive_id | defined_at | kind | seat_owner | Parent |
|---|---|---|---|---|---|
| 455 | `vault.post_gate_allowlist.operational-funding-goal-write.v1` | `section_02_v7_5_funding_goal_amendment.md#§2.13` | interface-contract | funding_goal | §2.13 allowlist row |
| 456 | `vault.layout.org_vault_operational_funding_goals.v1` | `section_02_v7_5_funding_goal_amendment.md#§2.14` | interface-contract | funding_goal | `VaultLayout.org_vault_operational_funding_goals(slug)`; slug validation (RT-01 + RT-C2-01) + O_NOFOLLOW (RT-02 + RT-C2-02) |

**Failure codes (rows 457-464) — explode-per-code pattern per §10/§11/§12/§13/§14/§15/§17 precedent:**

| Row | primitive_id | defined_at | kind | seat_owner | Parent / sub-tags |
|---|---|---|---|---|---|
| 457 | `logician.failure_code.F-FG-CROSS-ORG-LEAK.v1` | `section_04_v2_x_4_funding_goal_amendment.md#§4.X.4.2` | failure-code | funding_goal | **P0 (Law 3) — no M13 bypass.** Sub-tags `.path_traversal_detected`, `.unicode_normalization_bypass`, `.symlink_detected`, `.toctou_path_dereference`, `.cedar_engine_unavailable_fail_closed`, `.principal_org_slug_externally_supplied`. |
| 458 | `logician.failure_code.F-FG-SCHEMA-INVALID.v1` | `section_04_v2_x_4_funding_goal_amendment.md#§4.X.4.2` | failure-code | funding_goal | UMBRELLA module realizes 458 + 459 + 460. Sub-tags `.float_target_amount_detected`, `.invariant_<n>_violated`, `.canonical_round_trip_drift`, `.record_id_path_traversal`, `.future_timestamp`, `.match_db_estimated_contribution_float_detected`. |
| 459 | `logician.failure_code.F-FG-CIC-TAG-INVALID.v1` | `section_04_v2_x_4_funding_goal_amendment.md#§4.X.4.2` | failure-code | funding_goal | Sub-code under umbrella `f_fg_schema_validation.py`. |
| 460 | `logician.failure_code.F-FG-CLC-TAG-INVALID.v1` | `section_04_v2_x_4_funding_goal_amendment.md#§4.X.4.2` | failure-code | funding_goal | Sub-code under umbrella `f_fg_schema_validation.py`. |
| 461 | `logician.failure_code.F-FG-STATUS-TRANSITION-INVALID.v1` | `section_04_v2_x_4_funding_goal_amendment.md#§4.X.4.2` | failure-code | funding_goal | Sub-tags `.met_replay_attempted`, `.ledger_entry_missing`, `.malformed_ledger_entry`, `.ledger_lock_timeout`, forbidden-transition base case. |
| 462 | `logician.failure_code.F-FG-LINKED-CYCLE-ORPHAN.v1` | `section_04_v2_x_4_funding_goal_amendment.md#§4.X.4.2` | failure-code | funding_goal | **HIGH (effective P0 when `.cross_org_grant_reference` sub-tag fires per §4.X.4.1 severity inheritance rule).** Sub-tags `.cross_org_grant_reference` (P0; no M13 bypass), `.symlink_in_grant_path`, `.grant_path_outside_org_subtree`, advisory base case. |
| 463 | `logician.failure_code.F-FG-PRIORITY-MUTATION-UNAUDITED.v1` | `section_04_v2_x_4_funding_goal_amendment.md#§4.X.4.2` | failure-code | funding_goal | Priority changed without admin-risk-ledger entry. M13 audited. |
| 464 | `logician.failure_code.F-FG-DEADLINE-EXPIRED-IGNORED.v1` | `section_04_v2_x_4_funding_goal_amendment.md#§4.X.4.2` | failure-code | funding_goal | Deadline past + status pursuing. ADVISORY. M13 NOT needed. |

**AST-lint rules (rows 465 + 469-470) — under `ast-lint` vocabulary kind landed at §0.5 v19 §A.AST_LINT:**

| Row | primitive_id | defined_at | kind | seat_owner | Parent |
|---|---|---|---|---|---|
| 465 | `linting.r_fg_no_float_monetary.v1` | `pipeline/linting/r_fg_no_float_monetary.py` | ast-lint | funding_goal | A12 Decimal mandate enforcement. Scope: `pipeline/vault/sub_kinds/funding_goals.py` + `pipeline/match_db/scoring.py` + ALL sub-directories under `pipeline/match_db/` (recursive per RT-13 + RT-C2-07). Mirrors §17 WPFA RT-C2-01 R-WPFA-DECIMAL-MANDATE-ENERGY scope-extension precedent. |
| 469 | `linting.r_fg_no_catch_critical.v1` | `pipeline/linting/r_fg_no_catch_critical.py` | ast-lint | funding_goal | RT-C2-04 closure. Flags any `except BaseException` or `except CriticalPolicyError` constructs outside the Cedar-engine bootstrap module. Scope: workspace-wide. |
| 470 | `linting.r_fg_stub_only_at_v0_2.v1` | `pipeline/linting/r_fg_stub_only_at_v0_2.py` | ast-lint | funding_goal | RT-C2-10 closure. Flags any file under `pipeline/logician/gates/` defining an `F-FG-*` gate that lacks `raise NotImplementedError` AT v0.2 first ship. v1.x amendment lifts this restriction. Enforces SPEC-ONLY discipline structurally. |

**Scout DISCOVER + Match DB scoring interface-contracts (rows 466-468):**

| Row | primitive_id | defined_at | kind | seat_owner | Parent |
|---|---|---|---|---|---|
| 466 | `scout.discover.input_shape.funding_goals_block.v1` | `section_03_v6_funding_goal_amendment.md#§3.6+§3.8` | interface-contract | funding_goal | DISCOVER goals-block injection + slug validation (RT-01 + RT-C2-01) + O_NOFOLLOW (RT-02 + RT-C2-02) + classification-aware redaction (OQ-6 + RT-10 + RT-11) + numeric opaque slot enforcement (RT-12 + RT-C2-06) |
| 467 | `scout.discover.fit_score_cached.goal_aware_composer.v1` | `section_03_v6_funding_goal_amendment.md#§3.7.1` | interface-contract | funding_goal | Additive composition per dimension (RT-17); zero-LLM deterministic Python; Decimal arithmetic per v7.0.4-M1 §6 |
| 468 | `match_db.scoring.goal_aware_match_score.v1` | `pipeline/match_db/scoring.py:goal_aware_match_score` | interface-contract | funding_goal | Decimal-mandate composition callable; explicit `Decimal(int(...))` casts per RT-15; stringified-Decimal persistence per RT-16; OQ-7 routed under interface-contract per minimum-vocabulary-extension discipline (per Judge J-02 convention: new logic primitives parent under the primary logic amendment for a compound lock; this row's parent is §4 v2.x.4) |

**Row range: 446-470 (25 rows). Runtime-live total at compound LOCK: 470.**

**§0.5 vocabulary check:** every row resolves against the v5 + v6 + v19 closed vocabulary (marker / schema / interface-contract / failure-code / pre-gate-check / post-gate-check / ast-lint). NO further vocabulary extension required.

**Parent-wins discipline (E-05 closure):** each row's `parent_lock_version` + `parent_lock_commit_hash` resolve at LOCK ceremony to the actual sibling commit hash:
- Rows 446-456 → §2 v7.5 commit hash
- Rows 457-465 → §4 v2.x.4 commit hash
- Rows 466-467 → §3 v6 commit hash
- Row 468 → §4 v2.x.4 commit hash (per Judge J-02 convention)
- Rows 469-470 → §4 v2.x.4 commit hash (AST-lint rules realize Cycle 2 closures from F-FG-* family discipline)

**§A.SEAT_OWNER seat_owner attribute consistency check (RT-19 + RT-C2-09):** F-INDEX-STALE PRE-gate verifies every row in compound-LOCK range 446-470 contains `seat_owner: "funding_goal"`; any deviation triggers F-INDEX-STALE with sub-tag `.seat_owner_mismatch`. New §0.5 invariant per RT-C2-09 closure; mirrors §17 WPFA §0.5 v19 §5 F-CIC-CLC-COUPLING-VIOLATION-class regression test pattern.

# Amendment §B — F-CIC-CLC-COUPLING-VIOLATION regression test

Per §9 of spec card v3, every Thesis cycle (Cycle 1 + Cycle 2) ran the F-CIC-CLC-COUPLING-VIOLATION regression test against:
- The `funding_goal` schema (single-valued `cic_tag` + zero-or-more `clc_tags`).
- The Cedar `goal_taxonomy_closed` rule (independent set membership; no pre-mapping).
- The Scout DISCOVER ranking function (additive composition per RT-17; no AND-gating).
- The Match DB scoring composer (`goal_aware_match_score` independent dimensions).

All four detection layers (lexical regex / Pydantic AST / value-set / KP schema) PASS. CIC × CLC orthogonality preserved at all four layers per v7.0.8 LOCK + CLAUDE.md "CIC × CLC orthogonal — never pre-map".

# Amendment §C — F-FG-* family closed-set membership check (Path B regression)

Per §9 last bullet of spec card v3, every Thesis cycle ran the closed-set-membership check:
- No F-FG-* code crosses ownership to F-WPFA-/F-REFLECTION-/F-PACKET-/F-CLASS-/F-MATCH-DB-/F-DATACOLLECTOR-/F-REPORT-/F-ARCHIVIST-* family.
- All 8 F-FG-* failure-code rows + 3 R-FG-* AST-lint rows + 9 funding_goal-owned interface-contract rows + 5 funding_goal-owned schema rows + 1 funding_goal-owned marker row carry `seat_owner: "funding_goal"`.

PASS at both Cycle 1 and Cycle 2. F-FG-* family closed-set membership preserved.

# Changelog

- 2026-05-11 §0.5 v20 LOCKED — compound paired-commit (sibling 4/4) with §2 v7.5 + §3 v6 + §4 v2.x.4. 25 rows (446-470). seat_owner attribute extension per RT-19. NEW AST-lint primitives at rows 469 (R-FG-NO-CATCH-CRITICAL per RT-C2-04) + 470 (R-FG-STUB-ONLY-AT-V0_2 per RT-C2-10). Eleventh substantive v0.1+v0.2 round to LOCK at FULL live cross-family rigor. All 37 Cycle 1 + 13 Cycle 2 dispositions absorbed.
