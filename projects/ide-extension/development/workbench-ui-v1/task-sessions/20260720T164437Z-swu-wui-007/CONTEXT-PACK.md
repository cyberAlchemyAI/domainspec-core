# Context Pack: SWU-WUI-007

- Task: `SWU-WUI-007` - Legal Primary Action
- Parent: `TASK-WUI-003` - Run Lifecycle
- Mode: standard
- Runtime: local Node and Playwright
- Dependency receipts:
  - [SWU-WUI-005 PASS](../20260720T161925Z-swu-wui-005/TASK-SESSION-RESULT.md)
  - [SWU-WUI-006 PASS](../20260720T162753Z-swu-wui-006/TASK-SESSION-RESULT.md)
- Gate verdict: pass; the canonical `RunView` and ordered timeline are available

## Obligation Matrix

| ID | Obligation | Status | Controlling evidence |
| --- | --- | --- | --- |
| A1 | Execute exactly `SWU-WUI-007` after WUI-006. | covered | Work Pack, dependency receipts |
| A2 | Derive command controls only from `RunView.legal_actions`. | covered | RunView contract, task handoff |
| A3 | Expose one truthful primary affordance for every supported typestate. | covered | UX primary interaction rule, action matrix |
| A4 | Keep reject/revoke/unready/release as secondary actions. | covered | UX plan, existing controls |
| A5 | Keep claimed Running state from presenting premature completion or browser-owned interrupt. | covered | bridge contract, claimant ownership note |
| A6 | Provide `Inspect result` for admitted terminal states without creating execution authority. | covered | UX plan, evidence panel |
| A7 | Preserve ready-only secrecy and existing endpoint payloads. | covered | Work Pack gates, bridge tests |
| A8 | Prove the exhaustive action matrix independently of the timeline. | covered | RunView fixtures and new resolver tests |
| A9 | Prove one real browser journey across action transitions on desktop/mobile. | covered | Playwright config, focused action fixture |
| A10 | Do not add provider execution, browser control, worker, IDE-host, or kernel scope. | covered | Work Pack gates, task write scope |

## Selected Context

| Source | Why selected | Selectors / obligations |
| --- | --- | --- |
| `development/workbench-ui-v1/WORK-PACK.md` | authoritative ready unit and sequencing | WUI-007 row, gates; A1-A10 |
| `development/workbench-ui-v1/work-pack/tasks/TASK-WUI-003-LIFECYCLE.md` | exact action resolver contract | WUI-007 objective/write scope/handoff; A1-A10 |
| `development/workbench-ui-v1/UX-PLAN.md` | primary/secondary interaction rule | one primary action, inspect result, secondary destructive actions; A3-A6 |
| `development/workbench-ui-v1/ARCHITECTURE-BUNDLE.md` | state transition language and host boundary | Approve, Make available, Running, admitted result; A2, A5, A7, A10 |
| `src/ui/run-view.mjs` | canonical typestate and legal command IDs | legal actions and evidence; A2-A6 |
| `public/demo/l0.html` | existing controls, handlers, mobile view routing | `renderActions`, action handlers, evidence view; A2-A6, A9 |
| `src/server.mjs` | existing action endpoint contracts | approve, ready, unready, release; A4, A7 |
| `tests/workbench-ui-v1-run-view.test.mjs` | exhaustive legal-action source matrix | state/action expectations; A2, A5, A8 |
| `tests/e2e/manual-session-bridge.spec.mjs` | real approve/ready/claim/recovery journey | endpoint and mobile behavior; A7, A9 |
| `development/workbench-ui-v1/task-sessions/20260720T162753Z-swu-wui-006/TASK-SESSION-RESULT.md` | ordered timeline dependency | no timeline regression; A1, A9 |

## Action Matrix

| RunView typestate | Primary affordance | Browser commands | Secondary actions | Ownership note |
| --- | --- | --- | --- | --- |
| awaiting_approval | Approve request | `approve` | `reject` | local operator disposition |
| approved | Make available | `ready` | `reject` | authorization is not execution |
| ready_for_poll | Available to poll | none | `unready`, `reject` | any interested session may poll |
| claimed | Running | none | none | claimant owns `interrupt`; browser only observes |
| interrupted | Review interruption | none | `release` | operator release returns to approved |
| passed/flagged/blocked/failed/completed | Inspect result | none | none | terminal result/receipt remains inspectable |

The resolver returns the primary affordance separately from kernel command IDs.
Status/navigation affordances are truthful UI states, not new authority. The
browser only enables a command when its ID is present in `RunView.legal_actions`.

## Implementation Decision

Add a pure `src/ui/run-actions.mjs` resolver. It accepts a `RunView`, returns a
serializable primary affordance, browser-visible secondary command IDs, and
delegated command IDs. The page imports it beside `projectRunView`, uses the
result to enable/disable existing controls, and adds one terminal `Inspect
result` control that routes to the existing Evidence view. It does not add a
new server mutation endpoint or expose the claimant-owned interrupt action as a
browser button.

## Execution Constraints

- Preserve all endpoint payloads, approval receipts, ready-only secrecy, and
  bridge kernel authority.
- Do not infer actions from raw envelope state in the DOM after projection.
- Do not label claimed work completed or present Inspect result before terminal
  admission.
- Keep secondary reject/revoke/unready/release controls reachable and confirmed.
- Keep mobile Work/Evidence routing explicit for action controls.
- Do not change timeline markup except for the action projection needed to keep
  its lifecycle meaning intact.
- Do not add provider execution, browser automation, workers, VSCodium hosting,
  or Craft mutation.

## Validation Plan

1. Add resolver unit fixtures for all ten supported typestates, browser command
   legality, primary affordance, secondary actions, delegated interrupt, and
   terminal Inspect result.
2. Add a desktop/mobile Playwright journey that proves Prepare -> Approve ->
   Make available -> Running action projection without timeline assertions.
3. Run the existing workbench and bridge suites plus scoped diff checks.
4. Synchronize Work Pack, Craft ledger/index, README, and task receipt.

## Context Builder Result

- Files selected: 10
- Obligation coverage: 10/10
- Strict coverage: pass
- Fallback search: none
- Blockers: 0

## Next Actions

1. Add the pure action resolver and its exhaustive unit matrix.
2. Serve the canonical resolver through the existing explicit local UI route.
3. Wire controls and terminal Inspect result to the resolver projection.
4. Validate desktop/mobile behavior and synchronize the next workspace unit.
