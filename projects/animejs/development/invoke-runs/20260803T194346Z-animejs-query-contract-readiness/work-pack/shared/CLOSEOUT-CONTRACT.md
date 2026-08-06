# Task Session Closeout Contract

## Common route

- Lifecycle owner route: `invoke:refresh:apply-approved`
- Terminal source receipt projection: `TASK-SESSION-TERMINAL-RECEIPT.schema.json`
- Canonical governance receipt: `.agents/skills/task-session/schemas/governance-terminal-receipt.schema.json`
- Expected owner receipt schema: `work-pack/shared/refresh-report.schema.json`
- Activation source: `continuation`
- Mutation mode: `apply-approved`
- Authority effect: none

## Declared synchronization inventory

Every SWU may synchronize only these four planning artifacts:

1. `WORK-PACK.md`
2. its parent `work-pack/tasks/TASK-*.md`
3. `PLAN-TRANSPORT.json`
4. `HANDOFF-STATE.json`

## Baseline binding

The baseline is the exact SHA-256 and size tuple captured for all four targets by the latest Work Pack Readiness Audit whose work-pack SHA matches the Task Session request. Task Session must rehash the live targets during Step 4 closeout preflight and immediately before Step 8 synchronization. Any drift blocks before implementation mutation or owner dispatch.

## Allowed delta classes

- `evidence_added`
- `blocker_opened`
- `blocker_resolved`
- `status_changed`
- `route_changed`

No delta may execute implementation or another SWU, widen targets, change authority, promote, publish, deploy, release, accept policy/cost/risk, or perform destructive cleanup.

## Owner validation

The Refresh owner must:

1. validate its receipt against `work-pack/shared/refresh-report.schema.json`;
2. parse `PLAN-TRANSPORT.json` and `HANDOFF-STATE.json`;
3. verify that only the declared SWU row/task status and deterministic route changed;
4. verify that every applied change maps to the source terminal receipt;
5. return a separate receipt at the exact per-SWU path below.

## Per-SWU successor policy

| SWU | Expected owner receipt | Unique successor |
| --- | --- | --- |
| SWU-AKV-QRY-001 | `closeout/SWU-AKV-QRY-001/refresh-report.json` | SWU-AKV-QRY-002 |
| SWU-AKV-QRY-002 | `closeout/SWU-AKV-QRY-002/refresh-report.json` | SWU-AKV-QRY-003 |
| SWU-AKV-QRY-003 | `closeout/SWU-AKV-QRY-003/refresh-report.json` | SWU-AKV-QRY-004 |
| SWU-AKV-QRY-004 | `closeout/SWU-AKV-QRY-004/refresh-report.json` | SWU-AKV-QRY-005 |
| SWU-AKV-QRY-005 | `closeout/SWU-AKV-QRY-005/refresh-report.json` | none; expose `invoke:plan` for a relation-repair package |

The successor is exposed only after dependency readiness is mechanically true. It is never executed during closeout.
