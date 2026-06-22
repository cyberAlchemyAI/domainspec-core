# Deadline Policy

Status: frozen for MVP implementation

## Defaults

- `decision_timeout_ms`: `5000`
- `process_kill_after_ms`: `10000`
- clock: monotonic
- start: after the arena flushes the decision envelope to agent stdin
- stop: first complete stdout JSON object

## Classification

If no complete stdout JSON object arrives before `decision_timeout_ms`, the
decision is a `timeout`. The late action is ignored for gameplay and transcript
records deterministic fallback.

`process_kill_after_ms` is cleanup policy. It cannot extend the gameplay
deadline.
