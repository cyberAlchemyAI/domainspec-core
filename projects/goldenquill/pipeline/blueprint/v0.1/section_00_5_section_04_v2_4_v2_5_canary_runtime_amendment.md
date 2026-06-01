---
title: §0.5 Blueprint Interface Index — §4 v2.4/v2.5 Canary + Runtime Integrity rows amendment
filed: 2026-05-08
operator: Josh
status: LOCKED 2026-05-08 — paired with §4 v2.4/v2.5 (LOCKED 2026-05-08); 15 rows promoted PARENT_UNLOCKED → STABLE at compound commit. GPP three-tier closure: Tier 1 PASS, Tier 2 live (12 findings, 4 BLOCKING REJECTED with substantive rationale), Tier 3 signed manifest Ed25519+ML-DSA-65-stub valid.
parent_locks:
  - pipeline/blueprint/v0.1/section_00_5_interface_index_locked.md                                       # §0.5 base
  - pipeline/blueprint/v0.1/section_00_5_v5_amendment.md                                                 # §0.5 v5 LOCKED 2026-05-08 (27 GPP rows)
  - pipeline/blueprint/v0.1/section_00_5_section_04_v2_3_privacy_router_amendment.md                     # §0.5 v6 LOCKED 2026-05-08 (4 Privacy Router rows)
  - pipeline/blueprint/v0.1/section_04_v2_4_v2_5_amendment.md                                            # §4 v2.4/v2.5 LOCK-READY since 2026-04-19; this companion lands as paired commit at LOCK
companion_blueprint_amendment: pipeline/blueprint/v0.1/section_04_v2_4_v2_5_amendment.md  (§4.15 Canary + §4.16-§4.17 Runtime Integrity)
kind_of_amendment: pure row-append (15 new rows). NO vocabulary extension — every row's `primitive_kind` resolves against existing §0.5 closed vocabulary (mechanism, pre-gate-check, post-gate-check, failure-code, interface-contract).
row_count: 15
companion_file_pattern: matches §0.5 §6 + §0.5 §7 + §0.5 §10 + §0.5 v6 amendment-companion precedent.
parent_wins_discipline: each row's parent_lock_version + parent_lock_commit_hash fields populated at commit time from §4 v2.4/v2.5's sha3-512 prefix.
f_index_stale_preflight: F-INDEX-STALE PRE-gate fires at commit time; all 15 rows must be present in the index or the commit fails closed.
version_wording_discipline: "LOCKED" refers to on-disk LOCKED state only.
---

# Amendment intent

§4 v2.4/v2.5 introduces the Canary harness (v0.2 target; v0.1 stub) at §4.15 and the Runtime Integrity family at §4.16-§4.17 (key presence, router drift, family collision, rails-report emission). LOCK-READY since 2026-04-19; was blocked on GPP three-tier mechanism which LOCKed 2026-05-08 via v7.0.1. Per §0.5 paired-commit discipline, fifteen primitives introduced by §4 v2.4/v2.5 must land as §0.5 rows in the same commit that LOCKs §4 v2.4/v2.5.

The fifteen rows enumerate: 2 mechanisms (Canary + Runtime Integrity family) + 7 failure codes (3 F-CANARY-* + F-ROUTER-FAMILY-COLLISION + 2 F-RUNTIME-* + F-KEY-PRESENCE-* + F-RAILS-REPORT-EMISSION-FAIL) + 4 PRE-gates + 1 POST-gate + 1 interface-contract.

# §0.5 v7 row table (15 rows)

| Row | Primitive name | Kind | Source section | Parent lock version |
|---|---|---|---|---|
| 1 | `canary_harness_mechanism` | mechanism | §4 v2.4 §4.15 | v2.4 |
| 2 | `runtime_integrity_family_mechanism` | mechanism | §4 v2.5 §4.16-§4.17 | v2.5 |
| 3 | `F-CANARY-STR-REGRESSION` | failure-code | §4 v2.4 §6 | v2.4 |
| 4 | `F-CANARY-SCORE-REGRESSION` | failure-code | §4 v2.4 §6 | v2.4 |
| 5 | `F-CANARY-TEST-VECTORS-MISSING` | failure-code | §4 v2.4 §6 | v2.4 |
| 6 | `F-ROUTER-FAMILY-COLLISION` | failure-code | §4 v2.5 §4.16 (canonical; referenced from §4 v2.4) | v2.5 |
| 7 | `F-RUNTIME-DRIFT-FROM-LOCKED-ROUTER` | failure-code | §4 v2.5 §6 | v2.5 |
| 8 | `F-KEY-PRESENCE-PREFLIGHT-FAIL` | failure-code | §4 v2.5 §6 | v2.5 |
| 9 | `F-RAILS-REPORT-EMISSION-FAIL` | failure-code | §4 v2.5 §6 | v2.5 |
| 10 | `canary_edit_time_replay_gate` | pre-gate-check | §4 v2.4 §4.15 (edit-time) | v2.4 |
| 11 | `router_family_collision_runtime_pregate` | pre-gate-check | §4 v2.5 §4.16 | v2.5 |
| 12 | `key_presence_preflight_pregate` | pre-gate-check | §4 v2.5 Row 22 | v2.5 |
| 13 | `drift_from_locked_router_pregate` | pre-gate-check | §4 v2.5 Row 23 | v2.5 |
| 14 | `rails_report_emission_postgate` | post-gate-check | §4 v2.5 §4.17 | v2.5 |
| 15 | `locked_test_vector_corpus_interface` | interface-contract | §4a canary harness spec | v2.4 (TO_BE_PINNED_AT_COMMIT — interface artifact pinned at v0.2 canary harness wire-in) |

## Stability tier transitions

All 15 rows promote `PARENT_UNLOCKED` → `STABLE` at compound LOCK with §4 v2.4/v2.5. Row 15 (`locked_test_vector_corpus_interface`) lands as `STABLE` with `TO_BE_PINNED_AT_COMMIT` marker on the interface-artifact-path field — the row is committed; the implementation reference is pinned at v0.2 canary harness wire-in per §4 v2.4 v0.1 stub posture. Per GPP-DET Check 6 (INDEX-STALE-DRYRUN) the marker is acceptable.

## Parent_lock_commit_hash population

At compound LOCK time, all 15 rows' `parent_lock_commit_hash` field is populated with the SHA-3-512 canonical-bytes hash of `section_04_v2_4_v2_5_amendment.md` post-LOCKED-status edit. The paired commit binds §4 v2.4/v2.5 + §0.5 v7 atomically.

# Bundling rationale (carried from parent amendment)

§4 v2.4/v2.5 bundles Canary (v0.2 target) with Runtime Integrity (v0.1 target) because `F-ROUTER-FAMILY-COLLISION` is canonically defined at §4.16 (Runtime Integrity) and referenced from §4.15 (Canary). Splitting the amendments would create a partial-commit window where §4 v2.4 references a failure code whose canonical definition has not yet landed. The bundling is the L-005-cleared and operator-approved scope decision; reviewer recommendations to split (carried forward from v7.0.1 + v2.3 LOCK rounds) are dispositioned at this LOCK round's Tier 3 with rationale.

# Non-goals for this amendment

- Does not modify any existing §0.5 row.
- Does not introduce a new primitive kind. All 15 rows use existing kinds: mechanism, pre-gate-check, post-gate-check, failure-code, interface-contract.
- Does not pin the canary harness implementation — that ships at v0.2 per §4 v2.4 stub posture.
- Does not pre-empt v7.1 architecture amendment (Section addition naming Privacy Router as v7-amendment-class mechanism + F-ROUTER-FAMILY-COLLISION architecture-tier registration). Architecture-tier registration of F-ROUTER-FAMILY-COLLISION is deferred to v7.1; this LOCK pins the failure code as a §0.5 + §4 blueprint-tier primitive.

# Paired-commit reminder

This §0.5 v7 amendment LOCKs atomically with `pipeline/blueprint/v0.1/section_04_v2_4_v2_5_amendment.md`. F-INDEX-STALE PRE-gate fails-closed if the 15 rows are not in the index at the moment of compound commit.

# GPP three-tier expectations (2026-05-08 LOCK)

The compound LOCK runs through the GPP three-tier mechanism:

- **Tier 1 GPP-DET** — already PASS (`gpp_det_report_2026-05-08.md`); plan_sub_docs scope unchanged.
- **Tier 2 GPP-COUNCIL** — fresh live dispatch on §4 v2.4/v2.5 + this §0.5 v7 companion. Bundling concerns from prior rounds (RT-F005 v7.0.1 + RT-F004 v2.3 + GGRR-006 v7.0.1 + GGRR-004 v2.3) carried forward for §4 v2.4/v2.5-context disposition; expected resolution: REJECTED with rationale (F-ROUTER-FAMILY-COLLISION shared canonical definition + L-005 PASS preserved bundling).
- **Tier 3 GPP-SYNTHESIS** — operator dispositions + signed manifest. Ephemeral keypair (B1 not yet LOCKed).

# Thesis round expectations (already cleared 2026-04-19)

§4 v2.4/v2.5 cleared L-005 two-audit on 2026-04-19; this §0.5 v7 amendment is additive row-append against that cleared scope. No new Thesis round required — GPP three-tier substitutes per §0.5 paired-commit discipline.

# End of amendment
