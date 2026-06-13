# Test Specification: Tilth Runtime Build — Grant-Cycle Council Pipeline

Test obligations derived from the council-pipeline spec. IDs follow `T-{ASPECT}-{Concept}-{nn}`. Coverage targets the DomainSpec δ-rules: rules ×2 (pass + fail), 1 per postcondition, 1 per error state, 1 per transition, 1 per invariant, ≥2 per event (emit + consume), ≥2 per workflow step.

## Operation tests

### ScoutDiscovery

| ID | Scenario | Expect |
| -- | -------- | ------ |
| T-OP-ScoutDiscovery-01 | VERIFY passes live synopsis | verdict VERIFIED_FIT |
| T-OP-ScoutDiscovery-02 | No live endpoint at VERIFY | verdict UNVERIFIED (NO_LIVE_ENDPOINT) |
| T-OP-ScoutDiscovery-03 | Verify fetch errors | VERIFICATION_FAILED (VERIFY_FETCH_ERROR) |
| T-OP-ScoutDiscovery-04 | Candidate elevated to CRITICAL without VERIFY | rejected (R1 fail) |
| T-OP-ScoutDiscovery-05 | A channel marked as fallback | rejected (R2 fail) |
| T-OP-ScoutDiscovery-06 | Scoring references a CIC→CLC binding | rejected (R3 fail) |
| T-OP-ScoutDiscovery-07 | Emits OpportunityVerified on verdict | event produced |

### ScribeDraft

| ID | Scenario | Expect |
| -- | -------- | ------ |
| T-OP-ScribeDraft-01 | Section composed with traceable claims | draft section stored |
| T-OP-ScribeDraft-02 | Claim with no RFA/PROJECT_CONTEXT source | UNTRACEABLE_CLAIM (R4 fail) |
| T-OP-ScribeDraft-03 | KGIE preflight fails | KGIE_PREFLIGHT_FAIL |
| T-OP-ScribeDraft-04 | Gear co_pilot selected | seat executes/refines under direction |
| T-OP-ScribeDraft-05 | `[SLOT_x]` would enter a cloud prompt | blocked (R6 fail) |
| T-OP-ScribeDraft-06 | Provenance attached per section claim | postcondition holds |

### EditorPass

| ID | Scenario | Expect |
| -- | -------- | ------ |
| T-OP-EditorPass-01 | Flag carries 3 replacement options | accepted |
| T-OP-EditorPass-02 | Flag carries 1 option | MISSING_OPTIONS (R7 fail) |
| T-OP-EditorPass-03 | Silent substitution attempted | rejected (R8 fail, Law 4) |
| T-OP-EditorPass-04 | Substance unchanged before approval | postcondition holds |

### JudgeScore

| ID | Scenario | Expect |
| -- | -------- | ------ |
| T-OP-JudgeScore-01 | Judge family differs from Scribe | accepted |
| T-OP-JudgeScore-02 | Judge shares Scribe family | SAME_FAMILY_AS_SCRIBE (R9 fail) |
| T-OP-JudgeScore-03 | Every dimension scored, evidence in draft | DraftScored emitted |
| T-OP-JudgeScore-04 | Evidence string absent from draft | EVIDENCE_NOT_IN_DRAFT (R10 fail) |
| T-OP-JudgeScore-05 | Scores written onto draft | postcondition holds |

### RedTeamChallenge

| ID | Scenario | Expect |
| -- | -------- | ------ |
| T-OP-RedTeamChallenge-01 | Red Team family differs from Scribe + Judge | accepted |
| T-OP-RedTeamChallenge-02 | Red Team shares a family | SAME_FAMILY (R11 fail) |
| T-OP-RedTeamChallenge-03 | Red Team fires on every draft | unconditional (R12) |
| T-OP-RedTeamChallenge-04 | Delta ≥ 10 | CouncilSplitRaised emitted |

### LogicianGate

| ID | Scenario | Expect |
| -- | -------- | ------ |
| T-OP-LogicianGate-01 | All Five-Laws gates pass | draft Accepted |
| T-OP-LogicianGate-02 | A PRE/POST gate unsatisfied | GATE_FAIL_CLOSED (R13 fail) |
| T-OP-LogicianGate-03 | Split ≥10 routed to human | CouncilSplitPolicy applied (R14) |
| T-OP-LogicianGate-04 | Model invocation inside gate | LLM_CALL_IN_GATE (R15 fail) |
| T-OP-LogicianGate-05 | Fail-closed gate emits revision | DraftRevisionRequested |

## Calculation tests

### CouncilSplitDelta

| ID | Scenario | Expect |
| -- | -------- | ------ |
| T-OP-CouncilSplitDelta-01 | delta = abs(judge - redteam) | non-negative result |
| T-OP-CouncilSplitDelta-02 | delta exactly 10 | split == true (inclusive) |
| T-OP-CouncilSplitDelta-03 | delta 9 | split == false |

## Rule tests

### Law1TraceabilityRule

| ID | Scenario | Expect |
| -- | -------- | ------ |
| T-RULES-Law1TraceabilityRule-01 | Claim with valid source | pass |
| T-RULES-Law1TraceabilityRule-02 | Claim with no source | fail-close |

### VerifyBeforeCriticalRule

| ID | Scenario | Expect |
| -- | -------- | ------ |
| T-RULES-VerifyBeforeCriticalRule-01 | CRITICAL after VERIFIED_FIT | pass |
| T-RULES-VerifyBeforeCriticalRule-02 | CRITICAL without VERIFY | fail-close |

### CrossFamilyRule

| ID | Scenario | Expect |
| -- | -------- | ------ |
| T-RULES-CrossFamilyRule-01 | Distinct provider families | pass |
| T-RULES-CrossFamilyRule-02 | Shared family | fail-close |

### MagicStepValidationRule

| ID | Scenario | Expect |
| -- | -------- | ------ |
| T-RULES-MagicStepValidationRule-01 | validate() pass before complete | pass |
| T-RULES-MagicStepValidationRule-02 | complete without validate | fail-close |

## State machine tests

### DraftLifecycle

| ID | Scenario | Expect |
| -- | -------- | ------ |
| T-ST-DraftLifecycle-01 | ScribeDraft → Drafted | valid transition |
| T-ST-DraftLifecycle-02 | EditorPass: Drafted → Edited | valid transition |
| T-ST-DraftLifecycle-03 | DraftScored: Edited → Scored | valid transition |
| T-ST-DraftLifecycle-04 | CouncilSplitRaised: Scored → Challenged | valid transition |
| T-ST-DraftLifecycle-05 | LogicianGate pass: Scored → Accepted | valid transition |
| T-ST-DraftLifecycle-06 | DraftRevisionRequested: Challenged → Revising | valid transition |
| T-ST-DraftLifecycle-07 | ScribeDraft: Revising → Drafted | valid transition |
| T-ST-DraftLifecycle-08 | DraftScored from Drafted | rejected (must Edit first) |
| T-ST-DraftLifecycle-09 | Any event from Accepted | rejected (terminal) |
| T-ST-DraftLifecycle-10 | DL-INV-1 accepted ⇒ all scored | invariant holds |
| T-ST-DraftLifecycle-11 | DL-INV-2 evidence ⊑ sections | invariant holds |
| T-ST-DraftLifecycle-12 | DL-INV-3 revisionCount ≤ 2 | invariant holds |
| T-ST-DraftLifecycle-13 | DL-INV-4 every claim has provenance | invariant holds |

### GrantCycleStatus

| ID | Scenario | Expect |
| -- | -------- | ------ |
| T-ST-GrantCycleStatus-01 | OpportunityVerified → Opened | valid transition |
| T-ST-GrantCycleStatus-02 | ScribeDraft: Opened → Drafting | valid transition |
| T-ST-GrantCycleStatus-03 | DraftScored: Drafting → Reviewing | valid transition |
| T-ST-GrantCycleStatus-04 | CouncilSplitRaised: Reviewing → HumanGate | valid transition |
| T-ST-GrantCycleStatus-05 | LogicianGate: Reviewing → Closed | valid transition |
| T-ST-GrantCycleStatus-06 | DraftRevisionRequested: HumanGate → Drafting | valid transition |
| T-ST-GrantCycleStatus-07 | Human accepts: HumanGate → Closed | valid transition |
| T-ST-GrantCycleStatus-08 | DraftScored from Opened | rejected |
| T-ST-GrantCycleStatus-09 | Any event from Closed | rejected (terminal) |
| T-ST-GrantCycleStatus-10 | GC-INV-1 single orgSlug (Law 3) | invariant holds |
| T-ST-GrantCycleStatus-11 | GC-INV-2 closed ⇒ logicianPassed | invariant holds |
| T-ST-GrantCycleStatus-12 | GC-INV-3 orgSlug immutable | invariant holds |

### OpportunityState

| ID | Scenario | Expect |
| -- | -------- | ------ |
| T-ST-OpportunityState-01 | DISCOVER → Discovered | valid transition |
| T-ST-OpportunityState-02 | OpportunityVerified: Discovered → Verified | valid transition |
| T-ST-OpportunityState-03 | VERIFY error: Discovered → VerificationFailed | valid transition |
| T-ST-OpportunityState-04 | REVIEW: Verified → Reviewed | valid transition |
| T-ST-OpportunityState-05 | REVIEW from Discovered | rejected (no VERIFY) |
| T-ST-OpportunityState-06 | Any event from Reviewed | rejected (terminal) |
| T-ST-OpportunityState-07 | OP-INV-1 criticalFit ⇒ VERIFIED_FIT | invariant holds |
| T-ST-OpportunityState-08 | OP-INV-2 Reviewed only via human gate | invariant holds |

## Workflow tests

### GrantCyclePipeline

| ID | Scenario | Expect |
| -- | -------- | ------ |
| T-WF-GrantCyclePipeline-01 | Happy path Draft → Edit → Score → Challenge → Gate → Closed | cycle closes |
| T-WF-GrantCyclePipeline-02 | UNTRACEABLE_CLAIM at step 1 | section rejected |
| T-WF-GrantCyclePipeline-03 | EVIDENCE_NOT_IN_DRAFT at step 3 | loops to step 1 |
| T-WF-GrantCyclePipeline-04 | Delta ≥ 10 at step 4 | HumanGate reached (GP-INV-3) |
| T-WF-GrantCyclePipeline-05 | GATE_FAIL_CLOSED at step 5 | revision loop to step 1 |
| T-WF-GrantCyclePipeline-06 | GP-INV-1 Red Team fires before gate | invariant holds |
| T-WF-GrantCyclePipeline-07 | GP-INV-2 Logician is last before Closed | invariant holds |
| T-WF-GrantCyclePipeline-08 | GP-INV-4 post-substance seats LOCAL | invariant holds |

## Event tests

### DraftScored

| ID | Scenario | Expect |
| -- | -------- | ------ |
| T-EV-DraftScored-01 | JudgeScore emits DraftScored | producer emission |
| T-EV-DraftScored-02 | RedTeamChallenge consumes to compute delta | consumer handling |

### CouncilSplitRaised

| ID | Scenario | Expect |
| -- | -------- | ------ |
| T-EV-CouncilSplitRaised-01 | RedTeamChallenge emits on delta ≥ 10 | producer emission |
| T-EV-CouncilSplitRaised-02 | Pipeline routes to HumanGate | consumer handling |

### DraftRevisionRequested

| ID | Scenario | Expect |
| -- | -------- | ------ |
| T-EV-DraftRevisionRequested-01 | LogicianGate emits on fail-close | producer emission |
| T-EV-DraftRevisionRequested-02 | ScribeDraft consumes to recompose | consumer handling |

### OpportunityVerified

| ID | Scenario | Expect |
| -- | -------- | ------ |
| T-EV-OpportunityVerified-01 | ScoutDiscovery emits on VERIFY | producer emission |
| T-EV-OpportunityVerified-02 | Pipeline opens cycle on VERIFIED_FIT | consumer handling |

## Entity tests

### GrantCycle

| ID | Scenario | Expect |
| -- | -------- | ------ |
| T-DOM-GrantCycle-01 | Cycle bound to single orgSlug | Law 3 structural |
| T-DOM-GrantCycle-02 | LogicianGate acts on cycle | performs edge |

### Draft

| ID | Scenario | Expect |
| -- | -------- | ------ |
| T-DOM-Draft-01 | Draft carries provenance per claim | contains SectionProvenance |
| T-DOM-Draft-02 | Draft embeds rubric scores after JudgeScore | contains RubricScore |

### OpportunityCandidate

| ID | Scenario | Expect |
| -- | -------- | ------ |
| T-DOM-OpportunityCandidate-01 | Candidate records source channel | field stored |
| T-DOM-OpportunityCandidate-02 | Candidate cannot reach CRITICAL without VERIFY | rule enforced |
