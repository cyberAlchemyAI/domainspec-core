# Invoke Refresh: SWU-WFE-003B Option 1

- Mode: `refresh`
- Mutation mode: `apply-approved`
- Phase status: `pass`
- Handoff status: `ready`
- Evidence date: `2026-07-23`
- Approval source: direct user selection `1`

## Source signals

| ID | Type | Claim | Evidence |
| --- | --- | --- | --- |
| WFE003B-R1 | blocker_resolved | runtime packaging choice is resolved | `work-pack/session-evidence/SWU-WFE-003B/DECISION-GATE.md` |
| WFE003B-R2 | status_changed | SWU-WFE-003B can move from blocked to selected | Option 1 widens the exact runtime-support write scope |
| WFE003B-R3 | route_changed | the next route is bounded Task Session execution | serial work-pack order keeps SWU-WFE-004A queued |

## Applied deltas

- Recorded Decision Gate `PASS` with Option 1.
- Added `arcanum/spells/invoke/scripts/` and
  `arcanum/spells/invoke/schemas/` to the SWU scope.
- Kept fixtures, reports, and runners under `development/`.
- Changed SWU-WFE-003B from `blocked` to `selected`.
- Marked GAP-WFE-06 resolved without rewriting its historical blocker receipt.

## Boundary

This refresh changes planning and execution-readiness artifacts only. It does
not implement SWU-WFE-003B, close TASK-WFE-003, select SWU-WFE-004A, promote a
lifecycle artifact, or mutate `arcanum/tools/bootstrap_arcanum.sh`.

## Validation

- Decision selection matches a recorded real option.
- Work-pack, task contract, wave, gap ledger, decision ledger, and SWU manifest
  agree on Option 1 and the selected state.
- JSON syntax and scoped diff checks are required after materialization.

## Next route

`task-session` for `SWU-WFE-003B`.
