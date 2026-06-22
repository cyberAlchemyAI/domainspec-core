# Poker Agent Arena Mechanics Research

Boundary: this file collects the five explorer returns only. It does not claim executable implementation, engine execution, scoring execution, or validated runtime behavior.

## rules-mechanics

The rules lane proposes a conservative no-limit Texas Hold'em cash-hand baseline with deterministic table configuration: seat count, button, blinds, optional ante, stacks, timeout policy, and an engine-held hand seed. MVP scope should begin with heads-up and 6-max fixtures before tournament movement, multi-table play, antes, straddles, run-it-twice, bomb pots, or novelty variants.

Its hand lifecycle covers forced bets, private hole-card delivery, preflop/flop/turn/river betting rounds, immediate award when all but one player folds, and showdown when at least two players remain after river betting. It also defines legal actions for fold, check, call, bet, raise, all-in short calls, all-in short raises, and full-raise reopening.

The pot contract requires stack caps, side-pot layering by contribution threshold, folded-player ineligibility, uncalled excess return, and one deterministic odd-chip convention. The hidden-information boundary is allowlist-shaped: public table state, own hole cards, public board, public action history, legal actions, acting seat, and deadline may be exposed; deck order, seed, future cards, live opponent cards, mucked cards before legal reveal, and private reasoning must stay hidden.

The lane recommends deterministic fallback for timeout, malformed output, illegal action, and illegal amount, computed from engine legal actions at decision time. It also says the arena should use a local engine as game-state authority while owning observation filtering, action schema, timeout policy, reproducible configuration, and scoring hooks.

Needed checks include heads-up and multiway action order, legal-action matrix, side pots, tied showdown plus odd chips, hidden-information filtering, timeout fallback, and engine parity over a small deterministic hand corpus. Flagged risks are min-raise/reopen errors, side-pot divergence, hidden leaks through logs or serialized engine state, timeout exploitation, and unresolved odd-chip and muck/show conventions.

## scoring-economy

The scoring lane proposes a zero-rake virtual economy where in-hand chips remain zero-sum and leaderboard penalties are applied after the hand ledger. It recommends adjusted cash EV as the primary ranking signal, with `net_bb_per_100`, `mean_bb100`, clustered standard error by seed orbit, and `ev_lcb95 = mean_bb100 - 1.96 * clustered_se`.

Evaluation should run in seed orbits: each base seed is paired with all seat rotations so every agent receives equal exposure to positions against the same lineup. Leaderboard score is expressed in bb/100-equivalent units:

```text
arena_score = ev_lcb95 - latency_penalty - invalid_penalty - risk_penalty + adaptation_bonus
```

The lane recommends publishing both adjusted score and raw mean, marking rows provisional until variance shrinks or a hand cap is reached, and including reference bots such as always-fold/check, legal-random, simple value-bet/call, and a deterministic baseline.

Latency and invalid-action behavior are scoring-visible but post-ledger. Soft-deadline overage accrues small bb-equivalent penalty, hard timeout receives an added timeout penalty, invalid output receives a larger invalid penalty, and high invalid rates can flag or disqualify an agent. Drawdown/risk tracking uses a virtual bankroll, max drawdown, ruin count, and seed-orbit CVaR. Adaptation compares paired late-block EV against early-block EV using only public history.

Needed checks include seat-rotation invariance, variance shrinkage, timeout penalties, invalid-action fallback and DQ gates, risk penalty calibration, adaptation from public history, hidden-information tracing, and tie-breaker ordering. Residue includes exact deadlines, hand/orbit counts, whether tournament ROI stays report-only, and calibration against penalty gaming.

## agent-protocol

The protocol lane proposes a line-delimited JSON CLI protocol for MVP. The arena starts one process per agent seat, sends one JSON message per line to stdin, and reads one JSON object per decision from stdout. Stderr is reserved for logs and must not affect gameplay. The same envelopes can later map to WebSocket messages.

The decision envelope includes `protocol_version`, `type`, `match_id`, `hand_id`, `decision_id`, `seat_id`, `deadline_ms`, `observation`, and authoritative `legal_actions`. Observation fields are public-plus-own-private: game, street, button, acting seat, hero seat, hero cards, board, pot, side pots, stacks, committed chips, to-call, min-raise target, action history, and public seat state. Forbidden fields include deck order, seed, future board cards, other live private cards, premature mucked cards, engine evaluation internals, opponent-model hints, and hidden assignment metadata.

Agent stdout should return an action envelope with matching protocol version and decision id. The engine validates envelope, decision id, and action legality; metadata is ignored for scoring except logs and later analysis. Agents must not emit prose on stdout, and if multiple JSON objects appear for a decision, the first complete object is used while the rest is logged as noise.

Deadline handling is measured from engine write flush to first complete stdout JSON object. Timeout, malformed JSON, missing or mismatched decision id, unknown action, illegal amount, or stdout prose before JSON all map to deterministic fallback and logging. Repeated invalid output can retire the process for the match. Lifecycle messages are hello, ready, decision stream, optional hand and match result, and shutdown.

Needed checks include Kuhn hidden information, Leduc board reveal, timing fallback, invalid output, all-in/side-pot legal actions, replay logs, and later WebSocket parity. Residue includes strike limits, default deadlines, log retention and redaction, and seed-commitment visibility.

## toy-game-validator

The validator lane designs deterministic fixtures to validate arena mechanics before full no-limit Hold'em exists. It explicitly treats fixture success as coherence evidence, not proof that full Hold'em is implemented or balanced.

The fixture set includes Kuhn hidden-info smoke, Leduc two-street state boundary, invalid action matrix, clock and time-bank fixture, three-seat all-in pot accounting, seat-swapped variance scoring, adaptation ladder, exploitability oracle, and information-leak canary.

Expected transcript evidence includes per-seat observations, legal-action masks, referee-only traces, state hashes, deadline metadata, error codes, pot layers, payout rows, chip-conservation checks, seed-pair result tables, rolling EV, exploitability values for tiny games, and leak canary absence in agent-visible material.

Risks are that toy all-in checks do not cover full no-limit complexity, adaptation behavior changes do not prove strategic understanding, exploitability is tractable only for tiny games, and timing evidence must tolerate scheduler jitter. Implementation should block if the protocol cannot emit legal-action masks, deadline metadata, state hashes, and referee-only traces.

## novelty-lane

The novelty lane proposes agent-native resource and adaptation mechanics while preserving orthodox poker hands and hidden-information boundaries. Ranked ideas are time-bank market, observation bandwidth draft, memory/adaptation ladder, mixed toy-game ladder, explanation tax, counterfactual mirror seats, and adversarial observation compression.

Its recommended wild-card is the time-bank market. Agents receive match-level clock credits and may spend them for longer deadlines or sell unused reserve for score. Credits stay outside chip stacks, chip EV remains poker score, and tie-breaks in credit auctions must be deterministic.

Next-tier experiments are observation bandwidth and memory/adaptation ladder. Bandwidth only allocates among allowlisted safe fields and must keep legal actions authoritative and complete. Memory/adaptation must retain only agent-owned state and public transcripts, never referee logs or hidden traces.

Needed checks include Kuhn clock-credit replay, Leduc bandwidth serialization, adaptation without phase labels, mixed-game protocol compatibility, explanation-tax handling, and mirror-seat scoring. Residue includes credit pricing, reset policy, bandwidth categories, adaptation windows, and skeptic attacks against credit hoarding, intentional timeouts, compression blind spots, and explanation spam.
