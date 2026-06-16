# TASK-VTM-004 - Ontology-View Typed Model

## Objective

Author the ontology-view pilot for Ontologize, typing branch terms, nodes, edges, and forbidden relationships without redefining system-view shape or engineer-view verdicts.

## Layer And Slice

- Layer: L1.
- Slice: S3.
- SWU: SWU-VTM-004.

## Source Contracts

- `implementation/domainspec/.claude/skills/ontology-view/SKILL.md`
- Engineer-view decision rows from [TASK-VTM-003](TASK-VTM-003-ENGINEER-VIEW.md)
- Ontologize glossary and definitions sources.
- [BRANCH-MATERIALIZATION.md](../../BRANCH-MATERIALIZATION.md)
- `projects/ontologize/DAG-AND-METRICS.md`

## Implementation Detail

Algorithm:

1. Resolve the project-local ontology convention source, if one is in scope.
2. Type concepts from the source matrix as nodes.
3. Type relationships as edges with direction, cardinality, inverse, precedent, and legality status.
4. Attribute each node or edge to B1 meaning, B2 system, B3 run-context, B4 bridge, or explicit not-applicable status.
5. Check B4 bridge edges against the governed edge catalog.
6. Identify forbidden relationship candidates.
7. Apply endpoint-type unconstructibility first where possible.
8. Add named predicate guards for reflexive/self-loop or runtime-only classes.
9. Mark coined/project-local relationships as proposed or blocked, never silently canonical.
10. Build cross-reference map to engineer-view rows.

## Smallest Working Units

### SWU-VTM-004

- Goal: draft `view-triad/ontology-view.md`.
- Dependencies: SWU-VTM-003.
- Write scope: proposed `projects/ontologize/view-triad/ontology-view.md`.
- Done criteria:
  - node table, edge table, forbidden-edge table, and schema graph exist;
  - branch attribution exists for node and edge rows;
  - B4 bridge ledger includes edge, source branch, target branch, evidence, drift/contradiction status, owner-decision route, catalog status, and residue;
  - each verdict-dependent node/edge points to engineer-view;
  - coined or project-local edges carry route/blocker status;
  - raw drift is not modeled as adjudicated contradiction unless engineer-view records the owner-decision route;
  - no term meaning is duplicated in system-view or engineer-view.
- Acceptance evidence: typed node/edge count, branch attribution table, B4 bridge ledger, and forbidden-guard status table.
- Validation surface: manual review against ontology-view output contract.
- Execution owner: local-fallback.
- Handoff note: if no live guard exists, mark PLANNED or blocker; do not claim LIVE.

## Synchronization

Carry typed model into [TASK-VTM-005](TASK-VTM-005-INTEGRATION-VALIDATION.md).
