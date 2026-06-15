# RUNTIME HANDOFF - Branch-As-View Ontology Refinement

## Runtime Objective

After confirmation, redesign the Ontologize method pack so the ontology is represented by a branch-view artifact tree rather than by a triad that merely materializes branches.

## Current Status

- Dispatch route: [REFINE-DISPATCH.json](REFINE-DISPATCH.json)
- Authorization: pending operator confirmation.
- Runtime-backed stages: not run.
- Subagent strategy: none.
- Research mode: no-research.

## What Runs After Confirmation

1. Build a local evidence baseline from `ONTOLOGY-BRANCHES.md`, `DAG-AND-METRICS.md`, and the current method pack.
2. Define the branch-as-view ontology target.
3. Review whether names should be flat files or branch directories.
4. Record no-research decision.
5. Distill the coherent unit: ontology root plus four branch views.
6. Redesign the method pack.
7. Review the redesign for naming confusion and authority drift.
8. Repair any residue.
9. Plan the task-session deltas.
10. Produce final synthesis.

## Deferred Until Confirmation

- Editing `projects/ontologize/development/view-triad-method/`.
- Renaming or replacing the old `view-triad` model.
- Any product-facing Ontologize mutation.

## Receipt Requirements

Each stage must return:

- `dispatch_id`
- `step_id`
- `capability_ref`
- `status`
- `artifacts`
- `validation`
- `observer_status`
- `blockers`
- `residue`
- `handoff_note`
