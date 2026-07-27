# Execution Pack — Governed State Projection Amended Work

## Sequence

1. W0: `SWU-GSP-001` evidence harness.
2. W1: `SWU-GSP-002` store freshness, then `SWU-GSP-003` current-head
   projection.
3. W2: `SWU-GSP-004` visible-change evidence and `SWU-GSP-005`
   action/annotation/mobile. They may run in either order after GSP-003, but
   each receives its own receipt.
4. W3: `SWU-GSP-006` handoff readiness semantics.
5. W4: `SWU-GSP-007` docs, Craft, and completion closeout.

The coordinator selects and closes one SWU at a time. Parallel mutation is not
needed for this small brownfield surface.

## Gate Rules

- A selected SWU must have every dependency receipt.
- Write scope is fail-closed; discovered changes outside scope require a new
  plan delta.
- Unit or type evidence cannot substitute for browser evidence.
- Diagnostic browser shims cannot become checked-in receipts.
- Completing all implementation SWUs does not authorize release.

## Receipt Shape

```yaml
swu_id: SWU-GSP-001
result: pass | flag | block | interrupted
selected: true
files_touched: []
validation:
  - command: ""
    result: pass | fail
acceptance_evidence: []
blockers: []
residue: []
next_candidate: SWU-GSP-002 | none
```

## Completion Gate

The work-pack is implementation-complete only when GSP-001 through GSP-007
have current passing receipts, the full type/unit/browser suite passes, the
independent-process freshness witness passes, and active documentation carries
the release/human-study boundary.
