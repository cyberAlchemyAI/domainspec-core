# Diagnostics Report Schema

Status: frozen for MVP implementation

`diagnostics-report.json` must include:

```json
{
  "protocol_version": "paa.l0.v1",
  "fixture_id": "kuhn_hidden_info",
  "hands": 12,
  "agents": {
    "agent_a": {
      "clean_ev": 0.0,
      "fallback_inclusive_ev": 0.0,
      "invalid_rate": 0.0,
      "timeout_rate": 0.0,
      "fallback_count": 0
    }
  },
  "replay_determinism": true,
  "hidden_info_canary_pass": true,
  "public_replay_redaction_pass": true
}
```

Rates are per decision. EV is net chips over completed hands.
