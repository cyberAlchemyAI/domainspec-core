# Poker Agent Arena Spec

Status: refreshed Invoke artifact
Source evidence:

- `development/dispatches/20260619-agent-arena-mechanics/`
- `development/refinement-runs/20260619T022414Z-current-spec-architecture-plan/RESULT.md`

## Definition

Poker Agent Arena is a local competition harness where autonomous agents play poker-like games through a constrained CLI protocol. The arena rewards poker performance, protocol reliability, deadline discipline, replayability, and later adaptation, while preserving hidden-information boundaries.

The first product surface is not a public casino, hosted tournament service, or full no-limit Hold'em engine. It is `Local Arena CLI v0`: a governed local arena contract that can be tested with toy fixtures before larger engine integration.

## Rule Views

The arena keeps two complementary rule views:

- `RULES.md`: human/product rule view. It explains what the competition is, what agents do, what fairness promises exist, what counts as a violation, and what is outside the first arena.
- `AGENT-RULES.md`: engineer/agent rule view. It states the protocol-facing rules that agent authors, referee implementers, validators, and future task-session agents must obey.

The human view is allowed to be explanatory and product-readable. The engineer/agent view must stay precise enough to complement `SPEC.md`, `DESIGN.md`, and later versioned `spec/l0/` contracts.

## Owned Boundary

The arena owns:

- Agent process lifecycle and stdin/stdout decision protocol.
- Human and engineer/agent rule views for the arena contract.
- Observation allowlist and hidden-information filtering.
- Authoritative legal-action envelopes exposed to agents.
- Timeout, malformed-output, and illegal-action handling.
- Deterministic fallback events and diagnostics.
- Transcript replay, seed-orbit accounting, and raw toy-game scoring.
- Later leaderboard scoring hooks after penalty calibration.

The arena does not own:

- Real-money play, deposits, withdrawals, or gambling operations.
- A hosted public matchmaking service in the first milestone.
- Hand-rolled no-limit Hold'em settlement, side-pot, odd-chip, or min-raise law.
- Agent private reasoning, model internals, or training pipelines.
- Primary leaderboard claims before adversarial penalty fixtures pass.

## Milestone Shape

### Local Arena CLI v0

`Local Arena CLI v0` is the first executable route. It must support legal-action masks, deadline metadata, deterministic fallback, hidden-information canaries, seat-swapped raw chip EV, replayable transcripts, and an explicit split between referee-only transcript material and any public or agent-visible replay.

The first fixture gate is Kuhn hidden information. Leduc board reveal is the first staged expansion after Kuhn proves protocol, replay, fallback, and diagnostics.

Ranking is diagnostic only: raw chip EV by seat-rotated toy orbit plus timeout rate, invalid-decision rate, fallback count, and replay determinism.

### M1: Hold'em Engine Parity

M1 introduces a selected local poker engine as the authority for game state, hand ranking, legal transitions, and pot settlement. The arena continues to own protocol, observation filtering, deadlines, replay, and scoring hooks.

No-limit details such as min-raise, short all-in, full-raise reopening, side pots, uncalled refunds, odd chips, tied showdowns, and chip conservation are accepted only through engine-parity fixtures.

### M2: Leaderboard And Novelty

M2 introduces calibrated adjusted scoring, reference bots, risk diagnostics, adaptation checks, and side-leaderboards for novelty mechanics. Composite `arena_score` is deferred until adversarial fixtures show that fallbacks, penalties, credit markets, and adaptation windows cannot improve rank by gaming the mechanism.

Novelty mechanics start outside primary ranking. Time-bank market is the first appendix candidate after Local Arena CLI v0 clocks, fallbacks, and raw scoring are stable.

## Primary Contracts

| Contract | Local Arena CLI v0 Requirement | Follow-up Gate |
| --- | --- | --- |
| CLI transport | Line-delimited JSON over stdin/stdout, one process per seat | WebSocket parity |
| Decision envelope | Protocol version, match id, hand id, decision id, seat id, deadline, observation, legal actions | Versioned schema migration |
| Observation | Public table state plus own private cards only | Engine-backed Hold'em projection |
| Legal actions | Referee-emitted set only | Hold'em engine parity matrix |
| Fallback | Deterministic legal continuation with separate invalid/timeout event | Penalty calibration |
| Replay | Referee transcript plus redacted public replay; exported replay uses opaque ids, seed handles, or post-match commitments | Public replay policy |
| Scoring | Raw toy EV plus timeout, invalid-decision, and replay diagnostics | `ev_lcb95` and adjusted leaderboard |

## Acceptance Gates

- Agents cannot observe deck order, seed, future cards, opponent live private cards, premature mucked cards, referee traces, engine internals, phase labels, or hidden assignment metadata.
- Every accepted legal-action rule has at least one toy fixture or an explicit M1 engine-parity gate.
- Timeout, malformed JSON, mismatched decision id, stdout prose before JSON, extra decision objects, illegal action, and illegal amount are logged as invalid or timeout events.
- Fallback is never a score-improving strategy in Local Arena CLI v0 abuse fixtures or later calibration fixtures.
- Replay can reproduce accepted actions, fallback events, payouts, and diagnostics from recorded transcript material without exposing raw seed material to live agents or public replay consumers.
- Hidden-information canaries cover observations, legal-action payloads, action history, stdout/stderr capture, replay exports, state hashes, environment/log redaction, and retained memory inputs.
- Composite leaderboard scoring remains blocked until reference-bot and adversarial calibration fixtures pass.

## L0 Runtime Proof

`SWU-PAA-001R` through `SWU-PAA-004` have passed for the local proof slice.
The versioned L0 contracts live under `spec/l0/`, and the runtime lives under
`src/poker_agent_arena/`.

Accepted Local Arena CLI v0 defaults:

- `5000ms` decision timeout and `10000ms` process cleanup timeout.
- Monotonic deadline clock from decision-envelope flush to first complete stdout
  JSON object.
- Invalid output uses deterministic fallback per decision with no match
  retirement in v0.
- Public replay uses opaque seed handles; raw seed material is referee-only.
- First smoke proof uses a tiny deterministic Kuhn seat-rotated orbit.
- Fallback order is `check`, `fold`, `call`, then minimum legal wager.

Durable verification lives in
`development/verification/local-arena-cli-v0/VERIFICATION.md`.

## Remaining Decisions

These decisions are post-MVP and do not block Local Arena CLI v0:

- Initial local engine choice for M1.
- Whether appendix time credits reset per hand, match, or evaluation block.
- Calibrated leaderboard and novelty mechanics after reference and abuse
  fixtures exist.
