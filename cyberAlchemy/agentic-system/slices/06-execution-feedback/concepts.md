---
module: cyberalchemy-agentic-system
slice: 06-execution-feedback
status: candidate
updatedAt: 2026-05-19
docType: slice-concepts
---

# Concepts: Execution Feedback

Work: [README.md](README.md)

## What This Slice Compiles

This slice gathers execution and feedback content from:

- Agent Execution Orchestrator;
- Observed Invocation Loop;
- Workflow Reflect;
- DomainSpec Observability;
- DomainSpec Tuning Loop;
- Drift-Convergence;
- Arcanum capability lifecycle.

Execution is not the end of the system. Execution produces evidence for the next loop.

## Routed Execution

CyberAlchemy execution should happen through an owner:

- skill;
- sigil;
- spell;
- invoke lifecycle route;
- task-session;
- ontology-harness;
- decision-gate;
- agent execution route.

The owner matters because it defines:

- purpose;
- input contract;
- output contract;
- quality bar;
- validation;
- failure behavior;
- observability;
- maintenance route.

## Agent Execution Orchestrator

Agent Execution Orchestrator formalizes execution as explicit route artifacts, not only dynamic agent decisions.

It owns:

- deterministic pipeline route composition;
- run lifecycle semantics;
- branch and cancellation policy;
- governance telemetry and signal emission;
- verification and audit readiness.

Core concepts:

| Concept               | Meaning                                                                   |
| --------------------- | ------------------------------------------------------------------------- |
| ExecutionPipeline     | Ordered route template and versioned capability scope.                    |
| PipelineRouteTemplate | Lifecycle route or stage subset selection.                                |
| ExecutionRun          | One route execution with state and stage timeline.                        |
| StageContract         | Purpose, required inputs, terminal obligations, isolation mode.           |
| StageExecution        | One selected stage with unique stage id and terminal outcome.             |
| TelemetryEnvelope     | Started and terminal telemetry with guard evidence and decision snapshot. |
| RunStateMachine       | Ensures every started stage reaches terminal state.                       |

This provides a strong model for CyberAlchemy agentic execution:

```text
route artifact
  -> stage contract
  -> execution run
  -> terminal outcome
  -> telemetry envelope
  -> signal
  -> reflection
```

## Execution Evidence

A useful execution leaves more than a changed file.

It should leave:

- route selected;
- route rationale;
- input context;
- stage or task owner;
- output artifact;
- validation result;
- terminal outcome;
- gaps;
- telemetry id;
- next route.

Without this evidence, the system can complete a task but cannot learn from it.

## Observed Invocation Loop

Observed Invocation Loop wraps Arcanum-managed invocations with observability.

Its phases:

| Phase    | Responsibility                                                    |
| -------- | ----------------------------------------------------------------- |
| start    | Resolve capability id, kind, tier, mode, request summary, run id. |
| execute  | Run the target capability while preserving primary result.        |
| envelope | Assemble privacy-safe invocation metadata.                        |
| observe  | Append telemetry through signal observer.                         |
| reflect  | Run reflection if threshold or manual route requires it.          |
| closeout | Return primary result plus telemetry status.                      |

Important gates:

- managed invocation;
- envelope validity;
- telemetry append;
- threshold evaluation;
- reflection route;
- hook enforcement.

The key rule is that telemetry should not depend only on the agent remembering to write a summary. Hooks, wrappers, or deterministic command surfaces should perform the observation handoff wherever possible.

## DomainSpec Observability

DomainSpec's observability pipeline maps documentation to metrics.

It separates three metric layers:

| Layer                  | Question                                 | Derived From                     | Consumer         |
| ---------------------- | ---------------------------------------- | -------------------------------- | ---------------- |
| Domain Fidelity        | Does production behavior match the spec? | states, operations, events       | Engineering      |
| Operational Health     | Is the system reliable and performant?   | interfaces, queries, workflows   | Platform/SRE     |
| Business Effectiveness | Is the feature achieving its goal?       | SPEC capabilities, user journeys | Product/business |

Examples of deterministic metric derivation:

- every state transition produces a transition counter;
- invalid transitions produce domain fidelity violations;
- every invariant produces a runtime assertion metric;
- every operation produces execution, success, failure, and duration metrics;
- every rule produces a violation counter;
- every calculation can produce a drift monitor.

The lesson for CyberAlchemy: observability should derive from the governing model, not appear as an afterthought.

## Drift And Convergence

Execution feedback is meaningful because it can be compared to intent.

Drift:

```text
measurable divergence between intended behavior and observed reality
```

Convergence:

```text
evidence-backed reduction of critical drift over time
```

Execution feedback should make drift visible on:

- build-time fidelity;
- runtime fidelity;
- governance and meta-health;
- async learning and framework tuning;
- implementation closure.

## DomainSpec Tuning Loop

DomainSpec's tuning loop is a model for self-improvement.

It separates:

- fast observation during a pipeline run;
- async analysis across runs.

The loop:

```text
pipeline run
  -> emit signals
  -> append JSONL
  -> analyze thresholds
  -> create issue or report
  -> reflect
  -> propose framework changes
  -> human review
  -> update skill, agent, template, or governance
  -> next run benefits
```

This gives CyberAlchemy a precedent for Operational Ontology:

```text
agent run
  -> telemetry
  -> reflection
  -> operational lesson candidate
  -> promotion gate
  -> capability or context update
```

## Workflow Reflect

Workflow Reflect interprets accumulated telemetry.

It detects:

- recurring workflow gaps;
- quality failures;
- anti-pattern hits;
- output drift;
- useful patterns;
- trend changes.

It outputs:

- signal summary;
- thresholds triggered;
- repeated patterns;
- gap analysis;
- proposed iterations;
- rejected changes;
- contract preservation notes;
- recommended next lifecycle step.

Reflection proposes. Promotion decides. Maintenance mutates only when the owning lifecycle route approves.

## Signal To Ontology Flow

Execution feedback should move into ontology like this:

```text
execution run
  -> telemetry envelope
  -> signal
  -> reflection report
  -> operational lesson candidate
  -> inventory evidence
  -> ontology candidate
  -> promotion review
  -> context or capability update
```

## First Feedback Entries

| Entry                                     | Type                | Purpose                                                        |
| ----------------------------------------- | ------------------- | -------------------------------------------------------------- |
| `feedback-loop-observed-invocation`       | CapabilityPattern   | Managed invocations produce telemetry and reflection triggers. |
| `feedback-loop-workflow-reflection`       | CapabilityPattern   | Accumulated signals produce maintenance proposals.             |
| `signal-route-miss`                       | ObservabilitySignal | Repeated bad routing creates operational learning pressure.    |
| `signal-output-drift`                     | ObservabilitySignal | Capability output diverges from contract.                      |
| `maintenance-trigger-sigil-output-drift`  | MaintenanceTrigger  | Repeated output drift routes to sigil maintenance.             |
| `failure-mode-execution-without-evidence` | FailureMode         | Work completed without trace cannot teach the system.          |

## Core Rule

Execution is only part of the loop when it leaves evidence.

```text
artifact without evidence completes a task
artifact with evidence improves the system
```
