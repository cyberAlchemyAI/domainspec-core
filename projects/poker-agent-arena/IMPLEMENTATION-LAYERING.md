# Poker Agent Arena Implementation Layering

Status: refreshed Invoke artifact
Source evidence:

- `development/dispatches/20260619-agent-arena-mechanics/`
- `development/refinement-runs/20260619T022414Z-current-spec-architecture-plan/RESULT.md`

## Layer Summary

| Layer | Name | Purpose | Gate |
| --- | --- | --- | --- |
| L0R | L0 Contract Handoff Repair | Freeze the two rule views, output tree, component map, namespaces, transcript split, fixture requirements, fallback-abuse checks, canary scope, and timing policy | Required before L0 execution |
| L0 | Local Arena CLI v0 Contract | Freeze and validate protocol, observation, fallback, replay, and raw diagnostics with a Kuhn fixture gate first | After L0R |
| L1 | Hold'em Engine Parity | Wrap a local engine and prove arena projections match engine truth | After L0 |
| L2 | Reliability Leaderboard | Add calibrated `ev_lcb95`, reference bots, invalid/timeout penalties, and risk diagnostics | After L1 parity and calibration |
| L3 | Novelty Appendix | Add time-bank market, bandwidth, adaptation ladder, and mixed-game side leaderboards | Side-gated |

## L0R: L0 Contract Handoff Repair

L0R is the active refreshed layer. It produces a docs/schema/fixture contract packet and updates the root artifacts so `SWU-PAA-001` can execute without inventing structure mid-run.

Deliverables:

- L0 output tree for protocol, transcript, state namespaces, and fixtures.
- Two rule views: human/product `RULES.md` and engineer/agent `AGENT-RULES.md`.
- L0 component map with inputs, outputs, owned state, forbidden state, schema dependency, and replay responsibility.
- State namespace matrix.
- Referee transcript vs public replay split.
- Kuhn fixture-gate requirements and staged Leduc board-reveal expansion requirements.
- Fallback-abuse fixture requirements.
- Expanded hidden-information canary scope.
- Local Arena CLI v0 timing policy fields.
- Local Arena CLI v0 and M2 scoring language cleanup.

Exit gate:

- `WORK-PACK.md` names `SWU-PAA-001R` as the immediate next route.
- `SWU-PAA-001` has a concrete output tree and reviewable checks.
- `RULES.md` and `AGENT-RULES.md` exist and name their audiences, authority, and handoff relationship.
- Raw seed material is referee-only and public replay uses opaque handles or post-match commitments.
- Hidden-information canary surfaces include observations, legal-action payloads, action history, stdout/stderr captures, replay/public exports, state hashes, environment/log redaction, and retained memory inputs.

## L0: Toy CLI Contract

L0 executes only after L0R passes. It should produce enough executable evidence that later Hold'em work does not have to guess the protocol shape.

Deliverables:

- Product-readable competition rules and implementation-facing agent rules.
- Versioned decision and action envelope schemas.
- Observation allowlist and referee-only field list.
- Legal-action mask representation.
- Deterministic fallback event schema.
- Canonical Kuhn hidden-information fixture gate with rule id, deck, ante/blind/bet sizes, raise cap, legal-action table, terminal payout formula, reveal timing, seed corpus, and golden transcript/payout oracle.
- Staged Leduc board-reveal fixture expansion with rule id, deck, ante/blind/bet sizes, raise cap, legal-action table, terminal payout formula, reveal timing, seed corpus, and golden transcript/payout oracle.
- Invalid-output and timeout matrix.
- Fallback-abuse fixtures: always-timeout, always-invalid, invalid-only-when-facing-bet, crash, and EOF agents.
- Seat-rotated raw chip EV diagnostics.
- Replay verifier for transcript determinism.

Exit gate:

- Kuhn fixture gate passes; Leduc board-reveal expansion is staged unless the first route is deliberately widened.
- Hidden-information canary is absent from agent-visible envelopes, logs, action history, replay exports, reversible state hashes, retained memory inputs, and redaction surfaces.
- Every invalid and timeout path creates a diagnostic event.
- Replay reproduces payouts and diagnostics.
- Raw toy EV is derived from transcript records and reported separately from invalid/timeout rates.


## L1: Hold'em Engine Parity

L1 selects a local poker engine and treats it as game-state authority. The arena continues to own process protocol and filtered observation.

Deliverables:

- Engine adapter boundary.
- Engine-version capture in transcript.
- Legal-action parity fixture.
- Min-raise, short all-in, and reopening fixture.
- Side-pot, odd-chip, tied-showdown, uncalled-refund, and chip-conservation fixture.
- Observation projection fixture comparing referee-only and agent-visible state.

Exit gate:

- Arena legal actions match engine legal actions.
- Pot settlement and payouts match engine truth.
- No engine internals appear in observations.
- Hold'em transcript replays under the captured engine version.

## L2: Reliability Leaderboard

L2 turns diagnostics into a credible leaderboard only after calibration.

Deliverables:

- Reference bots: always-fold/check, legal-random, simple value-bet/call, deterministic baseline.
- Seat-orbit evaluator.
- `mean_bb100`, clustered standard error, and `ev_lcb95`.
- Timeout, invalid-output, latency, risk, drawdown, CVaR, worst-seat EV, and adaptation diagnostics.
- Adversarial calibration bots: always-timeout, always-invalid, invalid-only-when-facing-bet, latency-staller, credit-hoarder, risk-lottery, public-history-overfitter.

Exit gate:

- No adversarial calibration bot improves adjusted rank relative to raw zero-rake EV by abusing penalties, fallbacks, credits, variance controls, or adaptation windows.
- Composite `arena_score` coefficients are versioned and reportable.
- Raw EV remains visible beside adjusted score.

## L3: Novelty Appendix

L3 introduces agent-native mechanics without contaminating primary ranking.

Deliverables:

- Time-bank market fixture.
- Credit bidding redaction and anti-signaling tests.
- Observation bandwidth fixture.
- Memory/adaptation ladder with shuffled-block negative control.
- Mixed toy-game ladder.
- Explanation-tax logging policy.
- Collusion-adjacent side-channel diagnostics.

Exit gate:

- Novelty effects are side-leaderboard only unless independently calibrated.
- Credit bids cannot signal hidden-card information.
- Explanation text never affects gameplay validation.

## Current Recommendation

Start with L0R, then execute `Local Arena CLI v0`. Keep all code mutation bounded to the local arena CLI contract. The first executable task should freeze the protocol and Kuhn fixture gate before selecting or wrapping a Hold'em engine.
