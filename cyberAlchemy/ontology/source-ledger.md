---
module: cyberalchemy-agentic-system
version: current
status: candidate
updatedAt: 2026-05-19
docType: ontology-source-ledger
---

# CyberAlchemy Ontology Source Ledger

Ontology pack: [README.md](README.md)
Source digests: [source-digests/README.md](source-digests/README.md)
Work layer: [agentic-system/README.md](../agentic-system/README.md)

## Purpose

This ledger tracks source material imported into the CyberAlchemy ontology as compiled source digests.

The goal is not to copy other repositories blindly. The goal is to let their useful concepts evolve inside the CyberAlchemy agentic-system ontology, with provenance preserved.

```text
external source file
  -> ontology source digest
  -> ontology entry evidence
  -> context-builder retrieval
  -> future agent operation
```

## Current Source Digests

| Digest                                                                                                | Source Area | Status           | Ontology Use                                                                           |
| ----------------------------------------------------------------------------------------------------- | ----------- | ---------------- | -------------------------------------------------------------------------------------- |
| [arcanum-business-ontology.md](source-digests/arcanum-business-ontology.md)                           | Arcanum     | candidate digest | Business/System/Bridge ontology, axioms, constitutions, premises, confidence split.    |
| [arcanum-ontology-vault-harness.md](source-digests/arcanum-ontology-vault-harness.md)                 | Arcanum     | candidate digest | Ontology governance, branch mapping, premise review, confidence review, context proof. |
| [necronomicon-knowledge-substrate.md](source-digests/necronomicon-knowledge-substrate.md)             | Arcanum     | candidate digest | Authority ladder, memory boundary, side notes, inventory UX, promotion ownership.      |
| [arcanum-cyberalchemy-method.md](source-digests/arcanum-cyberalchemy-method.md)                       | Arcanum     | candidate digest | Governed synthesis, route before work, trace before promotion, reflection outer loop.  |
| [domainspec-structured-intent.md](source-digests/domainspec-structured-intent.md)                     | DomainSpec  | candidate digest | Specification-first method, taxonomy, relationships, derived tests, verification.      |
| [domainspec-drift-observability-tuning.md](source-digests/domainspec-drift-observability-tuning.md)   | DomainSpec  | candidate digest | Drift/convergence, production observability, signal-based tuning.                      |
| [agent-execution-orchestrator.md](source-digests/agent-execution-orchestrator.md)                     | DomainSpec  | candidate digest | Route templates, stage contracts, execution runs, telemetry envelopes.                 |
| [arcanum-observed-invocation-reflection.md](source-digests/arcanum-observed-invocation-reflection.md) | Arcanum     | candidate digest | Invocation telemetry, signal observer, workflow reflection, maintenance routing.       |

## Digest Rule

Each source digest should:

- compile useful source content into CyberAlchemy ontology language;
- preserve source references;
- state which ontology branches it informs;
- extract candidate ontology claims;
- name contradictions, risks, or promotion gaps;
- avoid pretending the digest is the original source.

## Promotion Rule

A source digest is evidence, not final authority.

It can support ontology entries, but promotion still requires the ladder defined in [knowledge-governance-authority-ladder.md](entries/knowledge-governance-authority-ladder.md).
