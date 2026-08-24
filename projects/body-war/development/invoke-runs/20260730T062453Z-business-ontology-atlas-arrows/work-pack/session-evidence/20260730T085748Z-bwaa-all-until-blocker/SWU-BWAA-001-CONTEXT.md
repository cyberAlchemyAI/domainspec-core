# Context Pack — SWU-BWAA-001

Mode: `standard`  
Handoff: none  
Status: `block-before-mutation`  
Strict coverage: `block`

## Task

Derive 13 deterministic ordered lens-flow groups that conserve all 109
cross-lens portal relation IDs. The first unit is uniquely dependency-ready.

## Controlling obligations

| Obligation | Evidence | Status |
| --- | --- | --- |
| exact task and frontier | `TASK-BWAA-001.md`, `WORK-PACK.md` | covered |
| semantic locks and authority ceiling | `WORK-PACK.md`, coverage receipt | covered |
| algorithm and failure behavior | `SPEC.md`, `ARCHITECTURE.md` | covered |
| write scope | task contract: projection, validator, projection test | covered |
| acceptance and validation | task acceptance table and three commands | covered |
| strict mutation admission | Task Session request/receipt schemas 1.2 | block |
| closeout owner preflight | `EXECUTION-CONTROL.md` plus live baselines | block |

## Current implementation evidence

- the existing projection conserves 237 nodes, 231 relations, 122 internal
  relations, 109 portals, and 44 isolates;
- current projection tests pass six baseline tests;
- current atlas validator passes;
- `projection.lens_flows` and its 13/109 fail-closed assertions are absent, so
  SWU-001 is not already complete.

## Execution contract

- write profile: `material-bound`;
- material writes:
  - `projects/body-war/ontology/business/scripts/view-atlas-projection.mjs`
  - `projects/body-war/ontology/business/scripts/validate-view-atlas.mjs`
  - `projects/body-war/ontology/business/tests/business-view-atlas-projection.test.mjs`
- execution output: the future Task Session terminal receipt only;
- lifecycle owner: private Body War business ontology atlas projection owner;
- authority: private;
- publication: private;
- ontology nodes, relations, policies, catalog, sibling views, and unrelated
  dirty files remain forbidden.

## Blocking gaps

1. No SWU-BWAA-001 Invoke material package exists.
2. No passing producer material receipt binds the three material writes.
3. No producer package currently binds the exact task/work-pack/context source
   frontier and validation commands.
4. Closeout owner receipt shape and validation are not packaged against the
   live Work Pack/Continuation baselines.

Context Builder cannot mark strict coverage true while those acceptance-
critical inputs are absent. Task Session must not implement the projection.
