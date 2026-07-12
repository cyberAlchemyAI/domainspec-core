# Task Contract: Interaction Return

## Control

| Field | Value |
| --- | --- |
| Task ID | `TASK-INTERACTION-RETURN` |
| Objective | Return generic user actions from the current HTML surface to session polling. |
| Layer / slice / wave | V0-C / S-004 / W3 |
| Dependencies | `SWU-SCW-005` pass |

## SWU-SCW-006: Interaction Event And Poll Protocol

**Goal:** Close iframe -> workbench -> kernel -> session without adding skill-
specific endpoints.

**Exact write scope:** interaction schema/fixtures if contract corrections are
needed, projector/server, `scripts/session-bridge.mjs`, `public/demo/l0.html`,
focused Node/UI/CLI tests, and package scripts.

**Algorithm:**

1. Listen for fixed-type `postMessage` events from the current iframe window.
2. Validate bounded event name and JSON-object payload in the host; attach the
   current surface and revision ids.
3. POST to `/api/canvas/events`; server schema-checks, confirms the revision is
   current, assigns event id/cursor/time, and commits one interaction event.
4. Host shows sending/sent/failed state and allows explicit retry after failure.
5. `GET /api/canvas/events?after=N` returns ordered events with cursor greater
   than N and `next_cursor`; empty polls are successful.
6. CLI `events --after N` prints the exact poll response.
7. Retrieval is at-least-once; stable event ids are the dedupe key.

**Edge cases:** message from another window, stale iframe after reload, blank or
oversized event, array payload, duplicate POST retry, append failure, cursor
beyond end, negative/noninteger cursor, restart before poll.

**Done criteria:** one valid surface action creates one durable pollable event;
invalid/stale actions create none; order and cursor survive restart; existing
CLI commands and workbench flows regress nowhere.

**Validation:** focused interaction API/projector/CLI/UI tests, duplicate/restart
cases, and full bridge/browser suites.

**Expected result:** pass with exact event/poll evidence. **Handoff:**
`SWU-SCW-007`.
