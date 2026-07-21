# Context Pack: SWU-WUI-009

- Task: `SWU-WUI-009` - Craft Seed
- Parent: `TASK-WUI-004` - Canvas, Craft, And Evidence
- Mode: standard
- Runtime: local Node and Playwright Chromium
- Dependency receipts:
  - [SWU-WUI-004 PASS](../20260720T161007Z-swu-wui-004/TASK-SESSION-RESULT.md)
  - [SWU-WUI-008 PASS](../20260720T165903Z-swu-wui-008/TASK-SESSION-RESULT.md)
- Gate verdict: pass; the read-only Craft frontier and prepare schema already exist

## Obligation Matrix

| ID | Obligation | Status | Controlling evidence |
| --- | --- | --- | --- |
| A1 | Execute exactly `SWU-WUI-009` after the completed Canvas boundary. | covered | Work Pack, WUI-008 receipt |
| A2 | Keep `/api/craft/frontier` read-only and use its verified projection. | covered | server route and Craft index verification |
| A3 | Make each pending Craft item selectable without introducing a mutation endpoint. | covered | current frontier renderer, task write scope |
| A4 | Seed Task with the selected item summary. | covered | Work Pack, architecture source-list contract |
| A5 | Seed Context with the selected item ID through existing `context_refs`. | covered | prepare schema, envelope projection |
| A6 | Preserve explicit Agent task/Dry run mode behavior and skill validation. | covered | WUI-004 receipt and composer tests |
| A7 | Prove Craft ledger/index bytes are unchanged by selection. | covered | source hash before/after selection |
| A8 | Keep selection reachable and fitted on desktop and mobile Work views. | covered | shell/mobile browser witnesses |
| A9 | Do not prepare, run, publish, sync, or mutate anything as part of selection. | covered | independent acceptance and Work Pack gates |

## Selected Context

| Source | Why selected | Selectors / obligations |
| --- | --- | --- |
| `development/workbench-ui-v1/WORK-PACK.md` | authoritative WUI-009 scope and sequencing | WUI-009 row, no-write gate; A1-A9 |
| `development/workbench-ui-v1/work-pack/tasks/TASK-WUI-004-WORKSPACE.md` | exact seed acceptance contract | task/context fields, read-only Craft, hash oracle; A1-A9 |
| `development/workbench-ui-v1/ARCHITECTURE-BUNDLE.md` | source-list responsibility and kernel boundary | Craft source list seeds task/context; A2-A5, A9 |
| `schemas/prepare-request.schema.json` | existing payload capability | optional `context_refs`; A5-A6 |
| `src/server.mjs` | existing Craft read route | `/api/craft/frontier` only; A2-A3, A9 |
| `public/demo/l0.html` | current frontier renderer and composer payload | Craft rows, Task/Skill fields, prepare handler; A3-A6, A8 |
| `tests/e2e/workbench-ui-v1-composer.spec.mjs` | explicit mode compatibility witness | mode and skill preservation; A6 |
| `tests/l0-workbench-ui.test.mjs` | frontier verification and stable UI contract | verified source and pending IDs; A2, A7 |
| `projects/ide-extension/.craft/ledger.yml` and `.craft/index.json` | no-write source authority | exact ledger hash relation; A7 |

## Implementation Decision

Extend the existing single-page composer with one optional Context input. Render
each pending Craft item as a keyboard-reachable button. Selecting an item stores
its ID in UI state, fills Task with the item summary, fills Context with the item
ID, clears task validation errors, and announces the selection. The existing
prepare request includes `context_refs` only when the Context field is non-empty;
all current Agent task/Dry run defaults and skill rules remain unchanged.

Selection reads the already verified frontier and never writes the ledger,
regenerates the index, prepares an envelope, or creates a new server endpoint.

## Execution Constraints

- Preserve the existing `/api/craft/frontier` response and source hash.
- Do not infer request mode from Craft selection or Context content.
- Do not make Skill optional for Agent task.
- Do not prepare or publish from a Craft selection.
- Keep the existing default context fallback when no Context is supplied.
- Use the selected Craft item ID as a context reference without inventing a file
  path or mutating the source ledger.
- Keep the desktop and mobile Work views usable with the longest pending text.

## Validation Plan

1. Add selectable Craft item rendering and the optional Context composer field.
2. Include non-empty Context as `context_refs` in the existing prepare payload.
3. Add a focused desktop/mobile Playwright witness that reads the source hash,
   selects a pending item, verifies Task/Context/announcement, and confirms the
   source hash is unchanged without preparing a task.
4. Run the existing workbench and composer suites plus the focused witness.
5. Synchronize the WUI-009 receipt, Work Pack, README route, Craft ledger, and
   generated index if validation passes.

## Context Builder Result

- Files selected: 9
- Obligation coverage: 9/9
- Strict coverage: pass
- Fallback search: none
- Blockers: 0

## Next Actions

1. Implement the narrow UI seed projection and optional payload field.
2. Validate desktop/mobile selection and no-write behavior.
3. Synchronize the pass receipt and route to WUI-010.
