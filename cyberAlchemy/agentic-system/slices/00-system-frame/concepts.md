---
module: cyberalchemy-agentic-system
slice: 00-system-frame
status: candidate
updatedAt: 2026-05-19
docType: slice-concepts
---

# Concepts: System Frame

Work: [README.md](README.md)

## What This Slice Compiles

This slice gathers the top-level operating idea from the scattered repository sources:

- CyberAlchemy frames software as a feedback surface for discovering and governing systems.
- Saturn gives that surface a convergence loop.
- DomainSpec gives the loop structured intent.
- Arcanum gives agents reusable capability surfaces.
- The CyberAlchemy Method gives the work a governed synthesis discipline.

The frame is:

```text
intent
  -> structured specification
  -> routed capability execution
  -> observable evidence
  -> drift and residue detection
  -> governed learning
```

## Schema And Evidence

CyberAlchemy starts from a two-layer view.

The schema layer contains what the system says should be true:

- ontology;
- definitions;
- contracts;
- policies;
- prompts;
- route templates;
- tests;
- observability obligations;
- axioms;
- constitutions;
- meta-models.

The evidence layer contains what actually happened:

- sessions;
- source files;
- code;
- tests;
- telemetry;
- run logs;
- route outcomes;
- user corrections;
- observed runtime behavior;
- operational friction.

The system is designed to chase symmetry between these layers. Symmetry does not mean they are identical. It means the relationship between intention and reality is visible, traceable, and correctable.

When schema and evidence do not align, the mismatch should become a named object:

- drift;
- bridge gap;
- validation gap;
- route miss;
- output drift;
- unresolved premise;
- user workflow friction;
- contradiction;
- residuality finding.

That named object then routes to inventory, ontology, decision, execution, or maintenance.

## Saturn: The Convergence Loop

Saturn is the control loop that acts on drift.

DomainSpec defines drift as measurable divergence between intended behavior and observed system reality. That divergence can appear as:

- semantic drift: concepts or relationships no longer describe the domain clearly;
- contract drift: feature behavior and derived obligations no longer match implementation;
- runtime drift: production behavior deviates from rules, calculations, states, or workflows;
- governance drift: enforcement and escalation stop matching policy intent;
- coordination drift: humans and agents stop aligning around priorities, risks, or closure evidence.

Convergence is evidence-backed reduction of critical drift. A system is converging when:

- formal contracts remain stable enough to guide implementation;
- tests and metrics continue to match intended behavior;
- violations, governance gaps, and coordination failures trend down;
- closure evidence gets clearer;
- blockers shrink over time;
- priorities reflect live objectives and measured reality.

Saturn sits above those definitions as the loop:

```text
observe drift
  -> decide response
  -> execute correction
  -> verify convergence
  -> update governance
```

Saturn is not the same thing as monitoring. Monitoring notices events. Saturn interprets those events against intent and asks what corrective route should respond.

## DomainSpec: Structured Intent

DomainSpec is the specification-first discipline that gives Saturn something precise to protect.

Its baseline claim is that many software problems are not caused by poor code, but by implementation outrunning understanding. DomainSpec slows that down by turning domain knowledge into formal, traceable artifacts before execution.

The DomainSpec pipeline is:

| Stage                  | Input                             | Output                                      |
| ---------------------- | --------------------------------- | ------------------------------------------- |
| 1. Classify            | Business knowledge                | Typed concept inventory                     |
| 2. Connect             | Concept inventory                 | Navigable knowledge graph                   |
| 3. Document            | Knowledge graph                   | Feature vertical slices                     |
| 4. Derive Tests        | Aspect docs and UI spec           | Backend and end-to-end test obligations     |
| 5. Implement Backend   | Test spec and aspect docs         | Production code and passing tests           |
| 6. Design And Build UI | UI architecture and aspect docs   | UI spec, pages, and E2E tests               |
| 7. Maintain Registry   | Feature concept tables            | Global registry and glossary sync           |
| 8. Observability       | Aspect docs and metadata          | Metrics, alerts, and monitoring obligations |
| 9. Infrastructure      | Infra architecture and SLOs       | Deployment artifacts and monitoring stack   |
| 10. Verify             | Backend, UI, observability, infra | PASS, FLAG, or BLOCK readiness verdict      |

DomainSpec also provides the domain modeling vocabulary. Its taxonomy includes backend meta-concepts such as Entity, Value Object, Enum, Operation, Query, Calculation, Rule, Policy, Workflow, Saga, Interface, Event, Mapping, and State Machine. Its UI vocabulary includes Page, Layout, Component, View Model, Hook, Form, Action, Guard, Binding, Adapter, and State Indicator.

The relationship catalog turns those concepts into a graph. Examples:

- `performs`: entity initiates operation;
- `enforces`: rule constrains operation;
- `calculates`: calculation feeds operation;
- `orchestrates`: workflow coordinates operations;
- `exposes`: interface exposes operation or query;
- `maps`: mapping transforms data;
- `renders`: page renders components;
- `fetches`: UI binding fetches backend query;
- `mutates`: UI binding invokes backend operation;
- `mirrors`: UI guard mirrors backend rule.

For CyberAlchemy, the key idea is that DomainSpec makes intent structured enough to compare against execution.

## Arcanum: Reusable Capability Surface

Arcanum is the reusable agent capability framework.

It categorizes capabilities by epistemic nature:

| Tier           | Meaning                            | Role                                                                  |
| -------------- | ---------------------------------- | --------------------------------------------------------------------- |
| Formulae       | Deterministic operational sigils   | Repeatable rule-based operations.                                     |
| Transmutations | Bounded cognitive synthesis sigils | Transform scattered material into a concrete artifact.                |
| Arcana         | Autonomous orchestration sigils    | Manage uncertainty across goals, evidence, roles, and decisions.      |
| Spells         | Workflow compositions              | Combine sigils with shared state, gates, handoffs, and observability. |

Arcanum prevents agent work from becoming a loose collection of prompts. A useful capability should have:

- purpose;
- trigger conditions;
- inputs;
- outputs;
- quality bar;
- anti-patterns;
- lifecycle owner;
- observability;
- maintenance route.

Necronomicon is the persistent repository harness for Arcanum. It keeps session memory, route history, checkpoints, research briefs, fallback discovery, and maintenance recommendations. It routes work to owning capabilities without becoming the owner of every truth.

## CyberAlchemy Method

The CyberAlchemy Method is the governed synthesis discipline behind Arcanum.

It keeps five anchors visible:

| Anchor          | Question                                                                |
| --------------- | ----------------------------------------------------------------------- |
| Objective       | What are we trying to solve?                                            |
| Output artifact | What should exist when the work is done?                                |
| Discovery       | What must we learn before closure?                                      |
| Tension         | What could make the artifact brittle, misleading, oversized, or unsafe? |
| Route           | Who or what owns the next lifecycle step?                               |

Its method loop is:

| Phase     | Purpose                                                            |
| --------- | ------------------------------------------------------------------ |
| Orient    | Name the seed, bound context, state target result.                 |
| Discover  | Find evidence, gaps, unknowns, and alternative frames.             |
| Shape     | Choose route, draft artifact, test with tension, revise.           |
| Stabilize | Make work navigable, preserve openness, record trace, route owner. |
| Evolve    | Reflect after use so repeated work improves the method.            |

The method primitives most relevant to the agentic system are:

- Route Before Work: choose the smallest responsible lifecycle authority before output.
- Gate Before Mutation: consequential changes stop until blocker decisions are resolved.
- Obligation-Linked Context: include evidence because it closes an obligation, not because it is interesting.
- Trace Before Promotion: terms and claims promote only when evidence and governance justify it.
- Reflection Outer Loop: usage signals and output drift should produce evidence-backed improvement proposals.

## How The Frame Fits Together

The whole frame can be read as a responsibility stack:

```text
Saturn
  names the convergence pressure

DomainSpec
  structures intent into concepts, relationships, tests, metrics, and verification

Arcanum
  turns repeated agent work into reusable capabilities

Necronomicon
  gives repository work durable memory and route coordination

Inventory
  compiles source evidence so it can be reused

Ontology
  governs meaning, confidence, branches, and promotion

Context Builder
  selects the task-sized slice

Execution
  acts through bounded capabilities

Observability and Reflection
  turn action into future learning
```

## What This Means For Ontology

The system frame should become ontology as a set of governing concepts, not as a vague narrative.

First ontology candidates:

| Candidate                             | Meaning                                                                            |
| ------------------------------------- | ---------------------------------------------------------------------------------- |
| `method-saturn-convergence-loop`      | The control loop that observes drift, routes correction, and verifies convergence. |
| `method-domainspec-structured-intent` | The discipline that turns domain understanding into traceable obligations.         |
| `method-arcanum-capability-system`    | The capability framework for reusable agent work.                                  |
| `concept-schema-data-symmetry`        | The governing lens between intended model and observed reality.                    |
| `concept-translation-residue`         | Loss, ambiguity, or contradiction created when moving between layers.              |

These entries should link downward to inventory, ontology, memory, execution, observability, and promotion slices.
