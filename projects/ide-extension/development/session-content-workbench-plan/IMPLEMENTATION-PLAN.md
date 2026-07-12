# Implementation Plan: Session Content Workbench

## Objective

Extend the existing loopback Approval Desk runtime so a Codex session can
publish a complete project `.html` file into the workbench, automatically
republish later revisions, and poll generic interactions emitted by that page.

## Brownfield Anchors

- Server and serialized mutation boundary: `src/server.mjs`.
- Event replay/projection: `src/kernel/projector.mjs` and `storage.mjs`.
- Schema registry and fixtures: `src/kernel/schema-validation.mjs`, `schemas/`,
  and `tests/fixtures/schemas/`.
- Session client: `scripts/session-bridge.mjs`.
- Browser workbench: `public/demo/l0.html`.
- Browser harness: `tests/e2e/server-harness.mjs` and Playwright specs.

## Data Model

The projection gains a `canvas` namespace:

```json
{
  "current_surface_id": "surface-...",
  "surfaces": {
    "surface-...": {
      "surface_id": "surface-...",
      "path": "relative/project/file.html",
      "title": "Presentation",
      "kind": "presentation",
      "current_revision_id": "revision-...",
      "revision_ids": ["revision-..."]
    }
  },
  "revisions": {
    "revision-...": {
      "surface_id": "surface-...",
      "content_sha256": "...",
      "byte_length": 56430,
      "published_at": "..."
    }
  },
  "interactions": [],
  "interaction_cursor": 0
}
```

One normalized workspace-relative path identifies one logical surface. First
publish assigns its `surface_id`; republishing the same path preserves that id
and adds a revision identified by the complete-file SHA-256.

## Publish Algorithm

1. Parse and schema-check `{path,title,kind}`.
2. Resolve the normalized relative path beneath configured `workspaceRoot`.
3. Require an existing regular `.html` file and read it completely.
4. Compute SHA-256 and byte length from those bytes.
5. Under the existing mutation queue, reconcile current projection.
6. Reuse the path's surface id or assign a new one; assign a revision id.
7. Append `canvas.surface_published` before returning success.
8. Expose the published content URL only from projected metadata.

The content route rereads the file and compares its hash with the requested
revision. If the file changed without republish, return `409 revision_changed`;
the already-loaded canvas remains visible until a complete revision is
published.

## Automatic Update Algorithm

`POST /api/canvas/publish` emits an in-process state-change notice only after
the event commits. `GET /api/canvas/notifications` uses EventSource. Every
notice carries the current revision id; the browser ignores duplicates, calls
`GET /api/canvas/current`, and reloads only when the revision changed.

Reconnect correctness comes from current-state fetch, not delivery of every
historical notice. After server restart, the reconnecting browser receives or
fetches current projected state. Manual Refresh remains available.

## Interaction Algorithm

1. A loaded surface sends `{type,eventName,payload}` with `postMessage`.
2. The host accepts messages only from the current iframe window and requires
   the fixed type plus JSON-compatible payload.
3. The host adds current surface/revision ids and POSTs the interaction.
4. The server verifies that the referenced revision is current, assigns stable
   `event_id` and monotonic cursor, then appends `canvas.interaction_recorded`.
5. `GET /api/canvas/events?after=N` returns matching events plus `next_cursor`.
6. Session CLI `events --after N` prints the response. Polling is at-least-once;
   stable event ids let the session ignore duplicates.

V0 has one global current canvas/event stream, matching the existing one-local-
operator experiment. Session authentication and multi-session routing belong to
later hardening.

## Browser Composition

- Add a full-width Canvas work area beneath the compact approval/connection
  controls.
- Header controls: title/kind/revision, Refresh, and open-current-content.
- Body: stable iframe that owns the available work area.
- States: no surface, loading, available, updating, unavailable, interaction
  sending/sent/failed.
- Existing proposal/history/evidence controls remain usable and do not overlay
  the canvas.

## Failure Rules

- Invalid or missing path: no event and no current-surface change.
- File changes during publish: hash/read result is one complete read; a later
  change requires republish.
- Changed file at content fetch: `409 revision_changed`, preserve current view.
- Duplicate publish of the same hash: return current revision idempotently and
  do not notify/reload.
- Stale iframe interaction: reject without appending.
- Failed event POST: surface remains usable and host exposes retry feedback.
- SSE unavailable: manual Refresh remains functional.

## Validation Strategy

- Schema fixtures and runtime schema enforcement.
- Mixed v1/v2/canvas replay plus restart projection tests.
- Publish/path/hash/idempotency/content API and CLI tests.
- Workbench structure/state tests.
- EventSource reconnect/duplicate/restart tests.
- Interaction source/binding/cursor/idempotency tests.
- Playwright desktop/mobile presentation, decision, and Craft journeys.
- Two real active-session witnesses with retained evidence.
