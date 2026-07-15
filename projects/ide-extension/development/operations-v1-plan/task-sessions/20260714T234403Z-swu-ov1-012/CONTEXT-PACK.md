# Context Pack: SWU-OV1-012

- Task: `SWU-OV1-012` - Automatic Hard/Expired-Grace Reclamation
- Mode: standard
- Handoff: none; local Task Session execution
- Strict coverage: blocked
- Gate verdict: block
- Runtime: local
- Dependency receipt: `../20260714T232409Z-swu-ov1-011/TASK-SESSION-RESULT.md`

## Obligation Matrix

| ID | Obligation | Status |
| --- | --- | --- |
| O1 | Evaluate only after successful startup reconciliation and after blob-producing or pruning commits. | covered |
| O2 | Disable deletion when replay/reference validation is incomplete or invalid. | covered |
| O3 | Trigger immediately above 2 GiB or after expired grace while still above 1 GiB. | covered |
| O4 | Schedule one deadline timer when grace remains active below hard. | covered |
| O5 | Reconcile again under serialized mutation before every destructive action. | covered |
| O6 | Delete stale temporary files and replay-proven orphan blobs before committed history. | covered |
| O7 | Reuse the oldest-eligible shared-reference-aware candidate algorithm for committed history. | covered |
| O8 | Tombstone every referenced revision before body deletion. | covered |
| O9 | Retry failures on later startup/evaluation without corrupting committed history. | covered |
| O10 | Preserve current, displayed, shared-still-referenced, and un-tombstoned bodies. | covered |
| O11 | Close the durable grace cycle after orphan-only cleanup converges below soft. | blocked: no legal V4 transition |
| O12 | Recover restart between tombstone and deletion without silently restoring body availability. | covered |
| O13 | Keep production defaults fixed and inject policy/clock only in tests. | covered |
| O14 | Prove hard, expiry, timer, orphan-only, shared, failure, malformed-history, and restart behavior. | blocked by O11 |

## Blocking Finding

The frozen V4 vocabulary contains `canvas.pruning_requested` and
`canvas.revision_pruned`, but no pruning completion event. The projector opens
`active_request` only on the request event and clears it only when a real
revision tombstone carries `retention_state_after: normal`.

SWU-012 requires orphan-only recovery. Automatic deletion can therefore reduce
physical storage below soft without any eligible revision to tombstone. No
legal event remains that can durably return the projection to `normal` and
clear `active_request`. A diagnostic-only override would replay as grace after
restart and would reuse an expired request on the next threshold crossing.

## Excluded While Blocked

- No timers, startup/post-commit hooks, orphan deletion, automatic tombstones,
  scheduler state, or event-vocabulary mutation may be implemented before the
  completion transition is selected.

## Context Builder Result

- Obligation coverage: 12/14 complete, 2/14 blocked
- Strict coverage: block
- Blockers: 1
- Fallback search: none
- Noise: bounded to durable automatic-retention completion semantics
