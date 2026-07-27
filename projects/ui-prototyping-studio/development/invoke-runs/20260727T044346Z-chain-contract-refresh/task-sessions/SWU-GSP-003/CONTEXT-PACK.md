# Context Pack — SWU-GSP-003

## Contract

- Task: `TASK-GSP-003`
- SWU: `SWU-GSP-003`
- Dependency: joined passing `SWU-GSP-002` receipts.
- Objective: one application-owned serializable projection binds current-head
  preview, annotation identity, historical variants, staged state, actions,
  and evidence.
- Allowed writes:
  - new application projection module and unit test;
  - `backend/src/cli/studio.ts`;
  - one focused Playwright spec.
- Acceptance-critical validation: typecheck, full unit suite, focused browser
  witness.
- Successor after joined closeout: `SWU-GSP-004` only.

## Current Defect

The HTTP adapter chooses variant cards and the annotation baseline directly.
After Accept/Revert, `/raw/baseline` happens to resolve current content, but
the primary cards and annotation iframe still point at original variants. The
browser therefore presents multiple incompatible “current” identities.

## Projection Decision

`buildGovernedStateProjection` accepts a fresh `StudioSession`, the store port,
and artifact port. It reuses `resolveCurrentHtml` and returns:

- current-head availability, source, ref, HTML, route, revision ID, and label;
- annotation route bound to that same revision/content;
- clearly historical variant references;
- staged record/content availability and current structural diff;
- action availability;
- comment, revision, and handoff evidence flags.

The adapter renders the projection and retains legacy raw routes only as
compatibility aliases. `/state` keeps its old top-level signal fields and adds
the typed projection.

Strict coverage: pass.
