# Invoke Refresh Proposal — Deterministic Chain Contract

## Result

`APPLY-APPROVED`, bounded to the material package in this run.

## Why This Refresh Exists

The approved implementation tasks are sound, but their dependency metadata
does not provide one unique successor for a bounded until-blocker execution.
The pack also lacks the exact closeout contract now required by Task Session.
Both are predictable control-plane blockers and must be repaired before any
application source is mutated.

## Exact Changes

1. Serialize GSP-001 through GSP-007 in the already-approved table order.
2. Bind every task to one common source-receipt and Invoke Refresh closeout
   contract.
3. Add machine schemas for task receipts, closeout receipts, and chain state.
4. Add a deterministic validator for order, bindings, schemas, and Craft
   indexes.
5. Record the chain amendment and sequencing decision in the scoped Craft
   ledger and human view.

## Boundary

This refresh changes planning/control metadata only. It creates no
implementation receipt, closes no architecture finding, proves no browser
behavior, and authorizes neither release nor publication.
