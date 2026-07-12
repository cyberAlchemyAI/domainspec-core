# Shared Context: V0 Canvas Repair

## Source Anchors

- `projects/ide-extension/SPEC.md:24`
- `projects/ide-extension/SPEC.md:96`
- `projects/ide-extension/ARCHITECTURE.md:14`
- `projects/ide-extension/src/server.mjs:163`
- `projects/ide-extension/src/server.mjs:568`
- `projects/ide-extension/src/server.mjs:628`
- `projects/ide-extension/src/kernel/canvas.mjs:29`
- `projects/ide-extension/tests/session-content-workbench-publish.test.mjs`
- `projects/ide-extension/development/html-builder-architecture-review/findings.md`

## Preserved Behavior

- `/api/canvas/publish` request and response shape;
- normalized workspace-relative `.html` paths;
- workspace file remains V0 canonical body;
- same-path surface identity and same-hash idempotency;
- revision drift response;
- event-derived projection and interaction behavior;
- trusted-local value posture.

## Worktree Rule

The repository contains unrelated concurrent changes. Each SWU must inspect its
exact write scope, preserve intersecting user changes, and use scoped diffs.
