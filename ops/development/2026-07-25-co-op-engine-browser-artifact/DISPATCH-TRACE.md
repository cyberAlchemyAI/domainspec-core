---
module: co-op-engine-browser-artifact
phase: define
status: pass
updatedAt: 2026-07-25
---

# Define Dispatch Technique Trace

## Full Dispatch

- Route: [execution.dispatch.json](execution.dispatch.json)
- Validation: [dispatch-validation.json](dispatch-validation.json)
- Result: pass, zero flags, zero blocks
- Subagents: none; the research dispatch is already closed and the remaining
  route is sequential with a human decision gate.

## Technique Activation

| Technique | Activation trigger | Affected step or gate | Validation expectation |
| --- | --- | --- | --- |
| `sequence` | Research must feed context, template selection, Define, Distill, and decision in order. | S2–S6 | Every later step consumes an earlier frame, artifact, ledger, or receipt. |
| `validation_loop` | Route and Define scope need deterministic checks before handoff. | S1, S5, G1–G2 | Dispatch passes; Distill returns a bounded verdict. |
| `handle_handoff` | Private research should be referenced, not copied across owners. | S2–S4 | Concrete paths preserve provenance and minimize context duplication. |
| `residue_ledger` | Research leaves real product and owner decisions. | S4–S6, G3–G4 | Every unresolved item remains in `DECISIONS.md` with an owner or next question. |
| `owner_boundary_check` | Invoke cannot approve product policy or public copy. | S3–S6, G3–G4 | Human product approval remains distinct from authored artifacts. |
| `concrete_path_evidence` | Claims and route receipts need durable selectors. | S1–S5 | All load-bearing evidence names exact repository paths. |
| `artifact_contract_bridge` | Define outputs need validation without implying implementation readiness. | S1, S4–S5, G2 | Required artifacts and checks exist; capability ceilings remain explicit. |
| `observability_grouping` | This Define run extends a prior governed research dispatch. | all steps | Events bind parent dispatch, current dispatch, step, and run IDs. |

## Skipped Techniques

- `scu_swu_reduction`: SWUs belong to Invoke Plan, not Define.
- `recomposition_proof`: used inside Distill concept closure, but no
  implementation recomposition is claimed in Define.
- `execution_receipt_handoff`: no mutation-capable execution is admitted.
- `authority_split_gate`: the owner boundary is material, but no public
  canonical capability or registry is being mutated.

