---
title: §0.5 Blueprint Interface Index — §15 Archivist rows amendment (LOCKED 2026-05-10)
filed: 2026-05-10
operator: Josh
status: LOCKED 2026-05-10 — compound paired-commit with §15 v1 LOCK per §6.17 Option-B. L-005 strict two-cycle CLOSED with FULL cross-family rigor (audit trail at pipeline/validation/blueprint_section_15_archivist_2026-05-10/{audit_v1_*.md, audit_v1_synthesis.md, audit_v2_*.md, audit_v2_synthesis.md}). Cycle 2 PARTIAL closures + NEW findings folded in at LOCK per row-170 transparent disposition pattern (mirrors WS-D v7.0.5 row 179 + WS-B v7.0.7 row 180 + WS-C-M1 v7.0.4-M1 row 190 precedents).
parent_locks:
  - pipeline/blueprint/v0.1/section_00_5_interface_index_locked.md                                 # §0.5 v5 LOCKED 2026-04-19 — 101 master rows
  - pipeline/blueprint/v0.1/section_00_5_section_06_operating_envelope_amendment.md                # §0.5 v6 LOCKED 2026-04-21 — rows 102-117
  - pipeline/blueprint/v0.1/section_00_5_section_07_scribe_amendment.md                            # §0.5 v7 LOCKED 2026-04-21 — rows 118-158
  - pipeline/blueprint/v0.1/section_00_5_section_10_red_team_amendment.md                          # §0.5 v8 LOCKED 2026-05-02 — rows 159-211
  - pipeline/blueprint/v0.1/section_00_5_section_12_uploader_amendment.md                          # §0.5 v9 LOCKED 2026-05-10 — rows 212-232
  - pipeline/blueprint/v0.1/section_00_5_section_11_intake_amendment.md                            # §0.5 v10 LOCKED 2026-05-10 — rows 233-256
  - pipeline/blueprint/v0.1/section_00_5_section_02_v7_2_operational_amendment.md                  # §0.5 v11 LOCKED 2026-05-10 — rows 257-278
  - pipeline/blueprint/v0.1/section_00_5_section_05_v8_amendment.md                                # §0.5 v12 LOCKED 2026-05-10 — rows 279-290
  - pipeline/blueprint/v0.1/section_15_archivist.md                                                # §15 v1 LOCKED 2026-05-10
companion_blueprint_amendment: pipeline/blueprint/v0.1/section_15_archivist.md  # paired-commit at §15 v1 LOCK per §6.17 Option-B
compound_lock_with: section_15_archivist.md v1
parent_wins_discipline: each row's parent_lock_version + parent_lock_commit_hash point at §15 v1; resolves to actual commit hash at LOCK ceremony.
row_delta: prior runtime-live total at §0.5 v12 LOCK 2026-05-10 = 290 rows. **§15 amendment claims rows 291-304 (14 rows: 1 marker + 3 input-schema + 4 digest-schema + 5 failure-code + 1 pre-gate-check).** New runtime-live total at this LOCK = 304.
kind_of_amendment: row-append. NO vocabulary extension — every row's `primitive_kind` resolves against the v5 + v6 16-value closed vocabulary (marker / schema / interface-contract / failure-code / pre-gate-check / post-gate-check).
dependency_order: §15 v1 LOCK + this §0.5 amendment land as a single compound paired-commit at the same `lock_timestamp_utc`. §4 v2.x amendment (Code session per WS-L, registering F-ARCHIVIST-* family — 5 codes — as proposes-only Cedar policies + extended R-ARCHIVIST-NO-CANONICAL-MUTATE AST-lint per RT-01/02/11 + Cycle 2 NF-01/02/05 closures) is the third sibling in the same compound transaction.
f_index_stale_preflight: F-INDEX-STALE PRE-gate fires at commit time; all 14 new rows must be present in the index or the commit fails closed.
cross_family_posture: LIVE FULL CROSS-FAMILY (no Section E carve-out) per WS-D v7.0.5 LOCK precedent (lock_history row 179, 2026-05-10). Six v0.1+v0.2 round to LOCK at this rigor level (after WS-D v7.0.5 architecture-class + WS-F §12 v1 + WS-E §11 v1 + WS-H §2 v7.2 + WS-G §5 v8 + WS-C-M1 v7.0.4-M1 blueprint/architecture-class precedents).
---

# Amendment intent

This amendment lands paired with §15 v1 LOCK per §6.17 Option-B compound-commit pattern. It registers §15-owned primitives (one section-anchor marker + three input-schema rows + four digest-schema rows + five failure-code rows + one consolidated pre-gate-check row) into the Index. It does NOT reserve section anchors for any other downstream blueprint — §15 is the last v0.2-wave seat-spec section to LOCK (Archivist is §15; Data Collector is §13 v0.2 horizon; Report Generator is §14 v0.2 horizon — both pending separate WS dispatches).

The §11 amendment (§0.5 v10 LOCKED 2026-05-10 with rows 233-256 across 24 rows) and the §12 amendment (§0.5 v9 LOCKED 2026-05-10 with rows 212-232 across 21 rows) are the load-bearing precedents for the explode-per-failure-code pattern. F-ARCHIVIST-* gate family at v1 contains 5 codes (smaller than §11's 11 because §15 is proposes-only between-cycle preservation rather than per-doc per-mode ingestion); this amendment registers one `failure-code` row per code (rows 299-303), then one consolidated `pre-gate-check` row (row 304) per the §4 v2.2 consolidated-check-callable pattern.

The master `section_00_5_interface_index_locked.md` remains LOCKED v5 on-disk; this amendment file is runtime-live at compound LOCK with §15. Future master re-author folds all v6 / v7 / v8 / v9 / v10 / v11 / v12 / this amendment files into the master.

# Amendment §A — row append (rows 291-304)

All rows enter §0.5 at `stability_tier = "STABLE"` at compound v1 LOCK (no PARENT_UNLOCKED transit since §15 LOCKs in the same compound transaction).

**Marker (row 291) — §15 section anchor:**

| Row | primitive_id | defined_at | parent_lock_version | parent_lock_commit_hash | kind | stability_tier |
|---|---|---|---|---|---|---|
| 291 | `blueprint.section_anchor.s15_archivist.v1` | `pipeline/blueprint/v0.1/section_15_archivist.md` | §15 v1 | `<resolved_at_commit>` | marker | STABLE |

**Schemas — input contracts (rows 292-294):**

| Row | primitive_id | defined_at | kind | Parent |
|---|---|---|---|---|
| 292 | `archivist.weekly_input.v1` | `pipeline/blueprint/v0.1/section_15_archivist.md#§15.4.1` | schema | ArchivistWeeklyInput frozen kw_only |
| 293 | `archivist.quarterly_workspace_input.v1` | `pipeline/blueprint/v0.1/section_15_archivist.md#§15.4.2.A` | schema | ArchivistQuarterlyWorkspaceInput frozen kw_only |
| 294 | `archivist.quarterly_per_org_input.v1` | `pipeline/blueprint/v0.1/section_15_archivist.md#§15.4.2.B` | schema | ArchivistQuarterlyPerOrgInput frozen kw_only |

**Schemas — digest entry contracts (rows 295-298):**

| Row | primitive_id | defined_at | kind | Parent |
|---|---|---|---|---|
| 295 | `archivist.kfr_refresh_digest.v1` | `pipeline/blueprint/v0.1/section_15_archivist.md#§15.5.1` | schema | KfrRefreshDigestEntry frozen kw_only; archivist_*-prefixed Archivist-introduced fields per §15.5.0.A; pointers-only schema (no upstream-substrate content re-encoded) |
| 296 | `archivist.match_db_lessons_delta.v1` | `pipeline/blueprint/v0.1/section_15_archivist.md#§15.5.1` | schema | MatchDbLessonsDeltaEntry frozen kw_only; pattern-level only per F-ARCHIVIST-LESSON-INSTANCE-LEAK |
| 297 | `archivist.funder_intel_quarterly.v1` | `pipeline/blueprint/v0.1/section_15_archivist.md#§15.5.2` | schema | FunderIntelQuarterlyEntry frozen kw_only; workspace-shared substrate per v7.0.5 §6 binding |
| 298 | `archivist.lessons_proposal.v1` | `pipeline/blueprint/v0.1/section_15_archivist.md#§15.5.2` | schema | LessonsProposalEntry frozen kw_only; pattern-level proposed_lesson_text per F-ARCHIVIST-LESSON-INSTANCE-LEAK three-layer detection (NFKC + NER + regex) |

**Failure codes (rows 299-303) — explode pattern per §10 / §11 / §12 precedent; one row per F-ARCHIVIST-* code at v1:**

| Row | primitive_id | defined_at | kind | Parent / sub-tags |
|---|---|---|---|---|
| 299 | `archivist.failure_code.F-ARCHIVIST-CROSS-ORG-LEAK.v1` | `pipeline/blueprint/v0.1/section_15_archivist.md#§15.9.1` | failure-code | PRE + POST. Sub-tags `.symlink_escape`, `.path_outside_org`, `.unconfirmed_substrate_read` (with metadata-only-read-tool contract per Judge DC-01 closure), `.workspace_digest_per_org_content`, `.aggregate_insufficient_orgs` (NEW per RT-06 closure — N=3 default workspace-aggregate threshold). |
| 300 | `archivist.failure_code.F-ARCHIVIST-LESSON-INSTANCE-LEAK.v1` | `pipeline/blueprint/v0.1/section_15_archivist.md#§15.9.2` | failure-code | PRE. Three-layer detection (Unicode NFKC + NER + regex) per RT-07 closure. Sub-tags `.client_name_present`, `.funder_specific_with_client`, `.reason_attributable_to_specific_outcome`, `.ner_entity_match` (NEW per RT-07), `.unicode_homoglyph` (NEW per RT-07). |
| 301 | `archivist.failure_code.F-ARCHIVIST-AUTO-APPLY-ATTEMPTED.v1` | `pipeline/blueprint/v0.1/section_15_archivist.md#§15.9.3` | failure-code | PRE three-layer (AST-lint + runtime guard + Cedar policy). Sub-tags `.ast_lint_violation`, `.runtime_dispatcher_violation`, `.cedar_policy_denied`, `.subprocess_canonical_cli_invocation` (NEW per RT-01), `.foreign_file_write_helper_import` (NEW per RT-02), `.principal_spoofing_detected` (NEW per RT-03), `.ffi_import_forbidden` (NEW per Cycle 2 RT-01 PARTIAL + NF-05 closure), `.dynamic_import_forbidden` (NEW per Cycle 2 RT-02 PARTIAL + RT-08 PARTIAL closure), `.token_rotation_requires_golden_image_rebuild` (NEW per Cycle 2 NF-03 disposition; advisory). |
| 302 | `archivist.failure_code.F-ARCHIVIST-CADENCE-DRIFT.v1` | `pipeline/blueprint/v0.1/section_15_archivist.md#§15.9.4` | failure-code | PRE. Informational at v0.2 (no scheduled cadence to drift from); v1.x severity=HIGH + action=FAIL_CLOSED per RT-10 closure. Sub-tags `.weekly_drift`, `.quarterly_workspace_drift`, `.quarterly_per_org_drift`. |
| 303 | `archivist.failure_code.F-ARCHIVIST-READ-WITHOUT-VAULT-INTENT.v1` | `pipeline/blueprint/v0.1/section_15_archivist.md#§15.9.5` | failure-code | PRE-substrate-read. NEW from RT-11 closure. Sub-tags `.raw_open_call`, `.generic_helper_import`, `.vault_intent_signature_invalid`, `.vault_intent_runtime_tampering` (NEW per Cycle 2 NF-01 closure — runtime-immutability self-check via function-id snapshot vs import-time snapshot). |

**PRE-gate-check (row 304) — consolidated per check callable per §4 v2.2 pattern:**

| Row | primitive_id | defined_at | kind | Parent / consolidated codes covered |
|---|---|---|---|---|
| 304 | `archivist.pre_gate.proposes_only_three_layer.v1` | `pipeline/blueprint/v0.1/section_15_archivist.md#§15.9.3` + `#§15.9.5` | pre-gate-check | Single check callable consolidating F-ARCHIVIST-AUTO-APPLY-ATTEMPTED (all sub-tags including the Cycle 2 .ffi_import_forbidden + .dynamic_import_forbidden + .token_rotation_requires_golden_image_rebuild closures) + F-ARCHIVIST-READ-WITHOUT-VAULT-INTENT (all sub-tags including the Cycle 2 .vault_intent_runtime_tampering closure). Both gates share the AST-lint + runtime-guard + Cedar policy three-layer pattern; consolidated check callable runs the union of all three layers per §4 v2.2 consolidated-check pattern. The other three F-ARCHIVIST-* codes (CROSS-ORG-LEAK, LESSON-INSTANCE-LEAK, CADENCE-DRIFT) have distinct check callables; v1.x amendment may consolidate further if implementation-level common code emerges. |

# Amendment §B — row description block (per-row narrative)

- **291** `blueprint.section_anchor.s15_archivist.v1` (kind=marker) — §15 Archivist section anchor. v0.2 SPEC LOCK; v1.x implementation deferred per dispatch packet decision 8d default. Between-cycle preservation seat (long-running curation work between grant cycles). Two cadences (weekly tick / quarterly review) with quarterly further routing to workspace OR per-org submodes per §15.4.2 split. Marker per `marker` precedent in v1 closed vocabulary (§0.5.3.1).
- **292** `archivist.weekly_input.v1` (kind=schema) — `ArchivistWeeklyInput` frozen kw_only Pydantic dataclass: run_id, org_slug, kfr_register_path (Path.resolve-normalized; under orgs/<org_slug>/), match_database_path (under orgs/<org_slug>/), lessons_json_path (under pipeline/institutional_memory/), lookback_window_days (default 7), invoked_at_utc, cadence (immutable "weekly"). Bundle invariants enforced PRE-gate by `archivist.pre_gate.proposes_only_three_layer.v1` + path-isolation per F-ARCHIVIST-CROSS-ORG-LEAK.
- **293** `archivist.quarterly_workspace_input.v1` (kind=schema) — `ArchivistQuarterlyWorkspaceInput` frozen kw_only: run_id, funder_intel_register_path (under vault_shared/funder_intelligence/), benchmarks_register_path (under vault_shared/benchmarks/), freshness_threshold_days (default 90), invoked_at_utc, cadence ("quarterly"), quarterly_mode ("quarterly_workspace").
- **294** `archivist.quarterly_per_org_input.v1` (kind=schema) — `ArchivistQuarterlyPerOrgInput` frozen kw_only: run_id, org_slug, kfr_register_path, match_database_path, reports_dir (under orgs/<org_slug>/vault/grants/), lookback_window_quarters (default 4), invoked_at_utc, cadence ("quarterly"), quarterly_mode ("quarterly_per_org").
- **295** `archivist.kfr_refresh_digest.v1` (kind=schema) — `KfrRefreshDigestEntry` frozen kw_only: digest_id, archivist_run_id, cadence, proposed_at_utc, proposed_action ("mark_stale" / "mark_pending_refresh" / "propose_archive" / "propose_supersede"), source_substrate_path, source_entry_id, rationale. Pointers-only per §15.5.0.A.
- **296** `archivist.match_db_lessons_delta.v1` (kind=schema) — `MatchDbLessonsDeltaEntry` frozen kw_only: digest_id, archivist_run_id, cadence, proposed_at_utc, proposed_action ("surface_pattern" / "propose_action_state_change" / "mark_for_review"), source_substrate_path, source_entry_id, pattern_summary (pattern-level only per F-ARCHIVIST-LESSON-INSTANCE-LEAK), rationale.
- **297** `archivist.funder_intel_quarterly.v1` (kind=schema) — `FunderIntelQuarterlyEntry` frozen kw_only: digest_id, archivist_run_id, proposed_at_utc, proposed_action ("mark_stale" / "propose_promotion" / "propose_drop" / "integrity_check_failed"), funder_id, source_substrate_path, source_entry_id, rationale. Workspace-shared per v7.0.5 §6 curation slot binding.
- **298** `archivist.lessons_proposal.v1` (kind=schema) — `LessonsProposalEntry` frozen kw_only: digest_id, archivist_run_id, proposed_at_utc, proposed_lesson_text (pattern-level only per F-ARCHIVIST-LESSON-INSTANCE-LEAK three-layer detection), source_lesson_refs (list of source lesson IDs), rationale. Mirrors Intake's `pending_facts.yaml → register.yaml` discipline applied to lessons curation: Archivist proposes; operator promotes via existing `tilth lessons promote` CLI.
- **299** `archivist.failure_code.F-ARCHIVIST-CROSS-ORG-LEAK.v1` (kind=failure-code) — PRE + POST. Per-org / workspace digest scope discipline. Sub-tags per §15.9.1 + RT-06 + RT-08 + Judge DC-01 closures.
- **300** `archivist.failure_code.F-ARCHIVIST-LESSON-INSTANCE-LEAK.v1` (kind=failure-code) — PRE. Three-layer detection (NFKC + NER + regex). Sub-tags per §15.9.2 + RT-07 closures. NF-04 NER adversarial-robustness disposition: bounded by v7 LOCKED A4 operator-trusted preflight.
- **301** `archivist.failure_code.F-ARCHIVIST-AUTO-APPLY-ATTEMPTED.v1` (kind=failure-code) — PRE three-layer (AST-lint + runtime guard + Cedar policy). Sub-tags per §15.9.3 + RT-01/02/03 + Cycle 2 RT-01 PARTIAL + NF-03 + NF-05 closures.
- **302** `archivist.failure_code.F-ARCHIVIST-CADENCE-DRIFT.v1` (kind=failure-code) — PRE. v0.2 informational; v1.x HIGH + FAIL_CLOSED per RT-10 closure.
- **303** `archivist.failure_code.F-ARCHIVIST-READ-WITHOUT-VAULT-INTENT.v1` (kind=failure-code; NEW from RT-11 + Cycle 2 NF-01 closures) — PRE-substrate-read. Three-layer enforcement: AST-lint + runtime guard + Vault read intent signature self-check + runtime-immutability self-check. Sub-tags per §15.9.5.
- **304** `archivist.pre_gate.proposes_only_three_layer.v1` (kind=pre-gate-check) — Single check callable consolidating F-ARCHIVIST-AUTO-APPLY-ATTEMPTED + F-ARCHIVIST-READ-WITHOUT-VAULT-INTENT (both share AST-lint + runtime-guard + Cedar three-layer pattern). Per §4 v2.2 consolidated-check pattern.

# Amendment §C — Vocabulary preservation

Every row in this amendment uses one of the 16-value closed `primitive_kind` vocabulary established at §0.5 v5 LOCK + extended at §0.5 v6 LOCK (`procedure`):

- `marker` (row 291) — already in the v1 closed vocabulary (§0.5.3.1).
- `schema` (rows 292, 293, 294, 295, 296, 297, 298).
- `failure-code` (rows 299, 300, 301, 302, 303).
- `pre-gate-check` (row 304).

**No vocabulary extension.** Every primitive_kind in this amendment resolves against the v5 + v6 closed set. F-INDEX-STALE precondition for vocabulary extension does NOT apply.

# Amendment §D — Stability tier

All 14 rows enter §0.5 at `stability_tier = "STABLE"` at compound v1 LOCK. No PARENT_UNLOCKED transit.

# Amendment §E — Row-count reconciliation (against runtime-live total)

| Surface | Rows |
|---|---|
| §0.5 v5 master LOCKED 2026-04-19 | 1–101 (101 rows) |
| §0.5 §6 operating-envelope amendment LOCKED 2026-04-21 | 102–117 (16 rows) |
| §0.5 §7 scribe amendment LOCKED 2026-04-21 | 118–158 (41 rows) |
| §0.5 §10 amendment LOCKED 2026-05-02 | 159–211 (53 rows) |
| §0.5 §12 amendment LOCKED 2026-05-10 | 212-232 (21 rows) |
| §0.5 §11 amendment LOCKED 2026-05-10 | 233–256 (24 rows) |
| §0.5 §2 v7.2 operational amendment LOCKED 2026-05-10 | 257–278 (22 rows) |
| §0.5 §5 v8 amendment LOCKED 2026-05-10 | 279–290 (12 rows) |
| **§0.5 §15 archivist amendment (this file)** | **291–304 (14 rows: 1 marker + 7 schema + 5 failure-code + 1 pre-gate-check)** |
| **Total runtime-live row count at this compound LOCK** | **304** (290 + 14) |

# Amendment §F — Companion JSON

`pipeline/blueprint/v0.1/section_00_5_section_15_archivist.json` — canonical-JSON encoding of this amendment's 14 rows. Sorted keys (`sort_keys=True`), UTF-8, LF, no trailing whitespace, no BOM, `ensure_ascii=False`, key separator `": "`, item separator `", "`. JSON companion's `index_version` field is `v13` (next runtime-live version after §0.5 v12 LOCKED 2026-05-10). Filename matches the per-section amendment-file pattern.

# Amendment §G — Paired-commit reminder

This §0.5 §15 amendment commits atomically with §15 v1 LOCK + §4 v2.x amendment LOCK (compound paired-commit per §6.17 Option-B; three-sibling transaction). F-INDEX-STALE PRE-gate fails-closed if any of the 14 rows are not in the index at the moment of compound commit.

# Amendment §H — Non-goals

- Does NOT modify any v5 master row.
- Does NOT modify any v6 / v7 / v8 / v9 / v10 / v11 / v12 amendment row.
- Does NOT reserve §13 / §14 section anchors (each downstream blueprint claims its own at its own v1 LOCK).
- Does NOT modify F-INDEX-STALE semantics.
- Does NOT extend the closed `primitive_kind` vocabulary.
- Does NOT modify `section_00_5_interface_index_locked.md` on disk — master re-author is a separate ceremony.

# Amendment §I — L-005 audit record

**Status: LOCKED 2026-05-10** — L-005 strict two-cycle CLOSED with FULL cross-family rigor + row-170 transparent disposition for Cycle 2 PARTIAL + NEW Red Team findings (operator-confirmation-precedent applied per WS-D + WS-B + WS-C-M1 row-170 pattern). Audit trail at:
- Cycle 1: `pipeline/validation/blueprint_section_15_archivist_2026-05-10/audit_v1_{editor,judge,red_team}.md` + `audit_v1_synthesis.md`
- Cycle 2: `pipeline/validation/blueprint_section_15_archivist_2026-05-10/audit_v2_{editor,judge,red_team}.md` + `audit_v2_synthesis.md`

Cycle 2 verdicts: Editor READY_TO_LOCK + Judge READY_TO_LOCK 100/100 + Red Team REQUIRES_FIXES dispositioned via row-170 transparent disposition (4 PARTIAL + 5 NEW folded in at LOCK with explicit text-level closures + bounded-by-v7-LOCKED-A1+A4 dispositions).

# End of amendment
