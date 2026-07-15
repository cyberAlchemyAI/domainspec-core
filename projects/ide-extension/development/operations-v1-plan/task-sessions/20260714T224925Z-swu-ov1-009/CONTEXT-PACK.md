# Context Pack: SWU-OV1-009

- Task: `SWU-OV1-009` - Durable Target And Transient Refresh Runtime
- Mode: standard
- Handoff: none; local Task Session execution
- Strict coverage: pass
- Gate verdict: pass
- Runtime: local
- Dependency receipt: `../20260714T224033Z-swu-ov1-008/TASK-SESSION-RESULT.md`

## Obligation Matrix

| ID | Obligation | Status |
| --- | --- | --- |
| O1 | Keep `/api/canvas/current` V0-compatible and separate from the displayed target. | covered |
| O2 | Every new V0 publication becomes the durable displayed V0 revision through replay. | covered |
| O3 | Redirect admits only an existing V0 or Operations revision with available immutable body. | covered |
| O4 | Bind redirect command id to a stable normalized request digest. | covered |
| O5 | Same redirect id and digest is idempotent; different digest conflicts without an event. | covered |
| O6 | Commit one `canvas.display_target_selected` V4 event and recover it after restart. | covered |
| O7 | Operations commits never redirect; only commits on the selected Operations surface emit revision notices. | covered |
| O8 | Refresh validates the current display target and appends no event. | covered |
| O9 | Retain refresh status for at most 15 minutes and 128 commands with digest-bound retry. | covered |
| O10 | Browser acknowledgement updates only a known retained transient command. | covered |
| O11 | Restart clears refresh/ack status while preserving the durable display target. | covered |
| O12 | Emit distinguishable redirect, refresh, and revision notices over the existing SSE hub. | covered |
| O13 | Prove offline, duplicate, same-target, missing/pruned, failed-ack, restart, V0 publish, and non-selected commit behavior. | covered |

## Implementation Shape

- Add a small `canvas-navigation` service that projects display responses,
  admits redirect targets, commits durable redirect events, and owns a bounded
  in-memory refresh/ack store.
- Extend the notification hub to broadcast typed notices while preserving the
  existing V0 revision notice contract.
- Derive the V0 display target from each existing V3 publish event so one V0
  publish remains one event and replay restores the expected display.
- Keep redirect under the server mutation queue; refresh and acknowledgement
  mutate only the local transient store.

## Write Scope

- `src/kernel/projector.mjs` V0 display projection.
- `src/kernel/canvas-navigation.mjs` service and transient status store.
- `src/kernel/canvas-notifications.mjs` typed notice transport.
- `src/server.mjs` display/navigation/status/ack routes.
- Focused navigation tests and package command.
- Task Session and synchronized plan/Craft evidence.

## Excluded

- Workbench iframe changes, interaction rebinding, browser identity, tabs,
  durable refresh replay, navigation queues, pruning implementation, regions,
  workspace watch, and implicit rebuild.

## Context Builder Result

- Obligation coverage: 13/13, 100 percent
- Strict coverage: pass
- Blockers: 0
- Fallback search: none
- Noise: bounded to durable display and transient refresh runtime
