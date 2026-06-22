# Poker Agent Arena Mechanics Handoff

Boundary: this package is design evidence only and does not claim executable implementation, engine execution, scoring execution, or validated runtime behavior. (rules-mechanics) (scoring-economy) (agent-protocol) (toy-game-validator) (novelty-lane)

## MVP Rules

- Use a toy-game-first CLI arena as MVP: Kuhn for hidden information and Leduc for board reveal, legal actions, deterministic fallback, transcript replay, and seat-swapped scoring. Treat no-limit Hold'em as the first engine-parity integration after those toy contracts pass. (toy-game-validator) (agent-protocol) (rules-mechanics)
- Keep the selected local poker engine as the authority for game state, hand ranking, and state transition, while the arena owns observation filtering, action schema, timeout policy, reproducible configuration, and scoring hooks. (rules-mechanics)
- Expose only public table state plus the acting agent's own private hole cards, and forbid deck order, random seed, future cards, live opponent cards, premature mucked cards, engine internals, and private reasoning. (rules-mechanics) (agent-protocol)
- For toy MVP, legal actions must come only from the authoritative legal-action set emitted by the referee. (agent-protocol) (toy-game-validator)
- For Hold'em integration, add min-raise, short all-in, and full-raise reopening only through engine-parity fixtures, not hand-rolled arena logic. (rules-mechanics) (toy-game-validator)
- Resolve timeout, malformed output, illegal action, and illegal amount through deterministic legal fallback computed from the current legal-action set, with scoring penalties handled outside the hand ledger. (rules-mechanics) (scoring-economy) (agent-protocol)
- Fallback is a recovery path, not a strategic option: every timeout, malformed output, illegal action, illegal amount, mismatched decision id, stdout prose-before-JSON, or extra decision object must be marked as an invalid/timeout event, recorded separately from agent-chosen legal actions, and penalized or disqualified strongly enough that an agent cannot improve `arena_score` by intentionally causing fallback in any fixture. Check-if-legal-else-fold is allowed only as the deterministic continuation action, not as forgiveness. (rules-mechanics) (scoring-economy) (agent-protocol)
- For toy MVP, require chip conservation, legal fallback, hidden-information filtering, and deterministic payouts. Move side pots, odd chips, uncalled excess return, and tied showdown to the Hold'em engine-parity gate. (rules-mechanics) (toy-game-validator)

## Scoring

- Use zero-rake chip accounting for hand results, then apply latency, invalid-action, risk, and adaptation adjustments after the hand ledger so poker EV stays auditable separately from operations reliability. (scoring-economy)
- Rank MVP agents by adjusted cash EV using seat-rotated seed orbits, `mean_bb100`, clustered standard error, and `ev_lcb95`, while also publishing raw mean and variance status. (scoring-economy)
- For first CLI MVP, publish raw chip EV by seat-rotated toy orbit plus timeout rate, invalid-decision rate, and replay determinism. Do not use a composite arena score until penalty coefficients are calibrated against reference bots. (scoring-economy) (toy-game-validator)
- Before leaderboard use, every non-EV component must pass adversarial calibration fixtures: always-timeout, always-invalid, invalid-only-when-facing-bet, latency-staller, credit-hoarder, risk-lottery, and public-history-overfitter. A component fails if the adversary improves adjusted rank relative to its raw zero-rake EV by exploiting penalties, credits, fallbacks, variance controls, or adaptation windows. (scoring-economy) (novelty-lane) (toy-game-validator)
- Use reference bots, including always-fold/check, legal-random, simple value-bet/call, and a known deterministic baseline, to make leaderboard behavior easier to interpret. (scoring-economy)
- Report latency, timeout rate, invalid decision rate, drawdown, ruin count, CVaR, worst-seat EV, and adaptation delta as first-class diagnostics, not hidden tie-break state. (scoring-economy)
- Adaptation bonus may use only public transcripts available to all agents at the same decision time. It must not expose opponent family labels, phase labels, seed ids, scripted-policy change markers, referee logs, hidden traces, or post-hand annotations during evaluation. Bonus eligibility requires a shuffled-block negative-control fixture that erases the claimed adaptation signal. (scoring-economy) (toy-game-validator) (novelty-lane)
- Keep tournament ROI report-only until payout fixtures exist, because the scoring lane identifies adjusted cash EV as the easier MVP surface to seed, replay, and compare. (scoring-economy)

## CLI Protocol

- Use line-delimited JSON over stdin/stdout as the MVP transport, with one arena process per agent seat and stderr captured only as opaque logs. (agent-protocol)
- Send each decision as an envelope with protocol version, match id, hand id, decision id, seat id, deadline, filtered observation, and authoritative legal actions. (agent-protocol)
- Accept only one JSON action envelope per decision from stdout, require matching `decision_id`, ignore free-form metadata for gameplay, and treat stdout prose or extra objects as protocol noise or invalid output. (agent-protocol)
- Measure deadline from engine write flush to the first complete stdout JSON object, then log timeout or invalid-output events and continue through deterministic fallback. (agent-protocol)
- Record replay material such as protocol version, engine version, ruleset id, seed handle or commitment, agent package digest, argv, environment allowlist, decision messages, accepted actions, fallbacks, elapsed time, and payouts. (agent-protocol)
- Seed handles, seed commitments, seed-orbit ids, block/phase labels, referee-only traces, state hashes with reversible hidden-state input, and engine internals must be referee-only during live decisions. Agent-visible match id, hand id, and decision id must be opaque and non-predictive with respect to deck order, future board cards, seat-rotation orbit, evaluation block, or opponent-script phase. Post-match replay may reveal commitments only under the declared redaction policy. (agent-protocol) (toy-game-validator) (rules-mechanics)
- Preserve schema compatibility for later WebSocket transport by keeping decision id, deadline, legal actions, and hidden-information rules stable. (agent-protocol)

## Toy-Game Fixtures

- Build a deterministic fixture harness before the full Hold'em arena, because the validator lane frames fixture success as contract-coherence evidence rather than proof of full Hold'em implementation. (toy-game-validator)
- MVP fixtures are Kuhn hidden information, Leduc board reveal, invalid action/output matrix, timeout fallback, seat-swapped scoring, deterministic transcript replay, and information-leak canary. Move exploitability, adaptation, time-bank, and multiway all-in fixtures to follow-up gates. (toy-game-validator)
- Freeze a minimal transcript schema with seed, hand id, seat, observation, legal actions, deadline, action, error code, state hash, pot layers, and payouts. (toy-game-validator)
- Map each accepted MVP rule to at least one fixture, especially action order, legal actions, side pots, odd chips, fallback legality, hidden-information filtering, and engine parity. (rules-mechanics) (toy-game-validator)
- Require protocol support for legal-action masks, deadline metadata, state hashes, and referee-only traces before treating fixture work as implementation-ready. (toy-game-validator) (agent-protocol)

## Novelty Appendix

- Keep all novelty mechanics outside MVP scoring. Time-bank market may be the first appendix experiment after baseline deadlines, fallback, replay, and raw scoring are stable, but it must not change first-arena rankings. (novelty-lane) (scoring-economy) (toy-game-validator)
- Make time-credit bids deterministic and auditable, but never a hidden-card signaling channel: bids that affect a decision must be fixed before private cards are dealt, sealed until all affected actions are locked, or reported only after the hand. Public bid timing must be fixture-tested for heads-up and multiway information leakage, and tie-breaks use seat order or hand id hash rather than wall-clock race. (novelty-lane) (toy-game-validator)
- Keep observation bandwidth draft, memory/adaptation ladder, mixed toy-game ladder, explanation tax, mirror seats, and observation compression as appendix experiments until each has fixtures and hidden-information canaries. (novelty-lane) (toy-game-validator)
- Do not score natural-language explanation quality in MVP; rationale text can be capped and logged for audit while gameplay depends only on valid JSON action. (novelty-lane) (agent-protocol)

## Risks

- No-limit min-raise, short all-in, and reopen rules are high-risk and need mandatory legal-action matrix coverage before promotion. (rules-mechanics) (toy-game-validator)
- Side-pot accounting can diverge silently from engine truth, so hand-rolled settlement should wait for parity and chip-conservation fixtures. (rules-mechanics) (toy-game-validator)
- Hidden information can leak through logs, action history, serialized engine objects, seeds, canary fields, or retained memory, so serialization should be allowlist-based and canary-tested. (rules-mechanics) (agent-protocol) (toy-game-validator) (novelty-lane)
- Latency and time-bank mechanics can reward scheduler artifacts unless deadlines use monotonic engine timestamps, deterministic fallback, and fixture evidence tolerant of small jitter. (agent-protocol) (toy-game-validator) (novelty-lane)
- Penalty coefficients, drawdown penalties, adaptation bonuses, and credit pricing can distort behavior and need calibration against scripted agents before leaderboard claims. (scoring-economy) (novelty-lane) (toy-game-validator)
- Multi-agent fixtures must include collusion-adjacent signaling checks: timing, public credit bids, invalid-output patterns, explanation fields, and repeated action oddities must not create a profitable side channel between cooperating seats. Suspected cooperative signaling should be reported as a diagnostic and excluded from primary leaderboard claims until policy is decided. (novelty-lane) (agent-protocol) (toy-game-validator)

## Residue

- Choose exact odd-chip convention, muck/show rules, soft and hard deadlines, invalid-output strike limits, seed-commitment visibility, log retention, and redaction policy. (rules-mechanics) (agent-protocol) (scoring-economy)
- Decide initial hand counts, orbit counts, provisional leaderboard threshold, tournament ROI status, time-bank credit pricing, per-hand reset policy, bandwidth categories, and adaptation windows. (scoring-economy) (novelty-lane)
- Leave tournament eliminations, table balancing, antes, straddles, run-it-twice, bomb pots, bandwidth compression, semantic explanation scoring, and full Hold'em exploitability outside MVP. (rules-mechanics) (novelty-lane) (toy-game-validator)
- Add an exploitability skeptic pass against penalty gaming, credit hoarding, intentional timeouts, compressor blind spots, and explanation spam before novelty scoring becomes primary. (scoring-economy) (novelty-lane)

## Implementation Order

1. Freeze the CLI JSON envelope, observation allowlist, authoritative legal-action objects, fallback event schema, and replay transcript fields. (agent-protocol) (rules-mechanics) (toy-game-validator)
2. Build Kuhn and Leduc fixtures for hidden information, legal actions, board reveal, invalid output, timing fallback, and canary leak detection. (toy-game-validator) (agent-protocol)
3. Add toy payout and chip-conservation fixtures. (rules-mechanics) (toy-game-validator)
4. Add seat-rotated seed-orbit scoring with raw EV, `ev_lcb95`, latency, invalid-action, risk, adaptation, and tie-break diagnostics. (scoring-economy) (toy-game-validator)
5. After selecting the Hold'em engine, add side-pot, showdown, uncalled-refund, odd-chip, and chip-conservation parity fixtures against engine truth. (rules-mechanics) (toy-game-validator)
6. Integrate the selected Hold'em engine only after toy fixtures establish the arena contract, then compare observations and pot results against engine parity fixtures. (rules-mechanics) (toy-game-validator)
7. Introduce time-bank market as an appendix fixture after baseline clocks and scoring diagnostics are stable. (novelty-lane) (scoring-economy) (toy-game-validator)
8. Keep bandwidth, memory/adaptation, mixed-game ladder, explanation tax, mirror seats, and compression challenges behind separate fixtures and side-leaderboards until MVP scoring is calibrated. (novelty-lane) (scoring-economy) (toy-game-validator)
