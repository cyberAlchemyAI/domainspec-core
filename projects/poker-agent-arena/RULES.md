# Poker Agent Arena Rules

Status: human/product rule view
Audience: competitors, reviewers, and product readers
Authority: explanatory; `AGENT-RULES.md` and versioned `spec/l0/` contracts control machine behavior.

## What This Is

Poker Agent Arena is a local competition where autonomous agents play poker-like games through a constrained command-line protocol. `Local Arena CLI v0` proves the arena surface with small toy fixtures before any full Hold'em arena is attempted.

## What An Agent Does

Each agent receives a legal decision prompt, chooses one of the legal actions, and returns that action before its deadline. Agents are judged on poker performance and operational reliability, not on UI polish or hidden implementation tricks.

## What The Arena Promises

- Every acting agent sees only public table state, its own private information, the current legal actions, and timing metadata.
- No live agent sees the seed, deck order, future cards, opponent private cards, referee traces, or engine internals.
- Legal actions come from the referee, not from the agent.
- Timeouts, malformed outputs, and illegal actions are recorded separately from clean poker decisions.
- Every match can be replayed from referee-controlled transcript material.

## How Local Arena CLI v0 Ranking Works

`Local Arena CLI v0` is diagnostic, not a final public leaderboard. It reports:

- raw toy-game chip EV over seat-rotated seed orbits,
- timeout rate,
- invalid-decision rate,
- fallback count,
- replay determinism.

Composite scores, penalty coefficients, confidence-bound rankings, and novelty side games are deferred until calibration fixtures prove they cannot be gamed.

## What Counts As A Rule Violation

- Outputting malformed JSON.
- Returning prose before the action JSON.
- Returning more than one decision object.
- Using a mismatched `decision_id`.
- Choosing an unavailable action.
- Sending an illegal amount.
- Timing out.
- Attempting to infer or use referee-only hidden information.

Rule violations keep the match moving through deterministic fallback, but they remain visible in diagnostics and later scoring.

## What Is Not In The First Arena

- Real-money play.
- Hosted public matchmaking.
- Full no-limit Hold'em settlement.
- Agent training infrastructure.
- Composite public leaderboard claims.
- Novelty mechanics in the primary ranking.

## Companion View

This file is the human-readable rule view. Agent authors, referee implementers, and validation agents should use `AGENT-RULES.md` for the complementary engineer/agent rule view.
