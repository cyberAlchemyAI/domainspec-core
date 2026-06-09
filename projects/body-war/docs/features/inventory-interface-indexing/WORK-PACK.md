---
feature: inventory-interface-indexing
version: current
status: active
updatedAt: 2026-06-08
docType: work-pack
owners:
  - body-war
  - inventory
---

# WORK-PACK: Inventory Interface And Indexing

## Control Fields

| Field                 | Value                    | Notes                                                     |
| --------------------- | ------------------------ | --------------------------------------------------------- |
| workPackGateStatus    | pass                     | Baseline created by `TASK-BW-INV-001`.                    |
| complexity            | medium                   | Templates, indexes, validators, and a pilot slice follow. |
| outputMode            | single-file              | Split into task files if detail grows.                    |
| specRef               | `SPEC.md`                | Feature behavior contract.                                |
| architectureRef       | `ARCHITECTURE.md`        | Boundary and component model.                             |
| implementationPlanRef | `IMPLEMENTATION-PLAN.md` | Delivery slices and task order.                           |
| activeLayerWindow     | L0-L3                    | Feature baseline through readiness sync.                  |
| readinessProfile      | blocked-at-decision-gate | `TASK-BW-INV-005` requires target confirmation.           |

## Objective Summary

Use Inventory to compile Body War's Park Track Control project knowledge into
source-backed cards, indexes, retrieval fixtures, coverage notes, and
lookup/status/explain views.

Primary objective:

```text
$inventory -> infer Body War target -> ask confirmation -> inventorize bounded
Park Track Control slice -> update JSON indexes and Markdown coverage
```

## Active Scope

In scope:

- Body War target proposal,
- chat-view templates,
- JSON index/link examples,
- validator fixtures/checks,
- confirmed Park Track Control pilot slice,
- lookup/status/explain examples,
- readiness and handoff sync.

Out of scope:

- broad Body War repository inventorization,
- app/prototype implementation,
- source doc rewrites,
- `.codex`, `.arcanum`, or generated observability mutation except task telemetry,
- ontology/definition promotion.

## Delivery Slices

| Slice ID  | Outcome                                          | Layer | Dependencies | Validation                          |
| --------- | ------------------------------------------------ | ----- | ------------ | ----------------------------------- |
| BW-INV-S0 | Feature pack baseline exists.                    | L0    | none         | file presence and review            |
| BW-INV-S1 | Target proposal and chat-view templates exist.   | L0    | S0           | template review                     |
| BW-INV-S2 | Index/link example templates exist.              | L1    | S0           | JSON parse                          |
| BW-INV-S3 | Validator checks source refs, links, and gaps.   | L2    | S2           | validator/fixture run               |
| BW-INV-S4 | Confirmed Park Track Control pilot slice exists. | L2    | S1-S3        | cards/index/retrieval/coverage pass |
| BW-INV-S5 | Lookup/status/explain examples prove usefulness. | L2    | S4           | retrieval review                    |
| BW-INV-S6 | Readiness and handoff synced.                    | L3    | S5           | readiness review                    |

## Task Status Board

| Task ID         | Goal                                                                        | Layer | Complexity | Gate Status                            | Status      |
| --------------- | --------------------------------------------------------------------------- | ----- | ---------- | -------------------------------------- | ----------- |
| TASK-BW-INV-001 | Create Body War Inventory feature pack baseline.                            | L0    | low        | ready                                  | completed   |
| TASK-BW-INV-002 | Add target proposal and chat-view templates for Body War.                   | L0    | medium     | ready-after-001                        | completed   |
| TASK-BW-INV-003 | Add Body War selector/link/index example templates.                         | L1    | medium     | ready-after-001                        | completed   |
| TASK-BW-INV-004 | Add validator checks or fixtures for Body War source refs, links, and gaps. | L2    | medium     | ready-after-003                        | completed   |
| TASK-BW-INV-005 | Confirm and create Park Track Control pilot slice.                          | L2    | medium     | blocked-by-target-confirmation         | blocked     |
| TASK-BW-INV-006 | Add lookup/status/explain examples.                                         | L2    | medium     | blocked-by-005                         | not-started |
| TASK-BW-INV-007 | Sync readiness and next-route handoff.                                      | L3    | low        | blocked-by-006                         | not-started |

## Smallest Working Units

| SWU ID         | Parent Task     | Goal                                           | Write Scope                                   | Done Criteria                                                     | Validation             | Status    |
| -------------- | --------------- | ---------------------------------------------- | --------------------------------------------- | ----------------------------------------------------------------- | ---------------------- | --------- |
| SWU-BW-INV-001 | TASK-BW-INV-001 | Create baseline feature pack docs.             | `docs/features/inventory-interface-indexing/` | required four files exist                                         | file presence and grep | completed |
| SWU-BW-INV-002 | TASK-BW-INV-002 | Add target confirmation template.              | feature folder templates path                 | template names included/excluded/write path/generated files/risks | review                 | completed |
| SWU-BW-INV-003 | TASK-BW-INV-002 | Add status/explain/lookup chat view templates. | feature folder templates path                 | views show selected evidence, exclusions, gaps, next owner        | review                 | completed |
| SWU-BW-INV-004 | TASK-BW-INV-003 | Add selector/link/index examples.              | feature folder templates path                 | examples parse as JSON                                            | `jq empty`             | completed |
| SWU-BW-INV-005 | TASK-BW-INV-004 | Add validator fixture/check plan.              | feature folder or future script path          | bad refs/edges/missing gaps fail                                  | fixture review         | completed |
| SWU-BW-INV-006 | TASK-BW-INV-005 | Confirm and create pilot slice.                | `pilot/park-track-control/`                   | cards/index/retrieval/coverage exist and pass                     | slice validation       | blocked   |

## Blockers

| Blocker ID                | Scope      | Description                                                                             | Owner              | Next Action                                                   |
| ------------------------- | ---------- | --------------------------------------------------------------------------------------- | ------------------ | ------------------------------------------------------------- |
| B-BW-PILOT-CONFIRMATION   | pilot      | Pilot slice mutation requires target confirmation.                                      | operator/inventory | Ask before `TASK-BW-INV-005`.                                 |
| B-BW-LIVE-PILOT-DECISIONS | live pilot | First park, track boundaries, validation channel, and scoring metric remain unresolved. | body-war/product   | Preserve in gap queue; resolve before live runner experiment. |

## Gate Checks

1. Run exactly one task/SWU at a time.
2. Do not create the pilot slice until target confirmation.
3. Do not inventory the whole Body War repo as the first slice.
4. Do not edit project source docs while generating Inventory read models.
5. Do not promote Inventory links into definitions, ontology, or canonical game
   rules.

## Change Log

| Date       | Change                                                           | Author |
| ---------- | ---------------------------------------------------------------- | ------ |
| 2026-06-08 | Completed `TASK-BW-INV-004`; added validator checks and invalid fixtures, then stopped at the target confirmation blocker for `TASK-BW-INV-005`. | Codex  |
| 2026-06-08 | Completed `TASK-BW-INV-003`; added selector, link, index, gap/risk, card, and retrieval JSON examples. | Codex  |
| 2026-06-08 | Completed `TASK-BW-INV-002`; added target confirmation and chat-view templates. | Codex  |
| 2026-06-08 | Completed `TASK-BW-INV-001`; created baseline feature pack docs. | Codex  |
