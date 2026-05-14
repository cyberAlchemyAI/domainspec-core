# TASK-AUDIT-LAYERING: Layering Alignment Audit

## Goal

Audit implementation layering, dependency direction, and boundary placement against DomainSpec architecture and Sonar Loop feature architecture.

## DomainSpec Coverage

`sonar-loop.CycleStateMachine`, `sonar-loop.ExecutionProviderFallbackPolicy`, `sonar-loop.ApiFirstTaskIntegrationPolicy`, `sonar-loop.CompletionGateUnderExportDegradationPolicy`, `sonar-loop.TelemetryCompletenessRule`, plus all mutation-capable operations.

## Architecture References

- `implementation/domainspec/architecture/pattern-library/ARCHITECTURE-FOUNDATIONS.md`
- `implementation/domainspec/architecture/pattern-library/LAYERING-REFERENCE.md`
- `implementation/domainspec/architecture/pattern-library/DEPENDENCY-RULES.md`
- `projects/sonar-loop/docs/features/sonar-loop/architecture.md`

## Implementation Directives

- Run `domainspec-audit-layering sonar-loop` after W1-W4 mutation-capable stages.
- Block closure on inner-layer imports from outer-layer implementation code.
- Require adapter placement for Sonar, runtime, GitHub, Jira, override registry, and telemetry exporters.
- Merge findings with semantic alignment findings into a single remediation order.

## Gaps and Questions

- Exact static import-boundary command depends on the selected implementation workspace.

## Decision Lock

- D-002 keeps scale-fit work downstream of governance-layer evidence.
