---
id: ide-extension-workbench-bridge-demo-v01-distill
project: ide-extension
status: pass
updatedAt: 2026-07-17
---

# Distill Validation

## Verdict

Pass.

## Selected Unit

The smallest coherent unit is the visible manual bridge demo loop in the
workbench UI.

## Why It Is Small Enough

- It reuses the existing open-poll bridge.
- It does not add worker behavior.
- It does not change receipt authority.
- It can start with one UI panel and focused tests.

## Why It Is Large Enough

Only adding one command hint would not prove user value. The unit must include
status, command recipe, and receipt display so the operator can see the complete
manual loop.

## Recomposition Proof

`TASK-WBD-001` creates the visible spine. `TASK-WBD-002` adds command use.
`TASK-WBD-003` adds terminal proof. `TASK-WBD-004` validates the blind boundary
and demo evidence. Together they implement the approved design without opening
deferred automation.

## Hidden Gaps

None blocking.

Non-blocking residue:

- Refresh cadence may be manual at first.
- UI copy must stay compact.
- Recovery states are L2 unless trivial to display from existing projection.
