# Dispatch Technique Trace

A full dispatch is required because the plan crosses private DomainSpec tooling,
four sigil lifecycles, two spell lifecycles, generated runtimes, the public
Arcanum submodule, and a reusable one-change-at-a-time route.

| Technique | Trigger | Applied to | Validation expectation | Status |
| --- | --- | --- | --- | --- |
| `sequence` | ten accepted requests have an explicit prevention-leverage order | dispatch steps, waves, task board | every non-first stage consumes a prior closure receipt | pass |
| `scu_swu_reduction` | high-complexity split plan | fifteen SWUs | one behavior and independent acceptance boundary per SWU | pass |
| `recomposition_proof` | owner-local changes must close the accepted audit | traceability and final verification | WFE-R01..R10 each map to evidence and final closure | pass |
| `validation_loop` | current false-ready states need causal proof | every task and final audit | prior bad state fails; positive control remains | pass |
| `owner_boundary_check` | Invoke targets sigils, spells, and private tooling | task owner/lifecycle fields | Invoke stops at authoring; lifecycle owner accepts mutation | pass |
| `handle_handoff` | private/public and canonical/generated sources coexist | task sources and receipts | pass paths/selectors, not copied private prose | pass |
| `residue_ledger` | known validator and runtime gaps remain | shared gaps and closure receipts | every residue has owner and repair route | pass |
| `execution_receipt_handoff` | one SWU at a time | lifecycle close and next-stage input | result/artifacts/validation/blockers/residue/reroute present | pass |
| `authority_split_gate` | lifecycle, execution, validation, evidence, and promotion differ | dispatch boundary map | unresolved owner blocks mutation or promotion | pass |
| `state_namespace_boundary` | private parent, public submodule, generated runtime, and Inventory roots differ | dispatch namespace map | writes stay in declared owner namespace | pass |
| `artifact_contract_bridge` | prose contracts require executable rejection | task fixtures and validators | artifact checks prove only declared axis | pass |
| `concrete_path_evidence` | drift and containment claims are path-sensitive | SWU source anchors and receipts | no completion claim from unresolved globs | pass |
| `observability_grouping` | ten lifecycle runs must recompose | dispatch/task/SWU/run IDs | signals group without changing authority | pass |

## Considered and skipped

| Technique | Reason |
| --- | --- |
| `frame_handoff` | controlled source handles are smaller and safer than copied context |
| `delegation_boundary` | no subagent execution is authorized by this plan; lifecycle capabilities own later work |
| `tournament` / `dialectic` | the review already resolved the design alternatives and the verifier accepted the boundary |
| `memory_promotion_split` | no memory or Inventory promotion is in scope |
| `toy_game` | task-local negative fixtures are more direct evidence |

## Full dispatch

- Path: `execution.dispatch.json`
- Validator: `arcanum/formulae/dispatch-spec/scripts/validate-dispatch.py`
- Required result: `pass` before the first lifecycle handoff.
