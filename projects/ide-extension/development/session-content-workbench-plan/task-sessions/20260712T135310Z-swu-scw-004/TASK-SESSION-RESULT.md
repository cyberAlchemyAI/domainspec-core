# Task Session Result: SWU-SCW-004

```yaml
swu_id: SWU-SCW-004
result: pass
capability_ref: task-session
receipt_kind: native-stage
receipt_artifact: development/session-content-workbench-plan/task-sessions/20260712T135310Z-swu-scw-004/TASK-SESSION-RESULT.md
files_touched:
  - public/demo/l0.html
  - tests/l0-workbench-ui.test.mjs
  - tests/e2e/session-content-workbench.spec.mjs
  - development/session-content-workbench-plan/work-pack/evidence/SWU-SCW-004-assets/desktop-canvas.png
  - development/session-content-workbench-plan/work-pack/evidence/SWU-SCW-004-assets/mobile-canvas.png
validation:
  - npm run test:workbench (5 passed)
  - npm run test:canvas-publish (4 passed)
  - npm run test:e2e (6 passed, desktop and mobile)
  - visual inspection of desktop and 390px screenshots passed
blockers: []
residue:
  - automatic updates remain owned by SWU-SCW-005
reroute: SWU-SCW-005
handoff_note: Manual Refresh loads and operates the real 14-slide Craft presentation while preserving Approval Desk behavior.
```

## Outcome

The Approval Desk now includes an unframed, full-width Canvas band. It reports
the current surface identity, loads only a changed complete revision, keeps the
previous iframe until the replacement has loaded, and provides Refresh and
open-content controls without overlaying the embedded HTML.

## Browser Evidence

The focused Playwright journey publishes
`arcanum/development/craft/teaching/craft-causal-class-2026-07-11/CRAFT-CAUSAL-CLASS-PRESENTATION.html`,
loads it through the workbench, and operates its next-slide control. Desktop and
mobile assertions cover overflow, canvas geometry, and control overlap.

- [Desktop canvas](../work-pack/evidence/SWU-SCW-004-assets/desktop-canvas.png)
- [Mobile canvas](../work-pack/evidence/SWU-SCW-004-assets/mobile-canvas.png)

The retained screenshots were visually inspected. Both preserve Approval Desk
use while making the actual presentation the primary lower work area.
