# Task Session Result: SWU-SCW-006

```yaml
swu_id: SWU-SCW-006
result: pass
capability_ref: task-session
receipt_kind: native-stage
receipt_artifact: development/session-content-workbench-plan/task-sessions/20260712T140913Z-swu-scw-006/TASK-SESSION-RESULT.md
files_touched:
  - src/server.mjs
  - scripts/session-bridge.mjs
  - public/demo/l0.html
  - tests/session-content-workbench-interactions.test.mjs
  - tests/session-content-workbench-cli.test.mjs
  - tests/l0-workbench-ui.test.mjs
  - tests/e2e/session-content-workbench.spec.mjs
  - package.json
validation:
  - npm run test:canvas-interactions (4 passed)
  - npm run test:schemas (6 passed)
  - npm run test:canvas-replay (4 passed)
  - npm run test:bridge (66 passed)
  - npm run test:e2e (8 passed, desktop and mobile)
  - visual inspection of desktop/mobile Canvas controls passed
  - git diff --check -- projects/ide-extension (pass)
blockers: []
residue:
  - interaction admission proves a request event, never the requested skill effect
reroute: SWU-SCW-007
handoff_note: Generic iframe actions now commit durably and return through stable non-destructive cursor polls and the one-shot CLI.
```

## Outcome

Current iframes can send the fixed `ide-extension.canvas.event` message with a
generic event name and JSON-object payload. The host rejects other window
sources and malformed messages, binds valid input to the loaded surface and
revision, and exposes Sending, Sent, Rejected, Failed, and explicit Retry states.

The server enforces the promised 16 KiB body limit before parsing, validates
the schema and current revision, assigns stable event id/time/cursor inside the
mutation queue, and appends `canvas.interaction_recorded`. Cursor polls are
ordered and non-destructive; a repeated cursor returns the same stable ids.
`session-bridge events --after N` prints that exact poll response.

## Boundary

The browser witness proves that a user action becomes a durable, pollable
request. It does not claim that Decision Gate, Craft, or any other capability
ran. That effect boundary remains with the active session and later witness.
