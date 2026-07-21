# Task Session Result: SWU-WUI-008

```yaml
swu_id: SWU-WUI-008
task_id: TASK-WUI-004
result: pass
capability_ref: task-session
receipt_kind: local-fallback
receipt_artifact: development/workbench-ui-v1/task-sessions/20260720T165903Z-swu-wui-008/TASK-SESSION-RESULT.md
files_touched:
  - tests/e2e/workbench-ui-v1-canvas.spec.mjs
  - tests/e2e/operations-v1-navigation.spec.mjs
  - tests/e2e/workbench-ui-v1-shell.spec.mjs
  - development/workbench-ui-v1/task-sessions/20260720T165903Z-swu-wui-008/CONTEXT-PACK.md
  - development/workbench-ui-v1/task-sessions/20260720T165903Z-swu-wui-008/TASK-SESSION-RESULT.md
validation:
  - focused Canvas Playwright witness: pass, desktop/mobile 2/2
  - existing Operations navigation Playwright regression: pass, desktop/mobile 2/2
  - intended desktop shell Playwright check: pass, 1/1
  - intended mobile reachability Playwright check: pass, 1/1
  - Canvas contract suite: pass, 4/4
  - Canvas live notification suite: pass, 1/1
  - Canvas publish and CLI suite: pass, 4/4
  - workbench UI unit suite: pass, 6/6
  - `node --check tests/e2e/workbench-ui-v1-canvas.spec.mjs`: pass
  - scoped `git diff --check`: pass
evidence:
  - development/workbench-ui-v1/task-sessions/20260720T165903Z-swu-wui-008/desktop-canvas.png
  - development/workbench-ui-v1/task-sessions/20260720T165903Z-swu-wui-008/mobile-canvas.png
blockers: []
residue:
  - WUI-009 is the next unit for read-only Craft frontier seeding.
  - WUI-010 remains downstream for receipt-linked Inspector evidence.
  - Provider execution, browser control, workers, VSCodium hosting, and the separate SCW human usefulness review remain deferred by the Work Pack.
reroute: SWU-WUI-009
handoff_note: The existing Canvas placement is now witnessed as the primary desktop column and reachable mobile view. Surface and revision identity remain visible; revision A stays interactive when revision B navigation fails; the existing Refresh canvas action then loads revision B. No Canvas server behavior changed.
```

## Result

PASS. The primary Canvas witness proves the retained artifact is visible in the
central desktop workspace and the mobile Canvas view. The browser exposes the
surface and revision identity, keeps the prior iframe and its interaction alive
when a later revision cannot load, and recovers to the later revision through
the existing refresh action.

## Context And Gates

- Context pack: [CONTEXT-PACK.md](CONTEXT-PACK.md), 8 selected sources, 8/8
  obligations covered, strict coverage pass.
- Dependencies: [SWU-WUI-003 PASS](../20260720T155936Z-swu-wui-003/TASK-SESSION-RESULT.md),
  [SWU-WUI-007 PASS](../20260720T164437Z-swu-wui-007/TASK-SESSION-RESULT.md).
- Runtime: local Node and Playwright Chromium; no runtime delegation and no
  subagents.
- Decision gate: n/a; the task contract and existing Canvas retention behavior
  determine the implementation path.
- Fallback search: none.

## Evidence

- The focused desktop/mobile journey publishes revision A, verifies the primary
  Canvas placement, clicks its live artifact, blocks revision B content, and
  confirms revision A remains visible, identified, and interactive.
- The same journey removes the block, uses the existing Refresh canvas command,
  and verifies revision B becomes the current frame.
- Existing Operations navigation proves durable selection, interaction, failed
  target retention, restart retention, and one visible frame on both viewports.
- Screenshots show central desktop placement and mobile Canvas framing without
  overlap or horizontal overflow.

## Compatibility Corrections

- The existing Operations navigation browser test now selects the mobile Canvas
  tab before interacting with the iframe; its contract and production code are
  unchanged.
- The existing shell geometry helper now ignores hidden zero-sized controls so
  WUI-007's hidden terminal Inspect result button is not reported as clipped.

## Synchronization

- `SWU-WUI-008`: completed with this receipt.
- `TASK-WUI-004`: remains in progress for the independent Craft Seed and
  Evidence Inspector units.
- `SWU-WUI-009`: ready as the next mutation-capable WUI handle.
- Craft ledger, human view, generated index, Work Pack, README route, and task
  synchronization are updated after this receipt.
- Experiment harness: not applicable; this is product implementation evidence,
  not reusable sigil behavior validation.

## Next Route

Run Task Session on `SWU-WUI-009` to seed composer fields from one read-only
Craft frontier selection without mutating the Craft ledger.
