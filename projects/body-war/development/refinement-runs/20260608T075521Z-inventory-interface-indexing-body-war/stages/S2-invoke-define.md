---
stage: S2-invoke-define
capability: invoke
mode: define
status: pass
updatedAt: 2026-06-08
---

# S2 Invoke Define

## Definition

Body War needs a project-local Inventory interface/indexing plan that lets
`$inventory` infer, confirm, inventorize, index, and retrieve project knowledge
from the current TROQAR evidence set without re-reading the whole project.

## Problem Statement

Body War already has useful knowledge distributed across project overview,
initial definitions, project decisions, hypotheses, experiments, source notes,
game rules, park-track pilot distillation, local DomainSpec bundle, and local
Arcanum command/observability surfaces. That knowledge is coherent enough to
plan from, but it is not yet compiled into an Inventory slice/index/read-model
shape.

## Users

| User                 | Need                                                                                |
| -------------------- | ----------------------------------------------------------------------------------- |
| Operator             | Ask what Body War currently knows and get a target confirmation before mutation.    |
| Agent                | Retrieve selected cards, selectors, links, exclusions, and gaps for a bounded task. |
| Product planner      | See game-rule and pilot decisions without opening every source note.                |
| Inventory maintainer | Prove the interface/indexing MVP on a live project target.                          |

## Scope

In scope:

- Body War-local Inventory refine plan,
- recommended first Inventory pilot corpus,
- target proposal shape,
- index/link/read-model planning,
- task-session handoff for implementation.

Out of scope:

- creating the pilot slice now,
- broad Body War repository inventorization,
- editing source docs,
- changing `.codex`, `.arcanum`, generated observability, or DomainSpec bundle files,
- promoting Inventory links to DomainSpec definitions or ontology.

## Definition Verdict

Pass. Body War is a stronger target than the framework repo for a first
real-project Inventory pilot because it has compact but dispersed knowledge and
clear open decisions.
