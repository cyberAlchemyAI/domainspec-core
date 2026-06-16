# TASK-VTM-001 - Method Boundary And Source Matrix

## Objective

Establish the source boundary, Branch Materialization Register, output path, dispatch mode, and mutation boundary for the Ontologize view-triad method.

## Layer And Slice

- Layer: L0.
- Slice: S0.
- SWU: SWU-VTM-001.

## Source Contracts

- [SPEC.md](../../SPEC.md)
- [DESIGN.md](../../DESIGN.md)
- [BRANCH-MATERIALIZATION.md](../../BRANCH-MATERIALIZATION.md)
- [SKILL-ROUTING.md](../../SKILL-ROUTING.md)
- `projects/ontologize/README.md`
- `projects/ontologize/ONTOLOGY-BRANCHES.md`
- `projects/ontologize/DAG-AND-METRICS.md`
- `projects/ontologize/OPTIMIZATION-CHAIN-METHOD.md`
- `implementation/domainspec/.claude/skills/system-view/SKILL.md`
- `implementation/domainspec/.claude/skills/engineer-view/SKILL.md`
- `implementation/domainspec/.claude/skills/ontology-view/SKILL.md`

## Smallest Working Units

### SWU-VTM-001

- Goal: produce the L0 method boundary, source matrix, and Branch Materialization Register.
- Dependencies: none.
- Write scope: `projects/ontologize/development/view-triad-method/`; proposed pilot path only if explicitly approved.
- Done criteria:
  - source matrix lists each source file, selector, role, and consuming view;
  - Branch Materialization Register lists B1/B2/B3/B4 rows with source selector, consuming view authority, status, owner, and residue;
  - B3 run-context candidate records run boundary, denominator, lifecycle state, scope/posture, stage-vs-outcome check, source events, and open decision route, or blocks publication explicitly;
  - B4 bridge candidates record edge, source branch, target branch, evidence, drift/contradiction status, owner-decision route, catalog status, and residue;
  - output path decision is recorded;
  - dispatch mode is recorded;
  - product-facing mutation status is recorded.
- Acceptance evidence: reviewer can run the next task without guessing source scope or branch coverage obligations.
- Validation surface: manual review of links and boundary table.
- Execution owner: local-fallback.
- Handoff note: use `domainspec-decision-gate` if output path or product-doc mutation is contested.

## Synchronization

Update [WORK-PACK.md](../../WORK-PACK.md) gate status after SWU completion.
