# Task Session Result: SWU-WUI-004

```yaml
swu_id: SWU-WUI-004
task_id: TASK-WUI-002
result: pass
capability_ref: task-session
receipt_kind: local-fallback
receipt_artifact: development/workbench-ui-v1/task-sessions/20260720T161007Z-swu-wui-004/TASK-SESSION-RESULT.md
files_touched:
  - public/demo/l0.html
  - tests/l0-workbench-ui.test.mjs
  - tests/e2e/workbench-ui-v1-composer.spec.mjs
  - tests/e2e/l0-approval-desk.spec.mjs
  - tests/e2e/workbench-ui-v1-mobile.spec.mjs
  - development/workbench-ui-v1/task-sessions/20260720T161007Z-swu-wui-004/CONTEXT-PACK.md
  - development/workbench-ui-v1/task-sessions/20260720T161007Z-swu-wui-004/TASK-SESSION-RESULT.md
  - development/workbench-ui-v1/WORK-PACK.md
  - development/workbench-ui-v1/work-pack/tasks/TASK-WUI-002-COMPOSER.md
  - development/workbench-ui-v1/README.md
  - .craft/ledger.yml
  - .craft/index.json
validation:
  - `npm run test:workbench`: pass, 6/6
  - focused Agent task/Dry run Playwright journey: pass, desktop and mobile
  - retained desktop approval and manual bridge journeys: pass, 3/3
  - retained mobile approval, composer, and shell journeys: pass, 3/3
  - scoped `git diff --check`: pass
blockers: []
residue:
  - Pure lifecycle projection, ordered timeline, and legal-action resolution are
    the next W1 units.
  - Provider execution, browser control, workers, VSCodium hosting, and the
    separate SCW human usefulness review remain deferred by the Work Pack.
reroute: SWU-WUI-005
handoff_note: Agent task is now explicit and selected by default; it requires a
  Skill and emits the existing schema-v2 payload. Dry run is explicit, hides
  Skill, and emits the existing legacy no-skill payload. Continue with a pure
  RunView mapper without changing the composer or server contracts.
```

## Result

PASS. The composer now has an explicit Agent task/Dry run segmented control.
Agent task is selected initially and requires Skill; Dry run hides and disables
Skill and never infers its mode from an empty field. The prepare handler branches
on the selected mode, preserving the existing endpoint payload contracts.

## Context And Gates

- Context pack: [CONTEXT-PACK.md](CONTEXT-PACK.md), 8 selected sources, 9/9
  obligations covered, strict coverage pass.
- Dependency: [SWU-WUI-003 PASS](../20260720T155936Z-swu-wui-003/TASK-SESSION-RESULT.md).
- Runtime: local Node and Playwright Chromium; no runtime delegation and no
  subagents.
- Decision gate: n/a; WUI-D1 already selected Agent task as the default and the
  server contract expressed both modes without migration.
- Fallback search: none.

## Payload Evidence

- Agent task with `decision-gate` produced `agent_ref: codex.current-session`,
  `requested_skill: decision-gate`, and `skill.invoke` in requested grants.
- Dry run after a Skill value had been entered produced
  `agent_ref: local.noop-agent`, normalized `requested_skill: null`, and no
  `skill.invoke` grant.
- Missing Skill returned a visible validation error and preserved the entered
  Task value.

## Synchronization

- `SWU-WUI-004`: completed with this receipt.
- Parent `TASK-WUI-002`: in progress; explicit request mode is complete.
- `SWU-WUI-005`: ready and is the only next mutation-capable handle.
- Craft ledger, human view, generated index, Work Pack, and README route are
  updated after this receipt.
- Experiment harness: not applicable; this is product implementation evidence,
  not reusable sigil behavior validation.

## Next Route

Run Task Session on `SWU-WUI-005` to project bridge state into a pure `RunView`
without DOM effects.
