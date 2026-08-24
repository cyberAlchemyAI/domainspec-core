# TASK-CHAIN-RUNTIME

## SWU-OAP-004 — Enforce approved finite epochs

- Primary behavior: decide whether exactly one next Task Session request is
  legal from durable chain evidence.
- Dependencies: OAP-003.
- Write scope: chain schemas, runner, fixture validator/data, task matrix, and
  validation documents only.
- Algorithm:
  1. Validate config and approved epoch.
  2. Exclusively create or re-read the chain record.
  3. Require the current transition to match epoch, frontier, risk, and budget.
  4. Reject repeated cursor, digest mismatch, ambiguous/out-of-order successor,
     or budget exhaustion.
  5. Append a hash-linked transition and expose at most one next selector.
- Done criteria: legacy 8 cases pass; epoch/cursor/risk/budget cases pass;
  invalid cases expose no next request.
- Validation: chain fixture script and schema parse.
- Execution owner: local fallback under candidate fast lane.

## SWU-OAP-005 — Enforce semantic NO_OP and compensation stop

- Primary behavior: close one completed transition only with a joined PASS or a
  schema-valid semantic NO_OP, and stop before owner-routed compensation.
- Dependencies: OAP-004.
- Write scope: same chain runner, fixtures, task matrix, and validation
  documents; sequential shared ownership is explicit.
- Algorithm:
  1. Bind terminal receipt and approved closeout contract.
  2. Compare exact before/after target inventories and require an empty delta.
  3. Bind validator identity/version and Continuation Router verification.
  4. Reject boolean-only NO_OP claims.
  5. For compensation `owner-routed`, stop and expose the owner route without
     executing it; for `none`, require a rationale.
- Done criteria: valid NO_OP continues; every missing or mismatched field
  blocks; compensation never auto-runs.
- Validation: chain fixture script and schema parse.
- Execution owner: local fallback under candidate fast lane.
