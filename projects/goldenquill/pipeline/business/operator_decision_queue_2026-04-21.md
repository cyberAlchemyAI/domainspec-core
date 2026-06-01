# Operator Decision Queue — 2026-04-21

**Filed:** 2026-04-21
**Purpose:** Clear the six decisions gating v0.1 ship progress in one sitting. Sources: `pipeline/business/final_roadmap_to_ship_2026-04-21.md` §3 + `pipeline/business/mvp_tilth_launch_readiness_2026-04-20.md` §5 Tier 1.
**Use:** Answer each decision. Paste the sign-off block at bottom into today's daily_log.

---

## Decision 3.1 — §1 Sovereignty Envelope Round J Capstone Sign-Off

**Question:** Do I sign off on §1 Round J capstone SELF-LOCK (214 tests / 2318 LOC / 4 test files; aggregate coverage 86% union-drift, per-round Rounds A-I were 100% individually) and promote §1 from LOCKED-per-module to LOCKED-as-a-whole-section?
**Unblocks:** §2 Vault committee-review dispatch (the longest-standing critical-path dependency — promotes §2 from LOCKED-backfilled to formal committee LOCK).
**Recommended default:** SIGN OFF. Flag the 86% union-drift coverage as a v0.1.x measurement fix. Per-module coverage was 100% individually; 86% aggregate is a cross-module measurement artifact, not missing code paths. Not a ship blocker.
**Implication if NO / if different choice:** §2 Vault committee dispatch stays blocked. The entire critical-path cascade (Scout R10/R11, §4 Logician 9-module review, §5 capstone, council seats as pipeline code) waits. If the 86% is treated as a real coverage gap, it reopens Rounds A-I and delays ship by an estimated 1-2 weeks.
**Operator signature location:** `daily_logs/2026-04-21.md` §1 capstone LOCK block + `pipeline/engineering/lock_history.v1.jsonl` (promote SELF-LOCKED row to LOCKED with operator_signature field + note union-drift as v0.1.x task).

---

## Decision 3.2 — Scout Round 10 Split vs. Bundle

**Question:** Does Midas dispatch Scout R10 as two separate rounds (R10a `review_stage.py` + R10b `entity_research.py`) or as one bundled two-module round?
**Unblocks:** Midas R10 dispatch; R11 capstone-of-capstones queued behind it.
**Recommended default:** SPLIT. R10 REVIEW stage is policy-light (striped lock + read-check-write + four F-SCOUT-R-* codes); R10 entity_research has external-API dependencies (domain allowlist, cross-domain diversity, EntityClaimFetcher Protocol, S11a/b/c three-part dossier lock) worth isolating for committee scrutiny. Committee-surface fatigue on an ~170-test single round risks cycle-1 corrections on the harder module hiding behind clean-looking review_stage tests. Precedent: Rounds 8-9 were also single-module dispatches.
**Implication if NO / if different choice:** Bundle saves ~1 committee dispatch window (~2-3 hours operator time). Risk: cycle-1 5/5 PASS streak breaks on a two-module round and a single entity_research fix forces re-dispatch of the entire bundle including the already-clean review_stage module.
**Operator signature location:** Update `pipeline/engineering/spec_cards/scout_round_10_review_and_entity_research.md` header with operator disposition (SPLIT → file R10a and R10b spec cards); note in `daily_logs/2026-04-21.md`.

---

## Decision 3.3 — §5 v6.1 Seat-Output-Schema Pin: Dispatch Thesis Now vs. Park to v2.3 Post-MVP

**Question:** Do I dispatch the §5 v6.1 seat-output-schema pin (Editor + Judge + Scribe output field-level schemas) as a Thesis round now, or park the proposal to v2.3 post-MVP?
**Unblocks:** §5 capstone close (which is already gated on §5 v6 + v6.1 decisions landing).
**Recommended default:** PARK to v2.3. v0.1 MVP doesn't need field-level schema rigidity yet — contract-level tracking plus v2.2 Wave 1 gates (F-VERDICT-BLOCKING-MISSING, F-VERDICT-CITATION-MISSING) cover the runtime failure modes. v2.2 gate queue is already 12; gate #13 pushes past a natural close. Revisit after first-run surfaces concrete schema-drift incidents, not before. Park proposal in place (file stays at `pipeline/blueprint/v0.1/section_05_v6_1_seat_output_schema_pin_proposal.md` with STATUS note bumped to PARKED-to-v2.3).
**Implication if NO / if different choice:** Dispatching now adds one Thesis round (cycle 1 driver + cycle 2 verification) plus three paired-commit artifacts (schemas registry + POST-gate + §5 v6.1 amendment). Estimate 2-3 Code windows. Delays §5 capstone by ~1 week. Upside: field-level schema enforced at v0.1 ship; less v0.1.x surface later.
**Operator signature location:** Amend §5 v6.1 proposal doc status line to `PARKED-to-v2.3`; entry in `daily_logs/2026-04-21.md`.

---

## Decision 3.4 — Admin_Risk v2.2 Register: Approve + Path Decision

**Question:** (a) Approve the admin_risk v2.2 proposal (17 → ~75 entries; two-axis dialect discipline; top-15 explicit tagging landed). (b) Path decision — move v2 register to canonical path `pipeline/institutional_memory/admin_risk_register.yaml` OR repoint POST step 6 to current path `pipeline/engineering/agents/references/admin_risk_register.yaml`?
**Unblocks:** First-run Law 3 enforcement; POST step 6 validation gate; Cedar policy integration.
**Recommended default:** APPROVE v2.2 + MOVE to canonical path `pipeline/institutional_memory/admin_risk_register.yaml`. CLAUDE.md §"Current System State" already names that as the canonical location. Moving once (now, pre-Cedar-land) is cheaper than repointing POST step 6 plus every future reference. Remaining ~60 entry tags land as Tier 2 task 2.23 post-move.
**Implication if NO / if different choice:** Repoint POST step 6 = less work today (5 min sed) but creates a split brain between CLAUDE.md canonical claim and actual register home. Tier 2 task 2.23 (60+ entries remaining) still requires operator taxonomy approval regardless. Rejecting v2.2 outright = admin_risk stays at v1 (17 entries); Law 4 admin-risk term scanning misses ~58 known failure terms at first-run.
**Operator signature location:** (1) Move file: `pipeline/engineering/agents/references/admin_risk_register_v2_proposal_2026-04-20.yaml` → `pipeline/institutional_memory/admin_risk_register.yaml`; (2) `daily_logs/2026-04-21.md` entry; (3) `pipeline/engineering/lock_history.v1.jsonl` row (`lock_class: "policy"`; scope: admin_risk v2.2 approved + path canonicalised).

---

## Decision 3.5 — §6 Operating Envelope + §7 Scribe Thesis Rounds — Status Check / Re-Dispatch

**Status check run 2026-04-21:**
- `pipeline/validation/section_06_thesis_round_1/` — directory does not exist; no Editor / Judge / Red Team verdict files landed.
- `pipeline/validation/section_07_thesis_round_1/` — directory does not exist; no verdict files landed.
- Handoffs filed 2026-04-20 (`thesis_round_section_06_operating_envelope_v1.md`, `thesis_round_section_07_scribe_v1.md`). Elapsed time as of 2026-04-21 end-of-day: ~24-30 hours. Under the 48h re-dispatch threshold.

**Question:** Do I wait 24 more hours for verdicts to land, or re-dispatch now with fresh addressees?
**Unblocks:** §7 Scribe blueprint LOCK → Scribe seat implementation in pipeline code (Week 2 Day 7-9 critical path).
**Recommended default:** WAIT until 2026-04-22 end-of-day (48h window). If no verdicts land by then, re-dispatch with fresh addressees per router.yaml, note the original addressees' silence in `daily_logs/` for the Thesis-round participation ledger, and escalate to operator-voice scope-reduction decision if second dispatch also stalls.
**Implication if NO / if different choice:** Re-dispatching now (at ~30h) wastes tokens on still-in-progress work and breaks the Thesis-round participation norm. Waiting past 48h without re-dispatch lets critical-path slip silently — §7 Scribe LOCK is the gating precondition for Week 2 Day 7-9 Scribe-seat implementation.
**Operator signature location:** Set calendar-check for 2026-04-22 23:00 UTC. If still empty, file `daily_logs/2026-04-22.md` entry + re-dispatch handoffs at `pipeline/handoffs/thesis_round_section_06_operating_envelope_v2.md` and `thesis_round_section_07_scribe_v2.md` with updated addressees and a note citing v1 dispatch date + re-dispatch rationale.

---

## Decision 3.6 — Outside-Advisor Onboarding Kickoff

**Question:** When do I kick off outside-audit advisor onboarding (per Da Vinci v2 §13 DV-F-10 + roadmap Group 10 — THE REAL LOCK)?
**Unblocks:** Group 10 outside-impartial audit (the ship-gate criterion that no internal council can satisfy); all LOCK-internal → LOCK-sealed promotion.
**Recommended default:** START Week 2 (2026-04-29 onward). Per roadmap §6 Week 2 Day 12, NDA sign + scope doc + 5-doc review queue explainer. Two-to-four-week audit window is realistic per roadmap §7 contingency. Starting Week 2 — not earlier — gives advisor delivery of mature artifacts (§1 Round J locked, §2 Vault committee-LOCKED, §5 capstone close within sight) rather than mid-build churn. Candidate sourcing + NDA draft happens THIS week in parallel; see `pipeline/business/outside_advisor_scoping_2026-04-21.md` for channel list and red-flag criteria.
**Implication if NO / if different choice:** Starting Week 1 = advisor reads moving targets; burns advisor goodwill; forces re-review after every late-stage LOCK. Delaying to Week 3+ = advisor engagement overlaps with first-run acceptance; ship slips past 2026-05-30 comfort target.
**Operator signature location:** `daily_logs/2026-04-21.md` kickoff commitment entry; candidate outreach begins Week 1 Day 4-5 per `pipeline/business/outside_advisor_scoping_2026-04-21.md`; formal onboarding commit at Week 2 Day 12.

---

## Sign-Off Block (paste into daily_log)

```
## Operator Decision Queue — cleared 2026-04-21

- 3.1 §1 Round J capstone sign-off: [ACCEPT / DEFER / REJECT]
  - 86% union-drift coverage: [FLAG as v0.1.x measurement fix / TREAT as gap]
- 3.2 Scout R10 split vs bundle: [SPLIT / BUNDLE]
- 3.3 §5 v6.1 seat-output-schema pin: [PARK to v2.3 / DISPATCH Thesis now]
- 3.4 Admin_risk v2.2: [APPROVE / REVISE / REJECT]
  - Path: [MOVE to pipeline/institutional_memory/admin_risk_register.yaml / REPOINT POST step 6]
- 3.5 §6 + §7 Thesis rounds: [WAIT to 2026-04-22 23:00 UTC / RE-DISPATCH NOW]
- 3.6 Outside-advisor kickoff: [WEEK 2 per roadmap / OTHER: ______]

Rationale notes (if deviating from recommended default): _____

Signed: Josh — 2026-04-21
```

---

*Living document. Archive after all six decisions cleared + landings referenced in lock_history.*
