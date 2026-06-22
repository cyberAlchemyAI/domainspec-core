# Scoring/Economy Receipt

dispatch_id: 2026-06-19-poker-agent-arena-mechanics
role_id: scoring-economy
spawn_status: spawned
join_status: completed
close_status: closed
status: pass

## Proposed scoring

Claim boundary: this is a measurable first scoring proposal, not a validated tournament model. Coefficients below should be treated as MVP defaults until toy-game checks calibrate them.

Use a zero-rake virtual economy. In-hand chips remain zero-sum except forced timeout/invalid fallbacks; leaderboard penalties are applied after the hand ledger so the engine can debug poker EV separately from operations reliability.

Primary unit: `net_bb_per_100 = 100 * net_big_blinds / hands_played`. For tournament-style wrappers, also report `roi = net_payout / total_buyin`, but do not make ROI primary until payout fixtures exist. MVP ranking should use adjusted cash EV because it is easier to seed, replay, and compare.

Evaluation is grouped into seed orbits. For each base seed, run all seat rotations so every agent occupies every seat against the same lineup and deterministic deck/action environment. Score each agent by the mean of its orbit results, not by isolated hands. Publish `mean_bb100`, clustered standard error by seed orbit, and `ev_lcb95 = mean_bb100 - 1.96 * clustered_se`.

Leaderboard score:

`arena_score = ev_lcb95 - latency_penalty - invalid_penalty - risk_penalty + adaptation_bonus`

Keep the score in bb/100-equivalent units so every component is visible and auditable.

Variance control:

- Minimum publishable batch: enough completed seed orbits that each agent has equal seat exposure.
- A leaderboard row is provisional until `clustered_se <= 1.0 bb/100` or a declared maximum hand cap is reached.
- Report both adjusted score and raw mean. Do not hide high variance behind one number.
- Include reference bots: always-fold/check, legal-random, simple value-bet/call, and a known deterministic baseline.

Latency and timeout:

- Each decision has a soft deadline and hard deadline defined by the rules lane.
- Under soft deadline: no penalty.
- Over soft but before hard: subtract `0.02 bb` per decision-second over soft, normalized into bb/100.
- Hard timeout: engine chooses `check` if legal, otherwise `fold`; subtract an additional `0.5 bb` per timeout, normalized into bb/100.
- Publish `p50_ms`, `p95_ms`, `timeout_rate`, and total latency penalty.

Invalid-action reliability:

- Invalid JSON, schema mismatch, illegal amount, illegal action, or action after deadline all count.
- Fallback is deterministic: `check` if legal, otherwise `fold`.
- Penalty: subtract `1.0 bb` per invalid action, normalized into bb/100.
- Reliability gate: flag an agent above `0.5%` invalid decisions; block/DQ above `2%` invalid decisions or any attempt to access forbidden hidden state.

Drawdown/risk:

- Track a virtual 1000bb bankroll per evaluation run while still allowing auto top-up for continued measurement.
- Publish max drawdown percentage, ruin count where bankroll crosses zero, and worst 5% seed-orbit CVaR.
- Penalty: subtract `0.1 bb/100` for each percentage point of max drawdown above 35%, plus `2.0 bb/100` per ruin event per 10k hands.
- This should punish brittle lottery agents without deleting legitimate high-EV aggression.

Adaptation:

- Divide the schedule into equal chronological blocks after seat rotation balancing.
- Compute `adaptation_delta = paired_ev_bb100(last_quarter) - paired_ev_bb100(first_quarter)` against the same opponent family mix.
- Bonus is `clamp(0.10 * adaptation_delta, -1.0, +1.0)`.
- Only public history may support adaptation. No opponent labels, seed identifiers, deck internals, or future-state hints.

Tie-breakers, in order:

1. Higher adjusted `arena_score`.
2. Higher raw `ev_lcb95`.
3. Better paired head-to-head EV over shared seed orbits.
4. Lower invalid decision rate.
5. Lower hard timeout rate.
6. Better worst-seat EV after rotation.
7. Lower max drawdown and CVaR loss.
8. Lower p95 decision latency.
9. Higher adaptation delta.

## Toy-game checks needed

- Seat-rotation invariant: identical deterministic agents should tie after a full rotation orbit.
- Variance shrink check: doubling seed orbits should reduce clustered SE in the expected direction.
- Timeout fixture: a strong but slow agent should lose leaderboard score even if raw EV is positive.
- Invalid-action fixture: always-invalid and malformed-output agents should fall back deterministically, accrue penalties, and cross the DQ gate.
- Risk fixture: compare steady small-edge strategy vs all-in lottery strategy; risk penalty should not overturn a clearly higher confident EV, but should break close ties toward robustness.
- Adaptation fixture: an agent that uses public action history against a stationary exploitable bot should earn a small capped bonus; shuffled block order should erase the measured bonus.
- Hidden-information fixture: trace observations to prove no private cards, deck order, seed IDs, or future board cards reach the agent.
- Tie-breaker fixture: create equal-EV agents with different latency/invalid/drawdown profiles and verify ordering.

## Risks/blockers/residue

No blocker for MVP design. Main risks are calibration risks: coefficients can over-penalize LLM-style agents, drawdown penalties can suppress valid aggressive poker, and adaptation can accidentally reward overfitting to seeded opponents. Residue for parent synthesis: choose soft/hard deadline values, choose initial hand/orbit counts, decide whether tournament ROI remains report-only or becomes a second leaderboard, and require the exploitability lane to attack penalty gaming.

## Handoff_note

Use `ev_lcb95` over seat-rotated seeded orbits as the primary quantitative signal. Keep penalties post-ledger, visible, and small enough to calibrate. The toy-game validator should verify invariants before any full no-limit Hold'em mechanics are promoted into the handoff.
