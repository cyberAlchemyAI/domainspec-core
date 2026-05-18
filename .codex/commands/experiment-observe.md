# experiment-observe

Append one signal-observer-compatible telemetry event for an experiment harness report.

## Usage

```bash
arcanum/arcana/experiment-harness/scripts/observe-harness.sh <artifact-path> [report-path]
```

The command writes to `.arcanum/observability/signals/sigil-invocations.jsonl` when the repository observability package exists. Telemetry failures should not change the primary experiment result.
