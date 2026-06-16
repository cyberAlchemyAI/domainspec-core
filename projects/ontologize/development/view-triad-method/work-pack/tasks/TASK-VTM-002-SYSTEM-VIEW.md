# TASK-VTM-002 - Method Artifact And System-View Pilot Shell

## Objective

Author the view-triad method artifact and the first branch-aware system-view pilot shell for Ontologize.

## Layer And Slice

- Layer: L0/L1.
- Slice: S1.
- SWU: SWU-VTM-002.

## Source Contracts

- `implementation/domainspec/.claude/skills/system-view/SKILL.md`
- Output from [TASK-VTM-001](TASK-VTM-001-METHOD-BOUNDARY.md)
- [BRANCH-MATERIALIZATION.md](../../BRANCH-MATERIALIZATION.md)
- `projects/ontologize/PRODUCT.md`
- `projects/ontologize/SPEC.md`
- `projects/ontologize/DESIGN.md`
- `projects/ontologize/OPTIMIZATION-CHAIN-METHOD.md`

## Implementation Detail

The system-view must name stakeholder shape, branch-shaped tensions, and live stances without deciding them. It may use concrete examples only when they do not reconstruct schemas, state enums, or build status.

## Smallest Working Units

### SWU-VTM-002

- Goal: draft `VIEW-TRIAD-METHOD.md` and `view-triad/system-view.md`.
- Dependencies: SWU-VTM-001.
- Write scope: proposed `projects/ontologize/VIEW-TRIAD-METHOD.md` and `projects/ontologize/view-triad/system-view.md`, or alternate path selected by SWU-VTM-001.
- Done criteria:
  - method artifact states sequence, gates, and relation to optimization chains;
  - system-view shell has objective, surface, layers, stance table, and closing map;
  - system-view materializes B1 meaning, B2 system, B3 run-context, and B4 bridge as stakes/tensions only;
  - B3 denominator and lifecycle stakes are visible as stances or explicit blockers;
  - B4 alignment, drift, contradiction, evidence-gap, realization, observation, or test tensions are visible as stances or explicit blockers;
  - every stance points to a provisional engineer-view row handle;
  - verdicts stated count is 0.
- Acceptance evidence: stance table can be harvested by TASK-VTM-003.
- Validation surface: manual review against the system-view output contract.
- Execution owner: local-fallback.
- Handoff note: if a stance appears already decided, cite the settling source in "what this view does not cover" rather than state a verdict.

## Synchronization

Carry the harvested stance list into [TASK-VTM-003](TASK-VTM-003-ENGINEER-VIEW.md).
