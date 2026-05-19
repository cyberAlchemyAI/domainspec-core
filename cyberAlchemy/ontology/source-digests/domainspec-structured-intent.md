---
id: digest.domainspec_structured_intent
sourceArea: domainspec
sourcePaths:
  - implementation/domainspec/README.md
  - implementation/domainspec/TAXONOMY.md
  - implementation/domainspec/RELATIONSHIPS.md
status: candidate-digest
updatedAt: 2026-05-19
branches:
  - philosophy
  - bridge
  - capability
---

# Source Digest: DomainSpec Structured Intent

Sources:

- [DomainSpec README](../../../implementation/domainspec/README.md)
- [TAXONOMY.md](../../../implementation/domainspec/TAXONOMY.md)
- [RELATIONSHIPS.md](../../../implementation/domainspec/RELATIONSHIPS.md)

Ledger: [../source-ledger.md](../source-ledger.md)

## Why This Source Matters

DomainSpec gives CyberAlchemy a disciplined way to make intent precise enough to compare with reality.

It says: understand the domain before implementation, then derive tests, code, UI, observability, infrastructure, and verification from structured documentation.

## Compiled Concepts

### Specification-First Pipeline

DomainSpec pipeline:

```text
classify concepts
  -> connect relationships
  -> document feature slices
  -> derive tests
  -> implement backend
  -> design and build UI
  -> maintain registry
  -> derive observability
  -> deploy infrastructure
  -> verify readiness
```

Each stage depends on prior structured understanding. Skipping a stage should be visible and deliberate.

### Meta-Concept Taxonomy

DomainSpec classifies domain knowledge into meta-types.

Backend concepts:

- Entity;
- Value Object;
- Enum / Type;
- Operation;
- Query;
- Calculation;
- Rule;
- Policy;
- Workflow;
- Saga;
- Interface;
- Event;
- Mapping;
- State Machine.

UI concepts:

- Page;
- Layout;
- Component;
- View Model;
- Hook;
- Form;
- Action;
- Guard;
- Binding;
- Adapter;
- State Indicator.

For CyberAlchemy, this is a model for ontology entry typing: knowledge becomes more useful when its type is explicit.

### Relationship Graph

DomainSpec turns concepts into a navigable graph through typed edges.

Examples:

- `performs`: entity initiates operation;
- `enforces`: rule gates operation;
- `calculates`: calculation feeds operation;
- `orchestrates`: workflow coordinates operations;
- `exposes`: interface makes operation/query accessible;
- `maps`: mapping transforms data;
- `renders`: page renders components;
- `fetches`: binding reads backend query;
- `mutates`: binding invokes backend operation;
- `mirrors`: UI guard mirrors backend rule.

CyberAlchemy should use this as precedent for ontology edge discipline.

## CyberAlchemy Adaptation

DomainSpec becomes the structured-intent layer of the CyberAlchemy stack.

It supports Saturn by giving the convergence loop something concrete to protect:

```text
domain concept
  -> typed relationship
  -> specification
  -> tests and metrics
  -> implementation
  -> evidence
  -> drift/convergence check
```

## Candidate Ontology Claims

| Claim                                                                    | Branch               | Candidate Entry                       |
| ------------------------------------------------------------------------ | -------------------- | ------------------------------------- |
| Intent must be structured before convergence can be measured.            | philosophy           | `method-domainspec-structured-intent` |
| Typed concepts make domain knowledge retrievable and testable.           | knowledge-governance | `concept-typed-concept-inventory`     |
| Relationships turn documentation into a graph.                           | knowledge-governance | `concept-typed-relationship-graph`    |
| Tests, observability, and verification should derive from specification. | bridge               | `bridge-spec-to-evidence-derivation`  |

## Tensions And Promotion Gaps

- DomainSpec's taxonomy is product/software oriented; CyberAlchemy must adapt it for agent-operation concepts.
- The ontology pack should define which DomainSpec types map directly to Operational Ontology entry types.

## Agent Payload

When using DomainSpec inside CyberAlchemy:

```text
do not protect vague intent
classify it
connect it
derive obligations
observe reality
compare evidence back to intent
```
