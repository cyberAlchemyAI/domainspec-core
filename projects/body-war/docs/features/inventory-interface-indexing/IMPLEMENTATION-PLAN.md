---
feature: inventory-interface-indexing
version: current
status: draft
updatedAt: 2026-06-08
docType: implementation-plan
owners:
  - body-war
  - inventory
---

# Implementation Plan: Inventory Interface And Indexing

## Objective

Create and prove a Body War-local Inventory interface/indexing workflow that can
answer project knowledge questions from source-backed cards and indexes without
re-reading the whole project.

## Active Inputs

| Input                                                                                                   | Role                                         |
| ------------------------------------------------------------------------------------------------------- | -------------------------------------------- |
| `SPEC.md`                                                                                               | Behavior contract.                           |
| `ARCHITECTURE.md`                                                                                       | Component, process, and boundary model.      |
| `../../../development/refinement-runs/20260608T075521Z-inventory-interface-indexing-body-war/RESULT.md` | Refine result and task board.                |
| `../../PROJECT-OVERVIEW.md`                                                                             | Project identity and source evidence.        |
| `../../PROJECT-DECISIONS.md`                                                                            | Open decisions and project-level selections. |
| `../game-rules/SPEC.md`                                                                                 | Game-rules source surface.                   |
| `../park-track-pilot/`                                                                                  | Pilot candidate source surface.              |

## Delivery Slices

| Slice     | Goal                                                      | Dependencies                   | Exit Condition                                                                   |
| --------- | --------------------------------------------------------- | ------------------------------ | -------------------------------------------------------------------------------- |
| BW-INV-S0 | Feature pack baseline exists.                             | refine result                  | `SPEC.md`, `ARCHITECTURE.md`, `IMPLEMENTATION-PLAN.md`, `WORK-PACK.md` exist.    |
| BW-INV-S1 | Target proposal and chat-view templates exist.            | S0                             | Templates describe Body War target confirmation and status/explain/lookup views. |
| BW-INV-S2 | Index/link example templates exist.                       | S0                             | JSON examples parse and preserve read-model authority.                           |
| BW-INV-S3 | Validator checks Body War source refs, links, and gaps.   | S2                             | Validator/fixtures catch bad refs, unknown edges, and missing gaps.              |
| BW-INV-S4 | Park Track Control pilot slice exists after confirmation. | S1-S3 plus target confirmation | Cards, index, retrieval, and coverage pass checks.                               |
| BW-INV-S5 | Lookup/status/explain examples prove usefulness.          | S4                             | Retrieval answers project/pilot questions with selected evidence and gaps.       |
| BW-INV-S6 | Readiness and handoff are synchronized.                   | S5                             | Work-pack/readiness status and next route are updated.                           |

## Task Decomposition

| Task            | Description                                                        | Layer | Depends On           |
| --------------- | ------------------------------------------------------------------ | ----- | -------------------- |
| TASK-BW-INV-001 | Create feature pack baseline.                                      | L0    | none                 |
| TASK-BW-INV-002 | Add target proposal and chat-view templates for Body War.          | L0    | TASK-BW-INV-001      |
| TASK-BW-INV-003 | Add Body War selector/link/index example templates.                | L1    | TASK-BW-INV-001      |
| TASK-BW-INV-004 | Add validator checks or fixtures for source refs, links, and gaps. | L2    | TASK-BW-INV-003      |
| TASK-BW-INV-005 | Confirm and create Park Track Control pilot slice.                 | L2    | TASK-BW-INV-002..004 |
| TASK-BW-INV-006 | Add lookup/status/explain examples.                                | L2    | TASK-BW-INV-005      |
| TASK-BW-INV-007 | Sync readiness and next-route handoff.                             | L3    | TASK-BW-INV-006      |

## Validation Strategy

| Validation        | Method                                                                     |
| ----------------- | -------------------------------------------------------------------------- |
| Baseline files    | `test -f` for required feature-pack files.                                 |
| Source links      | `rg` for required source refs and relative paths.                          |
| JSON examples     | `jq empty` after template/example task.                                    |
| Link discipline   | Validator checks edge vocabulary and non-authority notices.                |
| Gap queue         | Review open decisions from project and pilot docs are preserved.           |
| Lookup usefulness | Retrieval fixtures answer "what is the first pilot?" and "what blocks it?" |

## First Pilot Candidate

The planned pilot slice should use the Park Track Control corpus:

```text
docs/PROJECT-OVERVIEW.md
docs/PROJECT-DECISIONS.md
docs/features/game-rules/SPEC.md
docs/features/park-track-pilot/DISTILL.md
docs/features/park-track-pilot/implementation-layering.md
docs/research/source-notes/
```

Do not create the pilot slice until the confirmation proposal is accepted.

## Non-Goals

- no broad Body War inventory sweep,
- no source doc rewrites,
- no prototype/app code,
- no `.codex` or `.arcanum` runtime mutation,
- no ontology or definition promotion.

## Handoff

Use `WORK-PACK.md` as the current execution manifest. Continue with
`TASK-BW-INV-002`.
