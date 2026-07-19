---
taskId: TASK-HALP-VERIFY
docType: work-pack-task
status: ready-after-analysis
layer: L3
slice: S-004
---

# TASK-HALP-VERIFY — Alignment And Closeout Audit

## Objective

Verify spec-to-result alignment, receipt completeness, reproducibility,
license/publication boundaries, and whether exactly one extension is justified.

## Smallest Working Unit Exemption

Allowed because the task ID includes `VERIFY` and owns closure review only. It
does not implement production behavior or mutate experiment semantics.

## Dependencies

All prior tasks and the SWU 014 phase decision.

Related context: [shared execution context](../shared/context.md),
[cross-task gaps](../shared/cross-task-gaps.md), and
[traceability](../shared/traceability.md).

## Review Procedure

1. Check every spec capability against traceability and evidence.
2. Validate protocol, schema, fixture, stack, capacity, run, score, analysis,
   resource, and decision receipt inventories.
3. Re-run deterministic offline and analysis recomputation checks.
4. Confirm failures/exclusions remain visible.
5. Audit claim language against measured checkpoint/stack/workload scope.
6. Audit evidence storage, licenses, and publication redactions.
7. Test non-regression against L0–L2 guarantees.
8. Accept stop/package/repair or one decision-bearing extension route.

## Write Scope

`reports/closeout/`, status/receipt links in `WORK-PACK.md`,
`IMPLEMENTATION-LAYERING.md`, and `PLAN-TRANSPORT.md`. Upstream spec corrections
require explicit patch requests.

## Completion Evidence

- Closeout report with pass/flag/block verdict.
- Exact validation commands and results.
- Receipt inventory and unresolved residue.
- Signed extension/stop decision.

## Validation

Reviewable check plus repository-specific link/schema/test commands captured in
the closeout receipt.

## Execution Owner

Manual auditor or independent verification agent under a bounded dispatch.
