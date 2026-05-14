# TASK-L0-POC: Layer 0 Governed Pass

## Goal

Implement the minimum working unit: one governed pass from target gate selection through local remediation task output and checkpoint evidence.

## DomainSpec Coverage

`sonar-loop.ExecutionCycle`, `sonar-loop.QualityGateProfile`, `sonar-loop.CodebaseKnowledgeMap`, `sonar-loop.FindingBundle`, `sonar-loop.RemediationTask`, `sonar-loop.CheckpointControl`, `sonar-loop.TelemetryEnvelope`, `sonar-loop.DetermineTargetQualityGate`, `sonar-loop.MapCodebaseIntelligence`, `sonar-loop.BuildAndImproveTestEvidence`, `sonar-loop.EvaluateWithSonarQualityGate`, `sonar-loop.BundleFindingsByContext`, `sonar-loop.CreateAndExportRemediationTasks`, `sonar-loop.RecordCycleTelemetryTrend`, `sonar-loop.ApplyModeControlCheckpoint`, `sonar-loop.CycleStateMachine`, `sonar-loop.TestScopePolicy`, `sonar-loop.TelemetryCompletenessRule`.

## Architecture References

- Domain layer: entities, values, enums, rules, policies, state machine.
- Application layer: operations/use-cases and workflow orchestration.
- Infrastructure layer: local persistence, Sonar/runtime gateways behind ports.
- Interface layer: public module or CLI/API boundary calling application functions.

## Implementation Directives

- Implement domain rules and state transitions as pure TypeScript functions.
- Implement application use-cases for gate selection, mapping, evidence collection, Sonar evaluation, finding bundling, local task creation, telemetry recording, and checkpoint control.
- Keep Sonar/runtime IO and local persistence behind ports/adapters.
- Enforce D-001: L0 produces local repository task output only; do not require GitHub/Jira export.

## Gaps and Questions

- Sonar project key and runtime credentials are execution-time adapter configuration, not domain constants.
- Existing implementation location must be confirmed by W0 before mutation.

## Decision Lock

- D-001: local repository task only for L0.
- D-002: L2 and L3 remain separate; do not pull degraded-path governance into L0.
