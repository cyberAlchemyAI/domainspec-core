# MVP Finish Line — Copy-Paste Prompt Guide

**Filed:** 2026-04-29
**Baseline:** 6,219 tests green, 130 lock_history rows
**Target:** MVP-runnable — one grant in, scored draft out, all sections LOCKED-as-a-whole


## Status Summary

| Section | Status | What's Left |
|---|---|---|
| §1 Sovereignty Envelope | ✅ LOCKED-as-a-whole (Round J) | — |
| §2 Vault Topology | ✅ LOCKED-as-a-whole (Round K) | — |
| §3 Scout | ❌ Per-module LOCKED (R1–R10) | R11 orchestrator build + R12 capstone |
| §4 Logician | ❌ v2.2 gates LOCKED; 9 base modules backfill-only | Batches A/B/C committee + Round L capstone |
| §5 Pipeline Loop | ❌ Per-module LOCKED (R1–R12.B) | R13 capstone |
| §6 Operating Envelope | ✅ LOCKED (v1-r1) | — |
| §7 Scribe | ❌ Per-round LOCKED (R1–R3 committee) | Capstone (test-only) |
| §8 Editor | ❌ NOT BUILT | R1 adapter + R2 polish + capstone |
| §9 Judge | ❌ NOT BUILT | R1 types + R2 scoring + R3 seat + capstone |
| Demo Driver | ❌ | E2E pipeline test (capstone-of-capstones) |

**5 waves. ~15 sessions. Estimated 25–40 hours wall clock with parallel dispatch.**


## WAVE 1 — All parallel, no dependencies between them (6 sessions)

### 1A. §3 Scout R11 — Orchestrator Build · CODE · Opus · 30–50 turns

```
Read pipeline/SESSION_BOOTSTRAP.md for project orientation.
Read pipeline/handoffs/scout_round_11_capstone_dispatch_2026-04-21.md in full.

You are King Midas. BUDGET MODE: self-LOCK where eligible, no committee dispatch
unless the handoff explicitly requires it (R11 DOES require committee — execute that).

Execute the Scout R11 build per the handoff prompt. The handoff contains the full
spec, scope, interface contract, committee instructions, and done-definition.

Key reminders:
- Land pipeline/scout/run.py with run_scout_discover_verify_review(session) -> ScoutRunResult
- Compose DISCOVER (R8) + VERIFY (R9) + REVIEW+entity_research (R10) — no re-authoring
- _build_fit_rationale bounded ≤800 tokens, LLM imports confined to that function
- Per-stage checkpoint on success AND failure (Autonomy Rule 1)
- Pinned interpreter: .venv/bin/python3 (NOT system python3)
- AST-lint R1-R7 exit 0
- Zero regressions on 6219-test baseline
- Committee 5/5 PASS required per handoff — this round breaks Scout's self-LOCK streak

STOP CONDITION: R11 LOCKED in lock_history + memory file written + MEMORY.md updated.
```

### 1B. §4 Logician Batches A/B/C — Committee Promotion · CODE · Sonnet · 40–60 turns

```
Read pipeline/SESSION_BOOTSTRAP.md for project orientation.
Read pipeline/handoffs/section_4_logician_9_module_dispatch_2026-04-21.md in full.

You are King Midas. BUDGET MODE: execute the 3-batch committee dispatch per the
handoff. No architectural revision, no scope expansion.

The 9 modules (rows 45–53 in lock_history) are LOCKED-backfilled under F-03 but never
went through formal Code Thesis Committee review. This session promotes them.

Batch A (4 modules): pre_gate, post_gate, gate_runner, cedar_eval
Batch B (3 modules): claim_evidence, source_tag_verify, dossier_verify
Batch C (2 modules): admin_risk, conversation_log

Per the handoff:
- L-003 cross-family discipline on every committee dispatch
- F-AMDT-07 v1.1 author-family anti-collision
- code_retry_cap: 1
- E-027 prompt-token-estimate pre-check
- E-028 transport-retry discipline
- Batches A/B/C can run sequentially within this session

Pinned interpreter: .venv/bin/python3
Zero regressions on 6219-test baseline.

STOP CONDITION: All 9 modules show "LOCKED (committee 5/5 PASS)" in lock_history.
Memory files written. MEMORY.md updated.
```

### 1C. §5 Pipeline R13 — Whole-Section Capstone · CODE · Opus · 30–40 turns

```
Read pipeline/SESSION_BOOTSTRAP.md for project orientation.
Read pipeline/handoffs/section_05_round_13_handoff_2026-04-21.md in full.

You are King Midas. BUDGET MODE: self-LOCK, no committee dispatch.

Execute §5 Round 13 capstone per the embedded prompt in the handoff file. The handoff
contains full spec, scope, file layout, test floors, and done-definition.

Key reminders:
- Test-only round — ZERO new §5 production code
- 5 test files under tests/loop/ per spec card
- Floor ≥123 tests; E-024 capstone-relaxed 1.3× multiplier → ~160 expected
- Pinned interpreter: .venv/bin/python3
- AST-lint R1-R7 exit 0 on all 5 new files
- Zero regressions on 4894-test baseline (this was the count at R12.B LOCK;
  current suite is 6219 — verify no regressions against CURRENT count)
- Three self-LOCK questions per spec card — if all "no", self-LOCK

STOP CONDITION: §5 promoted to LOCKED-as-a-whole-section. lock_history row appended.
Memory file written. MEMORY.md updated.
```


### 1D. §7 Scribe Capstone — Whole-Section LOCK · CODE · Opus · 25–35 turns

```
Read pipeline/SESSION_BOOTSTRAP.md for project orientation.
Read pipeline/handoffs/section_7_scribe_whole_section_capstone_2026-04-29.md in full.

You are King Midas. BUDGET MODE: self-LOCK, no committee dispatch.

Execute §7 Scribe whole-section capstone per the handoff. All per-round work is done
(R1/R2/R2.5/R3 all LOCKED, R3 committee 19/20 PASS). This capstone promotes §7 from
per-round LOCKs to LOCKED-as-a-whole-section.

Key reminders:
- Test-only round — ZERO new §7 production code
- Verify full Scribe invocation lifecycle end-to-end
- Test every F-SCRIBE-* failure code
- Test admin-risk register consumption
- Pinned interpreter: .venv/bin/python3
- AST-lint R1-R7 exit 0
- Zero regressions on current test baseline (6219)
- Self-LOCK eligible (all consumed modules already committee-LOCKED)

STOP CONDITION: §7 promoted to LOCKED-as-a-whole-section. lock_history row appended.
Memory file written. MEMORY.md updated.
```


### 1E. §8 Editor R1 — Adapter Build · CODE · Opus · 25–35 turns

```
Read pipeline/SESSION_BOOTSTRAP.md for project orientation.
Read pipeline/handoffs/editor_round_1_dispatch_2026-04-21.md in full.
Read pipeline/engineering/spec_cards/section_08_editor_round_1_adapter.md in full.

You are King Midas. BUDGET MODE: self-LOCK where eligible, no committee dispatch
unless spec requires it.

GATING CHECK SATISFIED: Scribe R2 LOCKED (row ~125 in lock_history). All hard
prerequisites satisfied per handoff gating notice.

Execute Editor R1 per the handoff and spec card. Land 4 modules under
pipeline/seats/editor/:
- types.py (EditorInput, EditorOutput, FlaggedTerm, etc.)
- adapter.py (SkillLauncher Protocol, invoke_editor_adapter, parse_skill_output)
- seat.py (subprocess entry matching seat_runner §4.4 contract)
- __init__.py (__all__ + BLUEPRINT_DEPS)

Key reminders:
- Adapter pattern (Option A) — wraps existing skills/editor/SKILL.md, does NOT reimplement
- 180_000 ms timeout inline-literal (V1 rebind-resistance)
- 3 new F-EDITOR-* POST slots: OUTPUT-SHAPE, REWROTE-INSTEAD-OF-FLAGGED, SINGLE-REPLACEMENT
- SFR-exempt per architecture §F.1
- Pinned interpreter: .venv/bin/python3
- AST-lint R1-R7 exit 0
- Zero regressions on current test baseline

STOP CONDITION: Editor R1 LOCKED in lock_history. Tests green. Memory written.
```


### 1F. §9 Judge R1 — Types + Rubric Primitives · CODE · Opus · 25–35 turns

```
Read pipeline/SESSION_BOOTSTRAP.md for project orientation.
Read pipeline/handoffs/judge_round_1_dispatch_2026-04-21.md in full.
Read pipeline/engineering/spec_cards/section_09_judge_round_1_types_and_rubric_primitives.md in full.

You are King Midas. BUDGET MODE: self-LOCK where eligible, no committee dispatch
unless spec requires it.

GATING CHECK SATISFIED: Scribe R2 LOCKED (confirmed). All prerequisites per handoff.

Execute Judge R1 per the handoff and spec card. Land 4 modules under
pipeline/seats/judge/:
- types.py (Rubric, RubricCriterion, CriterionScore, JudgeInput, JudgeOutput, Protocols)
- rubric_loader.py (load_rubric + compute_rubric_sha256)
- dimension_scorer.py (score_dimension with E-017 LLMCallFn seam)
- __init__.py (__all__ + BLUEPRINT_DEPS)

Key reminders:
- Pure deterministic round — zero LLM calls, zero network, zero subprocess
- Full port pattern (NOT adapter like Editor)
- Real pipeline/rubrics/vapg_fy26.json as happy-path fixture
- 2 malformed rubric fixtures for adversarial tests
- Pinned interpreter: .venv/bin/python3
- AST-lint R1-R7 exit 0
- Zero regressions on current test baseline

STOP CONDITION: Judge R1 LOCKED in lock_history. Tests green. Memory written.
```


## WAVE 2 — Depends on Wave 1 (5 sessions, all parallel within wave)


### 2A. §3 Scout R12 — Whole-Section Capstone · CODE · Opus · 35–50 turns · after 1A

```
Read pipeline/SESSION_BOOTSTRAP.md for project orientation.
Read pipeline/handoffs/section_03_round_12_handoff_2026-04-29.md in full.

You are King Midas. BUDGET MODE: self-LOCK, no committee dispatch.

HARD PREREQUISITE: Confirm Scout R11 is LOCKED in lock_history before proceeding.
If not LOCKED, STOP and report.

Execute §3 Scout R12 capstone per the embedded prompt in the handoff file. The
handoff contains full spec, scope, file layout, test floors, and done-definition.

Key reminders:
- Test-only round — ZERO new §3 production code
- 4 test files under tests/scout/ per spec card
- Floor ≥120 tests; E-024 capstone-relaxed 1.3× → ~150-170 expected
- Pinned interpreter: .venv/bin/python3
- AST-lint R1-R7 exit 0
- Zero regressions on current test baseline
- Self-LOCK eligible if three audit questions all "no"

STOP CONDITION: §3 promoted to LOCKED-as-a-whole-section. lock_history row appended.
Memory file written. MEMORY.md updated.
```


### 2B. §4 Logician Round L — Whole-Section Capstone · CODE · Opus · 35–50 turns · after 1B

```
Read pipeline/SESSION_BOOTSTRAP.md for project orientation.
Read pipeline/handoffs/section_4_logician_round_L_capstone_2026-04-29.md in full.
Read pipeline/engineering/spec_cards/section_4_round_l_capstone.md in full.

You are King Midas. BUDGET MODE: self-LOCK, no committee dispatch.

HARD PREREQUISITE: Confirm Batches A/B/C all show "LOCKED (committee 5/5 PASS)" in
lock_history before proceeding. If any batch is not LOCKED, STOP and report.

Execute §4 Round L capstone per the handoff and spec card.

Key reminders:
- Test-only round — ZERO new §4 production code
- 4 test files under tests/logician/ per spec card
- Floor ≥150 tests; E-024 1.3× → ~195-230 expected
- Mirrors §2 Round K structure (8 integration classes, BT properties, N-fuzz)
- Pinned interpreter: .venv/bin/python3
- AST-lint R1-R7 exit 0
- Zero regressions on current test baseline
- Self-LOCK eligible if three audit questions all "no"

STOP CONDITION: §4 promoted to LOCKED-as-a-whole-section. lock_history row appended.
Memory file written. MEMORY.md updated.
```


### 2C. §8 Editor R2 — Polish · CODE · Sonnet · 20–30 turns · after 1E

```
Read pipeline/SESSION_BOOTSTRAP.md for project orientation.
Read pipeline/engineering/spec_cards/section_08_editor_round_2_polish.md in full.

You are King Midas. BUDGET MODE: self-LOCK, no committee dispatch.

HARD PREREQUISITE: Confirm Editor R1 is LOCKED in lock_history before proceeding.

Execute Editor R2 per the spec card. Extends R1 — does not redefine.

Scope:
- Retry-with-clarification bounded loop (1 retry on malformed skill output)
- Enhanced validation (taxonomy sort audit, tone consistency, quick-wins dedup,
  terms-to-verify cross-reference)
- §0.5 row refresh if applicable

Key reminders:
- Pinned interpreter: .venv/bin/python3
- AST-lint R1-R7 exit 0
- Zero regressions on current test baseline
- Self-LOCK eligible (pure extension of LOCKed R1 surface)

STOP CONDITION: Editor R2 LOCKED in lock_history. Tests green. Memory written.
```


### 2D. §9 Judge R2 — Cross-Rubric + Verdict · CODE · Opus · 30–40 turns · after 1F

```
Read pipeline/SESSION_BOOTSTRAP.md for project orientation.
Read pipeline/engineering/spec_cards/section_09_judge_round_2_cross_rubric_and_verdict.md in full.

You are King Midas. BUDGET MODE: self-LOCK where eligible, no committee dispatch
unless spec requires it.

HARD PREREQUISITE: Confirm Judge R1 is LOCKED in lock_history before proceeding.

Execute Judge R2 per the spec card. Builds scoring orchestrator atop R1 primitives.

Expected scope (confirm against spec card):
- Cross-rubric dispatcher (primary rubric + cross-check against rubric library)
- Responsiveness mapper
- JudgeVerdict full shape assembly
- §0.5 row population for §9

Key reminders:
- Pinned interpreter: .venv/bin/python3
- AST-lint R1-R7 exit 0
- Zero regressions on current test baseline

STOP CONDITION: Judge R2 LOCKED in lock_history. Tests green. Memory written.
```


### 2E. §9 Judge R3 — Seat Entry + Provider + SFR · CODE · Opus · 30–40 turns · after 2D

```
Read pipeline/SESSION_BOOTSTRAP.md for project orientation.
Read pipeline/engineering/spec_cards/section_09_judge_round_3_seat_entry_and_sfr.md in full.

You are King Midas. BUDGET MODE: self-LOCK where eligible, committee if spec requires.

HARD PREREQUISITE: Confirm Judge R2 is LOCKED in lock_history before proceeding.

Execute Judge R3 per the spec card. Final Judge build round.

Expected scope (confirm against spec card):
- seat.py subprocess entry (Google Gemini 2.5 Pro binding)
- SFR emission (three-block Premises/Execution/Conclusion — Judge is NOT SFR-exempt)
- Logician PRE/POST gate wiring (F-JUDGE-* failure codes)
- Provider cascade wiring

Key reminders:
- Cross-family discipline: Judge primary = Google; reviewer MUST NOT be Google
- Pinned interpreter: .venv/bin/python3
- AST-lint R1-R7 exit 0
- Zero regressions on current test baseline

STOP CONDITION: Judge R3 LOCKED in lock_history. Tests green. Memory written.
```


## WAVE 3 — Depends on Wave 2 (3 sessions, all parallel)


### 3A. §8 Editor Capstone — Whole-Section LOCK · CODE · Sonnet · 20–30 turns · after 2C

```
Read pipeline/SESSION_BOOTSTRAP.md for project orientation.
Read pipeline/handoffs/section_8_editor_whole_section_capstone_2026-04-29.md in full.

You are King Midas. BUDGET MODE: self-LOCK, no committee dispatch.

HARD PREREQUISITE: Confirm Editor R1 + R2 both LOCKED in lock_history.

Execute §8 Editor whole-section capstone per the handoff.

Key reminders:
- Test-only round — ZERO new §8 production code
- Verify full Editor invocation lifecycle end-to-end
- Test every F-EDITOR-* failure code
- Verify skill-subprocess boundary isolation
- Pinned interpreter: .venv/bin/python3
- AST-lint R1-R7 exit 0
- Zero regressions on current test baseline
- Self-LOCK eligible

STOP CONDITION: §8 promoted to LOCKED-as-a-whole-section. lock_history row appended.
```


### 3B. §9 Judge Capstone — Whole-Section LOCK · CODE · Opus · 30–40 turns · after 2E

```
Read pipeline/SESSION_BOOTSTRAP.md for project orientation.
Read pipeline/handoffs/section_9_judge_whole_section_capstone_2026-04-29.md in full.

You are King Midas. BUDGET MODE: self-LOCK, no committee dispatch.

HARD PREREQUISITE: Confirm Judge R1 + R2 + R3 all LOCKED in lock_history.

Execute §9 Judge whole-section capstone per the handoff.

Key reminders:
- Test-only round — ZERO new §9 production code
- Verify full Judge invocation lifecycle end-to-end
- Test every F-JUDGE-* failure code
- Cross-family discipline: Judge primary = Google; verify in tests
- Rubric hash-pin integrity end-to-end
- SFR emission verified
- Pinned interpreter: .venv/bin/python3
- AST-lint R1-R7 exit 0
- Zero regressions on current test baseline
- Self-LOCK eligible

STOP CONDITION: §9 promoted to LOCKED-as-a-whole-section. lock_history row appended.
```


## WAVE 4 — Demo Driver (1 session, blocked on all sections LOCKED)


### 4A. Demo Driver — MVP E2E Pipeline Test · CODE · Opus · 40–60 turns · after ALL

```
Read pipeline/SESSION_BOOTSTRAP.md for project orientation.
Read pipeline/engineering/spec_cards/demo_driver_mvp_end_to_end.md in full.

You are King Midas. BUDGET MODE: this is the capstone-of-capstones.

HARD PREREQUISITE: Confirm ALL sections are LOCKED-as-a-whole in lock_history:
- §1 Sovereignty Envelope ✅ (pre-existing)
- §2 Vault Topology ✅ (pre-existing)
- §3 Scout (Wave 1A + 2A)
- §4 Logician (Wave 1B + 2B)
- §5 Pipeline Loop (Wave 1C)
- §6 Operating Envelope ✅ (pre-existing)
- §7 Scribe (Wave 1D)
- §8 Editor (Wave 3A)
- §9 Judge (Wave 3B)
If ANY section is not LOCKED-as-a-whole, STOP and report which.

Execute the demo driver per the spec card. This is NOT a new module — it is a test
harness + orchestration script that exercises pipeline.loop.run_pipeline with:
- Real RFA: VAPG FY26 (from pipeline/rfa/ if live RFA closed)
- Real org: FIT Farms LLC (orgs/fit_farms_llc/PROJECT_CONTEXT.md)
- Real rubric: pipeline/rubrics/vapg_fy26.json
- Real API keys: operator's BYOK keys per router.yaml

Pipeline stages to verify:
1. Boot (§1) → 2. RFA Ingest → 3. Scout DISCOVER → 4. Scout VERIFY →
5. Scout REVIEW → 6. Scribe Draft → 7. Editor Pass → 8. Judge Score →
9. Logician Gate → 10. Output

Key reminders:
- Law 3: ONLY FIT Farms LLC data flows through
- All Five Operating Laws enforced end-to-end
- Must run on Dev tier (M1 Mac Mini, 8 GB RAM)
- Pinned interpreter: .venv/bin/python3
- Produce a scored, gated, audited grant proposal from a standing start

STOP CONDITION: Pipeline produces a scored draft. All Logician gates pass.
Full audit trail written to vault. Demo report filed at
pipeline/engineering/demo_driver_report_<date>.md.

This is the moment. One grant in, scored draft out. Tilth v0.1 runs.
```


## Summary

**15 sessions total** (all CODE / Claude Code). 12 Opus, 3 Sonnet. Max 6 parallel (Wave 1).

**Critical path:** Judge R1 → R2 → R3 → capstone → Demo Driver (4 serial sessions). Dispatch Judge R1 first.

**Wall-clock:** ~8–12h parallel, ~15–20h sequential.

**Convention across all prompts:** "BUDGET MODE" = self-LOCK where eligible, no committee unless handoff requires it. Pinned `.venv/bin/python3` (system python3 is 3.9, can't collect). King Midas = `pipeline/engineering/king_midas_implementation_prompt_v2_1.md`. SESSION_BOOTSTRAP.md = full project orientation.
