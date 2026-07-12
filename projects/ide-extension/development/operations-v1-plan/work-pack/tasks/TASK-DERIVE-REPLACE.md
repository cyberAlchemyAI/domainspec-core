# Task Contract: Exact Derivation And CAS Replacement

## Control

| Field | Value |
| --- | --- |
| Task ID | `TASK-DERIVE-REPLACE` |
| Objective | Prove the smallest coherent Operations V1 loop on immutable bytes. |
| Layer / slice / wave | L0 / OV1-S3 / W2 |
| Execution owner | Task Session, one SWU at a time |

## Source Handles

- [Surface derivation](../../../operations-v1-design/ARCHITECTURE-BUNDLE.md#surface-derivation)
- [CAS and retry](../../../operations-v1-design/ARCHITECTURE-BUNDLE.md#compare-and-set-and-retry)
- `projects/ide-extension/src/kernel/canvas.mjs`
- `projects/ide-extension/src/server.mjs`
- `projects/ide-extension/scripts/session-bridge.mjs`

## SWU-OV1-005: Derive Exact V0 Revision

**Goal:** copy one still-available V0 revision into a separate blob-canonical
surface exactly once.

**Dependencies:** SWU-OV1-004 pass.

**Exact write scope:** new operations service module, derivation and read routes
in `src/server.mjs`, derivation CLI support, focused API/CLI tests, and Task
Session evidence.

**Interfaces:** `POST /api/canvas/operation-surfaces` and
`GET /api/canvas/operation-surfaces/:surfaceId`.

**Algorithm:**

1. Enforce the 5 MiB HTTP request and derivation schema.
2. Under the existing serialized mutation boundary, reconcile projection.
3. Normalize semantic input in fixed field order and bind the idempotency key to
   its SHA-256 digest.
4. If the key exists with the same digest, return the original surface and
   revision; a different digest returns `derivation_key_conflict`.
5. Resolve the named V0 surface/revision without requiring it to be current.
6. Read its workspace path through existing canonical admission and require
   bytes to match the named revision digest and 4 MiB source limit.
7. On drift or unavailability, return `source_revision_unavailable` with no blob
   or event.
8. Store exact bytes, append `canvas.operations_surface_derived`, project, and
   return separate operations surface/revision identity.

**Postconditions:** derivation does not mutate, republish, synchronize, or
redirect V0; later V0 publication does not alter the derived surface.

**Failure modes:** blob success plus event failure leaves a reported orphan;
event success plus projection failure returns reconciliation required and
restart repairs it.

**Validation:** `npm run test:operations-derive` plus V0 publish/path/replay
suites.

**Execution owner:** local fallback. **Expected result:** exact-source,
idempotency, drift, crash, and V0 parity matrix. **Handoff:** SWU-OV1-006.

## SWU-OV1-006: Replace With CAS And Exact Retry

**Goal:** commit one complete inline replacement against an expected revision
and serve the immutable result after restart.

**Dependencies:** SWU-OV1-005 pass.

**Exact write scope:** operations service, operation/content routes, CLI operate
support, focused replace/idempotency/limit tests, and Task Session evidence.

**Interfaces:** `POST /api/canvas/operation-surfaces/:surfaceId/operations` and
`GET /api/canvas/operation-surfaces/:surfaceId/revisions/:revisionId/content`.

**Operation algorithm:**

1. Enforce 5 MiB HTTP and strict operation schema.
2. Build a normalized request object in fixed field order, replacing HTML body
   with its byte digest; hash the canonical JSON serialization.
3. Under serialized mutation, look up `operation_id` before checking CAS.
4. Same id/same digest returns original operation and result with
   `idempotent: true`, even when the surface has since advanced.
5. Same id/different digest returns `operation_id_conflict`.
6. Compare expected revision to current; mismatch returns `revision_changed`
   plus current revision and commits nothing.
7. Parse/serialize complete inline HTML, enforce 4 MiB input and 8 MiB result,
   store blob, append content-operation event, project, and notify only when the
   surface is already displayed.

**Content algorithm:** resolve surface/revision lineage; return 404 if unknown,
410 if pruned, otherwise verify/read blob and send exact bytes with no workspace
reread.

**Edge cases:** multibyte boundaries, same result bytes from different
operations, same operation retry after later commit, concurrent stale writers,
event append failure, projection replacement failure, restart, and unknown
surface/revision.

**Done criteria:** derive-plus-replace survives restart, exact retry never
creates a second revision, and every existing V0 canvas test remains green.

**Validation:** `npm run test:operations-replace`, `npm run test:canvas-publish`,
`npm run test:canvas-replay`, and `npm run test:canvas-paths`.

**Execution owner:** local fallback. **Expected result:** L0 evidence receipt
supporting or rejecting promotion to L1. **Handoff:** SWU-OV1-007 only on pass.

## Synchronization

W2 closure must link a retained Task Session result proving the complete L0
unit. Code completion without restart and V0 parity evidence does not promote.
