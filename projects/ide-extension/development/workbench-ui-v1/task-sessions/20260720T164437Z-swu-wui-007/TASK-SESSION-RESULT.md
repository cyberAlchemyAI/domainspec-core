# Task Session Result: SWU-WUI-007

```yaml
swu_id: SWU-WUI-007
task_id: TASK-WUI-003
result: pass
capability_ref: task-session
receipt_kind: local-fallback
receipt_artifact: development/workbench-ui-v1/task-sessions/20260720T164437Z-swu-wui-007/TASK-SESSION-RESULT.md
files_touched:
  - src/ui/run-actions.mjs
  - src/server.mjs
  - public/demo/l0.html
  - tests/workbench-ui-v1-run-actions.test.mjs
  - tests/l0-workbench-ui.test.mjs
  - tests/e2e/workbench-ui-v1-actions.spec.mjs
  - development/workbench-ui-v1/task-sessions/20260720T164437Z-swu-wui-007/CONTEXT-PACK.md
  - development/workbench-ui-v1/task-sessions/20260720T164437Z-swu-wui-007/TASK-SESSION-RESULT.md
  - development/workbench-ui-v1/WORK-PACK.md
  - development/workbench-ui-v1/work-pack/tasks/TASK-WUI-003-LIFECYCLE.md
  - development/workbench-ui-v1/README.md
  - .craft/ledger.yml
  - .craft/index.json
validation:
  - `node --check` for resolver and server: pass
  - action resolver matrix: pass, 3/3
  - `npm run test:workbench`: pass, 6/6
  - `npm run test:bridge`: pass, 68/68
  - focused action Playwright journey: pass, desktop/mobile 2/2
  - existing approval/manual/action browser journeys: pass, desktop 3/3 and mobile 3/3
  - scoped `git diff --check`: pass
evidence:
  - development/workbench-ui-v1/task-sessions/20260720T164437Z-swu-wui-007/desktop-actions.png
  - development/workbench-ui-v1/task-sessions/20260720T164437Z-swu-wui-007/mobile-actions.png
blockers: []
residue:
  - SWU-WUI-008 is the next unit for retained Canvas placement.
  - Claimant-owned interrupt remains delegated to the claimed session; the browser observes Running and does not impersonate it.
  - Provider execution, browser control, workers, VSCodium hosting, and the separate SCW human usefulness review remain deferred by the Work Pack.
reroute: SWU-WUI-008
handoff_note: The browser now consumes RunView legal actions through a pure resolver. Approve and Make available are enabled only in their legal states; Available and Running are truthful status affordances; terminal states expose Inspect result; reject, unready, and release remain secondary and claimant-owned interrupt is delegated. Continue with retained Canvas placement.
```

## Result

PASS. `resolveRunActions(runView)` provides one truthful primary affordance for
all supported typestates, separates browser command IDs from status/navigation
affordances, and preserves claimant-owned interrupt as delegated. The page uses
that projection to enable only legal controls and adds terminal `Inspect result`
navigation to the existing Evidence region.

## Context And Gates

- Context pack: [CONTEXT-PACK.md](CONTEXT-PACK.md), 10 selected sources, 10/10
  obligations covered, strict coverage pass.
- Dependencies: [SWU-WUI-005 PASS](../20260720T161925Z-swu-wui-005/TASK-SESSION-RESULT.md),
  [SWU-WUI-006 PASS](../20260720T162753Z-swu-wui-006/TASK-SESSION-RESULT.md).
- Runtime: local Node and Playwright Chromium; no runtime delegation and no
  subagents.
- Decision gate: n/a; the primary/secondary/delegated matrix was determined by
  the existing UX and claimant-ownership contracts.
- Fallback search: none.

## Evidence

- The resolver matrix covers all ten supported typestates and proves every
  browser command is present in `RunView.legal_actions`.
- `claimed` resolves to Running with delegated `interrupt`, not a browser
  command; terminal states resolve to navigation-only Inspect result.
- The desktop/mobile journey proves Approve -> Make available -> Available ->
  Running and terminal Inspect result without timeline assertions.
- Existing approval and manual bridge browser journeys remain green on both
  viewports, including mobile action routing.
- Retained screenshots show the terminal Inspect result control is enabled and
  does not overlap other controls on desktop or mobile.

## Synchronization

- `SWU-WUI-007`: completed with this receipt.
- Parent `TASK-WUI-003`: completed for RunView projection, timeline, and legal
  action projection; later workspace/evidence units remain downstream.
- `SWU-WUI-008`: ready and is now the only next mutation-capable WUI handle.
- Craft ledger, human view, generated index, Work Pack, README route, and task
  synchronization are updated after this receipt.
- Experiment harness: not applicable; this is product implementation evidence,
  not reusable sigil behavior validation.

## Next Route

Run Task Session on `SWU-WUI-008` to place the retained Canvas artifact in the
primary workspace without changing Canvas server behavior.
