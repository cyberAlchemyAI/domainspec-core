# Context Pack: SWU-WUI-011

- Task: `SWU-WUI-011` - Integrated Product Verdict
- Parent: `TASK-WUI-005` - V1 Validation
- Mode: standard
- Runtime: local Node and Playwright Chromium
- Dependency receipts:
  - [SWU-WUI-008 PASS](../20260720T165903Z-swu-wui-008/TASK-SESSION-RESULT.md)
  - [SWU-WUI-009 PASS](../20260720T170841Z-swu-wui-009/TASK-SESSION-RESULT.md)
  - [SWU-WUI-010 PASS](../20260720T172635Z-swu-wui-010/TASK-SESSION-RESULT.md)
- Gate verdict: machine validation is ready; human usefulness is intentionally
  unresolved and must not be inferred from browser green status

## Obligation Matrix

| ID | Obligation | Status | Controlling evidence |
| --- | --- | --- | --- |
| A1 | Execute exactly `SWU-WUI-011` after all three workspace SWUs pass. | covered | Work Pack, WUI-008/009/010 receipts |
| A2 | Run the scoped Node bridge/L0 regression matrix without mutating product behavior. | covered | `npm run test:bridge`, task write scope |
| A3 | Run the complete Workbench UI desktop/mobile browser matrix. | covered | WUI shell, composer, lifecycle, action, Canvas, Craft, Inspector witnesses |
| A4 | Prove desktop Work/Canvas/Inspector composition has no overlap, clipping, or unreachable controls. | covered | WUI-002 shell receipt and current shell witness |
| A5 | Prove mobile Work/Canvas/Evidence navigation, focus order, fit, and state preservation. | covered | WUI-003 mobile receipt and current mobile witness |
| A6 | Prove a real Agent task journey through prepare, approval, bridge claim/result, Canvas/Craft composition, and receipt inspection. | covered | WUI-004, WUI-008, WUI-009, WUI-010 receipts and matrix |
| A7 | Preserve ready-only opacity, terminal receipt distinction, Craft no-write behavior, and Canvas retention. | covered | bridge, Craft, Canvas, and Inspector witnesses |
| A8 | Record retained desktop/mobile screenshots and exact test counts for the integrated result. | covered | task-session evidence directory and matrix output |
| A9 | Do not alter product behavior while validating the composed V1. | covered | TASK-WUI-005 write scope, scoped diff |
| A10 | Obtain an explicit human usefulness verdict before promoting V1 or closing the Work Pack. | blocked_on_human | TASK-WUI-005 independent acceptance and Decision Gate |
| A11 | Keep provider execution, browser control, worker execution, and VSCodium hosting outside the V1 claim. | covered | Work Pack gates and Craft boundary |

## Selected Context

| Source | Why selected | Selectors / obligations |
| --- | --- | --- |
| `development/workbench-ui-v1/work-pack/tasks/TASK-WUI-005-VALIDATE.md` | authoritative machine/human acceptance contract | split gate, no self-approval; A1-A11 |
| `development/workbench-ui-v1/WORK-PACK.md` | dependency graph, all SWU receipts, and promotion boundary | WUI-011 row and gates; A1-A11 |
| `development/workbench-ui-v1/DECISION-GATE.md` | existing decision-gate format and prior boundary | explicit human decision shape; A10 |
| `development/workbench-ui-v1/UX-PLAN.md` | responsive usefulness and keyboard-order expectations | desktop/mobile composition; A4-A6 |
| `development/workbench-ui-v1/task-sessions/20260720T165903Z-swu-wui-008/TASK-SESSION-RESULT.md` | retained Canvas evidence | Canvas interaction and failed-navigation retention; A6-A7 |
| `development/workbench-ui-v1/task-sessions/20260720T170841Z-swu-wui-009/TASK-SESSION-RESULT.md` | Craft source-selection evidence | no-write source use and responsive Work rail; A6-A7 |
| `development/workbench-ui-v1/task-sessions/20260720T172635Z-swu-wui-010/TASK-SESSION-RESULT.md` | receipt Inspector evidence | same-run attribution and terminal evidence; A6-A7 |
| `tests/e2e/workbench-ui-v1-shell.spec.mjs` | desktop shell geometry witness | A4 |
| `tests/e2e/workbench-ui-v1-mobile.spec.mjs` | mobile navigation/focus/fit witness | A5 |
| `tests/e2e/workbench-ui-v1-composer.spec.mjs`, `workbench-ui-v1-lifecycle.spec.mjs`, and `workbench-ui-v1-actions.spec.mjs` | request-mode, lifecycle, and legal action matrix | A6-A7 |
| `tests/e2e/workbench-ui-v1-canvas.spec.mjs`, `workbench-ui-v1-craft-seed.spec.mjs`, and `workbench-ui-v1-evidence-inspector.spec.mjs` | workspace composition matrix | A6-A8 |
| `tests/e2e/operations-v1-navigation.spec.mjs` and `npm run test:bridge` | retained prior behavior and kernel contract matrix | A2, A6-A7 |

## Implementation Decision

Make no product change. Run the complete scoped machine matrix, preserve the
resulting screenshots and counts, and present the actual workbench to the human
reviewer for one usefulness verdict. A machine pass can establish regression
safety and reachability; it cannot decide whether the composed Workbench UI V1
is useful enough to become the default screen.

## Execution Constraints

- Do not promote V1 from green tests alone.
- Do not rewrite the old Decision Gate as though it were a new WUI-011 verdict
  before the human responds.
- Do not widen scope to provider, worker, browser-control, or VSCodium work.
- Do not change product behavior while validating.
- Preserve all prior receipts and screenshots as independent evidence.
- Separate machine pass, human verdict, and final promotion status.

## Validation Plan

1. Run the complete WUI desktop/mobile browser matrix with mobile-only witnesses
   assigned to the mobile project.
2. Run the scoped Node bridge/L0 suite and confirm the exact count.
3. Run scoped diff and projection checks with no product mutation.
4. Record a machine-only result and retained screenshots.
5. Stop at the human usefulness decision if no test blocker remains.
6. After an explicit verdict, synchronize final promotion or blocked residue.

## Context Builder Result

- Files selected: 12 source groups
- Obligation coverage: 11/11
- Strict coverage: pass
- Fallback search: none
- Blockers: 1 human decision by contract, not yet a machine failure

## Next Actions

1. Execute the machine matrix.
2. Preserve the machine result.
3. Request/record the human usefulness verdict before promotion.
