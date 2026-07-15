# Context Pack: SWU-OV1-003

- Task: `SWU-OV1-003` - Content-Addressed Blob Store
- Mode: standard
- Handoff: none; local Task Session execution
- Strict coverage: pass
- Gate verdict: pass
- Runtime: local

This file is session evidence. It is not a canonical planning or contract
source.

## Objective

Add a standalone content-addressed store for complete Operations V1 HTML bytes.
It must atomically write, verify, read, deduplicate, and inventory bodies under
`<stateDir>/canvas/blobs/` without appending events or changing projection,
server, CLI, or browser behavior.

## Obligation Matrix

| ID | Obligation | Controlling evidence | Status |
| --- | --- | --- | --- |
| O1 | Store only non-empty Buffer bytes no larger than the frozen 8 MiB result limit. | Task contract algorithm; SWU-OV1-001 constants. | covered |
| O2 | Derive lowercase SHA-256 final identity and path `<stateDir>/canvas/blobs/<digest>.html`. | Task data model and algorithm; architecture namespace. | covered |
| O3 | Verify an existing digest path before returning a deduplicated result; corrupt content fails closed. | Task algorithm step 3. | covered |
| O4 | Write a hidden unique sibling temp file exclusively, sync, close, and rename atomically. | Task algorithm step 4; existing `atomicWriteJson` pattern. | covered |
| O5 | On failure, close and remove only this operation's owned temp file. | Task algorithm step 5. | covered |
| O6 | Reads validate digest syntax, regular-file status, non-empty/size bounds, and exact digest. | Task algorithm step 6; artifact path patterns. | covered |
| O7 | Diagnostics deterministically report blob count, total bytes, largest blob, temporary files, and caller-supplied reachability without deleting. | Task algorithm step 7 and done criteria. | covered |
| O8 | Cover simultaneous same-digest writes, zero/overflow, corruption, missing, permission, rename failure, stale temp, and identical-byte dedupe. | Task edge-case matrix. | covered |
| O9 | Keep event, projector, server, CLI, browser, and V0 behavior read-only. | Exact write scope; shared Worktree Rule. | covered |
| O10 | Run focused blob tests plus inherited contract/transform checks. | Task Validation and dependency evidence. | covered |
| O11 | Synchronize a PASS receipt before exposing SWU-OV1-004. | Work-pack gate 2; W1 sequence. | covered |

## Selected Context

1. `development/operations-v1-plan/WORK-PACK.md`
   - Selectors: SWU manifest, gate checks, blockers/gaps, next route.
   - Covers: O9-O11.
2. `development/operations-v1-plan/work-pack/tasks/TASK-BLOB-REPLAY.md`
   - Selector: `SWU-OV1-003` and Synchronization.
   - Covers: O1-O11.
3. `development/operations-v1-plan/work-pack/waves/W1.md`
   - Selectors: entry, exit, promotion, stop.
   - Covers: O3, O7, O10, O11.
4. `development/operations-v1-plan/task-sessions/20260714T213203Z-swu-ov1-002/TASK-SESSION-RESULT.md`
   - Selectors: PASS result and reroute.
   - Covers: O10, O11.
5. `development/operations-v1-design/ARCHITECTURE-BUNDLE.md`
   - Selector: Storage Namespaces and event-before-blob order.
   - Covers: O2, O9.
6. `development/operations-v1-plan/work-pack/shared/cross-task-decisions.md`
   - Selectors: OV1-PD1, PD3, PD4.
   - Covers: O1-O3, O9.
7. `src/kernel/operations-contracts.mjs`
   - Selector: `OPERATIONS_V1_LIMITS.result_html_bytes`.
   - Covers: O1, O6.
8. `src/kernel/storage.mjs`
   - Selectors: `atomicWriteJson`, cleanup, typed reconciliation failures.
   - Covers: O4, O5, O7.
9. `src/kernel/artifacts.mjs`
   - Selectors: exclusive writes, regular-file checks, typed error style.
   - Covers: O3, O5, O6.
10. `tests/l0-persistence-recovery.test.mjs`
    - Selectors: temporary directories, failure injection, atomic residue checks.
    - Covers: O4, O5, O8, O10.
11. `tests/l0-artifact-evidence.test.mjs`
    - Selectors: hostile file and deterministic filesystem assertions.
    - Covers: O3, O6, O8, O10.

## Decisions And Assumptions

- Export `createCanvasBlobStore({ stateDir, fileSystem?, randomId? })` with
  `put(bytes)`, `read(digest)`, and `diagnostics(referencedDigests?)` methods.
- Writes accept Node `Buffer` values only. Existing workspace reads and the
  transformer already produce Buffers, and rejecting coercion preserves exact
  byte authority.
- Stable error codes distinguish invalid bytes/digests, empty/oversized bodies,
  missing/non-regular/corrupt blobs, and wrapped write failures.
- A per-store in-flight map serializes same-digest writes. It makes one local
  writer authoritative and lets concurrent followers verify/deduplicate the
  final body while preserving atomic on-disk semantics.
- Filesystem dependencies may be injected only through store construction for
  deterministic permission/rename failure tests. Production defaults are
  Node's `fs/promises` operations.
- Diagnostics return sorted `blobs`, `temporary_files`, `missing_references`,
  and `unreferenced_blobs` in addition to required totals/largest. Unknown
  sibling entries are reported rather than deleted.

## Write Scope

- New `src/kernel/canvas-blobs.mjs`.
- New `tests/operations-v1-blobs.test.mjs`.
- `package.json` only for `test:operations-blobs`.
- Task Session evidence and status synchronization after passing validation.

## Excluded

- Event append, replay, projector changes, operation services, routes, CLI,
  browser/UI, retention deletion, and orphan reclamation.
- String HTML parsing or transformation.
- Automatic cleanup of stale temporary, corrupt, orphan, or unknown files.

## Validation

1. `npm run test:operations-blobs`
2. `npm run test:operations-transform`
3. `npm run test:operations-contracts`
4. Focused syntax, deterministic-order, temp-residue, and whitespace checks

## Context Builder Result

- Files selected: 11
- Obligation coverage: 11/11, 100 percent
- Strict coverage: pass
- Blockers: 0
- Fallback search: state-directory and failure-injection patterns only; resolved
- Noise: bounded to explicit task sources and storage/test precedents
