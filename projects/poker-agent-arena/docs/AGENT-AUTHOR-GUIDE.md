# Agent Author Guide

This guide is for people preparing agents or validators for Local Arena CLI v0.
It does not replace [AGENT-RULES.md](../AGENT-RULES.md) or the versioned
contracts under [`spec/l0/`](../spec/l0/); it gives you the runnable shape of
the seat.

## Mental Model

Your agent is not the referee. It does not own game state, legal actions, payout logic, or hidden information. It receives a filtered decision envelope, chooses one legal action, and returns an action envelope before the deadline.

That is the whole job. It is a small box, which is how the interesting parts stay visible.

## Expected Loop

```text
read one decision envelope
verify protocol version and decision id
inspect observation and legal actions
choose one legal action
write one action envelope
flush stdout
wait for the next decision
```

The first complete stdout JSON object is the gameplay candidate. Anything around it may become a diagnostic liability.

## Quickstart

From the repository root:

```sh
PYTHONPATH=projects/poker-agent-arena/src python3 -m poker_agent_arena.cli doctor
PYTHONPATH=projects/poker-agent-arena/src python3 -m poker_agent_arena.cli eval --fixture kuhn_hidden_info --agent-a projects/poker-agent-arena/examples/agents/check_call.py --agent-b projects/poker-agent-arena/examples/agents/legal_random.py --out projects/poker-agent-arena/.tmp/smoke
PYTHONPATH=projects/poker-agent-arena/src python3 -m poker_agent_arena.cli replay projects/poker-agent-arena/.tmp/smoke/private-transcript.jsonl --out projects/poker-agent-arena/.tmp/smoke/replay
```

Expected outputs:

- `private-transcript.jsonl`: referee-owned replay authority.
- `diagnostics-report.json`: clean EV, fallback-inclusive EV, invalid rate,
  timeout rate, fallback count, canary status, and replay determinism.
- `public-replay.json`: redacted replay export with seed handles, not raw seed
  material.

## Decision Envelope Shape

The exact schema is versioned under [`spec/l0/protocol/decision-envelope.md`](../spec/l0/protocol/decision-envelope.md).
Required fields are:

- `protocol_version`
- `type`
- `match_id`
- `hand_id`
- `decision_id`
- `seat_id`
- `deadline_ms`
- `observation`
- `legal_actions`

The envelope must not include raw seed material, deck order, future cards, live opponent private cards, referee traces, engine internals, hidden assignment metadata, or reversible hidden-state hashes.

## Action Envelope Shape

The exact schema is versioned under [`spec/l0/protocol/action-envelope.md`](../spec/l0/protocol/action-envelope.md).
The runtime expects:

- `protocol_version`
- `decision_id`
- `action`

Optional metadata may exist, but gameplay must not depend on it. If an agent needs a long diary entry to make a legal action legible, the diary should stay out of the protocol.

## Reliability Priorities

Build for:

- valid JSON,
- one action per decision,
- matching `decision_id`,
- legal actions only,
- deadline discipline,
- deterministic behavior under fixture seeds,
- no hidden-information assumptions.

Avoid:

- stdout chatter before JSON,
- extra decision objects,
- attempting unavailable actions,
- embedding reasoning traces that can leak private assumptions,
- treating timeout fallback as a playable move.

## Fixture Expectations

The first route, `Local Arena CLI v0`, covers:

- Kuhn hidden information,
- invalid-output handling,
- timeout fallback,
- fallback abuse,
- hidden-information canaries.

Leduc board reveal is the next staged expansion after the Kuhn fixture gate.

If your agent survives small games cleanly, that is useful evidence. Bigger tables have a way of finding loose screws.

## Bundled Agents

- [`check_call.py`](../examples/agents/check_call.py): friendly legal baseline.
- [`legal_random.py`](../examples/agents/legal_random.py): friendly legal randomized baseline.
- [`invalid_json.py`](../examples/agents/invalid_json.py): adversarial invalid-output fixture.
- [`timeout.py`](../examples/agents/timeout.py): adversarial timeout fixture.
- [`crash.py`](../examples/agents/crash.py) and [`eof.py`](../examples/agents/eof.py): process lifecycle fixtures.

## Read Next

- [Human rules](../RULES.md)
- [Agent rules](../AGENT-RULES.md)
- [Design](../DESIGN.md)
- [Work pack](../WORK-PACK.md)
