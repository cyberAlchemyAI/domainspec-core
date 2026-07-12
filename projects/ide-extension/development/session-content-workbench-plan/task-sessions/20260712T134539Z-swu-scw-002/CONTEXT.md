# Context Pack: SWU-SCW-002

## Selection

- Work-pack: `projects/ide-extension/development/session-content-workbench-plan/WORK-PACK.md`
- Task/SWU: `TASK-CANVAS-CONTRACT / SWU-SCW-002`
- Mode: standard, local Task Session
- Dependency: SWU-SCW-001 PASS

## Obligations

| ID | Obligation | Evidence | Status |
| --- | --- | --- | --- |
| O1 | Preserve exact v1/v2 history and checksums. | Existing projector and replay fixtures/tests. | covered |
| O2 | Add version-aware canvas publish and interaction events. | Task rules and accepted data model. | covered |
| O3 | Preserve path identity and revision ordering. | PD-SCW-001 and implementation plan. | covered |
| O4 | Enforce current revision and monotonic cursor. | Interaction algorithm and task edge cases. | covered |
| O5 | Prove mixed history and restart determinism. | Storage reconciliation API and W0 exit gate. | covered |
| O6 | Add no server, CLI, or browser behavior. | Exact SWU write scope. | covered |

## Execution Decisions

- Use event version 3 for the independent canvas event family.
- Initialize `canvas` lazily on the first canvas event so checked-in v1/v2
  projections remain field-for-field unchanged.
- Reject same-surface same-hash publish events during pre-append reduction;
  SWU-003 will return the existing revision without appending.
- Store projected interactions in append order with cursor equal to prior cursor
  plus one; event envelope id is the stable interaction event id.

## Gates

- Dependency, context, write scope, and validation: pass.
- Decisions: no unresolved blocker.
- Strict coverage: pass, six of six obligations.
- Server/API behavior: excluded.

## Required Evidence

- Existing v1 fixture remains exact and bridge replay remains green.
- Mixed v1/v2/v3 history produces bridge plus canvas state.
- Duplicate ids/hashes, stale revisions, cursor gaps, and future versions fail.
- Projection rebuild after deletion yields the same checksum.
