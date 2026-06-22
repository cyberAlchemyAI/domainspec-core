# Invoke Define: Poker Agent Arena L0 Contract Target

Status: pass
Owner: `invoke` via parent Refine coordinator
Mode: `define`

## Definition

The next coherent unit is not "a poker arena" in full. It is a local L0 contract package that lets agents make decisions over toy poker games through a stable CLI protocol while the arena records enough evidence to prove hidden-information filtering, fallback behavior, replay determinism, and raw scoring diagnostics.

## Refined Problem Statement

Current root artifacts define the right direction but still bundle several horizons: protocol, toy fixtures, replay, scoring diagnostics, Hold'em engine parity, adjusted leaderboard scoring, and novelty mechanics. The Refine run should reduce that to the smallest task-session-ready target.

## Refined L0 Boundary

In:

- JSON decision and action envelopes.
- Observation allowlist and referee-only field list.
- Legal-action object representation.
- Invalid and timeout event taxonomy.
- Deterministic fallback selection rule.
- Transcript record shape.
- Kuhn and Leduc fixture skeleton definitions.
- Replay determinism and raw toy EV diagnostic expectations.

Out:

- Full Hold'em engine integration.
- Composite `arena_score`.
- Time-bank or bandwidth mechanics.
- Hosted arena service.
- Agent training or model evaluation harness beyond protocol conformance.

## Success Definition

The refined plan is task-session-ready when `SWU-PAA-001` can name concrete output files, schema examples, fixture skeleton files, and validation commands without inventing runtime architecture mid-run.
