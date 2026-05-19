---
module: cyberalchemy-agentic-system
slice: 05-memory-context
status: candidate
updatedAt: 2026-05-19
docType: slice-work
---

# Slice 05: Memory And Context

Work layer: [CyberAlchemy Agentic System](../../README.md)
Concepts: [concepts.md](concepts.md)
Navigation: [agentic-system-navigation.md](../../../agentic-system-navigation.md)
Definition: [agentic-system-definition.md](../../../agentic-system-definition.md)

## Purpose

Define how memory, user workflow patterns, active interaction state, and context solution cards help agents act with continuity without becoming hidden authority.

## Already Done

- The definition file defines Execution Context Memory, Context Solution, Memory Observation, and User Workflow Model.
- The deep dive separates memory from ontology authority.
- Necronomicon already defines active interaction, side notes, memory, routes, gaps, and checkpoints.
- The inventory pipeline defines `memory-pattern` and `context-solution` inventory entry types.

## Needs To Be Done

- Decide privacy classes for user workflow memory.
- Define context solution card schema.
- Create first context solution cards.
- Decide when memory patterns become inventory candidates.
- Decide when memory patterns become ontology candidates.
- Add retrieval proof for context solution cards.

## Implementation Slice

1. Create a context solution schema with:
   - trigger fingerprint,
   - recommended context,
   - route suggestion,
   - evidence selectors,
   - pitfalls,
   - expiry condition.
2. Create first context solutions:
   - `invoke-define-design`
   - `operational-ontology-schema-design`
   - `user-workflow-memory-privacy-decision`
3. Create memory promotion rules:
   - local continuity,
   - repeated pattern,
   - durable project fact,
   - privacy-scoped workflow preference,
   - contradiction.
4. Route privacy boundaries through `decision-gate`.
5. Prove one task can use a context solution without loading the whole corpus.

## Acceptance Checks

- Memory is described as continuity, not authority.
- User workflow patterns have a privacy class before ontology use.
- Context solution cards tell an agent what to load and what to exclude.
- Memory promotion requires inventory or explicit review.
- The system can explain why a memory shortcut was or was not used.

## Links

| Role                     | Link                                                                                                           |
| ------------------------ | -------------------------------------------------------------------------------------------------------------- |
| Definition               | [agentic-system-definition.md](../../../agentic-system-definition.md)                                          |
| Deep dive memory section | [agentic-system-deep-dive.md](../../../agentic-system-deep-dive.md)                                            |
| Inventory pipeline       | [agentic-system-inventory-ontology-pipeline.md](../../../agentic-system-inventory-ontology-pipeline.md)        |
| Necronomicon README      | [Necronomicon README](../../../../arcanum/spells/necronomicon/README.md)                                       |
| Necronomicon Design      | [DESIGN.md](../../../../arcanum/spells/necronomicon/development/DESIGN.md)                                     |
| Knowledge substrate flow | [KNOWLEDGE-SUBSTRATE-FLOW.md](../../../../arcanum/spells/necronomicon/development/KNOWLEDGE-SUBSTRATE-FLOW.md) |
| Context Builder          | [Context Builder](../../../../arcanum/transmutations/context-builder/README.md)                                |
