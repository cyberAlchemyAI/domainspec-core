# MARS Telemetry Schema

Append-only run signals for MARS orchestration.

## Envelope

- id
- timestamp
- project_id
- experiment_id
- run_id
- stage
- type
- severity
- data

## Required Types

- stage-verdict
- gate-decision
- dependency-check
- evidence-update
- retrospective

## Invariants

1. every run emits one gate-decision per applicable gate
2. blocked gates include remediation details
3. evidence-update references a claim ID and source result file
