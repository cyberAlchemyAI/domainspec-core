# Cross-Task Gaps

| Gap | Class | Owner | Execution treatment | Promotion effect |
| --- | --- | --- | --- | --- |
| GAP-MSBP-001 v1/v2 compatibility | acceptance-critical | SWU-001/002 | Add immutable v1 fixtures and version-aware reducer before endpoints. | Blocks W1. |
| GAP-MSBP-002 unattested identity | accepted limitation | architecture/L2 owner | Label every claim/receipt/UI state; keep loopback/read-only. | Blocks remote/effectful promotion, not L0. |
| GAP-MSBP-003 repeated read-only attempt | accepted limitation | SWU-004/009 | Operator-only release, attempt ledger, no automatic retry. | Mutation layers require new policy. |
| GAP-MSBP-004 live witness availability | environment | SWU-011 manual owner | Start fresh server/state and require active intended session; otherwise BLOCK. | Blocks final L0 witness only. |
| GAP-MSBP-005 unrelated repository diff findings | workspace residue | unrelated owner | Scoped validation only; record global warning; do not edit. | No L0 code effect. |
| GAP-MSBP-006 current default task UX | known defect | SWU-007 | Empty required task with visible label and stable validation. | Blocks W3 browser proof. |
| GAP-MSBP-007 skill package drift | evidence risk | SWU-005/011 | Bind resolved source handle and SHA-256 in result receipt. | Blocks truthful execution receipt. |

## Current Blocker State

- SWU-MSB-001: no blocker.
- W1: blocked until SWU-001 and SWU-002 pass.
- W2: blocked until SWU-005 passes.
- W3: blocked until SWU-008 passes.
- L1-L3: deliberately outside the active plan.
