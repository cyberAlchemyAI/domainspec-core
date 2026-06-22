# Agent Protocol Receipt

dispatch_id: 2026-06-19-poker-agent-arena-mechanics
role_id: agent-protocol
agent_id: Shannon
spawn_status: spawned
join_status: completed
close_status: closed
status: pass

## Proposed Protocol

Use a line-delimited JSON CLI protocol as the MVP. The arena starts one process per agent seat, writes exactly one JSON message per line to stdin, and reads exactly one JSON object per decision from stdout. Stderr is reserved for agent logs and must never affect gameplay. This gives Claude/Hermes/Codex-style agents a simple contract and leaves a clean path to WebSocket by mapping each stdin/stdout line to a socket message.

Protocol envelope:

```json
{
  "protocol_version": "poker-agent-arena.v0",
  "type": "decision",
  "match_id": "m-001",
  "hand_id": "h-000042",
  "decision_id": "h-000042:s2:a7",
  "seat_id": "seat-2",
  "deadline_ms": 750,
  "observation": {},
  "legal_actions": []
}
```

Observation schema should be public-plus-own-private only:

```json
{
  "game": "kuhn|leduc|holdem_nlhe",
  "street": "preflop|flop|turn|river|showdown",
  "button_seat": "seat-0",
  "acting_seat": "seat-2",
  "hero_seat": "seat-2",
  "hero_cards": ["As", "Kd"],
  "board": ["2c", "7h", "Jh"],
  "pot": 620,
  "side_pots": [{"amount": 240, "eligible_seats": ["seat-0", "seat-2"]}],
  "stacks": {"seat-0": 880, "seat-1": 0, "seat-2": 1420},
  "committed": {"seat-0": 120, "seat-1": 500, "seat-2": 120},
  "to_call": 80,
  "min_raise_to": 240,
  "action_history": [
    {"street": "preflop", "seat": "seat-0", "kind": "bet", "amount": 120}
  ],
  "public_seat_state": {
    "seat-1": {"status": "all_in"},
    "seat-2": {"status": "active"}
  }
}
```

Forbidden observation fields: deck order, random seed, future board cards, other live players' private cards, mucked cards before public showdown rules reveal them, engine evaluation internals, opponent model hints, and any hidden tournament assignment metadata.

Legal actions must be sent as authoritative objects, not inferred by the agent:

```json
[
  {"kind": "fold"},
  {"kind": "call", "amount": 80},
  {"kind": "check"},
  {"kind": "raise", "min_to": 240, "max_to": 1500, "step": 1},
  {"kind": "all_in", "amount": 1500}
]
```

Agent stdout response:

```json
{
  "type": "action",
  "protocol_version": "poker-agent-arena.v0",
  "decision_id": "h-000042:s2:a7",
  "action": {"kind": "raise", "amount": 360},
  "meta": {"client_elapsed_ms": 214, "note": "optional"}
}
```

The engine validates only the envelope, decision_id, and action legality. Free-form metadata is ignored for scoring except logs and later analysis. Agents must not emit prose on stdout. If multiple JSON objects arrive for one decision, use the first complete object and log the rest as protocol noise.

Deadline behavior: `deadline_ms` is measured from the engine write flush to first complete stdout JSON object. The default MVP should use a short per-action clock plus a small process-level grace window for IO jitter. If the deadline expires, apply the configured timeout fallback. Recommended fallback order: check if legal, otherwise fold if legal, otherwise lowest-cost legal action. Timeout and invalid-output penalties belong to scoring, but the hand must remain deterministic.

Invalid output handling: malformed JSON, missing decision_id, mismatched decision_id, unknown action kind, illegal amount, or stdout prose before JSON all count as invalid output. The engine should choose the deterministic fallback action, append an invalid-output event to the match log, and continue unless the agent exceeds a configurable strike limit. Repeated invalid output should retire the process for the match and mark future decisions as fallback actions.

Process lifecycle: start process, send `hello`, require `ready`, stream `decision` messages, optionally send `hand_result` and `match_result`, then send `shutdown`. On crash, EOF, or nonzero exit before shutdown, record process_exit and use fallback actions for unresolved decisions. The arena should support cold-start-per-match first; warm process reuse can come later after reproducibility checks pass.

Logs and reproducibility: stdout is protocol only. Stderr can be captured as opaque agent logs with timestamps, byte caps, and redaction of environment variables. Match logs should include protocol_version, engine_version, ruleset_id, deck_seed_commitment or seed handle, agent package digest, CLI argv, environment allowlist, decision messages, action responses, fallback decisions, elapsed_ms, and final payouts. Replay must be possible from engine version, ruleset, seeds, and recorded legal-action lists without reading agent logs.

WebSocket compatibility: keep the same envelope and schemas. Replace stdin lines with inbound server messages and stdout responses with outbound client messages. Add connection_id/session_id, ping/pong, and reconnect policy later, but do not change decision_id, deadline_ms, legal_actions, or hidden-information rules.

## Toy-Game Checks Needed

- Kuhn poker hidden-info fixture: each agent sees only its own card, public betting history, pot, stacks, and legal actions.
- Leduc fixture: verify private card plus public board transition without leaking deck order or unrevealed cards.
- Timing fixture: one agent sleeps past deadline; engine applies deterministic fallback and logs timeout.
- Invalid-output fixture: malformed JSON, illegal raise amount, and mismatched decision_id all map to fallback actions.
- All-in and side-pot fixture: legal_actions carry max_to/all_in precisely and replay reproduces payouts.
- WebSocket parity fixture later: same decision envelope over socket yields the same accepted action and logs.

## Risks, Blockers, Residue

No blocker for a CLI-first MVP. Main risks are clock nondeterminism, accidental hidden-state leakage through rich logs or action histories, agent stdout contamination, and schema drift between CLI and later WebSocket transport. Residue: choose exact strike limits, default per-action deadlines, log retention/redaction policy, and whether seed commitments or raw seeds are visible in public match artifacts.

## Handoff Note

Parent synthesis can treat this as a protocol baseline, not an implementation proof. Next owner should turn the schemas above into fixtures and validators, then require every mechanics lane to consume engine-provided `legal_actions` rather than deriving legality from private engine state.
