# Poker Agent Arena Agent Rules

Status: engineer/agent rule view
Audience: agent authors, referee implementers, validators, and future task-session agents
Authority: normative for L0 planning; future versioned files under `spec/l0/` control exact schemas once created.

## View Contract

This file complements `RULES.md`, `SPEC.md`, and `DESIGN.md`.

- `RULES.md` explains the competition in human/product language.
- `AGENT-RULES.md` states what an agent or referee implementation must obey.
- `SPEC.md` and `DESIGN.md` define the owned boundary and architecture.
- `spec/l0/` files, once created, become the versioned source for exact fields and fixtures.

## Transport Rules

- The arena sends one decision envelope to one agent process over stdin.
- The agent returns one action envelope over stdout.
- The first complete stdout JSON object is the only gameplay candidate.
- Prose before JSON, malformed JSON, extra decision objects, and mismatched ids are invalid events.
- Stderr may be captured for diagnostics but never changes gameplay legality.

## Decision Envelope Rules

The arena decision envelope must include:

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

## Action Envelope Rules

The agent action envelope must include:

- `protocol_version`
- `decision_id`
- `action`

Optional metadata is ignored for gameplay. It must not be required for legal action interpretation.

## Legal Action Rules

- The current `legal_actions` list is authoritative.
- An action not present in the current legal-action set is invalid.
- An amount outside the current legal-action bounds is invalid.
- The referee, not the agent, owns state transitions and payouts.

## Deadline And Fallback Rules

- Deadline timing starts after the arena flushes the decision envelope.
- Deadline timing stops at the first complete stdout JSON object.
- Timeout creates a timeout event and deterministic legal fallback.
- Invalid output creates an invalid event and deterministic legal fallback.
- Fallback keeps the hand moving but is not clean play.

## Transcript And Replay Rules

- Referee transcript may retain raw seed material and true state for deterministic verification.
- Public replay must use redacted state, opaque ids, seed handles, or post-match commitments.
- Raw seed material and reversible hidden-state hashes must not appear in live decision envelopes or public replay.
- Replay must reproduce accepted actions, fallback events, payouts, and diagnostics.

## Local Arena CLI v0 Scoring Rules

`Local Arena CLI v0` reports raw toy-game EV and diagnostics only.

Required diagnostics:

- timeout rate,
- invalid-decision rate,
- replay determinism,
- fallback events,
- seat-rotation coverage.

Adjusted scoring, confidence-bound ranking, and composite `arena_score` are blocked until calibration fixtures pass.

## Fixture Rules

The Local Arena CLI v0 fixture set must include:

- Kuhn hidden-information fixture,
- invalid-output matrix,
- timeout fallback fixture,
- fallback-abuse fixture,
- hidden-information leak canary fixture.

Leduc board reveal is the first staged fixture expansion after the Kuhn gate.

Fixtures must prove that illegal output, fallback behavior, replay exports, stdout/stderr captures, logs, and retained memory inputs do not leak hidden information or improve clean ranking value.
