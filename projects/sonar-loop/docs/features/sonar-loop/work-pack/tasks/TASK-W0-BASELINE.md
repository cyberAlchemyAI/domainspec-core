# TASK-W0-BASELINE: Architecture and Governance Baseline

## Goal

Lock dependency-direction, module-boundary, decision, and validation obligations before implementation begins.

## DomainSpec Coverage

`sonar-loop.ProgressiveQualityLoopWorkflow`, `sonar-loop.CycleStateMachine`, `sonar-loop.ExecutionCycle`, `sonar-loop.TelemetryCompletenessRule`, `sonar-loop.QualityTrendMapping`.

## Architecture References

- `implementation/domainspec/architecture/ARCHITECTURE.md`
- `implementation/domainspec/architecture/pattern-library/ARCHITECTURE-FOUNDATIONS.md`
- `implementation/domainspec/architecture/pattern-library/LAYERING-REFERENCE.md`
- `implementation/domainspec/architecture/pattern-library/DEPENDENCY-RULES.md`
- `projects/sonar-loop/docs/features/sonar-loop/architecture.md`

## Implementation Directives

- Do not mutate source implementation until W0 exits.
- Select source module paths for domain, application, infrastructure, and interface layers during execution.
- Establish dependency-direction verification before W1.
- Validate markdown links for all work-pack files one file at a time.

## Gaps and Questions

- Concrete source tree paths are not specified in feature docs.
- Execution must record chosen implementation paths before source mutation.

## Decision Lock

- D-001 and D-002 are selected in [../shared/03-cross-task-decisions.md](../shared/03-cross-task-decisions.md).
