# TASK-WCP-06: Bounded experiment closeout

## SWU-WCP-008

- Layer/slice/wave: L0, S-WCP-04, W3.
- Dependency: SWU-WCP-007 pass.
- Primary behavior: audit every Work Pack acceptance item and publish one
  candidate-local BOUND/HOLD/KILL verdict to the Craft owner route.
- Inputs: all seven prior Task Session receipts, closeout owner receipts,
  immutable sources, raw evidence bundles.
- Outputs: `experiment/execution/CLOSEOUT.md`, machine closeout receipt, final
  Work Pack status fields.
- Algorithm: validate identities and scopes; map each acceptance row to exact
  evidence; rerun non-destructive validators; scan claim language; preserve all
  HOLD/KILL residue; compute final artifact digests; return one next route.
- Edge cases: missing/flagged receipt, unjoined closeout, fabricated provenance,
  scope escape, unresolved L0 oracle, performance/durability/promotion claim
  inflation. All prevent `COMPLETE`.
- Write scope: exact closeout/session paths and Work Pack closeout fields.
- Done: all acceptance rows pass or the result is honest BLOCK with first
  failure; no open helper/session; next owner route explicit.
- Validation: schema/digest/source audit, boundary/claim scan, Work Pack
  acceptance matrix, helper/session inventory.
- Execution owner: Task Session local.

## Split analysis

Audit and handoff are one SWU because a handoff without a recomposed evidence
verdict is unsafe and an audit without its owner route does not close the finite
experiment.
