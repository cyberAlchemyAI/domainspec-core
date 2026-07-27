# Execution Pack — Governed State Projection Amended Work

## Sequence

1. W0: `SWU-GSP-001` evidence harness.
2. W1: `SWU-GSP-002` store freshness, then `SWU-GSP-003` current-head
   projection.
3. W2: `SWU-GSP-004` visible-change evidence, then `SWU-GSP-005`
   action/annotation/mobile. The order is serialized for a unique governed
   successor; each receives its own receipt.
4. W3: `SWU-GSP-006` handoff readiness semantics.
5. W4: `SWU-GSP-007` docs, Craft, and completion closeout.

The coordinator selects and closes one SWU at a time. Parallel mutation is not
needed for this small brownfield surface.

The exact captured order is GSP-001, GSP-002, GSP-003, GSP-004, GSP-005,
GSP-006, GSP-007. No other ready unit may be substituted during this chain.

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

The authoritative machine contracts are
`development/invoke-runs/20260727T044346Z-chain-contract-refresh/schemas/task-session-result.schema.json`
and
`development/invoke-runs/20260727T044346Z-chain-contract-refresh/schemas/closeout-owner-receipt.schema.json`.
Every inner session captures fresh exact target baselines before its first
implementation write. Every passing inner session then joins exactly one
Invoke Refresh closeout receipt before the series advances.

## Completion Gate

The work-pack is implementation-complete only when GSP-001 through GSP-007
have current passing receipts, the full type/unit/browser suite passes, the
independent-process freshness witness passes, and active documentation carries
the release/human-study boundary.
