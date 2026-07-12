# Task Session Result: SWU-SCW-007

```yaml
swu_id: SWU-SCW-007
result: pass
capability_ref: task-session
receipt_kind: native-stage
receipt_artifact: development/session-content-workbench-plan/task-sessions/20260712T141822Z-swu-scw-007/TASK-SESSION-RESULT.md
files_touched:
  - tests/fixtures/canvas/presentation.html
  - tests/fixtures/canvas/presentation-v2.html
  - tests/fixtures/canvas/decision.html
  - tests/fixtures/canvas/craft.html
  - tests/session-content-workbench-matrix.test.mjs
  - tests/e2e/session-content-workbench-matrix.spec.mjs
  - package.json
  - development/session-content-workbench-plan/work-pack/evidence/SWU-SCW-007-assets/
validation:
  - npm run test:canvas-matrix (1 passed)
  - npm run test:e2e:canvas-matrix (2 passed, desktop and mobile)
  - npm run test:bridge (66 passed)
  - npm run test:e2e (10 passed, desktop and mobile)
  - visual inspection of six retained screenshots passed
  - git diff --check -- projects/ide-extension (pass)
blockers: []
residue:
  - automated fixtures demonstrate request transport, not Decision Gate or Craft execution
reroute: SWU-SCW-008
handoff_note: Presentation, Decision, and Craft HTML all pass through the same generic publish/content/event/poll loop on desktop and mobile.
```

## Outcome

One browser matrix proves three independently useful standalone HTML forms:

- a keyboard/button presentation that visibly updates to a second complete
  revision without Refresh;
- a Decision Gate whose selected id/value returns exactly through the one-shot
  cursor poll CLI, including stable duplicate poll evidence;
- a Craft queue whose back-to-back task/action requests return through that
  same route after browser reload.

The source contract test confirms there is no Decision- or Craft-specific
server route. Both action surfaces use `ide-extension.canvas.event`, and neither
calls the kernel API directly.

## Visual Evidence

- [Desktop presentation](../work-pack/evidence/SWU-SCW-007-assets/desktop-presentation.png)
- [Desktop Decision Gate](../work-pack/evidence/SWU-SCW-007-assets/desktop-decision.png)
- [Desktop Craft queue](../work-pack/evidence/SWU-SCW-007-assets/desktop-craft.png)
- [Mobile presentation](../work-pack/evidence/SWU-SCW-007-assets/mobile-presentation.png)
- [Mobile Decision Gate](../work-pack/evidence/SWU-SCW-007-assets/mobile-decision.png)
- [Mobile Craft queue](../work-pack/evidence/SWU-SCW-007-assets/mobile-craft.png)
