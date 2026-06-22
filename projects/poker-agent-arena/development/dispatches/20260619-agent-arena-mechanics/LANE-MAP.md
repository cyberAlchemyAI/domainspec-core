# Poker Agent Arena Mechanics Lane Map

Status: route preview only. No subagents have been spawned.

Dispatch artifact:
`projects/poker-agent-arena/development/dispatches/20260619-agent-arena-mechanics/poker-agent-arena-mechanics.dispatch.json`

## Purpose

Design the first rules and mechanics package for a poker-agent competition:
baseline game rules, scoring, CLI protocol, toy-game fixtures, zig-zag critique,
and one dedicated novelty lane.

## Lanes

| Lane | Owns | Questions |
| --- | --- | --- |
| Rules/mechanics | Baseline games, legal actions, clocks, blinds/stacks, side pots, hidden-information boundary | What is the smallest fair game contract agents can play against? What engine state must never leak? |
| Scoring/economy | EV/ROI windows, latency, invalid-action penalties, drawdown, tie-breakers | How do we reward clever play without over-rewarding variance or slow thinking? |
| Agent protocol | CLI stdin/stdout JSON, deadline behavior, invalid output behavior, later WebSocket compatibility | What should a Claude/Hermes/Codex-style agent receive and return each turn? |
| Toy-game validator | Kuhn/Leduc/single-street/all-in fixtures, timing fixtures, hidden-info fixtures | Which tiny games prove the mechanics before full no-limit Hold'em? |
| Novelty lane | Unusual mechanics that make the competition more agent-native | What mechanics create strategy beyond ordinary poker while preserving fairness? |
| Exploitability skeptic | Degenerate strategy, time-bank abuse, scoring exploits, information leakage | How can agents break the proposed rules, and what repair or test catches it? |

## Zig-Zag Shape

1. Baseline lanes draft mechanics.
2. Toy-game validator reduces them into small controlled fixtures.
3. Mechanics advocate and exploitability skeptic run two critique loops.
4. Novelty lane runs separately and ranks unusual mechanics by novelty,
   fairness, implementability, agent-cleverness signal, and toy-game testability.
5. Parent synthesis combines accepted baseline mechanics, repaired critique
   outcomes, toy-game evidence, and one safe wild-card mechanic.

## Execution Gate

The dispatch recommends subagent lanes, but execution still requires explicit
operator approval. The route is ready for a later governed run through the
DomainSpec subagent lifecycle.
