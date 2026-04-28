# MARS Telemetry Signal Schema Template

Purpose: define a reusable telemetry contract for MARS research projects.

Target artifact:

- `research/projects/<project-key>/telemetry/SIGNAL-SCHEMA.md`

Append-only signal log:

- `research/projects/<project-key>/telemetry/signals.jsonl`

## Envelope

Required top-level fields:

- `id`
- `timestamp`
- `session`
- `project_id`
- `source`
- `type`
- `severity`
- `category`
- `stage`
- `data`

Optional when applicable:

- `experiment_id`
- `run_id`

## Categories

- `execution`
- `governance`
- `evidence`
- `discovery`
- `pattern`
- `operations`

## Core Signal Families

- `stage-verdict`
- `gate-decision`
- `workflow-gap`
- `contract-gap`
- `evidence-gap`
- `decision-friction`
- `rework`
- `overhead`
- `proposal`
- `pattern`
- `evidence-update`
- `retrospective`

## Reflection-Oriented Threshold Candidates

- repeated `workflow-gap` for same missing command or handoff
- repeated `contract-gap` for same artifact class
- repeated `decision-friction` for same unresolved decision type
- repeated gate BLOCK on same gate class
- repeated `evidence-gap` for same closure stage
- sustained high `overhead`
- clustered `proposal` signals on same target file

## Invariants

1. If any `stage-verdict` exists, emit exactly one `overhead` signal for the same session.
2. Every applicable gate emits one `gate-decision` signal.
3. Blocked workflow/contract/evidence gaps include remediation details and the missing control point.
4. `evidence-update` references claim ID and source artifact path.
5. Signal logs are append-only.
