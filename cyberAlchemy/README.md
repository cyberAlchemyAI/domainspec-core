---
module: cyberalchemy
version: current
status: candidate
updatedAt: 2026-05-19
docType: directory-readme
---

# CyberAlchemy

This directory gathers the CyberAlchemy product, method, and agentic-system knowledge into one navigable workspace.

It contains two kinds of material:

- product and philosophy surfaces, such as the HTML pages and Saturn explanation;
- the emerging agentic-system architecture, ontology, source digests, work slices, and implementation path.

The center of gravity is the CyberAlchemy agentic system: a knowledge and execution stack designed to preserve alignment between intent, execution, and evidence.

## Start Here

| Need                                 | Open                                                                         |
| ------------------------------------ | ---------------------------------------------------------------------------- |
| Read the whole-system article        | [agentic-system-ontology-synthesis.md](agentic-system-ontology-synthesis.md) |
| View the operational ontology HTML   | [operational-ontology-runtime.html](operational-ontology-runtime.html)       |
| Navigate the artifact pack           | [agentic-system-navigation.md](agentic-system-navigation.md)                 |
| Enter the implementation work slices | [agentic-system/README.md](agentic-system/README.md)                         |
| Inspect the ontology pack            | [ontology/README.md](ontology/README.md)                                     |
| See compiled source imports          | [ontology/source-ledger.md](ontology/source-ledger.md)                       |
| Read the deep conceptual reference   | [agentic-system-deep-dive.md](agentic-system-deep-dive.md)                   |

## Core Idea

CyberAlchemy treats software and agent work as a cybernetic system.

The system keeps three things in contact:

```text
intent
  what we meant to build or do

execution
  what agents, code, and systems actually did

evidence
  what tests, telemetry, source files, memory, and reflection show
```

When those layers drift apart, CyberAlchemy should name the drift, route a correction, preserve evidence, and improve the knowledge future agents use.

## Directory Map

| Path                                                                                           | Purpose                                                                                  |
| ---------------------------------------------------------------------------------------------- | ---------------------------------------------------------------------------------------- |
| [agentic-system-ontology-synthesis.md](agentic-system-ontology-synthesis.md)                   | Main article explaining the CyberAlchemy agentic system.                                 |
| [operational-ontology-runtime.html](operational-ontology-runtime.html)                         | Visual HTML explainer for ontology, promotion, axioms, operational guidance, and memory. |
| [agentic-system-navigation.md](agentic-system-navigation.md)                                   | Progressive disclosure navigation for all agentic-system artifacts.                      |
| [agentic-system/](agentic-system/README.md)                                                    | Self-contained work slices. Each slice has work/status and compiled concept deep dives.  |
| [ontology/](ontology/README.md)                                                                | Candidate ontology pack with thick entries and compiled source digests.                  |
| [agentic-system-definition.md](agentic-system-definition.md)                                   | Define baseline: mission, scope, capabilities, concepts, decisions, gaps.                |
| [agentic-system-architecture.md](agentic-system-architecture.md)                               | Discovery-mode architecture and system views.                                            |
| [agentic-system-knowledge-map.md](agentic-system-knowledge-map.md)                             | Repository research map and source references.                                           |
| [agentic-system-inventory-ontology-pipeline.md](agentic-system-inventory-ontology-pipeline.md) | Inventory-to-ontology pipeline, source cohorts, storage model, entry types.              |
| [agentic-system-ontology-entry-model.md](agentic-system-ontology-entry-model.md)               | Thick ontology entry contract.                                                           |
| [agentic-system-first-working-slice.md](agentic-system-first-working-slice.md)                 | Practical first loop from source to inventory to ontology to execution.                  |
| [assets/](assets/README.md)                                                                    | CyberAlchemy visual identity assets: reusable mark, palette, and CSS tokens.             |
| [saturn-research-presentation.md](saturn-research-presentation.md)                             | Saturn convergence-loop explanation.                                                     |
| [main.html](main.html)                                                                         | CyberAlchemy product/philosophy surface.                                                 |
| [necronomicon.html](necronomicon.html)                                                         | Necronomicon product/philosophy surface.                                                 |

## Agentic-System Layers

The current model is:

```text
Saturn
  convergence loop

DomainSpec
  structured intent and specification discipline

Arcanum
  reusable agent capability method

Inventory
  compiled source evidence

Ontology
  governed, agent-usable meaning

Knowledge Governance
  authority ladder, confidence, promotion, contradiction

Bridge And Residue
  traceability and visible translation loss

Operational Ontology
  reusable knowledge about agent operation

Memory
  continuity without silent authority

Context Builder
  task-sized context selection

Execution
  routed agent work

Observability And Reflection
  telemetry, drift, lessons, maintenance
```

## Ontology Pack

The ontology pack lives at [ontology/](ontology/README.md).

It is where CyberAlchemy starts turning scattered material into thick, agent-usable knowledge objects.

Current ontology material includes:

- [knowledge-governance-authority-ladder.md](ontology/entries/knowledge-governance-authority-ladder.md), the candidate ontology entry that owns the authority ladder;
- [source-ledger.md](ontology/source-ledger.md), the ledger of imported source material;
- [source-digests/](ontology/source-digests/README.md), compiled digests of important Arcanum and DomainSpec sources.

The purpose of source digests is to let cross-repository knowledge evolve inside CyberAlchemy's ontology context without losing provenance.

## Work Slices

The work layer lives at [agentic-system/](agentic-system/README.md).

Each slice is self-contained:

- `README.md` describes purpose, current status, implementation steps, acceptance checks, and links;
- `concepts.md` compiles the relevant source content into the slice itself.

The current slices are:

- System Frame;
- Inventory Foundation;
- Ontology Entry Contract;
- Promotion Governance;
- Operational Ontology;
- Memory And Context;
- Execution Feedback;
- First Working Loop.

## Current Status

This is a candidate design and ontology workspace.

The main conceptual shape is in place. The next practical work is to run the first working loop:

```text
source
  -> inventory
  -> ontology
  -> context
  -> execution
  -> telemetry/reflection
```

That loop should prove whether the system can leave future agents with a better knowledge state than the previous run had.
