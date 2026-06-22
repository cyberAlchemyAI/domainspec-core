# Legal Actions

Status: frozen for MVP implementation

The current `legal_actions` list is authoritative. The agent may choose only one
listed action.

## Kuhn Action Set

- `check`
- `bet` with `amount=1`
- `call`
- `fold`

`bet` is legal only when the current state allows opening the betting round.
`call` and `fold` are legal only facing a bet.

## Amount Rules

If a legal action has `min_amount` and `max_amount`, the submitted `amount` must
be inside the inclusive bounds. Local Arena CLI v0 Kuhn uses only `amount=1`.
