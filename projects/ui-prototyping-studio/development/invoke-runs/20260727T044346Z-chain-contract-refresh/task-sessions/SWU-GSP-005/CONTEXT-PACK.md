# Context Pack — SWU-GSP-005

## Contract

- Task: `TASK-GSP-005`
- SWU: `SWU-GSP-005`
- Dependency: joined passing `SWU-GSP-004` receipts.
- Objective: durable Accept/Revert actions require actor-neutral explicit
  acknowledgment, while annotation and 390px comparison remain inspectable.
- Allowed writes: preview adapter plus focused desktop/mobile browser tests.
- Acceptance-critical validation: typecheck, full units, focused browser
  witness, and retained browser regression coverage.
- Successor after joined closeout: `SWU-GSP-006` only.

## Acknowledgment Boundary

Acknowledgment records that the caller inspected a named action context. It
does not grant authority or replace existing core authorization. The preview
POST must bind:

- action (`accept` or `revert`);
- current candidate/revision identity;
- target state;
- explicit `acknowledged=true`.

The server recomputes the expected context and refuses absent or stale
acknowledgment. Export remains terminal-only.

## Inspectable UI

- Accept shows candidate identity, target state, and full visible-diff recap.
- Revert shows current revision identity, target state, and the evidence for
  the current revision being undone.
- Annotation shows captured count immediately, keeps its form disabled until
  an actual `data-od-id` target is selected, and constrains severity to the
  domain values.
- At 390px the before/after cards stack and the document has no horizontal
  overflow.

Strict coverage: pass.
