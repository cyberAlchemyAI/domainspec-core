# Public Replay

Status: frozen for MVP implementation

Public replay is a redacted export for sharing and debugging. It is not the
private replay authority.

## Required Content

- match id,
- fixture id,
- seed handles,
- public betting history,
- accepted legal actions,
- fallback events,
- shown-down cards only when the hand reaches showdown,
- payouts,
- diagnostics summary.

## Forbidden Content

Public replay must not include raw seed material, deck order, hidden-state hash,
future state, folded unrevealed private cards, referee trace, or environment
paths.
