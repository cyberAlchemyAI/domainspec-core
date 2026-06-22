# Dispatch Technique Trace

Invoke mode: `plan/full` authoring package.

## Selected Techniques

| Technique | Phase or artifact | Validation expectation |
| --- | --- | --- |
| `sequence` | Research findings feed Define, Design, Plan, Work Pack, and Handoff. | Artifacts cite the same target and boundaries. |
| `scu_swu_reduction` | `tasks/SWU-VW-001.md` | The SWU is the smallest coherent implementation unit. |
| `recomposition_proof` | `IMPLEMENTATION-LAYERING.md` | SWU outputs recompose into the approved router/receipt design. |
| `validation_loop` | `PLAN.md`, `QUALITY-BAR.md`, negative controls. | Every delivery slice has validation evidence. |
| `owner_boundary_check` | Owner lane matrix and non-goals. | Parent route does not absorb lane authority. |
| `handle_handoff` | `RUNTIME-HANDOFF.md` | Handoff uses file handles, not copied source context. |
| `residue_ledger` | `INVOKE-RESULT.md` and `RUNTIME-HANDOFF.md` | Seed/draft/public-safety gaps remain visible. |
| `execution_receipt_handoff` | `OUTPUT-CONTRACT.md` and `WORK-PACK.md` | Expected task-session receipt and validation are named. |
| `concrete_path_evidence` | Research package and inventory entries. | Private source refs stay internal; public package receives abstracted lessons only. |
| `authority_split_gate` | Public/private and promotion boundaries. | Parent receipt cannot promote owner artifacts. |

## Full Dispatch JSON Requirement

This route crosses owner capabilities, protected/private context, public/private
artifact boundaries, and reusable route intent. A full dispatch document is
therefore included as `DISPATCH.json`.

## Skipped Techniques

- `observability_grouping`: skipped for the authoring package because no runtime
  example is executed yet. It becomes required when the public package gets an
  experiment-harness run.
- `memory_loop`: skipped because Inventory artifacts, not memory promotion, are
  the chosen durable read model.
