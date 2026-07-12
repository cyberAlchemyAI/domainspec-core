# Task Contract: Immutable Blob And Replay Substrate

## Control

| Field | Value |
| --- | --- |
| Task ID | `TASK-BLOB-REPLAY` |
| Objective | Make complete HTML bodies immutable and event references replayable before exposing operation APIs. |
| Layer / slice / wave | L0 / OV1-S2 / W1 |
| Execution owner | Task Session, one SWU at a time |

## Source Handles

- [Architecture storage contract](../../../operations-v1-design/ARCHITECTURE-BUNDLE.md#storage-namespaces)
- `projects/ide-extension/src/kernel/storage.mjs`
- `projects/ide-extension/src/kernel/projector.mjs`
- `projects/ide-extension/src/kernel/audit.mjs`
- `projects/ide-extension/tests/l0-persistence-recovery.test.mjs`
- `projects/ide-extension/tests/session-content-workbench-replay.test.mjs`

## SWU-OV1-003: Content-Addressed Blob Store

**Goal:** atomically store, read, verify, deduplicate, and inventory complete
Operations V1 HTML bodies without appending events.

**Dependencies:** SWU-OV1-002 pass.

**Exact write scope:** new `src/kernel/canvas-blobs.mjs`, focused blob tests,
`package.json` test script, and Task Session evidence. Existing event/projector
logic is read-only.

**Data model:** `<stateDir>/canvas/blobs/<sha256>.html`; temporary files remain
in that directory with a hidden unique name and `.tmp` suffix.

**Algorithm:**

1. Accept non-empty bytes no larger than the 8 MiB committed-result limit.
2. Compute SHA-256 from exactly those bytes and derive the final path.
3. If final content exists, verify its bytes hash to the requested digest and
   return it as deduplicated; mismatched content fails closed.
4. Otherwise create a unique temporary file with exclusive mode, write bytes,
   sync, close, and atomically rename to the digest path.
5. On any write failure, close and remove only the owned temporary file.
6. Reads validate digest syntax, file regularity, size, and content digest.
7. Diagnostics list blob count, total bytes, largest blob, temporary files, and
   caller-supplied reference reachability; they do not delete.

**Edge cases:** simultaneous same-digest writes, zero bytes, limit overflow,
pre-existing corrupt digest file, missing blob, permission failure, rename
failure, stale temporary file, and identical bytes across surfaces.

**Done criteria:** no partial final file is observable, duplicate bytes occupy
one final blob, and diagnostic order is deterministic.

**Validation:** `npm run test:operations-blobs`.

**Execution owner:** local fallback. **Expected result:** atomic/dedupe/error
matrix and retained test count. **Handoff:** SWU-OV1-004.

## SWU-OV1-004: Additive Event V4 And Reference Reconciliation

**Goal:** replay operations metadata and refuse committed references whose
unpruned bodies are absent or corrupt.

**Dependencies:** SWU-OV1-003 pass.

**Exact write scope:** `src/kernel/projector.mjs`, `src/kernel/storage.mjs`,
event fixtures, focused replay/recovery tests, and Task Session evidence. HTTP,
CLI, and browser files are read-only.

**Projected state:** add an Operations V1 namespace under canvas containing
derivation keys, operation surfaces, immutable revisions, operation records,
durable redirect records/display target, pruning state, and prune tombstones.
Existing V0 `surfaces`, `revisions`, `current_surface_id`, and interactions
remain present and replay-compatible.

**Event vocabulary:** version 4 admits only declared event shapes:

- `canvas.operations_surface_derived`;
- `canvas.content_operation_committed`;
- `canvas.display_target_selected`;
- `canvas.pruning_requested`;
- `canvas.revision_pruned`;
- Operations V1 interaction event when the displayed target is operations V1.

Only derivation and content events are exercised in this SWU; later SWUs add
their event-producing routes.

**Replay algorithm:** validate exact keys and bindings; enforce one derivation
key/digest outcome, ordered per-surface revision lineage, unique operation id,
operation digest/result bindings, current revision, and tombstone consistency.
After pure reduction, storage reconciliation verifies every unpruned blob ref.
Missing or corrupt referenced content fails closed. Projection write failure
after event append remains `reconciliation_required`; the referenced blob is
not classified orphaned.

**Edge cases:** exact V1/V2/V3 fixtures, mixed V3/V4 history, unknown V4 event,
duplicate ids, operation result outside surface lineage, missing blob, corrupt
blob, orphan blob, stale projection, and append-success/projection-failure.

**Done criteria:** old fixtures replay unchanged; valid V4 history repairs from
events plus blobs; invalid references never produce a usable projection.

**Validation:** `npm run test:operations-replay`, `npm run test:canvas-replay`,
`npm run test:bridge-replay`, and `npm run test:persistence`.

**Execution owner:** local fallback. **Expected result:** replay matrix and exact
fail-closed codes. **Handoff:** SWU-OV1-005.

## Synchronization

No route may emit V4 events until this task passes. Event shape changes after
fixture acceptance require a new version or explicit compatible migration.
