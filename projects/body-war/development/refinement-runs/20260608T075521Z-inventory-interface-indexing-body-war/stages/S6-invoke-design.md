---
stage: S6-invoke-design
capability: invoke
mode: design
status: pass
updatedAt: 2026-06-08
---

# S6 Invoke Redefine / Design

## Design Statement

Body War should host a project-local Inventory feature surface under:

```text
docs/features/inventory-interface-indexing/
```

This surface should govern how Inventory compiles Body War's existing project
knowledge into source-backed cards, indexes, retrieval fixtures, coverage notes,
and gap/decision queues.

## Architecture Shape

```text
User asks about Body War
  -> Inventory infers project/pilot target
  -> confirmation proposal lists sources and exclusions
  -> confirmed slice writes cards/index/retrieval/coverage
  -> indexes link project overview, decisions, game rules, pilot layering
  -> lookup/status/explain views expose selected evidence, gaps, and next owner
```

## Candidate Slice Structure

```text
docs/features/inventory-interface-indexing/
  SPEC.md
  ARCHITECTURE.md
  IMPLEMENTATION-PLAN.md
  WORK-PACK.md
  pilot/
    park-track-control/
      target-confirmation.md
      cards.json
      index.json
      retrieval.json
      COVERAGE.md
      indexes/
```

## Body War Inventory Components

| Component         | Purpose                                                                                               |
| ----------------- | ----------------------------------------------------------------------------------------------------- |
| Target proposal   | Show inferred Body War corpus before mutation.                                                        |
| Evidence cards    | Capture project identity, game rules, park-track candidate, decisions, and gaps.                      |
| Selector index    | Let future agents jump to exact source sections.                                                      |
| Link index        | Connect overview, decisions, rules, distill, layering, and source notes.                              |
| Gap/risk queue    | Preserve open decisions such as first park, scoring metric, validation channel, and track boundaries. |
| Retrieval fixture | Prove lookup such as "what is the L0 pilot?" or "what decisions block the park pilot?"                |
| Coverage report   | Explain included and excluded Body War sources.                                                       |

## Design Boundaries

- Inventory output is a read model.
- Body War source docs remain source evidence.
- DomainSpec feature docs remain project authority.
- Generated Inventory links do not promote definitions or ontology.
- `.codex`, `.arcanum`, and generated observability remain runtime state, not
  planning source of truth.

## Recommended Pilot Corpus

```text
docs/PROJECT-OVERVIEW.md
docs/PROJECT-DECISIONS.md
docs/features/game-rules/SPEC.md
docs/features/park-track-pilot/DISTILL.md
docs/features/park-track-pilot/implementation-layering.md
docs/research/source-notes/
```

## Design Verdict

Pass. This is a project-local feature planning surface plus later pilot slice,
not broad repository ingestion.
