---
id: digest.agent_execution_orchestrator
sourceArea: domainspec
sourcePath: implementation/domainspec/docs/features/agent-execution-orchestrator/SPEC.md
status: candidate-digest
updatedAt: 2026-05-19
branches:
  - operational
  - feedback
  - capability
---

# Source Digest: Agent Execution Orchestrator

Source: [Agent Execution Orchestrator SPEC](../../../implementation/domainspec/docs/features/agent-execution-orchestrator/SPEC.md)
Ledger: [../source-ledger.md](../source-ledger.md)

## Why This Source Matters

Agent Execution Orchestrator provides a formal execution model for agent routes, stage contracts, lifecycle state, and governance telemetry.

It is the strongest existing source for turning agent execution into structured evidence.

## Compiled Concepts

### Module Ownership

The module owns deterministic composition and execution of lifecycle routes as explicit artifacts.

It covers:

- route templates;
- stage contracts;
- sandbox/worktree lifecycle;
- branch strategy;
- bounded retry;
- cancellation;
- resume;
- telemetry envelopes;
- audit readiness.

### Core Capabilities

| Capability                                      | Meaning                                                    |
| ----------------------------------------------- | ---------------------------------------------------------- |
| Explicit Pipeline Route Composition             | Define route templates before execution.                   |
| Sandcastle-Aligned Run Lifecycle                | Execute routes with provider-agnostic lifecycle semantics. |
| Policy-Governed Branch And Cancellation Control | Apply branch, retry, and cancellation policies.            |
| Governance Telemetry And Signal Emission        | Emit telemetry envelopes and governance signals.           |

### Domain Concepts

| Concept               | Meaning                                                                |
| --------------------- | ---------------------------------------------------------------------- |
| ExecutionPipeline     | Ordered route template and versioned capability scope.                 |
| PipelineRouteTemplate | Full lifecycle or ordered stage subset selection.                      |
| ExecutionRun          | One route execution with state and ordered stages.                     |
| StageContract         | Stage purpose, inputs, terminal obligations, isolation mode.           |
| StageExecution        | One execution record per selected stage.                               |
| TelemetryEnvelope     | Telemetry pair, guard evidence, transcript excerpt, decision snapshot. |
| RunStateMachine       | Requires terminal state for every started stage.                       |

### Execution Graph

The source models execution as:

```text
route template
  -> stage contract
  -> execution run
  -> stage execution
  -> terminal outcome
  -> telemetry envelope
  -> governance signal
```

This is directly useful for CyberAlchemy's Operational Ontology.

## CyberAlchemy Adaptation

Operational Ontology should represent execution evidence using this shape:

- route selected;
- stage or capability owner;
- terminal obligation;
- execution status;
- validation result;
- telemetry envelope;
- next route.

Context solution cards should be able to reference route templates or stage contracts when available.

## Candidate Ontology Claims

| Claim                                                                               | Branch      | Candidate Entry                           |
| ----------------------------------------------------------------------------------- | ----------- | ----------------------------------------- |
| Agent execution should be represented as explicit route artifacts.                  | operational | `concept-explicit-route-artifact`         |
| Stage contracts should define purpose, inputs, terminal obligations, and isolation. | operational | `concept-stage-contract`                  |
| Every started execution stage should have a terminal outcome.                       | feedback    | `rule-terminal-outcome-required`          |
| Telemetry envelopes connect execution to governance signals.                        | feedback    | `concept-telemetry-envelope`              |
| Route execution evidence can feed operational lessons.                              | operational | `edge-execution-feeds-operational-lesson` |

## Tensions And Promotion Gaps

- The source is DomainSpec-specific; CyberAlchemy should generalize without importing every implementation detail.
- The first ontology loop can start with manual telemetry, but future execution should use deterministic envelopes.
- Stage model may be too heavy for small tasks; route policy should preserve proportionality.

## Agent Payload

Before executing a routed task, ask:

```text
what route owns this?
what are the stage obligations?
what terminal outcome will be recorded?
what telemetry or evidence proves the result?
what future ontology or capability lesson could this feed?
```
