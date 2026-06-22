# MVP Minimality Review Receipt

dispatch_id: 2026-06-19-poker-agent-arena-mechanics
role_id: mvp-minimality-skeptic
spawn_status: spawned
join_status: completed
close_status: closed
status: ACCEPT_WITH_EDITS

## validation

I read `findings.md` and `research.md`. Their own boundary is design evidence only, with no executable implementation, scoring execution, engine execution, or validated runtime behavior. The CLI protocol and toy-game validator lanes are appropriate MVP anchors. The current handoff only passes MVP minimality if "MVP" is narrowed to a first CLI arena over deterministic toy games, with full no-limit Hold'em, rich ranking, and novelty mechanics treated as later integration layers.

## blockers

1. The first MVP rule overcommits to "no-limit Texas Hold'em cash-hand baseline" with heads-up and 6-max fixture coverage. That makes engine law, multiway action order, and pot settlement prerequisites for the first CLI arena. Exact edit: replace that bullet with: "Use a toy-game-first CLI arena as MVP: Kuhn for hidden information and Leduc for board reveal, legal actions, deterministic fallback, transcript replay, and seat-swapped scoring. Treat no-limit Hold'em as the first engine-parity integration after those toy contracts pass."

2. The legal-action rule lists all-in short calls, short raises, min-raise, and full-raise reopening as MVP commitments. Those are engine-scope details, not first-arena requirements. Exact edit: split the bullet into two bullets: "For toy MVP, legal actions must come only from the authoritative legal-action set emitted by the referee." and "For Hold'em integration, add min-raise, short all-in, and full-raise reopening only through engine-parity fixtures, not hand-rolled arena logic."

3. Side pots, odd chips, folded-player ineligibility, uncalled excess return, and tied showdown are necessary poker mechanics, but they are too large for the first CLI arena. Exact edit: change the fixture-gated mechanics bullet to: "For toy MVP, require chip conservation, legal fallback, hidden-information filtering, and deterministic payouts. Move side pots, odd chips, uncalled excess return, and tied showdown to the Hold'em engine-parity gate."

4. The scoring section is too ambitious for an MVP because it combines adjusted EV, clustered standard error, risk penalty, adaptation bonus, diagnostics, and a composed `arena_score`. Exact edit: replace the `arena_score` bullet with: "For first CLI MVP, publish raw chip EV by seat-rotated toy orbit plus timeout rate, invalid-decision rate, and replay determinism. Do not use a composite arena score until penalty coefficients are calibrated against reference bots."

5. The toy fixture list contains valid later checks, but exploitability oracle, adaptation ladder, clock/time-bank behavior, and three-seat all-in pot accounting are not needed before the first CLI arena is useful. Exact edit: change the fixture bullet to: "MVP fixtures are Kuhn hidden information, Leduc board reveal, invalid action/output matrix, timeout fallback, seat-swapped scoring, deterministic transcript replay, and information-leak canary. Move exploitability, adaptation, time-bank, and multiway all-in fixtures to follow-up gates."

6. The novelty appendix still names the time-bank market as the "first wild-card mechanic" and says it can include a score component. That risks pulling scheduling economics into the MVP. Exact edit: replace the first two Novelty Appendix bullets with: "Keep all novelty mechanics outside MVP scoring. Time-bank market may be the first appendix experiment after baseline deadlines, fallback, replay, and raw scoring are stable, but it must not change first-arena rankings."

7. The implementation order places toy pot, showdown, side-pot, uncalled-refund, odd-chip, and chip-conservation fixtures before Hold'em settlement. Exact edit: in step 3, replace that list with: "Add toy payout and chip-conservation fixtures." Add a new post-engine step: "After selecting the Hold'em engine, add side-pot, showdown, uncalled-refund, odd-chip, and chip-conservation parity fixtures against engine truth."

## residue

- Choose the exact M0 game set: recommend Kuhn plus Leduc only.
- Choose one deterministic fallback policy for timeout, malformed output, illegal action, and illegal amount.
- Freeze the minimal line-delimited JSON decision/action schema before scoring work.
- Pick two reference bots for M0: always-fold/check and legal-random are enough.
- Leave selected Hold'em engine, 6-max coverage, side-pot parity, exploitability, adaptation scoring, and time-bank pricing as named follow-up decisions.

## reroute

Do not send the whole handoff to implementation as one MVP. Reroute into:

1. M0 CLI toy arena contract: process protocol, observation allowlist, legal-action mask, deterministic fallback, transcript replay, Kuhn/Leduc fixtures, raw chip EV, invalid/timeout diagnostics.
2. M1 Hold'em engine parity: engine selection, heads-up first, then 6-max, min-raise/reopen behavior, side pots, uncalled refunds, tied showdown, odd chips, and engine observation parity.
3. M2 leaderboard and novelty: `ev_lcb95`, risk/adaptation penalties, exploitability reports, time-bank market, bandwidth, explanation tax, and mixed-game ladders.

## handoff_note

ACCEPT_WITH_EDITS. The design is promising, but MVP minimality requires a hard toy-game-first boundary. Implement only M0 after applying the exact edits above; otherwise the first CLI arena will be blocked by full poker-engine scope and scoring-economy calibration before it can teach anything.
