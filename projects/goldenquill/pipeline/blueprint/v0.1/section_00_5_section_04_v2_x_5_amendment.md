---
title: §0.5 v27 — Interface Index paired-commit for §4 v2.x.5 narrow-corrective amendment (CC-007 seat-local provider HTTP egress wrapper + R-NO-DIRECT-PROVIDER-HTTP lint rule + envelope-schema sub-tag extensions)
filed: 2026-05-16
operator: Josh Inklovich
status: LOCKED 2026-05-16T08:00:00Z. Compound paired-commit with §4 v2.x.5 amendment per §6.17 Option-B. Mirrors §0.5 v16 paired-commit precedent for §4 v2.x.1 (lock_history rows 198/199, 2026-05-10) + §0.5 v23 precedent for §4 v2.x.3 (lock_history rows 219/220, 2026-05-15). L-005 strict two-cycle CLOSED with FULL live cross-family rigor — audit trail at `pipeline/validation/cc007_thesis_2026-05-16/`.
parent_locks:
  - pipeline/blueprint/v0.1/section_00_5_interface_index_locked.md                                  # §0.5 v5 LOCKED 2026-04-19 — 101 master rows
  - pipeline/blueprint/v0.1/section_00_5_section_06_operating_envelope_amendment.md                 # §0.5 v6 LOCKED 2026-04-21 — rows 102-117
  - pipeline/blueprint/v0.1/section_00_5_section_07_scribe_amendment.md                             # §0.5 v7 LOCKED 2026-04-21 — rows 118-158
  - pipeline/blueprint/v0.1/section_00_5_section_10_red_team_amendment.md                           # §0.5 v8 LOCKED 2026-05-02 — rows 159-211
  - pipeline/blueprint/v0.1/section_00_5_section_12_uploader_amendment.md                           # §0.5 v9 LOCKED 2026-05-10 — rows 212-232
  - pipeline/blueprint/v0.1/section_00_5_section_11_intake_amendment.md                             # §0.5 v10 LOCKED 2026-05-10 — rows 233-256
  - pipeline/blueprint/v0.1/section_00_5_section_02_v7_2_operational_amendment.md                   # §0.5 v11 LOCKED 2026-05-10 — rows 257-278
  - pipeline/blueprint/v0.1/section_00_5_section_05_v8_amendment.md                                 # §0.5 v12 LOCKED 2026-05-10 — rows 279-290
  - pipeline/blueprint/v0.1/section_00_5_section_15_archivist_amendment.md                          # §0.5 v13 LOCKED 2026-05-10 — rows 291-304
  - pipeline/blueprint/v0.1/section_00_5_section_04_v2_x_amendment.md                               # §0.5 v14 LOCKED 2026-05-10 — rows 305-348
  - pipeline/blueprint/v0.1/section_00_5_section_13_data_collector_amendment.md                     # §0.5 v15 LOCKED 2026-05-10 — rows 349-376
  - pipeline/blueprint/v0.1/section_00_5_section_04_v2_x_1_amendment.md                             # §0.5 v16 LOCKED 2026-05-10 — rows 377-378 — narrow-corrective + sub-tag-extension precedent
  - pipeline/blueprint/v0.1/section_00_5_section_14_report_generator_amendment.md                   # §0.5 v17 LOCKED 2026-05-10 — rows 379-395
  - pipeline/blueprint/v0.1/section_00_5_section_15_reflection_amendment.md                         # §0.5 v18 LOCKED 2026-05-10 — rows 396-413
  - pipeline/blueprint/v0.1/section_00_5_section_17_wpfa_amendment.md                               # §0.5 v19 LOCKED 2026-05-11 — rows 414-445; `ast-lint` vocabulary kind landed
  - pipeline/blueprint/v0.1/section_00_5_section_11_v1_1_amendment.md                               # §0.5 v19 paired-commit 2026-05-11 (narrow-corrective; rows 414-415)
  - pipeline/blueprint/v0.1/section_00_5_section_funding_goal_amendment.md                          # §0.5 v20 LOCKED 2026-05-11 — rows 446-470; `seat_owner` row attribute extension landed (RT-19 closure)
  - pipeline/blueprint/v0.1/section_00_5_v7_0_10_amendment.md                                       # §0.5 v21 LOCKED 2026-05-15 — rows 506-509 (v7.0.10 four F-CLASS-* + sub-tag extensions on F-CLASS-REGISTER-*)
  - pipeline/blueprint/v0.1/section_00_5_section_16_packet_amendment.md                             # §0.5 v22 LOCKED 2026-05-15 — rows 471-505 (Reflection Packet compound triple)
  - pipeline/blueprint/v0.1/section_00_5_section_04_v2_x_3_amendment.md                             # §0.5 v23 LOCKED 2026-05-15 — F-REPORT-* registration (rows 219/220 lock_history)
  - pipeline/blueprint/v0.1/section_00_5_section_16_v1_1_amendment.md                               # §0.5 v24 LOCKED 2026-05-15 — Reflection Packet v0.2 first wave
  - pipeline/blueprint/v0.1/section_00_5_section_18_cards_wave_1_paired_commit_amendment.md         # §0.5 v25 LOCKED 2026-05-15 — Cards Wave 1; `card` vocabulary kind landed
  - pipeline/blueprint/v0.1/section_00_5_section_18_v1_1_amendment.md                               # §0.5 v26 LOCKED 2026-05-16 — §18 v1.1 paired-commit
  - pipeline/blueprint/v0.1/section_04_v2_x_5_provider_boundary_amendment.md                        # §4 v2.x.5 SCOPING DRAFT 2026-05-16 (LOCKs atomically with this amendment)
companion_blueprint_amendment: pipeline/blueprint/v0.1/section_04_v2_x_5_provider_boundary_amendment.md  # paired-commit at §4 v2.x.5 LOCK per §6.17 Option-B
compound_lock_with: section_04_v2_x_5_provider_boundary_amendment.md
parent_wins_discipline: each row's parent_lock_version + parent_lock_commit_hash point at §4 v2.x.5; resolves to actual commit hash at LOCK ceremony.
row_delta: prior runtime-live total at §0.5 v26 LOCK = 538 rows (after §18 v1.1 paired-commit at row 538). **§4 v2.x.5 amendment claims rows 539-548 (10 rows: 1 routing-module + 5 failure-code sub-tag-extension records + 1 ast-lint rule + 3 subprocess-envelope-schema sub-tag-extension records).** Cycle 1 fold-in registered 3 sub-tag-extension records; Cycle 2 fold-in added 2 more (`.signed_file_invalid` on F-CLASS-REGISTER-SIGNATURE-INVALID + `.cedar_load_failure` on F-CLASS-CLOUD-RECEIVED-CONFIDENTIAL). Existing F-CLASS-ROUTING-INDETERMINATE row (§0.5 v14 row 305) + F-CLASS-CLOUD-RECEIVED-CONFIDENTIAL row (§0.5 v14 row 306) + F-CLASS-REGISTER-SIGNATURE-INVALID row (§0.5 v14 row 307) — sub-tag extensions recorded under existing-row ownership; no new top-level failure-code rows. New runtime-live total at this LOCK = 548.
kind_of_amendment: row-append (1 routing-module + 1 ast-lint + 3 subprocess-envelope-schema sub-tag-extension records) + sub-tag-extension recording (3 records under existing F-CLASS-* row ownership). NO new vocabulary kind — every row's `primitive_kind` resolves against the v5 + v6 + v19 + v25 closed vocabulary (marker / schema / interface-contract / failure-code / ast-lint / card / routing_module / subprocess_envelope_schema).
seat_owner_attribute: each row carries seat_owner per RT-19 extension (landed at §0.5 v20 FG amendment).
cross_family_posture: LIVE FULL CROSS-FAMILY (no Section E carve-out) per WS-D v7.0.5 LOCK precedent (lock_history row 179, 2026-05-10). SEVENTEENTH substantive v0.1+v0.2 round to LOCK at this rigor level — after WS-D + WS-F + WS-E + WS-H + WS-G + WS-K + WS-C-M1 + WS-L + WS-I + §4 v2.x.1 + §14 v1 / §0.5 v17 + WS-Reflection / §15 v1 reflection / §0.5 v18 + §4 v2.x.2 + §11 v1.1 + §17 v1 / §0.5 v19 + Funding Goal v0.2 SPEC / §0.5 v20 + §16 v1 / §0.5 v22 + §4 v2.x.3 / §0.5 v23 + Reflection Packet v0.2 first wave / §0.5 v24 + Wave 1 / §0.5 v25 + §18 v1.1 / §0.5 v26 precedents.
narrow_corrective_precedent: §4 v2.x.1 + §0.5 v16 paired-commit (lock_history rows 198/199, 2026-05-10) — same pattern (narrow-corrective amendment with one new dedicated AST-lint module + sub-tag-extension records under existing failure-code-row ownership; parent §4 v2.x text not modified in place).
---

# Amendment intent

This amendment lands paired with §4 v2.x.5 LOCK per §6.17 Option-B compound-commit pattern. §4 v2.x.5 closes CC-007 — seat-local provider HTTP egress sovereignty bypass — by landing `pipeline/orchestrator/provider_boundary.py::enforce_outbound_boundary`, registering three sub-tag extensions on existing F-CLASS-* primitives, registering AST-lint rule R-NO-DIRECT-PROVIDER-HTTP, and extending three seat envelope schemas with `classification_context_json` + `posture` fields.

The amendment mirrors the §4 v2.x.1 + §0.5 v16 paired-commit precedent (lock_history rows 198/199): the parent §4 v2.x LOCK (row 193) is NOT modified in place; the corrective extension lands as the authoritative source for the wrapper-injection mechanism.

This §0.5 paired-commit registers:

1. **Row 539** — `pipeline/orchestrator/provider_boundary.py` routing-module anchor.
2. **Row 540** — sub-tag extension record on F-CLASS-ROUTING-INDETERMINATE: `.outbound_boundary_missing_context` (PRE; structural).
3. **Row 541** — sub-tag extension record on F-CLASS-CLOUD-RECEIVED-CONFIDENTIAL: `.outbound_boundary_classification_deny` (PRE).
4. **Row 542** — sub-tag extension record on F-CLASS-CLOUD-RECEIVED-CONFIDENTIAL: `.outbound_boundary_post_drift` (POST).
5. **Row 543** — `R-NO-DIRECT-PROVIDER-HTTP` AST-lint rule.
6. **Row 544** — sub-tag extension record on subprocess-envelope-schema for `ScribeEnvelope` (classification_context_json + posture fields).
7. **Row 545** — sub-tag extension record on subprocess-envelope-schema for `JudgeEnvelope`.
8. **Row 546** — sub-tag extension record on subprocess-envelope-schema for `RedTeamEnvelope`.

NO new vocabulary kinds. NO new top-level failure-code rows. F-CLASS-* family roster count stays at 16.

# Amendment §A — row append (rows 539-546)

All rows enter §0.5 at `stability_tier = "STABLE"` at compound v2.x.5 LOCK (the §4 v2.x.5 LOCK is the parent; no PARENT_UNLOCKED transit since the compound paired-commit lands at the same `lock_timestamp_utc`).

## §A.1 Row 539 — routing-module anchor for `pipeline/orchestrator/provider_boundary.py`

| Row | primitive_id | defined_at | parent_lock_version | kind | seat_owner | stability_tier |
|---|---|---|---|---|---|---|
| 539 | `orchestrator.routing_module.provider_boundary.v1` | `pipeline/orchestrator/provider_boundary.py` (NEW at §4 v2.x.5 LOCK) | §4 v2.x.5 | routing_module | orchestrator | STABLE |

Module surface: `enforce_outbound_boundary` + `stdlib_urlopen_caller` + `OutboundCallable` Protocol + `ClassificationContext` mirror + `OutboundBoundaryRefusedError` typed exception + three sub-tag string constants. Per §4 v2.x.5 §1 + §4 v2.x.5 §4.

The `routing_module` primitive_kind is the existing closed-set kind shared with `pipeline/orchestrator/router.py` (§0.5 v5 master rows). No new primitive_kind extension.

## §A.2 Rows 540-542 — failure-code sub-tag extension records

Per §4 v2.x.1 row 198 precedent: sub-tag extensions land as discrete §0.5 records under the existing failure-code-row ownership; they do NOT create new top-level rows. The sub-tag record is itself a §0.5 entry of `primitive_kind: failure-code` whose `parent_primitive_id` field names the owning top-level row.

| Row | primitive_id | defined_at | parent_primitive_id | parent_row | parent_lock_version | kind | seat_owner | stability_tier |
|---|---|---|---|---|---|---|---|---|
| 540 | `logician.failure_code.F-CLASS-ROUTING-INDETERMINATE.outbound_boundary_missing_context.v1` | `section_04_v2_x_5_provider_boundary_amendment.md#§2 + §4.5` + `pipeline/orchestrator/provider_boundary.py` | `logician.failure_code.F-CLASS-ROUTING-INDETERMINATE.v1` | 305 (§0.5 v14) | §4 v2.x.5 | failure-code | f_class | STABLE |
| 541 | `logician.failure_code.F-CLASS-CLOUD-RECEIVED-CONFIDENTIAL.outbound_boundary_classification_deny.v1` | `section_04_v2_x_5_provider_boundary_amendment.md#§2 + §4.5` + `pipeline/orchestrator/provider_boundary.py` | `logician.failure_code.F-CLASS-CLOUD-RECEIVED-CONFIDENTIAL.v1` | 306 (§0.5 v14) | §4 v2.x.5 | failure-code | f_class | STABLE |
| 542 | `logician.failure_code.F-CLASS-CLOUD-RECEIVED-CONFIDENTIAL.outbound_boundary_post_drift.v1` | `section_04_v2_x_5_provider_boundary_amendment.md#§2 + §4.5` + `pipeline/orchestrator/provider_boundary.py` | `logician.failure_code.F-CLASS-CLOUD-RECEIVED-CONFIDENTIAL.v1` | 306 (§0.5 v14) | §4 v2.x.5 | failure-code | f_class | STABLE |
| 547 | `logician.failure_code.F-CLASS-REGISTER-SIGNATURE-INVALID.signed_file_invalid.v1` (Cycle 2 fold-in RT-C2-01) | `section_04_v2_x_5_provider_boundary_amendment.md#§12.3` + `pipeline/vault/classification/signed_register_loader.py` | `logician.failure_code.F-CLASS-REGISTER-SIGNATURE-INVALID.v1` | 307 (§0.5 v14) | §4 v2.x.5 | failure-code | f_class | STABLE |
| 548 | `logician.failure_code.F-CLASS-CLOUD-RECEIVED-CONFIDENTIAL.cedar_load_failure.v1` (Cycle 2 fold-in RT-C2-04) | `section_04_v2_x_5_provider_boundary_amendment.md#§12.6` + `pipeline/logician/cedar_engine.py` | `logician.failure_code.F-CLASS-CLOUD-RECEIVED-CONFIDENTIAL.v1` | 306 (§0.5 v14) | §4 v2.x.5 | failure-code | f_class | STABLE |

**Disposition per row:**

- **Row 540 `.outbound_boundary_missing_context`** — PRE per-call sub-tag. Fires when `enforce_outbound_boundary` is invoked with `classification_context=None` AND posture ≠ local_only_sovereign. HARD_BLOCK; NO M13 bypass (structural — even M13 cannot retroactively produce classification proof). Drift-test: `tests/orchestrator/test_provider_boundary.py::test_outbound_boundary_missing_context_fails_closed`.
- **Row 541 `.outbound_boundary_classification_deny`** — PRE per-call sub-tag. Fires when (a) posture == local_only_sovereign (structural refusal), or (b) any input has class_name ∈ {confidential, operator_flagged}. P0 / M13 audited admin-risk HIGH on the input-class branch; HARD_BLOCK NO M13 on the local-only branch. Drift-test: `tests/orchestrator/test_provider_boundary.py::test_outbound_boundary_classification_deny_local_only_fails_closed` + `::test_outbound_boundary_classification_deny_confidential_input_fails_closed`.
- **Row 542 `.outbound_boundary_post_drift`** — POST per-call sub-tag. Fires when the response payload from the wrapped HTTP egress contains a classified-value literal that did not appear in the request payload (post-egress classification leak). P0 / M13 audited. Drift-test: `tests/orchestrator/test_provider_boundary.py::test_outbound_boundary_post_drift_classification_hit_fails_closed`.

**Family roster impact:** F-CLASS-* family count remains 16 top-level primitives. The sub-tag extensions are recorded as `parent_primitive_id`-bound child rows, NOT new top-level entries. F-CLASS-COVERAGE-INCOMPLETE META-gate scope is unchanged.

## §A.3 Row 543 — `R-NO-DIRECT-PROVIDER-HTTP` AST-lint rule

| Row | primitive_id | defined_at | parent_lock_version | kind | seat_owner | stability_tier |
|---|---|---|---|---|---|---|
| 543 | `linting.ast_lint.R-NO-DIRECT-PROVIDER-HTTP.v1` | `pipeline/linting/r_no_direct_provider_http.py` (NEW) | §4 v2.x.5 | ast-lint | orchestrator | STABLE |

Rule scope: `pipeline/**/*.py` MINUS `ALLOWLISTED_FILES` frozenset (`{pipeline/orchestrator/provider_boundary.py, pipeline/orchestrator/router.py}`) MINUS `pipeline/validation/**/*.py` grandfathered glob (OD-4).

Sub-tags (5 per §4 v2.x.5 §3.2): `.urlopen` / `.requests_lib` / `.httpx_lib` / `.aiohttp` / `.raw_socket`.

`FORBIDDEN_PRIMITIVES` table covers 25 concrete `(module, attr)` call shapes. `MappingProxyType`-wrapped per RT-14 precedent (§4 v2.x.1 row 198 RT-14 closure).

Registered into `pipeline.linting.ast_lint.DEFAULT_RULES` via the `_section_04_v2_x_5_rules()` lazy-import block (mirrors `_section_04_v2_x_1_rules()` discipline).

## §A.4 Rows 544-546 — subprocess-envelope-schema sub-tag extension records

The three seat envelope schemas extend with `classification_context_json: str` + `posture: Literal[...]` fields per §4 v2.x.5 §4. The extensions are recorded as `subprocess_envelope_schema`-kind sub-tag records under each existing envelope-row ownership.

| Row | primitive_id | defined_at | parent_primitive_id | parent_lock_version | kind | seat_owner | stability_tier |
|---|---|---|---|---|---|---|---|
| 544 | `seats.scribe.envelope_schema.classification_context_extension.v1` | `pipeline/seats/scribe/seat.py` (UPDATED) + `section_04_v2_x_5_provider_boundary_amendment.md#§4.1` | `seats.scribe.envelope_schema.ScribeEnvelope.v1` (existing per §0.5 v7) | §4 v2.x.5 | subprocess_envelope_schema | scribe | STABLE |
| 545 | `seats.judge.envelope_schema.classification_context_extension.v1` | `pipeline/seats/judge/seat.py` (UPDATED) + `section_04_v2_x_5_provider_boundary_amendment.md#§4.2` | `seats.judge.envelope_schema.JudgeEnvelope.v1` (existing per §0.5 v?) | §4 v2.x.5 | subprocess_envelope_schema | judge | STABLE |
| 546 | `seats.red_team.envelope_schema.classification_context_extension.v1` | `pipeline/seats/red_team/seat.py` (UPDATED) + `section_04_v2_x_5_provider_boundary_amendment.md#§4.3` | `seats.red_team.envelope_schema.RedTeamEnvelope.v1` (existing per §0.5 v8) | §4 v2.x.5 | subprocess_envelope_schema | red_team | STABLE |

Each row adds two fields to its owning envelope schema:

- `classification_context_json: str` — canonical-JSON-encoded `ClassificationContext` per §4 v2.x.5 §4.4 schema.
- `posture: Literal["frontier_eligible", "split_context_hybrid", "local_only_sovereign"]` — deployment posture per architecture v7.0.10 §1.

Existing `F-{SCRIBE,JUDGE,RT}-ENVELOPE-MALFORMED` predicates extend to require both new fields non-empty + well-formed. The extension is in-place; no new top-level F-* row.

**Runtime-live total at this LOCK: 548 rows** (538 + 10 new rows = 548; +2 from Cycle 2 fold-in for signed_file_invalid + cedar_load_failure sub-tag-extension records on existing F-CLASS-REGISTER-SIGNATURE-INVALID + F-CLASS-CLOUD-RECEIVED-CONFIDENTIAL row ownership).

# Amendment §B — F-CIC-CLC-COUPLING-VIOLATION-class regression scope

F-CIC-CLC-COUPLING-VIOLATION-class regression test runs at v2.x.5 paired-commit per Path B naming reconciliation:

- F-CLASS-* codes (rows 305-348 + sub-tag-extension rows 506-509 from v7.0.10 + this amendment's three sub-tag-extension records on existing rows 305-306) belong only to architecture-layer classification routing (seat_owner: "f_class").
- F-WPFA-* codes belong only to §17 WPFA.
- F-REFLECTION-* codes belong only to §15 Archivist sub-mode.
- F-ARCHIVIST-* codes belong only to §15 Archivist proper.
- F-FG-* codes belong only to §2 v7.5 FG.
- F-REPORT-* codes belong only to §14 Report Generator.
- F-PACKET-* codes belong only to §16 Reflection Packet.
- F-DATACOLLECTOR-* codes belong only to §13 Data Collector.
- F-CARDS-* codes belong only to §18 Card System.

No cross-family coupling introduced at this amendment. The sub-tag extensions stay within F-CLASS-* family ownership.

# Amendment §C — AST-lint binding

R-NO-DIRECT-PROVIDER-HTTP (row 543) registers into `pipeline.linting.ast_lint.DEFAULT_RULES` via lazy-import block `_section_04_v2_x_5_rules()` mirroring the §4 v2.x.1 `_section_04_v2_x_1_rules()` discipline. The lazy import avoids the circular-import surface that fires when `ast_lint` is invoked as `python -m pipeline.linting.ast_lint`.

# Amendment §D — `R-CLASS-POSTURE-FIELD-COVERAGE` cross-rule

The existing R-CLASS-POSTURE-FIELD-COVERAGE rule (registered at v7.0.10 paired-commit / §0.5 v21) extends its scope to verify that the three seat envelope schemas inspect the `posture` field at the F-{SCRIBE,JUDGE,RT}-ENVELOPE-MALFORMED predicate. The scope extension is recorded inline in the existing R-CLASS-POSTURE-FIELD-COVERAGE row (no new top-level row); the predicate body extends in `pipeline/linting/r_class_posture_field_coverage.py` at LOCK.

# Amendment §E — F-INDEX-STALE PRE-gate clearance

F-INDEX-STALE PRE-gate clears at compound commit:

1. seat_owner consistency: all 8 new rows carry valid seat_owner per RT-19 invariant.
2. immutable_kind enforcement: routing_module + ast-lint + subprocess_envelope_schema rows carry `immutable_kind: true` per row 507 RT-C2-04 precedent; failure-code sub-tag-extension records inherit immutable_kind from their parent rows.
3. F-CIC-CLC-COUPLING-VIOLATION regression test PASS (no CIC/CLC coupling field appears in any new row).
4. Path B naming reconciliation PASS (F-CLASS-* sub-tag extensions stay within F-CLASS-* family ownership; no cross-family F-* code introduced).
5. R-CLASS-POSTURE-FIELD-COVERAGE scope-extension PASS at compound commit (companion edit in `r_class_posture_field_coverage.py` lands at the same commit).

# Amendment §F — Compound lock_history rows

Two lock_history rows append at LOCK ceremony per §6.17 Option-B paired-commit pattern:

- **Row N (§4 v2.x.5):** `lock_class: blueprint`, `lock_kind: compound-paired-commit-double-member-1`.
- **Row N+1 (§0.5 v27 — this amendment):** `lock_class: blueprint-interface-index`, `lock_kind: compound-paired-commit-double-member-2`, `parent_lock_row: <N>`.

Single `lock_timestamp_utc` across the compound transaction.
