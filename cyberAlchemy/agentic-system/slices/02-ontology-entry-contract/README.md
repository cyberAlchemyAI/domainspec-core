---
module: cyberalchemy-agentic-system
slice: 02-ontology-entry-contract
status: candidate
updatedAt: 2026-05-19
docType: slice-work
---

# Slice 02: Ontology Entry Contract

Work layer: [CyberAlchemy Agentic System](../../README.md)
Concepts: [concepts.md](concepts.md)
Navigation: [agentic-system-navigation.md](../../../agentic-system-navigation.md)
Entry model: [agentic-system-ontology-entry-model.md](../../../agentic-system-ontology-entry-model.md)

## Purpose

Define what an ontology entry must contain before it can guide agents.

This slice prevents ontology from becoming a thin pointer layer. Entries should carry usable meaning, context, evidence, confidence, edges, and maintenance rules.

## Already Done

- The ontology entry model defines thick entries.
- The inventory pipeline defines ontology branches and required maps.
- The deep dive explains ontology as governed meaning.
- The definition file names `OperationalOntology`, `OperationalLesson`, `ContextSolution`, and `PromotionGate`.

## Needs To Be Done

- Create `cyberAlchemy/ontology/README.md`.
- Create `cyberAlchemy/ontology/source-ledger.md`.
- Create the first ontology maps.
- Create the first thick ontology entries.
- Add a linter or checklist for pointer-only entries.
- Decide canonical storage for generated ontology outputs.

## Implementation Slice

1. Create the ontology pack root:
   - `cyberAlchemy/ontology/README.md`
   - `cyberAlchemy/ontology/source-ledger.md`
   - `cyberAlchemy/ontology/agentic-system-ontology-map.md`
   - `cyberAlchemy/ontology/entries/`
2. Create first thick entries:
   - `entries/method-saturn-convergence-loop.md`
   - `entries/method-domainspec-structured-intent.md`
   - `entries/ontology-branch-operational-ontology.md`
   - `entries/failure-mode-memory-treated-as-authority.md`
3. For each entry, include:
   - content,
   - context,
   - agent payload,
   - edges,
   - evidence,
   - confidence,
   - promotion,
   - maintenance.
4. Run ontology-harness review or a manual equivalent before calling any entry promoted.

## Acceptance Checks

- No ontology entry is only a pointer to another file.
- Every entry has a clear branch and type.
- Every entry names when to use it and when not to use it.
- Every entry cites inventory or raw source evidence.
- Every entry has a promotion state and review trigger.

## Links

| Role                        | Link                                                                                                    |
| --------------------------- | ------------------------------------------------------------------------------------------------------- |
| Entry model                 | [agentic-system-ontology-entry-model.md](../../../agentic-system-ontology-entry-model.md)               |
| Deep dive ontology section  | [agentic-system-deep-dive.md](../../../agentic-system-deep-dive.md)                                     |
| Pipeline ontology branches  | [agentic-system-inventory-ontology-pipeline.md](../../../agentic-system-inventory-ontology-pipeline.md) |
| Ontology Vault              | [Ontology Vault](../../../../arcanum/arcana/ontology-vault/README.md)                                   |
| Ontology Harness            | [Ontology Harness](../../../../arcanum/spells/ontology-harness/README.md)                               |
| Business ontology precedent | [BUSINESS-ONTOLOGY.md](../../../../arcanum/BUSINESS-ONTOLOGY.md)                                        |
