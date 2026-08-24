# Plan Dispatch Technique Trace

Validated route: `EXECUTION-DISPATCH.json`

| Technique | Concrete effect | Gate/evidence |
| --- | --- | --- |
| sequence | five dependency-ordered SWUs | each non-first step consumes predecessor closeout receipt |
| scu_swu_reduction | five-way split | atomicity table and task contracts |
| recomposition_proof | five receipts form one QRY-003 contract/replay chain | Plan Distill |
| validation_loop | exact command per SWU plus readiness audit | command matrix and audit report |
| concrete_path_evidence | sources, writes, outputs, receipts, closeout targets | task files and audit config |
| execution_receipt_handoff | terminal projection + governance receipt -> Refresh receipt | closeout contract |
| approval_semantics_map | package authoring, material decision, SWU selection, ontology confirmation are distinct | runtime/selection/authority gates |
| authority_split_gate | Invoke, Task Session, Refresh, and Ontology Vault keep separate owners | promotion guardrail |
| residue_ledger | runtime package, relation repair, ontology gate remain explicit | work-pack blockers |
| observability_grouping | step/unit events share one dispatch ID | dispatch observability |

No subagent route is selected or authorized.
