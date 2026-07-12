# Task Contract: Canvas Contract And Replay

## Control

| Field | Value |
| --- | --- |
| Task ID | `TASK-CANVAS-CONTRACT` |
| Objective | Define typed canvas state and deterministic replay without regressing bridge history. |
| Layer / slice / wave | V0-A / S-001 / W0 |
| Execution owner | Task Session, one SWU at a time |

## Source Handles

- [Shared context](../shared/context.md)
- [Cross-task decisions](../shared/cross-task-decisions.md)
- Approved architecture: `../../../session-content-canvas-design/ARCHITECTURE-BUNDLE.md`
- Runtime: `SPEC.md`, `ARCHITECTURE.md`, `schemas/`, schema registry,
  `src/kernel/projector.mjs`, storage, and replay tests.

## SWU-SCW-001: Canvas Contract Oracle

**Goal:** Define surface publication and interaction payloads before behavior.

**Dependencies:** none.

**Exact write scope:** `projects/ide-extension/SPEC.md`, `ARCHITECTURE.md`, new
`schemas/canvas-publish-request.schema.json` and
`schemas/canvas-interaction-request.schema.json`, schema registry/validator,
valid/invalid fixtures, focused contract tests, and required `package.json`
scripts. No server route or browser behavior.

**Implementation rules:**

1. Publish input requires schema version, workspace-relative `.html` path,
   bounded title, and kind (`presentation`, `decision`, `craft`, or `generic`).
2. Interaction input requires surface id, revision id, bounded event name, and a
   JSON object payload with a bounded serialized size.
3. Define projected `CanvasSurface`, `CanvasRevision`, and `CanvasInteraction`
   fields in SPEC/ARCHITECTURE, including stable ids, hash, bytes, timestamps,
   cursor, and current-state semantics.
4. Define complete-file publication, same-path surface identity, same-hash
   idempotency, hash-drift response, and global V0 stream explicitly.
5. Register schemas explicitly and add fixtures that fail for absolute/path-
   traversal paths, non-HTML files, blank event names, arrays as payloads, and
   additional fields.
6. Preserve all current schemas and fixtures unchanged.

**Edge cases:** Windows separators, `.`/`..`, percent-like path strings, empty
title, unknown kind, oversized payload, non-JSON values, schema union overlap.

**Done criteria:** spec/architecture/schemas agree; valid fixtures pass; each
invalid fixture fails at its intended field; no runtime behavior changes.

**Validation:** `npm run validate:schemas`, focused canvas contract tests, and
the existing bridge contract suite.

**Expected result:** pass with contract paths and test counts. **Handoff:**
`SWU-SCW-002` only after all schema oracles pass.

## SWU-SCW-002: Canvas Event Replay

**Goal:** Project published surfaces, revisions, and interactions from persisted
events while preserving all existing history.

**Dependencies:** `SWU-SCW-001` pass.

**Exact write scope:** `src/kernel/projector.mjs`, storage integration only if
needed, new canvas event fixtures, and focused replay/restart tests.

**Implementation rules:**

1. Add a version-aware canvas event branch without rewriting v1/v2 logs.
2. Initialize an empty `canvas` namespace deterministically.
3. Apply `canvas.surface_published`: enforce normalized path identity, preserve
   surface id for republish, append a unique revision, and set current surface.
4. Same surface/hash duplicate must be either rejected before append or replay
   idempotently; it must not create two revisions.
5. Apply `canvas.interaction_recorded`: require known current surface/revision,
   monotonic cursor, unique event id, and append-only order.
6. Mixed approval/bridge/canvas logs replay to the same projection after restart.
7. Unknown versions and illegal state transitions fail closed with event index.

**Edge cases:** interaction before publish, stale revision, duplicate cursor,
two surface paths sharing id, republish with new title/kind, truncated event,
restart after multiple revisions.

**Done criteria:** exact existing fixtures remain unchanged; legal canvas paths
replay; illegal paths fail; projection checksum is stable across restart.

**Validation:** focused canvas replay tests plus `npm run test:bridge` and
recovery tests.

**Expected result:** pass with mixed-history and restart evidence. **Handoff:**
W0 closes and `SWU-SCW-003` becomes ready.

## Synchronization

Update statuses only from Task Session results. Any need for snapshots,
authentication, or per-session streams goes to the shared gap ledger.
