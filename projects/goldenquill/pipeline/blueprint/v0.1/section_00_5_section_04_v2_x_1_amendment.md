---
title: §0.5 Blueprint Interface Index — §4 v2.x.1 corrective Tilth-RT-07 closure (LOCKED 2026-05-10)
filed: 2026-05-10
operator: Josh
status: LOCKED 2026-05-10 — compound paired-commit with §4 v2.x.1 LOCK per §6.17 Option-B. L-005 strict two-cycle CLOSED with FULL live cross-family rigor (audit trail at pipeline/validation/v4_v2_x_1_thesis_2026-05-10/). Cycle 2 closure FOLDED-IN at LOCK per row-170 transparent-disposition pattern (mirrors WS-D v7.0.5 row 179 + WS-B v7.0.7 row 180 + WS-C-M1 v7.0.4-M1 row 190 + §15 Archivist v1 rows 191/192 + WS-L §4 v2.x rows 193/194 + WS-I §13 rows 196/197 precedents). Ninth substantive v0.1+v0.2 round to LOCK at FULL live cross-family rigor.
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
  - pipeline/blueprint/v0.1/section_04_v2_x_1_amendment.md                                         # §4 v2.x.1 LOCKED 2026-05-10
companion_blueprint_amendment: pipeline/blueprint/v0.1/section_04_v2_x_1_amendment.md  # paired-commit at §4 v2.x.1 LOCK per §6.17 Option-B
compound_lock_with: section_04_v2_x_1_amendment.md
parent_wins_discipline: each row's parent_lock_version + parent_lock_commit_hash point at §4 v2.x.1; resolves to actual commit hash at LOCK ceremony.
row_delta: prior runtime-live total at §0.5 v15 LOCK 2026-05-10 = 376 rows. **§4 v2.x.1 amendment claims rows 377-378 (2 rows: 1 marker + 1 enforcement-infrastructure primitive row).** New runtime-live total at this LOCK = 378.
kind_of_amendment: row-append. NO vocabulary extension — every row's `primitive_kind` resolves against the v5 + v6 closed vocabulary (marker / enforcement-infrastructure).
dependency_order: §4 v2.x.1 LOCK + this §0.5 amendment land as a single compound paired-commit at the same `lock_timestamp_utc`.
f_index_stale_preflight: F-INDEX-STALE PRE-gate fires at commit time; all 2 new rows must be present in the index or the commit fails closed.
cross_family_posture: LIVE FULL CROSS-FAMILY (no Section E carve-out) per WS-D v7.0.5 LOCK precedent (lock_history row 179, 2026-05-10). Ninth substantive v0.1+v0.2 round to LOCK at this rigor level.
narrow_corrective_precedent: v7.0.4-M1 (lock_history row 190) — same pattern (narrow extension of LOCKed predicate body via dedicated module + §0.5 paired commit; parent text not modified in place).
---

# Amendment intent

This amendment lands paired with §4 v2.x.1 LOCK per §6.17 Option-B compound-commit pattern. §4 v2.x.1 is a **narrow-corrective amendment** closing Tilth-RT-07 PARTIAL via R-ARCHIVIST-NO-CANONICAL-MUTATE AST-lint enumeration extension (six low-level rename primitive sub-tags under the existing `F-ARCHIVIST-AUTO-APPLY-ATTEMPTED` failure code at row 301). It mirrors the v7.0.4-M1 narrow-corrective pattern (row 190) — the parent §4 v2.x amendment text at rows 193/194 is NOT modified in place; instead, a dedicated module + amendment file land as the authoritative source for the extension.

Because the sub-tag enumeration extends an existing failure code (row 301 `F-ARCHIVIST-AUTO-APPLY-ATTEMPTED`) rather than registering a new top-level code, this §0.5 paired commit lands only **two rows**: a §4 v2.x.1 amendment-anchor marker (row 377) + an enforcement-infrastructure primitive row for the new dedicated AST-lint rule module (row 378). Sub-tag set extends from row 301's existing closure (`.ast_lint_violation`, `.runtime_dispatcher_violation`, `.cedar_policy_denied`, `.subprocess_canonical_cli_invocation`, `.foreign_file_write_helper_import`, `.principal_spoofing_detected`, `.ffi_import_forbidden`, `.dynamic_import_forbidden`, `.token_rotation_requires_golden_image_rebuild`) with six new `.low_level_rename_*` sub-tags (`replace`, `rename`, `renames` [Cycle-1 RT-09 fold-in], `shutil_move`, `shutil_copy`, `os_link`). Owner remains §15.9.3 per row 301 parent_lock_version; this amendment is a sub-tag extension under the existing owner, not a re-parent.

The master `section_00_5_interface_index_locked.md` remains LOCKED v5 on-disk; this amendment file is runtime-live at compound LOCK with §4 v2.x.1. Future master re-author folds all v6 / v7 / ... / this amendment files into the master.

# Amendment §A — row append (rows 377-378)

All rows enter §0.5 at `stability_tier = "STABLE"` at compound v2.x.1 LOCK (no PARENT_UNLOCKED transit since §4 v2.x.1 LOCKs in the same compound transaction).

**Marker (row 377) — Tilth-RT-07 / §4 v2.x.1 amendment anchor:**

| Row | primitive_id | defined_at | parent_lock_version | parent_lock_commit_hash | kind | stability_tier |
|---|---|---|---|---|---|---|
| 377 | `blueprint.amendment_anchor.s4_v2_x_1.v1` | `pipeline/blueprint/v0.1/section_04_v2_x_1_amendment.md` | §4 v2.x.1 | `<resolved_at_commit>` | marker | STABLE |

**Enforcement-infrastructure (row 378) — R-ARCHIVIST-NO-CANONICAL-MUTATE rule module (per ARCH-04 enforcement-infrastructure precedent at row 100):**

| Row | primitive_id | defined_at | parent_lock_version | parent_lock_commit_hash | kind | stability_tier |
|---|---|---|---|---|---|---|
| 378 | `linting.r_archivist_no_canonical_mutate.v1` | `pipeline/linting/r_archivist_no_canonical_mutate.py` (sha3_512[:16] resolved at commit time) | §4 v2.x.1 | `<resolved_at_commit>` | enforcement-infrastructure | STABLE |

**Row 378 description:** Deterministic AST-lint rule module for the R-ARCHIVIST-NO-CANONICAL-MUTATE low-level-rename-primitives enumeration extension. Exposes `ARCHIVIST_NO_CANONICAL_MUTATE: Rule` + `FORBIDDEN_PRIMITIVES: Mapping[(str,str), str]` (immutable `types.MappingProxyType` view over an internal mutable source-of-truth dict per Cycle-1 RT-14 fold-in). The rule fires under `pipeline/orchestrator/seats/archivist/**/*.py` and emits one `Violation` per offending `ast.Call` node with `reason_tag = "archivist_auto_apply_attempted.<sub_tag>"` (six sub-tags) and `message` body carrying `F-ARCHIVIST-AUTO-APPLY-ATTEMPTED` failure-code attribution. Single source of truth for the forbidden-call set; the future §15 v1.x runtime-guard wrapper extension must mirror this table per the v1.x amendment-realization checklist contract at §4 v2.x.1 §4. Lazy-imported into `pipeline.linting.ast_lint.DEFAULT_RULES` via `_section_04_v2_x_1_rules()` block (mirrors the WS-L Slice 4 `_wsl_slice4_rules()` decomposition pattern — one rule per file for reading-surface coherence + minimal blast radius).

## Row 301 sub-tag closure extension (annotation; not a row mutation)

Row 301 (`archivist.failure_code.F-ARCHIVIST-AUTO-APPLY-ATTEMPTED.v1`, parent §15 v1, in §0.5 v13 amendment at rows 291-304) carries the failure code at §15.9.3. The Cycle-1 RT-09-extended sub-tag set adds six new `.low_level_rename_*` sub-tags (`replace`, `rename`, `renames`, `shutil_move`, `shutil_copy`, `os_link`) under §4 v2.x.1's predicate body. This is documented as a sub-tag extension under the existing row 301 owner — **NOT** a new row, **NOT** a re-parent. The §0.5 v13 amendment row 301 narrative does not change; the §4 v2.x.1 amendment text + the new enforcement-infrastructure row 378 carry the sub-tag extension narrative.

Consumers of the §0.5 Index that resolve row 301's sub-tag set must consult both the §0.5 v13 amendment row 301 narrative AND the §4 v2.x.1 amendment text at §0 + Appendix A for the canonical six-sub-tag enumeration.

# Amendment §B — row delta + invariants

- Runtime-live total at §0.5 v15 LOCK = 376 rows.
- This amendment adds 2 rows (1 marker + 1 enforcement-infrastructure primitive).
- New runtime-live total at compound LOCK = 378 rows.
- Vocabulary preservation: every row's `primitive_kind` resolves against the v5 + v6 closed vocabulary (marker + enforcement-infrastructure).
- F-INDEX-STALE PRE-gate fires at commit time; both new rows must be present in the index or the commit fails closed.

# Amendment §C — sub-tag-extension precedent

This amendment establishes the **narrow-corrective + sub-tag-extension §0.5 paired-commit pattern**:

- When a narrow-corrective amendment (mirroring v7.0.4-M1 row 190) extends sub-tags under an existing failure code rather than registering a new top-level failure code, the §0.5 paired commit lands only:
  - One marker row for the amendment anchor.
  - Zero or more enforcement-infrastructure rows for new dedicated module(s).
  - **NO** new failure-code row (the existing failure-code row's sub-tag set extends in-place at the narrative level; the §0.5 v13/v14/etc. amendment hosting the failure-code row gains an annotation in its row description block referencing the new sub-tag closure).

This is distinct from the **failure-code-row-explode pattern** at §10 / §11 / §12 / §13 / §15 v1 (one row per F-ARCHIVIST-*/F-INTAKE-*/F-UPLOADER-*/F-DATACOLLECTOR-* code) — those amendments registered *new* failure codes. §4 v2.x.1 reuses existing row 301 owner; the precedent applies to any future narrow-corrective amendment that extends an existing failure code's sub-tag set.

# Amendment §D — cross-references

- §4 v2.x.1 LOCK: `pipeline/blueprint/v0.1/section_04_v2_x_1_amendment.md` (LOCKED 2026-05-10)
- Audit trail: `pipeline/validation/v4_v2_x_1_thesis_2026-05-10/{audit_prompt_v1_*.md, audit_v1_*.md, audit_v1_synthesis.md, audit_prompt_v2_*.md, audit_v2_*.md, audit_v2_synthesis.md, dispatch_audit_v{1,2}.sh}`
- Predecessor disposition packet: `pipeline/planning/section_15_external_review_disposition_2026-05-10.md` §2.1 (lock_history row 195)
- Backlog packet: `pipeline/planning/section_04_v2_x_1_tilth_rt_07_backlog_2026-05-10.md`
- Parent §15 v1 SPEC LOCK: rows 191/192 (§0.5 v13 amendment hosts row 301 `F-ARCHIVIST-AUTO-APPLY-ATTEMPTED`)
- Parent §4 v2.x LOCK: rows 193/194 (predicate-body home for the AST-lint rule's existing enumeration at §15.13.1 line 694)
- Narrow-corrective + sub-tag-extension precedent: this amendment (the v7.0.4-M1 precedent at row 190 is corrective at the architectural layer; this is the first §0.5 narrow-corrective at the blueprint-amendment + sub-tag-extension layer)
- v7.0.4-M1 corrective precedent: `pipeline/architecture/v0.1/architecture_v7_0_4_M1_amendment.md` (lock_history row 190)
- ARCH-04 enforcement-infrastructure precedent at row 100: `pipeline/blueprint/v0.1/section_00_5_arch04_ast_lint_amendment.md`
