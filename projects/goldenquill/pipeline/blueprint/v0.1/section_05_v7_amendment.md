---
title: Blueprint §5 Pipeline — Amendment v7 (Red Team in inner loop alongside Judge)
filed: 2026-05-01
operator: Josh
amendment_status: **LOCKED 2026-05-02** — v7 LOCKED under L-005 strict two-cycle. Round 1 + Round 2 audited the §10 v1 + §5 v7 + §0.5 §10 amendment compound transaction (synthesis at `pipeline/validation/section_10_thesis_round_1/synthesis.md`; closeout at `pipeline/validation/section_10_thesis_round_2/CLOSEOUT.md`). Zero findings specific to §5 v7 amendment surfaced across both rounds; Judge scored §5_v7_amendment_narrowness 10/10 in Round 1 and re-affirmed at Round 2. §5 v7 amendment-text UNCHANGED through both rounds (sha `7355080bef0faad4` preserved). LOCKs as compound transaction with §10 v1.1 + §0.5 v8 per §6.17 Option-B paired-commit pattern.
parent_lock: pipeline/blueprint/v0.1/section_05_pipeline.md (§5 v6 LOCKED 2026-04-19; §5 LOCKED-as-a-whole-section R13 capstone 2026-04-29 row 131)
companion_amendments:
  - pipeline/blueprint/v0.1/section_10_red_team.md (§10 v1 SCOPING DRAFT 2026-05-01 — adversarial-review seat blueprint; this amendment wires §10's seat-lifecycle into §5's inner loop)
  - pipeline/blueprint/v0.1/section_00_5_section_10_red_team_amendment.md (§0.5 §10 amendment — ~50 row-append at compound LOCK)
architecture_parent: pipeline/architecture/v0.1/tilth_architecture_locked.md (v7 A1-A12 LOCKED 2026-04-19; §A3 SFR mandates Red Team verdict format; §E cross-family rigor; §F.1 F-VERDICT-CERT-MALFORMED; §M13 review-seat outage escape valve)
prerequisite_interlock: §10 Red Team v1 SCOPING DRAFT (LANDED 2026-05-01) — pins shapes (RedTeamVerdict, RedTeamCriterionScore, AttackMemo, Weakness, TotalScoreCorrection, RedTeamInput, CouncilSplitDecision) and seat lifecycle. §5 v7 amendment consumes these shapes and wires them into the §5 inner loop.
discipline: L-005 two-audit + Section 13 audit-binding; F-INDEX-STALE PRE-gate; Five Laws (Section E)
bundling_rationale: §10 Red Team is the LAST unsealed-as-a-whole council seat; wiring it into §5's inner loop is the gate to §10 v1 LOCK. Compound transaction with §10 v1 + §0.5 §10 amendment closes the §10 build chain at the blueprint layer in one atomic LOCK.
paired_commit_sec00_5: 2 new §0.5 rows for §5 v7 surface (RT_DISAGREEMENT_THRESHOLD constant, RT_ANCHOR_SUSPECTED_THRESHOLD constant) + the ~50 §10 rows from §10 v1 LOCK paired commit
---

## Amendment intent

§5 v6 LOCKED 2026-04-19 specifies the inner loop as Scribe → Editor → Judge → POST-gate → operator-signoff → tab-delivery. Red Team is not in v6's lifecycle. §10 Red Team v1 SCOPING DRAFT (LANDED 2026-05-01, sha `2b2c0c61e1325f0a`) pins the seat-lifecycle but cannot LOCK without §5 wiring it into the inner loop alongside Judge.

This amendment is **narrow and bounded**:

1. **Adds §4.5a Red Team invocation** as a peer to §4.5 Judge invocation; fires AFTER Judge returns each iteration.
2. **Extends §4.6 revision-loop control** to invoke Red Team after Judge per iteration; both verdicts checkpoint BEFORE iteration advances.
3. **Extends §4.7 POST-gate invocation** with F-COUNCIL-SPLIT routing — when `|judge_score - red_team_score| ≥ RT_DISAGREEMENT_THRESHOLD`, transition to new sub-phase `signoff_pending_council_split` (a sub-state of `signoff_pending`).
4. **Extends §3.2.1 RunState** with three new fields: `red_team_verdict_ref: str | None`, `council_split_decision: CouncilSplitDecision | None`, plus the new `signoff_pending_council_split` phase Literal.
5. **Adds §6 failure code F-COUNCIL-SPLIT** with sub-tags `.exceeds_threshold` (the primary trigger) and `.no_decision_at_signoff` (operator advanced past sign-off without choosing).
6. **Adds §8 constants** RT_DISAGREEMENT_THRESHOLD: Final[int] = 10 and RT_ANCHOR_SUSPECTED_THRESHOLD: Final[int] = 2 with module-load integrity asserts (V1 inline-literal rebind-resistance pattern, mirroring TAB_ORDERING discipline).
7. **Adds §9 tests** for council-split detection, anti-averaging invariant, 3-way cross-family distinct, anti-anchoring smoke check.
8. **Adds §11 Law map row** for §10 Red Team's Five-Laws enforcement integration.
9. **Names but does NOT specify** §3 Modules addition `pipeline.seats.red_team` — that R1 production seat is a downstream round (§10 R1) consuming this amendment.

This is a targeted amendment. Existing §5.1–§5.10 (submission_mode run-lifecycle), §4.12 (eval_mode), §5.6 (forward-dep predicates), §5.7 (InvocationRecord schema from v6), §5.8 (STR derivation), all failure codes F-PIPE-01 through F-PIPE-23, all v5/v6 invariants, and all v5/v6 §10 OQs are preserved without change. The amendment adds new surface; it does not touch existing surface.

---

## §3.2.1 RunState — three new fields + one new phase Literal

The v6 RunState shape (preserved verbatim) extends with three new fields and one new phase Literal value. Schema version bumps from `2` (v6) to `3` (v7).

```python
@dataclass(slots=True)
class RunState:
    schema_version: int  # v7: bumped to 3 (red_team_verdict_ref + council_split_decision + signoff_pending_council_split)
    # ... all v6 fields preserved verbatim ...
    phase: Literal[
        # ... v6 phases preserved ...
        "signoff_pending",
        "signoff_pending_council_split",  # v7 NEW: F-COUNCIL-SPLIT routes here from POST-gate; operator must choose before report_signed
        # ... rest v6 ...
    ]
    # v7 NEW fields:
    red_team_verdict_ref: str | None  # vault path to current iteration's RedTeamVerdict; mirrors judge_verdict_ref pattern
    council_split_decision: CouncilSplitDecision | None  # operator's binary decision (PROCEED-WITH-JUDGE / PROCEED-WITH-RED-TEAM / REVISE / DROP); set at signoff_pending_council_split exit
```

**`CouncilSplitDecision` shape (frozen, kw_only, slots=True; LOCKed at this amendment as part of §10 v1 paired commit):**

```python
@dataclass(frozen=True, kw_only=True, slots=True)
class CouncilSplitDecision:
    decision: Literal["proceed_with_judge", "proceed_with_red_team", "revise", "drop"]
    judge_total_score: int
    red_team_total_score: int
    delta_absolute: int  # = abs(judge_total_score - red_team_total_score); MUST equal RT_DISAGREEMENT_THRESHOLD or higher (POST-gate invariant)
    operator_signoff_at_iso: str  # ISO 8601 UTC at moment operator chose
    operator_rationale: str  # ≤ 480 chars; ledger-stamped HIGH-severity to admin-risk register at decision time
```

**Schema-version migration discipline.** Schema bump v6 → v7 follows the v5 → v6 pattern (B-v1-08 + v5 MA-07/MB-05 closures). `_assert_runstate_schema_current(rs)` predicate (v5 addition) is updated to require `schema_version == 3`; resume of a v6 RunState (`schema_version=2`) trips F-PIPE-22.runstate_schema_downgrade and writes `state-failure` checkpoint.

**v7 mode-discriminated-union invariants (extending v4/v5 invariants).**
- `mode == "submission"` ⟹ `red_team_verdict_ref` is non-None after Red Team has fired in any iteration; `council_split_decision` is non-None iff `phase == "signoff_pending_council_split"` has been entered (set at exit, before transition to `report_signed`).
- `mode == "eval"` ⟹ `red_team_verdict_ref` is None throughout (eval_mode does not invoke Red Team — calibration scoring is Judge-only); `council_split_decision` is None throughout.
- A run in `signoff_pending_council_split` cannot transition to `report_signed` while `council_split_decision is None` — F-COUNCIL-SPLIT.no_decision_at_signoff is raised on attempted advancement.

---

## §4.5a (NEW v7) — Red Team invocation

**Trigger.** Fires AFTER Judge returns each iteration (v7 §4.6 amendment names the trigger; this subsection specifies the seat-call mechanics).

**Sequence (v7):**

1. Read JudgeVerdict from current iteration's checkpoint (`run_state.judge_verdict_ref` resolves via `vault_read` SIMPLE path).
2. Compose `RedTeamInput` per §10.3 (consumes the same `SectionDraft[]` Scribe emitted + the same `claim_evidence_map` + `RfaExtractedRecord` + `rubric` + `judge_verdict` + `funder_dialect` + `admin_risk_register_snapshot` that Editor and Judge consumed).
3. Verify cross-family discipline (§10.7): `F-RT-FAMILY-OVERLAP` PRE-gate compares Red Team's resolved family against `run_state.run_iteration_families_so_far["scribe"]` AND `["judge"]` — collision against EITHER hard-aborts.
4. Resolve provider via `ProviderCascade` reordered to skip {scribe_family, judge_family}; if reorder leaves the cascade empty, `F-RT-NO-COMPLIANT-FAMILY` raised (M13 escape-valve required).
5. `seat_launch` (Section 2 v7 §3.5) constructs subprocess with MINIMAL env (matches §4.3/§4.4/§4.5 v2 A-v1-13 closure); seat-binding for vault-read of API key.
6. Streamed model output parsed per §10.4 SFR three-block format; `RedTeamVerdict` constructed per §10.5.
7. Tuple return: `(red_team_verdict_hash, landed_family, landed_model_id)` — same return-shape as Scribe/Editor/Judge (v6 A-v1-02 closure).
8. `run_state.run_iteration_families_so_far["red_team"] = (landed_family, landed_model_id)` immediately on return — BEFORE any subsequent seat call (closes A-v1-02 ordering race for Red Team).
9. Write `RedTeamVerdict` to vault under `orgs/<slug>/drafts/<run_id>/iterations/<n>/red_team_verdict.json` via SIMPLE `vault_write`; pin `red_team_verdict_ref` on `run_state`; checkpoint.
10. Run Logician POST-gate per §4.7 (extended in this amendment to evaluate F-COUNCIL-SPLIT alongside the v6 POST-gate row set).

**Telemetry.** Same `InvocationRecord` (§5.7 from v6 amendment) schema applies — Red Team is just another seat in the registry. `seat = "red_team"`.

**Iteration-cap participation.** Red Team fires every iteration alongside Judge (max 3 iterations per architecture; OQ-10.2 in §10 SCOPING DRAFT confirmed at this amendment). Tokens-per-iteration roughly doubles vs v6 (Judge + Red Team both fire); this is acceptable for v0.1 (operator's BYOK; cost passes through to operator). v0.2 may add `--red-team-final-iteration-only` toggle as a cost-optimization, but per v1 LOCK the every-iteration default is preserved for symmetry with Judge and for full per-iteration adversarial pressure.

**Bypass.** M13 review-seat outage escape valve applies (architecture §M13). `red_team_bypass_authorization_ref: str | None` is read from `run_state` (NEW v7 sub-field of the existing `bypass_authorization_ref` family); when present and signed and unexpired, Red Team invocation is skipped with rigor-breach flag in rails report. Default remains hard-abort on review-seat outage.

---

## §4.6 (v6 → v7 amendment) — Revision-loop control with Red Team

The v6 inner-loop sequence Scribe → Editor → Judge becomes Scribe → Editor → Judge → Red Team. Both Judge and Red Team verdicts are checkpointed BEFORE iteration advances. Per-iteration writes (v6 ordering preserved with v7 addition):

1. Scribe call → `IterationState.scribe_draft_ref` set + checkpoint.
2. Editor call → `IterationState.editor_findings_ref` set + checkpoint.
3. Judge call → `IterationState.judge_verdict_ref` set + checkpoint (v6 A-v1-15 closure preserved: success-checkpoint occurs AFTER Judge parse succeeds).
4. **Red Team call (v7 NEW)** → `IterationState.red_team_verdict_ref` set + checkpoint. If Red Team parse fails after retry (§10 SFR three-block parser), iteration is written as `state-failure` with `red_team_verdict=None, failure_code=F-RT-VERDICT-CERT-MALFORMED`. Never recorded as success.
5. Convergence-or-advance decision: same v6 semantics for revision-loop continuation, BUT v7 extends: if `|judge_total_score - red_team_total_score| ≥ RT_DISAGREEMENT_THRESHOLD` AND iteration ≥ 1 (Scribe has had at least one revision pass), the loop EXITS with the council-split signal — no further revision iterations run, run transitions to `post_gate_pending` (then `signoff_pending_council_split` per §4.7 v7).

**Why exit on council-split rather than revise.** A 10+ point gap between Judge and Red Team is not a draft quality signal — it's a council-disagreement signal. Further Scribe revisions cannot resolve seat-disagreement; only the operator can. Continuing to revise would burn tokens on a draft whose verdict will be operator-broken regardless.

**Iteration-cap interaction.** v6's max-3-iterations cap is unchanged. Council-split exit is an EARLY exit; if it fires on iteration 1, iterations 2 and 3 are not run. The exit cause is recorded in `run_state.iterations[*].exit_reason: Literal["converged", "max_iterations", "council_split"]` (v6 had `"converged"` and `"max_iterations"` only; v7 adds `"council_split"`).

**Soft-restart guard preserved.** v2's A-v1-10 closure (F-PIPE-19.soft_restart_forbidden — once `inner_loop_iter_N` with N≥1, no transition back to lower N) still applies. Council-split exit is a forward transition (loop_iter_N → post_gate_pending), not a soft-restart.

---

## §4.7 (v6 → v7 amendment) — POST-gate invocation with F-COUNCIL-SPLIT

The v6 POST-gate row set is preserved verbatim. v7 adds ONE new row evaluated AFTER the v6 row set (so a draft that fails any v6 POST-gate row never reaches F-COUNCIL-SPLIT — F-COUNCIL-SPLIT presumes the draft is otherwise gateable):

| # (v6 ordering preserved) | Check | Source |
|---|---|---|
| ... v6 POST-gate rows 1..N preserved ... | ... | ... |
| N+1 (v7 NEW) | F-COUNCIL-SPLIT: if `abs(judge_total_score - red_team_total_score) >= RT_DISAGREEMENT_THRESHOLD` → transition to `signoff_pending_council_split` instead of `signoff_pending`. Non-blocking on run; blocking on auto-advancement to `report_signed`. | §10.6 |

**Ordering rationale.** F-COUNCIL-SPLIT runs AFTER all v6 deterministic POST-gates because (a) F-COUNCIL-SPLIT is dispatch-only — it routes to operator UI but does not refuse the draft, and (b) the operator's UI presentation needs all the gate-pass-status context from v6 rows. If a v6 POST-gate hard-fails, the draft is rejected and the operator never sees the council-split decision UI; F-COUNCIL-SPLIT never fires in that path.

**Anti-anchoring smoke check.** F-RT-JUDGE-ANCHOR-SUSPECTED (§10.6) is evaluated AFTER F-COUNCIL-SPLIT in the same POST-gate batch but is NON-BLOCKING — it surfaces only as an admin-risk LOW-severity entry visible at sign-off. The smoke check fires when `abs(judge - red_team) < RT_ANCHOR_SUSPECTED_THRESHOLD` AND `len(rubric.criteria) >= 5` AND `total_words(section_drafts) >= 1000`.

---

## §6 (v7) Failure code addition — F-COUNCIL-SPLIT

### F-COUNCIL-SPLIT

POST-gate (§4.7 v7 row N+1): operator-routing failure code emitted when Judge and Red Team disagree by ≥ RT_DISAGREEMENT_THRESHOLD points. Routes to `signoff_pending_council_split` phase. Sub-tags:
- `.exceeds_threshold` — primary trigger; `delta_absolute >= RT_DISAGREEMENT_THRESHOLD`.
- `.no_decision_at_signoff` — secondary trigger; operator advanced past `signoff_pending_council_split` without setting `council_split_decision` (state-machine invariant violation).

Non-blocking on run-validity; blocking on auto-advancement to `report_signed` (operator decision required to advance).

### F-RT-JUDGE-ANCHOR-SUSPECTED

POST-gate (§4.7 v7 row N+2): non-blocking advisory. Triggers on suspiciously-close Judge-vs-Red-Team agreement on a non-trivial draft. Surfaces as admin-risk LOW-severity entry; visible at sign-off; does not block run. Sub-tags none — single-trigger advisory.

---

## §8 (v7) Constants — two additions + module-load asserts

```python
RT_DISAGREEMENT_THRESHOLD: Final[int] = 10
"""Council-split detection threshold per §10.6. Disagreement of 10 or more
points on a 100-point rubric routes through F-COUNCIL-SPLIT. Operator-
configurable per-org via PROJECT_CONTEXT.rt_disagreement_threshold_override."""
assert RT_DISAGREEMENT_THRESHOLD == 10, (
    "RT_DISAGREEMENT_THRESHOLD has been rebound at module load; refusing "
    "to load pipeline.config — V1 inline-literal rebind-resistance discipline "
    "(parallel to TAB_ORDERING from v3 V1 closure)"
)

RT_ANCHOR_SUSPECTED_THRESHOLD: Final[int] = 2
"""Anti-anchoring smoke check threshold per §10.6. Disagreement strictly less
than 2 points on a non-trivial draft (≥ 5 criteria + ≥ 1000 words) emits
F-RT-JUDGE-ANCHOR-SUSPECTED non-blocking advisory."""
assert RT_ANCHOR_SUSPECTED_THRESHOLD == 2, (
    "RT_ANCHOR_SUSPECTED_THRESHOLD has been rebound at module load; refusing "
    "to load pipeline.config"
)
```

**Operator override.** `PROJECT_CONTEXT.rt_disagreement_threshold_override: int | None` (default None → use the module constant). Override is ledger-stamped Medium-severity at Phase 0 (§10.6); a per-org override carries an override-ID that flows into the rails report.

**No override on RT_ANCHOR_SUSPECTED_THRESHOLD** — the smoke check is advisory; operator already controls whether to act on the advisory at sign-off.

---

## §9 (v7) Tests — new property + adversarial + integration tests

Add to §9.9 (v6 had subsections 27-35; v7 adds 36-44):

### 9.9.36 test_red_team_fires_after_judge_per_iteration
Property test over 100 fuzzed runs: for every `IterationState`, `red_team_verdict_ref` is None until `judge_verdict_ref` is non-None.

### 9.9.37 test_council_split_threshold_inclusive_at_10
Synthetic Judge=85, Red Team=75 (delta exactly 10); F-COUNCIL-SPLIT.exceeds_threshold fires (boundary inclusive). Synthetic Judge=85, Red Team=76 (delta 9); F-COUNCIL-SPLIT does NOT fire (strict inequality boundary).

### 9.9.38 test_council_split_routes_to_signoff_pending_council_split
Synthetic delta ≥ 10; phase transitions to `signoff_pending_council_split` not `signoff_pending`. Operator-signoff prompt receives both verdicts + per-criterion delta map.

### 9.9.39 test_council_split_advance_blocked_without_decision
With `phase == "signoff_pending_council_split"` and `council_split_decision is None`, attempted transition to `report_signed` raises F-COUNCIL-SPLIT.no_decision_at_signoff and writes state-failure checkpoint.

### 9.9.40 test_three_way_family_distinct_invariant
Property test over 1000 router cascade draws (with realistic family-priority weights): Red Team's resolved family is never equal to Scribe's resolved family AND never equal to Judge's resolved family. F-RT-FAMILY-OVERLAP fires on every collision attempt.

### 9.9.41 test_no_score_averaging_in_pipeline
AST-grep test scans `pipeline/` for the patterns:
- `(judge_score + red_team_score) / 2`
- `(judge_total_score + red_team_total_score) / 2`
- `mean(judge_score, red_team_score)`
- `(judge.total_score + red_team.total_score) / N` for any N
None must appear anywhere in `pipeline/`. Anti-averaging invariant per §10.6.

### 9.9.42 test_rt_disagreement_threshold_module_load_integrity
Module-load assert for `RT_DISAGREEMENT_THRESHOLD == 10` (V1 inline-literal pattern). Mutates the constant in a test process and asserts re-import raises.

### 9.9.43 test_anti_anchoring_smoke_check_advisory_only
Synthetic Judge=85, Red Team=86 (delta 1, < 2) on a 7-criterion 1500-word draft; F-RT-JUDGE-ANCHOR-SUSPECTED fires as admin-risk LOW-severity entry; phase advances normally to `signoff_pending` (NOT split); run completes. Smoke check is advisory, never blocks.

### 9.9.44 test_red_team_eval_mode_isolated
Property: `mode == "eval"` runs never invoke Red Team. `red_team_verdict_ref` stays None throughout. Eval-mode is calibration-scoring-only (Judge alone scores against the operator's golden set).

---

## §11 (v7) Law map — Red Team enforcement integration

Add row:

| Architecture obligation | Gate | Check | v7 addition |
|---|---|---|---|
| §10 Red Team Five-Laws enforcement (Law 1 evidence-in-draft / Law 2 boundary-drift critique vector / Law 3 single-PROJECT_CONTEXT / Law 4 admin-risk-flagging in verdict prose / Law 5 unsupported-assertions critique) | PRE + POST | §10.2 + §4.5a (PRE), §4.7 v7 (POST) | New row: F-RT-* family enforces all five laws on Red Team's input + verdict; F-COUNCIL-SPLIT routes operator decision per Law 4 (cross-family rigor + operator-tie-breaker) |

---

## §10 OQ amendments

OQ-1 through OQ-10 from v5/v6 preserved unchanged.

**OQ-11 (NEW v7):** Red Team's bypass authorization scope under M13. Per architecture §M13, operator-signed bypass authorizations are per-review-seat. Does Red Team's bypass also bypass F-COUNCIL-SPLIT (since with Red Team bypassed, no second score exists to disagree with Judge)? Recommendation: when `red_team_bypass_authorization_ref is not None`, F-COUNCIL-SPLIT is structurally impossible (no Red Team verdict to disagree); rails report carries the rigor-breach flag. Confirm at Thesis Round 1.

**OQ-12 (NEW v7):** Red Team participation in eval_mode. v7 amendment names eval_mode-isolation invariant (Red Team does not fire in eval). Is this correct? Eval_mode is Judge-only calibration against golden sets. Recommendation: confirmed at this amendment; Red Team is submission_mode-only at v0.1. v0.2 may extend eval_mode to include Red Team for adversarial calibration (operator opt-in).

---

## §12 Non-ownership

Unchanged from v6. §5 v7 amendment does NOT specify §10 Red Team's seat internals (those live in §10 v1 SCOPING DRAFT and the future §10 R1 production seat). §5 v7 specifies ONLY the inner-loop wiring and the POST-gate routing; how Red Team produces its verdict is §10's concern.

---

## §13 Closure — forward-dependency contract

This amendment introduces ONE forward dependency:
- **§10 v1 LOCK** (post Thesis Round 1+2 per §10.15 version history) is the prerequisite for THIS amendment to LOCK as a code-binding amendment. Until §10 v1 LOCK lands, this amendment is a SCOPING DRAFT and the production-code wiring (R1 production seat at `pipeline/seats/red_team/`) cannot consume it.

**Compound transaction option (Option-B per §6.17 / §7 v1.1.1 precedent).** §5 v7 + §10 v1 + §0.5 §10 amendment may LOCK as one atomic commit. Discipline: each gets its own lock_history row (per §6 v1-r1 + §7 v1.1.1 + §0.5 v6 paired-commit pattern), but all three LOCK at the same `lock_timestamp_utc` ± 60 seconds and reference each other via `companion_amendments` frontmatter.

---

## L-005 Audit record

**Status: SCOPING DRAFT — Thesis Round 1 not yet dispatched per BUDGET MODE per session prompt.** Same discipline as §10 v1 SCOPING DRAFT: shapes pinned, content authored; Thesis Team committee dispatch deferred to a future session.

When Round 1 dispatches, the expected verdicts:
- Editor: clarity-fixes + table-formatting nits.
- Judge: scoring against §5 amendment-discipline rubric (narrow-scoped? preserves v5/v6 surface? compound-transaction structure correct?).
- Red Team: adversarial (does the council-split mechanism leak between iterations? does the soft-restart guard interact with council-split exit? does the bypass scope leak to non-Red-Team seats? does eval_mode isolation hold?).

**Self-LOCK basis (this round only — SCOPING DRAFT, not v7 LOCK).** Pure-blueprint self-LOCK precedent: `section_04_v2_2_consolidated_amendment.md` (lock_history 2026-04-21, first `lock_class="blueprint"` row) + `section_04_v2_6_deferred_scope_amendment.md` (lock_history 2026-04-29) + `section_10_red_team.md` (lock_history 2026-05-01, this session — §10 v1 SCOPING DRAFT). SCOPING DRAFT only; no production code; no test code; no committee dispatch (BUDGET MODE per session prompt). Three audit questions all NO — (a) does NOT modify §5 v6 surface (only adds new surface); (b) does NOT introduce mechanisms not derivable from §10 SCOPING DRAFT + §4 v2.5 + arch §M13 (council-split is the §M13-adjacent operator-tie-breaker; cross-family is §4.16 subclass; constants follow V1 inline-literal pattern); (c) does NOT pre-empt paired commits (§10 v1 + §0.5 §10 amendment are explicit compound-transaction siblings).
