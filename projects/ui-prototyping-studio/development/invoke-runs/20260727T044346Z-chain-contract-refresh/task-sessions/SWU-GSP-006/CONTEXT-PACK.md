# Context Pack — SWU-GSP-006

## Contract

- Task: `TASK-GSP-006`
- SWU: `SWU-GSP-006`
- Dependency: joined passing `SWU-GSP-005` receipts.
- Objective: export confirmation, evidence completeness, integration
  readiness, and implementation readiness remain separate facts.
- Allowed writes: handoff domain/use case, fail-closed persistence and HTTP
  projections, and slice tests.
- Acceptance-critical validation: typecheck and full unit/slice suite.
- Successor after joined closeout: `SWU-GSP-007` only.

## Predicate Boundary

- `exportConfirmed`: the core accepted a non-empty explicit confirmer.
- `evidenceComplete`: `missingRefs.length === 0`.
- `integrationReady`: evidence is complete and the exported head has accepted
  content plus honest diff evidence.
- `implementationReady`: integration-ready head also has applied tasks and no
  unresolved comments.

These are monotone conjunctions over explicit positive evidence. Confirmation
is recorded in the bundle but is not an input to either readiness predicate.
No release-authorization field is inferred.

## Compatibility

New exports always persist all four booleans and an explicit `missingRefs`
array. Older persisted bundles fail closed to false readiness at store and
HTTP projections rather than surfacing `undefined` as implied readiness.

Strict coverage: pass.
