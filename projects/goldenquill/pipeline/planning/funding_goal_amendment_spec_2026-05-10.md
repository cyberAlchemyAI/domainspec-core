---
title: Funding-Goal Sub-Kind — Dispatch Spec Card (§2 v7.3 + §6 ?? + Match DB scoring + §0.5 v16 compound-LOCK candidate)
filed: 2026-05-10
operator: Josh Inklovich
status: DISPATCH_SPEC_DRAFT — pre-Thesis dispatch packet; no LOCK ceremony. L-005 two-cycle review (Editor + Judge + Red Team, FULL live cross-family per /AGENTS.md) MUST close before any LOCK. This is a spec card per `pipeline/engineering/engineering_process_v0.1.md` §11 adapted to a blueprint-amendment family (multiple sections under one compound LOCK) rather than a single Python module.
parent_locks:
  - pipeline/blueprint/v0.1/section_02_vault_topology.md                                # v7.1 LOCKED 2026-04-19 (§2 LOCKED-as-a-whole 2026-04-22)
  - pipeline/blueprint/v0.1/section_02_v7_2_amendment.md                                # §2 v7.2 LOCKED 2026-05-10 — Operational-data sub-kinds (7 SIMPLE rows; sub-kind registry; cross-product Cedar matrix)
  - pipeline/blueprint/v0.1/section_06_operating_envelope.md                            # §6 v1-r1 LOCKED 2026-04-21 — host for prompt-compilation, track-registry, SFR; consumed (not amended) by this spec for Scout DISCOVER prompt-template binding
  - pipeline/blueprint/v0.1/section_03_scout.md                                         # §3 v5 LOCKED 2026-04-17 — DISCOVER channels A–F; (channel G added at architecture v7.0.5)
  - pipeline/architecture/v0.1/architecture_v7_0_5_amendment.md                         # v7.0.5 LOCKED 2026-05-10 row 179 — Funder Intelligence DB + Match DB + Scout channel G + Stage-5 consent-tier on-ramp
  - pipeline/blueprint/v0.1/section_04_v2_x_amendment.md                                # §4 v2.x LOCKED 2026-05-10 rows 193/194 — F-CLASS-* dormant primitives activated; KFR residuals; v7.0.4-M1 corrective predicates
  - pipeline/blueprint/v0.1/section_00_5_section_13_data_collector_amendment.md        # §0.5 v15 LOCKED 2026-05-10 — runtime-live total row 376
  - pipeline/blueprint/v0.1/section_11_intake.md                                        # §11 v1 LOCKED 2026-05-10 — AWARD_INGEST mode (proposal_commitments.yaml; signature-verified award acceptance)
  - pipeline/architecture/v0.1/tilth_architecture_locked.md                             # v7 LOCKED 2026-04-19 A1–A12; A12 Decimal mandate; A1 single-client v0.1 threat model; A4 operator-trusted preflight
  - pipeline/architecture/v0.1/architecture_v7_0_4_M1_amendment.md                      # v7.0.4-M1 LOCKED 2026-05-10 row 190 — Decimal-mandate three-layer ban-float; canonicalization regime; atomic-read fcntl.flock; symlink rejection
  - pipeline/architecture/v0.1/architecture_v7_0_7_amendment.md                         # v7.0.7 LOCKED 2026-05-10 row 180 — Beta classification-driven routing + Classification Review stage + 12 F-CLASS-* primitives
authority: orchestrator dispatch 2026-05-10 — "Funding Goal as a §2 Vault operational-data sub-kind ... goal-driven discovery"
purpose: Stage a SPEC for the Funding Goal sub-kind so a downstream Thesis round + Code phase can audit and LOCK it. SPEC ONLY — no Python written; no LOCK ceremony invoked; no row range reserved against §0.5 until paired blueprint amendments land.
dispatch_class: spec_card_for_blueprint_amendment_family
ws_dispatch_target: NEW WS — provisionally "WS-FG Funding Goal" — not yet on `pipeline/planning/v0_2_dispatch_plan_2026-05-09.md`; one of the Josh-decisions below is whether to slot this into v0.1 finalization, v0.2 first wave, or v0.2 second wave
review_discipline: L-005 strict two-cycle, FULL live cross-family per /AGENTS.md (Editor=Llama/Groq + Judge=Gemini/Google + Red Team=GPT-OSS/Groq) — no Section E carve-out. Mirrors the rigor level applied to §2 v7.2, §11 v1, §12 v1, §13 v1, §15 v1, §4 v2.x.
---

# §0. Why this spec card exists

A **funding goal** is an org-level persistent intent (target_amount + target_deadline + purpose + status + linked_cycle_ids + priority_weight) that survives across grant cycles. Today's Tilth is a per-cycle drafter: Scout DISCOVER walks six channels (A–F + new channel G at v7.0.5) and ranks candidates against an opportunity-list shape. There is no first-class place to say "FIT Farms is trying to raise $480,000 for a regional food-hub buildout by 2027-09-30, and Cycle 1 (USDA RFSI) + Cycle 2 (USDA VAPG Planning) are part of pursuing it."

Without a goal primitive, three load-bearing things degrade:

1. **DISCOVER stays opportunity-list-driven.** Scout walks the world and ranks; the operator has to mentally re-map results against the unstated multi-year goal every cycle.
2. **Match DB scoring is single-cycle.** §7.0.5 Match DB captures match reasoning per cycle but has no multi-cycle aggregation primitive; a candidate that is a B+ fit for a single cycle but an A+ contributor to a $480K goal scores identically with a B+ contributor to an unrelated $25K goal.
3. **Monday fund-radar routine** (memory: `project_monday_fund_routine.md`) digests opportunities without funnel awareness. Goal-aware delivery turns the Monday brief into "$N still needed against goal G; here are the candidates that move the needle most."

Per `feedback_dont_drift_from_tilth_trunk.md` this primitive belongs to the v0.1 trunk only if it materially upgrades grant-writer-on-the-Quill behavior. **Open question 1 below is whether the operator wants funding_goal in v0.1 Beta or v0.2.** This spec is written to support either landing; the boundary table in §11 is explicit.

# §1. Compound-LOCK pairing identity

Following the WS-H §2 v7.2 + §0.5 v11 precedent and the WS-I §13 + §0.5 v15 precedent (paired-commit per `pipeline/blueprint/v0.1/section_06_operating_envelope.md` §6.17 Option-B), the funding-goal amendment is a **compound-LOCK across three to four siblings**:

| Sibling | What lands | Pairing class |
|---|---|---|
| §2 v7.3 (new amendment file `section_02_v7_3_funding_goal_amendment.md`) | New SIMPLE sub-kind row `funding_goal` in §2.13 POST_GATE_ALLOWLIST; new `FundingGoal` frozen-dataclass schema at §2.11.8; new Cedar rule(s) in `operational_subkinds.cedar`; new vault subtree `operational/funding_goals/`; new failure codes routed via §4 (see below) | Primary |
| §6 ?? (new amendment file `section_00_5_section_06_funding_goal_amendment.md` ON THE §6 SIDE OR a §6.1x amendment to §6 v1-r1; OQ-2 selects) | §6 Scout DISCOVER input-shape extension — goal as primary input alongside CIC/CLC weights; how channel G + channel A–F are goal-aware; whether the §5 track-registry adds a `goal_aware_submission` track or whether `submission` track gains a goal-binding sub-config | Sibling |
| §4 v2.x.1 (extends `section_04_v2_x_amendment.md` — see §6 below for new F-GOAL-* family) | F-GOAL-* failure codes registered; PRE/POST gate rows allocated; module skeletons pointed at | Sibling |
| §0.5 v16 amendment (new file `section_00_5_section_02_v7_3_funding_goal_amendment.md`) | Row append starting at 377; sub-kind row + schema rows + Cedar policy row + failure-code rows + Scout DISCOVER interface-contract row + Match-DB scoring-callable row + Monday-fund-radar consumer row | Sibling |

Compound transaction discipline per §2 v7.2 §11 audit prompt + WS-I §13 paired-commit pattern: all four sibling rows enter `lock_history.v1.jsonl` at the same `lock_timestamp_utc`. F-INDEX-STALE PRE-gate fires at commit time per §6.2 order 3; all new §0.5 rows must be present in the index or the compound commit fails closed.

**Compound LOCK row(s) in lock_history:** anticipated rows ≥ 198 (current runtime-live row at §13 v1 LOCK = 197 per memory line `project_blueprint_section_13_data_collector_v1_locked.md`; pre-staging only — actual row depends on which other LOCKs land first).

# §2. Pydantic dataclass shape — `FundingGoal` (proposed §2.11.8)

Following the §2 v7.2 sub-kind convention EXACTLY: `@dataclass(frozen=True, kw_only=True)`; one record = one file; SIMPLE class; `write-if-absent` mode; `__post_init__` invariant validation; canonical-JSON encode/decode round-trip; module at `pipeline/vault/sub_kinds/funding_goals.py`; tests at `tests/vault/sub_kinds/test_funding_goals.py`.

```python
@dataclass(frozen=True, kw_only=True)
class FundingGoal:
    record_id: str                          # opaque caller-minted ID; matches filename {record_id}.json
    goal_name: str                          # operator-facing label, e.g. "Regional Food Hub Buildout"
    target_amount_minor_units: int          # smallest currency unit (cents); A12 Decimal-mandate via dedicated decoder helper (see §2.1)
    currency: str                           # ISO-4217 alpha-3 (e.g., "USD")
    target_deadline: str                    # UTC ISO-8601 date 'YYYY-MM-DD'; v7.2 'Z' convention does NOT apply (date not datetime)
    purpose: str                            # free-form purpose statement (operator-discipline; no content validation per §2 v7.2 boundary)
    cic_tag: str                            # one of the six CIC slugs per `assets/cards/customer_identification/` — Food Systems | Educator | Public Agency | Arts & Culture | Cooperative | Ecosystem Intermediary
    clc_tags: tuple[str, ...]               # ZERO OR MORE of the eight CLC slugs; ordered sortable; an empty tuple is valid (CIC × CLC orthogonality per v7.0.8 LOCK — see §3 below)
    status: str                             # "pursuing" | "blocked" | "met" | "abandoned"
    blockers: tuple[GoalBlocker, ...]       # structured blocker rows; empty tuple permitted; non-empty REQUIRED iff status == "blocked"
    linked_cycle_ids: tuple[str, ...]       # grant_id strings under orgs/{slug}/vault/grants/{grant_id}/; ordered; may be empty
    priority_weight: int                    # 0..100 (operator-set); higher = more weight in Match-DB scoring contribution
    created_at: str                         # UTC ISO-8601 'Z' (datetime convention per v7.2)
    last_status_change_at: str              # UTC ISO-8601 'Z'; equals created_at at construction; mutates only via the re-key path (no in-place mutation per v7.2)


@dataclass(frozen=True, kw_only=True)
class GoalBlocker:
    blocker_kind: str                       # "rejection" | "capacity" | "timing" | "scope_change" | "external_constraint" | "other"
    summary: str                            # one-line blocker summary
    surfaced_at: str                        # UTC ISO-8601 'Z'
    surfaced_by_grant_id: str | None        # grant_id if the blocker originated from a cycle outcome
    surfaced_by_match_id: str | None        # match_id if originated from Match DB analysis
    resolution_hint: str                    # operator-supplied hint; may be empty
```

## §2.1 A12 Decimal mandate dispatch

Per architecture v7.0.4-M1 §6 the Decimal mandate is three-layer (AST-lint ban on `float` for monetary fields + dedicated decoder helper + explicit-context-required helper). `target_amount_minor_units` is `int` (smallest currency unit) — matches §2.11.2 `FinancialsRecord.amount_minor_units` exactly. The decoder helper `from_canonical_bytes` MUST re-validate that the JSON-parsed value is `int` and not float; tampered-on-disk records with `target_amount_minor_units: 480000.0` (decoded as float) fail-close on `F-OPERATIONAL-SCHEMA-INVALID` per §2 v7.2 §7. **No `float` field in `FundingGoal` or `GoalBlocker`.** AST-lint R3-equivalent rule applies (matches §2 v7.2 discipline; concrete predicate body deferred to §4 v2.x.1 follow-on).

## §2.2 Invariants (`__post_init__` — fail-close at write AND at decode round-trip)

1. `record_id` non-empty; matches expected filename derivation `record_id_for(record) == record.record_id`.
2. `goal_name` non-empty.
3. `currency` is exactly three uppercase ASCII letters (`^[A-Z]{3}$`).
4. `target_amount_minor_units` is `int` (not `bool`, not `float`); `target_amount_minor_units >= 0`.
5. `target_deadline` matches `^\d{4}-\d{2}-\d{2}$` (date-only); reject non-ISO; reject `target_deadline < created_at[:10]` IF status is "pursuing" or "blocked" (operator cannot create a goal with an already-past deadline in active status — see OQ-3 for the alternative).
6. `cic_tag` is in the closed set of six CIC slugs declared in CLAUDE.md.
7. `clc_tags` is a tuple of CLC slug strings; every element is in the closed set of eight CLC slugs declared in CLAUDE.md; duplicates rejected; tuple is lex-sorted (deterministic on-disk form).
8. `status` is in `{"pursuing", "blocked", "met", "abandoned"}`.
9. If `status == "blocked"`, `blockers` is non-empty. If `status != "blocked"`, `blockers` MAY be non-empty (historical blocker rows persist after status flips back to `pursuing`).
10. `linked_cycle_ids` is a tuple of non-empty strings; duplicates rejected; per-tuple lex-sorted on-disk form.
11. `priority_weight` is `int` in `[0, 100]`.
12. `created_at` and `last_status_change_at` end with `'Z'`; `last_status_change_at >= created_at` (lex compare).
13. Per `GoalBlocker`: `blocker_kind` in the closed set; `summary` non-empty; `surfaced_at` ends with `'Z'`; at most one of `surfaced_by_grant_id` / `surfaced_by_match_id` is non-None (mutually exclusive; both-None permitted for operator-asserted blockers).

## §2.3 Sub-kind registry row (§2.12 amendment)

```python
"funding_goal": SubKindDescriptor(
    intent="operational-funding-goal-write",
    vault_subtree="operational/funding_goals/",
    record_class=FundingGoal,
    to_canonical_bytes=funding_goals.to_canonical_bytes,
    from_canonical_bytes=funding_goals.from_canonical_bytes,
    record_id_for=funding_goals.record_id_for,
    severity_default="YELLOW",            # see §2.4
    severity_for=lambda record: "RED" if record.status == "blocked" else "YELLOW",
),
```

## §2.4 Admin-risk severity

Default YELLOW (multi-cycle persistent operator intent, may surface in cross-cycle prompts to cloud-routed seats — see §3 classification posture). RED when `status == "blocked"` so the admin-risk ledger surfaces blockers for operator attention each cycle. (OQ-4 below challenges whether blocked goals warrant RED or stay YELLOW — operator decides.)

## §2.5 Status mutation discipline

Per §2 v7.2 §1, in-place mutation is by design impossible (`write-if-absent` everywhere). Status changes follow the v7.2 "worked operator re-key path":

1. Operator mints a fresh `record_id` (UUID4).
2. Operator writes the updated `FundingGoal` record (new status, fresh `last_status_change_at`, augmented `blockers` tuple if applicable, possibly augmented `linked_cycle_ids`).
3. Operator appends an admin-risk-ledger entry naming both `record_id`s and the supersession reason (e.g., `"goal_status_change: pursuing → blocked: USDA RFSI declined cycle 1"`).
4. The original record persists at its path; the ledger entry is the disambiguator. v0.2 `tilth-vault rekey-record` CLI wraps steps 1–3.

A downstream Match-DB scoring read (see §4) MUST resolve the live `record_id` for a goal via the ledger trail — naive "latest write" semantics is forbidden because the vault has no delete. **OQ-5: should the spec ship a thin `funding_goals.resolve_live(record_id_set, admin_risk_ledger) → FundingGoal` helper or defer that to the seat-side?**

# §3. §6 Scout DISCOVER integration — goal as primary input

## §3.1 Integration surface (existing structure to extend)

Per §3 v5 + v7.0.5 channel G addition, Scout DISCOVER reads the union of seven parallel-primary channels (A federal APIs / B cached datasets / C portal adapters / D program pages / E RSS / F web search / G local funder-intel corpus). Each channel produces `Candidate` rows (§3.2.1) with `fit_score_cached` (0..100 cache-only heuristic — NOT a VERIFY decision).

Today the operator's PROJECT_CONTEXT.md supplies CIC/CLC/sector tags; Scout's channel adapters filter and score using those tags. **The new input shape adds**: an optional `funding_goals: tuple[FundingGoal, ...]` parameter, read at Scout session start from `orgs/{slug}/vault/operational/funding_goals/` (filtering for `status in {"pursuing", "blocked"}`).

## §3.2 What changes in DISCOVER

- **No channel-dispatch change.** A–G stay parallel primary. Scout does NOT add a new "goal-aware channel" — the goals modulate ranking and de-dup, not channel selection. This preserves the channel-A-through-G architecture from v7.0.5 and avoids the L-006 dormant-binding miss.
- **`fit_score_cached` composition.** The cache-only heuristic at DISCOVER gets a goal-bonus added per active `pursuing` / `blocked` goal whose CIC tag matches the candidate's tags AND whose CLC tag overlap with the candidate's inferred CLC is non-empty (CLC orthogonality preserved per v7.0.8 — see §3.5). The bonus is computed by a deterministic Python function (zero LLM cost), bounded `[0, +25]`, with the goal's `priority_weight` as the weight. The combined `fit_score_cached` is still clamped to `[0, 100]`.
- **Per-goal de-dup pass.** After channel-dispatch dedup, candidates are tagged with the set of goals they could plausibly contribute to (zero, one, or many). This tag travels through VERIFY into REVIEW and is surfaced to the operator at REVIEW.
- **Goal-aware ranking is post-dedup, pre-VERIFY.** This keeps the VERIFY 10-second-default cap unchanged (per §3 v5 §4.7) and keeps `fit_score_cached` truthful as the entry-to-VERIFY filter.

## §3.3 What §6 (operating envelope) needs

§6 hosts the prompt-template compilation pipeline (§6.11) and the SFR certificate format (§6.5). The Scout DISCOVER prompts (per-channel) currently inject CIC/CLC weights at the schema block. The goal-bearing extension adds:

- A **goals-block** in the start-block + end-block injection (per §6.11 step 2 + step 3). The goals-block carries the active `funding_goals` tuple in a compact YAML form keyed by `goal_id`. Per A4 architectural FLOOR, this block goes in BOTH start AND end with byte-identical content (`F-CONTEXT-PLACEMENT` PRE-gate already enforces; goals-block joins the existing four load-bearing markers).
- A **classification-aware redaction** at the goals-block. Per v7.0.7 LOCK + the §4 v2.x F-CLASS-OUTBOUND-BOUNDARY family, the `purpose` field of any active goal is classification-tagged at the per-org classification register. Cloud-routed Scout channels (Channel F web search if BYOK provider is cloud-shaped; Channel G if any future component routes through cloud — currently always-local per v7.0.5) receive the goals-block with `purpose` opaque-slot-filled (`[SLOT_<numeric_id>]` per §1 of v7.0.7) UNLESS the operator's per-org default has `funding_goal.purpose` classified `public` / `shareable`.

**OQ-6:** does `FundingGoal.purpose` default `confidential` (operator-revenue-strategy-adjacent) or `shareable` (typical goal statements like "regional food-hub buildout" are not sensitive)? Card-level default decision per v7.0.7 §3.6 three-layer defaults.

## §3.4 Whether DISCOVER changes channel-A-through-F dispatch

**It does NOT.** The seven channels (A–G) keep their existing routing. The goal-aware modulation lives entirely at:

1. The DISCOVER input-shape (a new `funding_goals` parameter on the Scout session call).
2. The `fit_score_cached` composition function (post-channel-dispatch ranking).
3. The post-dedup tagging pass.

Channel-G (v7.0.5 local funder-intel corpus) gains a single new query mode: "given an active goal G with `target_amount_minor_units = X` and `target_deadline = D`, surface corpus docs about funders whose typical award range overlaps `X` AND whose program cadence permits a submission by `D`." This is a deterministic filter over the funder-intel register's `documents[].award_range` + `documents[].cadence` fields — no new vector substrate.

## §3.5 CIC × CLC orthogonality preservation

Per v7.0.8 LOCK + CLAUDE.md "CIC × CLC orthogonal — never pre-map", the goal's `cic_tag` is single-valued (the org's primary CIC for this goal) and `clc_tags` is zero-or-more CLC slugs naming pathways the goal could be funded through. The goal does NOT pre-map CIC → CLC subset; it captures the operator's belief about which capital logics could feed this goal at this time. Scout's ranking function reads both `cic_tag` and `clc_tags` but treats them as **independent dimensions** in the score composition. F-CIC-CLC-COUPLING-VIOLATION (v7.0.8 PRE-gate) MUST regress-test against the goal-schema at LOCK to confirm no implicit coupling slipped in.

# §4. Match DB scoring weight addition

Per v7.0.5 §2, Match DB lives at `orgs/<slug>/match_database/register.yaml` and captures per-match `match_score` (0.0–1.0) + structured boolean fields (sector_match / funding_world_match / etc.) + narrative summary + operator action + cycle outcome. **It currently has no field that reflects which goal(s) a match contributes to.**

## §4.1 Schema additions to `match_database.v1` (Match DB schema bump → `match_database.v2`)

Two new fields per match row:

```yaml
matches:
  - match_id: <opaque-uuid>
    funder_doc_id: <reference>
    proposed_at: <utc>
    proposed_by: <scout_session_id>
    proposed_for_grant_cycle: <rfa_hash if specific cycle, else null>
    match_score: <0.0 - 1.0>              # existing
    match_reasoning: { ... }              # existing
    operator_action: { ... }              # existing
    cycle_outcome: { ... }                # existing
    consent_tier: <consent_tier>          # existing
    # NEW v0.2 fields:
    contributes_to_goals:                 # zero-or-more goal record_ids this match would advance
      - goal_record_id: <FundingGoal.record_id>
        estimated_contribution_minor_units: <int>    # operator-confirmed at REVIEW; A12 int, no float
        estimated_contribution_confidence: <"low" | "medium" | "high">
    goal_aware_match_score: <0.0 - 1.0>   # composite score combining match_score with goal-fit weight; see §4.2
```

## §4.2 Goal-aware match score composition

Deterministic Python (zero LLM cost), runs at Match DB write time AND at every Match DB read used for scoring:

```
goal_aware_match_score(match, active_goals) =
    base = match.match_score                                                 # 0.0–1.0
    if match.contributes_to_goals is empty: return base
    goal_bonus = max over each (gc in match.contributes_to_goals where gc.goal_record_id resolves to a live goal in active_goals):
        weight_g = active_goals[gc.goal_record_id].priority_weight / 100.0   # 0.0–1.0
        contribution_ratio_g = min(1.0, gc.estimated_contribution_minor_units / max(1, active_goals[gc.goal_record_id].target_amount_minor_units))
        confidence_factor_g = {"low": 0.5, "medium": 0.75, "high": 1.0}[gc.estimated_contribution_confidence]
        goal_bonus_g = weight_g * contribution_ratio_g * confidence_factor_g   # 0.0–1.0
    composite = min(1.0, base + GOAL_BONUS_WEIGHT * goal_bonus)              # GOAL_BONUS_WEIGHT default 0.25, operator-tunable
    return composite
```

Where the goal record IDs resolve via the §2.5 live-record resolution helper (admin-risk-ledger walk). Goals whose `record_id` no longer resolves to a live record (e.g., the goal was rekeyed to abandoned) contribute zero. A failure-closed code surfaces stale goal references (`F-GOAL-LINKED-CYCLE-ORPHAN` — see §6).

**A12 Decimal-mandate composition.** The composition function uses `Decimal` arithmetic via the explicit-context-required helper per v7.0.4-M1 §6; the `0.5 / 0.75 / 1.0` confidence factors are `Decimal("0.5")` literals at module load (not float literals — AST-lint catches), and the final score is rounded to a fixed precision (`Decimal('0.0001')`, ROUND_HALF_EVEN) before being cast back to `float` for the on-disk YAML round-trip. Tests assert that the same `(match, active_goals)` input produces byte-identical YAML on disk across re-runs.

## §4.3 Where the scoring callable lives

Module: `pipeline/match_db/scoring.py` (NEW). Function: `goal_aware_match_score(match: MatchRow, active_goals: Mapping[str, FundingGoal]) → Decimal`. Called from:

- **Scout REVIEW stage** when surfacing a candidate's match score to the operator (per §3 v5 §4.8). The operator sees BOTH `match_score` (raw) AND `goal_aware_match_score` (composite) — Law 4 substance-not-style applies (transparent surfacing, no silent rewrite).
- **Match DB read** at any other downstream consumer (Scribe seat preflight, Editor seat clarity-review of match reasoning, Judge seat rubric-scoring when the rubric weights goal-alignment).
- **Monday fund-radar routine** (per `project_monday_fund_routine.md`) — see §5.

## §4.4 §0.5 row for the scoring callable

New row at §0.5 v16: `match_db.goal_aware_match_score.v1` — kind `pre-gate-check`-adjacent `scoring-callable` (NEW primitive_kind — but per §6.9 D-05 step 4 the closed vocabulary is 13 + 2 PENDING_PARENT_BACKFILL = 15). **OQ-7: does `scoring-callable` need to be added to the §0.5 primitive_kind closed vocabulary, or should it route under the existing `interface-contract` kind?** Default per minimum-vocabulary-extension discipline: route under `interface-contract`. The row's `parent` field cites `section_04_v2_x_amendment.md#§<new>` once the §4 F-GOAL-* family lands.

# §5. Push-notify wiring — Monday fund-radar + critical-fit-against-goal trigger

## §5.1 Concept

When a CRITICAL-fit opportunity (Scout VERIFY returns `VERIFIED_FIT` + operator's `match_score >= operator_critical_threshold`) matches an active `pursuing` or `blocked` goal (i.e., the candidate is tagged with at least one live goal in §3.2's post-dedup pass), a push-notify event fires through the operator-pinned channel.

## §5.2 v0.1 channel options vs v0.2 Cultivator-based

**v0.1 channel options** (subset of what's already shippable):

| Option | Source on disk | Effort | Trade-off |
|---|---|---|---|
| **A. Monday-brief integration only** | `project_monday_fund_routine.md` (cron Mon 8:30 AM) | Lowest — wire into existing weekly job | Notification is delayed up to 7 days |
| **B. Email-via-operator-SMTP at VERIFY close** | BYOK SMTP per operator's existing keys | Medium — needs a single new tilth-side helper + classification-aware redaction | TCPA / CAN-SPAM N/A (operator-to-self); always-local routing |
| **C. Local file-watcher + macOS Notification Center** | `osascript` (Josh's M1 dev node + Pro tier) | Medium-low — single shell tool | Mac-only; appliance-pinned UI surface |
| **D. CLI-on-next-run surface** | Already exists (Scout REVIEW gate) | Zero | No interrupt-time push; operator sees at next `tilth scout review` invocation |

**v0.2 Cultivator-based** (per §13 v1 LOCK 2026-05-10 rows 196/197):

- Cultivator's per-employee Telegram-bot (Cultivator framework runs MTProto with the OrgScopedBot wrapper @final per Cycle 2 RT-C2-03). Sending operator-to-self over the operator's own Cultivator bot is the natural v0.2 home — consent ledger is trivially "self-consenting" (operator's own employee record); F-DATACOLLECTOR-CONSENT-MISSING auto-satisfied; per-recipient signed batch envelope path is the same one §13 v1 ships.

## §5.3 Recommended v0.1/v0.2 boundary

**v0.1 Beta ships option D (CLI-on-next-run surface) by default + option A (Monday-brief integration) as a free byproduct of the Monday cron.** Options B and C are forward-design markers in this spec and become v0.2 work if the operator requests them. Option v0.2 Cultivator-based is the canonical post-§13 push surface — it shares the `data_collector.outbound_batch_compose_input.v1` + `data_collector.signed_batch_envelope.v1` schemas (§0.5 rows 350 + 364) and inherits the eight F-DATACOLLECTOR-* gates for free.

## §5.4 Monday fund-radar routine — goal-aware brief

Per `project_monday_fund_routine.md`, Mondays 8:30 AM cron produces a Josh-facing digest + per-client briefs (Law 3 Org Isolation enforced). The goal-aware extension reorganizes the per-client brief into goal sections:

```
[Per-client brief — FIT Farms LLC — 2026-09-21]

GOAL: Regional Food Hub Buildout
  target: $480,000 USD by 2027-09-30
  status: pursuing (linked cycles: USDA-RFSI-2026, PA-SCBGP-FY27)
  remaining: $355,000 (committed-or-awarded $125,000 from prior cycles per Match DB outcomes)
  this week's candidates (3):
    1. USDA AMS Local Agriculture Market Program — match_score 0.78, goal_aware 0.91 [CRITICAL-FIT-AGAINST-GOAL]
    2. Heinz Endowments Regional Food Systems Initiative — match_score 0.62, goal_aware 0.77
    3. ...

GOAL: Worker Co-op Conversion Pilot
  ...

UNALLOCATED CANDIDATES (no live goal match): 4 — see Scout review queue
```

The "CRITICAL-FIT-AGAINST-GOAL" tag is the v0.1 push-notify surface (option D + Monday integration); v0.2 Cultivator-based push fires the same tag through Telegram. The brief itself does NOT redefine the Monday routine — it references `project_monday_fund_routine.md` and adds the goal sectioning as a per-client-brief format extension.

# §6. F-GOAL-* failure-code family (§4 v2.x.1 follow-on amendment seed)

Following the §4 v2.x format (tier / module / severity / §ref columns) and the v7.0.5 F-MATCH-DB-* + F-CHANNEL-G-* family naming conventions, this spec proposes **seven F-GOAL-* failure codes**. The §4 v2.x.1 amendment registers them; module skeletons land at `pipeline/logician/gates/`; Cedar predicate bodies land at WS-L follow-on.

| Code | Tier | Module (proposed) | Severity | Rationale / Trigger |
|---|---|---|---|---|
| `F-GOAL-CROSS-ORG-LEAK` | PRE | `f_goal_cross_org_leak.py` | P0 (Law 3) | Any `FundingGoal` read whose path resolves to `orgs/<other_slug>/vault/operational/funding_goals/...` — mirrors `F-MATCH-DB-CROSS-ORG` (v7.0.5 §5.1). Defense-in-depth on top of existing `org_isolation.cedar` Rule 2. **No M13 bypass.** |
| `F-GOAL-SCHEMA-INVALID` | PRE-write + POST-read | `f_goal_schema_invalid.py` | HIGH | Schema validation failure (any of the 13 invariants in §2.2) at write OR at decode round-trip. Tampered-on-disk records (e.g., float target_amount, missing 'Z' on created_at, CIC tag outside the six closed slugs, status outside the closed set) fail-close. Mirrors `F-OPERATIONAL-SCHEMA-INVALID` (§2 v7.2 §7). M13 audited. |
| `F-GOAL-CIC-TAG-INVALID` | PRE-write | `f_goal_cic_tag_invalid.py` | HIGH | `cic_tag` not in the six-CIC closed set per CLAUDE.md / `assets/cards/customer_identification/`. Sibling to F-CIC-CLC-COUPLING-VIOLATION (v7.0.8) but at the schema layer rather than the coupling layer. M13 audited (operator may add a NEW CIC at v0.2, but at v0.1 the closed set is hard). |
| `F-GOAL-CLC-TAG-INVALID` | PRE-write | `f_goal_clc_tag_invalid.py` | HIGH | Any element of `clc_tags` not in the eight-CLC closed set per CLAUDE.md / `assets/cards/capital_logic/`. Same family rationale as F-GOAL-CIC-TAG-INVALID. M13 audited. |
| `F-GOAL-STATUS-TRANSITION-INVALID` | PRE-write | `f_goal_status_transition_invalid.py` | HIGH | A new `FundingGoal` record (via the §2.5 re-key path) carries a `status` transition the policy forbids. Default-permitted transitions: `pursuing → blocked / met / abandoned`, `blocked → pursuing / met / abandoned`, `met → abandoned` (rare — operator-curation override), `abandoned → pursuing` (operator un-abandons). Default-forbidden: `met → pursuing` (a met goal cannot be reactivated; operator must mint a NEW goal). **OQ-8: is the operator OK with this transition closure or should the spec be more permissive?** M13 audited (operator can override an unusual transition with audited record). |
| `F-GOAL-LINKED-CYCLE-ORPHAN` | POST-read + PRE-cycle-start | `f_goal_linked_cycle_orphan.py` | MEDIUM | A `linked_cycle_ids` element does not resolve to a live grant under `orgs/<slug>/vault/grants/<grant_id>/` (e.g., operator deleted the cycle or renamed the grant). Surfaces at goal-aware-match-scoring time (Match DB scoring composition silently treating the orphan as null) AND at cycle-start to prompt operator to either remove the orphan or restore the cycle. M13 audited. |
| `F-GOAL-PRIORITY-MUTATION-UNAUDITED` | PRE-write | `f_goal_priority_mutation_unaudited.py` | MEDIUM | A new `FundingGoal` record (via the §2.5 re-key path) carries a `priority_weight` that differs from the prior live record's `priority_weight` without a matching admin-risk-ledger entry capturing the mutation reason. Mirrors v7.0.5 `F-MATCH-DB-CONSENT-TIER-VIOLATION` (§5.4 Trigger B). M13 audited. |
| `F-GOAL-DEADLINE-EXPIRED-IGNORED` | POST-read | `f_goal_deadline_expired_ignored.py` | MEDIUM (advisory) | A goal whose `target_deadline < today_utc` AND `status == "pursuing"` AND has been read by any seat without a status mutation in the last operator-set window (default 30 days). Advisory — does not block pipeline; surfaces at next REVIEW gate so operator confirms goal expiration. M13 NOT needed (advisory). |

**Module/sub-code collapse:** following the v2.2 F-AMDT-08/09/10/11 + v2.x F-CLASS-* sub-code-collapse precedent, F-GOAL-SCHEMA-INVALID / F-GOAL-CIC-TAG-INVALID / F-GOAL-CLC-TAG-INVALID MAY share a single module `f_goal_schema_validation.py` (three sub-codes) since all three consume the same `FundingGoal` decoder + per-field validator surface. Final module count after collapse: five modules realizing eight codes (one umbrella, four singletons). **OQ-9: does the operator want sub-code collapse here (matches §4 v2.x precedent) or one module per code (cleaner ownership, larger module count)?**

**PRE-gate order rows (§4 v2.x §X.1 family):** rows allocate from PRE-66 onward (current §4 v2.x last allocated PRE-58 per v7.0.7 §5.1 + F-CLASS-COVERAGE-INCOMPLETE) — re-allocate at LOCK ceremony after WS-L follow-on amendments land. POST-gate rows allocate from POST-26 onward.

**META-gate composition:** F-CLASS-COVERAGE-INCOMPLETE (the META PRE-cycle gate at v7.0.7) MUST learn the F-GOAL-* codes if the goal-aware-routing surface ships at v0.1 Beta — i.e., the `REQUIRED_F_CLASS_CODES` registry in `pipeline/logician/gates/f_class_coverage_incomplete.py` extends to include the F-GOAL-* family at compound LOCK. **OQ-10: does the spec activate F-CLASS-COVERAGE-INCOMPLETE binding for F-GOAL-* at v0.1, or is the family classified `confidential` and exempt from cloud-outbound boundary checks (in which case the META gate doesn't gate it)?**

# §7. Cedar policy additions

Lives at `pipeline/vault/policies/operational_subkinds.cedar` (extending the v7.2 file). Three new rules + one extension:

1. **Extension to `operational_org_isolation`:** add `sub_kind == "funding_goal"` to the default-permit set so funding-goal writes match the per-org isolation rule with no new rule required. F-GOAL-CROSS-ORG-LEAK at the Logician layer is defense-in-depth (mirrors v7.2 §6 Rule 1 + F-OPERATIONAL-ORG-MISMATCH precedent).
2. **`goal_status_transition`:** permits goal writes when the new record's `status` is a permitted transition from the prior-live record's `status` per the §6 F-GOAL-STATUS-TRANSITION-INVALID table. Operator-key-id signature of an admin-risk-ledger entry capturing the supersession reason is REQUIRED (forbidden transitions fall to implicit deny → F-GOAL-STATUS-TRANSITION-INVALID).
3. **`goal_priority_mutation_audited`:** permits goal writes whose `priority_weight` differs from the prior-live record's `priority_weight` ONLY when an admin-risk-ledger entry captures the mutation reason. Mirrors v7.0.5 §5.4 Trigger B.
4. **`goal_taxonomy_closed`:** permits goal writes ONLY when `cic_tag` ∈ six-CIC closed set AND every element of `clc_tags` ∈ eight-CLC closed set. Falls through to F-CIC-CLC-COUPLING-VIOLATION's existing surface (sibling — see CLAUDE.md "Do not encode any CIC→CLC subset binding in any code, schema, prompt, knowledge pack, scoring weight, or config — F-CIC-CLC-COUPLING-VIOLATION enforces fail-closed").

The Python evaluator at `pipeline/vault/sub_kinds/policy_eval.py` is authoritative at v0.1 (per §2 v7.1 §3.4 + v7.2 §6 lifecycle) until the file is M15-sealed.

# §8. §0.5 v16 amendment — row range allocation

Current runtime-live total at §13 LOCK = **376** (per `pipeline/blueprint/v0.1/section_00_5_section_13_data_collector_amendment.md` row_delta line 21). **The funding-goal compound LOCK allocates rows starting at 377.**

Row count breakdown for the compound-LOCK family (subject to OQ-1 ship-window decision):

| Row | primitive_id | kind | parent |
|---|---|---|---|
| 377 | `blueprint.section_anchor.s02_v7_3_funding_goal.v1` | marker | §2 v7.3 |
| 378 | `vault.sub_kinds.funding_goal.v1` | schema | `FundingGoal` frozen kw_only |
| 379 | `vault.sub_kinds.funding_goal.goal_blocker.v1` | schema | `GoalBlocker` frozen kw_only |
| 380 | `vault.sub_kinds.funding_goal.canonical_codec.v1` | interface-contract | `to_canonical_bytes` / `from_canonical_bytes` codec pair |
| 381 | `vault.sub_kinds.registry.funding_goal_descriptor.v1` | interface-contract | `SUB_KIND_REGISTRY["funding_goal"]` row per §2.12 |
| 382 | `vault.policy.operational_subkinds.cedar.goal_status_transition.v1` | interface-contract | Cedar rule per §7 |
| 383 | `vault.policy.operational_subkinds.cedar.goal_priority_mutation_audited.v1` | interface-contract | Cedar rule per §7 |
| 384 | `vault.policy.operational_subkinds.cedar.goal_taxonomy_closed.v1` | interface-contract | Cedar rule per §7 |
| 385 | `vault.post_gate_allowlist.operational-funding-goal-write.v1` | interface-contract | §2.13 allowlist row (`write-if-absent` SIMPLE) |
| 386 | `vault.layout.org_vault_operational_funding_goals.v1` | interface-contract | `VaultLayout.org_vault_operational_funding_goals(slug)` per §5 v7.2 |
| 387 | `logician.failure_code.F-GOAL-CROSS-ORG-LEAK.v1` | failure-code | per §6 |
| 388 | `logician.failure_code.F-GOAL-SCHEMA-INVALID.v1` | failure-code | per §6 (umbrella w/ sub-tags if §6 OQ-9 picks collapse) |
| 389 | `logician.failure_code.F-GOAL-CIC-TAG-INVALID.v1` | failure-code | per §6 |
| 390 | `logician.failure_code.F-GOAL-CLC-TAG-INVALID.v1` | failure-code | per §6 |
| 391 | `logician.failure_code.F-GOAL-STATUS-TRANSITION-INVALID.v1` | failure-code | per §6 |
| 392 | `logician.failure_code.F-GOAL-LINKED-CYCLE-ORPHAN.v1` | failure-code | per §6 |
| 393 | `logician.failure_code.F-GOAL-PRIORITY-MUTATION-UNAUDITED.v1` | failure-code | per §6 |
| 394 | `logician.failure_code.F-GOAL-DEADLINE-EXPIRED-IGNORED.v1` | failure-code | per §6 |
| 395 | `scout.discover.input_shape.funding_goals_block.v1` | interface-contract | §3 — DISCOVER goals-block injection |
| 396 | `scout.discover.fit_score_cached.goal_aware_composer.v1` | interface-contract | §3.2 — deterministic Python compositor; zero-LLM |
| 397 | `match_db.scoring.goal_aware_match_score.v1` | interface-contract | §4 — Decimal-mandate composition callable |
| 398 | `match_db.schema.contributes_to_goals.v2` | schema | §4.1 Match DB schema bump |
| 399 | `monday_fund_radar.goal_aware_brief_format.v1` | interface-contract | §5.4 per-client brief format extension |

**Row range allocated by this spec: 377–399 (23 rows). Runtime-live total at proposed compound LOCK: 399.**

**§0.5 vocabulary check:** every row resolves against the v5 + v6 closed vocabulary (marker / schema / interface-contract / failure-code / pre-gate-check / post-gate-check). NO vocabulary extension required. The "scoring-callable" concept from §4.4 above routes under `interface-contract` per minimum-vocabulary-extension discipline.

**Parent-wins discipline:** each row's `parent_lock_version` + `parent_lock_commit_hash` point at §2 v7.3 (rows 377–386), §4 v2.x.1 (rows 387–394), §6 ?? or §3 v6 (rows 395–396 — see OQ-2), `match_db.v2` (rows 397–398), and `project_monday_fund_routine.md` (row 399 — though the Monday memory is not a LOCKed blueprint section, so this row's parent points at the §6 v1-r1 compilation pipeline that hosts the brief format).

# §9. L-005 two-cycle Thesis discipline notes

Per `/AGENTS.md` § "Cross-family review — bridge pattern" and recent precedents (WS-D v7.0.5 LOCK row 179 + WS-F §12 v1 + WS-E §11 v1 + WS-H §2 v7.2 + WS-G §5 v8 + WS-K §15 + WS-C-M1 v7.0.4-M1 row 190 + WS-L §4 v2.x rows 193/194 + WS-I §13 v1 LOCK rows 196/197), this amendment family requires:

- **Cycle 1 (driver):** Editor (Llama 3.3 70B / Groq, Meta family) + Judge (Gemini 2.5 Pro / Google) + Red Team (GPT-OSS 120B / Groq, OpenAI-OSS family). Three live model IDs per /AGENTS.md. Templates: `pipeline/validation/v7_0_5_thesis_2026-05-09/dispatch_audit_v{1,2}.sh`.
- **Cycle 2 (verification):** same three reviewers on a delta-review packet per `pipeline/engineering/engineering_process_v0.1.md` §7. If Cycle 2 surfaces NEW probes (mirroring recent WS-C-M1 / WS-D / WS-K precedent), the row-170 transparent disposition pattern applies — NEW probes either FOLD-IN at LOCK with explicit text-level mechanisms OR forward-track to a follow-on minor amendment per `project_section_15_external_review_disposition_2026-05-10.md`.
- **Section E carve-out:** NOT invoked unless a logged dispatch failure (curl/openclaw error in the audit trail) per `/AGENTS.md` § "Section E carve-out — invocation discipline".
- **L-006 dormant-binding hook:** F-CLASS-COVERAGE-INCOMPLETE META gate (v7.0.7 row 180; activated at v7.0.4 row 178 + v2.x rows 193/194) checks the F-GOAL-* family's `REQUIRED_F_CLASS_CODES` registry membership IF OQ-10 selects "include F-GOAL-* in the META gate's coverage set." If excluded, document explicitly in §4.3.3-equivalent paragraph in the §4 v2.x.1 amendment why F-GOAL-* is out of META scope.
- **F-CIC-CLC-COUPLING-VIOLATION regression:** at every Thesis cycle, the audit prompt's "CIC × CLC orthogonality" rubric (mirroring §2 v7.2 §11.3) MUST verify no implicit coupling slipped into the goal schema, the Cedar rules, the Scout DISCOVER ranking function, or the Match DB scoring composer.

## §9.1 HARD-LOCKED elements (Thesis cannot relitigate)

- A12 Decimal mandate for `target_amount_minor_units` (int minor units; no float; AST-lint ban) per v7.0.4-M1 §6.
- `write-if-absent` discipline + re-key path for status mutations per §2 v7.2 §1.
- CIC × CLC orthogonality (six × eight, no pre-mapping) per v7.0.8 + CLAUDE.md.
- F-CLASS-* opaque-slot-only outbound boundary (any cloud-routed `purpose` field uses `[SLOT_<numeric_id>]` per v7.0.7 §1).
- Law 3 Org Isolation — goals live under `orgs/{slug}/vault/operational/funding_goals/` per §2 v7.2 §5.
- §2 v7.2 sub-kind registry pattern (single canonical `SUB_KIND_REGISTRY` mapping; downstream callers bind through the registry, never hardcode intent strings).

## §9.2 OPEN QUESTIONS for the Thesis dispatch (Thesis-resolvable; operator-overridable)

- Module/sub-code collapse for F-GOAL-SCHEMA-INVALID family (§6 OQ-9).
- Whether `scoring-callable` warrants its own §0.5 primitive_kind row or routes under `interface-contract` (§4.4 OQ-7).
- Whether `FundingGoal.purpose` default classification is `shareable` or `confidential` (§3.3 OQ-6).
- Whether F-GOAL-* joins F-CLASS-COVERAGE-INCOMPLETE's `REQUIRED_F_CLASS_CODES` (§6 OQ-10).
- Match-DB schema bump versioning: does `match_database.v1 → v2` warrant a paired migration shim (per v7.0.4-M1 §2 legacy-migration discipline) or is v0.1 / v0.2 schema-of-record the only on-disk shape? (NEW Thesis Q — call it OQ-11.)

# §10. v0.1 vs v0.2 boundary table

| Element | v0.1 Beta | v0.2 first wave | v1.x / horizon |
|---|---|---|---|
| `FundingGoal` schema + sub-kind registry row | **OQ-1 dependent** — operator decides if goals ship in v0.1 Beta or are v0.2 | **OQ-1 dependent** | — |
| §3 Scout DISCOVER goal-aware input shape | **OQ-1 dependent** | **OQ-1 dependent** | — |
| Match DB schema bump → v2 (`contributes_to_goals` + `goal_aware_match_score`) | **OQ-1 dependent** | If v0.1 ships goals, Match DB v2 ships paired | — |
| §4 v2.x.1 F-GOAL-* family realization (Cedar/Python predicates) | If v0.1 ships goals, predicates ship paired | Predicate bodies could land at v0.2 as a follow-on amendment if v0.1 LOCKs the schema-only surface | — |
| F-GOAL-LINKED-CYCLE-ORPHAN + F-GOAL-DEADLINE-EXPIRED-IGNORED (advisory) | **v0.2** — these surface across multi-cycle reads; v0.1 single-cycle reads do not need them | **v0.2** | — |
| Monday fund-radar goal-aware brief format | **v0.1 ready** — extends an already-shipping routine; zero new substrate | — | — |
| Push-notify CRITICAL-FIT-AGAINST-GOAL via macOS Notification Center (option C) | Forward-design marker | **v0.2 candidate** (operator-decision) | — |
| Push-notify via Cultivator Telegram bot (operator-to-self) | — | **v0.2 first wave** — natural home post-§13 LOCK | — |
| `tilth-vault rekey-goal-status` CLI wrapper | — | **v0.2** — same v0.2 CLI work track as `tilth-vault rekey-record` per §2 v7.2 §10 | — |
| Goal-aware Scribe prompt context-injection | — | **v0.2** — Scribe seat reads active goals at preflight and includes them in dialogue with operator | — |
| `tilth funding-goal *` CLI verbs (create / list / status-change) | If v0.1 ships goals, basic CLI ships paired | — | — |
| Multi-org / Stage-2 fleet aggregation of goals | — | — | **Stage 2 (12-Tilth fleet milestone)** — out of scope for v0.1 / v0.2 |
| Stage-5 commons goal-pattern composability | — | — | **Stage 5** — per cooperative sovereignty consent tiers; out of scope per CLAUDE.md "Do not propose substrate replacements for v0.1" + v7.0.5 §4 commons-corpus on-ramp |

# §11. Open questions for Josh (operator-decision-required-first per `pipeline/planning/v0_2_dispatch_plan_2026-05-09.md` decision-log convention)

These are the decisions the spec cannot resolve from the locked corpus. Each is framed with the trade-offs so Josh can decide quickly.

**OQ-1 — Ship window: v0.1 Beta or v0.2 first wave?**
- **v0.1 Beta**: goal primitive ships paired with §13 v1 + §4 v2.x + Classification Review wrapper before first paid Beta deployment. Trade-off: extends the v0.1 Beta scope by ~one compound LOCK family (estimated 1 Cowork Thesis + 1 Code phase + 1 Pre-stage = ~3 sessions). Aligns with "per-cycle drafter → per-org strategist" framing, which is brand-aligned ("Strong organizations are not short on substance — they lack funding infrastructure").
- **v0.2 first wave**: defer goal primitive to the v0.2 reporting vertical. Trade-off: v0.1 Beta clients don't get goal-aware DISCOVER or Monday briefs in their first cycle; the strategist framing lands at v0.2 production cut.
- **v0.2 second wave**: defer further (after Data Collector + Report Generator are stable). Trade-off: pushes goal-aware Match DB scoring past the v0.2 production cut.
- *Recommended default if Josh under-specifies: **v0.2 first wave***, because v0.1 Beta is paper-light right now per memory `project_classification_review_ux_wrapper_2026-05-10` ("remaining v0.1 Beta items: README + CLAUDE.md + ARCHITECTURE_OVERVIEW v0.1 Beta launch posture section"), and adding a goal-primitive compound LOCK extends Beta scope.

**OQ-2 — §6 amendment shape: extend §6 v1-r1 with a goals-block injection clause, or extend §3 v5 with a DISCOVER input-shape clause (or both)?**
- §6 v1-r1 hosts the prompt-template compilation pipeline (§6.11) and is the natural home for "what blocks the start-block + end-block injection carries." A §6.1x amendment would add a goals-block to the load-bearing constraints set.
- §3 v5 is the DISCOVER seat blueprint and is the natural home for "what DISCOVER reads as input from the operator's org context."
- Both — most defensible; one amendment per concern.
- *Recommended default: **both**, with §3 owning the input-shape and §6 owning the prompt-compilation. Adds a §3 v6 amendment + a §6.2 minor amendment to the compound LOCK family.*

**OQ-3 — Past-deadline goal at construction: reject, or permit with WARNING-tagged status?**
- Reject: §2.2 invariant 5 rejects new `FundingGoal` records whose `target_deadline < created_at[:10]` if status is `pursuing` or `blocked`. Operator cannot create an already-expired pursuit.
- Permit with WARNING: allow operator to create historical goals (e.g., importing a goal from a prior funding cycle that has already lapsed but operator wants to track it for retrospection).
- *Recommended default: **reject***, mirroring the v7.2 lex-compare discipline (`ended_at > started_at` in `TimelineActivity`). Importing historical goals = use AWARD_INGEST or operator-direct vault write.

**OQ-4 — RED severity on blocked goals: yes, or stay YELLOW?**
- RED: matches v7.2 BeneficiaryRecord PII-present convention (severity discriminated by a record-level flag). Forces blocked goals into admin-risk surfacing every cycle.
- YELLOW: simpler; blocked is operator-internal state, not a per-cycle admin-risk event.
- *Recommended default: **RED***, because a blocked goal IS a per-cycle operator decision surface (e.g., "do we keep pursuing this $480K goal after USDA RFSI declined?").

**OQ-5 — Goal status mutation: thin resolution helper (`funding_goals.resolve_live(...)`) or seat-side walk?**
- Thin helper: cleaner ownership; one place to test; matches v7.2 sub-kind registry pattern.
- Seat-side walk: each consumer (Scout REVIEW, Match DB scoring, Monday brief) implements its own admin-risk-ledger walk; more flexibility, more risk of drift.
- *Recommended default: **thin helper***, because the §2.5 re-key path already adds operator overhead and tools should subtract overhead.

**OQ-6 — `FundingGoal.purpose` default classification: `shareable` or `confidential`?**
- `shareable`: most goal statements are public-facing ("regional food-hub buildout"). Cloud-routed Scout channels and Scribe seat see the purpose verbatim.
- `confidential`: goal-revenue-strategy adjacency. Cloud-routed seats get `[SLOT_<numeric_id>]` opaque-fill per v7.0.7. Local slot-fill agent renders the value into post-fill drafts only.
- *Recommended default: **shareable** (Card-level archetype default), with per-org operator override at white-glove and per-grant SP0 override per v7.0.7 §3.6 three-layer pattern.*

**OQ-7 — `scoring-callable` as new §0.5 primitive_kind, or route under `interface-contract`?**
- New kind: cleaner type discrimination in the index; matches the "deterministic Python composition function" semantic.
- `interface-contract`: minimum-vocabulary-extension discipline; the row's `defined_at` field documents the semantic.
- *Recommended default: **interface-contract** (minimum extension).*

**OQ-8 — Status transition closure: how permissive?**
- Default proposed (§6 F-GOAL-STATUS-TRANSITION-INVALID): `met → pursuing` forbidden; `abandoned → pursuing` permitted; all others permitted.
- More permissive: every transition permitted; operator-discipline at the admin-risk ledger.
- More restrictive: e.g., `abandoned → pursuing` also forbidden (an abandoned goal stays abandoned; operator mints new goal).
- *Recommended default: **as proposed in §6***.

**OQ-9 — F-GOAL-SCHEMA-INVALID family: sub-code collapse or one-module-per-code?**
- Sub-code collapse (§6 default): five modules realizing eight codes; matches v2.2 F-AMDT-08/09/10/11 + v2.x F-CLASS-* precedent.
- One-module-per-code: eight modules realizing eight codes; cleaner ownership, larger module count.
- *Recommended default: **collapse***.

**OQ-10 — F-GOAL-* in F-CLASS-COVERAGE-INCOMPLETE META gate registry?**
- Include: every F-GOAL-* code participates in the META gate's `REQUIRED_F_CLASS_CODES` registry; Beta deployment cannot ship without each code having a live module + test on disk. Adds eight codes to the META gate's coverage check.
- Exclude: F-GOAL-* is a v0.2 family (per OQ-1 default); the META gate's contract is "v7.0.7 §5.1 codes" only; F-GOAL-* is structurally outside the F-CLASS-* family the META gate audits.
- *Recommended default: **exclude*** — F-GOAL-* is its own family with its own coverage discipline; the META gate stays focused on F-CLASS-* per its current contract.

**OQ-11 — Match DB schema bump v1 → v2: migration shim or schema-of-record only?**
- Migration shim: per v7.0.4-M1 §2 legacy-migration discipline, any existing `match_database.v1` registers get a one-time migration to v2 at WS-FG LOCK. Trade-off: v0.1 has zero `match_database.v1` registers on disk today (per my knowledge of the repo state), so the shim is empty-execute.
- Schema-of-record only: v2 is the on-disk shape; no migration needed.
- *Recommended default: **schema-of-record only***, with a documentary note in the §4.1 amendment saying "no v1 registers existed on disk at the time of v2 LOCK; future schema bumps from v2 onward MAY require a migration shim per v7.0.4-M1."

**OQ-12 — Push-notify v0.1 surface: option D (CLI-on-next-run) + option A (Monday brief) only, or also wire option B (BYOK SMTP) or option C (macOS Notification Center)?**
- D+A only: zero new substrate; ships in v0.1 with the rest of the family.
- D+A+B: BYOK SMTP push at VERIFY close; medium effort; always-local routing (no Law 4 / TCPA concern; operator-to-self).
- D+A+B+C: macOS Notification Center via `osascript`; Mac-pinned UI surface (Josh's M1 dev node + Pro tier are both macOS — works today; Linux Pro DGX Spark would need a different surface).
- *Recommended default: **D+A only*** for v0.1; B+C as v0.2 candidates per operator request.

---

# §12. Pre-dispatch checklist (self-check before this spec is handed to a Thesis-dispatch session)

Per `pipeline/engineering/engineering_process_v0.1.md` §11 Done definition pattern, this spec's done-definition is:

- [x] §11 spec-card template followed (header + parent locks + dispatch_class + L-005 review note).
- [x] §2 v7.2 sub-kind convention followed exactly (frozen kw_only; canonical bytes codec; SUB_KIND_REGISTRY row; vault subtree; admin-risk severity; SIMPLE write-if-absent).
- [x] A12 Decimal mandate respected (no float fields; int minor units; explicit-context-required helper; AST-lint ban referenced).
- [x] CIC × CLC orthogonality preserved (no pre-mapping in schema, Cedar, scoring, or DISCOVER).
- [x] Law 3 Org Isolation enforced at three layers (Cedar default-permit; F-GOAL-CROSS-ORG-LEAK defense-in-depth; vault subtree path).
- [x] F-CLASS-* opaque-slot discipline applied to outbound boundary on cloud-routable seats reading goals (§3.3).
- [x] §0.5 row range allocated correctly from row 377 (current runtime-live = 376).
- [x] L-005 two-cycle Thesis discipline notes flagged (HARD-LOCKED vs OPEN QUESTIONS distinction).
- [x] v0.1 vs v0.2 boundary table explicit.
- [x] Open questions for Josh enumerated with trade-offs and recommended defaults.
- [x] No Python written (SPEC, not implementation).
- [x] No LOCK ceremony invoked.
- [x] Path-only references (no content dumps of locked sections per L-002).

# §13. Changelog

- 2026-05-10 v1 DISPATCH_SPEC_DRAFT filed. Grounded in §2 v7.2 LOCKED 2026-05-10, §6 v1-r1 LOCKED 2026-04-21, §3 v5 LOCKED 2026-04-17, §4 v2.x LOCKED 2026-05-10 (rows 193/194), §0.5 v15 LOCKED 2026-05-10 (runtime-live 376), §11 v1 LOCKED 2026-05-10, architecture v7.0.4-M1 + v7.0.5 + v7.0.7 + v7.0.8 LOCKED state. Open-question count: 12. Awaiting Josh's OQ-1 ship-window decision before Thesis dispatch.
