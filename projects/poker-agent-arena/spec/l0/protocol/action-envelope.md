# Action Envelope

Status: frozen for MVP implementation

The agent writes exactly one JSON action envelope.

## Required Shape

```json
{
  "protocol_version": "paa.l0.v1",
  "decision_id": "hand-0001:d0:s0",
  "action": {"type": "check"}
}
```

For wager actions in Local Arena CLI v0:

```json
{
  "protocol_version": "paa.l0.v1",
  "decision_id": "hand-0001:d0:s0",
  "action": {"type": "bet", "amount": 1}
}
```

Optional metadata is ignored for gameplay.

## Invalid Cases

- malformed JSON,
- prose before JSON,
- extra JSON object after the first action object,
- mismatched `decision_id`,
- missing `action`,
- unavailable action type,
- amount outside current legal bounds.
