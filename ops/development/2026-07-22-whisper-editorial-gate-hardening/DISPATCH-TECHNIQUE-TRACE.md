# Dispatch Technique Trace

The full dispatch is required because this plan crosses Invoke, Spellcraft, Task Session, Experiment Harness, and observability; creates a reusable execution route; and carries a protected private witness toward generic public changes.

| Technique | Trigger | Applied to | Validation expectation | Status |
| --- | --- | --- | --- | --- |
| `sequence` | Define → design → plan → lifecycle → execution → validation | dispatch steps and waves | each non-first step consumes a prior artifact or receipt | pass |
| `scu_swu_reduction` | high-complexity plan | work-pack tasks and SWUs | one primary behavior and one acceptance boundary per SWU | pass |
| `recomposition_proof` | split implementation | SWUs → WEG-R1..R10 → design | traceability and final validation cover all outcomes | pass |
| `validation_loop` | repeated false-positive readiness | fixture-first W0 and final Experiment Harness | red controls fail causally before promotion | pass |
| `owner_boundary_check` | Invoke targets a spell | Invoke/Spellcraft/Task Session boundaries | Invoke stops at authoring; Spellcraft owns lifecycle | pass |
| `handle_handoff` | private and public sources coexist | artifact path handoffs | private content is referenced by handle, never copied into public fixtures | pass |
| `residue_ledger` | human semantics and candidate promotion remain open | cross-task gaps and task receipts | every unresolved gap has an owner/route | pass |
| `execution_receipt_handoff` | one-SWU execution | Task Session and Experiment Harness returns | receipts contain run, artifacts, validation, residue, reroute | pass |
| `authority_split_gate` | multiple lifecycle/evidence owners | dispatch boundary authority map | unresolved lifecycle/execution/validation/promotion owner blocks | pass |
| `protected_context_flag` | private BTE witness informs public spell | namespace and boundary B1 | public output contains generic contracts only | pass |
| `state_namespace_boundary` | canonical, generated, local, and private roots differ | dispatch state namespaces | writes stay inside the owner namespace | pass |
| `approval_semantics_map` | ambient approvals were over-read | design approval record and gates | editorial approval differs from plan/apply/execution approval | pass |
| `artifact_contract_bridge` | schema/tool/docs must agree | W0–W3 evidence | artifact validation is explicit and does not imply promotion | pass |
| `concrete_path_evidence` | generated/local drift and privacy claims | tasks and receipts | evidence names exact paths, no unresolved glob as completion proof | pass |
| `observability_grouping` | corrections and phase results must recompose | dispatch/run/SWU IDs | signals carry dispatch, step, SWU, run, and invalidation refs | pass |

## Considered and skipped

| Technique | Reason skipped |
| --- | --- |
| `frame_handoff` | Controlled artifact handles are safer than restating private source content. |
| `delegation_boundary` | This plan does not authorize subagents; Task Session is a capability handoff, not delegated sibling-agent work. |
| `memory_promotion_split` | No memory or Inventory promotion is part of execution. Inventory was lookup-only. |
| `tournament` / `dialectic` | The design choice is resolved; competing implementation routes would add cost without a live blocker. |
| `toy_game` | Experiment fixtures provide the required controlled evidence more directly. |

## Full dispatch

- Path: `execution.dispatch.json`
- Validator: `arcanum/formulae/dispatch-spec/scripts/validate-dispatch.py`
- Result: generated in `dispatch-validation.json`; must be `pass` before Spellcraft execution.
