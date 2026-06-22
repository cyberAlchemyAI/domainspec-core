# Local Arena CLI v0 Match Config

Status: frozen for MVP implementation

## Required Fields

```json
{
  "fixture_id": "kuhn_hidden_info",
  "agents": {
    "agent_a": "projects/poker-agent-arena/examples/agents/check_call.py",
    "agent_b": "projects/poker-agent-arena/examples/agents/legal_random.py"
  },
  "seat_rotation": true,
  "seed_handles": ["kuhn-smoke-000"],
  "decision_timeout_ms": 5000,
  "process_kill_after_ms": 10000,
  "out_dir": "projects/poker-agent-arena/.tmp/smoke"
}
```

## Rules

- `fixture_id` must be `kuhn_hidden_info` in Local Arena CLI v0.
- `agents` must name exactly `agent_a` and `agent_b`.
- A path ending in `.py` is executed with the active Python interpreter.
- `seat_rotation=true` swaps agent-to-seat assignment over the smoke orbit.
- `seed_handles` are public opaque handles. Raw seed material is referee-only.
- `decision_timeout_ms` is the action acceptance deadline.
- `process_kill_after_ms` is cleanup policy only; late actions are never accepted
  after `decision_timeout_ms`.
- `out_dir` owns all command output for the run.
