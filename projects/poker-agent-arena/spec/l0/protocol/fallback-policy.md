# Fallback Policy

Status: frozen for MVP implementation

Fallback keeps evaluation moving when an agent fails the protocol. It must be
deterministic, legal, and competitively poor.

## Selector

Choose the first currently legal action in this order:

1. `check`
2. `fold`
3. `call`
4. minimum legal wager action by the referee-defined order

For Local Arena CLI v0 Kuhn, the only wager action is `bet` with `amount=1`.

## Transcript

Every fallback event records:

- event code,
- original invalid or timeout reason,
- fallback action,
- decision id,
- seat id,
- elapsed time when available.
