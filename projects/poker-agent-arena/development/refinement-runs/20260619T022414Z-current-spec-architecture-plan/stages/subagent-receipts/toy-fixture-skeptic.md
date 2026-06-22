# Toy Fixture Skeptic Receipt

Agent ID: `019eddbc-1d93-7632-952d-d990b76e22d0`
Role ID: `toy-fixture-skeptic`
Status: `flag`

## Artifacts Reviewed

- `projects/poker-agent-arena/WORK-PACK.md`
- `projects/poker-agent-arena/IMPLEMENTATION-LAYERING.md`
- `projects/poker-agent-arena/SPEC.md`
- `projects/poker-agent-arena/development/dispatches/20260619-agent-arena-mechanics/LANE-MAP.md`
- `projects/poker-agent-arena/development/dispatches/20260619-agent-arena-mechanics/DISPATCH-VALIDATION.md`
- `projects/poker-agent-arena/development/dispatches/20260619-agent-arena-mechanics/subagent-run/research.md`
- `projects/poker-agent-arena/development/dispatches/20260619-agent-arena-mechanics/subagent-run/findings.md`
- `projects/poker-agent-arena/development/dispatches/20260619-agent-arena-mechanics/subagent-run/REVIEW-REPAIR.md`
- Relevant receipts and reviews under `projects/poker-agent-arena/development/dispatches/20260619-agent-arena-mechanics/subagent-run/`

## Findings

| Severity | File | Evidence | Proposed Fix |
| --- | --- | --- | --- |
| MAJOR | `projects/poker-agent-arena/development/dispatches/20260619-agent-arena-mechanics/subagent-run/receipts/toy-game-validator.md` | Kuhn is only specified as "J/Q/K deck, one private card each, ante 1, one betting round"; Leduc as "paired J/Q/K deck, one private card, one public board card, fixed bet sizes." This is not enough to prevent fixture drift in raise caps, terminal states, payout conventions, or expected traces. | Freeze canonical Kuhn/Leduc fixture specs with rule ids, deck, ante/blind/bet sizes, raise caps, legal-action table per state, terminal payout formula, reveal timing, seed corpus, and golden transcript/payout oracles. |
| MAJOR | `projects/poker-agent-arena/SPEC.md` | Replay allows "Seed handle or commitment," while "Seed commitment visibility and public replay redaction policy" remains open. | Split transcript surfaces before schema freeze: referee replay may retain raw seed/internal state; public or agent-visible replay gets only opaque/non-predictive ids and post-match commitments under a declared redaction policy. |
| MAJOR | `projects/poker-agent-arena/WORK-PACK.md` | `SWU-PAA-001` acceptance requires named timeout/invalid codes and deterministic fallback, but abuse-proofing is deferred to later calibration fixtures. | Add an M0 abuse fixture requirement: always-timeout, always-invalid, invalid-only-when-facing-bet, and crash/EOF agents must not gain clean ranking value through fallback; fallback-derived actions must be flagged separately from agent-chosen legal actions. |
| MAJOR | `projects/poker-agent-arena/IMPLEMENTATION-LAYERING.md` | The L0 exit gate says the hidden-information canary must be absent from "agent-visible envelopes," but the dispatch evidence names logs, replay exports, state hashes, and retained material as leak surfaces too. | Broaden the canary gate to observations, legal-action payloads, action history, stdout/stderr captures, replay/public exports, state hashes, environment/log redaction, and retained memory inputs; include one injected-leak failure fixture. |
| MINOR | `projects/poker-agent-arena/SPEC.md` | "Exact soft and hard deadline defaults" are open, while timing fallback and replay determinism are M0 acceptance surfaces. | In `SWU-PAA-001`, freeze clock source, start/stop points, grace policy, timeout classification, recorded elapsed/deadline fields, and replay behavior for timeout diagnostics. |

## Residue

The toy-first boundary survived: Hold'em parity, side pots, composite scoring, novelty mechanics, and adjusted leaderboard claims are gated later. The remaining risk is ambiguity during the next contract-freeze step, not a reason to reject the direction.

## Next Route Recommendation

Proceed to `task-session` on `SWU-PAA-001` only, but make the output a concrete protocol plus fixture-spec packet that closes the five findings above before any runtime engine or scoring implementation.
