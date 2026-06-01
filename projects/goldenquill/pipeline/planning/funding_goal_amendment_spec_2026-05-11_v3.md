---
title: Funding-Goal Sub-Kind — Dispatch Spec Card v3 (Cycle 1 closures absorbed; Cycle 2 ready)
filed: 2026-05-11
operator: Josh Inklovich
supersedes: pipeline/planning/funding_goal_amendment_spec_2026-05-11_v2.md (v2 DISPATCH_SPEC_READY → Cycle 1 closed)
status: DISPATCH_SPEC_CYCLE_2_READY — Cycle 1 absorbed all 37 dispositions per `pipeline/validation/funding_goal_thesis_2026-05-11/cycle_1_disposition.md` (8 Editor + 2 Judge + 6 P0 + 8 HIGH + 6 MED + 7 LOW = 37 closures: 35 FOLD-IN + 1 BOUNDED-by-A1+A4 + 1 DEFERRED to v1.x). L-005 strict two-cycle Thesis Cycle 2 (verification) is the next gate.
parent_locks:
  # See v2 spec card for the full 18-parent_lock chain — unchanged.
  - pipeline/planning/funding_goal_amendment_spec_2026-05-11_v2.md                       # v2 DISPATCH_SPEC_READY (this file's predecessor)
  - pipeline/validation/funding_goal_thesis_2026-05-11/cycle_1_disposition.md           # Cycle 1 absorption per row-170 transparent disposition pattern
authority: Cycle 1 closures absorbed; Cycle 2 verification dispatch is the next L-005 step
dispatch_class: spec_card_for_blueprint_amendment_family (Cycle 2 ready)
ws_dispatch_target: WS-FG Funding Goal
review_discipline: L-005 strict two-cycle, FULL live cross-family per /AGENTS.md (Editor + Judge + Red Team) — Cycle 2 verifies Cycle 1 closures.
naming_reconciliation_status: Path B applied preemptively (F-FG-* family). Per Cycle 1 RT-20 closure, naming reconciliation packet update reserves `FG` abbreviation as Funding-Goal-only; documented at `pipeline/planning/f_reflection_f_wpfa_naming_reconciliation_2026-05-10.md` §3 follow-up edit at LOCK ceremony (paired with §0.5 v20 amendment).
---

# §0. Cycle 1 closures absorbed (delta from v2)

This v3 absorbs all 37 dispositions from `pipeline/validation/funding_goal_thesis_2026-05-11/cycle_1_disposition.md`. Section-by-section deltas:

## §0.1 Editor closures (8)

E-01 / E-04 / E-06: §0 OQ-resolution table cross-references reinforced (each OQ row now lists the downstream sections that absorb it).
E-02: §0 path-reference to naming reconciliation packet added.
E-03: §6 SPEC-ONLY discipline note expanded to cite §15 v1 precedent inline.
E-05: §8 dedicated parent-wins discipline sub-paragraph (§8.1) added.
E-07: §6 umbrella-module-pattern inline note added.
E-08: §9.2 OQ relevance annotations added.

## §0.2 Judge closures (2)

J-01: §4.1 illustrative YAML float-literal corrected (`<0.0 - 1.0>` → string-Decimal form).
J-02: §8 row 468 parenting comment added.

## §0.3 Red Team closures (27 RT-NN findings → 35 FOLD-IN + 1 BOUNDED + 1 DEFERRED)

**P0 (6):** RT-01 (slug validation) + RT-02 (O_NOFOLLOW on funding_goal reads) + RT-04 (Cedar engine-bound principal) + RT-05 (Cedar fail-closed CriticalPolicyError) + RT-23 (orphan check enforces same-org subtree, severity upgraded to HIGH) — all FOLD-IN.

**HIGH (8):** RT-03 (record_id regex), RT-06 (CIC/CLC asset signing — bounded-by-A1+A4 at v0.2; v1.x SN-LLC signing), RT-07 (status-transition gate consults ledger), RT-12 (slot-naming numeric-only enforcement), RT-13 (AST-lint scope extension to match_db/), RT-14 (F-FG-SCHEMA-INVALID umbrella covers MatchDB rows), RT-15 (explicit Decimal cast), RT-24 (orphan check O_NOFOLLOW + realpath + prefix check) — all FOLD-IN; RT-10 BOUNDED-by-A1+A4 (cache invalidation latency v0.2 known-limitation; v1.x per-cycle hook; v2 real-time per Section O.5).

**MED (6):** RT-08 (gate verifies ledger entry) + RT-09 (`created_at <= now_utc`) + RT-11 (per-grant SP0 propagation) + RT-16 (no float persistence) + RT-19 (seat_owner attribute) + RT-25 (Monday cron per-org) + RT-26 (CRITICAL-FIT-AGAINST-GOAL per-org filter) — all FOLD-IN.

**LOW (7):** RT-17 (additive bonus clarification) + RT-20 (FG abbreviation reservation) + RT-21/22 (LIVE/stub annotation table) + RT-27 (UNALLOCATED admin-only) — FOLD-IN; RT-18 (Cedar pair-blacklist) — DEFERRED to v1.x.

# §1. Compound-LOCK pairing identity (unchanged from v2)

Four siblings: §2 v7.5 + (§3 v6 + §6.x amendment) + §4 v2.x.4 + §0.5 v20. Anticipated lock_history rows 209-212 (compound at single `lock_timestamp_utc`).

**§1.1 Partition summary (E-04 closure).** Each sibling's content scope:
- **§2 v7.5:** `FundingGoal` + `GoalBlocker` schemas + sub-kind registry row + Cedar policy extension + vault subtree.
- **§3 v6:** Scout DISCOVER input-shape extension (`funding_goals` parameter; goal-aware ranking composer; per-org slug validation per RT-01).
- **§6.x amendment:** prompt-template goals-block injection (start-block + end-block; classification-aware redaction; numeric opaque slot enforcement per RT-12).
- **§4 v2.x.4:** F-FG-* failure-code family registration (8 codes / 5 modules per OQ-9; SPEC-ONLY skeleton stubs raising NotImplementedError per §15 v1 precedent).
- **§0.5 v20:** row-append registration (rows 446-468; seat_owner attribute per RT-19; AST-lint row 465 under v19 vocabulary).

# §2. Pydantic dataclass shape — `FundingGoal` (with Cycle 1 closures)

Mirror §2 v7.2 sub-kind convention exactly. v0.2 first-ship LIVE: dataclasses + `__post_init__` invariants + canonical codec + sub-kind registry row + thin `resolve_live` helper. v0.2 first-ship STUB: F-FG-* gate predicates raise NotImplementedError per §15 v1 SPEC-ONLY precedent.

```python
@dataclass(frozen=True, kw_only=True)
class FundingGoal:
    record_id: str                          # opaque caller-minted ID; matches filename {record_id}.json
    goal_name: str                          # operator-facing label
    target_amount_minor_units: int          # smallest currency unit; A12 Decimal mandate; no float
    currency: str                           # ISO-4217 alpha-3
    target_deadline: str                    # UTC ISO-8601 date 'YYYY-MM-DD'
    purpose: str                            # free-form operator-discipline; classification: shareable default per OQ-6
    cic_tag: str                            # one of six CIC slugs per CLAUDE.md
    clc_tags: tuple[str, ...]               # zero or more of eight CLC slugs; lex-sorted; orthogonal per v7.0.8
    status: str                             # "pursuing" | "blocked" | "met" | "abandoned"
    blockers: tuple[GoalBlocker, ...]
    linked_cycle_ids: tuple[str, ...]
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

## §2.1 A12 Decimal mandate dispatch (extended per RT-13)

R-FG-NO-FLOAT-MONETARY AST-lint rule scope: **`pipeline/vault/sub_kinds/funding_goals.py` + `pipeline/match_db/scoring.py` + `pipeline/match_db/`** (RT-13 extension). Mirrors §17 WPFA RT-C2-01 R-WPFA-DECIMAL-MANDATE-ENERGY scope-extension precedent (extended to composer modules). Registered as `ast-lint` row 465 in §0.5 v20.

## §2.2 Invariants (extended per RT-03 + RT-09)

Thirteen invariants from v1 spec card carry forward byte-identically with two extensions:

**Invariant 1 (extended per RT-03):** `record_id` non-empty AND matches regex `^[a-z0-9_-]+$` (no `..`, no `/`, no path separators). Tampered records fail-close on `F-FG-SCHEMA-INVALID.record_id_path_traversal`.

**Invariant 12 (extended per RT-09):** `created_at` and `last_status_change_at` end with `'Z'`; `last_status_change_at >= created_at` (lex compare); **AND `created_at <= now_utc` (lex compare; reject future timestamps).** Tampered records fail-close on `F-FG-SCHEMA-INVALID.future_timestamp`.

## §2.3 Sub-kind registry row + LIVE/STUB primitive table (per RT-21 + RT-22)

```python
"funding_goal": SubKindDescriptor(
    intent="operational-funding-goal-write",
    vault_subtree="operational/funding_goals/",
    record_class=FundingGoal,
    to_canonical_bytes=funding_goals.to_canonical_bytes,           # LIVE at v0.2
    from_canonical_bytes=funding_goals.from_canonical_bytes,       # LIVE at v0.2
    record_id_for=funding_goals.record_id_for,                     # LIVE at v0.2
    severity_default="YELLOW",
    severity_for=lambda record: "RED" if record.status == "blocked" else "YELLOW",  # LIVE at v0.2
),
```

**LIVE/STUB primitive table at v0.2 first ship:**

| Primitive | LIVE at v0.2? | Note |
|-----------|---------------|------|
| `FundingGoal` + `GoalBlocker` dataclasses + `__post_init__` invariants | LIVE | Schema enforcement at write + decode round-trip |
| `funding_goals.to_canonical_bytes` / `from_canonical_bytes` codec pair | LIVE | §2 v7.2 sub-kind convention requires working codec |
| `funding_goals.record_id_for` | LIVE | Filename derivation |
| `funding_goals.resolve_live(record_id_set, admin_risk_ledger)` thin helper | LIVE | OQ-5 helper; consumed by Scout REVIEW + Match DB scoring + Monday brief |
| `SUB_KIND_REGISTRY["funding_goal"]` row | LIVE | §2.12 registry binding |
| `severity_for` lambda | LIVE | RED-on-blocked discrimination |
| Cedar rules (`goal_status_transition`, `goal_priority_mutation_audited`, `goal_taxonomy_closed`) | LIVE | Cedar engine evaluates at write + read |
| F-FG-* gate predicates (8 codes, 5 modules) | **STUB-RAISE NotImplementedError at v0.2** | Per §15 v1 SPEC-ONLY precedent; v1.x Code-phase realizes |

## §2.4 Admin-risk severity (unchanged)

Default YELLOW. RED when `status == "blocked"` per OQ-4.

## §2.5 Status mutation discipline + thin resolution helper (extended per RT-07 + RT-08)

Re-key path per §2 v7.2 §1 unchanged. `funding_goals.resolve_live(...)` thin helper LIVE at v0.2 per OQ-5.

**Forbidden transition (OQ-8 + RT-07 extended):** `met → pursuing` is forbidden; F-FG-STATUS-TRANSITION-INVALID gate consults the admin-risk ledger via `resolve_live(...)` to find the prior logical-goal status; reject any transition where prior was `met`. Adds sub-tag `.met_replay_attempted`.

**Ledger entry verification (RT-08 fold-in):** F-FG-STATUS-TRANSITION-INVALID gate ALSO verifies presence of admin-risk-ledger entry for every status change; missing or malformed entry → fail-closed. Adds sub-tag `.ledger_entry_missing`.

# §3. §3 v6 Scout DISCOVER + §6.x prompt-compilation integration (with closures)

## §3.1 §3 v6 amendment — DISCOVER input-shape (extended per RT-01 + RT-02)

`Scout.session_call()` adds optional `funding_goals: tuple[FundingGoal, ...]` parameter, read at session start from `orgs/{slug}/vault/operational/funding_goals/` filtering `status in {"pursuing", "blocked"}`.

**Slug validation (RT-01 fold-in):** `{slug}` MUST be validated against `orgs/ORG_INDEX.md` registry membership at session start; reject `slug` containing `..` or path separators or any character outside `^[a-z0-9_-]+$`. F-FG-CROSS-ORG-LEAK PRE-gate fails closed on validation failure.

**O_NOFOLLOW + atomic read (RT-02 fold-in):** every read of `operational/funding_goals/*.json` uses `os.O_NOFOLLOW` + `fcntl.flock(LOCK_SH)` per v7.0.4-M1 §4 atomic-read precedent. Symlink rejection inherited from v7.0.4-M1 §4. Goals-read substrate explicitly inherits this guarantee in spec text.

## §3.2 §6.x prompt-compilation goals-block injection (extended per RT-10 + RT-11 + RT-12)

§6.11 prompt-template compilation pipeline gains a goals-block injected at start-block + end-block (A4 architectural FLOOR; F-CONTEXT-PLACEMENT PRE-gate enforces).

**Per-grant SP0 override propagation (RT-11 fold-in):** goals-block compiler reads BOTH org-level + per-grant SP0 classification register, with per-grant override taking precedence. Mirrors v7.0.7 §3.6 three-layer-defaults precedence rule.

**Numeric opaque slot enforcement (RT-12 fold-in):** goals-block compiler MUST emit only `[SLOT_<int>]` numeric opaque slots; semantic-named slots like `[SLOT_GOAL_PURPOSE_<record_id>]` are forbidden. F-CLASS-SLOT-ID-NON-OPAQUE PRE-gate's regex extended via §4 v2.x to reject any slot containing alphabetic characters after `SLOT_`. Spec adds dedicated note that the goals-block compiler is covered.

**Cache-invalidation latency (RT-10 BOUNDED-by-A1+A4):** at v0.2, classification override cache-invalidation latency is bounded by single-cycle wall (operator runs explicit cycle restart per v7.0.7 §3.6). v1.x amendment lands per-cycle invalidation hook. v2 multi-tenant amendment lands real-time invalidation per Section O.5. Mirrors WPFA RT-04/RT-05 BOUNDED-by-A1+A4 precedent at row 207. **v0.2 known-limitation explicitly documented.**

## §3.3 `fit_score_cached` composition — additive per dimension (RT-17 fold-in clarification)

`bonus = (cic_match_bonus) + (clc_overlap_bonus)`, NOT AND-gated. Both bonuses fire independently when their respective dimension matches. CIC × CLC orthogonality preserved as truly additive composition.

## §3.4 CIC × CLC orthogonality preservation (unchanged)

Per v7.0.8 LOCK + CLAUDE.md, treated as independent dimensions. F-CIC-CLC-COUPLING-VIOLATION regression-test against goal-schema, Cedar rules, Scout DISCOVER ranking function, and Match DB scoring composer at LOCK against four detection layers.

# §4. Match DB v1→v2 (with closures)

## §4.1 Schema additions to `match_database.v2` (corrected per Judge J-01 + RT-14 + RT-16)

```yaml
contributes_to_goals:
  - goal_record_id: <FundingGoal.record_id>
    estimated_contribution_minor_units: <int>            # int only; F-FG-SCHEMA-INVALID.match_db_estimated_contribution_float_detected fires on float (RT-14)
    estimated_contribution_confidence: <"low" | "medium" | "high">
goal_aware_match_score: <stringified-Decimal-4dp>        # e.g. "0.9123" — string in YAML, parsed via Decimal at decode (J-01 + RT-16)
```

## §4.2 Goal-aware match score composition — explicit Decimal cast (extended per RT-15)

```python
def goal_aware_match_score(match: MatchRow, active_goals: Mapping[str, FundingGoal]) -> Decimal:
    base = Decimal(str(match.match_score))                   # base ratio in [0, 1]
    if not match.contributes_to_goals:
        return base
    goal_bonuses = []
    for gc in match.contributes_to_goals:
        if gc.goal_record_id not in active_goals:
            continue                                         # silent contributes 0; F-FG-LINKED-CYCLE-ORPHAN advisory surfaces separately
        weight_g = Decimal(active_goals[gc.goal_record_id].priority_weight) / Decimal(100)
        # RT-15 explicit Decimal cast — no implicit float division
        contribution_ratio_g = min(
            Decimal(1),
            Decimal(int(gc.estimated_contribution_minor_units))
                / Decimal(int(active_goals[gc.goal_record_id].target_amount_minor_units)),
        )
        confidence_factor_g = {"low": Decimal("0.5"), "medium": Decimal("0.75"), "high": Decimal("1.0")}[gc.estimated_contribution_confidence]
        goal_bonuses.append(weight_g * contribution_ratio_g * confidence_factor_g)
    goal_bonus = max(goal_bonuses) if goal_bonuses else Decimal(0)
    GOAL_BONUS_WEIGHT = Decimal("0.25")
    composite = min(Decimal(1), base + GOAL_BONUS_WEIGHT * goal_bonus)
    # RT-16 no-float-persistence — round + return Decimal; YAML serializer renders as string
    return composite.quantize(Decimal("0.0001"), rounding=ROUND_HALF_EVEN)
```

## §4.3 Scoring callable (unchanged from v2)

Module `pipeline/match_db/scoring.py` (NEW). Function `goal_aware_match_score(...)`. §0.5 row 468 registered as `interface-contract` per OQ-7.

## §4.4 No migration shim (unchanged from v2)

# §5. Push-notify wiring (extended per RT-25 + RT-26 + RT-27)

## §5.1 Per-org isolation enforcement (RT-25 + RT-26 fold-in)

Monday fund-radar cron runs **PER-ORG** (one brief per org); Josh-facing digest aggregates ONLY metadata (total candidate count, total goal count), NEVER per-org dollar amounts or per-org goal names. Mirrors `project_monday_fund_routine.md` Law 3 isolation guarantee.

CRITICAL-FIT-AGAINST-GOAL tag generation MUST filter per-org BEFORE tag emission; cross-org goal-aware tagging is forbidden.

## §5.2 v0.2 first-ship channels (D + A only per OQ-12 v0.2-shift)

Per v2 spec card §5 unchanged. CLI-on-next-run + Monday-brief integration. B + C as v0.2 second-wave candidates. Cultivator Telegram via §13 OrgScopedBot @final wrapper as v0.2 second-wave home.

## §5.3 Per-client brief format (extended per RT-27)

Per v2 spec card §5.4 unchanged with one rename: "UNALLOCATED CANDIDATES" → **"GLOBAL UNALLOCATED CANDIDATES — admin only"**; emitted ONLY to Josh-facing digest, NEVER to per-client briefs.

# §6. F-FG-* failure-code family (extended per RT-04 + RT-05 + RT-07 + RT-08 + RT-09 + RT-12 + RT-14 + RT-23 + RT-24)

SPEC-ONLY at v0.2 per §15 v1 precedent (predicate bodies stub-raise NotImplementedError; v1.x Code-phase realization).

| Code | Tier | Module | Severity | Sub-tags / Trigger |
|---|---|---|---|---|
| `F-FG-CROSS-ORG-LEAK` | PRE | `f_fg_cross_org_leak.py` | P0 (Law 3) | Read whose path resolves outside `orgs/<this_slug>/vault/operational/funding_goals/`. **No M13 bypass.** Sub-tags: `.path_traversal_detected` (RT-01), `.symlink_detected` (RT-02), `.cedar_engine_unavailable_fail_closed` (RT-05), `.principal_org_slug_externally_supplied` (RT-04). |
| `F-FG-SCHEMA-INVALID` | PRE-write + POST-read | `f_fg_schema_validation.py` (UMBRELLA — collapses three codes per OQ-9) | HIGH | Sub-tags: `.float_target_amount_detected`, `.invariant_<n>_violated`, `.canonical_round_trip_drift`, `.record_id_path_traversal` (RT-03), `.future_timestamp` (RT-09), `.match_db_estimated_contribution_float_detected` (RT-14). Fires at MatchDB scoring invocation time per RT-14 to validate every MatchDB row's `estimated_contribution_minor_units` is `int`. M13 audited. |
| `F-FG-CIC-TAG-INVALID` | PRE-write | `f_fg_schema_validation.py` (sub-code) | HIGH | `cic_tag` not in six-CIC closed set. M13 audited. |
| `F-FG-CLC-TAG-INVALID` | PRE-write | `f_fg_schema_validation.py` (sub-code) | HIGH | Any element of `clc_tags` not in eight-CLC closed set. M13 audited. |
| `F-FG-STATUS-TRANSITION-INVALID` | PRE-write | `f_fg_status_transition_invalid.py` | HIGH | New record carries forbidden transition. **Gate consults admin-risk ledger via `funding_goals.resolve_live(...)` to find prior logical-goal status (RT-07 fold-in).** Sub-tags: `.met_replay_attempted` (RT-07), `.ledger_entry_missing` (RT-08), `.malformed_ledger_entry` (RT-08), forbidden-transition base case. M13 audited. |
| `F-FG-LINKED-CYCLE-ORPHAN` | POST-read + PRE-cycle-start | `f_fg_linked_cycle_orphan.py` | **HIGH (upgraded from MEDIUM per RT-23)** | `linked_cycle_ids` element does not resolve to live grant. **Gate enforces resolution WITHIN `orgs/<this_slug>/vault/grants/` (RT-23 fold-in).** Resolution uses `os.O_NOFOLLOW` + `os.path.realpath` + prefix check (RT-24 fold-in). Sub-tags: `.cross_org_grant_reference` (RT-23, P0 sub-tag), `.symlink_in_grant_path` (RT-24), `.grant_path_outside_org_subtree` (RT-23), advisory base case. M13 audited (cross-org sub-tag NO bypass). |
| `F-FG-PRIORITY-MUTATION-UNAUDITED` | PRE-write | `f_fg_priority_mutation_unaudited.py` | MEDIUM | Priority changed without admin-risk-ledger entry. M13 audited. |
| `F-FG-DEADLINE-EXPIRED-IGNORED` | POST-read | `f_fg_deadline_expired_ignored.py` | MEDIUM (advisory) | Deadline past + status pursuing + no mutation in operator-set window. M13 NOT needed. |

**Module count after collapse: 5 modules realizing 8 codes** (one umbrella `f_fg_schema_validation.py` realizing F-FG-SCHEMA-INVALID + F-FG-CIC-TAG-INVALID + F-FG-CLC-TAG-INVALID; four singletons).

**Umbrella module pattern (E-07 fold-in):** `f_fg_schema_validation.py` consolidates three codes that share the same `FundingGoal` decoder + per-field validator surface. Mirrors §4 v2.x F-CLASS-* sub-code-collapse precedent + §17 WPFA F-WPFA-COEFFICIENT-REGISTRY-VALIDATION triplet collapse precedent (row 207).

**META gate exclusion (OQ-10):** F-FG-* family does NOT register in F-CLASS-COVERAGE-INCOMPLETE's `REQUIRED_F_CLASS_CODES`. Mirrors §17 WPFA F-WPFA-* exclusion at row 207.

**Cedar engine fail-closed contract (RT-05 fold-in):** Cedar engine MUST be loaded at module-load time; load failure raises `CriticalPolicyError(BaseException)` (mirrors §13 v1 RT-C2-04 Cedar engine mandatory-at-module-load precedent). F-FG-CROSS-ORG-LEAK fires fail-closed on engine-unavailable. Defense-in-depth at Logician layer.

# §7. Cedar policy additions (extended per RT-04 + RT-06)

Three new rules + one extension:

1. **Extension to `operational_org_isolation`:** add `sub_kind == "funding_goal"` to default-permit set. F-FG-CROSS-ORG-LEAK at Logician layer is defense-in-depth.
2. **`goal_status_transition`:** permits goal writes only when transition is permitted per §6 + admin-risk-ledger entry signed.
3. **`goal_priority_mutation_audited`:** permits goal writes whose `priority_weight` differs from prior live only when admin-risk-ledger entry captures mutation reason.
4. **`goal_taxonomy_closed`:** permits goal writes only when `cic_tag` ∈ six-CIC AND every element of `clc_tags` ∈ eight-CLC.

**Engine-bound principal (RT-04 fold-in):** Cedar engine MUST derive `principal.org_slug` from authenticated session token at engine-load time; reject any externally-supplied `principal.org_slug` value at policy evaluation. Mirrors §13 v1 RT-C2-04 OrgScopedBot @final wrapper precedent.

**CIC/CLC closed-set asset signing (RT-06 BOUNDED-by-A1+A4 at v0.2):** CIC/CLC closed-set assets at `assets/cards/customer_identification/` + `assets/cards/capital_logic/` are **operator-pinned at white-glove onboarding** at v0.2 (per A4 operator-trusted preflight). v1.x amendment lands SN-LLC Ed25519 signing + verification at engine-load (mirrors v7.0.7 §6.1 router-template signing precedent). Bounded by v7 LOCKED A1+A4 at v0.2; v2 multi-tenant amendment per Section O.5 lands real-time signing.

# §8. §0.5 v20 amendment — row range 446-468 (extended per RT-19 + Judge J-02)

Current runtime-live = **445** (post §17 + §0.5 v19 LOCK row 208). Funding Goal compound LOCK allocates rows 446-468 (23 rows).

| Row | primitive_id | kind | seat_owner (RT-19) | Parent |
|---|---|---|---|---|
| 446 | `blueprint.section_anchor.s02_v7_5_funding_goal.v1` | marker | funding_goal | §2 v7.5 |
| 447 | `vault.sub_kinds.funding_goal.v1` | schema | funding_goal | `FundingGoal` frozen kw_only |
| 448 | `vault.sub_kinds.funding_goal.goal_blocker.v1` | schema | funding_goal | `GoalBlocker` frozen kw_only |
| 449 | `vault.sub_kinds.funding_goal.canonical_codec.v1` | interface-contract | funding_goal | `to_canonical_bytes` / `from_canonical_bytes` codec pair (LIVE at v0.2) |
| 450 | `vault.sub_kinds.funding_goal.resolve_live.v1` | interface-contract | funding_goal | thin status-resolution helper per OQ-5 (LIVE at v0.2) |
| 451 | `vault.sub_kinds.registry.funding_goal_descriptor.v1` | interface-contract | funding_goal | `SUB_KIND_REGISTRY["funding_goal"]` row per §2.12 |
| 452 | `vault.policy.operational_subkinds.cedar.goal_status_transition.v1` | interface-contract | funding_goal | Cedar rule per §7 |
| 453 | `vault.policy.operational_subkinds.cedar.goal_priority_mutation_audited.v1` | interface-contract | funding_goal | Cedar rule per §7 |
| 454 | `vault.policy.operational_subkinds.cedar.goal_taxonomy_closed.v1` | interface-contract | funding_goal | Cedar rule per §7 |
| 455 | `vault.post_gate_allowlist.operational-funding-goal-write.v1` | interface-contract | funding_goal | §2.13 allowlist row |
| 456 | `vault.layout.org_vault_operational_funding_goals.v1` | interface-contract | funding_goal | `VaultLayout.org_vault_operational_funding_goals(slug)` |
| 457 | `logician.failure_code.F-FG-CROSS-ORG-LEAK.v1` | failure-code | funding_goal | per §6 |
| 458 | `logician.failure_code.F-FG-SCHEMA-INVALID.v1` | failure-code | funding_goal | per §6 (umbrella w/ sub-tags) |
| 459 | `logician.failure_code.F-FG-CIC-TAG-INVALID.v1` | failure-code | funding_goal | per §6 (sub-code under umbrella) |
| 460 | `logician.failure_code.F-FG-CLC-TAG-INVALID.v1` | failure-code | funding_goal | per §6 (sub-code under umbrella) |
| 461 | `logician.failure_code.F-FG-STATUS-TRANSITION-INVALID.v1` | failure-code | funding_goal | per §6 |
| 462 | `logician.failure_code.F-FG-LINKED-CYCLE-ORPHAN.v1` | failure-code | funding_goal | per §6 |
| 463 | `logician.failure_code.F-FG-PRIORITY-MUTATION-UNAUDITED.v1` | failure-code | funding_goal | per §6 |
| 464 | `logician.failure_code.F-FG-DEADLINE-EXPIRED-IGNORED.v1` | failure-code | funding_goal | per §6 |
| 465 | `linting.r_fg_no_float_monetary.v1` | ast-lint | funding_goal | AST-lint rule under `ast-lint` kind (vocabulary landed at §0.5 v19 row 208 §A.AST_LINT). Scope: `pipeline/vault/sub_kinds/funding_goals.py` + `pipeline/match_db/scoring.py` + `pipeline/match_db/` per RT-13. |
| 466 | `scout.discover.input_shape.funding_goals_block.v1` | interface-contract | funding_goal | §3 v6 — DISCOVER goals-block injection + slug validation per RT-01 |
| 467 | `scout.discover.fit_score_cached.goal_aware_composer.v1` | interface-contract | funding_goal | §3.3 — additive composition per RT-17 |
| 468 | `match_db.scoring.goal_aware_match_score.v1` | interface-contract | funding_goal | §4.3 — Decimal-mandate composition callable; OQ-7 routed under interface-contract (per convention of parenting new logic primitives in the primary logic amendment for a compound lock per Judge J-02 closure) |

**Row range: 446-468 (23 rows). Runtime-live total at compound LOCK: 468.**

**§8.1 Parent-wins discipline (E-05 closure).** Each row's `parent_lock_version` + `parent_lock_commit_hash` resolve at LOCK ceremony to the actual sibling commit hash:
- Rows 446-456 → §2 v7.5 commit hash
- Rows 457-465 → §4 v2.x.4 commit hash
- Rows 466-467 → §3 v6 commit hash
- Row 468 → §4 v2.x.4 commit hash (per Judge J-02 convention: new logic primitives parent under the primary logic amendment for a compound lock)

**§8.2 seat_owner attribute (RT-19 fold-in).** Every row in this amendment carries `seat_owner: "funding_goal"`. F-INDEX-STALE PRE-gate at compound commit verifies seat_owner consistency across all 23 rows. Mirrors §17 WPFA §0.5 v19 §5 closed-set-membership pattern.

**§0.5 vocabulary check:** every row resolves against the v5 + v6 + v19 closed vocabulary (marker / schema / interface-contract / failure-code / pre-gate-check / post-gate-check / ast-lint). NO further vocabulary extension required.

# §9. L-005 two-cycle Thesis discipline notes (Cycle 2 ready)

Per `/AGENTS.md` § "Cross-family review — bridge pattern". Cycle 1 closed per `cycle_1_disposition.md`. **Cycle 2 verification dispatch is the next step.**

## §9.1 HARD-LOCKED elements (Thesis Cycle 2 cannot relitigate)

All v2 hard-locked elements PLUS:
- Cycle 1 P0 + HIGH closures listed in §0.3 (text-level mechanism specifications for path validation, regex, fail-closed defaults, AST-lint scope, ledger consultation, per-org scoping).
- F-FG-LINKED-CYCLE-ORPHAN severity upgrade to HIGH (was MEDIUM at v2; upgrade per RT-23 P0 sub-tag).
- LIVE/STUB primitive table at §2.3 distinguishing v0.2 LIVE plumbing from STUB-RAISE Logician gate predicates.

## §9.2 OPEN QUESTIONS for Cycle 2 dispatch

Cycle 2 verifies Cycle 1 closures are correctly absorbed AND surfaces any NEW probes per row-170 transparent disposition pattern. Specifically:

- (Why-it-matters: closure verification) Are all 35 FOLD-IN closures correctly absorbed in v3 text? Re-scan §2/§3/§4/§5/§6/§7/§8 against `cycle_1_disposition.md` table.
- (Why-it-matters: regression test) Is the F-CIC-CLC-COUPLING-VIOLATION regression test scope correctly extended to cover the new Cedar rules + composer + slot-naming? (RT-04/05/06/12)
- (Why-it-matters: bounded-by-A1+A4 disposition) Is the RT-10 cache-invalidation BOUNDED disposition consistent with WPFA RT-04/RT-05 BOUNDED precedent (row 207)? Is the v0.2-known-limitation language clear?
- (Why-it-matters: orphan-check P0) Does F-FG-LINKED-CYCLE-ORPHAN's `.cross_org_grant_reference` sub-tag (RT-23) correctly inherit Law 3 P0 severity even though the parent code is MEDIUM/HIGH-advisory? Should the parent code be upgraded to P0 or stay HIGH with the sub-tag carrying P0?
- (Why-it-matters: AST-lint scope) Is the R-FG-NO-FLOAT-MONETARY scope extension to `pipeline/match_db/` consistent with WPFA R-WPFA-DECIMAL-MANDATE-ENERGY scope-extension precedent (RT-C2-01 row 207)?
- NEW probes per row-170 transparent disposition pattern: surface any new attack paths Cycle 2 reviewers identify in the Cycle 1 closures themselves (defense-in-depth check).

# §10. v0.2 vs v1.x boundary table (with closures)

Same as v2 §10 PLUS:
- **RT-10 cache-invalidation latency** — v0.2 known-limitation; v1.x per-cycle invalidation hook; v2 real-time per Section O.5.
- **RT-06 CIC/CLC asset signing** — v0.2 operator-pinned at white-glove (A4 trusted); v1.x SN-LLC Ed25519 signing + verification.
- **RT-18 Cedar pair-blacklist** — v1.x feature; not needed at v0.2 SPEC LOCK (no pre-mapping mandate per CLAUDE.md).
- **F-FG-* gate predicate bodies** — STUB-RAISE NotImplementedError at v0.2; LIVE bodies at v1.x amendment per §15 v1 SPEC-ONLY precedent.

# §11. Pre-Cycle-2-dispatch checklist (self-check)

- [x] All 37 Cycle 1 dispositions absorbed per `cycle_1_disposition.md`.
- [x] LIVE/STUB primitive table at §2.3 added.
- [x] §3.1 slug validation + O_NOFOLLOW added (RT-01/02).
- [x] §2.2 invariant 1 record_id regex + invariant 12 future-timestamp added (RT-03/09).
- [x] §3.2 per-grant SP0 propagation + numeric opaque slot enforcement added (RT-11/12).
- [x] §3.2 RT-10 BOUNDED-by-A1+A4 disposition explicit (cache invalidation).
- [x] §3.3 additive bonus clarification (RT-17).
- [x] §4.1 YAML float-literal fix (J-01) + RT-14/RT-16 fold-in.
- [x] §4.2 explicit Decimal cast (RT-15).
- [x] §5.1 per-org isolation enforcement (RT-25/26).
- [x] §5.3 UNALLOCATED admin-only rename (RT-27).
- [x] §6 F-FG-* gate sub-tags extended (RT-04/05/07/08/09/12/14/23/24).
- [x] §6 F-FG-LINKED-CYCLE-ORPHAN severity upgraded HIGH; cross-org sub-tag NO M13 bypass.
- [x] §6 Cedar engine fail-closed CriticalPolicyError contract (RT-05).
- [x] §7 engine-bound principal (RT-04) + asset signing (RT-06 BOUNDED-by-A1+A4).
- [x] §8 seat_owner attribute on every row (RT-19).
- [x] §8 Judge J-02 row 468 parenting comment.
- [x] §8.1 parent-wins discipline sub-paragraph (E-05).
- [x] §6 umbrella module pattern note (E-07).
- [x] §9.2 OQ relevance annotations (E-08).
- [x] §0.1-§0.3 changelog summarizes 8 + 2 + 27 closures across 35 FOLD-IN + 1 BOUNDED + 1 DEFERRED.
- [x] No Python written (still SPEC).
- [x] No LOCK ceremony invoked.
- [x] Path-only references per L-002.

# §12. Changelog

- 2026-05-10 v1 DISPATCH_SPEC_DRAFT filed.
- 2026-05-11 v2 DISPATCH_SPEC_READY (operator decisions absorbed; F-GOAL-* → F-FG-*; row range 446-468 against runtime-live=445).
- 2026-05-11 v3 DISPATCH_SPEC_CYCLE_2_READY (this file). Cycle 1 closures absorbed (35 FOLD-IN + 1 BOUNDED + 1 DEFERRED across Editor 8 + Judge 2 + Red Team 27 findings). Ready for L-005 Cycle 2 verification dispatch.
