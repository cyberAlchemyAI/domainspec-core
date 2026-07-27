# Dispatch Technique Trace: Invoke Design Coverage

## Selected techniques

| Technique | Trigger | Applied to | Validation expectation |
| --- | --- | --- | --- |
| `sequence` | schemas and algorithms have strict dependencies | all waves | later steps consume explicit prior receipts |
| `scu_swu_reduction` | high-complexity spell revision | task/SWU boundaries | each SWU owns one independently reviewable behavior |
| `recomposition_proof` | small components must preserve the accepted model | SWU-DVC-008 and VERIFY | live result maps back to DVC-R01..R14 |
| `validation_loop` | selection predicates need causal fixtures | L0-L3 | red-before/green-after, bounded controls, and mutation tests pass |
| `owner_boundary_check` | Invoke authors while Spellcraft mutates | every source step | no step claims promotion or another owner's lifecycle |
| `handle_handoff` | public/private and canonical/generated boundaries | work-pack and dispatch | steps exchange paths and receipts, not copied private prose |
| `residue_ledger` | dirty baselines and absent implementation remain visible | `GAPS.md` and task gates | every gap has owner and repair |
| `execution_receipt_handoff` | each SWU needs governed closeout | all mutation SWUs | exact result and refresh receipts exist |
| `authority_split_gate` | author, extractor, validator, consumer, and promotion differ | schemas, validator, handoff | self-issued and authority-collapse cases reject |
| `artifact_contract_bridge` | prose selection rules require schemas and validators | L1/L2 | validator results bind exact artifact digests |
| `concrete_path_evidence` | dirty worktree and public/private boundary | all task write scopes | no unresolved write globs enter admission |
| `observability_grouping` | Invoke and Distill emit separate non-authority signals | authoring and validation | parent/child run IDs and evidence ceiling are explicit |

## Considered and skipped

| Technique | Reason |
| --- | --- |
| `frame_handoff` | stable artifact handles are sufficient; no copied conversational frame is needed |
| `decision_gate` | no consequential multi-option blocker remains for authoring or the first SWU |
| fan-out/tournament | implementation is sequential and owner-bound; no delegated authoring run is required |

## Full dispatch

A full dispatch is required because the route revises a reusable public spell,
crosses Invoke authoring and Spellcraft lifecycle ownership, carries a
private-to-public boundary, and later synchronizes generated profiles.

- Dispatch: `execution.dispatch.json`.
- Validator: `arcanum/formulae/dispatch-spec/scripts/validate-dispatch.py`.
- Result: `dispatch-validation.json`.

