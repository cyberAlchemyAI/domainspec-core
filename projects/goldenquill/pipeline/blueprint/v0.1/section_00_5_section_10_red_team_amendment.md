---
title: §0.5 Blueprint Interface Index — §10 Red Team rows amendment (SCOPING DRAFT)
filed: 2026-05-01
operator: Josh
status: **LOCKED 2026-05-02** — v8 LOCKED as compound-transaction sibling to §10 v1.1 + §5 v7 amendment under L-005 strict two-cycle. Round 1 + Round 2 audited the compound transaction (synthesis at `pipeline/validation/section_10_thesis_round_1/synthesis.md`; closeout at `pipeline/validation/section_10_thesis_round_2/CLOSEOUT.md`). Zero findings specific to §0.5 §10 amendment surfaced across both rounds; Judge scored §0.5_§10_amendment_row_append_quality 10/10 in Round 1 and re-affirmed at Round 2. §0.5 §10 amendment-text UNCHANGED through both rounds (sha `3c7ca1612524a2ca` preserved). All 53 rows (159-211) promote from `stability_tier = "PARENT_UNLOCKED"` → `stability_tier = "STABLE"` at compound LOCK. Companion-file pattern matches §0.5 §6 + §0.5 §7 amendment files; runtime-live at compound LOCK.
parent_locks:
  - pipeline/blueprint/v0.1/section_00_5_interface_index_locked.md                      # §0.5 v5 LOCKED 2026-04-19 — 101 rows
  - pipeline/blueprint/v0.1/section_00_5_section_06_operating_envelope_amendment.md     # §0.5 v6 LOCKED 2026-04-21 (companion to §6 v1-r1) — rows 102-117
  - pipeline/blueprint/v0.1/section_00_5_section_07_scribe_amendment.md                 # §0.5 v7 LOCKED 2026-04-21 (companion to §7 v1.1.1) — rows 118-158
  - pipeline/blueprint/v0.1/section_10_red_team.md                                      # §10 v1 SCOPING DRAFT LANDED 2026-05-01 — sha 2b2c0c61e1325f0a; this amendment row-appends §10 primitives
  - pipeline/blueprint/v0.1/section_05_v7_amendment.md                                  # §5 v7 amendment SCOPING DRAFT 2026-05-01 — sha 7355080bef0faad4; this amendment row-appends two §5 v7 constants (RT_DISAGREEMENT_THRESHOLD, RT_ANCHOR_SUSPECTED_THRESHOLD)
kind_of_amendment: pure row-append (rows 159–211; ~53 new rows). NO vocabulary extension — every row's `primitive_kind` resolves against the v5-LOCKED + v6/v7-extended 16-value closed vocabulary.
dependency_order: §10 v1 SCOPING DRAFT + §5 v7 amendment + this §0.5 amendment land as a compound transaction at the same `lock_timestamp_utc` (Option-B per §6.17). All three SCOPING DRAFT this round; all three v1 LOCK at compound transaction post Thesis Round 1+2.
---

# Amendment §A — row append (rows 159–211)

Reproduced from §10 v1 SCOPING DRAFT §10.13 + §5 v7 amendment §8 Constants with kind-vocabulary alignment. All rows `stability_tier = "PARENT_UNLOCKED"` while parents are SCOPING DRAFT; promote to `STABLE` at compound v1 LOCK.

**Schemas (rows 159–166) — Red Team's 7 canonical shapes:**

| Row | Path | Kind | Parent |
|---|---|---|---|
| 159 | `red_team.input_bundle.v1` | schema | §10.3 |
| 160 | `red_team.verdict.v1` | schema | §10.5 |
| 161 | `red_team.criterion_score.v1` | schema | §10.5 |
| 162 | `red_team.attack_memo.v1` | schema | §10.5 |
| 163 | `red_team.weakness.v1` | schema | §10.5 |
| 164 | `red_team.total_score_correction.v1` | schema | §10.5 |
| 165 | `red_team.council_split_decision.v1` | schema | §10.6 + §5 v7 §3.2.1 |
| 166 | `red_team.iteration_state_extension.v1` | schema | §5 v7 §4.6 (`IterationState.red_team_verdict_ref` + `exit_reason` Literal extension) |

**Constants (rows 167–169):**

| Row | Path | Kind | Parent |
|---|---|---|---|
| 167 | `red_team.constant.rt_disagreement_threshold.v1` | constant | §5 v7 §8 — `RT_DISAGREEMENT_THRESHOLD: Final[int] = 10` (V1 inline-literal pattern) |
| 168 | `red_team.constant.rt_anchor_suspected_threshold.v1` | constant | §5 v7 §8 — `RT_ANCHOR_SUSPECTED_THRESHOLD: Final[int] = 2` (V1 inline-literal pattern) |
| 169 | `red_team.constant.recommendation_set.v1` | constant | §10.5 — closed Literal `{"competitive", "marginal", "not_ready"}` |

**Invariants (rows 170–174):**

| Row | Path | Kind | Parent |
|---|---|---|---|
| 170 | `red_team.invariant.three_way_family_distinct.v1` | invariant | §10.7 (strict 3-way: Red Team ≠ Scribe AND ≠ Judge); arch §E |
| 171 | `red_team.invariant.no_score_averaging.v1` | invariant | §10.6 (no `(judge + red_team) / N` anywhere in `pipeline/`); arch §F.1 |
| 172 | `red_team.invariant.computed_total_authoritative.v1` | invariant | §10.8 (`total_score == sum(c.score for c in criteria)`; auto-correction logged in `total_score_correction`) |
| 173 | `red_team.invariant.tier_matched_verbatim.v1` | invariant | §10.8 (`tier_matched` MUST be substring of `RubricCriterion.tier_descriptions[<tier>]`) |
| 174 | `red_team.invariant.evidence_substring_of_draft.v1` | invariant | §10.5 + §10.9 (every quoted evidence MUST be byte-identical substring of `SectionDraft.body_text`; Law 5 mirror) |

**Failure codes (rows 175–197) — 23 §10-owned Logician-registered codes (10 PRE + 12 POST + 1 forwarded-canonical):**

| Row | Path | Kind | Parent |
|---|---|---|---|
| 175 | `red_team.failure_code.F-RT-INPUT-MISSING.v1` | failure-code | §10.9 PRE |
| 176 | `red_team.failure_code.F-RT-INPUT-INCONSISTENT.v1` | failure-code | §10.9 PRE |
| 177 | `red_team.failure_code.F-RT-RUBRIC-DRIFT.v1` | failure-code | §10.9 PRE |
| 178 | `red_team.failure_code.F-RT-RFA-MISSING.v1` | failure-code | §10.9 PRE |
| 179 | `red_team.failure_code.F-RT-SCOPE-MISSING.v1` | failure-code | §10.9 PRE |
| 180 | `red_team.failure_code.F-RT-ORG-CROSS-REF.v1` | failure-code | §10.9 PRE |
| 181 | `red_team.failure_code.F-RT-DIALECT-UNCLASSIFIED.v1` | failure-code | §10.9 PRE |
| 182 | `red_team.failure_code.F-RT-FAMILY-OVERLAP.v1` | failure-code | §10.9 PRE (sub-tags `.with_scribe`, `.with_judge`); §4.16 subclass |
| 183 | `red_team.failure_code.F-RT-NO-COMPLIANT-FAMILY.v1` | failure-code | §10.9 PRE; §M13 review-seat outage |
| 184 | `red_team.failure_code.F-RT-ADMIN-RISK-REGISTER-STALE.v1` | failure-code | §10.9 PRE |
| 185 | `red_team.failure_code.F-RT-CONTEXT-PLACEMENT.v1` | failure-code | §10.9 PRE; §6 subclass |
| 186 | `red_team.failure_code.F-RT-VERDICT-CERT-MALFORMED.v1` | failure-code | §10.9 POST (sub-tags `.missing_block`, `.premise_without_citation`, `.step_without_premise_reference`, `.conclusion_grounded_in_undeclared_premise`); arch §F.1 subclass |
| 187 | `red_team.failure_code.F-RT-EVIDENCE-NOT-IN-DRAFT.v1` | failure-code | §10.9 POST; Law 5 mirror |
| 188 | `red_team.failure_code.F-RT-SCORE-OUT-OF-RANGE.v1` | failure-code | §10.9 POST (sub-tags `.criterion`, `.total`) |
| 189 | `red_team.failure_code.F-RT-SCORE-SUM-MISMATCH.v1` | failure-code | §10.9 POST |
| 190 | `red_team.failure_code.F-RT-CRITERION-MISSING.v1` | failure-code | §10.9 POST |
| 191 | `red_team.failure_code.F-RT-TIER-NOT-VERBATIM.v1` | failure-code | §10.9 POST |
| 192 | `red_team.failure_code.F-RT-WEAKNESSES-EMPTY.v1` | failure-code | §10.9 POST |
| 193 | `red_team.failure_code.F-RT-WEAKNESS-FIELD-MISSING.v1` | failure-code | §10.9 POST |
| 194 | `red_team.failure_code.F-RT-RECOMMENDATION-INVALID.v1` | failure-code | §10.9 POST |
| 195 | `red_team.failure_code.F-RT-ADMIN-RISK-UNFLAGGED.v1` | failure-code | §10.9 POST |
| 196 | `red_team.failure_code.F-RT-DIALECT-DRIFT.v1` | failure-code | §10.9 POST |
| 197 | `red_team.failure_code.F-COUNCIL-SPLIT.v1` | failure-code | §10.6 + §5 v7 §6 + §10.9 POST (sub-tags `.exceeds_threshold`, `.no_decision_at_signoff`); operator-routing only |
| 198 | `red_team.failure_code.F-RT-JUDGE-ANCHOR-SUSPECTED.v1` | failure-code | §10.6 + §5 v7 §6 + §10.9 POST; non-blocking advisory |

**PRE-gate checks (rows 199–202):**

| Row | Path | Kind | Parent |
|---|---|---|---|
| 199 | `red_team.pre_gate.input_consistency.v1` | pre-gate-check | §10.3 (RedTeamInput field invariants + claim_evidence_map union check + judge_verdict run_id/rubric_hash binding) |
| 200 | `red_team.pre_gate.three_way_family_distinct.v1` | pre-gate-check | §10.7 / §4.16 subclass |
| 201 | `red_team.pre_gate.context_placement.v1` | pre-gate-check | §10.9 / §6 subclass (anti-anchoring instructions present at start AND end) |
| 202 | `red_team.pre_gate.cascade_reorder_compliance.v1` | pre-gate-check | §10.7 (resolved Red Team family ∉ {scribe_family, judge_family}; cascade reordered before resolution) |

**POST-gate checks (rows 203–208):**

| Row | Path | Kind | Parent |
|---|---|---|---|
| 203 | `red_team.post_gate.evidence_in_draft.v1` | post-gate-check | §10.9 (every evidence string a verbatim substring of cited section's `body_text`); Law 5 mirror |
| 204 | `red_team.post_gate.sfr_three_block_parse.v1` | post-gate-check | §10.4 / arch §F.1 subclass |
| 205 | `red_team.post_gate.score_invariants.v1` | post-gate-check | §10.8 (range + sum + tier-verbatim + criterion-coverage in one batch) |
| 206 | `red_team.post_gate.attack_memo_completeness.v1` | post-gate-check | §10.5 (top_weaknesses ≥ 1; every weakness carries severity + claim + why_it_fails + what_a_reviewer_would_say + fix_hint; overall_verdict non-empty) |
| 207 | `red_team.post_gate.council_split.v1` | post-gate-check | §10.6 + §5 v7 §4.7 row N+1 |
| 208 | `red_team.post_gate.anchor_suspected_advisory.v1` | post-gate-check | §10.6 + §5 v7 §4.7 row N+2; non-blocking advisory |

**§5 v7 wiring rows (rows 209–211):**

| Row | Path | Kind | Parent |
|---|---|---|---|
| 209 | `pipeline.runstate.signoff_pending_council_split.v1` | constant | §5 v7 §3.2.1 (new phase Literal value) |
| 210 | `pipeline.iteration.exit_reason.council_split.v1` | constant | §5 v7 §4.6 (`IterationState.exit_reason` Literal extension) |
| 211 | `pipeline.law_map.row_red_team_five_laws.v1` | invariant | §5 v7 §11 (Red Team Five-Laws enforcement integration row) |

---

# Amendment §B — Index version bump

§0.5 amendment-file lineage at compound v1 LOCK:
- §0.5 v5 LOCKED 2026-04-19 (master, 101 rows).
- §0.5 v6 LOCKED 2026-04-21 (companion `section_00_5_section_06_operating_envelope_amendment.md`; rows 102-117; vocabulary extension to 16 values; +`procedure` kind).
- §0.5 v7 LOCKED 2026-04-21 (companion `section_00_5_section_07_scribe_amendment.md`; rows 118-158).
- **§0.5 v8 SCOPING DRAFT 2026-05-01 (this file; rows 159-211).** Promotes to LOCKED at compound transaction with §10 v1 + §5 v7.

Total row count at compound v1 LOCK: 211 rows. JSON companion `section_00_5_interface_index.v8.json` is rebuilt from amendment-file row schemas at LOCK time per §0.5.3.3 canonical-bytes rule.

---

# Amendment §C — Vocabulary preservation

Every row in this amendment uses one of the 16-value closed primitive_kind vocabulary established at §0.5 v5 LOCK + extended at §0.5 v6 LOCK (`procedure`):

- `schema` (rows 159-166)
- `constant` (rows 167-169 + 209-210)
- `invariant` (rows 170-174 + 211)
- `failure-code` (rows 175-198)
- `pre-gate-check` (rows 199-202)
- `post-gate-check` (rows 203-208)

**No vocabulary extension.** Every primitive_kind in this amendment resolves against the v5+v6 closed set. F-INDEX-STALE precondition for vocabulary extension does NOT apply.

---

# Amendment §D — Stability tier

All rows enter §0.5 at `stability_tier = "PARENT_UNLOCKED"` while parents (§10 v1, §5 v7) are SCOPING DRAFT. At compound v1 LOCK (post Thesis Round 1+2), all rows promote to `stability_tier = "STABLE"` via the same parent-backfill discipline §0.5 v6/v7 used.

---

# Amendment §E — Rationale

§10 Red Team is the LAST unsealed-as-a-whole council seat. v0.1 Tilth needs an §0.5 row-set for Red Team primitives so downstream blueprint amendments (§5 v7 wiring, future R1 production seat) can cite Red Team primitives via `IDX:v8:red_team.*` Index-mediated handles per §0.5.4. The 53-row authoring lifts §10.13 (~50 row proposals from §10 SCOPING DRAFT) + §5 v7 §8 (constants) + §5 v7 §11 (Law map row) into Index registration.

**Why amendment-file pattern, not in-place edit of `section_00_5_interface_index_locked.md`.** Matches §0.5 v6 (§6 companion) + §0.5 v7 (§7 companion) precedent. The master Index file remains LOCKED v5 on-disk; amendment files are runtime-live at compound LOCK; future §0.5 v8 master re-author rolls all v6/v7/v8 amendments into the master.

---

# L-005 audit record

**Status: SCOPING DRAFT — Thesis Round 1 not yet dispatched per BUDGET MODE per session prompt.** When Round 1 dispatches, expected verdicts:
- Editor: row-table formatting, cross-amendment row-number alignment, parent pointer accuracy.
- Judge: scoring against §0.5 amendment rubric (vocabulary preservation? row count math? parent-lock pointer freshness?).
- Red Team: adversarial (does row 197 F-COUNCIL-SPLIT collide with any v6/v7 row name? does row 211 invariant correctly bind Law 4 / §10.7 / §5 v7 §11? does the exit_reason extension at row 210 break any v6 §5 lifecycle property test?).

**Self-LOCK basis (this round only — SCOPING DRAFT, not v8 LOCK).** Pure-blueprint self-LOCK precedent: §0.5 §6 amendment 2026-04-21 + §0.5 §7 amendment 2026-04-21. Amendment-file pattern preserves master-file lock-state; companion to compound-transaction siblings (§10 v1 + §5 v7).
