---
module: cyberalchemy-agentic-system
slice: 04-operational-ontology
status: candidate
updatedAt: 2026-05-19
docType: slice-concepts
---

# Concepts: Operational Ontology

Work: [README.md](README.md)

## What This Slice Compiles

This slice gathers operational knowledge from:

- Arcanum capability model;
- Necronomicon route and memory model;
- Observed Invocation Loop;
- Workflow Reflect;
- Sigil Maintenance Loop;
- DomainSpec tuning loop;
- Agent Execution Orchestrator;
- existing agentic-system definition and architecture.

Operational Ontology is the branch that lets the system learn how its agents, routes, prompts, sigils, spells, and execution patterns actually work.

## Why Operational Ontology Exists

Most ontologies describe the product domain or the technical system.

CyberAlchemy also needs an ontology of operation:

```text
how agents should choose routes
which context solves which task
what failure modes repeat
which sigil needs maintenance
which prompt contract is brittle
which lesson generalizes
which shortcut should expire
```

This is the system governing the governor.

## What It Owns

Operational Ontology owns reusable knowledge about agent operation.

| Knowledge Type           | Example                                                                           |
| ------------------------ | --------------------------------------------------------------------------------- |
| Route pattern            | Use ontology-harness before invoke when the task is knowledge promotion.          |
| Operational lesson       | Define the schema of a capability before implementing its runner.                 |
| Failure mode             | Memory treated as authority creates accidental canon.                             |
| Context solution         | For `invoke define -> design`, load definition, glossary, architecture, and gaps. |
| Capability pattern       | A sigil with repeated output drift should route to workflow reflect.              |
| Prompt contract lesson   | Prompts need input/output/gate shape before they can be maintained.               |
| Telemetry threshold      | Repeated validation gaps should create maintenance pressure.                      |
| Maintenance trigger      | A capability repeatedly misses a route or asks the same clarification.            |
| User workflow constraint | A preference can guide ergonomics only inside privacy scope.                      |

## What It Does Not Own

Operational Ontology is not:

- session transcript storage;
- raw memory;
- the Arcanum registry;
- source of truth for business meaning;
- automatic capability mutation;
- a personal profile without privacy boundaries.

The Arcanum registry names capabilities. Operational Ontology explains how and when to use them, what has been learned from use, and what evidence supports the lesson.

## Entry Classes

Operational Ontology entries should include:

| Entry Class          | Required Content                                                               |
| -------------------- | ------------------------------------------------------------------------------ |
| Operational lesson   | Lesson, source context, applicability, avoided failure, confidence, expiry.    |
| Context solution     | Trigger fingerprint, recommended context, route, evidence selectors, pitfalls. |
| Failure mode         | Stressor, degradation path, detection signal, recovery route, prevention edge. |
| Route policy         | Task conditions, route owner, confidence, fallback route, review trigger.      |
| Capability pattern   | Capability, input/output contract, composition rule, telemetry expectation.    |
| Maintenance trigger  | Signal pattern, threshold, affected capability, proposed owner route.          |
| Prompt contract      | Prompt purpose, required inputs, output shape, gates, anti-patterns.           |
| Meta-model candidate | Generalized pattern, examples, limits, contradiction trigger.                  |

## Source Seeds

The repository already has operational knowledge seeds.

| Source Area                  | What It Contributes                                                                                                       |
| ---------------------------- | ------------------------------------------------------------------------------------------------------------------------- |
| Observed Invocation Loop     | Managed invocations produce envelopes, one telemetry signal, reflection counters, and threshold routing.                  |
| Workflow Reflect             | Accumulated telemetry becomes evidence-backed recommendations: no change, targeted update, major revision, or retirement. |
| Sigil Maintenance Loop       | Observation and reflection can route into approved capability updates.                                                    |
| DomainSpec Tuning Loop       | Append-only signals accumulate across runs, thresholds create tuning pressure, reports propose structural improvements.   |
| Agent Execution Orchestrator | Route templates, stage contracts, execution runs, terminal outcomes, telemetry envelopes.                                 |
| Necronomicon                 | Route ledgers, checkpoints, active interaction, side notes, maintenance proposals.                                        |
| CyberAlchemy Method          | Route before work, gate before mutation, trace before promotion, reflection outer loop.                                   |

## Observed Invocation As Operational Evidence

Observed Invocation Loop turns each managed skill, sigil, or spell run into a safe invocation envelope.

The envelope should capture:

- capability id;
- capability kind;
- mode;
- execution status;
- outputs;
- validation;
- observer evidence;
- telemetry append status;
- reflection trigger;
- next route.

This is operational evidence. It can support claims like:

```text
this route repeatedly succeeds
this sigil repeatedly drifts from its output contract
this command lacks validation evidence
this task type needs a better context solution
```

## Workflow Reflection As Candidate Producer

Workflow Reflect reads accumulated signals and looks for:

- recurring workflow gaps;
- quality failures;
- anti-pattern hits;
- output drift;
- useful patterns;
- trend changes.

Its output is not direct ontology mutation. Its output is a proposal:

- no change;
- targeted update;
- major revision;
- retirement;
- context update;
- capability owner route;
- promotion candidate.

Operational Ontology receives those proposals as candidates.

## DomainSpec Tuning As Precedent

DomainSpec's tuning loop separates fast observation from async analysis.

The synchronous pipeline emits structured signals. Later analysis reads the JSONL signal file, checks thresholds, creates issues or reports, and proposes changes.

Signal types include:

- `step-verdict`;
- `alignment-gap`;
- `spec-gap`;
- `governance-gap`;
- `rework`;
- `overhead`;
- `decision`;
- `proposal`;
- `pattern`;
- `spec-compliance`;
- `agent-cost`.

Threshold examples:

- same governance gap appears in multiple signals;
- overhead stays high across consecutive runs;
- repeated spec gaps appear across features;
- rework appears repeatedly on the same step;
- alignment gaps accumulate;
- critical governance gap appears once.

Operational Ontology can reuse this logic for agent capability operation.

## Agent Execution Orchestrator As Execution Model

Agent Execution Orchestrator contributes a formal model for routed execution.

Key concepts:

| Concept               | Meaning                                                                                |
| --------------------- | -------------------------------------------------------------------------------------- |
| ExecutionPipeline     | Owns ordered route template and versioned capability scope.                            |
| PipelineRouteTemplate | Defines lifecycle or stage subset selection.                                           |
| ExecutionRun          | One route execution with state and stage timeline.                                     |
| StageContract         | Stage purpose, required inputs, terminal obligations, isolation mode.                  |
| StageExecution        | One execution record per selected stage with unique stage id.                          |
| TelemetryEnvelope     | Started and terminal telemetry, guard evidence, transcript excerpt, decision snapshot. |
| RunStateMachine       | Requires terminal state for every started stage run.                                   |

Operational Ontology should be able to represent these execution facts as lessons and constraints.

## First Operational Entries

| Entry                                      | Type               | Purpose                                                        |
| ------------------------------------------ | ------------------ | -------------------------------------------------------------- |
| `ontology-branch-operational-ontology`     | OntologyBranch     | Defines branch authority and scope.                            |
| `operational-lesson-route-before-work`     | OperationalLesson  | Route should be selected before artifact production.           |
| `context-solution-invoke-define-design`    | ContextSolution    | Reusable context for moving from define to design.             |
| `failure-mode-memory-treated-as-authority` | FailureMode        | Prevents session memory from becoming hidden law.              |
| `failure-mode-context-overload`            | FailureMode        | Prevents loading everything instead of task context.           |
| `maintenance-trigger-sigil-output-drift`   | MaintenanceTrigger | Repeated output mismatch routes to reflection and maintenance. |

## Operational Lesson Shape

An operational lesson should answer:

```text
what was learned?
from what evidence?
which execution context does it apply to?
which failure does it avoid?
which route or capability does it affect?
how confident are we?
when should it expire?
what would contradict it?
```

## Core Boundary

Operational Ontology should make future agents more capable, not more rigid.

It should reduce rediscovery while preserving scope:

```text
remember the lesson
name the context
show the evidence
keep the exit door visible
```
