# Poker Agent Arena

Small games. Sharp edges.

Poker Agent Arena is a local competition harness for agents that make poker decisions through a constrained command-line protocol. The first table is intentionally small: toy poker games, strict hidden-information boundaries, deterministic replay, and diagnostics for timing or invalid output.

The point is not to dress up a leaderboard before the rules can hold weight. The point is to build a table where clean decisions, legal actions, and calm behavior under pressure can be inspected hand by hand.

## Current Stage

The project now has a Local Arena CLI v0 proof slice: L0 contract files, a small
Kuhn hidden-information runtime, bundled sample agents, private transcript
writing, deterministic replay, public replay redaction, and diagnostics for
invalid output, timeouts, fallback, and replay determinism.

Current first route: `local-arena-cli-v0`.

Not yet included:

- full no-limit Hold'em runtime,
- hosted public matchmaking,
- real-money play,
- final composite leaderboard scoring,
- calibrated novelty mechanics.

## What The Arena Tests

- Can an agent choose from the legal actions it is actually given?
- Does it stay within the observation boundary?
- Does it answer before the deadline?
- Does it recover cleanly from strict protocol expectations?
- Can the match be replayed from transcript material without leaking hidden state?

`Local Arena CLI v0` ranking is diagnostic: raw toy-game chip EV, timeout rate, invalid-decision rate, fallback count, and replay determinism. The flashier scoring can wait its turn at the rail.

## Start Here

- [Human rules](RULES.md): the competition view.
- [Agent rules](AGENT-RULES.md): the implementation-facing rule view.
- [Competitor guide](docs/COMPETITOR-GUIDE.md): what a submitted agent should expect.
- [Agent author guide](docs/AGENT-AUTHOR-GUIDE.md): how to run and debug the L0 protocol.
- [Naming](NAMING.md): route, SWU, and fixture naming convention.
- [MVP path](MVP-PATH.md): the one implementation stream and current blockers.
- [Spec](SPEC.md): owned boundary and acceptance gates.
- [Work pack](WORK-PACK.md): current route and next execution unit.

## Local Smoke

```sh
PYTHONPATH=projects/poker-agent-arena/src python3 -m poker_agent_arena.cli doctor
PYTHONPATH=projects/poker-agent-arena/src python3 -m poker_agent_arena.cli eval --fixture kuhn_hidden_info --agent-a projects/poker-agent-arena/examples/agents/check_call.py --agent-b projects/poker-agent-arena/examples/agents/legal_random.py --out projects/poker-agent-arena/.tmp/smoke
PYTHONPATH=projects/poker-agent-arena/src python3 -m poker_agent_arena.cli replay projects/poker-agent-arena/.tmp/smoke/private-transcript.jsonl --out projects/poker-agent-arena/.tmp/smoke/replay
```

The smoke path writes `private-transcript.jsonl`, `diagnostics-report.json`,
`summary.json`, `public-replay.json`, and `replay-report.json` under the output
directory.

## Project Shape

`Local Arena CLI v0` is the first executable route. It uses a Kuhn fixture gate first, then stages Leduc board reveal as the next validation expansion before any larger poker engine is selected. M1 may wrap a local Hold'em engine after toy fixtures prove the protocol and replay surfaces. M2 is reserved for calibrated leaderboards and side-leaderboard novelty mechanics.

The arena keeps the referee honest, the agents bounded, and the transcript useful. A good agent will still need cards. It will also need manners.
