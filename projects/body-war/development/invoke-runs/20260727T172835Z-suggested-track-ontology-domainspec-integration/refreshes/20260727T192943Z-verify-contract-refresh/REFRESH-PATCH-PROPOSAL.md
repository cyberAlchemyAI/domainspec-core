# Refresh Patch Proposal

## Approved Scope

Update exactly:

1. `WORK-PACK.md`
2. `work-pack/tasks/TASK-BWOI-VERIFY.md`

## Signal-to-Delta Map

| Source signal | Evidence | Applied delta |
| --- | --- | --- |
| verification write scope missing | blocked `PREFLIGHT.json` | add exact Task Session report, digest, residue, and result paths |
| closeout inventory missing | blocked `PREFLIGHT.json` | add a `TASK-BWOI-VERIFY` closeout row with four exact sync targets |
| delta and validation contract missing | owner `CONTINUATION-HANDOFF.json` | add BWOI-scoped allowed deltas and owner checks |
| expected owner receipt missing | owner `CONTINUATION-HANDOFF.json` | add a distinct Verify receipt path |
| successor policy missing | W3 terminal route and owner handoff | declare no successor and require a new bounded plan for later work |

## Non-Deltas

- selected SWU and task statuses;
- implementation, tests, receipts, Craft state, or continuity cursor;
- ontology, DomainSpec, promotion, release, or deployment state.

