---
id: ide-extension-domainspec-roadmap-lab-implementation-plan
status: planned
updatedAt: 2026-07-14
docType: implementation-plan
---

# Implementation Plan: DomainSpec v2 Roadmap Lab

## Outcome

Deliver a trusted-local pilot in which Victor can learn FPR-01, restate it,
request source inspection, submit a durable proposal, see its honest lifecycle
status, and—when an owner accepts a presentation-copy proposal—see the updated
roadmap rebuilt and republished with evidence.

This plan does not implement the feature and does not authorize source changes.
`WORK-PACK.md` is the canonical execution state.

## System Delta

```text
private roadmap inputs -------------------------------+
roadmap-copy.json --schema/coverage--> build-roadmap  |
source references ------------------------------------+
                                                        v
                                   fingerprinted roadmap.html
                                                        |
                              existing Canvas publish/current/content
                                                        |
                                    focused /demo/roadmap-lab mode
                                                        |
                         semantic postMessage -> existing Canvas event API
                                                        |
                                    cursor poll -> review packet adapter
                                                        |
                                  owner review/evidence reference
                                                        |
                              proposal history / accepted copy round trip
```

## Data Contracts

### Presentation copy

`roadmap-copy.json` must contain stable `field_id` values, associated `node_id`,
field role, human text, and schema version. The builder must reject duplicate
IDs, unknown nodes, missing required roles, unused required fields, and template
literal fallbacks for migrated copy.

### Build metadata

The builder emits or embeds:

- schema/build version;
- deterministic `input_fingerprint` over normalized roadmap data, presentation
  copy, and source-reference inputs;
- rendered node and field IDs;
- coverage summary;
- no absolute local paths.

### Semantic events

Event-specific contracts are validated in the generated surface and again by
the session-side review adapter. They remain payloads inside the existing
generic Canvas envelope.

| Event | Required semantic payload |
| --- | --- |
| `roadmap.orientation.acknowledged` | participant label, Canvas binding, input fingerprint |
| `roadmap.restatement.submitted` | participant label, node, answer fields, Canvas binding, fingerprint |
| `roadmap.source.requested` | participant label, node, repo-relative path, optional selector, bindings |
| `roadmap.improvement.proposed` | proposal id, participant label, class, node, optional field, observed original, proposed change/claim, reason, evidence refs, bindings |
| `roadmap.proposal.disposition.recorded` | proposal id, owner route, disposition, owner evidence reference, bindings |

The last event is a local projection reference. It never substitutes for the
owner evidence it names.

## Component Responsibilities

| Component | Planned responsibility | Must not own |
| --- | --- | --- |
| Roadmap copy schema/data | Stable human-facing fields and validation. | Node/claim identity or continuation state. |
| Roadmap builder/template | Coverage, fingerprint, learning packet, event-producing UI. | Proposal acceptance or direct source mutation. |
| Focused ide-extension mode | Display current roadmap surface, forward valid events, show history/status, preserve retry drafts. | DomainSpec/Craft/Whisper/research effects. |
| Existing Canvas kernel | Complete revision publication, current binding, append-only interactions, polling. | Event-specific business authority. |
| Review packet adapter | Revalidate event, detect stale context, classify target, emit owner handoff. | Execute the owner route or forge a receipt. |
| Trial/round-trip evidence | Prove real comprehension, usefulness, acceptance, rebuild, and republish. | General production readiness. |

## Algorithms

### Deterministic fingerprint

1. Load only declared build inputs.
2. Validate each input against its owned contract.
3. Normalize JSON objects with deterministic key ordering and UTF-8 encoding;
   normalize source-reference ordering by stable ID.
4. Hash a version-tagged manifest containing the normalized input digests.
5. Embed the resulting fingerprint and manifest version into the rendered HTML.
6. Golden-build the same inputs twice; bytes and fingerprint must match.

### Proposal admission

1. Read bindings supplied by the published surface, not user-editable controls.
2. Resolve node/field against the embedded projection manifest.
3. Capture the observed original value from the rendered model.
4. Validate proposal class and class-specific required fields.
5. Reject payloads exceeding the event-specific bound before the Canvas 16 KiB
   boundary.
6. Post the exact generic Canvas message envelope.
7. Mark submitted only after the parent returns API success; preserve draft on
   failure.

### Review and stale detection

1. Poll the append-only event by cursor and revalidate its semantic payload.
2. Compare surface/revision to the event record and fingerprint/node/field/
   observed value to current review inputs.
3. If any material binding differs, emit a review packet with
   `stale-review-required`; never rewrite the original event.
4. Otherwise classify owner route from the proposal class.
5. Produce a bounded review packet with original evidence references and the
   expected owner receipt shape.
6. Project a later disposition only when it cites owner-held evidence.

### Applied copy round trip

1. Select a presentation-copy proposal with an owner acceptance reference.
2. Apply only its accepted text through the presentation-copy owner route.
3. Validate copy, rebuild deterministically, and run regression/browser checks.
4. Publish the complete new HTML revision.
5. Retain original proposal, acceptance reference, source diff, old/new
   fingerprint, old/new Canvas revision, and validation output.
6. Only then project `applied-with-evidence`.

## Test Strategy

| Surface | Positive evidence | Negative/degraded evidence |
| --- | --- | --- |
| Copy contract | all required stable fields load and cover rendered targets | duplicate/unknown/missing/unused IDs; authority field mixed into copy |
| Build | deterministic bytes/fingerprint; no absolute paths; complete coverage | input change without fingerprint change; hidden template fallback; malformed source ref |
| Events | valid class payloads post and replay | extra fields, wrong types, oversized, editable binding, stale revision, API failure |
| Focused route | relevant context only; keyboard path; refresh/restart | no Canvas, republish during draft, disconnected notification, generic Craft leakage |
| Review routing | five class outcomes and owner handles | unsupported protected action, missing evidence ref, tampered original, cursor duplicate |
| Human trial | truthful 30-minute report and actionable proposal | facilitator rescue, incorrect answers, abandonment, no proposal—all retained as non-pass evidence |
| Round trip | accepted source change, rebuild, republish, before/after | submission treated as acceptance, stale accepted text, tests fail, new revision absent |

## Task Decomposition

| Task | Purpose | SWUs |
| --- | --- | --- |
| [TASK-RDL-CONTRACTS](work-pack/tasks/TASK-RDL-CONTRACTS.md) | Establish copy and semantic-event oracles. | 001–002 |
| [TASK-RDL-BUILDER](work-pack/tasks/TASK-RDL-BUILDER.md) | Extract copy, enforce coverage, and fingerprint builds. | 003–004 |
| [TASK-RDL-GUIDED-SURFACE](work-pack/tasks/TASK-RDL-GUIDED-SURFACE.md) | Build the FPR-01 learning/proposal UI and focused IDE route. | 005–006 |
| [TASK-RDL-HISTORY](work-pack/tasks/TASK-RDL-HISTORY.md) | Make proposals repeatable, restart-safe, and visibly stale when required. | 007–008 |
| [TASK-RDL-GOVERNED-HANDOFF](work-pack/tasks/TASK-RDL-GOVERNED-HANDOFF.md) | Classify proposals, create owner packets, and project receipt-backed dispositions. | 009–010 |
| [TASK-RDL-ROUNDTRIP](work-pack/tasks/TASK-RDL-ROUNDTRIP.md) | Validate degraded behavior and close one accepted copy update. | 011–012 |
| [TASK-RDL-VERIFY](work-pack/tasks/TASK-RDL-VERIFY.md) | Run the real Victor trial and audit pilot readiness. | 013–014 |

## Operational Constraints

- Execution is one selected SWU per Task Session.
- Before every SWU, re-read `git status --short -- projects/ide-extension` and
  compare the exact write scope with current owners; never clean or overwrite
  unrelated changes.
- The DomainSpec visibility package is private. Nothing from this work-pack is
  copied into public `arcanum/`.
- Node, schema, builder, and browser tests are scoped first; broader regression
  runs follow when shared files such as `l0.html`, `server.mjs`, or package
  scripts are touched.
- Human and owner gates return `block` or `waiting-for-owner`; they are not
  simulated.

