# Plan Dispatch Technique Trace

| Technique | Applied to | Validation expectation | Status |
| --- | --- | --- | --- |
| `sequence` | W0 -> W5 and one machine-bound selected SWU per Task Session | Every executable SWU consumes a fresh literal SWU/step-matched decision; no later wave starts without prior receipts | pass-reconciled-authored |
| `scu_swu_reduction` | task-local SWU contracts | One primary behavior and independent boundary per SWU | pass-authored |
| `recomposition_proof` | SWUs -> layers -> significant scenario -> objective | VERIFY-001 covers every accepted claim | pass-authored |
| `validation_loop` | focused -> security/repo -> live browser | Failures route back to owner SWUs | pass-authored |
| `owner_boundary_check` | Bootstrap/product/Augmentor/owner/memory/decision boundaries | No authority collapse in tasks or closeout | pass-authored |
| `handle_handoff` | proposal/run/child/artifact refs | Opaque refs cross owners; raw private state does not | pass-authored |
| `residue_ledger` | blockers and deferred layers | Each residue has owner and next action | pass-authored |
| `execution_receipt_handoff` | Task Session admission and closeout | Fresh single-use selection decision required before start; exact terminal receipt required before successor selection | pass-reconciled-authored |
| `state_namespace_boundary` | generated/product/extension/archive stores | Every writer and cross-boundary mutation is declared | pass-authored |

The implementation dispatch is deterministically validated separately. The
read-only Distill dispatch is also validated before any confirmation request.
