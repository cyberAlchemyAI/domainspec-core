# Local Arena CLI v0 Output Layout

Status: frozen for MVP implementation

Each `run`, `eval`, or `replay` command writes into the supplied output
directory.

## `run` And `eval`

```text
<out>/
  private-transcript.jsonl
  diagnostics-report.json
  summary.json
```

## `replay`

```text
<out>/
  replay-report.json
  public-replay.json
  diagnostics-report.json
```

Private transcript files may contain referee-only material. Public replay files
must follow `spec/l0/transcript/redaction-policy.md`.
