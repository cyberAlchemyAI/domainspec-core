# Context Pack: SWU-OV1-012 Resume

- Task: `SWU-OV1-012` - Automatic Hard/Expired-Grace Reclamation
- Mode: standard
- Handoff: none; local Task Session execution
- Strict coverage: pass
- Gate verdict: pass
- Runtime: local
- Dependency receipt: `../20260714T232409Z-swu-ov1-011/TASK-SESSION-RESULT.md`
- Resolved blocker: `../20260714T234403Z-swu-ov1-012/DECISION-GATE.md`

## Obligation Matrix

| ID | Obligation | Status |
| --- | --- | --- |
| O1 | Evaluate only after successful startup reconciliation and after blob-producing or pruning commits. | covered |
| O2 | Disable deletion when replay/reference validation is incomplete or invalid. | covered |
| O3 | Trigger immediately at/above hard or after expired grace while still at/above soft. | covered |
| O4 | Schedule one deadline timer when grace remains active below hard. | covered |
| O5 | Reconcile again under serialized mutation before every destructive phase. | covered |
| O6 | Delete stale temporary files and replay-proven orphan blobs before committed history. | covered |
| O7 | Reuse the oldest-eligible shared-reference-aware candidate algorithm for committed history. | covered |
| O8 | Tombstone every referenced revision before body deletion. | covered |
| O9 | Retry failures on later startup/evaluation without corrupting committed history. | covered |
| O10 | Preserve current, displayed, shared-still-referenced, and un-tombstoned bodies. | covered |
| O11 | Close the durable grace cycle after orphan-only cleanup converges below soft. | covered by selected completion event |
| O12 | Recover restart between tombstone and deletion without silently restoring body availability. | covered |
| O13 | Keep production defaults fixed and inject policy/clock/timer only in tests. | covered |
| O14 | Prove hard, expiry, timer, orphan-only, shared, failure, malformed-history, and restart behavior. | covered |

## Controlling Decision

The user selected additive `canvas.pruning_completed`. It binds the active
request to automatic cleanup evidence and can clear that request only after a
validated final total is below the request's soft limit. Existing revision
tombstones retain their exact meaning.

## Execution Boundary

- Extend V4 by one additive event and projector transition.
- Add automatic cleanup and one deadline timer to the existing retention
  coordinator.
- Enter every startup, post-commit, and timer evaluation through the server's
  existing mutation queue.
- Preserve the manual API, thresholds, candidate order, and tombstone-before-
  delete behavior.
- Add focused deterministic tests and synchronize Task Session/Craft evidence.

## Context Builder Result

- Obligation coverage: 14/14 complete
- Strict coverage: pass
- Blockers: 0
- Fallback search: none
- Noise: bounded to SWU-OV1-012 automatic retention
