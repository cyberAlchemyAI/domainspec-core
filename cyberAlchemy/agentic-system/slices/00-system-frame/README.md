---
module: cyberalchemy-agentic-system
slice: 00-system-frame
status: candidate
updatedAt: 2026-05-19
docType: slice-work
---

# Slice 00: System Frame

Work layer: [CyberAlchemy Agentic System](../../README.md)
Concepts: [concepts.md](concepts.md)
Navigation: [agentic-system-navigation.md](../../../agentic-system-navigation.md)
Synthesis: [agentic-system-ontology-synthesis.md](../../../agentic-system-ontology-synthesis.md)
Deep dive: [agentic-system-deep-dive.md](../../../agentic-system-deep-dive.md)

## Purpose

Define the top-level frame of the CyberAlchemy agentic system: Saturn as the convergence loop, DomainSpec as structured intent, Arcanum as reusable capability method, and schema/data symmetry as the governing lens.

This slice gives every later slice its north star.

## Already Done

- The narrative synthesis explains the whole system in approachable language.
- The deep dive gathers Saturn, DomainSpec, Arcanum, inventory, ontology, memory, execution, and feedback in one reference.
- The architecture file defines the schema/evidence split and the pursuit of symmetry.
- The definition file names the mission, ownership boundary, capabilities, and concept model.

## Needs To Be Done

- Convert the top-level concepts into first ontology candidates.
- Reconcile the discovery architecture wording with the newer define baseline.
- Create a clean concept map that shows which lower slices realize each top-level idea.
- Decide whether `Philosophy Ontology` remains its own branch or becomes tagged knowledge inside the agentic-system ontology.

## Implementation Slice

1. Create inventory entries for:
   - `concept-schema-data-symmetry`
   - `method-saturn-convergence-loop`
   - `method-domainspec-structured-intent`
   - `method-arcanum-capability-system`
2. Create ontology candidates for the entries that should guide agents.
3. Add edges from these candidates into the downstream slices:
   - inventory foundation,
   - ontology entry contract,
   - promotion governance,
   - operational ontology,
   - memory and context,
   - execution feedback.
4. Run a context-builder dry run for: "explain the CyberAlchemy agentic system to a new contributor."

## Acceptance Checks

- A new reader can explain Saturn, DomainSpec, and Arcanum without reading the whole repository.
- The schema/data split is described without becoming vague or ornamental.
- Each top-level concept links to at least one source and one downstream implementation slice.
- No claim of implementation readiness is made without a source or a pending-gate note.

## Links

| Role                | Link                                                                                  |
| ------------------- | ------------------------------------------------------------------------------------- |
| System article      | [agentic-system-ontology-synthesis.md](../../../agentic-system-ontology-synthesis.md) |
| Deep reference      | [agentic-system-deep-dive.md](../../../agentic-system-deep-dive.md)                   |
| Definition baseline | [agentic-system-definition.md](../../../agentic-system-definition.md)                 |
| Architecture seed   | [agentic-system-architecture.md](../../../agentic-system-architecture.md)             |
| Saturn source       | [saturn-research-presentation.md](../../../saturn-research-presentation.md)           |
| DomainSpec source   | [DomainSpec README](../../../../implementation/domainspec/README.md)                  |
| Arcanum source      | [Arcanum README](../../../../arcanum/README.md)                                       |
| CyberAlchemy Method | [CYBERALCHEMY-METHOD.md](../../../../arcanum/framework/CYBERALCHEMY-METHOD.md)        |
