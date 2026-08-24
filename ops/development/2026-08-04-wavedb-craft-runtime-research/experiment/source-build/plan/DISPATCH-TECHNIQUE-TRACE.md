# Plan dispatch technique trace

| Technique | Applied to | Concrete effect | Validation |
| --- | --- | --- | --- |
| `sequence` | route and W0 | runner must close before native build; parent refresh last | Dispatch dependency validation |
| `scu_swu_reduction` | two SWUs | separates protocol material from native execution | atomicity and narrow-first-unit checks |
| `recomposition_proof` | SWUs to L0 receipt | runner plus one attempt close the approved Design | Distill recomposition pass |
| `validation_loop` | every stage and SWU | all obligations have commands/oracles | task validations and terminal receipts |
| `owner_boundary_check` | Invoke, Task Session, parent, Craft, publication | prevents authority/lifecycle collapse | boundary evidence and claim scans |
| `artifact_contract_bridge` | Design source/build contracts to task files | exact identities become executable inputs | source anchors and manifests |
| `execution_receipt_handoff` | both Task Sessions and parent refresh | terminal/owner receipt required at each hop | closeout rows |
| `concrete_path_evidence` | material, generated, and receipt scopes | fixes exact roots before mutation | scope audits |
| `residue_ledger` | deferred L1–L3 and package gaps | prevents overclaim/premature promotion | cross-task gap ledger |

Full dispatch: `source-build.dispatch.json`; validator result:
`dispatch-validation.json`. Subagent strategy is none because the route is one
strict serial stream and the user did not authorize delegation.
