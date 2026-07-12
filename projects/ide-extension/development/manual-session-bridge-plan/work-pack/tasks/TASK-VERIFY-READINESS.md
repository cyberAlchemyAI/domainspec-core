# Task Contract: Verify Readiness

## Task Control

| Field | Value |
| --- | --- |
| Task ID | `TASK-VERIFY-READINESS` |
| Objective | Audit completed L0 evidence and synchronize readiness without adding behavior. |
| Layer / slice / wave | L0 / S-004 / W3 closure |
| Dependencies | `SWU-MSB-011` result and all prior SWU receipts. |
| Execution owner | Task Session (`local-fallback`). |

## Smallest Working Unit Exemption

This is a closure-only verification task. It has no implementation SWU because
it may not mutate runtime behavior; its bounded unit is the evidence audit and
status synchronization after all eleven implementation/proof SWUs have returned.
The `VERIFY` task ID and this explicit exemption satisfy the plan contract.

## Verification Contract

**Source handles:** [work-pack](../../WORK-PACK.md), [traceability](../shared/traceability.md),
all task results/receipts, schema/test/browser outputs, and the manual witness report.

**Permitted write scope:** this plan package's status/evidence tables, the
project's relevant readiness/release documentation, and an immutable closure
report. Runtime source, schemas, fixtures, and tests are read-only here.

**Ordered checks:**

1. Confirm one result envelope for each `SWU-MSB-001` through `011` and validate
   dependency order, write scope, and unresolved residue.
2. Run the full project validation suite plus schema, bridge, and Playwright
   commands from a clean temporary state.
3. Resolve both receipt types and every cited artifact; confirm authorization
   makes no execution claim and terminal state has an execution receipt.
4. Recheck all ten obligations and every W0-W3 exit gate against concrete paths.
5. Confirm L1-L3 deferrals remain absent and global workspace caveats are not
   misreported as project-clean evidence.
6. Mark `pass` only when the real witness passed. Otherwise preserve `block`,
   `flag`, or `interrupted` and name the next owning task.

**Acceptance evidence:** closure matrix, validation command results, scoped diff
check, unresolved residue list, and exact readiness claim.

**Expected result:** `pass` means the L0 manual read/preview bridge is ready for
its bounded pilot; it does not claim authentication, mutation safety, automatic
recovery, persistent workers, VSCodium integration, or arbitrary agent execution.

## Synchronization

- Update work-pack/task status from evidence only.
- Preserve failed/manual/interrupted receipts; never rewrite them into success.
