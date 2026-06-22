# Review Dispatch Findings

Dispatch ID: `2026-06-19-poker-agent-arena-refine-review`
Status: `flag`

## Surviving Findings

| # | Source | Severity | File | Change Request |
| --- | --- | --- | --- | --- |
| 1 | spec-boundary-critic | MAJOR | `development/dispatches/20260619-agent-arena-mechanics/LANE-MAP.md` | Add or update an execution manifest that distinguishes route-preview validation from approved subagent execution. |
| 2 | spec-boundary-critic | MAJOR | `development/dispatches/20260619-agent-arena-mechanics/subagent-run/findings.md` | Demote adjusted EV, `ev_lcb95`, risk, and adaptation language out of M0. |
| 3 | spec-boundary-critic, toy-fixture-skeptic | MAJOR | `development/dispatches/20260619-agent-arena-mechanics/subagent-run/receipts/toy-game-validator.md`, `SPEC.md` | Split referee transcript from public/agent replay schema; raw seed stays referee-only, exported replay uses opaque handles or post-match commitments. |
| 4 | spec-boundary-critic | MINOR | `development/dispatches/20260619-agent-arena-mechanics/subagent-run/receipts/agent-protocol.md` | Replace structured/predictive id examples with opaque ids. |
| 5 | architecture-component-mapper | MAJOR | `WORK-PACK.md` | Add a concrete L0 output tree for `SWU-PAA-001`. |
| 6 | architecture-component-mapper | MAJOR | `DESIGN.md` | Add an L0 x-ray component map with inputs, outputs, owned state, forbidden state, schema dependency, and replay responsibility. |
| 7 | architecture-component-mapper | MAJOR | `DESIGN.md` | Add a state namespace matrix for referee truth, agent observation, action protocol, private transcript, public transcript, and diagnostics. |
| 8 | architecture-component-mapper | MINOR | `IMPLEMENTATION-LAYERING.md` | Separate replay-required transcript fields from scoring-derived diagnostics. |
| 9 | toy-fixture-skeptic | MAJOR | `development/dispatches/20260619-agent-arena-mechanics/subagent-run/receipts/toy-game-validator.md` | Freeze canonical Kuhn/Leduc fixture specs with rule ids, legal-action tables, terminal payout formulas, seed corpus, and golden transcript/payout oracles. |
| 10 | toy-fixture-skeptic | MAJOR | `WORK-PACK.md` | Add M0 abuse fixtures for timeout/invalid/crash fallback gaming. |
| 11 | toy-fixture-skeptic | MAJOR | `IMPLEMENTATION-LAYERING.md` | Broaden hidden-information canary gates beyond agent-visible envelopes to logs, replay exports, state hashes, retained memory inputs, and redaction surfaces. |
| 12 | toy-fixture-skeptic | MINOR | `SPEC.md` | Freeze timing semantics for clock source, start/stop points, grace policy, timeout classification, and replay diagnostics. |

## Verdict

The current spec, architecture, and plan are directionally sound but not task-session-ready for runtime mutation. They are ready for a small root-artifact repair pass that turns `SWU-PAA-001` into a concrete protocol/schema/fixture packet.
