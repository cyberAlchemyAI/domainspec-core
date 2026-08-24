# Decision: Implementation dispatch repair shape

## Decision

- ID: `DG-ARC-REPAIR-ROUTE-SHAPE-001`
- Status: direct admissible route
- Selected option: `OPT-EXACT-SWU-GRAPH`
- Admissibility receipt:
  `route-shape-admissibility-receipt.json`
- Source: the user authorized the consolidated Invoke repair; the option
  prefilter owns only the structural representation inside that approved scope.
- Recorded at: `2026-07-30T15:05:49-03:00`

## Question

How should `plan/DISPATCH.json` encode one Task Session per SWU while making
partial-wave advancement structurally impossible?

## Considered Options

| Option | Disposition | Reason |
| --- | --- | --- |
| `OPT-EXACT-SWU-GRAPH` | admissible/direct | Exact SWU receipt edges and wave joins are mechanically inspectable and satisfy `NEW-001`. |
| `OPT-GENERIC-WAVE-LOOP` | rejected | A generic selected-SWU receipt leaves the same early-advance ambiguity. |
| `OPT-PROSE-ONLY-GATE` | rejected | Prose stop conditions cannot repair the dispatch dependency graph. |

## Rationale

The operator profile prefers the smallest reliable, testable, owner-scoped
route and rejects acting on ambiguous or stale assumptions. Exact SWU nodes
reuse the already-authored work-pack dependencies; explicit wave-complete
receipts become the only inputs to later waves. This is a reversible planning
change and grants no execution authority.

The deterministic prefilter returned `routeOutcome=direct`,
`decisionGateRequired=false`, and selected only `OPT-EXACT-SWU-GRAPH`.

## Remaining Gates

- Invoke material-package validation must pass before target mutation.
- Dispatch Spec must validate the repaired JSON.
- Independent exact-byte revalidation remains required before
  `B-DESIGN-001` can close.
- `selectedSWU` remains `none`.
