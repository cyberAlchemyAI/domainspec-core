---
module: cyberalchemy-agentic-system
slice: 04-operational-ontology
status: candidate
updatedAt: 2026-05-19
docType: slice-work
---

# Slice 04: Operational Ontology

Work layer: [CyberAlchemy Agentic System](../../README.md)
Concepts: [concepts.md](concepts.md)
Navigation: [agentic-system-navigation.md](../../../agentic-system-navigation.md)
Definition: [agentic-system-definition.md](../../../agentic-system-definition.md)

## Purpose

Create the ontology branch that stores reusable knowledge about agent operation itself.

Operational Ontology captures lessons about routes, sigils, spells, skills, prompts, context solutions, failure modes, telemetry, and maintenance.

## Already Done

- The definition file names Operational Ontology as a candidate branch.
- The deep dive explains Operational Ontology and its entry classes.
- The architecture file identifies operational lessons, route ledgers, and context solution cards.
- Existing source material includes observed invocation, workflow reflection, sigil maintenance, and agent execution contracts.

## Needs To Be Done

- Create `cyberAlchemy/ontology/operational-ontology-map.md`.
- Create the first Operational Ontology branch entry.
- Create first operational lesson entries.
- Create first failure mode entries.
- Create first context solution entries.
- Decide when an operational lesson becomes a route policy or capability update.

## Implementation Slice

1. Create `entries/ontology-branch-operational-ontology.md`.
2. Create first operational entries:
   - `operational-lesson-route-before-work.md`
   - `context-solution-invoke-define-design.md`
   - `failure-mode-memory-treated-as-authority.md`
   - `failure-mode-context-overload.md`
3. Link entries to source evidence:
   - observed invocation,
   - workflow reflect,
   - sigil maintenance,
   - agent execution orchestrator,
   - capability sequence lessons.
4. Add promotion states and review triggers.
5. Use context-builder to prepare context for one real operational decision.

## Acceptance Checks

- Operational Ontology is distinct from memory and the Arcanum registry.
- Each operational lesson names scope, evidence, failure mode avoided, and expiry condition.
- Context solution entries contain trigger fingerprints and recommended context.
- Route policies do not become authoritative without confidence and owner review.
- The branch can answer: "What should a future agent do differently because of prior execution evidence?"

## Links

| Role                         | Link                                                                                                                                                                |
| ---------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| Definition                   | [agentic-system-definition.md](../../../agentic-system-definition.md)                                                                                               |
| Deep dive                    | [agentic-system-deep-dive.md](../../../agentic-system-deep-dive.md)                                                                                                 |
| Architecture                 | [agentic-system-architecture.md](../../../agentic-system-architecture.md)                                                                                           |
| Observed Invocation Loop     | [Observed Invocation Loop](../../../../arcanum/spells/observed-invocation-loop/README.md)                                                                           |
| Workflow Reflect             | [Workflow Reflect](../../../../arcanum/arcana/workflow-reflect/README.md)                                                                                           |
| Sigil Maintenance Loop       | [Sigil Maintenance Loop](../../../../arcanum/spells/sigil-maintenance-loop/README.md)                                                                               |
| Agent Execution Orchestrator | [SPEC.md](../../../../implementation/domainspec/docs/features/agent-execution-orchestrator/SPEC.md)                                                                 |
| Capability sequence lessons  | [capability-sequence-lessons.md](../../../../implementation/domainspec/docs/features/agent-execution-orchestrator/work-pack/context/capability-sequence-lessons.md) |
