---
module: whisper-research-state-contract-repair
version: candidate-v1
status: plan-authored
docType: work-pack
authority_effect: none
---

# Work Pack

## Control fields

| Field | Value |
| --- | --- |
| `work_pack_id` | `WP-WHISPER-RSCH-STATE-001` |
| `output_mode` | `single-swu-plus-closeout` |
| `selected_swu` | `SWU-WHISPER-RSCH-STATE-001` |
| `execution_mode` | `one-unit` |
| `authority_effect` | `none` |
| `task_session_route` | `task-session` |
| `research_closeout_route` | `review -> writer -> auditor` |

## Objective and exclusion

Make the candidate Whisper EV01-EV26 command/event/state contract total and deterministically replayable, then use the passing receipt to close the two-front research. Excluded: ontology creation/admission, runtime implementation, Whisper source, co-op product/infra, public artifacts, external effects, deployment, promotion, release, production.

## Ordered frontier

| Order | Unit/gate | Owner | Writes | Acceptance | Successor |
| --- | --- | --- | --- | --- | --- |
| 1 | `SWU-WHISPER-RSCH-STATE-001` | Task Session | revision 3, state schema/fixture/negatives/checker, validation receipt | all three validation contracts pass twice; terminal receipt complete | research closeout |
| 2 | `GATE-WHISPER-RSCH-CLOSE-001` | research closeout | completion review, findings, audit, closure receipt, RESULT sync | non-vacuity pass; findings exact-bound; auditor pass | none |

The closeout gate is deliberately not represented as an implementation SWU. It cannot start without the content-addressed terminal receipt and cannot claim runtime or ontology proof.

## SWU atomicity

The schema, event fixture, negative fixtures, reducer/checker, revision-3 prose, and validation receipt are one smallest workable unit. A subset would either lack an oracle, lack enforcement, or lack research-consumable evidence. The unit is candidate-local, reversible, and bounded to new files.

## Material write set

- `projects/co-op-engine/research/2026-08-05-whisper-ontology-runtime/synthesis-revision-3.md`
- `projects/co-op-engine/research/2026-08-05-whisper-ontology-runtime/state-contract/state.schema.json`
- `projects/co-op-engine/research/2026-08-05-whisper-ontology-runtime/state-contract/event-sequence.json`
- `projects/co-op-engine/research/2026-08-05-whisper-ontology-runtime/state-contract/negative-fixtures.json`
- `projects/co-op-engine/research/2026-08-05-whisper-ontology-runtime/state-contract/validate-state-contract.mjs`
- `projects/co-op-engine/research/2026-08-05-whisper-ontology-runtime/receipts/state-contract-validation.json`

Task Session evidence may be written only under this package's `execution/` directory. L2 closeout later owns `review-completion.md`, `findings.md`, `receipts/findings-audit.json`, `receipts/evidence-closure-completion.json`, and the bounded synchronization of `RESULT.md`.

## Admission and stop rules

Task Session requires: fixed-point Design receipt; exact work-pack/task/context digests; explicit selected unit; content-addressed material package and producer receipt; passing mutation admission; and fast-entry `TASK_READY`. Stop on scope drift, stale baseline, changed prior evidence, failed validator, destructive/external effect, owner/authority change, or any ontology/runtime/product/deployment request.

## Closeout

Task Session emits one terminal receipt with write inventory, command results, runtime identity, before/after boundaries, remaining residue, and `authority_effect:none`. It emits a cursor to `GATE-WHISPER-RSCH-CLOSE-001` but does not execute that gate. The research closeout then issues its own reviewer and auditor receipts before RESULT synchronization.
