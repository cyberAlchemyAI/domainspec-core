# TASK-TTP-005M - Lean Boundary Proof Slice

Status: `pending`
Layer: L1 formal-validation lane

## Objective

Encode the fixed-mask/fixed-load formal boundary and prove or stub the first
small router algebra obligations needed for the paper.

## Write Scope

- `research/projects/mars/papers/triton-top2-backward-kernel/formal/TritonTop2/*.lean`
- `research/projects/mars/papers/triton-top2-backward-kernel/formal/FORMAL-VALIDATION-REPORT.md`

## Implementation Detail

1. Define finite index types or finite ranges for token, expert, and feature
   dimensions.
2. Encode algebraic definitions for `Z = X W^T`, `dW = dZ^T X`, and
   `dX_router = dZ W`.
3. Add theorem targets for PO-004, PO-005, and PO-006 from
   `research/triton-top2-backward-kernel/FORMAL-MATH-SPEC.md`.
4. Prove small algebraic identities where feasible.
5. If a target remains too expensive, leave a Lean-shaped stub only if the
   report marks it as `stub`, not `proved`.
6. Update `FORMAL-VALIDATION-REPORT.md` with proven/stubbed/deferred status.

## Smallest Working Units

| SWU ID | Goal | Done Criteria | Verification |
| --- | --- | --- | --- |
| SWU-TTP-005M-A | Encode fixed-boundary definitions. | Lean modules build. | `lake build` |
| SWU-TTP-005M-B | Add first proof/stub targets. | PO-004/PO-005/PO-006 status is explicit. | review report |
| SWU-TTP-005M-C | Integrate paper-facing report. | report has proved/stubbed/deferred table. | `test -f .../FORMAL-VALIDATION-REPORT.md` |

## Validation

```sh
cd research/projects/mars/papers/triton-top2-backward-kernel/formal
lake build
rg -n "proved|stub|deferred|non-theorem" FORMAL-VALIDATION-REPORT.md
```

