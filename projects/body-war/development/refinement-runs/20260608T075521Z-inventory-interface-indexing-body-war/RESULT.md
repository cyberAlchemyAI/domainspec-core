---
docType: refine-result
runId: 20260608T075521Z-inventory-interface-indexing-body-war
status: pass
updatedAt: 2026-06-08
---

# Refine Result: Inventory Interface/Indexing For Body War

## Target

```text
/home/vrondelli/projects/domainspec-core/projects/body-war
```

## Status

Pass.

The Body War-targeted refine route is complete and ready for the first bounded
Task Session. Pilot slice mutation remains intentionally deferred.

## Final Synthesis

Inventory should be applied to Body War as a project-local knowledge compiler
for TROQAR's existing discovery and pilot evidence.

The first coherent Inventory target is not the entire project. It is the Park
Track Control knowledge cluster:

```text
docs/PROJECT-OVERVIEW.md
docs/PROJECT-DECISIONS.md
docs/features/game-rules/SPEC.md
docs/features/park-track-pilot/DISTILL.md
docs/features/park-track-pilot/implementation-layering.md
docs/research/source-notes/
```

This cluster is rich enough to test Inventory's actual MVP:

- infer a target from a live project question,
- ask a confirmation proposal before mutation,
- write source-backed evidence cards,
- build selector/link/tag/gap indexes,
- expose lookup/status/explain views,
- preserve unresolved product and pilot decisions.

## Recommended Feature Surface

Create:

```text
docs/features/inventory-interface-indexing/
```

This feature surface should own the Body War-local plan for Inventory interface
and indexing. It should not own Arcanum Inventory behavior globally.

## Refined Architecture

```text
Body War user asks about project knowledge
  -> Inventory infers Park Track Control or project slice target
  -> confirmation proposal lists included and excluded sources
  -> confirmed slice writes cards/index/retrieval/coverage
  -> indexes connect overview, decisions, game rules, pilot distill, layering
  -> lookup/status/explain views surface evidence, gaps, and next owners
```

## Refined Plan

| Task            | Goal                                                                                                                     | Gate                                   |
| --------------- | ------------------------------------------------------------------------------------------------------------------------ | -------------------------------------- |
| TASK-BW-INV-001 | Create Body War Inventory feature pack baseline: `SPEC.md`, `ARCHITECTURE.md`, `IMPLEMENTATION-PLAN.md`, `WORK-PACK.md`. | ready                                  |
| TASK-BW-INV-002 | Add target proposal and chat-view templates for Body War.                                                                | ready-after-001                        |
| TASK-BW-INV-003 | Add Body War selector/link/index example templates.                                                                      | ready-after-001                        |
| TASK-BW-INV-004 | Add validator checks or fixtures for Body War source refs, links, and gaps.                                              | blocked-by-003                         |
| TASK-BW-INV-005 | Confirm and create Park Track Control pilot slice.                                                                       | blocked-by-004-and-target-confirmation |
| TASK-BW-INV-006 | Add lookup/status/explain examples.                                                                                      | blocked-by-005                         |
| TASK-BW-INV-007 | Sync readiness and next-route handoff.                                                                                   | blocked-by-006                         |

## Required Gates

1. Do not inventory the whole Body War repository as the first slice.
2. Do not mutate source docs during the Inventory refine or feature baseline.
3. Do not create pilot slice files until target confirmation.
4. Do not treat generated Inventory cards as canonical game rules.
5. Do not mutate `.codex`, `.arcanum`, or generated observability state as part
   of the Inventory plan.

## Stage Evidence

| Stage                              | Verdict | Artifact                                      |
| ---------------------------------- | ------- | --------------------------------------------- |
| Context Builder evidence baseline  | pass    | `stages/S1-context-builder.md`                |
| Invoke Define                      | pass    | `stages/S2-invoke-define.md`                  |
| Interrogation refine-review        | pass    | `stages/S3-interrogation-review.md`           |
| Research decision                  | pass    | `stages/S4-research-decision.md`              |
| Distill                            | pass    | `stages/S5-distill.md`                        |
| Invoke Redefine / Design           | pass    | `stages/S6-invoke-design.md`                  |
| Interrogation refine-design-review | pass    | `stages/S7-design-review.md`                  |
| Distill Repair                     | pass    | `stages/S8-distill-repair.md`                 |
| Invoke Plan                        | pass    | `stages/S9-invoke-plan.md`                    |
| Final Interrogation and Synthesis  | pass    | `stages/S10-final-interrogation-synthesis.md` |

## Recommended Next Route

Run `task-session` for:

```text
TASK-BW-INV-001: Create Body War Inventory feature pack baseline.
```

Expected write scope:

```text
docs/features/inventory-interface-indexing/
```

No pilot slice mutation in that first task.
