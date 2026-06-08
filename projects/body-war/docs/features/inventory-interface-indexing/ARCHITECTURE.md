---
feature: inventory-interface-indexing
version: current
status: draft
updatedAt: 2026-06-08
docType: architecture
owners:
  - body-war
  - inventory
---

# Inventory Interface And Indexing Architecture

## Architecture Intent

Body War needs a local knowledge compiler for existing TROQAR discovery and
pilot evidence. The architecture keeps source docs immutable, creates
Inventory-generated read models only after confirmation, and exposes project
knowledge through lookup/status/explain surfaces.

## Scope Boundary

Owned behavior:

- Body War target proposal shape.
- Body War Inventory feature pack and execution plan.
- Project-local template/index/validator planning.
- Recommended Park Track Control pilot corpus.

Explicit exclusions:

- No broad repository inventory sweep.
- No pilot slice mutation in the baseline.
- No app or prototype implementation.
- No `.codex`, `.arcanum`, or generated state mutation except observability
  signals for task execution.
- No canonical promotion of Inventory links into game rules or ontology.

## Source Contracts

| Contract ID | Source                                                                                                  | Required | Notes                                                   |
| ----------- | ------------------------------------------------------------------------------------------------------- | -------- | ------------------------------------------------------- |
| SC-001      | `../../PROJECT-OVERVIEW.md`                                                                             | yes      | Body War identity, audience, source policy, and scope.  |
| SC-002      | `../../PROJECT-DECISIONS.md`                                                                            | yes      | Selected and open project/pilot decisions.              |
| SC-003      | `../game-rules/SPEC.md`                                                                                 | yes      | Game-rule objects, workflows, and open decisions.       |
| SC-004      | `../park-track-pilot/DISTILL.md`                                                                        | yes      | Smallest coherent pilot candidate.                      |
| SC-005      | `../park-track-pilot/implementation-layering.md`                                                        | yes      | L0-L3 pilot progression and open decisions.             |
| SC-006      | `../../../development/refinement-runs/20260608T075521Z-inventory-interface-indexing-body-war/RESULT.md` | yes      | Refined plan and task board.                            |
| SC-007      | Arcanum Inventory development pack                                                                      | yes      | Capability source for interface/index/linking behavior. |

## Component View

| Component                  | Owner                          | Responsibility                                                                   |
| -------------------------- | ------------------------------ | -------------------------------------------------------------------------------- |
| Body War Source Docs       | Body War                       | Canonical project knowledge and open decisions.                                  |
| Inventory Interface        | Arcanum Inventory              | Infer target, ask confirmation, expose status/explain/lookup behavior.           |
| Target Proposal            | Inventory for Body War         | Preview included sources, excluded sources, write path, and generated outputs.   |
| Slice Artifacts            | Inventory                      | Cards, index, retrieval, coverage after confirmation.                            |
| JSON Indexes               | Inventory                      | Tags, selectors, links, backlinks, traceability, query patterns, gap/risk queue. |
| Markdown Views             | Inventory                      | Human-readable coverage, status, explain, and lookup projection.                 |
| Decision/Governance Owners | Body War and downstream sigils | Resolve game, pilot, definition, or ontology decisions.                          |

## Process View

```text
User asks about Body War knowledge
  -> Inventory infers target
  -> target proposal asks confirmation
  -> confirmed task creates one bounded slice
  -> cards cite source selectors
  -> indexes connect overview, decisions, rules, pilot distill, layering
  -> lookup/status/explain show evidence, exclusions, gaps, and next owners
```

## Dependency Rules

| Rule                                                      | Applies To           | Enforcement                               |
| --------------------------------------------------------- | -------------------- | ----------------------------------------- |
| Source docs remain read-only during Inventory generation. | All source contracts | Task-session gate.                        |
| Every generated card must cite source refs.               | Evidence cards       | Validator in later task.                  |
| Links are Inventory read models only.                     | Link index           | Non-authority notice and edge vocabulary. |
| Open decisions must become gaps, not claims.              | Gap/risk queue       | Coverage review and validator.            |
| Pilot slice mutation requires target confirmation.        | Pilot tasks          | Decision gate before `TASK-BW-INV-005`.   |

## First Pilot Architecture

Planned later path:

```text
pilot/park-track-control/
  target-confirmation.md
  cards.json
  index.json
  retrieval.json
  COVERAGE.md
  indexes/
```

The baseline feature pack does not create this path.

## Risks

| Risk                                                     | Impact                                       | Mitigation                                                  |
| -------------------------------------------------------- | -------------------------------------------- | ----------------------------------------------------------- |
| Inventory becomes a broad project wiki too early.        | Dilutes MVP and creates noisy records.       | Keep first pilot corpus bounded.                            |
| Generated cards become mistaken for game-rule authority. | Confuses product decisions.                  | Mark as read models and cite sources.                       |
| Open pilot decisions are flattened into claims.          | Hides real blockers.                         | Route unresolved choices into gap/risk queue.               |
| Runtime surfaces become mutation targets.                | Churns `.codex` or `.arcanum` unnecessarily. | Treat local command surfaces as evidence only in this pack. |
