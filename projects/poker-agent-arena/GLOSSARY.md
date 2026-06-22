# Poker Agent Arena Glossary

Status: refreshed Invoke artifact
Source evidence:

- `development/dispatches/20260619-agent-arena-mechanics/`
- `development/refinement-runs/20260619T022414Z-current-spec-architecture-plan/RESULT.md`

## Terms

Arena: The local harness that runs agent processes, applies game rules, filters observations, validates actions, records transcripts, and computes diagnostics.

Local Arena CLI v0: The first executable route. It freezes the local CLI arena surface, runner, protocol, transcript, replay, diagnostics, sample agents, and fixture gates without tying the route id to one toy game.

Route id: A compact durable identifier for a work route. In this project it follows `<scope>-<surface>-<interface>-<version>`, such as `local-arena-cli-v0`.

Fixture gate: A game-specific or abuse-specific proof case inside a route. Kuhn hidden information is the first fixture gate for `Local Arena CLI v0`.

Human/product rule view: The reader-facing rules surface in `RULES.md`. It explains the competition, fairness promise, scoring shape, violations, and non-goals without serving as exact protocol schema.

Engineer/agent rule view: The implementation-facing rules surface in `AGENT-RULES.md`. It complements the spec by stating protocol, deadline, fallback, transcript, scoring, and fixture obligations for agent authors and validators.

Agent process: One submitted executable process bound to one seat. It receives decision envelopes on stdin and returns action envelopes on stdout.

Referee: The authority that owns true game state, legal actions, payout calculation, hidden-information boundaries, and replay material.

Observation allowlist: The explicit list of fields an acting agent may see. Anything not allowlisted is referee-only.

Legal-action mask: The authoritative set of currently legal actions and amounts emitted by the referee for one decision.

Decision envelope: The JSON message from the arena to an agent for a single action decision.

Action envelope: The JSON message from an agent to the arena containing the chosen action for a matching `decision_id`.

Deterministic fallback: A legal continuation action selected by the arena after timeout or invalid output. It keeps the hand moving but records a penalty-visible event.

Invalid event: A protocol or gameplay failure such as malformed JSON, mismatched decision id, stdout prose before JSON, extra decision object, illegal action, or illegal amount.

Transcript replay: A recorded sequence of observations, legal actions, accepted actions, fallbacks, elapsed times, state hashes, and payouts that can reproduce diagnostics.

Referee transcript: The private replay surface that may retain raw seed material, true state, internal traces, and state hashes for deterministic verification. It is never sent to live agents.

Public replay: The redacted replay surface that can be shared after a hand or match under policy. It uses opaque ids, seed handles, or commitments rather than raw seed or hidden state.

Seed handle: An opaque replay reference for randomness. It must not reveal deck order or predict future cards during live decisions.

Seed commitment: A public or post-match commitment that lets results be audited without exposing live hidden state.

Referee-only state: Any state that must never enter an agent decision envelope, including deck order, future board, live opponent cards, phase labels, hidden traces, and engine internals.

State namespace: A named boundary for where a piece of state may live and how it may move, such as `referee.truth`, `agent.observation`, `protocol.action`, `transcript.private`, `transcript.public`, or `score.diagnostics`.

Toy-game fixture: A small controlled game or scenario, such as Kuhn or Leduc, used to test protocol and scoring contracts before Hold'em integration.

Kuhn: A tiny poker game useful for hidden-information and legal-action smoke tests.

Leduc: A small two-street poker game useful for board reveal, state transition, and replay fixtures.

Seed orbit: A group of seeded hands replayed across seat rotations so each agent receives matched exposure.

Seat rotation: Reassigning agents to seats across a seed orbit to reduce position bias.

Raw chip EV: Zero-rake hand result before operational penalties or adjusted leaderboard scoring.

`ev_lcb95`: A lower confidence bound for EV, calculated from mean bb/100 and clustered standard error once enough fixtures exist.

Reference bot: A deterministic baseline agent such as always-fold/check, legal-random, or simple value-bet/call, used to interpret leaderboard behavior.

Adversarial calibration fixture: A scripted agent or scenario designed to prove that penalties, fallbacks, credits, or adaptation mechanics cannot improve rank by abuse.

Time-bank market: A novelty appendix where agents can spend or sell clock credits under deterministic, auditable, non-signaling rules.

Observation bandwidth: A novelty appendix where agents receive different allowlisted information budgets while legal actions remain complete and authoritative.

Adaptation window: A scoring or diagnostic interval that measures whether an agent improves from public history without receiving hidden labels or post-hand annotations.

Engine parity: The condition where arena projections, legal actions, pots, payouts, and chip conservation match a selected local poker engine.

Hidden-information canary: A test field or trace used to detect whether forbidden information leaks into agent-visible observations, logs, or replay material.

Fallback-abuse fixture: A fixture proving timeout, invalid, crash, or EOF behavior cannot improve clean ranking value through deterministic fallback.

Timing policy: The contract for clock source, decision deadline start, decision deadline stop, grace policy, timeout classification, elapsed-time recording, and replay behavior.

Collusion-adjacent side channel: Any timing, invalid-output, explanation, bidding, or repeated-action pattern that can signal hidden information between cooperating agents.
