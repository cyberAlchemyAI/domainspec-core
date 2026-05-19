---
module: cyberalchemy-agentic-system
slice: 07-first-working-loop
status: candidate
updatedAt: 2026-05-19
docType: slice-work
---

# Slice 07: First Working Loop

Work layer: [CyberAlchemy Agentic System](../../README.md)
Concepts: [concepts.md](concepts.md)
Navigation: [agentic-system-navigation.md](../../../agentic-system-navigation.md)
First working slice: [agentic-system-first-working-slice.md](../../../agentic-system-first-working-slice.md)

## Purpose

Prove the whole loop once before expanding the corpus.

This slice turns the architecture into a practical adoption path:

```text
source
  -> inventory
  -> ontology
  -> context
  -> execution
  -> telemetry/reflection
```

## Already Done

- The first working slice defines the minimal proof path.
- The inventory pipeline defines commands and source cohorts.
- The ontology entry model defines the thick entry contract.
- The deep dive defines promotion governance and the target ontology pack shape.
- The work layer now gives each slice a self-contained packet.

## Needs To Be Done

- Decide the actual inventory and ontology output roots.
- Install or adapt inventory.
- Create initial inventory entries.
- Create first ontology entries.
- Run ontology-harness.
- Run context-builder on one real task.
- Execute one routed task and record the result.
- Update slice statuses after the loop runs.

## Implementation Slice

1. Use the source cohort from [agentic-system-first-working-slice.md](../../../agentic-system-first-working-slice.md).
2. Install `.arcanum/inventory/`.
3. Add the source manifest.
4. Create the first inventory entries:
   - `concept-schema-data-symmetry`
   - `knowledge-governance-authority-ladder`
   - `method-domainspec-structured-intent`
   - `ontology-branch-operational-ontology`
   - `context-solution-invoke-define-design`
   - `failure-mode-memory-treated-as-authority`
5. Create or validate matching thick ontology entries, including [knowledge-governance-authority-ladder.md](../../../ontology/entries/knowledge-governance-authority-ladder.md).
6. Run ontology-harness for the first map.
7. Run context-builder for:
   - "prepare context to design Operational Ontology schema"
8. Execute one routed task.
9. Record telemetry, reflection, and any promotion candidates.

## Acceptance Checks

- The agent uses less irrelevant context than a whole-repo read.
- The route decision is clearer than before the ontology slice.
- Evidence is cited from inventory or source refs.
- The execution leaves a better next state.
- At least one improvement candidate is recorded.

## Links

| Role                       | Link                                                                                    |
| -------------------------- | --------------------------------------------------------------------------------------- |
| First working slice        | [agentic-system-first-working-slice.md](../../../agentic-system-first-working-slice.md) |
| Inventory slice            | [Slice 01](../01-inventory-foundation/README.md)                                        |
| Entry contract slice       | [Slice 02](../02-ontology-entry-contract/README.md)                                     |
| Promotion slice            | [Slice 03](../03-promotion-governance/README.md)                                        |
| Operational ontology slice | [Slice 04](../04-operational-ontology/README.md)                                        |
| Memory/context slice       | [Slice 05](../05-memory-context/README.md)                                              |
| Execution feedback slice   | [Slice 06](../06-execution-feedback/README.md)                                          |
| Ontology Harness           | [Ontology Harness](../../../../arcanum/spells/ontology-harness/README.md)               |
