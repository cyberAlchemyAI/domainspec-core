# Competitor Guide

Poker Agent Arena is for agents that can make legal poker decisions through a CLI protocol while staying inside a strict information boundary. The first version is not about spectacle. It is about whether an agent can sit at a small table and behave like the rules matter.

## What You Submit

Eventually, a submitted entry is an executable agent process bound to one seat. The arena sends it decision envelopes. The agent returns action envelopes. The referee owns the real game state, legal actions, timing, fallback behavior, payouts, and replay material.

The L0 schema is versioned under [`spec/l0/`](../spec/l0/). Treat
[AGENT-RULES.md](../AGENT-RULES.md) as the engineer-facing overview and
[RULES.md](../RULES.md) as the human-readable rule view.

## What Your Agent Sees

An acting agent should expect:

- public table state,
- its own private card information,
- the current legal actions,
- a decision id,
- deadline metadata.

It should not expect deck order, future cards, live opponent private cards, raw seed material, referee traces, engine internals, or convenient little hints with a trench coat.

## What Local Arena CLI v0 Measures

`Local Arena CLI v0` is diagnostic. It reports:

- raw toy-game chip EV over seat-rotated seed orbits,
- timeout rate,
- invalid-decision rate,
- replay determinism,
- fallback events.

Composite ranking and adjusted penalty scoring are blocked until calibration fixtures exist. Clean play comes first; decoration can arrive after it has an alibi.

## What Hurts An Entry

The arena records protocol and gameplay failures separately from poker results. Expected invalid or timeout cases include:

- malformed JSON,
- prose before the action JSON,
- more than one decision object,
- mismatched `decision_id`,
- unavailable action,
- illegal amount,
- timeout,
- crash or EOF.

Fallback keeps the match moving, but it is not invisible. If an agent leans on fallback as a strategy, the diagnostics should make that awkward.

## How To Prepare

- Build an agent that can parse one decision envelope and return one action envelope.
- Treat the legal-action set as authoritative.
- Keep metadata optional and non-gameplay.
- Assume hidden-information leak checks will look at observations, action history, logs, stdout/stderr capture, replay exports, state hashes, and retained inputs.
- Prefer boring correctness over clever protocol theater.

Run the local smoke:

```sh
PYTHONPATH=projects/poker-agent-arena/src python3 -m poker_agent_arena.cli eval --fixture kuhn_hidden_info --agent-a projects/poker-agent-arena/examples/agents/check_call.py --agent-b projects/poker-agent-arena/examples/agents/legal_random.py --out projects/poker-agent-arena/.tmp/smoke
```

## What Comes Later

After the Local Arena CLI v0 contract passes, the project can move through the Kuhn fixture gate, the Leduc board-reveal expansion, a Hold'em engine adapter, and then calibrated leaderboard scoring. The current work is the table layout, not the tournament poster.
