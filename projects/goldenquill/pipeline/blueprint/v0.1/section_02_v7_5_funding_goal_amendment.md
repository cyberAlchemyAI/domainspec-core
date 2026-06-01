---
title: §2 v7.5 — Funding Goal sub-kind (compound paired-commit sibling 1/4)
filed: 2026-05-11
operator: Josh Inklovich
status: LOCKED 2026-05-11 — compound paired-commit (sibling 1/4) with §3 v6 + §4 v2.x.4 + §0.5 v20 at the same `lock_timestamp_utc` per §6.17 Option-B. L-005 strict two-cycle CLOSED with FULL LIVE CROSS-FAMILY rigor. Eleventh substantive v0.1+v0.2 round to LOCK at this rigor level.
parent_locks:
  - pipeline/blueprint/v0.1/section_02_vault_topology.md                                # v7.1 LOCKED 2026-04-19; §2 LOCKED-as-a-whole 2026-04-22
  - pipeline/blueprint/v0.1/section_02_v7_2_amendment.md                                # §2 v7.2 LOCKED 2026-05-10 rows 186/187 — Operational-data sub-kinds (THE convention this amendment follows EXACTLY)
  - pipeline/blueprint/v0.1/section_02_v7_4_coefficient_registry_amendment.md           # §2 v7.4 LOCKED 2026-05-11 row 206 — Coefficient Registry signed-asset class (mirrored discipline)
  - pipeline/architecture/v0.1/architecture_v7_0_4_M1_amendment.md                      # v7.0.4-M1 LOCKED 2026-05-10 row 190 — Decimal mandate + atomic-read fcntl.flock + symlink rejection
  - pipeline/architecture/v0.1/architecture_v7_0_7_amendment.md                         # v7.0.7 LOCKED 2026-05-10 row 180 — classification-driven routing
  - pipeline/architecture/v0.1/architecture_v7_0_8_amendment.md                         # v7.0.8 LOCKED — CIC × CLC orthogonality
  - pipeline/blueprint/v0.1/section_15_archivist.md                                     # §15 v1 SPEC LOCKED 2026-05-10 rows 191/192 — THE SPEC-ONLY-AT-v0.2 PRECEDENT this amendment mirrors
  - pipeline/blueprint/v0.1/section_14_report_generator.md                              # §14 v1 LOCKED 2026-05-10 rows 200/201 — FundingGoal feeds report narrative + claim_evidence_map per OQ-1
  - pipeline/planning/funding_goal_amendment_spec_2026-05-11_v3.md                      # spec card v3 (DISPATCH_SPEC_CYCLE_2_READY) — operator-pinned + 12 OQs absorbed + Cycle 1 + Cycle 2 closures
companion_amendment: pipeline/blueprint/v0.1/section_00_5_section_funding_goal_amendment.md  # §0.5 v20 paired-commit
compound_lock_with: section_03_v6_funding_goal_amendment.md + section_04_v2_x_4_funding_goal_amendment.md + section_00_5_section_funding_goal_amendment.md
v0_2_implementation_disposition: SPEC-ONLY at v0.2 per §15 v1 precedent. v0.2 first-ship LIVE: dataclasses + `__post_init__` invariants + canonical codec + sub-kind registry row + thin `resolve_live` helper + Cedar rules. v0.2 first-ship STUB: F-FG-* gate predicates raise NotImplementedError; v1.x amendment realizes LIVE bodies.
review_discipline: L-005 strict two-cycle, FULL live cross-family. Audit trail at `pipeline/validation/funding_goal_thesis_2026-05-11/`. Cycle 1 + Cycle 2 closures absorbed per cycle_1_disposition.md + cycle_2_disposition.md. Eleventh v0.1+v0.2 round at FULL live cross-family rigor (after WS-D/F/E/H/G/K/C-M1/L/I/J/Reflection v0.1 hook + WS-WPFA).
---

# §2.5 Reading map (extends §2 v7.2 §0)

This amendment adds an **eighth SIMPLE sub-kind** to the §2 v7.2 sub-kind family. The reading-map row:

| R.PF2 type | §1 row | Schema (this doc) | Cedar policy (this doc) | Failure codes | Code module | Test module | Severity |
|------------|--------|-------------------|--------------------------|---------------|-------------|-------------|----------|
| **funding_goal** (operator multi-year capital intent) | 8 | §2.11.8 | §6 (`goal_status_transition`, `goal_priority_mutation_audited`, `goal_taxonomy_closed`) | §7 (F-FG-* family — see §4 v2.x.4 amendment) | `pipeline/vault/sub_kinds/funding_goals.py` | `tests/vault/sub_kinds/test_funding_goals.py` | RED if `status == "blocked"`, else YELLOW |

# §2.13 Sub-kind table extension (eighth row)

Extends §2 v7.2 §1 sub-kind table:

| # | Sub-kind | Vault subtree | Intent | Permitted modes | Admin-risk severity |
|---|---|---|---|---|---|
| 8 | `funding_goal` | `operational/funding_goals/` | `operational-funding-goal-write` | `write-if-absent` | RED if `status == "blocked"`, else YELLOW |

SIMPLE class (no compound transaction; one record = one file). `write-if-absent` discipline uniform with the v7.2 seven sub-kinds.

# §2.11.8 `FundingGoal` schema

All schemas live at `pipeline/vault/sub_kinds/funding_goals.py`. Module exports the dataclasses, codec pair, and registry descriptor. Per §15 v1 SPEC-ONLY precedent, the gate predicates at `pipeline/logician/gates/f_fg_*.py` skeleton-stub-raise NotImplementedError at v0.2 first ship; the SUB_KIND module is fully LIVE.

```python
from dataclasses import dataclass

@dataclass(frozen=True, kw_only=True)
class FundingGoal:
    record_id: str                          # opaque caller-minted ID; matches filename {record_id}.json; regex ^[a-z0-9_-]+$ (RT-03)
    goal_name: str                          # operator-facing label
    target_amount_minor_units: int          # smallest currency unit (cents); A12 Decimal mandate; no float
    currency: str                           # ISO-4217 alpha-3
    target_deadline: str                    # UTC ISO-8601 date 'YYYY-MM-DD'
    purpose: str                            # free-form operator-discipline; classification SHAREABLE default per OQ-6
    cic_tag: str                            # one of six CIC slugs per CLAUDE.md
    clc_tags: tuple[str, ...]               # zero or more of eight CLC slugs; lex-sorted; orthogonal per v7.0.8
    status: str                             # "pursuing" | "blocked" | "met" | "abandoned"
    blockers: tuple[GoalBlocker, ...]       # non-empty REQUIRED iff status == "blocked"
    linked_cycle_ids: tuple[str, ...]       # grant_id strings; lex-sorted
    priority_weight: int                    # 0..100
    created_at: str                         # UTC ISO-8601 'Z'
    last_status_change_at: str              # UTC ISO-8601 'Z'


@dataclass(frozen=True, kw_only=True)
class GoalBlocker:
    blocker_kind: str                       # "rejection" | "capacity" | "timing" | "scope_change" | "external_constraint" | "other"
    summary: str
    surfaced_at: str                        # UTC ISO-8601 'Z'
    surfaced_by_grant_id: str | None
    surfaced_by_match_id: str | None
    resolution_hint: str
```

## §2.11.8.1 Invariants (`__post_init__` — fail-close at write AND at decode round-trip)

1. `record_id` non-empty AND matches regex `^[a-z0-9_-]+$` after Unicode NFKC normalization (RT-03 + RT-C2-01); reject any non-ASCII characters; reject `..`, `/`, path separators. Tampered records fail-close on `F-FG-SCHEMA-INVALID.record_id_path_traversal` + `.unicode_normalization_bypass`.
2. `goal_name` non-empty.
3. `currency` exactly three uppercase ASCII letters (`^[A-Z]{3}$`).
4. `target_amount_minor_units` is `int` (not `bool`, not `float`); `target_amount_minor_units >= 0`. Tampered records fail-close on `F-FG-SCHEMA-INVALID.float_target_amount_detected`.
5. `target_deadline` matches `^\d{4}-\d{2}-\d{2}$` (date-only); reject `target_deadline < created_at[:10]` IF status is "pursuing" or "blocked" (OQ-3 reject).
6. `cic_tag` is in the closed set of six CIC slugs declared in CLAUDE.md.
7. `clc_tags` is a tuple of CLC slug strings; every element is in the closed set of eight CLC slugs; duplicates rejected; tuple is lex-sorted (deterministic on-disk form).
8. `status` is in `{"pursuing", "blocked", "met", "abandoned"}`.
9. If `status == "blocked"`, `blockers` is non-empty.
10. `linked_cycle_ids` tuple of non-empty strings; duplicates rejected; lex-sorted on-disk form.
11. `priority_weight` is `int` in `[0, 100]`.
12. `created_at` and `last_status_change_at` end with `'Z'`; `last_status_change_at >= created_at` (lex compare); **AND `created_at <= now_utc` (lex compare; reject future timestamps per RT-09).** Tampered records fail-close on `F-FG-SCHEMA-INVALID.future_timestamp`.
13. Per `GoalBlocker`: `blocker_kind` in closed set; `summary` non-empty; `surfaced_at` ends with `'Z'`; at most one of `surfaced_by_grant_id` / `surfaced_by_match_id` is non-None.

## §2.11.8.2 LIVE/STUB primitive table at v0.2 first ship

Per Cycle 2 RT-21 + RT-22 + RT-C2-10 closures, explicit per-primitive LIVE/STUB annotation:

| Primitive | LIVE at v0.2? | Note |
|-----------|---------------|------|
| `FundingGoal` + `GoalBlocker` dataclasses + `__post_init__` invariants | LIVE | Schema enforcement at write + decode round-trip |
| `funding_goals.to_canonical_bytes` / `from_canonical_bytes` codec pair | LIVE | §2 v7.2 sub-kind convention requires working codec |
| `funding_goals.record_id_for` | LIVE | Filename derivation |
| `funding_goals.resolve_live(record_id_set, admin_risk_ledger)` thin helper | LIVE | OQ-5; consumed by Scout REVIEW + Match DB scoring + Monday brief |
| `SUB_KIND_REGISTRY["funding_goal"]` row | LIVE | §2.12 registry binding |
| `severity_for` lambda | LIVE | RED-on-blocked discrimination |
| Cedar rules (`goal_status_transition`, `goal_priority_mutation_audited`, `goal_taxonomy_closed`) | LIVE | Cedar engine evaluates at write + read |
| F-FG-* gate predicates (8 codes, 5 modules) | **STUB-RAISE NotImplementedError at v0.2** | Per §15 v1 SPEC-ONLY precedent (rows 191/192). v1.x Code-phase realizes LIVE bodies. AST-lint rule R-FG-STUB-ONLY-AT-V0_2 enforces (per RT-C2-10). |

## §2.11.8.3 A12 Decimal mandate dispatch

R-FG-NO-FLOAT-MONETARY AST-lint rule scope: `pipeline/vault/sub_kinds/funding_goals.py` + `pipeline/match_db/scoring.py` + ALL sub-directories under `pipeline/match_db/` (RT-13 + RT-C2-07; recursive). Mirrors §17 WPFA RT-C2-01 R-WPFA-DECIMAL-MANDATE-ENERGY scope-extension precedent.

# §2.12 Sub-kind registry row (extends §2 v7.2 §2.12)

```python
"funding_goal": SubKindDescriptor(
    intent="operational-funding-goal-write",
    vault_subtree="operational/funding_goals/",
    record_class=FundingGoal,
    to_canonical_bytes=funding_goals.to_canonical_bytes,
    from_canonical_bytes=funding_goals.from_canonical_bytes,
    record_id_for=funding_goals.record_id_for,
    severity_default="YELLOW",
    severity_for=lambda record: "RED" if record.status == "blocked" else "YELLOW",
),
```

# §2.13 POST_GATE_ALLOWLIST extension (eighth row)

```python
POST_GATE_ALLOWLIST.add("operational-funding-goal-write")  # SIMPLE; write-if-absent
```

# §2.14 Vault layout

```python
class VaultLayout:
    @staticmethod
    def org_vault_operational_funding_goals(slug: str) -> Path:
        return Path(f"orgs/{slug}/vault/operational/funding_goals")
```

**Slug validation (RT-01):** caller MUST validate `slug` against `orgs/ORG_INDEX.md` registry membership AT call site. After Unicode NFKC normalization (RT-C2-01), enforce regex `^[a-z0-9_-]+$`. Reject `..`, `/`, any character outside the set. F-FG-CROSS-ORG-LEAK PRE-gate fails closed on validation failure.

**O_NOFOLLOW + atomic read (RT-02 + RT-C2-02):** every read of `operational/funding_goals/*.json` uses `os.open(path, os.O_RDONLY | os.O_NOFOLLOW)` + `fcntl.flock(LOCK_SH)` per v7.0.4-M1 §4 atomic-read precedent. No intermediate path-string dereference between regex check and open() call. Symlink rejection inherited from v7.0.4-M1 §4.

# §2.15 Status mutation discipline (extends §2 v7.2 §1 worked operator re-key path)

Status changes follow the v7.2 worked operator re-key path:

1. Operator mints a fresh `record_id` (UUID4).
2. Operator writes the updated `FundingGoal` record.
3. Operator appends an admin-risk-ledger entry naming both `record_id`s and the supersession reason.
4. The original record persists at its path.

**Forbidden transitions (OQ-8 + RT-07):** `met → pursuing` is forbidden. F-FG-STATUS-TRANSITION-INVALID gate consults the admin-risk ledger via `funding_goals.resolve_live(...)` to find prior logical-goal status; reject any transition where prior was `met`.

**Atomic ledger lookup + status write (RT-C2-05):** `resolve_live(...)` lookup AND any subsequent status mutation MUST be performed within a single OS-level file lock (`fcntl.flock(LOCK_EX)`) on the admin-risk ledger file to guarantee serialization. Lock-acquisition-timeout-30s → fail-closed. Mirrors §15 v1 RT-05 confirmation_id ledger discipline.

**Thin resolution helper (OQ-5):** `funding_goals.resolve_live(record_id_set: set[str], admin_risk_ledger: AdminRiskLedger) -> FundingGoal` LIVE at v0.2; consumed by Scout REVIEW + Match DB scoring + Monday brief.

# §2.16 Cedar policy additions

Three new rules + one extension to `pipeline/vault/policies/operational_subkinds.cedar`:

1. **Extension to `operational_org_isolation`:** add `sub_kind == "funding_goal"` to default-permit set. F-FG-CROSS-ORG-LEAK at Logician layer is defense-in-depth.
2. **`goal_status_transition`:** permits goal writes only when transition is permitted per §6 (forbids `met → pursuing`) AND admin-risk-ledger entry signed.
3. **`goal_priority_mutation_audited`:** permits goal writes whose `priority_weight` differs from prior live only when admin-risk-ledger entry captures mutation reason.
4. **`goal_taxonomy_closed`:** permits goal writes only when `cic_tag` ∈ six-CIC AND every element of `clc_tags` ∈ eight-CLC. CIC × CLC orthogonality preserved (independent set membership; no pre-mapping).

**Engine-bound principal (RT-04):** Cedar engine MUST derive `principal.org_slug` from authenticated session token at engine-load time; reject any externally-supplied `principal.org_slug` value at policy evaluation. Mirrors §13 v1 RT-C2-04 OrgScopedBot @final wrapper precedent.

**Cedar engine fail-closed contract (RT-05):** Cedar engine MUST be loaded at module-load time. Load failure raises `CriticalPolicyError(BaseException)` (mirrors §13 v1 RT-C2-04 Cedar engine mandatory-at-module-load precedent). F-FG-CROSS-ORG-LEAK fires fail-closed on engine-unavailable.

**`CriticalPolicyError` un-catchable contract (RT-C2-04):** `CriticalPolicyError` MUST NOT be caught by any application code. AST-lint rule R-FG-NO-CATCH-CRITICAL (registered at §0.5 v20 row 469) flags any `except BaseException` or `except CriticalPolicyError` outside the Cedar-engine bootstrap module.

**Session-token integrity (RT-C2-03 BOUNDED-by-A1+A4):** session token MUST be cryptographically signed by the Org-Auth service, include a nonce, and be verified for freshness (≤ 5 min). At v0.2, single-client A1 + operator-trusted A4 bounds the threat model; v2 multi-tenant amendment per Section O.5 lands token integrity full-stack.

**CIC/CLC closed-set asset signing (RT-06 BOUNDED-by-A1+A4):** CIC/CLC closed-set assets at `assets/cards/customer_identification/` + `assets/cards/capital_logic/` are operator-pinned at white-glove onboarding at v0.2 (per A4 operator-trusted preflight). v1.x amendment lands SN-LLC Ed25519 signing + verification at engine-load (mirrors v7.0.7 §6.1 router-template signing precedent).

# §2.17 Operator-discipline boundary (matches §2 v7.2 convention)

`FundingGoal` schema validates **structure** (types, ISO-8601 trailing 'Z', currency three-letter, regex on record_id, status closed set, CIC/CLC closed sets, Decimal mandate). Schema does NOT validate **content** of free-form text fields (`goal_name`, `purpose`, `blocker.summary`, `blocker.resolution_hint`). Operator-discipline boundary per §2 v7.2 §2.11 free-text fields contract.

# §2.18 Changelog

- 2026-05-11 v7.5 LOCKED — compound paired-commit (sibling 1/4) with §3 v6 + §4 v2.x.4 + §0.5 v20. SPEC-ONLY at v0.2 per §15 v1 precedent. Operator OQ-1 pin: ships alongside §14 Report Generator. F-FG-* family (8 codes / 5 modules per OQ-9 collapse). All 37 Cycle 1 dispositions + 13 Cycle 2 NEW dispositions absorbed. L-005 strict two-cycle CLOSED with FULL live cross-family rigor.
