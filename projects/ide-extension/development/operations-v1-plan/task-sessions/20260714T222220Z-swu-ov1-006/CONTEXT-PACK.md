# Context Pack: SWU-OV1-006

- Task: `SWU-OV1-006` - Replace With CAS And Exact Retry
- Mode: standard
- Handoff: none; local Task Session execution
- Strict coverage: pass
- Gate verdict: pass
- Runtime: local
- Dependency receipt: `../20260714T221130Z-swu-ov1-005/TASK-SESSION-RESULT.md`

## Obligation Matrix

| ID | Obligation | Status |
| --- | --- | --- |
| O1 | Enforce 5 MiB HTTP and strict content-operation schema, admitting only replace in this SWU. | covered |
| O2 | Hash exact inline UTF-8 bytes and normalize fixed semantic fields with body replaced by its digest. | covered |
| O3 | Look up operation id before CAS; same id/same digest returns original, different digest conflicts. | covered |
| O4 | Require expected revision to equal current after idempotency lookup; stale input commits nothing. | covered |
| O5 | Enforce 4 MiB inline and 8 MiB serialized-result limits. | covered |
| O6 | Use parse5 8.0.1 complete-document replacement and persist exact serializer bytes. | covered |
| O7 | Store result blob before appending strict `canvas.content_operation_committed`. | covered |
| O8 | Preserve ordered surface lineage and allow distinct operations/revisions to share result digest/blob. | covered |
| O9 | Serve any admitted unpruned Operations revision from the blob store without workspace reread. | covered |
| O10 | Return 404 for unknown lineage and stable 410 metadata for a pruned revision. | covered |
| O11 | Notify only when the operated surface is already the selected Operations display target; never redirect. | covered |
| O12 | Prove retry-after-advance, conflict, stale/concurrent, limits, crash residue, restart, CLI, and V0 parity. | covered |

## Implementation Shape

- Extend `src/kernel/operations.mjs` with canonical operation normalization,
  `replace`, and immutable content lookup.
- Canonical normalized input contains fixed-order schema, operation, surface,
  expected revision, mode, whole-document target, and inline input kind plus
  `content_sha256`; raw HTML never enters the event log.
- Return operation, surface, revision, `content_url`, and `idempotent`.
- Extend the existing operation-surface metadata response with the current
  immutable content URL.
- Add POST operations and GET revision-content routes in `src/server.mjs`.
- Add generic CLI `operate --surface-id --input` so later append/rebuild reuse
  the same command contract.
- Broadcast the existing revision-available envelope only when the committed
  surface was already selected as the Operations display target; do not mutate
  that target.

## Write Scope

- `src/kernel/operations.mjs`.
- `src/server.mjs` operation/content routes and error mapping.
- `scripts/session-bridge.mjs` operate command.
- Focused replacement API/CLI tests and `package.json` command.
- Task Session and synchronized plan/Craft evidence.

## Excluded

- Append, rebuild, navigation commands, durable target changes, browser
  delivery behavior, retention deletion, V0 route/schema changes, and regions.

## Context Builder Result

- Obligation coverage: 12/12, 100 percent
- Strict coverage: pass
- Blockers: 0
- Fallback search: none
- Noise: bounded to replace, immutable content, and compatibility evidence
