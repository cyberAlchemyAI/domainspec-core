# Task Session Result: SWU-WUI-009

```yaml
swu_id: SWU-WUI-009
task_id: TASK-WUI-004
result: pass
capability_ref: task-session
receipt_kind: local-fallback
receipt_artifact: development/workbench-ui-v1/task-sessions/20260720T170841Z-swu-wui-009/TASK-SESSION-RESULT.md
files_touched:
  - public/demo/l0.html
  - tests/e2e/workbench-ui-v1-craft-seed.spec.mjs
  - development/workbench-ui-v1/task-sessions/20260720T170841Z-swu-wui-009/CONTEXT-PACK.md
  - development/workbench-ui-v1/task-sessions/20260720T170841Z-swu-wui-009/TASK-SESSION-RESULT.md
validation:
  - focused Craft seed Playwright witness: pass, desktop/mobile 2/2
  - existing composer Playwright regression: pass, desktop/mobile 2/2
  - desktop shell Playwright regression: pass, 1/1
  - workbench bridge and L0 regression suite: pass, 68/68
  - `node --check tests/e2e/workbench-ui-v1-craft-seed.spec.mjs`: pass
  - desktop Craft geometry probe: pass, panel/body/list remain within the 300px Work rail
  - scoped `git diff --check`: pass
evidence:
  - development/workbench-ui-v1/task-sessions/20260720T170841Z-swu-wui-009/desktop-craft-seed.png
  - development/workbench-ui-v1/task-sessions/20260720T170841Z-swu-wui-009/mobile-craft-seed.png
blockers: []
residue:
  - WUI-010 is the next unit for receipt-linked Inspector evidence.
  - WUI-011 remains downstream for the composed V1 machine matrix and human usefulness gate.
  - Provider execution, browser control, workers, VSCodium hosting, and the separate SCW human usefulness review remain deferred by the Work Pack.
reroute: SWU-WUI-010
handoff_note: The verified Craft frontier is now a read-only source picker. Selecting a pending item fills Task with its summary and Context with its stable item ID, announces the selection, and leaves the Craft ledger/index bytes, pending projection, event count, proposals, request mode, and Skill behavior unchanged. The existing prepare path emits context_refs only when Context is non-empty. The Craft sidebar stacks its next move and source list so the fixed Work rail remains readable on desktop and mobile.
```

## Result

PASS. The workbench now lets a user choose one pending Craft item as the source
for a new agent task without changing Craft or preparing work. The selected
summary becomes Task, the stable Craft item ID becomes Context, and the existing
Agent task/Dry run composer contract remains explicit.

## Context And Gates

- Context pack: [CONTEXT-PACK.md](CONTEXT-PACK.md), 9 selected sources, 9/9
  obligations covered, strict coverage pass.
- Dependencies: [SWU-WUI-004 PASS](../20260720T161007Z-swu-wui-004/TASK-SESSION-RESULT.md),
  [SWU-WUI-008 PASS](../20260720T165903Z-swu-wui-008/TASK-SESSION-RESULT.md).
- Runtime: local Node and Playwright Chromium; no runtime delegation and no
  subagents.
- Decision gate: n/a; the existing read-only frontier and prepare schema
  determine the implementation path.
- Fallback search: none.

## Evidence

- The focused desktop/mobile journey reads the verified Craft frontier, selects
  the first pending item, verifies Task, Context, selected state, announcement,
  and Agent task/Skill controls, then confirms the source hash, pending list,
  event count, and proposal count are unchanged.
- The desktop geometry witness catches the previously hidden negative-position
  Craft grid. The final layout keeps the Craft panel and its stacked next-move
  and pending-list regions inside the Work rail.
- Existing composer coverage proves explicit Agent task and Dry run behavior
  remains valid after adding Context.
- The 68-test bridge/L0 suite retains the kernel, schema, Craft freshness,
  persistence, approval, claim, result, and receipt contracts.
- Screenshots show readable Craft stacking on desktop and mobile without page
  overflow or clipped controls.

## Compatibility Corrections

- Craft layout tracks now allow the fixed Work rail to size them without a
  negative-position overflow. The next move and pending list stack in the
  sidebar so source summaries remain readable.
- The focused browser witness now checks the Craft panel and both child regions
  against the Work rail bounds, in addition to the existing no-write assertions.

## Synchronization

- `SWU-WUI-009`: completed with this receipt.
- `TASK-WUI-004`: remains in progress for the independent Evidence Inspector
  unit.
- `SWU-WUI-010`: ready as the next mutation-capable WUI handle.
- Craft ledger, human view, generated index, Work Pack, README route, and task
  synchronization are updated after this receipt.
- Experiment harness: not applicable; this is product implementation evidence,
  not reusable sigil behavior validation.

## Next Route

Run Task Session on `SWU-WUI-010` to present receipt-linked run evidence in the
Inspector while preserving attribution and terminal-state boundaries.
