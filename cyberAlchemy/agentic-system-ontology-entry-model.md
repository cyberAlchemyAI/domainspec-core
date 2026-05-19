---
module: cyberalchemy-agentic-system
version: current
status: candidate
updatedAt: 2026-05-19
docType: ontology-entry-model
---

# Agentic System Ontology Entry Model

Navigation: [agentic-system-navigation.md](agentic-system-navigation.md)
Pipeline: [agentic-system-inventory-ontology-pipeline.md](agentic-system-inventory-ontology-pipeline.md)
Definition: [agentic-system-definition.md](agentic-system-definition.md)

## Core Rule

Ontology entries are thick knowledge objects.

They should contain the usable content, context, applicability rules, retrieval payload, edges, confidence, and promotion state that an agent needs. They should not be thin pointers to inventory pages.

Inventory prepares evidence. Ontology owns usable knowledge. Context Builder extracts the task-specific slice.

```text
raw source
  -> inventory captures source summaries, extracted claims, tags, contradictions, and provenance
  -> ontology entry distills the agent-usable knowledge object
  -> context-builder selects the relevant ontology slice for a concrete task
  -> agent executes with cited context, constraints, and confidence
```

## Layer Responsibilities

| Layer           | Owns                                                                                                                           | Does Not Own                                              |
| --------------- | ------------------------------------------------------------------------------------------------------------------------------ | --------------------------------------------------------- |
| Raw Sources     | Original evidence, authored context, source authority.                                                                         | Generated synthesis, promotion, retrieval shortcuts.      |
| Inventory       | Ingestion, source summaries, extracted claims, indexes, tags, contradictions, provenance, lookup selectors.                    | Final meaning, route authority, operational instructions. |
| Ontology        | Thick knowledge entries, definitions, context payloads, edges, confidence, applicability, promotion state, retrieval guidance. | Raw source mutation, unreviewed memory promotion.         |
| Context Builder | Task-specific context packs selected from ontology and inventory evidence.                                                     | Ontology promotion or source reinterpretation.            |
| Agent Execution | Uses context, runs route, emits evidence.                                                                                      | Silent ontology mutation.                                 |

## Ontology As Superset

Ontology is a superset of inventory in the semantic and operational sense:

- It can classify everything important in inventory.
- It can relate inventory entries to broader concepts, routes, policies, and meta-models.
- It can contain distilled content that is directly usable by agents.
- It keeps evidence references back to inventory and raw sources.

Ontology is not a storage superset:

- It should not copy every source summary.
- It should not absorb every weak claim.
- It should not replace inventory indexes, logs, or tags.
- It should not treat generated inventory pages as source authority.

## Required Entry Shape

Every ontology entry should include these sections.

| Section       | Purpose                                                                                                          |
| ------------- | ---------------------------------------------------------------------------------------------------------------- |
| Identity      | Stable id, title, type, branch, status, owner, dates.                                                            |
| Content       | Definition, purpose, scope, exclusions, examples, non-examples.                                                  |
| Context       | Use-when rules, applicability, invalidation conditions, operational constraints.                                 |
| Agent Payload | Compact instructions or retrieval payload an agent can use during execution.                                     |
| Edges         | Typed relationships to other ontology entries, inventory entries, sources, capabilities, signals, and decisions. |
| Evidence      | Inventory entries and raw source references supporting the entry.                                                |
| Confidence    | Evidence confidence, commitment confidence, scope of validity, expiry condition.                                 |
| Promotion     | Candidate/reviewed/promoted state, next gate, required evidence, contradiction path.                             |
| Maintenance   | Review trigger, owner route, stale conditions, related open questions.                                           |

## Markdown Template

Use this shape for entries under `cyberAlchemy/ontology/entries/`.

```markdown
---
id: agentic.<stable-id>
type: <OntologyBranch | OperationalLesson | ContextSolution | MemoryPattern | CapabilityPattern | FailureMode | MethodPrimitive | MetaModelCandidate>
branch: <philosophy | knowledge-governance | operational | memory | capability | feedback | research | bridge>
status: candidate
owner: CyberAlchemy AI
updatedAt: YYYY-MM-DD
evidenceConfidence: low | medium | high
commitmentConfidence: low | medium | high
---

# <Entry Title>

## Content

Definition:

Purpose:

Scope:

- Includes:
- Excludes:

Examples:

Non-examples:

## Context

Use when:

Do not use when:

Applies to:

Invalidated when:

Operational constraints:

## Agent Payload

Summary:

Required checks:

Recommended route:

Context to load:

Pitfalls:

## Edges

| Edge      | Target            | Evidence | Notes  |
| --------- | ----------------- | -------- | ------ |
| traced_to | <source-or-entry> | <path>   | <note> |

## Evidence

Inventory entries:

- <inventory-entry-path>

Source references:

- <source-path>

## Confidence

Evidence confidence:

Commitment confidence:

Scope of validity:

Expiry condition:

## Promotion

Current state:

Next gate:

Required evidence:

Contradiction path:

## Maintenance

Review trigger:

Owner route:

Open questions:
```

## Example: Operational Ontology Entry

```yaml
id: agentic.operational_ontology
type: OntologyBranch
branch: operational
status: candidate
owner: CyberAlchemy AI
evidenceConfidence: medium
commitmentConfidence: medium

content:
  definition: >
    Operational Ontology governs reusable knowledge about agent operation,
    including lessons, route patterns, context solutions, failure modes,
    prompt contracts, and capability maintenance.
  purpose: >
    Help agents retrieve prior operational knowledge and apply it safely
    in similar execution contexts.
  scope:
    includes:
      - sigil optimization lessons
      - spell composition lessons
      - skill and agent definitions
      - context solution cards
      - route policies
      - operational failure modes
    excludes:
      - raw session memory as authority
      - unreviewed user-specific workflow assumptions

context:
  use_when:
    - an agent is choosing a route
    - a task resembles a past execution pattern
    - telemetry suggests repeated operational friction
  invalidated_when:
    - ontology-harness rejects the branch model
    - evidence shows repeated harmful overgeneralization

agent_payload:
  summary: Use Operational Ontology to retrieve prior agent-operation lessons.
  required_checks:
    - cite evidence
    - check scope of validity
    - check expiry condition
    - do not treat memory as authority
  recommended_route: ontology-harness or context-builder

edges:
  learned_from:
    - inventory.operational_lessons.aeo_capability_sequence
  applies_to:
    - agentic.execution_context
  constrained_by:
    - agentic.user_workflow_privacy_policy
  observed_by:
    - agentic.feedback_ontology

evidence:
  inventory_entries:
    - .arcanum/inventory/entries/cyberalchemy-agentic-system/ontology-branch-operational-ontology.md
  source_refs:
    - cyberAlchemy/agentic-system-definition.md
    - arcanum/arcana/ontology-vault/README.md
    - implementation/domainspec/docs/features/agent-execution-orchestrator/work-pack/context/capability-sequence-lessons.md

promotion:
  current_state: candidate
  next_gate: ontology-harness review
  required_evidence:
    - branch map validates node and edge vocabulary
    - at least one context-builder proof uses the entry successfully
```

## Entry Types

| Entry Type           | Thick Content It Must Carry                                                                                     |
| -------------------- | --------------------------------------------------------------------------------------------------------------- |
| `OntologyBranch`     | Authority, allowed claim types, excluded claim types, branch edge rules, promotion route.                       |
| `AuthorityLadder`    | Ordered states, authority level per state, transition owners, skip rules, confidence gates, contradiction path. |
| `OperationalLesson`  | Lesson, source context, applicability, failure mode avoided, route impact, confidence, expiry.                  |
| `ContextSolution`    | Trigger fingerprint, compact payload, recommended route, required evidence, pitfalls, invalidation.             |
| `MemoryPattern`      | Memory behavior, ergonomics value, privacy class, promotion boundary, repeated evidence.                        |
| `CapabilityPattern`  | Capability owner, route behavior, input/output contract, composition rule, telemetry expectation.               |
| `FailureMode`        | Stressor, degradation path, detection signal, recovery route, prevented-by edges.                               |
| `MethodPrimitive`    | Rule, phase, operational use, anti-pattern, route owner, source method reference.                               |
| `MetaModelCandidate` | Generalization, source examples, scope, recomposition proof, contradiction trigger.                             |

## Retrieval Rule

Context Builder should prefer ontology entries when the task needs meaning, policy, route choice, or operational guidance.

Inventory lookup should be included when the task needs source evidence, raw provenance, contradictions, or broader discovery.

```text
Need action guidance? Load ontology entry.
Need proof or provenance? Load inventory entry and source refs.
Need task context? Load the smallest ontology slice plus only the evidence selectors required by the task.
```

## Promotion Rule

An ontology entry can become more authoritative only when its content and context survive review.

```text
memory observation or raw source
  -> inventory evidence entry
  -> thick ontology candidate
  -> context-builder proof or ontology-harness review
  -> premise or promoted ontology entry
  -> route/capability/context update
```

Never promote a pointer-only node. If an ontology entry cannot explain its meaning, use context, evidence, and constraints, it is not ready to guide an agent.
