# TASK-OVSS-04 — Humane Authoring And Multi-View Parity

- Layer/slice: L1; S-004
- Wave: W1
- Objective: prove the complete create-review-correct-recover journey and parity across human, graph, and query views.
- Sources: Stage 06 workflow; Stage 07 AuthoringProfile attack; Stage 08 R7/R8
- Dependencies: W0 pass; B-002 resolved
- Proposed write scope: `arcanum/arcana/ontology-vault/development/semantic-source-spine/src/authoring/`; `arcanum/arcana/ontology-vault/development/semantic-source-spine/src/projectors/`; `arcanum/arcana/ontology-vault/development/semantic-source-spine/fixtures/authoring/`; `arcanum/arcana/ontology-vault/development/semantic-source-spine/fixtures/multi-view/`
- Current gate: blocked

## SWU-OVSS-008 — Atomic SourcePatch authoring journey

- Primary behavior: forms/editors produce explicit semantic patches, semantic diffs, atomic application, rebase, invalid-draft retention, and recovery.
- Acceptance boundary: one natural-person workflow completes without editing JSON/Markdown views directly; hidden AuthoringProfile semantics and stale preconditions fail.
- Split analysis: form generation, diff, patch application, and recovery are independently implementable, but the product decision is the full author journey; formal UX planning must decide whether to split execution.
- Dependencies: W0 and formal UX plan.
- Source anchors: Stage 06 workflow; Stage 08 R7 and atomic patch semantics.
- Write scope: authoring source and fixtures only.
- Done: executed positive journey, stale-base/hidden-default/dependent-relation negatives, and UX evidence.
- Validation: exact automation and browser/CLI evidence belong to the missing UX/runtime plan.
- Execution owner: Sigil Development plus UX validation owner.
- Handoff: semantic defaults must be explicit patch operations.

## Required Plan Refresh

GraphView and QueryView parity are part of TASK-OVSS-04 but do not yet have
atomic SWUs. A later Invoke Plan refresh must add them before W1 admission.

## Synchronization

No migration, admission, or public convention mutation in this task.
