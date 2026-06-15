# Invoke Redesign - Branch Materialization Method Pack

## Redesign Verdict

Status: pass.

The selected route from [05-distill-branch-materialization.md](05-distill-branch-materialization.md) was applied to the method pack: constrain the existing `system-view` / `engineer-view` / `ontology-view` triad with branch materialization evidence, rather than adding a standalone `branch-view`.

## Method Pack Deltas

| Artifact | Delta |
| --- | --- |
| `projects/ontologize/development/view-triad-method/BRANCH-MATERIALIZATION.md` | Added method-local branch coverage law, Branch Materialization Register schema, B3 run-context record, B4 bridge ledger, authority map, and validation gates. |
| `projects/ontologize/development/view-triad-method/README.md` | Added branch register to method spine and source boundary. |
| `projects/ontologize/development/view-triad-method/SPEC.md` | Added branch materialization requirements and success criteria. |
| `projects/ontologize/development/view-triad-method/GLOSSARY.md` | Added local terms for branch materialization, B3, B4, raw drift, and adjudicated contradiction. |
| `projects/ontologize/development/view-triad-method/DESIGN.md` | Added Branch Materialization Register, B3 record, B4 ledger, branch gates, and authority decisions. |
| `projects/ontologize/development/view-triad-method/IMPLEMENTATION-LAYERING.md` | Updated L0-L3 evidence so branch validation is part of promotion decisions. |
| `projects/ontologize/development/view-triad-method/PLAN.md` | Updated delivery slices and implementation specs for branch coverage. |
| `projects/ontologize/development/view-triad-method/WORK-PACK.md` | Updated SWU done criteria, acceptance evidence, and publication gates. |
| `projects/ontologize/development/view-triad-method/EXECUTION-PACK.md` | Updated wave choreography to include branch register, B3 record, and B4 ledger. |
| `projects/ontologize/development/view-triad-method/work-pack/tasks/` | Updated all task contracts with branch-specific evidence requirements. |
| `projects/ontologize/development/view-triad-method/work-pack/waves/` | Updated wave entry/exit gates for branch materialization. |

## Preserved Boundaries

- Product-facing Ontologize docs were not edited.
- `ONTOLOGY-BRANCHES.md` remains the branch definition authority.
- `DAG-AND-METRICS.md` remains the edge catalog and event/metric authority.
- The Branch Materialization Register is run evidence, not canonical branch doctrine.

## Stage Verdict

Proceed to design review.
