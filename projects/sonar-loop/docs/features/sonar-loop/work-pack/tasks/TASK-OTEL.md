# TASK-OTEL: Telemetry Instrumentation and Verification

## Goal

Instrument stage telemetry and verify observability coverage against Sonar Loop observability contracts.

## DomainSpec Coverage

`sonar-loop.TelemetryEnvelope`, `sonar-loop.QualityTrendMapping`, `sonar-loop.CycleTelemetryEvent`, `sonar-loop.TerminalCycleSummary`, `sonar-loop.RecordCycleTelemetryTrend`, `sonar-loop.TelemetryCompletenessRule`.

## Architecture References

- Application layer emits semantic telemetry events through ports.
- Infrastructure layer owns concrete OTel/exporter adapters.
- Domain/application completion must block when telemetry completeness is unsatisfied.

## Implementation Directives

- Instrument pass stages: gate, mapping, testing, evaluating, bundling, tasking, learning, telemetry recording, and mode control.
- Add fallback fields only when runtime mode is not `sandcastle`, but validate they are complete when present.
- Emit terminal summary only when mode control authorizes completion.
- Run `domainspec-otel-verify sonar-loop` in W5 after instrumentation.

## Gaps and Questions

- Concrete OTel backend/exporter is not specified; use adapter abstraction and verify payload shape.

## Decision Lock

- D-002 keeps full governance telemetry completion before scale-fit proof.
