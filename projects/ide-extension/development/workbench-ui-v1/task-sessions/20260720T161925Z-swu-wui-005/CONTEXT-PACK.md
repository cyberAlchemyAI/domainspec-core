# Context Pack: SWU-WUI-005

- Task: `SWU-WUI-005` - RunView Projection
- Mode: standard
- Runtime: local Node test runner
- Dependency receipt: [SWU-WUI-004 PASS](../20260720T161007Z-swu-wui-004/TASK-SESSION-RESULT.md)
- Gate verdict: pass; the projected bridge state is available and stable

## Obligation Matrix

| ID | Obligation | Status | Controlling evidence |
| --- | --- | --- | --- |
| A1 | Execute exactly `SWU-WUI-005` after `SWU-WUI-004`. | covered | Work Pack, task contract, dependency receipt |
| A2 | Map raw envelope, approval, claim, result, and receipt state into one pure `RunView`. | covered | task contract, architecture bundle, projector shape |
| A3 | Cover every supported bridge typestate with a truthful label and lifecycle stage. | covered | bridge projector branches, UX content rules |
| A4 | Derive only legal actions for each typestate without claiming browser-side execution. | covered | task contract, architecture decision flow, current action rules |
| A5 | Expose attributable evidence handles for receipts, result IDs, and evidence refs. | covered | task contract, receipt/result projector contract |
| A6 | Keep claimed work distinct from completed/admitted result. | covered | UX plan, spec success criteria, bridge labels |
| A7 | Keep the mapper free of DOM effects and independent of rendering. | covered | task write scope and handoff |
| A8 | Prove the exhaustive fixture matrix and run `npm run test:bridge`. | covered | task validation, package scripts, bridge tests |
| A9 | Do not change the composer, timeline renderer, action controls, kernel authority, provider, browser, worker, or IDE-host scope. | covered | task handoff, Work Pack gates, spec exclusions |

## Selected Context

| Source | Why selected | Selectors / obligations |
| --- | --- | --- |
| `development/workbench-ui-v1/WORK-PACK.md` | authoritative ready unit and lifecycle sequencing | WUI-005 manifest, gates; A1-A9 |
| `development/workbench-ui-v1/work-pack/tasks/TASK-WUI-003-LIFECYCLE.md` | exact projection contract, done criteria, and handoff | SWU-WUI-005 contract; A1-A9 |
| `development/workbench-ui-v1/SPEC.md` | truthful lifecycle and excluded authority boundaries | success criteria, exclusions; A3-A6, A9 |
| `development/workbench-ui-v1/ARCHITECTURE-BUNDLE.md` | UI mapper boundary and kernel ownership | component/dependency views; A2, A4, A7, A9 |
| `src/kernel/projector.mjs` | authoritative raw bridge state and supported event-derived fields | `withBridgeState`, V2 reducers, claims/results; A2-A5 |
| `public/demo/l0.html` | current state-to-label/action behavior to preserve while extracting pure semantics | `statusLabel`, `renderActions`, detail/receipt fields; A3-A6 |
| `tests/manual-session-bridge-contracts.test.mjs` | exact bridge schema/grant and receipt distinctions | bridge typestate contracts; A3-A5, A8 |
| `tests/manual-session-bridge-claim-recovery.test.mjs` | ready, claimed, interrupted, released, and secrecy scenarios | claim lifecycle states; A3-A6, A8 |

## Implementation Assumption

Create `src/ui/run-view.mjs` with a pure `projectRunView(input)` function. The
function accepts the already projected detail pieces (`envelope`, `approval`,
`activeClaim`, `result`, `receipts`, and optional ready target), returns a stable
serializable object, and never imports browser or DOM APIs. The stage is one of
`prepared`, `approved`, `available`, `running`, `interrupted`, `result`, or
`receipt`; legal action IDs are derived from envelope state; evidence contains
only attributable IDs/refs already present in the input. Unknown or missing
state maps to an explicit `unknown` view with no legal actions.

## Execution Constraints

- Preserve the existing bridge state and endpoint contracts.
- Do not rederive authority from files, DOM text, or receipt presence alone.
- Do not label `claimed` as completed; use `running` and keep result absent.
- Do not treat chat output or a result-like field without admission as terminal
  receipt proof.
- Keep legacy dry-run and schema-v2 bridge terminal states distinguishable in
  source metadata while giving them truthful shared lifecycle stages.
- Do not wire the new mapper into rendering until `SWU-WUI-006`.

## Context Builder Result

- Files selected: 8
- Snippets selected: 8 selector-level excerpts
- Obligation coverage: 9/9
- Strict coverage: pass
- Fallback search: none
- Blockers: 0

## Next Actions

1. Add the pure `RunView` module with exhaustive typestate/action/evidence
   projection.
2. Add fixture-matrix unit tests that assert no input mutation and no DOM/API
   dependency.
3. Run the focused mapper tests plus `npm run test:bridge`, then synchronize
   WUI-006 only after pass.
