# MVP Scope Cutter Receipt

Agent id: `019ee093-8a7a-75e0-a043-a8e6b6c3fcf9`
Role id: `mvp-scope-cutter`
Agent name: `Banach, Stefan`
Status: `flag`

## Findings

| Severity | File | Evidence | Proposed fix |
| --- | --- | --- | --- |
| major | `REFINE-DISPATCH.json`, `SPEC.md` | Selected route is `local-kuhn-cli-mvp`, "one toy poker game," but M0 says "Kuhn and Leduc fixtures." | Preserve the selected route by making Kuhn the MVP-required game and moving Leduc to the first post-MVP extension, or explicitly rename the route to `kuhn-leduc-cli-mvp`. |
| major | `WORK-PACK.md` | Raw scoring diagnostics depend on both `SWU-PAA-002` and `SWU-PAA-003`, so a Kuhn MVP cannot report EV until Leduc exists. | Split diagnostics: Kuhn raw EV/replay diagnostics depend on `SWU-PAA-002`; Leduc diagnostics become an extension after `SWU-PAA-003`. |
| major | `IMPLEMENTATION-LAYERING.md`, `AGENT-RULES.md` | L0 exit requires "Kuhn and Leduc fixtures pass," and the fixture set "must include" Leduc. | Change L0 MVP gate to Kuhn plus protocol/fallback/replay proof. Keep Leduc as a named next gate for board-reveal coverage. |
| medium | `IMPLEMENTATION-LAYERING.md`, `WORK-PACK.md` | First L0 demands a broad fallback-abuse matrix: timeout, invalid, invalid-facing-bet, crash, EOF. | For MVP, require one timeout and one invalid-output abuse path proving fallback is not score-improving. Defer crash/EOF and invalid-facing-bet variants to calibration hardening. |
| medium | `IMPLEMENTATION-LAYERING.md`, `README.md` | Current recommendation says "Start with L0," while current first route is `SWU-PAA-001R`. | Reword the recommendation: start with L0R contract repair, then execute the Kuhn-only L0 runtime slice. |

## Smallest Credible MVP Boundary

A credible `local-kuhn-cli-mvp` is Kuhn-only: local CLI process runner, line-delimited JSON decision/action envelopes, observation allowlist, referee-owned legal actions, deterministic timeout/invalid fallback, private transcript plus redacted replay split, replay verification, and raw Kuhn chip EV with timeout/invalid/replay diagnostics. Leduc is useful, but it is not part of the smallest selected route.

## Premature Features To Defer

Defer Leduc board-reveal fixtures, Hold'em engine selection, hosted matchmaking, WebSocket parity, real-money language, composite `arena_score`, `ev_lcb95`, penalty coefficients, novelty/time-bank mechanics, full adversarial bot suite, and broad crash/EOF abuse variants.

## Acceptance Gates That Must Remain

Keep hidden-information denial, authoritative legal actions, invalid/timeout event logging, deterministic fallback, replay determinism, raw EV separated from diagnostics, referee transcript versus public replay split, no composite leaderboard, and the `RULES.md` versus `AGENT-RULES.md` authority split.

## Handoff To Parent Synthesis

Parent synthesis should accept the local Kuhn route only after repairing the M0/L0 wording so "MVP" no longer silently means Kuhn plus Leduc. The clean move is Kuhn-first with Leduc preserved as an explicit next-stage validation extension, while keeping the hard safety gates around hidden information, fallback abuse, replay, and non-leaderboard diagnostics.
