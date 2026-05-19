---
id: digest.arcanum_business_ontology
sourceArea: arcanum
sourcePath: arcanum/BUSINESS-ONTOLOGY.md
status: candidate-digest
updatedAt: 2026-05-19
branches:
  - knowledge-governance
  - bridge
  - operational
---

# Source Digest: Arcanum Business Ontology

Source: [BUSINESS-ONTOLOGY.md](../../../arcanum/BUSINESS-ONTOLOGY.md)
Ledger: [../source-ledger.md](../source-ledger.md)

## Why This Source Matters

This source gives CyberAlchemy its branch-aware ontology precedent.

It separates ontology into:

- Business Ontology: intent, meaning, policy, value, outcomes, and rules;
- System Ontology: implementation, runtime evidence, technical architecture, code, APIs, infrastructure;
- Bridge Layer: traceability between intent and realization through tests, observability, constraints, and drift reports.

CyberAlchemy should reuse this structure, then extend it with Operational Ontology for agent operation knowledge.

## Compiled Concepts

### Business Ontology

Business Ontology owns pure domain intent.

It answers:

```text
what does the system mean?
who interacts with it?
what value should it provide?
which rules or policies govern it?
```

It should avoid implementation details. Implementation belongs to System Ontology.

### System Ontology

System Ontology owns operational reality.

It describes:

- code;
- services;
- data shape;
- APIs;
- runtime behavior;
- infrastructure;
- metrics;
- tests;
- deployment facts.

### Bridge Layer

Bridge Layer connects intent and realization.

It contains:

- traceability graph;
- tests;
- observability metrics;
- constraints;
- drift reports;
- evidence gaps.

The bridge prevents two failures:

- business claims pretending implementation exists without evidence;
- system artifacts silently redefining business meaning.

### Axioms

Axioms are load-bearing truths. They justify downstream governance.

They should be rare, reviewed, and hard to revise. A slogan is not an axiom. A useful principle becomes an axiom only when it is foundational enough to govern many decisions.

### Constitutions

Constitutions are codified rules or process conventions.

They translate a principle into operational behavior:

```text
axiom explains why
constitution defines how
```

For CyberAlchemy, constitutions could later govern privacy boundaries, promotion gates, ontology entry shape, or capability maintenance rules.

### Premises

Premises are working bets.

They are useful because they allow the system to reason with uncertainty without pretending the uncertainty is gone. A premise can be promoted, revised, split, retired, or contradicted.

### Confidence Split

The source separates:

- evidence confidence: how well reality supports a claim;
- commitment confidence: how strongly the project should rely on the claim.

CyberAlchemy should preserve this split across all ontology promotion.

## CyberAlchemy Adaptation

Business/System/Bridge becomes:

```text
intent branch
  -> realization branch
  -> bridge evidence
  -> drift/residue response
```

Operational Ontology extends this model:

```text
agent operation intent
  -> actual route behavior
  -> telemetry/reflection evidence
  -> operational lesson or capability update
```

## Candidate Ontology Claims

| Claim                                                                        | Branch               | Candidate Entry                        |
| ---------------------------------------------------------------------------- | -------------------- | -------------------------------------- |
| Intent and realization should be separated before being bridged.             | bridge               | `concept-bridge-layer`                 |
| Axioms should be rare load-bearing principles.                               | knowledge-governance | `knowledge-role-axiom`                 |
| Constitutions codify operating rules derived from higher principles.         | knowledge-governance | `knowledge-role-constitution`          |
| Premises are reviewed working bets, not truths.                              | knowledge-governance | `knowledge-role-premise`               |
| Evidence confidence and commitment confidence must remain separate.          | knowledge-governance | `concept-confidence-split`             |
| Operational Ontology should extend branch-aware ontology to agent operation. | operational          | `ontology-branch-operational-ontology` |

## Tensions And Promotion Gaps

- The Business Ontology source focuses on domain/system alignment; CyberAlchemy must adapt it to agent operation without blurring branches.
- Axioms and constitutions should not be created too early.
- Operational rules may need a lower authority level before becoming constitutions.

## Agent Payload

When mapping CyberAlchemy knowledge, ask:

```text
Is this intent, realization, bridge evidence, or operational knowledge?
Does it deserve to be a premise, constitution, axiom, or only a candidate?
What evidence supports it?
What commitment does the system actually need?
```
