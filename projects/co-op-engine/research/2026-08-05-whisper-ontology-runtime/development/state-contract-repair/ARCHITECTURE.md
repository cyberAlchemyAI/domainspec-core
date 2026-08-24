# Candidate research architecture

Status: `design-validator-pass`. This is a research acceptance architecture, not a runtime architecture or owner decision.

## State model

Each reduced state contains exactly `revision`, `lifecycle_phase`, `pending_gate`, `correction_state`, and `outcome_ceiling`.

- `pending_gate`: `none | intent_freeze | editorial_decision | mechanical_validation | post_apply_review | corrected_intent_freeze | graph_policy_validation | comprehension_assessment`
- `correction_state`: `none | open | resolved`
- `outcome_ceiling`: `not_assessed | pass | flag | block`
- initial state: `r0 / not_started / none / none / not_assessed`

`outcome_ceiling` is the current maximum claim permitted by accumulated valid evidence, not a monotone severity score. It changes only at EV11, EV12, EV22, and EV25.

## Total EV01-EV26 oracle

The tuple after each event is `revision / lifecycle_phase / pending_gate / correction_state / outcome_ceiling`.

| Event | Required resulting tuple |
| --- | --- |
| EV01 IntentRecorded | `r1 / intake_recorded / intent_freeze / none / not_assessed` |
| EV02 IntentFrozen | `r2 / intent_frozen / none / none / not_assessed` |
| EV03 PlanGenerationScheduled | `r3 / plan_generation_scheduled / none / none / not_assessed` |
| EV04 PlanProduced | `r4 / plan_ready / none / none / not_assessed` |
| EV05 AuditionGenerationScheduled | `r5 / audition_generation_scheduled / none / none / not_assessed` |
| EV06 AuditionProduced | `r6 / awaiting_editorial_decision / editorial_decision / none / not_assessed` |
| EV07 EditorialDecisionRecorded | `r7 / editorial_decision_recorded / none / none / not_assessed` |
| EV08 DraftGenerationScheduled | `r8 / draft_generation_scheduled / none / none / not_assessed` |
| EV09 DraftProduced | `r9 / draft_ready / mechanical_validation / none / not_assessed` |
| EV10 DraftValidationScheduled | `r10 / draft_validation_scheduled / none / none / not_assessed` |
| EV11 MechanicalAssessmentRecorded | `r11 / mechanically_validated / post_apply_review / none / flag` |
| EV12 CorrectionRecorded | `r12 / correction_pending / corrected_intent_freeze / open / block` |
| EV13 IntentFrozen | `r13 / intent_frozen / none / open / block` |
| EV14 PlanGenerationScheduled | `r14 / plan_generation_scheduled / none / open / block` |
| EV15 PlanProduced | `r15 / plan_ready / none / open / block` |
| EV16 AuditionGenerationScheduled | `r16 / audition_generation_scheduled / none / open / block` |
| EV17 AuditionProduced | `r17 / awaiting_editorial_decision / editorial_decision / open / block` |
| EV18 EditorialDecisionRecorded | `r18 / editorial_decision_recorded / none / open / block` |
| EV19 DraftGenerationScheduled | `r19 / draft_generation_scheduled / none / open / block` |
| EV20 DraftProduced | `r20 / draft_ready / mechanical_validation / open / block` |
| EV21 DraftValidationScheduled | `r21 / draft_validation_scheduled / none / open / block` |
| EV22 MechanicalAssessmentRecorded | `r22 / mechanically_validated / graph_policy_validation / resolved / flag` |
| EV23 GraphValidationScheduled | `r23 / graph_validation_scheduled / none / resolved / flag` |
| EV24 GraphAssessmentRecorded | `r24 / graph_validated / comprehension_assessment / resolved / flag` |
| EV25 ComprehensionAssessmentRecorded | `r25 / reviewed / none / resolved / pass` |
| EV26 ResidueRecorded | `r26 / residue_recorded / none / resolved / pass` |

The reducer accepts an event only when the current full tuple equals the prior row (or the initial tuple for EV01), the event id/type match the row, and any event-specific guard passes. Acceptance replaces only the four non-revision axes with the row's values and increments revision by one. Unknown, skipped, repeated, reordered, or mismatched events reject without revision/head advance.

## EV22 correction-resolution guard

EV22 is the sole transition from `open` to `resolved`. It requires all of:

- prior tuple exactly EV21's resulting tuple;
- `correction_id = COR1` and `correction_sha256` equals the fixture-bound COR1 digest;
- `artifact_id = NE2` and `artifact_sha256` equals the fixture-bound NE2 digest;
- `assessment_id = MA2`, `assessment_result = pass`, and `assessment_sha256` equals the fixture-bound MA2 digest;
- no prior accepted EV22 for the run.

Wrong correction/artifact, missing or stale digest, a non-pass MA2, premature/duplicate EV22, or an unbound identifier rejects atomically. The correction is not erased; immutable COR1 remains addressable, while the state axis records that its exact replacement passed the required mechanical assessment.

## Live/replay and projection proof

One pure reducer function consumes the same closure and events for both paths. “Live” means reducing as each accepted event is appended; “replay” means reducing the complete immutable sequence from the initial closure in a fresh state. Canonical state bytes use recursively key-sorted compact JSON plus one terminal LF. SHA-256 is over those exact bytes. RS26 passes only when live bytes equal replay bytes and their digests match.

RP26 is constructed from a deep copy of RS26 plus read-only event-head/residue references. The checker snapshots RS26 bytes, derives RP26, then proves the RS26 bytes, revision, and accepted-event count did not change. RP26 is not appended as an event.

## Failure, integration, and authority boundaries

- Every invalid fixture returns `BLOCK`, names a stable error code, and proves unchanged revision/state.
- The checker reads only candidate JSON fixtures and emits a research validation receipt; it has no external effects.
- The receipt is evidence for research closeout only. It is not evidence of a Whisper runtime, durable store, crash recovery engine, ontology, product integration, or deployment.
- Existing revision-2 and prior receipts are immutable. Revision 3 supersedes only the proposed state-contract passages for research interpretation.
