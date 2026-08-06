# Synthesis Revision 3 — Deterministic State Repair

Status: `STATE_CONTRACT_REPAIRED_AND_EXECUTABLE_FOR_REVIEW`.

This revision supersedes only the deterministic-state passages of `synthesis-revision-2.md`. Every other evidence, ownership, fixture, privacy, stale-control, crash/retry, graph, denied-write, and claim-ceiling obligation in revision 2 remains unchanged and unexecuted unless a new receipt says otherwise.

## Closed state vocabulary

- `pending_gate`: `none | intent_freeze | editorial_decision | mechanical_validation | post_apply_review | corrected_intent_freeze | graph_policy_validation | comprehension_assessment`
- `correction_state`: `none | open | resolved`
- `outcome_ceiling`: `not_assessed | pass | flag | block`

`not_assessed` replaces the undeclared `absent`. `outcome_ceiling` is the current maximum research claim permitted by accumulated valid evidence, not a monotone severity order. It changes only at the declared reducer transitions.

## Exact reduction rule

The canonical oracle is `state-contract/event-sequence.json`; the state shape is `state-contract/state.schema.json`. Initial state is `r0 / not_started / none / none / not_assessed`. EV01 through EV26 each bind one exact prior full state and one exact result full state. Acceptance requires the current state to equal the declared prior state, the event id/type to equal the ordinal oracle row, and any event-specific guard to pass. Acceptance advances revision exactly once and replaces only the four non-revision axes. Unknown, skipped, repeated, reordered, or mismatched events reject without revision or state advance.

The repaired command-level milestones are:

| Event milestone | Resulting state |
| --- | --- |
| EV01 | `r1 / intake_recorded / intent_freeze / none / not_assessed` |
| EV06 | `r6 / awaiting_editorial_decision / editorial_decision / none / not_assessed` |
| EV09 | `r9 / draft_ready / mechanical_validation / none / not_assessed` |
| EV11 | `r11 / mechanically_validated / post_apply_review / none / flag` |
| EV12 | `r12 / correction_pending / corrected_intent_freeze / open / block` |
| EV17 | `r17 / awaiting_editorial_decision / editorial_decision / open / block` |
| EV20 | `r20 / draft_ready / mechanical_validation / open / block` |
| EV22 | `r22 / mechanically_validated / graph_policy_validation / resolved / flag` |
| EV24 | `r24 / graph_validated / comprehension_assessment / resolved / flag` |
| EV25 | `r25 / reviewed / none / resolved / pass` |
| EV26 | `r26 / residue_recorded / none / resolved / pass` |

All intermediate scheduled-event states are also explicit in the canonical oracle.

## EV22 correction resolution

EV22 remains `MechanicalAssessmentRecorded`; no extra event is invented. Its reducer rule may transition `correction_state` from `open` to `resolved` only when prior state is exactly EV21, correction is `COR1`, corrected artifact is `NE2`, assessment is `MA2/pass`, all three supplied digests equal the closure bindings, and no EV22 was already accepted. Wrong, missing, stale, premature, duplicate, or non-pass data rejects atomically.

This rule does not erase the correction or collapse an assessment into a correction. COR1 remains immutable evidence; `resolved` records that its exact replacement bytes passed the required second mechanical assessment.

## RS26, replay, and projection

The research checker uses one pure reducer for live append and a clean replay from closure. Canonical state bytes are recursively key-sorted compact JSON plus one terminal LF; SHA-256 is over those exact bytes. RS26 exists only if live bytes equal replay bytes and their digests match.

RP26 is derived from a deep copy of RS26 plus event-head and residue references. Projection creates no event/revision, and the checker proves that RS26 bytes, revision, and accepted-event count are unchanged. Replay runs only the pure reducer and starts zero external effects.

## Evidence and claim ceiling

`receipts/state-contract-validation.json` is the only execution evidence added by this SWU. It proves this repaired state-contract subset, not the full future Whisper fixture or a proper runtime. It grants no ontology, runtime, product, publication, deployment, promotion, release, or production authority. Research findings remain ineligible until independent non-vacuity review, writer, and auditor closeout pass.
