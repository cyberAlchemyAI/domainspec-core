# State Namespaces

Status: frozen for MVP implementation

## Live Agent Namespace

Allowed:

- protocol version,
- match id,
- hand id,
- decision id,
- seat id,
- deadline,
- public betting state,
- own private card,
- legal actions.

Forbidden:

- raw seed,
- deck order,
- opponent private card,
- future state,
- referee trace,
- hidden-state hash.

## Private Referee Namespace

Allowed:

- raw seed,
- deck order,
- all private cards,
- full state transition trace,
- accepted and fallback actions,
- payouts,
- diagnostics.

## Public Replay Namespace

Allowed:

- seed handle,
- public betting history,
- actions and fallback events,
- payouts,
- shown-down cards only,
- diagnostics summary.

Forbidden:

- raw seed,
- deck order,
- unrevealed folded cards,
- future state,
- referee trace,
- hidden-state hash.
