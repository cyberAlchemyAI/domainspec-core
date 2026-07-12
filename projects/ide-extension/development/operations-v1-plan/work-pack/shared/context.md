# Shared Context: Operations V1

## Accepted Source Anchors

- `projects/ide-extension/development/operations-v1-design/ARCHITECTURE-BUNDLE.md:89`
- `projects/ide-extension/development/operations-v1-design/ARCHITECTURE-BUNDLE.md:116`
- `projects/ide-extension/development/operations-v1-design/ARCHITECTURE-BUNDLE.md:175`
- `projects/ide-extension/development/operations-v1-design/ARCHITECTURE-BUNDLE.md:193`
- `projects/ide-extension/development/operations-v1-design/ARCHITECTURE-BUNDLE.md:281`
- `projects/ide-extension/development/operations-v1-design/DECISIONS.md`
- `projects/ide-extension/development/operations-v1-design/PLANNING-DECISION-GATE.md`
- `projects/ide-extension/src/kernel/canvas.mjs:130`
- `projects/ide-extension/src/kernel/projector.mjs:716`
- `projects/ide-extension/src/kernel/storage.mjs:71`
- `projects/ide-extension/src/server.mjs:492`
- `projects/ide-extension/src/server.mjs:568`
- `projects/ide-extension/src/server.mjs:628`
- `projects/ide-extension/public/demo/l0.html:1052`
- `projects/ide-extension/scripts/session-bridge.mjs:84`

## Preserved V0 Behavior

- `/api/canvas/publish` remains workspace-canonical and same-path identified.
- `/api/canvas/current` continues to describe V0 current publication state.
- `/api/canvas/surfaces/:surface/revisions/:revision/content` continues to
  detect workspace drift rather than claiming immutable history.
- V0 publication still selects its current surface as existing clients expect.
- Existing interactions, bridge history, schemas, replay, and approval desk
  behavior remain valid.

## Operations V1 Boundary

- Operations surfaces use separate ids and blob-canonical bodies.
- Workbench display selection is separate from V0 current publication state.
- Browser-loaded scripts are trusted-local content; server transformations do
  not execute them.
- Canvas operations remain preview/display effects, not protected-effect
  execution receipts.

## Worktree Rule

The repository contains unrelated concurrent changes. Every Task Session must
inspect its exact write scope, preserve intersecting edits, and use scoped diffs.
