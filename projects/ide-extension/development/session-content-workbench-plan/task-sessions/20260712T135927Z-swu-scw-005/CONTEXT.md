# Context Pack: SWU-SCW-005

## Selection

- Task/SWU: `TASK-LIVE-UPDATE / SWU-SCW-005`
- Mode: standard, local Task Session
- Dependency: SWU-SCW-004 PASS

## Obligations

| ID | Obligation | Evidence | Status |
| --- | --- | --- | --- |
| O1 | Register and clean up Canvas EventSource clients. | Task algorithm steps 1 and 6. | covered |
| O2 | Broadcast exactly one identity-only notice after a new publish commit. | Task algorithm step 2. | covered |
| O3 | Reconnect and restart must converge through current-state authority. | Task algorithm step 3. | covered |
| O4 | Browser ignores duplicate revisions and swaps only after load. | Task algorithm step 4 and SWU-004 behavior. | covered |
| O5 | Preserve Refresh and expose connected/reconnecting/manual status. | Task algorithm step 5. | covered |
| O6 | Prove duplicate, reconnect, restart, idempotency, and fallback behavior. | SWU validation and edge cases. | covered |

## Execution Decisions

- Keep notification fan-out process-local and identity-only; event replay and
  `GET /api/canvas/current` remain durable authority.
- Send a current-state notice when a client connects, then fetch current state
  in the browser on every changed revision notice.
- Allocate monotonic process-local SSE ids; correctness does not depend on
  replaying missed ids because reconnect converges through current state.
- Reuse the SWU-004 preflight and atomic iframe replacement path.

## Gates

- Dependency/context/write scope/validation: pass.
- Blocker decisions: none.
- Strict coverage: pass, six of six obligations.

## Required Evidence

- Deterministic API tests cover registration, commit timing, idempotency, and cleanup.
- Browser journey proves automatic replacement, duplicate suppression, reconnect,
  server restart convergence, and manual fallback.
- Existing bridge and Approval Desk suites remain green.
