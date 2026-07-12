# Task Session Result: SWU-SCW-005

```yaml
swu_id: SWU-SCW-005
result: pass
capability_ref: task-session
receipt_kind: native-stage
receipt_artifact: development/session-content-workbench-plan/task-sessions/20260712T135927Z-swu-scw-005/TASK-SESSION-RESULT.md
files_touched:
  - src/kernel/canvas-notifications.mjs
  - src/server.mjs
  - public/demo/l0.html
  - tests/session-content-workbench-notifications.test.mjs
  - tests/e2e/session-content-workbench.spec.mjs
  - package.json
  - development/session-content-workbench-plan/work-pack/evidence/SWU-SCW-005-assets/
validation:
  - npm run test:canvas-live (1 passed)
  - npm run test:bridge (66 passed)
  - npm run test:e2e (8 passed, desktop and mobile)
  - visual inspection of desktop and mobile degraded-path screenshots passed
  - git diff --check -- projects/ide-extension (pass)
blockers: []
residue:
  - notification ids are process-local; durable convergence intentionally uses current projected state
reroute: SWU-SCW-006
handoff_note: New complete revisions load automatically; reconnect, restart, duplicate suppression, and manual Refresh fallback are proved.
```

## Outcome

`/api/canvas/notifications` now exposes an identity-only EventSource stream.
Only successful non-idempotent publication commits broadcast. The browser
fetches current durable state after connection and changed-revision notices,
ignores duplicates, and keeps the existing atomic iframe replacement path.

Closing the HTTP server drains stream clients before shutdown. A reconnecting
browser converges after missed notices or process restart because the stream is
never treated as durable authority.

## Evidence

The browser witness generated four project HTML revisions, proved automatic
replacement and iframe interaction, suppressed an idempotent duplicate, crossed
a real same-port server restart, and then disabled EventSource to prove manual
Refresh still works.

- [Desktop manual fallback](../work-pack/evidence/SWU-SCW-005-assets/desktop-manual-fallback.png)
- [Mobile manual fallback](../work-pack/evidence/SWU-SCW-005-assets/mobile-manual-fallback.png)
