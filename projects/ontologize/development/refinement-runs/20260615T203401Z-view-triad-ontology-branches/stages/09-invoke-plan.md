# Invoke Plan - Branch Materialization Deltas

## Plan Verdict

Status: pass.

The work-pack is ready for a `task-session` run that starts with branch materialization instead of a generic source matrix.

## Plan Deltas

| SWU | Added Requirement |
| --- | --- |
| SWU-VTM-001 | Create Branch Materialization Register and record B1/B2/B3/B4 coverage or blockers. |
| SWU-VTM-002 | System-view names branch-shaped stakes and tensions without verdicts. |
| SWU-VTM-003 | Engineer-view owns branch-boundary decision rows, B3 denominator/lifecycle decisions, and B4 owner-decision routes. |
| SWU-VTM-004 | Ontology-view types branch nodes/edges and validates B4 bridge edges against the edge catalog. |
| SWU-VTM-005 | Validation report covers B1/B2/B3/B4 gates and recomposition trace. |

## Execution Order

```text
TASK-VTM-001
-> TASK-VTM-002
-> TASK-VTM-003
-> TASK-VTM-004
-> TASK-VTM-005
```

No parallel write path is recommended before W0, because the branch register becomes the shared evidence substrate.

## Validation Targets For Next Execution

- Markdown links for the method pack.
- JSON and dispatch validation for this refine run.
- Manual review that product-facing docs are unchanged.
- `rg` check that new branch materialization language is confined to development-pack and refinement-run artifacts unless owner approval is later granted.

## Stage Verdict

Proceed to final synthesis.
