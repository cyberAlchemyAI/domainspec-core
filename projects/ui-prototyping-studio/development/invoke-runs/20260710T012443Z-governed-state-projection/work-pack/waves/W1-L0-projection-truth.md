# W1 - L0 Projection Truth

## Layer Question

After this wave, we know whether the browser can project the governed current
head as the primary artifact after Accept/Revert/external writes.

## Tasks

- [TASK-GSP-001](../tasks/TASK-GSP-001-current-head-projection.md)

## Gate

Pass only when `SWU-GSP-001` has a failing-before/passing-after witness.

## Validation

- Playwright current-head projection test.
- `/state` assertion after external CLI write while preview is running.
- Screenshot or DOM receipt showing current head, not original variant.
