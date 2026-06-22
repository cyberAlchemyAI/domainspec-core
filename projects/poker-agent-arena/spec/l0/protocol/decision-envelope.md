# Decision Envelope

Status: frozen for MVP implementation

The arena sends exactly one JSON decision envelope per acting decision.

## Required Shape

```json
{
  "protocol_version": "paa.l0.v1",
  "type": "decision",
  "match_id": "match-0001",
  "hand_id": "hand-0001",
  "decision_id": "hand-0001:d0:s0",
  "seat_id": "seat_0",
  "deadline_ms": 5000,
  "observation": {
    "fixture_id": "kuhn_hidden_info",
    "seat_id": "seat_0",
    "own_card": "K",
    "public_state": {
      "pot": 2,
      "betting_history": [],
      "to_act": "seat_0"
    }
  },
  "legal_actions": [
    {"type": "check"},
    {"type": "bet", "min_amount": 1, "max_amount": 1}
  ]
}
```

## Forbidden Live Fields

Decision envelopes must not contain:

- opponent private card,
- deck order,
- raw seed,
- future state,
- referee trace,
- engine internals,
- hidden assignment metadata,
- reversible hidden-state hash.
