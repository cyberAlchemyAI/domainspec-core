---
module: cyberalchemy-agentic-system
version: current
status: candidate
updatedAt: 2026-05-19
docType: ontology-pack
---

# CyberAlchemy Agentic System Ontology

Navigation: [agentic-system-navigation.md](../agentic-system-navigation.md)
Work layer: [agentic-system/README.md](../agentic-system/README.md)
Entry model: [agentic-system-ontology-entry-model.md](../agentic-system-ontology-entry-model.md)
Promotion governance slice: [Slice 03](../agentic-system/slices/03-promotion-governance/README.md)
Source ledger: [source-ledger.md](source-ledger.md)
Source digests: [source-digests/README.md](source-digests/README.md)

## Purpose

This directory is the candidate ontology pack for the CyberAlchemy agentic system.

It owns thick, agent-usable knowledge entries. Inventory prepares evidence; ontology owns governed meaning; Context Builder selects the task slice.

This ontology pack also carries source digests for important material imported from Arcanum, DomainSpec, and related source areas. Those digests compile the useful content into CyberAlchemy's ontology context so it can evolve here, while preserving provenance to the original files.

## Current Entries

| Entry                                                                                        | Branch               | Status    | Purpose                                                                                                                       |
| -------------------------------------------------------------------------------------------- | -------------------- | --------- | ----------------------------------------------------------------------------------------------------------------------------- |
| [knowledge-governance-authority-ladder.md](entries/knowledge-governance-authority-ladder.md) | knowledge-governance | candidate | Defines the authority ladder that controls how knowledge moves from raw evidence to promoted ontology and downstream updates. |

## Source Digests

| Digest                                                                                                | Source Area | Ontology Use                                                            |
| ----------------------------------------------------------------------------------------------------- | ----------- | ----------------------------------------------------------------------- |
| [arcanum-business-ontology.md](source-digests/arcanum-business-ontology.md)                           | Arcanum     | Branch-aware ontology, authority roles, confidence split.               |
| [arcanum-ontology-vault-harness.md](source-digests/arcanum-ontology-vault-harness.md)                 | Arcanum     | Ontology governance, promotion, branch mapping, context proof.          |
| [necronomicon-knowledge-substrate.md](source-digests/necronomicon-knowledge-substrate.md)             | Arcanum     | Memory, active interaction, side notes, inventory UX, authority ladder. |
| [arcanum-cyberalchemy-method.md](source-digests/arcanum-cyberalchemy-method.md)                       | Arcanum     | Governed synthesis, route before work, trace before promotion.          |
| [domainspec-structured-intent.md](source-digests/domainspec-structured-intent.md)                     | DomainSpec  | Specification-first structured intent, taxonomy, relationship graph.    |
| [domainspec-drift-observability-tuning.md](source-digests/domainspec-drift-observability-tuning.md)   | DomainSpec  | Drift, convergence, observability derivation, signal tuning.            |
| [agent-execution-orchestrator.md](source-digests/agent-execution-orchestrator.md)                     | DomainSpec  | Route artifacts, stage contracts, execution telemetry.                  |
| [arcanum-observed-invocation-reflection.md](source-digests/arcanum-observed-invocation-reflection.md) | Arcanum     | Invocation telemetry, workflow reflection, maintenance routing.         |

## Rule

Entries may be created as candidates before they are promoted, but they must name their evidence, confidence, promotion state, next gate, and contradiction path.

Do not treat a candidate ontology entry as final authority until its promotion state says so.

Source digests are evidence, not final authority. They can support entries, context packs, and promotion reviews, but they do not replace the original source files.
