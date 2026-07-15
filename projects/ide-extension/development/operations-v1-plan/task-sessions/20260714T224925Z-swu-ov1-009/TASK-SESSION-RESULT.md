# Task Session Result: SWU-OV1-009

```yaml
swu_id: SWU-OV1-009
result: pass
capability_ref: task-session
receipt_kind: local-fallback
receipt_artifact: development/operations-v1-plan/task-sessions/20260714T224925Z-swu-ov1-009/TASK-SESSION-RESULT.md
files_touched:
  - package.json
  - src/kernel/canvas-navigation.mjs
  - src/kernel/canvas-notifications.mjs
  - src/kernel/projector.mjs
  - src/server.mjs
  - tests/operations-v1-navigation.test.mjs
validation:
  - npm run test:operations-navigation: pass
  - npm run test:canvas-live: pass
  - npm run test:canvas-publish: pass
  - npm run test:canvas-replay: pass
  - npm run test:operations-replay: pass
  - npm run test:operations-derive: pass
  - npm run test:operations-replace: pass
  - npm run test:operations-append: pass
  - npm run test:operations-rebuild: pass
  - npm run test:persistence: pass
  - npm run test:schemas: pass
  - npm run test:operations-contracts: pass
  - Node syntax and scoped whitespace checks: pass
blockers: []
residue:
  - Browser frame loading, atomic swap, acknowledgement wiring, and Operations interaction routing remain deferred to SWU-OV1-010.
  - Refresh and acknowledgement diagnostics intentionally expire after 15 minutes, 128 commands, or restart.
  - One local workbench display target is global; browser identities, tabs, queues, and durable refresh replay remain excluded.
  - V0 bodies remain exact workspace-backed publications; unavailable or drifted bytes fail display admission.
  - Unrelated concurrent worktree changes remain preserved outside this SWU.
reroute: SWU-OV1-010
handoff_note: Make the browser consume /api/canvas/display and typed notices with hidden-frame load, atomic swap, and loaded/failed acknowledgement while retaining the last good frame.
```

## Result

PASS. The server now exposes one durable workbench display target independently
from `/api/canvas/current`. Redirect validates an exact V0 workspace revision or
verified Operations blob, digest-binds the command id, appends the existing V4
`canvas.display_target_selected` event, projects the target, and emits a typed
display notice. Exact retries return the committed result without another event;
conflicting IDs, unknown targets, drifted V0 bytes, and pruned revisions fail
without navigation history.

The display projection survives restart. A commit on the displayed Operations
surface advances that target to the new revision and emits a revision notice;
commits on other surfaces do neither. A later V0 publication keeps the existing
V0 current contract and durably makes that new V0 revision the display target.
Pure V1/V3 histories remain projection-exact until V4 state exists.

Refresh and browser acknowledgement are deliberately transient. They use the
same digest-bound command identity while retained, broadcast a distinct refresh
notice, append no event, and live in an in-memory store bounded to 15 minutes
and 128 commands. Loaded or failed acknowledgement updates only that store;
restart clears it while the display target remains recoverable from replay.

## Failure And Recovery Matrix

The focused server tests cover offline redirect recovery, same-command retry,
ID conflict, V0-current compatibility, typed SSE, selected/non-selected commits,
later V0 publication, unknown/drifted/pruned target rejection, failed load ack,
refresh duplicate suppression, expiry, capacity eviction, append failure, and
projection-failure repair. A committed redirect that loses its projection write
is recovered from the authoritative event and becomes exactly retryable.

## Validation Evidence

| Command | Result |
| --- | --- |
| `npm run test:operations-navigation` | PASS: 5 tests. |
| `npm run test:canvas-live` | PASS: 1 test. |
| `npm run test:canvas-publish` | PASS: 4 tests. |
| `npm run test:canvas-replay` | PASS: 4 tests. |
| `npm run test:operations-replay` | PASS: 8 tests. |
| `npm run test:operations-derive` | PASS: 6 tests. |
| `npm run test:operations-replace` | PASS: 7 tests. |
| `npm run test:operations-append` | PASS: 5 tests. |
| `npm run test:operations-rebuild` | PASS: 7 tests. |
| `npm run test:persistence` | PASS: 6 tests. |
| `npm run test:schemas` | PASS: 6 tests. |
| `npm run test:operations-contracts` | PASS: 8 tests. |
| Runtime/test syntax checks | PASS. |
| Scoped `git diff --check` | PASS. |

## Session Metadata

- Context pack: [CONTEXT-PACK.md](CONTEXT-PACK.md)
- Gate: [GATE.md](GATE.md)
- Strict context coverage: pass, 13/13 obligations
- Gate verdict: pass
- Runtime: local
- Handoff: none
- Subagents: not applicable; started 0, completed 0, failed 0, blocked 0
- Experiment harness: not applicable
- L2 promotion recommendation: partial; W4 browser delivery remains
- Next bounded unit: `SWU-OV1-010`
