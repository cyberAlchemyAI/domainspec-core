---
title: Blueprint §0.5 Interface Index — Amendment v5 (27 paired-commit rows for GPP — Thesis-round F-2 decision)
filed: 2026-04-19
operator: Josh
amendment_status: LOCKED 2026-05-08 — paired with architecture v7.0.1 + §4 v2.1.1. GPP three-tier closure: Tier 1 PASS (gpp_det_report_2026-05-08), Tier 2 live dispatch (council_findings_2026-05-08), Tier 3 signed manifest (gpp_manifest_2026-05-08). 27 §0.5 rows promoted PARENT_UNLOCKED → STABLE in this commit (Thesis-round 2026-04-19 F-2 decision honored).
parent_lock: pipeline/blueprint/v0.1/section_00_5_interface_index_locked.md  (§0.5 v4 LOCKED 2026-04-19)
supersedes_relationship: inserts v5 as a paired commit alongside architecture v7.0.1 and blueprint §4 v2.1.1. Adds 27 rows (Thesis-round 2026-04-19 F-2 decision: commit 27, matching amendment enumeration; spec §6.4 updated 26 → 27 in paired commit). No existing v4 rows are modified.
companion_architecture_amendment: pipeline/architecture/v0.1/architecture_v7_0_1_amendment.md  (Section E.P)
companion_blueprint_amendment: pipeline/blueprint/v0.1/section_04_v2_1_1_amendment.md  (§4.14a)
scope_source: pipeline/validation/integration_scope_close_2026-04-19/gpp/gpp_spec_v1.md  (§6.4 enumerates 26 rows)
future_lock_citations:
  - pipeline/architecture/v0.1/architecture_v7_0_1_amendment.md  # paired
  - pipeline/blueprint/v0.1/section_04_v2_1_1_amendment.md        # paired
parent_wins_discipline: each row's parent_lock_version and parent_lock_commit_hash fields point to the specific section that defines it. Rows 1, 26, 27 point at v7.0.1 architecture (Section E.P). Rows 2-25 point at §4 v2.1.1 blueprint.
row_count: 27
f_index_stale_preflight: F-INDEX-STALE PRE-gate fires at commit time; all 27 rows must be present in the index or the commit fails closed.
version_wording_discipline: "LOCKED" refers to on-disk LOCKED state only; target-LOCK wording for forward-looking items.
---

# Amendment intent

§0.5 discipline is parent-wins paired-commit: every load-bearing primitive introduced by an architecture or blueprint section must land as a §0.5 row in the same commit. This amendment pins 27 rows that the paired commit of architecture v7.0.1 (Section E.P) + blueprint §4 v2.1.1 (§4.14a) must carry atomically.

The 27 rows enumerate: the GPP architecture mechanism (1), pipeline-start PRE-gate rows for each GPP-DET check (10), the dispatch and synthesis-tier rows (2 — dispatch-time PRE-gate + synthesis-time POST-gate), the failure-code family (12), the manifest schema (1), and the council-dispatch interface contract (1). Total: 1 + 10 + 2 + 12 + 1 + 1 = 27. This count supersedes an earlier 26-count in `gpp_spec_v1.md` §6.4; the 26-count folded `gpp_council_dispatch_contract` into the mechanism row's description at a cost of primitive-kind purity. **Thesis-round 2026-04-19 F-2 decision: commit 27 rows (primitive-kind purity preferred); amend spec §6.4 26 → 27 in the same paired commit.**

# Proposed 26 new §0.5 rows

Each row has the §0.5 v4 schema: primitive_id, defined_at (file path + section anchor), parent_lock_version, parent_lock_commit_hash (`TO_BE_PINNED_AT_COMMIT`), primitive_kind, description, introduced_in_index_version (`v5`), stability_tier.

## Group A — Architecture mechanism (1 row)

| # | primitive_id | defined_at | parent_lock | kind | stability |
|---|---|---|---|---|---|
| 1 | `governance_plan_preflight_mechanism` | `pipeline/architecture/v0.1/tilth_architecture_locked.md` Section E.P | v7.0.1 | architecture-mechanism | Tier 1 (stable) |

Description: The three-tier GPP mechanism family (DET + COUNCIL + SYNTHESIS) as defined in architecture v7.0.1 Section E.P. Tier 1 deterministic + Tier 2 bounded-council + Tier 3 operator-signed manifest.

## Group B — Pipeline-start PRE-gate-check rows (10 rows, one per GPP-DET check)

| # | primitive_id | defined_at | parent_lock | kind | stability |
|---|---|---|---|---|---|
| 2 | `gpp_det_cite_resolve_pregate` | §4.14a + §4.2.1 row | §4 v2.1.1 | pre-gate-check | Tier 1 |
| 3 | `gpp_det_version_resolve_pregate` | §4.14a + §4.2.1 row | §4 v2.1.1 | pre-gate-check | Tier 1 |
| 4 | `gpp_det_xdoc_ref_pregate` | §4.14a + §4.2.1 row | §4 v2.1.1 | pre-gate-check | Tier 1 |
| 5 | `gpp_det_row_count_arithmetic_pregate` | §4.14a + §4.2.1 row | §4 v2.1.1 | pre-gate-check | Tier 1 |
| 6 | `gpp_det_hash_pin_pregate` | §4.14a + §4.2.1 row | §4 v2.1.1 | pre-gate-check | Tier 1 |
| 7 | `gpp_det_index_stale_dryrun_pregate` | §4.14a + §4.2.1 row | §4 v2.1.1 | pre-gate-check | Tier 1 |
| 8 | `gpp_det_family_taxonomy_pregate` | §4.14a + §4.2.1 row | §4 v2.1.1 | pre-gate-check | Tier 1 |
| 9 | `gpp_det_scope_freeze_backdoor_flag_pregate` | §4.14a + §4.2.1 row | §4 v2.1.1 | pre-gate-check | Tier 1 (flag semantics) |
| 10 | `gpp_det_version_skew_disclosure_pregate` | §4.14a + §4.2.1 row | §4 v2.1.1 | pre-gate-check | Tier 1 |
| 11 | `gpp_det_blocker_carry_check_pregate` | §4.14a + §4.2.1 row | §4 v2.1.1 | pre-gate-check | Tier 1 |

## Group C — Dispatch + synthesis tier rows (2 rows)

| # | primitive_id | defined_at | parent_lock | kind | stability |
|---|---|---|---|---|---|
| 12 | `gpp_manifest_present_at_dispatch_pregate` | §4.14a + §4.2.1 row | §4 v2.1.1 | pre-gate-check | Tier 1 (dispatch-time) |
| 13 | `gpp_finding_disposition_complete_postgate` | §4.14a + §4.2.1 table | §4 v2.1.1 | post-gate-check | Tier 1 (synthesis-time) |

## Group D — Failure-code family (12 rows)

| # | primitive_id | defined_at | parent_lock | kind | stability |
|---|---|---|---|---|---|
| 14 | `F-GPP-CITATION-UNRESOLVED` | §4 v2.1.1 §6 + architecture v7.0.1 E.P.5 | v7.0.1 / §4 v2.1.1 | failure-code | Tier 1 |
| 15 | `F-GPP-VERSION-UNRESOLVED` | §4 v2.1.1 §6 + architecture v7.0.1 E.P.5 | v7.0.1 / §4 v2.1.1 | failure-code | Tier 1 |
| 16 | `F-GPP-CROSSDOC-BROKEN` | §4 v2.1.1 §6 + architecture v7.0.1 E.P.5 | v7.0.1 / §4 v2.1.1 | failure-code | Tier 1 |
| 17 | `F-GPP-ROW-COUNT-MISMATCH` | §4 v2.1.1 §6 + architecture v7.0.1 E.P.5 | v7.0.1 / §4 v2.1.1 | failure-code | Tier 1 |
| 18 | `F-GPP-CANONICAL-HASH-MISMATCH` | §4 v2.1.1 §6 + architecture v7.0.1 E.P.5 | v7.0.1 / §4 v2.1.1 | failure-code | Tier 1 |
| 19 | `F-GPP-INDEX-STALE-ON-PROPOSED-ROWS` | §4 v2.1.1 §6 + architecture v7.0.1 E.P.5 | v7.0.1 / §4 v2.1.1 | failure-code | Tier 1 |
| 20 | `F-GPP-FAMILY-TAXONOMY-MISMATCH` | §4 v2.1.1 §6 + architecture v7.0.1 E.P.5 | v7.0.1 / §4 v2.1.1 | failure-code | Tier 1 |
| 21 | `F-GPP-SCOPE-FREEZE-BACKDOOR-UNREVIEWED` | §4 v2.1.1 §6 + architecture v7.0.1 E.P.5 | v7.0.1 / §4 v2.1.1 | failure-code | Tier 1 |
| 22 | `F-GPP-VERSION-SKEW-UNDISCLOSED` | §4 v2.1.1 §6 + architecture v7.0.1 E.P.5 | v7.0.1 / §4 v2.1.1 | failure-code | Tier 1 |
| 23 | `F-GPP-BLOCKER-UNCARRIED` | §4 v2.1.1 §6 + architecture v7.0.1 E.P.5 | v7.0.1 / §4 v2.1.1 | failure-code | Tier 1 |
| 24 | `F-GPP-MANIFEST-MISSING` | §4 v2.1.1 §6 + architecture v7.0.1 E.P.5 | v7.0.1 / §4 v2.1.1 | failure-code | Tier 1 |
| 25 | `F-GPP-FINDING-UNDISPOSED` | §4 v2.1.1 §6 + architecture v7.0.1 E.P.5 | v7.0.1 / §4 v2.1.1 | failure-code | Tier 1 |

## Group E — Schema + interface contract (2 rows)

| # | primitive_id | defined_at | parent_lock | kind | stability |
|---|---|---|---|---|---|
| 26 | `gpp_manifest_schema_v1` | architecture v7.0.1 E.P.4 + `gpp_spec_v1.md` §3 Tier 3 | v7.0.1 | schema | Tier 1 |
| 27 | `gpp_council_dispatch_contract_v1` | architecture v7.0.1 E.P.2 + `gpp_spec_v1.md` §3 Tier 2 | v7.0.1 | interface-contract | Tier 1 |

# Row-count reconciliation (Thesis-round 2026-04-19 F-2 decision — RESOLVED)

Groups tally: A(1) + B(10) + C(2) + D(12) + E(2) = **27 rows.**

`gpp_spec_v1.md` §6.4 originally listed a 26-count. Two reconciliation paths were available:
- **Path (a):** commit 26 rows; fold `gpp_council_dispatch_contract_v1` into row 1's description (mechanism row absorbs the interface-contract).
- **Path (b):** commit 27 rows; amend spec §6.4 from 26 → 27 in the same paired commit.

**Thesis-round 2026-04-19 synthesis decision (F-2): Path (b).** Rationale:
1. Primitive-kind purity — `architecture-mechanism` and `interface-contract` are distinct §0.5 kinds; folding them into a single row muddies row 1's `kind` field and makes downstream consumers (e.g., `gpp_council_dispatch.py` discovery) harder to write cleanly.
2. The kind-splitting pattern matches how §0.5 v4 handles schemas + interface-contracts elsewhere.
3. Spec §6.4 is updated in the same paired commit (26 → 27); no permanent cross-document inconsistency.

Defender of Path (a) rejected at Tier 2 with rationale: "interface-contract is a sufficiently distinct primitive kind that consumers will need to discover it independently; folding it into mechanism row trades clarity for a one-row cost."

The F-INDEX-STALE PRE-gate checks that the declared row count matches the actual row count at commit time — GPP-DET's ROW-COUNT-ARITHMETIC check (Check 4) catches this class of mismatch preflight.

# Parent_lock_commit_hash population

At commit time, each row's `parent_lock_commit_hash` field is populated with the SHA-3-512 canonical-bytes hash of the parent section file at commit. Rows 1, 26, 27 point at architecture v7.0.1 (one hash). Rows 2-25 point at §4 v2.1.1 (one hash). The paired commit bundles both hashes into §0.5 v5.

# §0.5 v5 front-matter updates

- `version` → `v5`
- `parent_relationships` → add `v7.0.1 architecture (Section E.P) + §4 v2.1.1 (§4.14a)` as the parent lock set for the 26 new rows.
- `row_count` → previous v4 count + 27 (exact v4 row count to be confirmed at commit-time read of v4; spec §6.4 canonical count updated to 27 in same paired commit).
- `discipline_version` → unchanged from v4 (parent-wins paired commit).

# Non-goals for this amendment

- Does not modify any v4 row.
- Does not introduce a new primitive kind. All 26 rows use existing kinds: architecture-mechanism, pre-gate-check, post-gate-check, failure-code, schema, interface-contract.
- Does not modify F-INDEX-STALE semantics.
- Does not retroactively tag v4 rows.

# Paired-commit reminder

This §0.5 v5 amendment commits atomically with architecture v7.0.1 and blueprint §4 v2.1.1. F-INDEX-STALE PRE-gate in §0.5 v4 fails-closed if the 26 rows are not in the index at the moment of commit.

# Thesis round expectations

- **Audit pass 1 (Editor + Judge):** Editor audits row-id naming consistency with existing v4 naming conventions, parent_lock_version cross-references, primitive_kind vocabulary fit. Judge scores against §0.5 v4 discipline rubric (parent-wins, same-commit landing, F-INDEX-STALE clean).
- **Audit pass 2 (Red Team + Reasoner):** Red Team adversarial on: does the 26-vs-27 reconciliation hide a missing row? can a row id be conflated with an existing v4 row id? does the parent_lock_commit_hash population have a race between v7.0.1 architecture commit and §4 v2.1.1 blueprint commit (they are paired but are two distinct file edits in the same commit)? Reasoner audits decision journal for: was the "commit 27 + amend spec to 27" path rejected with rationale? was the stability_tier assignment (Tier 1) justified for each row?
- **Synthesis:** operator + Opus 4.7 emits LOCK commit atomically with paired v7.0.1 + §4 v2.1.1.

# End of amendment
