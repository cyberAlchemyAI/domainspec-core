# Context Builder Evidence Baseline

## Target

Refine `projects/ontologize/development/view-triad-method/` so its view surface materializes ontology branches rather than only describing a generic system/engineer/ontology view triad.

## Core Evidence

| Selector | Evidence | Refinement Implication |
| --- | --- | --- |
| `projects/ontologize/ONTOLOGY-BRANCHES.md` §The four branches | Ontologize already defines B1 meaning, B2 system, B3 run-context, and B4 bridge as first-class branches. | The method pack should treat these branches as the material being surfaced by each view. |
| `projects/ontologize/ONTOLOGY-BRANCHES.md` §B3 run-context is load-bearing | Denominators are defined inside run context; stage/outcome distinction is a branch boundary. | The refined method must not let system-view or engineer-view treat B3 as optional background context. |
| `projects/ontologize/ONTOLOGY-BRANCHES.md` §Bridge edge types | B4 edges are `realized_by`, `depends_on`, `observed_by`, `tested_by`, `drifts_from`, `traced_to`; edge catalog lives in `DAG-AND-METRICS.md`. | Ontology-view must materialize bridge-edge legality and guard status, not just term lists. |
| `projects/ontologize/ONTOLOGY-BRANCHES.md` §Cross-branch interaction | Improvement is a branch walk: B2 events -> B3 metrics -> B4 candidate -> B1 update. | The refined method should validate that the triad can trace at least one branch walk. |
| `projects/ontologize/DAG-AND-METRICS.md` §Branch view | Execution DAG maps to B2/B3; ontology DAG maps to B1/B4; denominators live in B3. | System/engineer/ontology views need branch-specific duties for both DAGs. |
| `projects/ontologize/development/view-triad-method/DESIGN.md` §View 2 | Current method structure is source inventory -> system-view -> engineer-view -> ontology-view -> integration. | The sequence is probably still usable if branch materialization constraints are added. |
| `projects/ontologize/development/view-triad-method/PLAN.md` §IDS-VTM-002 | Current procedure says system-view extracts shape, engineer-view writes decision rows, ontology-view types terms and edges. | Procedure needs branch-specific acceptance checks for B1/B2/B3/B4. |

## Constraint Frame

The refined method should keep the sibling division of law:

- `system-view`: branch shape, branch stakes, branch tensions, and stance handles.
- `engineer-view`: branch-boundary verdicts, enforcement authorities, schemas/contracts, and runtime mechanics.
- `ontology-view`: branch node types, bridge edge legality, forbidden branch relations, and guard status.

No product-facing Ontologize docs should be edited during this refine run unless final synthesis explicitly recommends a later owner-approved route.

## Source Handles

- `branch-materialization-source-map`: this context pack.
- `current-method-pack`: `projects/ontologize/development/view-triad-method/`
- `branch-source`: `projects/ontologize/ONTOLOGY-BRANCHES.md`
- `dag-source`: `projects/ontologize/DAG-AND-METRICS.md`

## Stage Verdict

Status: pass.

The local evidence is sufficient for no-research refinement. No external research is needed unless a later stage identifies a named gap in the branch model itself.

