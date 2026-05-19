---
module: cyberalchemy-agentic-system
version: current
status: candidate
updatedAt: 2026-05-19
docType: work-layer-index
---

# CyberAlchemy Agentic System Work Layer

Navigation: [agentic-system-navigation.md](../agentic-system-navigation.md)
Synthesis: [agentic-system-ontology-synthesis.md](../agentic-system-ontology-synthesis.md)
Deep dive: [agentic-system-deep-dive.md](../agentic-system-deep-dive.md)
First working slice: [agentic-system-first-working-slice.md](../agentic-system-first-working-slice.md)
Ontology pack: [ontology/README.md](../ontology/README.md)

## Purpose

This directory is the self-contained work layer for the CyberAlchemy agentic system.

The existing top-level files explain the system from different angles. This layer breaks the work into slices. Each slice directory contains:

- `README.md`: what the slice owns, what already exists, what needs to be done, implementation steps, acceptance checks, and source links.
- `concepts.md`: the compiled deep-dive for the slice. It arranges the scattered source content directly inside the slice, with links kept as provenance rather than as the main payload.

The goal is progressive disclosure:

```text
synthesis
  -> work layer
  -> slice README
  -> slice concepts
  -> source links
  -> implementation work
```

## Slice Map

| Slice                                                                     | Owns                                                                                                        | Status                                                                  |
| ------------------------------------------------------------------------- | ----------------------------------------------------------------------------------------------------------- | ----------------------------------------------------------------------- |
| [00 System Frame](slices/00-system-frame/README.md)                       | Saturn, DomainSpec, Arcanum, schema/data symmetry, and the high-level architecture.                         | Conceptual baseline exists; needs reconciliation into ontology entries. |
| [01 Inventory Foundation](slices/01-inventory-foundation/README.md)       | Source cohorts, inventory package, typed inventory entries, source summaries, tags, contradictions.         | Pipeline defined; inventory package not installed for this corpus yet.  |
| [02 Ontology Entry Contract](slices/02-ontology-entry-contract/README.md) | Thick ontology entry shape, branches, evidence, confidence, agent payloads, edges.                          | Entry model exists; concrete entries still need creation.               |
| [03 Promotion Governance](slices/03-promotion-governance/README.md)       | Authority ladder, promotion states, gates, decision records, non-promotion rules.                           | Deep-dive model exists; needs promotion rules file and first records.   |
| [04 Operational Ontology](slices/04-operational-ontology/README.md)       | Agent operation knowledge: lessons, route policies, context solutions, failure modes, maintenance triggers. | Branch defined as candidate; needs first map and entries.               |
| [05 Memory And Context](slices/05-memory-context/README.md)               | Execution memory, user workflow model, context solution cards, privacy boundary.                            | Semantics defined; privacy decision and retrieval cards still pending.  |
| [06 Execution Feedback](slices/06-execution-feedback/README.md)           | Routed execution, telemetry, workflow reflection, sigil maintenance, feedback loops.                        | Source seeds exist; needs integration into operational ontology.        |
| [07 First Working Loop](slices/07-first-working-loop/README.md)           | First proof from source -> inventory -> ontology -> context -> execution -> reflection.                     | Practical slice defined; ready to execute after storage decisions.      |

## How To Use This Layer

Use the slice directories as work packets.

For conceptual writing, open the slice `concepts.md` first.

For implementation, open the slice `README.md` and follow:

```text
Already Done
  -> Needs To Be Done
  -> Implementation Slice
  -> Acceptance Checks
  -> Links
```

For ontology work, start with:

1. [03 Promotion Governance](slices/03-promotion-governance/README.md)
2. [02 Ontology Entry Contract](slices/02-ontology-entry-contract/README.md)
3. [04 Operational Ontology](slices/04-operational-ontology/README.md)
4. [01 Inventory Foundation](slices/01-inventory-foundation/README.md)

For the first execution pass, start with:

1. [07 First Working Loop](slices/07-first-working-loop/README.md)
2. [01 Inventory Foundation](slices/01-inventory-foundation/README.md)
3. [03 Promotion Governance](slices/03-promotion-governance/README.md)

## Directory Contract

Every slice should remain self-contained:

- It must state its purpose.
- It must list what is already done.
- It must list what still needs to be done.
- It must include a concrete implementation slice.
- It must include acceptance checks.
- It must link to the source files that support the slice.
- It must have a conceptual companion file that compiles and arranges the relevant source content, not only points to it.

When a slice becomes implemented, update the slice `README.md` before changing the global synthesis.
