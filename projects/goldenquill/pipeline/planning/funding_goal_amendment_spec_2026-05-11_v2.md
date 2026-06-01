---
title: Funding-Goal Sub-Kind — Dispatch Spec Card v2 (operator-decisions absorbed; ready-for-Thesis)
filed: 2026-05-11
operator: Josh Inklovich
supersedes: pipeline/planning/funding_goal_amendment_spec_2026-05-10.md (v1 DISPATCH_SPEC_DRAFT)
status: DISPATCH_SPEC_READY — operator OQ-1 pinned + 11 default-OQs absorbed + Path B naming applied (F-FG-*). L-005 strict two-cycle Thesis (Editor=Llama/Groq + Judge=Gemini/Google + Red Team=GPT-OSS/Groq via openclaw bridge) is the next gate. SPEC-ONLY at v0.2, mirrors §13/§14/§15 SPEC-ONLY discipline; predicate bodies skeleton stubs raising NotImplementedError at v0.2 first ship; v1.x Code-phase realization deferred per §15 v1 SPEC-ONLY precedent.
parent_locks:
  - pipeline/blueprint/v0.1/section_02_vault_topology.md                                # v7.1 LOCKED 2026-04-19 (§2 LOCKED-as-a-whole 2026-04-22)
  - pipeline/blueprint/v0.1/section_02_v7_2_amendment.md                                # §2 v7.2 LOCKED 2026-05-10 — Operational-data sub-kinds; sub-kind registry; cross-product Cedar matrix
  - pipeline/blueprint/v0.1/section_02_v7_4_coefficient_registry_amendment.md           # §2 v7.4 LOCKED 2026-05-11 row 206 — Coefficient Registry signed-asset class (mirrored discipline for FundingGoal sub-kind registration)
  - pipeline/blueprint/v0.1/section_06_operating_envelope.md                            # §6 v1-r1 LOCKED 2026-04-21 — host for prompt-compilation, track-registry, SFR; consumed (not amended) by this spec
  - pipeline/blueprint/v0.1/section_03_scout.md                                         # §3 v5 LOCKED 2026-04-17 — DISCOVER channels A–F; (channel G added at architecture v7.0.5)
  - pipeline/architecture/v0.1/architecture_v7_0_5_amendment.md                         # v7.0.5 LOCKED 2026-05-10 row 179 — Funder Intelligence DB + Match DB + Scout channel G + Stage-5 consent-tier on-ramp
  - pipeline/blueprint/v0.1/section_04_v2_x_amendment.md                                # §4 v2.x LOCKED 2026-05-10 rows 193/194 — F-CLASS-* dormant primitives + KFR residuals + v7.0.4-M1 corrective predicates
  - pipeline/blueprint/v0.1/section_04_v2_x_1_amendment.md                              # §4 v2.x.1 LOCKED 2026-05-10 row 199 — narrow corrective with R-ARCHIVIST-NO-CANONICAL-MUTATE sub-tag extension
  - pipeline/blueprint/v0.1/section_04_logician_v2_x_2_amendment.md                     # §4 v2.x.2 LOCKED 2026-05-10 row 203 (paired with arch v7.0.9) — F-REFLECTION-* sub-tag-extension family
  - pipeline/blueprint/v0.1/section_04_v2_x_z_wpfa_amendment.md                         # §4 v2.x.z LOCKED 2026-05-11 row 207 — F-WPFA-* family with LIVE bodies
  - pipeline/blueprint/v0.1/section_00_5_section_17_wpfa_amendment.md                   # §0.5 v19 LOCKED 2026-05-11 row 208 — runtime-live total row 445
  - pipeline/blueprint/v0.1/section_11_intake.md                                        # §11 v1 LOCKED 2026-05-10 row 185 — AWARD_INGEST mode (proposal_commitments.yaml)
  - pipeline/blueprint/v0.1/section_14_report_generator.md                              # §14 v1 LOCKED 2026-05-10 — TRACK in §5 v8 report_mode; FundingGoal feeds report narrative + claim_evidence_map at v0.2 first ship
  - pipeline/blueprint/v0.1/section_15_archivist.md                                     # §15 v1 SPEC-LOCKED 2026-05-10 rows 191/192 — SPEC-ONLY at v0.2 precedent for this Funding Goal SPEC LOCK
  - pipeline/architecture/v0.1/tilth_architecture_locked.md                             # v7 LOCKED 2026-04-19 A1–A12; A12 Decimal mandate; A1 single-client v0.1 threat model; A4 operator-trusted preflight
  - pipeline/architecture/v0.1/architecture_v7_0_4_M1_amendment.md                      # v7.0.4-M1 LOCKED 2026-05-10 row 190 — Decimal-mandate three-layer ban-float; canonicalization regime; atomic-read fcntl.flock; symlink rejection
  - pipeline/architecture/v0.1/architecture_v7_0_7_amendment.md                         # v7.0.7 LOCKED 2026-05-10 row 180 — Beta classification-driven routing + Classification Review stage + 12 F-CLASS-* primitives
  - pipeline/architecture/v0.1/architecture_v7_0_9_amendment.md                         # v7.0.9 LOCKED 2026-05-10 row 202 — Reflection v0.1 Beta hook (architectural posture for cycle-close artifacts FundingGoal coexists with via §14 read-substrate)
  - pipeline/planning/f_reflection_f_wpfa_naming_reconciliation_2026-05-10.md           # Naming reconciliation pass: Path B applied preemptively (F-FG-* family chosen over F-GOAL-*; no cross-pollination with F-WPFA-/F-REFLECTION-/F-PACKET-)
authority: orchestrator dispatch 2026-05-11 — operator pinned OQ-1 = v0.2 alongside §14 Report Generator (mirrors §13/§14/§15 v0.2 SPEC-ONLY discipline; explicitly NOT spec-default "v0.2 first wave")
purpose: Stage a SPEC for the FundingGoal sub-kind so the L-005 two-cycle Thesis (FULL live cross-family rigor; no Section E carve-out) audits and LOCKs it as a v0.2 horizon SPEC. Predicate bodies remain skeleton stubs raising NotImplementedError per §15 v1 SPEC-ONLY precedent; v1.x Code-phase realization deferred.
dispatch_class: spec_card_for_blueprint_amendment_family
ws_dispatch_target: WS-FG Funding Goal — provisional workstream name, will be filed against `pipeline/planning/v0_2_dispatch_plan_2026-05-09.md` at LOCK ceremony.
review_discipline: L-005 strict two-cycle, FULL live cross-family per /AGENTS.md (Editor=Llama 3.3 70B/Groq Meta family + Judge=Gemini 2.5 Pro/Google + Red Team=GPT-OSS 120B/Groq OpenAI-OSS family) — no Section E carve-out. Mirrors the rigor level applied to §2 v7.2, §11 v1, §12 v1, §13 v1, §14 v1, §15 v1 SPEC, §17 v1, §4 v2.x, §4 v2.x.1, §4 v2.x.2, §4 v2.x.z, Reflection v0.1 hook.
naming_reconciliation_status: Path B applied preemptively. F-GOAL-* (v1 spec) → F-FG-* (this v2). No textual collision with F-WPFA-*, F-REFLECTION-*, F-PACKET-* families exists today; rename is preemptive per `pipeline/planning/f_reflection_f_wpfa_naming_reconciliation_2026-05-10.md` §3 Path B principle ("each family has a single seat-owner; minimizes downstream-consumer confusion") + matches the WS-FG dispatch-target abbreviation.
---

# §0. Operator decisions absorbed into this v2 (changelog summary)

Reflects the operator-pinned OQ-1 + the eleven default-OQs from `pipeline/planning/operator_spec_card_status_2026-05-10.md` §1.

| OQ | Operator-pinned answer | Source |
|----|------------------------|--------|
| **OQ-1 — Ship window** | **v0.2 alongside §14 Report Generator (NOT spec-default v0.2 first wave).** FundingGoal feeds report narrative + the proposal_commitments.yaml extraction path from §11 AWARD_INGEST. Structurally a v0.2 SPEC-LOCK artifact. | Operator dispatch 2026-05-11 |
| OQ-2 — §6 vs §3 amendment shape | **Both, paired.** §3 v6 owns the DISCOVER input-shape; new §6.x amendment owns the prompt-compilation goals-block injection. | Discovery report default |
| OQ-3 — Past-deadline at construction | **Reject.** Mirrors v7.2 lex-compare discipline (`ended_at > started_at`). | Discovery report default |
| OQ-4 — RED severity on blocked goals | **RED.** Blocked goal IS a per-cycle operator decision surface. | Discovery report default |
| OQ-5 — Status mutation helper | **Thin helper (`funding_goals.resolve_live(...)`).** | Discovery report default |
| OQ-6 — `purpose` default classification | **`shareable`** (Card-level archetype default; per-org/per-grant override per v7.0.7 §3.6 three-layer pattern). | Discovery report default |
| OQ-7 — `scoring-callable` primitive_kind | **Route under `interface-contract`** (minimum-vocabulary-extension discipline). | Discovery report default |
| OQ-8 — Status transition closure | **As proposed in §6** (`met → pursuing` forbidden; `abandoned → pursuing` permitted; rest permitted). | Discovery report default |
| OQ-9 — F-FG-SCHEMA-INVALID family collapse | **Sub-code collapse** (matches §4 v2.x F-CLASS-* / v2.2 F-AMDT-* precedent). Five modules realize eight codes. | Discovery report default |
| OQ-10 — F-FG-* in F-CLASS-COVERAGE-INCOMPLETE META | **Exclude.** F-FG-* is its own family with its own coverage discipline; META gate stays focused on F-CLASS-* per its current contract. Mirrors WPFA F-WPFA-* exclusion at row 207. | Discovery report default |
| OQ-11 — Match DB v1→v2 schema bump | **Schema-of-record only** (no migration shim; documentary note: "no v1 registers existed on disk at the time of v2 LOCK"). | Discovery report default |
| OQ-12 — Push-notify v0.1 surface | **D + A only** (CLI-on-next-run + Monday-brief integration). B+C deferred to v0.2 candidates. **Note:** since OQ-1 = v0.2, even D+A surface as v0.2 first-ship rather than v0.1. | Discovery report default |

**Naming swap.** All `F-GOAL-*` references in v1 → `F-FG-*` in this v2. Justification: preemptive Path B per `pipeline/planning/f_reflection_f_wpfa_naming_reconciliation_2026-05-10.md` §3 + closes generic-prefix ambiguity. Eight code names:
- `F-FG-CROSS-ORG-LEAK`
- `F-FG-SCHEMA-INVALID`
- `F-FG-CIC-TAG-INVALID`
- `F-FG-CLC-TAG-INVALID`
- `F-FG-STATUS-TRANSITION-INVALID`
- `F-FG-LINKED-CYCLE-ORPHAN`
- `F-FG-PRIORITY-MUTATION-UNAUDITED`
- `F-FG-DEADLINE-EXPIRED-IGNORED`

**Row range re-allocation.** v1 spec card was authored against runtime-live = 376; rows 377-399 reserved. Today's runtime-live = **445** (post §17 WPFA + §0.5 v19 LOCK row 208). **This compound LOCK allocates rows 446 onward.**

# §1. Compound-LOCK pairing identity

Following the WS-J §14 + §0.5 v17 (rows 200/201) and WS-WPFA §17 v1 + §2 v7.4 + §4 v2.x.z + §0.5 v19 (rows 205-208) precedents, this is a **compound-LOCK across four siblings**, atomically committed at the same `lock_timestamp_utc`:

| Sibling | What lands | Lock_history row (anticipated) |
|---|---|---|
| §2 v7.5 (`section_02_v7_5_funding_goal_amendment.md`) | New SIMPLE sub-kind row `funding_goal` in §2.13 POST_GATE_ALLOWLIST; new `FundingGoal` + `GoalBlocker` frozen-dataclass schemas at §2.11.8; new Cedar rules in `operational_subkinds.cedar`; new vault subtree `operational/funding_goals/` | 209 |
| §3 v6 (`section_03_v6_funding_goal_amendment.md`) + §6.x amendment (`section_06_funding_goal_amendment.md`) | §3 owns DISCOVER input-shape extension; §6 owns prompt-template goals-block injection | 210 |
| §4 v2.x.4 (`section_04_v2_x_4_funding_goal_amendment.md`) | F-FG-* failure-code family registered (8 codes / 5 modules per OQ-9 collapse); SPEC-ONLY at v0.2 (predicate bodies skeleton stubs raising NotImplementedError, mirrors §15 v1 SPEC-ONLY precedent) | 211 |
| §0.5 v20 amendment (`section_00_5_section_funding_goal_amendment.md`) | Row append starting at 446; sub-kind row + schema rows + Cedar policy rows + failure-code rows + Scout DISCOVER interface-contract row + Match-DB scoring-callable row + Monday-fund-radar consumer row | 212 |

Compound transaction discipline per §6.17 Option-B + WS-J §14 + WS-WPFA §17 precedents: all four sibling rows enter `lock_history.v1.jsonl` at the same `lock_timestamp_utc`. F-INDEX-STALE PRE-gate fires at commit time; all new §0.5 rows must be present in the index or the compound commit fails closed.

# §2. Pydantic dataclass shape — `FundingGoal` (proposed §2.11.8)

Following the §2 v7.2 sub-kind convention EXACTLY: `@dataclass(frozen=True, kw_only=True)`; one record = one file; SIMPLE class; `write-if-absent` mode; `__post_init__` invariant validation; canonical-JSON encode/decode round-trip; module at `pipeline/vault/sub_kinds/funding_goals.py`; tests at `tests/vault/sub_kinds/test_funding_goals.py`. **At v0.2 SPEC LOCK, the module is a skeleton with the dataclass definitions present + invariants enforced + canonical codec implemented; the Logician gate predicates raise NotImplementedError per §15 v1 SPEC-ONLY precedent.**

```python
@dataclass(frozen=True, kw_only=True)
class FundingGoal:
    record_id: str                          # opaque caller-minted ID; matches filename {record_id}.json
    goal_name: str                          # operator-facing label, e.g. "Regional Food Hub Buildout"
    target_amount_minor_units: int          # smallest currency unit (cents); A12 Decimal-mandate via dedicated decoder helper
    currency: str                           # ISO-4217 alpha-3 (e.g., "USD")
    target_deadline: str                    # UTC ISO-8601 date 'YYYY-MM-DD'; v7.2 'Z' convention does NOT apply (date not datetime)
    purpose: str                            # free-form purpose statement (operator-discipline; no content validation per §2 v7.2 boundary)
    cic_tag: str                            # one of the six CIC slugs per CLAUDE.md
    clc_tags: tuple[str, ...]               # ZERO OR MORE of the eight CLC slugs; lex-sorted; CIC × CLC orthogonality preserved per v7.0.8
    status: str                             # "pursuing" | "blocked" | "met" | "abandoned"
    blockers: tuple[GoalBlocker, ...]       # structured blocker rows; non-empty REQUIRED iff status == "blocked"
    linked_cycle_ids: tuple[str, ...]       # grant_id strings under orgs/{slug}/vault/grants/{grant_id}/; lex-sorted
    priority_weight: int                    # 0..100 (operator-set); higher = more weight in Match-DB scoring
    created_at: str                         # UTC ISO-8601 'Z'
    last_status_change_at: str              # UTC ISO-8601 'Z'; equals created_at at construction; mutates only via re-key path


@dataclass(frozen=True, kw_only=True)
class GoalBlocker:
    blocker_kind: str                       # "rejection" | "capacity" | "timing" | "scope_change" | "external_constraint" | "other"
    summary: str                            # one-line blocker summary
    surfaced_at: str                        # UTC ISO-8601 'Z'
    surfaced_by_grant_id: str | None        # grant_id if surfaced from cycle outcome
    surfaced_by_match_id: str | None        # match_id if surfaced from Match DB analysis
    resolution_hint: str                    # operator-supplied hint; may be empty
```

## §2.1 A12 Decimal mandate dispatch

Per architecture v7.0.4-M1 §6, Decimal mandate is three-layer (AST-lint ban on `float` for monetary fields + dedicated decoder helper + explicit-context-required helper). `target_amount_minor_units` is `int` (smallest currency unit) — matches §2.11.2 `FinancialsRecord.amount_minor_units` exactly. The decoder helper `from_canonical_bytes` MUST re-validate that the JSON-parsed value is `int` and not float; tampered records fail-close on `F-FG-SCHEMA-INVALID.float_target_amount_detected`. **No `float` field in `FundingGoal` or `GoalBlocker`.** AST-lint R-FG-NO-FLOAT-MONETARY rule (mirrors WPFA's R-WPFA-DECIMAL-MANDATE-ENERGY pattern at row 444); registered in `pipeline/linting/r_fg_no_float_monetary.py` at v0.2 first-ship + AST-lint row at §0.5 v20 (under `ast-lint` kind, the vocabulary extension landed at row 208 §0.5 v19 §A.AST_LINT).

## §2.2 Invariants (`__post_init__` — fail-close at write AND at decode round-trip)

Thirteen invariants — see v1 spec card §2.2 (1-13) — apply byte-identically. The only delta from v1: failure codes are F-FG-* not F-GOAL-*.

## §2.3 Sub-kind registry row (§2.12 amendment)

```python
"funding_goal": SubKindDescriptor(
    intent="operational-funding-goal-write",
    vault_subtree="operational/funding_goals/",
    record_class=FundingGoal,
    to_canonical_bytes=funding_goals.to_canonical_bytes,
    from_canonical_bytes=funding_goals.from_canonical_bytes,
    record_id_for=funding_goals.record_id_for,
    severity_default="YELLOW",
    severity_for=lambda record: "RED" if record.status == "blocked" else "YELLOW",  # OQ-4 RED-on-blocked locked
),
```

## §2.4 Admin-risk severity

Default YELLOW (multi-cycle persistent operator intent). RED when `status == "blocked"` per OQ-4. Surface in admin-risk ledger every cycle.

## §2.5 Status mutation discipline + thin resolution helper (OQ-5 locked)

Per §2 v7.2 §1, in-place mutation impossible (`write-if-absent` everywhere). Status changes follow the v7.2 worked operator re-key path (1 mint fresh record_id → 2 write updated record → 3 append admin-risk-ledger entry → 4 original persists; ledger entry is disambiguator).

**Thin helper (OQ-5 locked):** `funding_goals.resolve_live(record_id_set: set[str], admin_risk_ledger: AdminRiskLedger) -> FundingGoal` — single-place resolution helper at `pipeline/vault/sub_kinds/funding_goals.py`. Walks ledger to find latest live record_id for a logical goal. Used by Scout REVIEW + Match DB scoring + Monday brief — eliminates seat-side walk drift.

**Forbidden transitions (OQ-8 locked):** `met → pursuing` (a met goal cannot be reactivated; operator must mint a NEW goal). All other transitions permitted with admin-risk-ledger entry.

# §3. §6 Scout DISCOVER + §6 prompt-compilation integration (OQ-2 locked: both, paired)

## §3.1 §3 v6 amendment — DISCOVER input-shape

`Scout.session_call()` adds optional `funding_goals: tuple[FundingGoal, ...]` parameter, read at session start from `orgs/{slug}/vault/operational/funding_goals/` filtering `status in {"pursuing", "blocked"}`. Channel A-G dispatch unchanged; goals modulate post-channel ranking only.

## §3.2 §6 prompt-compilation goals-block injection

§6.11 prompt-template compilation pipeline gains a goals-block injected at start-block + end-block (per A4 architectural FLOOR; F-CONTEXT-PLACEMENT PRE-gate already enforces; goals-block joins the existing four load-bearing markers).

**Classification-aware redaction (OQ-6 locked: shareable default).** Cloud-routed seats (Channel F web search if BYOK provider is cloud-shaped) receive goals-block with `purpose` field rendered verbatim by default. Operator override via per-org classification register (v7.0.7 §3.6 three-layer defaults) flips `purpose` to `confidential` → opaque-slot-filled per F-CLASS-SLOT-ID-NON-OPAQUE PRE-gate.

## §3.3 `fit_score_cached` composition (deterministic Python; zero LLM)

Bonus `[0, +25]` per active goal whose `cic_tag` matches candidate AND `clc_tags` overlap is non-empty. Goal's `priority_weight` weights the bonus. Combined score clamped `[0, 100]`. Decimal arithmetic per v7.0.4-M1 §6.

## §3.4 CIC × CLC orthogonality preservation

`cic_tag` single-valued + `clc_tags` zero-or-more, treated as **independent dimensions** in score composition. F-CIC-CLC-COUPLING-VIOLATION (v7.0.8 PRE-gate) MUST regress-test against the goal-schema at LOCK against the four detection layers (lexical regex / Pydantic AST / value-set / KP schema).

# §4. Match DB v1→v2 (OQ-11 locked: schema-of-record only)

## §4.1 Schema additions to `match_database.v2`

Two new fields per match row:

```yaml
contributes_to_goals:
  - goal_record_id: <FundingGoal.record_id>
    estimated_contribution_minor_units: <int>
    estimated_contribution_confidence: <"low" | "medium" | "high">
goal_aware_match_score: <0.0 - 1.0>
```

## §4.2 Goal-aware match score composition (Decimal-mandated)

Per v1 spec card §4.2 — applied byte-identically. `confidence_factor` literals are `Decimal("0.5") / Decimal("0.75") / Decimal("1.0")` (AST-lint ban on float literals enforces). `GOAL_BONUS_WEIGHT = Decimal("0.25")`, operator-tunable. Final score rounded `Decimal('0.0001')` ROUND_HALF_EVEN.

## §4.3 Scoring callable

Module `pipeline/match_db/scoring.py` (NEW). Function `goal_aware_match_score(match: MatchRow, active_goals: Mapping[str, FundingGoal]) → Decimal`. **§0.5 row registered as `interface-contract` per OQ-7** (NOT new `scoring-callable` primitive_kind — minimum-vocabulary-extension discipline).

## §4.4 No migration shim (OQ-11 locked)

v0.1 has zero `match_database.v1` registers on disk; schema-of-record only. Documentary note in §4.1 amendment: "no v1 registers existed on disk at the time of v2 LOCK; future schema bumps from v2 onward MAY require a migration shim per v7.0.4-M1 §2 legacy-migration discipline."

# §5. Push-notify wiring (OQ-12 locked: D + A only at v0.2 first ship; B + C as v0.2 candidates)

Per v1 spec card §5 — applied byte-identically with the OQ-1 v0.2-shift correction. Since FundingGoal lands at v0.2 (not v0.1 Beta), even D+A surface is v0.2 first-ship rather than v0.1. Cultivator-based Telegram option becomes the natural v0.2 second-wave home (per §13 v1 OrgScopedBot @final wrapper).

# §6. F-FG-* failure-code family (§4 v2.x.4 amendment seed; SPEC-ONLY at v0.2)

Per OQ-9 sub-code collapse (locked): **eight codes / five modules**. Predicate bodies skeleton stubs raising `NotImplementedError` at v0.2 first ship per §15 v1 SPEC-ONLY precedent; v1.x Code-phase realization deferred.

| Code | Tier | Module (proposed) | Severity | Sub-tags / Trigger |
|---|---|---|---|---|
| `F-FG-CROSS-ORG-LEAK` | PRE | `f_fg_cross_org_leak.py` | P0 (Law 3) | Read whose path resolves outside `orgs/<this_slug>/vault/operational/funding_goals/`. Mirrors `F-MATCH-DB-CROSS-ORG`. **No M13 bypass.** |
| `F-FG-SCHEMA-INVALID` | PRE-write + POST-read | `f_fg_schema_validation.py` (UMBRELLA — collapses three codes per OQ-9) | HIGH | Sub-tags `.float_target_amount_detected`, `.invariant_<n>_violated`, `.canonical_round_trip_drift`. M13 audited. |
| `F-FG-CIC-TAG-INVALID` | PRE-write | `f_fg_schema_validation.py` (sub-code under umbrella) | HIGH | `cic_tag` not in six-CIC closed set per CLAUDE.md. M13 audited. |
| `F-FG-CLC-TAG-INVALID` | PRE-write | `f_fg_schema_validation.py` (sub-code under umbrella) | HIGH | Any element of `clc_tags` not in eight-CLC closed set. M13 audited. |
| `F-FG-STATUS-TRANSITION-INVALID` | PRE-write | `f_fg_status_transition_invalid.py` | HIGH | New record carries forbidden transition (`met → pursuing`). M13 audited. |
| `F-FG-LINKED-CYCLE-ORPHAN` | POST-read + PRE-cycle-start | `f_fg_linked_cycle_orphan.py` | MEDIUM | `linked_cycle_ids` element does not resolve to live grant. M13 audited. |
| `F-FG-PRIORITY-MUTATION-UNAUDITED` | PRE-write | `f_fg_priority_mutation_unaudited.py` | MEDIUM | Priority changed without admin-risk-ledger entry. M13 audited. |
| `F-FG-DEADLINE-EXPIRED-IGNORED` | POST-read | `f_fg_deadline_expired_ignored.py` | MEDIUM (advisory) | Deadline past + status pursuing + no mutation in operator-set window (default 30d). M13 NOT needed. |

**Module count after collapse: 5 modules realizing 8 codes** (one umbrella `f_fg_schema_validation.py` realizing F-FG-SCHEMA-INVALID + F-FG-CIC-TAG-INVALID + F-FG-CLC-TAG-INVALID; four singletons).

**META gate exclusion (OQ-10 locked):** F-FG-* family does NOT register in F-CLASS-COVERAGE-INCOMPLETE's `REQUIRED_F_CLASS_CODES`. Documentary note in §4 v2.x.4 amendment §X: "F-FG-* is its own family with its own coverage discipline; META gate stays focused on F-CLASS-* per its current contract. Mirrors §17 WPFA F-WPFA-* exclusion at row 207."

**PRE/POST gate row allocation:** PRE-67 onward / POST-27 onward (re-allocate at LOCK ceremony after WS-L follow-on amendments land).

# §7. Cedar policy additions

Three new rules + one extension to `pipeline/vault/policies/operational_subkinds.cedar`:

1. **Extension to `operational_org_isolation`:** add `sub_kind == "funding_goal"` to default-permit set. F-FG-CROSS-ORG-LEAK at the Logician layer is defense-in-depth.
2. **`goal_status_transition`:** permits goal writes only when transition is permitted per §6 + admin-risk-ledger entry signed.
3. **`goal_priority_mutation_audited`:** permits goal writes whose `priority_weight` differs from prior live only when admin-risk-ledger entry captures mutation reason.
4. **`goal_taxonomy_closed`:** permits goal writes only when `cic_tag` ∈ six-CIC AND every element of `clc_tags` ∈ eight-CLC.

# §8. §0.5 v20 amendment — row range allocation (rows 446-468)

Current runtime-live total at §17 WPFA + §0.5 v19 LOCK 2026-05-11 = **445** rows. **Funding Goal compound LOCK allocates rows 446-468 (23 rows).**

| Row | primitive_id | kind | parent |
|---|---|---|---|
| 446 | `blueprint.section_anchor.s02_v7_5_funding_goal.v1` | marker | §2 v7.5 |
| 447 | `vault.sub_kinds.funding_goal.v1` | schema | `FundingGoal` frozen kw_only |
| 448 | `vault.sub_kinds.funding_goal.goal_blocker.v1` | schema | `GoalBlocker` frozen kw_only |
| 449 | `vault.sub_kinds.funding_goal.canonical_codec.v1` | interface-contract | `to_canonical_bytes` / `from_canonical_bytes` codec pair |
| 450 | `vault.sub_kinds.funding_goal.resolve_live.v1` | interface-contract | thin status-resolution helper per OQ-5 |
| 451 | `vault.sub_kinds.registry.funding_goal_descriptor.v1` | interface-contract | `SUB_KIND_REGISTRY["funding_goal"]` row per §2.12 |
| 452 | `vault.policy.operational_subkinds.cedar.goal_status_transition.v1` | interface-contract | Cedar rule per §7 |
| 453 | `vault.policy.operational_subkinds.cedar.goal_priority_mutation_audited.v1` | interface-contract | Cedar rule per §7 |
| 454 | `vault.policy.operational_subkinds.cedar.goal_taxonomy_closed.v1` | interface-contract | Cedar rule per §7 |
| 455 | `vault.post_gate_allowlist.operational-funding-goal-write.v1` | interface-contract | §2.13 allowlist row |
| 456 | `vault.layout.org_vault_operational_funding_goals.v1` | interface-contract | `VaultLayout.org_vault_operational_funding_goals(slug)` |
| 457 | `logician.failure_code.F-FG-CROSS-ORG-LEAK.v1` | failure-code | per §6 |
| 458 | `logician.failure_code.F-FG-SCHEMA-INVALID.v1` | failure-code | per §6 (umbrella w/ sub-tags) |
| 459 | `logician.failure_code.F-FG-CIC-TAG-INVALID.v1` | failure-code | per §6 (sub-code under umbrella module) |
| 460 | `logician.failure_code.F-FG-CLC-TAG-INVALID.v1` | failure-code | per §6 (sub-code under umbrella module) |
| 461 | `logician.failure_code.F-FG-STATUS-TRANSITION-INVALID.v1` | failure-code | per §6 |
| 462 | `logician.failure_code.F-FG-LINKED-CYCLE-ORPHAN.v1` | failure-code | per §6 |
| 463 | `logician.failure_code.F-FG-PRIORITY-MUTATION-UNAUDITED.v1` | failure-code | per §6 |
| 464 | `logician.failure_code.F-FG-DEADLINE-EXPIRED-IGNORED.v1` | failure-code | per §6 |
| 465 | `linting.r_fg_no_float_monetary.v1` | ast-lint | AST-lint rule under `ast-lint` kind (vocabulary landed at §0.5 v19 row 208 §A.AST_LINT) |
| 466 | `scout.discover.input_shape.funding_goals_block.v1` | interface-contract | §3 v6 — DISCOVER goals-block injection |
| 467 | `scout.discover.fit_score_cached.goal_aware_composer.v1` | interface-contract | §3.3 — deterministic Python compositor; zero-LLM |
| 468 | `match_db.scoring.goal_aware_match_score.v1` | interface-contract | §4.3 — Decimal-mandate composition callable; OQ-7 routed under interface-contract |

**Row range: 446-468 (23 rows). Runtime-live total at compound LOCK: 468.**

**§0.5 vocabulary check:** every row resolves against the v5 + v6 + v19 closed vocabulary (marker / schema / interface-contract / failure-code / pre-gate-check / post-gate-check / ast-lint). NO further vocabulary extension required. The "scoring-callable" concept routes under `interface-contract` per OQ-7 minimum-vocabulary-extension discipline.

**Match-DB schema bump rows.** v1 spec card §8 reserved `match_db.schema.contributes_to_goals.v2` + `monday_fund_radar.goal_aware_brief_format.v1`. Per OQ-1 v0.2-shift, both move to a §0.5 v21 follow-on amendment when §14 + Funding Goal Code-phase wires Match DB v2 + Monday-brief format extension. v0.2 SPEC LOCK ships the schema definition only at §4.1 here; live registration at §0.5 happens with Code-phase. **Net §0.5 v20 row count: 23 (rows 446-468), as tabulated above.**

**Parent-wins discipline:** rows 446-456 → §2 v7.5 commit hash; rows 457-465 → §4 v2.x.4 commit hash; rows 466-467 → §3 v6 commit hash; row 468 → §4 v2.x.4 commit hash (sub-kind reads from §2 sub-kind registry).

# §9. L-005 two-cycle Thesis discipline notes

Per `/AGENTS.md` § "Cross-family review — bridge pattern" and recent precedents (rows 178-208), this amendment family requires:

- **Cycle 1 (driver):** Editor (Llama 3.3 70B/Groq, Meta family) + Judge (Gemini 2.5 Pro/Google) + Red Team (GPT-OSS 120B/Groq, OpenAI-OSS family).
- **Cycle 2 (verification):** same three reviewers on a delta-review packet. NEW probes from Cycle 2 disposed per row-170 transparent disposition pattern.
- **Section E carve-out:** NOT invoked unless logged dispatch failure.
- **L-006 dormant-binding hook:** F-FG-* EXCLUDED from F-CLASS-COVERAGE-INCOMPLETE per OQ-10.
- **F-CIC-CLC-COUPLING-VIOLATION regression:** at every Thesis cycle, the audit prompt's "CIC × CLC orthogonality" rubric MUST verify no implicit coupling slipped into the goal schema, the Cedar rules, the Scout DISCOVER ranking function, or the Match DB scoring composer.
- **F-FG-* family closed-set membership check (Path B regression):** at every Thesis cycle, audit prompt MUST confirm no F-FG-* code crosses ownership to F-WPFA-/F-REFLECTION-/F-PACKET-/F-CLASS-* family. Mirrors WPFA §0.5 v19 §5 F-CIC-CLC-COUPLING-VIOLATION-class regression test.

## §9.1 HARD-LOCKED elements (Thesis cannot relitigate)

- A12 Decimal mandate for `target_amount_minor_units` (int minor units; no float).
- `write-if-absent` discipline + re-key path for status mutations.
- CIC × CLC orthogonality (six × eight, no pre-mapping).
- F-CLASS-* opaque-slot-only outbound boundary on cloud-routed `purpose` field.
- Law 3 Org Isolation — goals live under `orgs/{slug}/vault/operational/funding_goals/`.
- §2 v7.2 sub-kind registry pattern.
- **OQ-1 = v0.2 alongside §14 (operator-pinned).**
- **F-FG-* naming (Path B applied; Thesis cannot relitigate the prefix swap).**

## §9.2 OPEN QUESTIONS for the Thesis dispatch (Thesis-resolvable; operator-overridable at LOCK)

All twelve operator-OQs are absorbed. The Thesis-overrideable surface is now:

- Whether the §2 v7.5 schema as drafted has any subtle orthogonality leak (CIC × CLC AST scan).
- Whether the Cedar rule wording in §7 is over- or under-permissive vs spec text.
- Whether the F-FG-* sub-tag enumeration in §6 covers the load-bearing failure surfaces (Red Team's job).
- Whether the §3 v6 + §6.x amendment shapes correctly inherit §6 v1-r1 prompt-template compilation invariants (F-CONTEXT-PLACEMENT).
- Whether the goal-aware-match-score Decimal composition rounding direction is consistent with v7.0.4-M1 §6.

# §10. v0.2 vs v1.x boundary table (revised per OQ-1 v0.2-shift)

| Element | v0.2 first ship (alongside §14 Report Generator) | v1.x | Stage 2+ horizon |
|---|---|---|---|
| `FundingGoal` schema + sub-kind registry row | **YES — SPEC LOCK + skeleton module** | Predicate bodies LIVE at v1.x amendment | — |
| §3 v6 Scout DISCOVER goal-aware input shape | **YES — SPEC LOCK** | LIVE composer at v1.x | — |
| §6.x prompt-compilation goals-block | **YES — SPEC LOCK** | LIVE injection at v1.x | — |
| Match DB schema bump → v2 (`contributes_to_goals` + `goal_aware_match_score`) | **YES — schema definition** | LIVE composer + Match DB v2 register at v1.x | — |
| §4 v2.x.4 F-FG-* family realization (Cedar/Python predicates) | **SPEC ONLY** — predicate bodies stub-raise NotImplementedError per §15 v1 SPEC-ONLY precedent | LIVE bodies at v1.x amendment | — |
| F-FG-LINKED-CYCLE-ORPHAN + F-FG-DEADLINE-EXPIRED-IGNORED (advisory) | **YES — SPEC LOCK** | LIVE at v1.x | — |
| Monday fund-radar goal-aware brief format | **YES — SPEC** (extends already-shipping routine) | LIVE composer at v1.x | — |
| Push-notify CRITICAL-FIT-AGAINST-GOAL (D + A surfaces) | **YES — SPEC** | LIVE at v1.x | — |
| Push-notify via Cultivator Telegram (operator-to-self; v0.2 second-wave home) | — | **v1.x candidate** (post-§13 LOCK) | — |
| `tilth-vault rekey-goal-status` CLI wrapper | — | **v1.x** (same v0.2 CLI work track as `tilth-vault rekey-record`) | — |
| Goal-aware Scribe prompt context-injection | — | **v1.x** | — |
| `tilth funding-goal *` CLI verbs (create / list / status-change) | **YES — basic CLI** (paired with skeleton module) | Full feature at v1.x | — |
| Multi-org / Stage-2 fleet aggregation of goals | — | — | **Stage 2 (12-Tilth fleet)** |
| Stage-5 commons goal-pattern composability | — | — | **Stage 5** per consent tiers |

# §11. Pre-dispatch checklist (self-check)

- [x] §11 spec-card template followed.
- [x] §2 v7.2 sub-kind convention followed exactly.
- [x] A12 Decimal mandate respected.
- [x] CIC × CLC orthogonality preserved.
- [x] Law 3 Org Isolation enforced at three layers.
- [x] F-CLASS-* opaque-slot discipline applied to outbound boundary.
- [x] §0.5 row range allocated correctly from row 446 (current runtime-live = 445).
- [x] L-005 two-cycle Thesis discipline notes flagged.
- [x] HARD-LOCKED vs OPEN-QUESTIONS distinction explicit.
- [x] v0.2 SPEC-ONLY discipline applied per §15 v1 precedent (predicate bodies stub-raise NotImplementedError).
- [x] Path B naming applied preemptively (F-FG-* not F-GOAL-*).
- [x] Operator OQ-1 + 11 default-OQs absorbed.
- [x] No Python written (SPEC, not implementation).
- [x] No LOCK ceremony invoked.
- [x] Path-only references (no content dumps per L-002).

# §12. Changelog

- 2026-05-10 v1 DISPATCH_SPEC_DRAFT filed at `pipeline/planning/funding_goal_amendment_spec_2026-05-10.md`. Open-question count: 12. Awaiting Josh's OQ-1 ship-window decision.
- 2026-05-11 v2 DISPATCH_SPEC_READY (this file). All 12 OQs absorbed: OQ-1 = v0.2 alongside §14 (operator-pinned 2026-05-11); OQ-2..12 = discovery report defaults. Path B naming applied preemptively (F-GOAL-* → F-FG-*). Row range re-allocated 446-468 against today's runtime-live = 445. SPEC-ONLY discipline at v0.2 mirrors §15 v1 precedent. Ready for L-005 strict two-cycle Thesis dispatch.
