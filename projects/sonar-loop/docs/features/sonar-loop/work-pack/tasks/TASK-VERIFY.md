# TASK-VERIFY: Feature Verification Closure

## Goal

Run the final DomainSpec verification and readiness checks for Sonar Loop.

## DomainSpec Coverage

All coverage families in [../shared/04-traceability.md](../shared/04-traceability.md), with special attention to `sonar-loop.ProgressiveQualityLoopWorkflow`, `sonar-loop.CycleStateMachine`, `sonar-loop.TelemetryCompletenessRule`, and all four capability docs.

## Architecture References

- Verification must include semantic behavior and architecture boundary evidence.
- DomainSpec docs remain source of truth over execution convenience.

## Implementation Directives

- Run `domainspec-verify-feature sonar-loop` after W1-W4 mutation-capable stages.
- Run readiness profile `pilot` unless the work-pack is explicitly promoted.
- Convert BLOCK/FLAG findings into ordered remediation tasks without deleting seeded closure obligations.

## Gaps and Questions

- Exact generated verification artifact paths are produced by the verification command.

## Decision Lock

- D-001 and D-002 must be reflected in the verification narrative.
