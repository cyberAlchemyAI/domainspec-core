# Refresh Dispatch Technique Trace

## Dispatch Decision

- Full Dispatch Spec: not required.
- One bounded read-only helper completed and joined.
- No parallel execution, reusable route, or multi-owner mutation is designed.
- Apply owner: direct-user-approved Invoke Refresh over the exact target
  inventory.

## Techniques

| Technique | Trigger | Effect |
| --- | --- | --- |
| `sequence` | Design and Plan receipts must follow source changes | context → stage → material gate → apply → Design validation → Plan validation |
| `frame_handoff` | user correction enters an existing run | refresh signals preserve the intent and old blockers |
| `residue_ledger` | ontology blockers and runtime blockers differ | status/questions/residue remain data; execution blockers remain ledger rows |
| `owner_boundary_check` | ontology is read-only | only Invoke-authored artifacts enter target inventory |
| `artifact_contract_bridge` | schema fields feed presentation requirements | exact node/relation/lens fields map to reference-brief content |
| `validation_loop` | Design digests and SWU structure change | deterministic Design rerun and five-SWU Plan checks |
| `concrete_path_evidence` | apply approval must equal material scope | 22 normalized target paths |
| `observability_grouping` | Refresh and triggered Distill both emit signals | parent/child lineage is explicit |

## Rejected

- Folding briefs into SWU 002 or 003: rejected as task-shaped.
- Editing ontology schemas or records: rejected; current source fields suffice.
- Tooltip-only `title` attributes: rejected because required meaning must remain
  keyboard/touch/no-JS accessible.
- Full multi-agent dispatch: rejected; one read-only helper and one apply owner
  do not require fan-out.

## Validation

Pass when the material package target/approval/validated scopes match exactly,
the helper is terminal, all old blockers remain, Design reaches a new fixed
point, Plan has five atomic SWUs, and product bytes remain unchanged.
