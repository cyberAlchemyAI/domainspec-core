---
stage: S9-invoke-plan
capability: invoke
mode: plan
status: pass
updatedAt: 2026-06-08
---

# S9 Invoke Plan

## Plan Objective

Create a Body War-local Inventory interface/indexing feature pack and then
execute a confirmed Inventory pilot slice around Park Track Control.

## Delivery Slices

| Slice     | Outcome                                                                     | Depends On                    | Validation                          |
| --------- | --------------------------------------------------------------------------- | ----------------------------- | ----------------------------------- |
| BW-INV-S0 | Feature pack baseline exists.                                               | refine result                 | files present and linked            |
| BW-INV-S1 | Body War target proposal template exists.                                   | S0                            | template review                     |
| BW-INV-S2 | Body War index/link template examples exist.                                | S0                            | `jq empty`                          |
| BW-INV-S3 | Validator covers source refs, edge vocabulary, and Body War open decisions. | S2                            | validator examples                  |
| BW-INV-S4 | Confirmed Park Track Control pilot slice exists.                            | S1-S3 and target confirmation | cards/index/retrieval/coverage pass |
| BW-INV-S5 | Lookup/status/explain examples prove usefulness.                            | S4                            | retrieval fixture review            |
| BW-INV-S6 | Readiness and next-route handoff synced.                                    | S5                            | readiness review                    |

## Task Board

| Task            | Goal                                                                                                                     | Gate                                   |
| --------------- | ------------------------------------------------------------------------------------------------------------------------ | -------------------------------------- |
| TASK-BW-INV-001 | Create Body War Inventory feature pack baseline: `SPEC.md`, `ARCHITECTURE.md`, `IMPLEMENTATION-PLAN.md`, `WORK-PACK.md`. | ready                                  |
| TASK-BW-INV-002 | Add target proposal and chat-view templates for Body War.                                                                | ready-after-001                        |
| TASK-BW-INV-003 | Add Body War selector/link/index example templates.                                                                      | ready-after-001                        |
| TASK-BW-INV-004 | Add validator checks or fixtures for Body War source refs, links, and gaps.                                              | blocked-by-003                         |
| TASK-BW-INV-005 | Confirm and create Park Track Control pilot slice.                                                                       | blocked-by-004-and-target-confirmation |
| TASK-BW-INV-006 | Add lookup/status/explain examples.                                                                                      | blocked-by-005                         |
| TASK-BW-INV-007 | Sync readiness and next-route handoff.                                                                                   | blocked-by-006                         |

## Recommended First Pilot Target

```text
Park Track Control Inventory Slice
```

Recommended sources:

```text
docs/PROJECT-OVERVIEW.md
docs/PROJECT-DECISIONS.md
docs/features/game-rules/SPEC.md
docs/features/park-track-pilot/DISTILL.md
docs/features/park-track-pilot/implementation-layering.md
docs/research/source-notes/
```

## Validation Strategy

| Check                | Method                                                                             |
| -------------------- | ---------------------------------------------------------------------------------- |
| Dispatch route       | `python3 formulae/dispatch-spec/scripts/validate-dispatch.py REFINE-DISPATCH.json` |
| JSON examples        | `jq empty`                                                                         |
| Source selectors     | validator checks paths and selector shape                                          |
| Link discipline      | validator checks controlled edge vocabulary and non-authority notices              |
| Body War gap queue   | review open decisions from `PROJECT-DECISIONS.md` and `game-rules/SPEC.md`         |
| Retrieval usefulness | query examples answer "what is the first pilot?" and "what decisions block it?"    |

## Non-Goals

- no broad Body War inventory sweep,
- no app/prototype implementation,
- no source doc rewrites,
- no mutation of `.codex`, `.arcanum`, or generated observability state,
- no promotion into definitions or ontology.

## Next Route

Use `task-session` for `TASK-BW-INV-001`.
