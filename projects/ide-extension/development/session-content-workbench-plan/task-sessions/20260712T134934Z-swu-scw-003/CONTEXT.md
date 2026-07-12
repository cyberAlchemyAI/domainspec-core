# Context Pack: SWU-SCW-003

## Selection

- Task/SWU: `TASK-PUBLISH-DISPLAY / SWU-SCW-003`
- Mode: standard, local Task Session
- Dependency: W0 and SWU-SCW-002 PASS

## Obligations

| ID | Obligation | Evidence | Status |
| --- | --- | --- | --- |
| O1 | Resolve and read complete relative project HTML. | Publish algorithm and canvas publish schema. | covered |
| O2 | Preserve path identity and same-hash idempotency. | PD-SCW-001 and v3 projector rules. | covered |
| O3 | Append publication before returning current metadata. | Existing mutation queue/store contract. | covered |
| O4 | Detect changed bytes at revision content fetch. | PD-SCW-004 and task failure rules. | covered |
| O5 | Expose one-shot session publish command. | Existing CLI process/exit conventions. | covered |
| O6 | Prove races, restart, invalid inputs, and append failure. | Task edge cases and W1 gate. | covered |
| O7 | Do not edit browser UI. | Exact write scope. | covered |

## Execution Decisions

- Use a focused `src/kernel/canvas.mjs` helper for workspace resolution,
  complete-file metadata, publication construction, and UI projection.
- Default `workspaceRoot` to the repository/evidence root, but expose an
  independent server option and environment variable.
- Return 201 for a new revision and 200 with `idempotent: true` for same hash.
- Reread and hash at content fetch; return `409 revision_changed` on drift.
- Extend the current one-shot CLI with `publish`; do not add event polling yet.

## Gates

- Dependency/context/write scope/validation: pass.
- Blocker decisions: none.
- Strict coverage: pass, seven of seven obligations.

## Required Evidence

- Publish/current/content and CLI agree.
- Same-hash races append one event.
- Changed file requires republish and preserves surface id.
- Restart reconstructs current metadata.
- Invalid/missing/nonfile inputs and append failure expose no current surface.
