# TASK-TESTS: DomainSpec-Derived Tests

## Goal

Generate and execute tests that prove Sonar Loop contracts across L0-L3 and closure.

## DomainSpec Coverage

All capability coverage families in [../shared/04-traceability.md](../shared/04-traceability.md), especially `sonar-loop.CycleStateMachine`, `sonar-loop.TestScopePolicy`, `sonar-loop.SonarRetryPolicy`, `sonar-loop.ExecutionProviderFallbackPolicy`, `sonar-loop.ApiFirstTaskIntegrationPolicy`, `sonar-loop.CompletionGateUnderExportDegradationPolicy`, `sonar-loop.RiskAcceptanceOverrideValidityPolicy`, and `sonar-loop.TelemetryCompletenessRule`.

## Architecture References

- Unit tests target pure domain rules and calculations.
- Application tests target use-case orchestration and state transitions.
- Integration tests target adapters through ports.
- Functional tests prove the progressive workflow.

## Implementation Directives

- Generate tests from DomainSpec artifacts with `domainspec-generate-tests sonar-loop`.
- Cover mandatory integration, e2e, and functional test evidence before Sonar evaluation.
- Include negative tests for missing fallback evidence, invalid override, invalid export transition, and incomplete telemetry.
- Add dependency-boundary tests or static checks before W5 closure.

## Gaps and Questions

- Exact package test command is implementation-workspace dependent and must be recorded during W0/W1 execution.

## Decision Lock

- D-001 affects L0 test expectations: local task output is enough for W1.
- D-002 affects W3/W4 test sequencing: governance tests must pass before scale-fit tests.
