# Task Contract: Threshold-And-Grace Retention

## Control

| Field | Value |
| --- | --- |
| Task ID | `TASK-RETENTION` |
| Objective | Bound blob growth while preserving explicit, tombstoned deletion semantics. |
| Layer / slice / wave | L2 / OV1-S6 / W5 |
| Execution owner | Task Session, one SWU at a time |

## Source Handles

- [OVG-003 selection](../../../operations-v1-design/PLANNING-DECISION-GATE.md#selected-hybrid-retain-ask-then-automatically-prune)
- [Blob task](TASK-BLOB-REPLAY.md)
- [Cross-task decisions](../shared/cross-task-decisions.md)

## SWU-OV1-011: Diagnostics, Grace, Preview, And Manual Prune

**Goal:** ask the user at soft threshold and provide a deterministic preview and
manual commit path that never deletes before durable tombstones.

**Dependencies:** SWU-OV1-010 pass.

**Exact write scope:** new retention coordinator, projector/storage V4 pruning
events, storage/pruning API routes, workbench storage notice/control, focused
tests, and Task Session evidence.

**Interfaces:** `GET /api/canvas/storage`,
`POST /api/canvas/pruning/preview`, and
`POST /api/canvas/pruning/commit` with command id and expected candidate digest.

**Policy model:** `normal -> grace -> reclaiming | normal`. Crossing 1 GiB
appends one `canvas.pruning_requested` event with observed bytes and a deadline
seven days later. Diagnostics expose unique referenced bytes, orphan bytes,
largest blob, thresholds, deadline, state, eligible count, and blocked reason.

**Candidate algorithm:** after successful full replay, protect every operations
surface current revision; sort historical unpruned revisions by committed time
then revision id; select enough oldest revisions to bring unique referenced
bytes below 1 GiB, accounting for shared blob refs; hash event cursor, policy,
and selected ids into a preview digest.

**Manual commit:** under serialized mutation, recompute candidates and require
the preview digest. Append one `canvas.revision_pruned` tombstone per selected
revision. Delete a body only after its tombstone commits and only when no
unpruned revision references it. Any append failure stops; already committed
tombstones remain valid and un-tombstoned bodies remain.

**Response semantics:** pruned content URL returns `410 revision_pruned`.
Exact old operation retry returns original metadata plus
`operation_result_pruned`; it never reruns the operation.

**Edge cases:** shared digest, current old surface, stale preview, partial batch,
projection failure, no eligible revisions, already pruned request, unknown id,
and usage already below soft.

**Validation:** `npm run test:operations-retention`, replay tests, browser notice
test, and event-before-delete fault injection.

**Execution owner:** local fallback. **Expected result:** diagnostics, preview,
tombstone, 410, shared-ref, and partial-failure matrix. **Handoff:** SWU-OV1-012.

## SWU-OV1-012: Automatic Hard/Expired-Grace Reclamation

**Goal:** use the same safe coordinator automatically when hard threshold is
crossed or grace expires.

**Dependencies:** SWU-OV1-011 pass.

**Exact write scope:** retention scheduler/startup and post-commit hooks,
dependency-injected clock/threshold tests, automatic policy tests, and Task
Session evidence. Manual contract and defaults remain unchanged.

**Automatic algorithm:**

1. Evaluate after successful startup reconciliation and after blob-producing or
   pruning commits.
2. If history replay/reference validation is incomplete or invalid, disable all
   automatic deletion and report the cleanup block.
3. If bytes exceed 2 GiB, reclaim immediately; if grace deadline has expired
   while bytes exceed 1 GiB, reclaim; otherwise schedule one deadline timer.
4. Reconcile again under serialized mutation.
5. Delete stale temporary files and replay-proven orphan blobs first.
6. If still above target, use the same oldest-eligible candidate/tombstone path
   as manual pruning until below 1 GiB or no eligible revision remains.
7. Report failures and retry on next startup/evaluation; never delete current,
   shared, or un-tombstoned referenced content.

**Test policy:** production defaults stay fixed; tests inject byte-scale
thresholds and a fake clock. No environment variable changes V1 behavior.

**Edge cases:** restart after grace expiry, hard crossing before grace, timer
race with manual prune, event append failure, deletion permission failure,
orphan-only recovery, shared refs, all bytes current, malformed events, corrupt
blob, and process stop between tombstone and delete.

**Done criteria:** disk use converges below soft when eligible data exists, and
every non-convergence has an explicit diagnostic reason without semantic
corruption.

**Validation:** `npm run test:operations-retention-auto`, retention/replay/
persistence suites, and deterministic fake-clock repetitions.

**Execution owner:** local fallback. **Expected result:** automatic trigger and
restart matrix. **Handoff:** SWU-OV1-013.

## Synchronization

The plan constants are fixed. Changing thresholds, timer semantics, reclaim
order, or protected revision classes requires a recorded plan/decision delta.
