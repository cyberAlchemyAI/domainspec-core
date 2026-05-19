# CyberAlchemy Agentic System Knowledge Map

Status: discovery-mode architecture reference
Date: 2026-05-19
Owner: CyberAlchemy AI
Navigation: [agentic-system-navigation.md](agentic-system-navigation.md)

This map collects the repository knowledge that should be consulted when drafting the CyberAlchemy agentic system architecture. It is intentionally a synthesis layer: source files remain authoritative, and this document points back to them instead of replacing them.

## Core Thesis

CyberAlchemy is building an agentic system that chases symmetry between intent and reality.

The repository expresses that thesis in several local dialects:

| Dialect                 | Local expression                                                                                                                                                                   | Source                                                                                                                                     |
| ----------------------- | ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------ |
| CyberAlchemy philosophy | Software is an observational probe for discovering and mapping unknown domains; systems should track intent, interpret reality, verify alignment, and feed data back to operators. | [main.html](main.html)                                                                                                                     |
| Saturn                  | Drift is the force pulling blueprint and runtime apart; Saturn is the cybernetic loop that observes, decides, executes, and verifies convergence.                                  | [saturn-research-presentation.md](saturn-research-presentation.md)                                                                         |
| DomainSpec              | Domain documents are semantic source of truth; code is their compiled image; typed concepts and relationships derive tests, metrics, implementation, and verification.             | [README.md](../implementation/domainspec/README.md), [domainspec-axioms.md](../implementation/domainspec/vault/axiom/domainspec-axioms.md) |
| Arcanum                 | Reusable agent capabilities are classified, composed, observed, and maintained as sigils and spells.                                                                               | [README.md](../arcanum/README.md)                                                                                                          |
| Necronomicon            | Repository work needs durable memory, selected capability routing, inventory, ontology, checkpoints, and candidate-only promotion.                                                 | [README.md](../arcanum/spells/necronomicon/README.md), [necronomicon.html](necronomicon.html)                                              |
| MARS                    | Research programs need deterministic gates, explicit dependency contracts, append-only evidence, and claim updates over time.                                                      | [README.md](../research/projects/mars/README.md), [MARS-PIPELINE.md](../research/projects/mars/definitions/MARS-PIPELINE.md)               |
| MOGT                    | Agentic conversation decisions should expose objective vectors, tradeoffs, traceability, overhead, and negotiation/convergence behavior.                                           | [README.md](../research/projects/mogt-agentic-conversation/README.md)                                                                      |

## Knowledge Tower

The repo already describes a progressive authority ladder. This is the most important architecture seed for knowledge and memory.

```text
raw interaction
  -> session evidence
  -> discovery baseline
  -> inventory knowledge
  -> ontology candidate
  -> reviewed premise
  -> confidence decision
  -> constitution or axiom
  -> bridge-validated operating context
```

Reference: [KNOWLEDGE-SUBSTRATE-FLOW.md](../arcanum/spells/necronomicon/development/KNOWLEDGE-SUBSTRATE-FLOW.md).

Use this as the default rule for new knowledge:

1. Memory preserves working continuity.
2. Inventory makes source-grounded knowledge reusable.
3. Ontology assigns roles, branches, confidence, and bridge edges.
4. Premises and confidence reviews decide what can be relied on.
5. Constitutions and axioms are rare, reviewed, high-authority promotions.
6. Bridge evidence is required before claiming system reality realizes intent.

## Current Ontology Model

The repository has a mature branch-aware ontology model:

| Branch            | Authority                                                                                  | Typical claims                                                                       | Source                                                                                            |
| ----------------- | ------------------------------------------------------------------------------------------ | ------------------------------------------------------------------------------------ | ------------------------------------------------------------------------------------------------- |
| Business Ontology | Meaning, intent, policy, value, outcome, domain rules.                                     | What should be true, why it matters, who it affects, and how success is judged.      | [BUSINESS-ONTOLOGY.md](../arcanum/BUSINESS-ONTOLOGY.md)                                           |
| System Ontology   | Implementation, runtime behavior, data shape, technical constraints, tests, observability. | What exists, how it behaves, where it runs, and how it is measured.                  | [ontology-vault README](../arcanum/arcana/ontology-vault/README.md)                               |
| Bridge Ontology   | Traceability, realization, coverage, constraints, evidence gaps, drift.                    | How business claims connect to system artifacts, tests, metrics, and drift findings. | [business-system-bridge.md](../arcanum/arcana/ontology-vault/templates/business-system-bridge.md) |

Existing bridge edge types:

```text
realized_by
depends_on
constrained_by
observed_by
tested_by
drifts_from
traced_to
```

Reference: [Ontology Vault](../arcanum/arcana/ontology-vault/README.md).

### Operational Ontology Gap

The user-requested Operational Ontology is not yet modeled as a first-class branch. The repo has the ingredients, but they are distributed:

| Ingredient                | What it already captures                                                                 | Source                                                                                                                                                     |
| ------------------------- | ---------------------------------------------------------------------------------------- | ---------------------------------------------------------------------------------------------------------------------------------------------------------- |
| Capability lessons        | Reusable execution sequence lessons from agent execution work.                           | [capability-sequence-lessons.md](../implementation/domainspec/docs/features/agent-execution-orchestrator/work-pack/context/capability-sequence-lessons.md) |
| Invocation telemetry      | Capability run envelopes, signal ledgers, reflection triggers.                           | [Observed Invocation Loop](../arcanum/spells/observed-invocation-loop/README.md), [Signal Observer](../arcanum/arcana/signal-observer/README.md)           |
| Workflow reflection       | Repeated gaps and patterns become evidence-backed improvement proposals.                 | [Workflow Reflect](../arcanum/arcana/workflow-reflect/README.md)                                                                                           |
| Sigil maintenance         | Observation -> reflection -> approved sigil updates.                                     | [Sigil Maintenance Loop](../arcanum/spells/sigil-maintenance-loop/README.md)                                                                               |
| Agent execution contracts | Route templates, stage contracts, stage IDs, terminal outcomes, telemetry envelopes.     | [Agent Execution Orchestrator](../implementation/domainspec/docs/features/agent-execution-orchestrator/SPEC.md)                                            |
| Subagent premises         | Dispatch thresholds, parallel independence, briefing quality, trust-but-verify.          | [domainspec-subagents-strategy-premises.md](../implementation/domainspec/vault/premise/domainspec-subagents-strategy-premises.md)                          |
| User ergonomics           | Side notes, active interaction, continuation before fresh routing, local-first evidence. | [USAGE-VISION.md](../arcanum/spells/necronomicon/development/USAGE-VISION.md)                                                                              |

Operational Ontology should unify these into a governed branch for agent operation knowledge: what routes work, in what context, with what evidence, against which failure modes, and when a shortcut should become a skill, sigil, spell, or agent definition.

## Memory Model Seeds

Memory is already defined as a working state vault, not as authority.

| Memory artifact                                 | Role                                                                          | Source                                                                                                |
| ----------------------------------------------- | ----------------------------------------------------------------------------- | ----------------------------------------------------------------------------------------------------- |
| `.arcanum/necronomicon/sessions/<id>/memory.md` | Durable session summary of objective, facts, decisions, and next action.      | [necronomicon.html](necronomicon.html#memory)                                                         |
| `routes.jsonl`                                  | Route attempts, selected command, confidence, result, and validation.         | [necronomicon.html](necronomicon.html#memory)                                                         |
| `decisions.md`                                  | Resolved choices, assumptions, and blocked tradeoffs.                         | [necronomicon.html](necronomicon.html#memory)                                                         |
| `side-notes.jsonl`                              | Side notes, research seeds, unblockers, contradictions, reminders.            | [KNOWLEDGE-SUBSTRATE-FLOW.md](../arcanum/spells/necronomicon/development/KNOWLEDGE-SUBSTRATE-FLOW.md) |
| `active-interaction.json`                       | Continuation state so user replies continue the active capability by default. | [Necronomicon Design](../arcanum/spells/necronomicon/development/DESIGN.md)                           |
| `.arcanum/observability/`                       | Telemetry for capability use, validation, thresholds, reflection.             | [Observed Invocation Loop](../arcanum/spells/observed-invocation-loop/README.md)                      |

Design implication: memory should be execution-context driven. It should help the next run retrieve shortcuts, active constraints, user preferences, repeated route patterns, and pending gaps. It should not silently become ontology. Repeated memory patterns become inventory candidates, then Operational Ontology candidates, then lifecycle updates only through review gates.

## Execution System Seeds

The repo has three execution models that should be reconciled rather than duplicated.

### Arcanum capability model

Arcanum tiers capabilities by epistemic nature:

| Tier           | Meaning                                                                    | Example                                             |
| -------------- | -------------------------------------------------------------------------- | --------------------------------------------------- |
| Formulae       | Deterministic operational sigils.                                          | `observability-setup`                               |
| Transmutations | Bounded cognitive synthesis.                                               | `context-builder`, `implementation-layering`        |
| Arcana         | Autonomous orchestration with uncertainty, roles, evidence, and decisions. | `ontology-vault`, `task-session`, `signal-observer` |
| Spells         | Compositions of sigils with state, gates, handoffs, and observability.     | `invoke`, `necronomicon`, `ontology-harness`        |

References: [Arcanum README](../arcanum/README.md), [Sigil Registry](../arcanum/registry/SIGILS.md), [Spell Registry](../arcanum/registry/SPELLS.md).

### DomainSpec execution model

DomainSpec is the specification-first delivery pipeline:

```text
classify concepts
  -> connect relationships
  -> write vertical slice docs
  -> derive tests
  -> implement
  -> derive observability
  -> deploy/infrastructure
  -> verify/readiness
  -> emit signals
  -> tune framework
```

References: [DomainSpec README](../implementation/domainspec/README.md), [TUNING-LOOP.md](../implementation/domainspec/TUNING-LOOP.md).

### Agent Execution Orchestrator model

Agent Execution Orchestrator formalizes agent runs as route templates and telemetry envelopes:

| Concept                 | Purpose                                                                                 |
| ----------------------- | --------------------------------------------------------------------------------------- |
| `ExecutionPipeline`     | Owns one orchestration capability and route policy.                                     |
| `PipelineRouteTemplate` | Ordered stage composition contract.                                                     |
| `StageContract`         | Purpose, inputs, terminal obligations, isolation mode.                                  |
| `ExecutionRun`          | One route execution with state, stages, retries, leases, snapshots.                     |
| `TelemetryEnvelope`     | Started/terminal telemetry pair, guard evidence, transcript ref, decision snapshot ref. |

References: [SPEC.md](../implementation/domainspec/docs/features/agent-execution-orchestrator/SPEC.md), [domain.md](../implementation/domainspec/docs/features/agent-execution-orchestrator/domain.md), [observability.md](../implementation/domainspec/docs/features/agent-execution-orchestrator/observability.md).

## Feedback Loop Map

| Loop                     | Signal input                                                        | Control decision                                               | Actuator                                               | Learning output                                        |
| ------------------------ | ------------------------------------------------------------------- | -------------------------------------------------------------- | ------------------------------------------------------ | ------------------------------------------------------ |
| Saturn                   | Tests, telemetry, governance drift, runtime drift.                  | Corrective routing and convergence priorities.                 | Governance, execution, regulation, interface.          | Drift/convergence trend.                               |
| DomainSpec tuning        | `docs/signals/pipeline-signals.jsonl`.                              | Thresholds TH1-TH10 and reflect reports.                       | Skill, agent, template, governance updates.            | Evidence-backed tuning proposals.                      |
| Observed Invocation Loop | Capability invocation envelopes.                                    | Reflection trigger and maintenance recommendation.             | `workflow-reflect`, `sigil-development`, `spellcraft`. | Capability telemetry and reflection reports.           |
| Necronomicon             | Route misses, gaps, memory, side notes, checkpoints.                | Route, checkpoint, inventory, ontology, decision, maintenance. | Selected sigils/spells.                                | Resumable session memory and candidate knowledge.      |
| MARS                     | Experiment run data, integrity audits, analysis, evidence status.   | Claim adjudication and next experiment priorities.             | Research pipeline stages.                              | Stronger or weaker claim support.                      |
| MOGT                     | Decision traces, objective vectors, negotiation outcomes, overhead. | Policy selection and conversation arbitration.                 | Agent decision policy.                                 | Traceability, quality, cost, latency, safety evidence. |

## Schema/Data Symmetry

The user's schema/data lens appears across the repo as several equivalent splits:

| Schema side            | Data/evidence side             | Translation residue                                                   |
| ---------------------- | ------------------------------ | --------------------------------------------------------------------- |
| Business Ontology      | System Ontology                | Bridge gaps, drift reports, unfulfilled promises, unauthorized scope. |
| DomainSpec typed graph | Code, tests, metrics           | Orphan behavior, derived obligation drift, failed verification.       |
| Sigil/Spell contracts  | Invocation telemetry           | Workflow gaps, output drift, anti-pattern hits, validation gaps.      |
| MARS protocols         | Run JSONL and analysis outputs | Evidence gaps, integrity failures, claim-status uncertainty.          |
| User workflow model    | Session routes and side notes  | Ergonomic friction, repeated clarifications, route misses.            |

Design implication: the system should make translation residue explicit as a first-class object, not as a hidden failure. Residue can then become research, ontology review, task work, or capability maintenance.

## Consultable Source Contracts

Use these sources when drafting or revising the architecture.

### Philosophy and product surface

| Source                                                             | Use in design                                                                                           |
| ------------------------------------------------------------------ | ------------------------------------------------------------------------------------------------------- |
| [main.html](main.html)                                             | CyberAlchemy philosophy: research as domain discovery; code as observational probe; Cybernetics^2.      |
| [saturn-research-presentation.md](saturn-research-presentation.md) | Drift/convergence loop and four-layer Saturn architecture.                                              |
| [necronomicon.html](necronomicon.html)                             | Human-facing explanation of knowledge substrate, business/system ontology, session memory, and routing. |
| [mars.html](mars.html)                                             | Public MARS framing: deterministic research governance.                                                 |
| [mogt.html](mogt.html)                                             | Public MOGT framing: objective-vector conversational decisions.                                         |

### Ontology, knowledge, and memory

| Source                                                                                                | Use in design                                                                         |
| ----------------------------------------------------------------------------------------------------- | ------------------------------------------------------------------------------------- |
| [BUSINESS-ONTOLOGY.md](../arcanum/BUSINESS-ONTOLOGY.md)                                               | Business/System/Bridge ontology model and Via Negativa promotion threshold.           |
| [Ontology Vault README](../arcanum/arcana/ontology-vault/README.md)                                   | Branch-aware authority model, confidence split, edge types, output artifacts.         |
| [Ontology Harness README](../arcanum/spells/ontology-harness/README.md)                               | How inventory, ontology-vault, and context-builder compose into governance.           |
| [KNOWLEDGE-SUBSTRATE-FLOW.md](../arcanum/spells/necronomicon/development/KNOWLEDGE-SUBSTRATE-FLOW.md) | Authority ladder and candidate-only promotion flow.                                   |
| [ontology-conventions.md](../implementation/domainspec/vault/ontology-conventions.md)                 | Vault frontmatter, roles, confidence axes, edge discipline, orthogonality discipline. |
| [confidence-levels.md](../implementation/domainspec/vault/confidence-levels.md)                       | Draft -> exploratory -> active -> consolidated -> evergreen maturity levels.          |
| [ontology-architecture-draft.md](../implementation/domainspec/vault/ontology-architecture-draft.md)   | Event-sourced knowledge graph, trust gates, graph-dropping RAG.                       |

### Execution and feedback

| Source                                                                                                          | Use in design                                                     |
| --------------------------------------------------------------------------------------------------------------- | ----------------------------------------------------------------- |
| [Arcanum README](../arcanum/README.md)                                                                          | Sigil/spell framework, tier ontology, runtime command surface.    |
| [Invoke README](../arcanum/spells/invoke/README.md)                                                             | Governed define/design/plan lifecycle and output contract.        |
| [Necronomicon README](../arcanum/spells/necronomicon/README.md)                                                 | Persistent repository harness and active interaction state.       |
| [Observed Invocation Loop](../arcanum/spells/observed-invocation-loop/README.md)                                | Capability telemetry, reflection trigger, closeout contract.      |
| [Signal Observer](../arcanum/arcana/signal-observer/README.md)                                                  | Post-run signal derivation and telemetry append.                  |
| [Workflow Reflect](../arcanum/arcana/workflow-reflect/README.md)                                                | Cross-run pattern analysis and improvement proposals.             |
| [Sigil Maintenance Loop](../arcanum/spells/sigil-maintenance-loop/README.md)                                    | Observe -> reflect -> update composition.                         |
| [Agent Execution Orchestrator](../implementation/domainspec/docs/features/agent-execution-orchestrator/SPEC.md) | Route artifacts, stage contracts, run state, telemetry envelopes. |
| [DELEGATION-TUNING.md](../docs/signals/DELEGATION-TUNING.md)                                                    | StageRunId pairing, watchdog windows, started/terminal telemetry. |
| [TERMINAL-GUARD.md](../docs/signals/TERMINAL-GUARD.md)                                                          | Command safety, timeout, retry, and terminal telemetry.           |

### DomainSpec and research

| Source                                                                                                   | Use in design                                                                   |
| -------------------------------------------------------------------------------------------------------- | ------------------------------------------------------------------------------- |
| [DomainSpec README](../implementation/domainspec/README.md)                                              | Spec-first pipeline and typed knowledge graph.                                  |
| [TAXONOMY.md](../implementation/domainspec/TAXONOMY.md)                                                  | Meta-type vocabulary for domain and UI concepts.                                |
| [RELATIONSHIPS.md](../implementation/domainspec/RELATIONSHIPS.md)                                        | Typed edge vocabulary and graph navigation.                                     |
| [DRIFT-CONVERGENCE.md](../implementation/domainspec/DRIFT-CONVERGENCE.md)                                | Operational definition of drift, convergence, and Saturn.                       |
| [TUNING-LOOP.md](../implementation/domainspec/TUNING-LOOP.md)                                            | Async signal-based framework tuning loop.                                       |
| [OBSERVABILITY.md](../implementation/domainspec/OBSERVABILITY.md)                                        | Docs -> runtime metrics derivation model.                                       |
| [DomainSpec definitions](../research/projects/domainspec/definitions/DEFINITIONS.md)                     | Dual-track L0-L7 architecture and deterministic derivation definitions.         |
| [DomainSpec claims](../research/projects/domainspec/claims/CLAIMS.md)                                    | Research claims for traceability, derivation, attenuation, and meta-governance. |
| [MARS README](../research/projects/mars/README.md)                                                       | Research program architecture and completeness dashboard.                       |
| [MARS pipeline](../research/projects/mars/definitions/MARS-PIPELINE.md)                                  | 13-stage research lifecycle and hard gates.                                     |
| [Research knowledge stack](../research/projects/mars/definitions/RESEARCH-KNOWLEDGE-STACK-CONTRACT.md)   | Foundations, definitions, references, inventory, context, resources.            |
| [MOGT domain context](../research/projects/mogt-agentic-conversation/foundations/DOMAIN-CONTEXT.md)      | Agentic conversation decision setting and failure modes.                        |
| [MOGT methodology](../research/projects/mogt-agentic-conversation/foundations/METHODOLOGY-AND-THEORY.md) | Comparative method, objective vectors, overhead and reviewer burden.            |

## Gaps That Matter

| Gap                                                                             | Why it matters                                                                                                             | Likely owner                                             |
| ------------------------------------------------------------------------------- | -------------------------------------------------------------------------------------------------------------------------- | -------------------------------------------------------- |
| Operational Ontology is not yet a formal ontology branch.                       | Agent operation lessons exist but are scattered across telemetry, work-pack context, premises, and maintenance docs.       | `ontology-harness` plus new Operational Ontology design. |
| Memory does not yet have a promotion protocol into Operational Ontology.        | Repeated shortcuts and user workflow signals can remain session residue instead of becoming reusable capability knowledge. | Necronomicon + `ontology-vault`.                         |
| Cross-ledger signal schemas are related but not unified.                        | OIL, DomainSpec tuning, MARS telemetry, delegation tuning, and terminal guard use different event vocabularies.            | Observability / operational ontology.                    |
| User mental model is acknowledged but not modeled.                              | Ergonomics and personal workflow are necessary for agent usefulness and should be testable against repeated interactions.  | Memory + operational ontology + privacy policy.          |
| Meta-model discovery is present but not registered as a stable artifact family. | Concept-layer optimizer, DomainSpec taxonomy, and MARS taxonomy need a shared way to promote reusable meta-models.         | Definitions governance + operational ontology.           |
| Residue/residuality is a strong concept but not tied to translation residue.    | Residuality can become the method for naming what survives failed translations between schema and data.                    | Residuality spec + ontology bridge.                      |

## Recommended Reading Order

1. [main.html](main.html) and [saturn-research-presentation.md](saturn-research-presentation.md) for philosophy.
2. [BUSINESS-ONTOLOGY.md](../arcanum/BUSINESS-ONTOLOGY.md), [Ontology Vault](../arcanum/arcana/ontology-vault/README.md), and [KNOWLEDGE-SUBSTRATE-FLOW.md](../arcanum/spells/necronomicon/development/KNOWLEDGE-SUBSTRATE-FLOW.md) for knowledge governance.
3. [Necronomicon README](../arcanum/spells/necronomicon/README.md) for memory and routing.
4. [DomainSpec README](../implementation/domainspec/README.md), [DRIFT-CONVERGENCE.md](../implementation/domainspec/DRIFT-CONVERGENCE.md), and [TUNING-LOOP.md](../implementation/domainspec/TUNING-LOOP.md) for spec-to-runtime loops.
5. [Agent Execution Orchestrator](../implementation/domainspec/docs/features/agent-execution-orchestrator/SPEC.md) for execution contracts.
6. [MARS README](../research/projects/mars/README.md) and [MOGT README](../research/projects/mogt-agentic-conversation/README.md) for research and decision-policy evidence.
