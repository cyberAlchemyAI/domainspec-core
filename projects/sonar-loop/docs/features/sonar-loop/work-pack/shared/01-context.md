# Shared Context

## Scope

Sonar Loop owns a governed progressive quality loop for TypeScript repositories. The implementation plan follows the POC-first layer model in [../../implementation-layering.md](../../implementation-layering.md): L0 proves one local actionable pass, L1 adds deterministic repeatability, L2 hardens degraded governance paths, and L3 validates pilot/scale fit.

## Authoritative Feature Sources

| Source                                                               | Planning Use                                                                   |
| -------------------------------------------------------------------- | ------------------------------------------------------------------------------ |
| [../../SPEC.md](../../SPEC.md)                                       | Capability map, concept registry, and feature graph                            |
| [../../architecture.md](../../architecture.md)                       | Consumer architecture, flow, runtime fallback, and completion governance       |
| [../../implementation-layering.md](../../implementation-layering.md) | Layer and wave backbone                                                        |
| [../../domain.md](../../domain.md)                                   | Entity, value object, and enum contracts                                       |
| [../../operations.md](../../operations.md)                           | Mutation operations and state transitions                                      |
| [../../rules.md](../../rules.md)                                     | Policies, state machine, and invariants                                        |
| [../../interfaces.md](../../interfaces.md)                           | Runtime, Sonar, GitHub, Jira, mode-control, override, and telemetry boundaries |
| [../../observability.md](../../observability.md)                     | Telemetry events, metrics, alerts, and evidence checklist                      |
| [../../STORIES.md](../../STORIES.md)                                 | Story and acceptance traceability                                              |
| [../../glossary.md](../../glossary.md)                               | Feature language and source-linked definitions                                 |

## Architecture Baseline

Implementation must preserve these constraints from DomainSpec architecture:

| Constraint            | Directive                                                                                                                           |
| --------------------- | ----------------------------------------------------------------------------------------------------------------------------------- |
| Domain-first          | Domain types, policies, state machines, rules, and calculations are pure and framework-free.                                        |
| Dependency direction  | Domain imports no outer layers; application imports domain only; infrastructure implements ports; interfaces call application APIs. |
| Functional TypeScript | Prefer types/interfaces plus pure functions and factories over classes.                                                             |
| Encapsulation         | Export only module public APIs and keep helpers file-local.                                                                         |
| Boundary checks       | Use static checks or architecture tests to fail invalid import graphs before merge.                                                 |

## Mutation-Capable Stages

The plan includes mutation-capable backend/runtime implementation and OTel instrumentation. Closure therefore requires verification plus alignment and layering audits.

## Non-Mutation Skips

UI pipeline is skipped because no user-facing UI contract or `UI-SPEC.md` exists. Infra deployment is skipped because concrete deployment topology is an explicit non-goal in [../../architecture.md](../../architecture.md).
