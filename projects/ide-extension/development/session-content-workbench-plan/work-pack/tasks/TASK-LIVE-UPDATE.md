# Task Contract: Automatic Complete-Revision Update

## Control

| Field | Value |
| --- | --- |
| Task ID | `TASK-LIVE-UPDATE` |
| Objective | Make a newly published complete revision appear automatically while preserving manual Refresh. |
| Layer / slice / wave | V0-B / S-003 / W2 |
| Dependencies | `SWU-SCW-004` pass |

## SWU-SCW-005: EventSource Notice And Reload

**Goal:** Add the smallest automatic-update loop after manual display is proved.

**Exact write scope:** focused notification helper if useful,
`src/server.mjs`, `public/demo/l0.html`, API/UI/e2e tests, and package scripts.

**Algorithm:**

1. Register EventSource clients at `/api/canvas/notifications`.
2. After a successful non-idempotent publish commit, broadcast one notice with
   revision id and SSE id; never send file bytes.
3. On connection/reconnection, send a current-state notice or require an
   immediate current-state fetch so missed notices cannot lose the latest state.
4. Browser compares revision id, ignores duplicates, fetches current metadata,
   and swaps iframe only after the new content URL loads.
5. Preserve Refresh as fallback and show connected/reconnecting/manual status.
6. Close client registrations on connection close and server shutdown.

**Edge cases:** duplicate notice, disconnect during publish, reconnect after
multiple publishes, server restart, idempotent same-hash publish, unavailable
content, rapid sequential complete revisions, EventSource unsupported/error.

**Done criteria:** new revision appears without Refresh; duplicates do not
reload; reconnect/restart converges to latest revision; manual fallback works;
current iframe is preserved until replacement loads.

**Validation:** deterministic notification tests, browser reconnect/duplicate/
restart journey, generated-presentation republish journey, full bridge suite.

**Expected result:** pass with automatic and degraded-path evidence. **Handoff:**
`SWU-SCW-006`.
