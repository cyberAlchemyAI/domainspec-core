---
title: §4 v2.x.4 — F-FG-* failure-code family registration (compound paired-commit sibling 3/4)
filed: 2026-05-11
operator: Josh Inklovich
status: LOCKED 2026-05-11 — compound paired-commit (sibling 3/4) with §2 v7.5 + §3 v6 + §0.5 v20. L-005 strict two-cycle CLOSED with FULL LIVE CROSS-FAMILY rigor. SPEC-ONLY at v0.2 per §15 v1 precedent — predicate bodies skeleton stubs raise NotImplementedError; v1.x Code-phase realizes LIVE bodies.
parent_locks:
  - pipeline/blueprint/v0.1/section_04_logician.md                                      # §4 v2.x in flight
  - pipeline/blueprint/v0.1/section_04_v2_x_amendment.md                                # §4 v2.x LOCKED 2026-05-10 rows 193/194 — F-CLASS-* dormant primitives
  - pipeline/blueprint/v0.1/section_04_v2_x_1_amendment.md                              # §4 v2.x.1 LOCKED 2026-05-10 row 199 — narrow corrective with R-ARCHIVIST-NO-CANONICAL-MUTATE
  - pipeline/blueprint/v0.1/section_04_logician_v2_x_2_amendment.md                     # §4 v2.x.2 LOCKED 2026-05-10 row 203 — F-REFLECTION-* sub-tag-extension family
  - pipeline/blueprint/v0.1/section_04_v2_x_z_wpfa_amendment.md                         # §4 v2.x.z LOCKED 2026-05-11 row 207 — F-WPFA-* family with LIVE bodies (THE family-prefix-by-section-abbreviation pattern this amendment mirrors per Path B preemptive naming reconciliation)
  - pipeline/blueprint/v0.1/section_15_archivist.md                                     # §15 v1 SPEC LOCKED 2026-05-10 rows 191/192 — THE SPEC-ONLY-AT-v0.2 PRECEDENT this amendment mirrors
  - pipeline/blueprint/v0.1/section_02_v7_5_funding_goal_amendment.md                   # §2 v7.5 (paired-commit sibling 1/4)
  - pipeline/planning/f_reflection_f_wpfa_naming_reconciliation_2026-05-10.md           # Path B preemptive naming swap; F-FG-* family chosen
companion_amendment: pipeline/blueprint/v0.1/section_00_5_section_funding_goal_amendment.md  # §0.5 v20 paired-commit
compound_lock_with: section_02_v7_5_funding_goal_amendment.md + section_03_v6_funding_goal_amendment.md + section_00_5_section_funding_goal_amendment.md
v0_2_implementation_disposition: SPEC-ONLY. F-FG-* gate predicate bodies skeleton stubs raise NotImplementedError. v1.x amendment realizes LIVE bodies. Mirrors §15 v1 SPEC-ONLY precedent (rows 191/192) byte-for-byte. AST-lint rule R-FG-STUB-ONLY-AT-V0_2 (registered at §0.5 v20 row 470 per RT-C2-10) enforces.
---

# §4.X.4 F-FG-* failure-code family

This amendment registers the F-FG-* failure-code family for the `funding_goal` sub-kind. Per OQ-9 sub-code collapse: **8 codes / 5 modules**. Per §15 v1 SPEC-ONLY precedent: predicate bodies skeleton stubs raise NotImplementedError at v0.2; v1.x amendment realizes LIVE bodies.

## §4.X.4.1 Severity inheritance rule (RT-C2-08 + E-10)

**When a failure-code includes sub-tags, the effective severity is the maximum of the parent severity and all sub-tag severities. The Logician dispatcher MUST treat the code as P0 (no M13 bypass) if any sub-tag is P0.** This is the load-bearing rule for F-FG-LINKED-CYCLE-ORPHAN (parent HIGH + `.cross_org_grant_reference` sub-tag P0 → effective dispatch P0). Mirrors §17 WPFA F-WPFA-CROSS-ORG-LEAK pattern.

## §4.X.4.2 Failure-code table

| Code | Tier | Module | Severity | Sub-tags / Trigger |
|---|---|---|---|---|
| `F-FG-CROSS-ORG-LEAK` | PRE | `f_fg_cross_org_leak.py` | **P0 (Law 3) — no M13 bypass** | Read whose path resolves outside `orgs/<this_slug>/vault/operational/funding_goals/`. Sub-tags: `.path_traversal_detected` (RT-01), `.unicode_normalization_bypass` (RT-C2-01), `.symlink_detected` (RT-02), `.toctou_path_dereference` (RT-C2-02), `.cedar_engine_unavailable_fail_closed` (RT-05), `.principal_org_slug_externally_supplied` (RT-04). |
| `F-FG-SCHEMA-INVALID` | PRE-write + POST-read | `f_fg_schema_validation.py` (UMBRELLA — collapses three codes per OQ-9; module realizes F-FG-SCHEMA-INVALID + F-FG-CIC-TAG-INVALID + F-FG-CLC-TAG-INVALID) | HIGH | Sub-tags: `.float_target_amount_detected`, `.invariant_<n>_violated`, `.canonical_round_trip_drift`, `.record_id_path_traversal` (RT-03), `.future_timestamp` (RT-09), `.match_db_estimated_contribution_float_detected` (RT-14). Fires at MatchDB scoring invocation time per RT-14 to validate every MatchDB row's `estimated_contribution_minor_units` is `int`. M13 audited. |
| `F-FG-CIC-TAG-INVALID` | PRE-write | `f_fg_schema_validation.py` (sub-code) | HIGH | `cic_tag` not in six-CIC closed set. M13 audited. |
| `F-FG-CLC-TAG-INVALID` | PRE-write | `f_fg_schema_validation.py` (sub-code) | HIGH | Any element of `clc_tags` not in eight-CLC closed set. M13 audited. |
| `F-FG-STATUS-TRANSITION-INVALID` | PRE-write | `f_fg_status_transition_invalid.py` | HIGH | New record carries forbidden transition. **Gate consults admin-risk ledger via `funding_goals.resolve_live(...)` for prior status (RT-07).** Atomic ledger lookup + status write within `fcntl.flock(LOCK_EX)` (RT-C2-05); lock-acquisition-timeout-30s → fail-closed. Sub-tags: `.met_replay_attempted` (RT-07), `.ledger_entry_missing` (RT-08), `.malformed_ledger_entry` (RT-08), `.ledger_lock_timeout` (RT-C2-05), forbidden-transition base case. M13 audited. |
| `F-FG-LINKED-CYCLE-ORPHAN` | POST-read + PRE-cycle-start | `f_fg_linked_cycle_orphan.py` | **HIGH (effective P0 when `.cross_org_grant_reference` sub-tag fires per §4.X.4.1)** | `linked_cycle_ids` element does not resolve to live grant. **Gate enforces resolution WITHIN `orgs/<this_slug>/vault/grants/` (RT-23)** — uses `os.O_NOFOLLOW` + `os.path.realpath` + prefix check (RT-24). Sub-tags: `.cross_org_grant_reference` (RT-23, **P0 sub-tag — no M13 bypass**), `.symlink_in_grant_path` (RT-24), `.grant_path_outside_org_subtree` (RT-23), advisory base case. M13 audited (cross-org sub-tag NO bypass per §4.X.4.1). |
| `F-FG-PRIORITY-MUTATION-UNAUDITED` | PRE-write | `f_fg_priority_mutation_unaudited.py` | MEDIUM | Priority changed without admin-risk-ledger entry. M13 audited. |
| `F-FG-DEADLINE-EXPIRED-IGNORED` | POST-read | `f_fg_deadline_expired_ignored.py` | MEDIUM (advisory) | Deadline past + status pursuing + no mutation in operator-set window (default 30d). M13 NOT needed. |

**Module count after collapse: 5 modules realizing 8 codes** (one umbrella + four singletons).

## §4.X.4.3 META gate exclusion (OQ-10)

F-FG-* family does NOT register in F-CLASS-COVERAGE-INCOMPLETE's `REQUIRED_F_CLASS_CODES` registry. Documentary note: "F-FG-* is its own family with its own coverage discipline; META gate stays focused on F-CLASS-* per its current contract. Mirrors §17 WPFA F-WPFA-* exclusion at row 207."

## §4.X.4.4 Cedar engine fail-closed contract (RT-05 + RT-C2-04)

Cedar engine MUST be loaded at module-load time; load failure raises `CriticalPolicyError(BaseException)`. Mirrors §13 v1 RT-C2-04 Cedar engine mandatory-at-module-load precedent.

**`CriticalPolicyError` un-catchable contract (RT-C2-04):** AST-lint rule R-FG-NO-CATCH-CRITICAL flags any `except BaseException` or `except CriticalPolicyError` constructs outside the Cedar-engine bootstrap module. Registered at §0.5 v20 row 469.

## §4.X.4.5 F-CLASS-SLOT-ID-NON-OPAQUE PRE-gate regex extension (RT-12 + RT-C2-06)

Existing F-CLASS-SLOT-ID-NON-OPAQUE PRE-gate regex extended:
- Reject any slot containing alphabetic characters after `SLOT_` (RT-12).
- Slot IDs MUST be positive integers ≥ 1 (RT-C2-06): regex `^\[SLOT_[1-9][0-9]*\]$`. Reject `[SLOT_0]`, `[SLOT_-1]`, `[SLOT_]`.

Sub-tags: `.alphabetic_slot_id` (RT-12), `.non_positive_integer` (RT-C2-06).

## §4.X.4.6 SPEC-ONLY discipline at v0.2 (RT-C2-10)

All files under `pipeline/logician/gates/` defining an `F-FG-*` gate at v0.2 first ship MUST contain `raise NotImplementedError` AND MUST be excluded from test coverage AT v0.2. AST-lint rule R-FG-STUB-ONLY-AT-V0_2 (registered at §0.5 v20 row 470) flags any deviation. v1.x amendment lifts this restriction when LIVE bodies are realized.

This rule is the load-bearing structural enforcement of the §15 v1 SPEC-ONLY-at-v0.2 precedent.

# §4.X.4.7 §0.5 row registration

Eight failure-code rows in §0.5 v20 (rows 457-464):
- 457: F-FG-CROSS-ORG-LEAK
- 458: F-FG-SCHEMA-INVALID (umbrella)
- 459: F-FG-CIC-TAG-INVALID (sub-code under umbrella module)
- 460: F-FG-CLC-TAG-INVALID (sub-code under umbrella module)
- 461: F-FG-STATUS-TRANSITION-INVALID
- 462: F-FG-LINKED-CYCLE-ORPHAN
- 463: F-FG-PRIORITY-MUTATION-UNAUDITED
- 464: F-FG-DEADLINE-EXPIRED-IGNORED

Plus three AST-lint rows in §0.5 v20:
- 465: R-FG-NO-FLOAT-MONETARY (RT-13 + RT-C2-07)
- 469: R-FG-NO-CATCH-CRITICAL (RT-C2-04)
- 470: R-FG-STUB-ONLY-AT-V0_2 (RT-C2-10)

Plus one interface-contract row at §0.5 v20:
- 468: `match_db.scoring.goal_aware_match_score.v1` (the scoring composition callable per §4.3 of spec card v3; OQ-7 routed under interface-contract per minimum-vocabulary-extension discipline).

# §4.X.4.8 Changelog

- 2026-05-11 §4 v2.x.4 LOCKED — compound paired-commit (sibling 3/4). F-FG-* family registered (8 codes / 5 modules per OQ-9 collapse). SPEC-ONLY at v0.2 per §15 v1 precedent. All Cycle 1 + Cycle 2 closures absorbed. Severity inheritance rule §4.X.4.1 + Cedar engine fail-closed contract §4.X.4.4 + F-CLASS-SLOT-ID-NON-OPAQUE regex extension §4.X.4.5 + SPEC-ONLY discipline §4.X.4.6.
