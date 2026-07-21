# Task Session Result: SWU-WUI-006

```yaml
swu_id: SWU-WUI-006
task_id: TASK-WUI-003
result: pass
capability_ref: task-session
receipt_kind: local-fallback
receipt_artifact: development/workbench-ui-v1/task-sessions/20260720T162753Z-swu-wui-006/TASK-SESSION-RESULT.md
files_touched:
  - src/ui/run-timeline.mjs
  - src/server.mjs
  - public/demo/l0.html
  - tests/l0-workbench-ui.test.mjs
  - tests/e2e/workbench-ui-v1-lifecycle.spec.mjs
  - tests/e2e/manual-session-bridge.spec.mjs
  - development/workbench-ui-v1/task-sessions/20260720T162753Z-swu-wui-006/CONTEXT-PACK.md
  - development/workbench-ui-v1/task-sessions/20260720T162753Z-swu-wui-006/TASK-SESSION-RESULT.md
  - development/workbench-ui-v1/WORK-PACK.md
  - development/workbench-ui-v1/work-pack/tasks/TASK-WUI-003-LIFECYCLE.md
  - development/workbench-ui-v1/README.md
  - .craft/ledger.yml
  - .craft/index.json
validation:
  - `node --check` for the renderer, mapper, and server: pass
  - `npm run test:workbench`: pass, 6/6
  - `npm run test:bridge`: pass, 68/68
  - focused lifecycle Playwright desktop/mobile matrix: pass, 4/4
  - intended desktop workbench/bridge/browser matrix: pass, 6/6
  - intended mobile workbench/bridge/browser matrix: pass, 6/6
  - scoped `git diff --check`: pass
evidence:
  - development/workbench-ui-v1/task-sessions/20260720T162753Z-swu-wui-006/desktop-timeline.png
  - development/workbench-ui-v1/task-sessions/20260720T162753Z-swu-wui-006/mobile-timeline.png
blockers: []
residue:
  - SWU-WUI-007 remains the next unit for legal primary-action projection from RunView.
  - The two `/ui/*.mjs` routes are explicit local workbench transport, not a general static source server.
  - Provider execution, browser control, workers, VSCodium hosting, and the separate SCW human usefulness review remain deferred by the Work Pack.
reroute: SWU-WUI-007
handoff_note: The browser now imports the canonical RunView mapper and ordered DOM renderer. Prepared, Approved, Available, Running, Result, and Receipt remain distinct; claimed work is Running, interrupted and residue labels remain truthful, and the timeline creates no action controls. Continue with legal primary-action resolution from RunView.
```

## Result

PASS. `renderRunTimeline(container, runView)` renders the ordered six-stage
lifecycle from the canonical `RunView`. Earlier stages are completed, the
current stage is active, later stages are pending, and interrupted/terminal
states retain truthful labels. The renderer never creates action controls.

## Context And Gates

- Context pack: [CONTEXT-PACK.md](CONTEXT-PACK.md), 9 selected sources, 10/10
  obligations covered, strict coverage pass.
- Dependency: [SWU-WUI-005 PASS](../20260720T161925Z-swu-wui-005/TASK-SESSION-RESULT.md).
- Runtime: local Node and Playwright Chromium; no runtime delegation and no
  subagents.
- Decision gate: n/a; the only transport choice was a bounded local route for
  the canonical UI modules and did not change authority or filesystem scope.
- Fallback search: none.

## Evidence

- The browser fixture imports `projectRunView` and `renderRunTimeline` and
  renders all ten supported typestates in desktop and mobile Chromium.
- The real bridge journey advances a prepared request through approval,
  availability, and an atomic claim; the Running stage remains distinct from
  Result and Receipt.
- Interrupted, flagged, blocked, and failed fixtures retain their RunView
  labels on the relevant lifecycle stage.
- The timeline contains six ordered `data-stage` elements, one active state,
  no buttons, and no horizontal overflow at either viewport.
- A small adjacent test-only mobile navigation repair keeps the existing manual
  bridge action journey green after the shell's view-specific action hiding.

## Synchronization

- `SWU-WUI-006`: completed with this receipt.
- Parent `TASK-WUI-003`: in progress; RunView projection and timeline rendering
  are complete.
- `SWU-WUI-007`: ready and is now the only next mutation-capable WUI handle.
- Craft ledger, human view, generated index, Work Pack, README route, and task
  synchronization are updated after this receipt.
- Experiment harness: not applicable; this is product implementation evidence,
  not reusable sigil behavior validation.

## Next Route

Run Task Session on `SWU-WUI-007` to resolve one legal primary action per
`RunView` state without exposing action controls from the timeline itself.
