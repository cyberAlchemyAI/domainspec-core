---
feature: inventory-interface-indexing
version: current
status: draft
updatedAt: 2026-06-08
docType: spec
owners:
  - body-war
  - inventory
---

# Inventory Interface And Indexing Spec

## Summary

Inventory Interface And Indexing defines how Body War will use the Arcanum
Inventory capability to compile existing TROQAR project knowledge into
source-backed cards, JSON indexes, Markdown coverage, lookup/status views, and
gap queues.

This feature is not the Inventory runtime itself. It is the Body War-local
feature pack that governs how Inventory is applied to this project.

## Source Evidence

| Source                                                                                                  | Used For                                                |
| ------------------------------------------------------------------------------------------------------- | ------------------------------------------------------- |
| `../../PROJECT-OVERVIEW.md`                                                                             | Project identity, source evidence, audience, and scope. |
| `../../PROJECT-DECISIONS.md`                                                                            | Selected decisions and unresolved pilot/game decisions. |
| `../game-rules/SPEC.md`                                                                                 | Game-rule objects, workflows, and open rule decisions.  |
| `../park-track-pilot/DISTILL.md`                                                                        | Smallest coherent pilot candidate.                      |
| `../park-track-pilot/implementation-layering.md`                                                        | Pilot layers and promotion gates.                       |
| `../../../development/refinement-runs/20260608T075521Z-inventory-interface-indexing-body-war/RESULT.md` | Refined Inventory plan and task board.                  |

## Goals

- Give `$inventory` a Body War target contract.
- Confirm bounded source scope before any Inventory mutation.
- Compile the Park Track Control knowledge cluster into source-backed evidence.
- Preserve open decisions as gaps instead of flattening them into claims.
- Support future lookup/status/explain answers without rereading all Body War docs.

## Non-Goals

- No pilot slice creation in this baseline task.
- No broad repository inventorization.
- No app or prototype implementation.
- No edits to game-rules, project decisions, source notes, `.codex`, `.arcanum`,
  or the local DomainSpec bundle.
- No promotion of Inventory links into canonical game rules, definitions, or
  ontology.

## Actors

| Actor                | Need                                                                      |
| -------------------- | ------------------------------------------------------------------------- |
| Operator             | Ask Inventory what Body War knows and approve the target before mutation. |
| Agent                | Retrieve cards, selectors, links, exclusions, and gaps for a task.        |
| Product planner      | See project identity, game-rule decisions, and pilot readiness quickly.   |
| Pilot operator       | Understand what decisions block the Park Track Control pilot.             |
| Inventory maintainer | Prove Inventory interface/indexing behavior on a real project.            |

## Core Objects

| Object                    | Type     | Notes                                                                                |
| ------------------------- | -------- | ------------------------------------------------------------------------------------ |
| Inventory Target Proposal | Artifact | Human-readable confirmation before creating or updating an Inventory slice.          |
| Evidence Card             | Record   | Source-backed JSON card with source refs, tags, links, and optional trace/residue.   |
| Selector Index            | Index    | Maps source selectors to cards and records.                                          |
| Link Index                | Index    | Stores typed read-model relationships between sources, cards, records, and handoffs. |
| Gap/Risk Queue            | Index    | Tracks unresolved pilot/game decisions and next owners.                              |
| Retrieval Fixture         | Artifact | Example lookup result with selected cards, excluded records, gaps, and next route.   |
| Coverage Report           | Markdown | Human explanation of included sources, excluded sources, and omissions.              |

## First Inventory Pilot Candidate

The recommended first Inventory pilot is:

```text
Park Track Control Inventory Slice
```

Recommended source corpus:

```text
docs/PROJECT-OVERVIEW.md
docs/PROJECT-DECISIONS.md
docs/features/game-rules/SPEC.md
docs/features/park-track-pilot/DISTILL.md
docs/features/park-track-pilot/implementation-layering.md
docs/research/source-notes/
```

This pilot is not created by this baseline. It is created later only after a
target confirmation proposal is approved.

## Required Behavior

1. `$inventory` should infer Body War project or Park Track Control targets from
   user prompts.
2. Any mutation must first show a target confirmation proposal.
3. The confirmation proposal must list included sources, excluded sources, write
   path, generated files, and known risks.
4. The first slice must preserve open decisions from `PROJECT-DECISIONS.md`,
   `game-rules/SPEC.md`, and `park-track-pilot/implementation-layering.md`.
5. Generated cards and indexes must cite source selectors.
6. Generated links must use Inventory read-model edge vocabulary and
   non-authority language where needed.
7. Lookup/status/explain views must show selected evidence, excluded nearby
   evidence, unresolved gaps, and next owner.

## Open Decisions To Preserve

| Decision                             | Source                                                                | Why It Matters                                           |
| ------------------------------------ | --------------------------------------------------------------------- | -------------------------------------------------------- |
| Primary conquest metric              | `PROJECT-DECISIONS.md`, `game-rules/SPEC.md`                          | Determines scoring authority before game implementation. |
| Pilot validation city                | `PROJECT-DECISIONS.md`                                                | Determines runner density and manual operating context.  |
| Initial validation channel           | `PROJECT-DECISIONS.md`, `game-rules/SPEC.md`                          | Determines manual/no-code/app path.                      |
| First park and track set             | `PROJECT-DECISIONS.md`, `park-track-pilot/implementation-layering.md` | Required before live runner pilot.                       |
| L0 track boundary description format | `park-track-pilot/implementation-layering.md`                         | Required before recruiting runners.                      |

## Acceptance Criteria

- The feature pack exists and points to source evidence.
- The work-pack marks the baseline task complete.
- Later tasks can derive templates, index examples, validators, and pilot slice
  work from this pack.
- No generated artifact claims source authority over Body War rules.
