# Local Arena CLI v0 Implementation Stream

Status: parent refine synthesis
Input evidence:

- `review-dispatch/findings.md`
- `naming-observer-receipt.md`
- `../../../WORK-PACK.md`
- `../../../MVP-PATH.md`

## Synthesis

The review findings do not block design continuation. They do block MVP acceptance. The fix is to stop treating Kuhn, Leduc, Hold'em, scoring, and novelty as peer tracks and make one executable line:

```text
handoff repair -> contract freeze -> local runner + Kuhn -> replay/diagnostics -> author proof
```

`local-arena-cli-v0` remains the route id. Kuhn is the first fixture gate. Leduc is the first post-MVP validation expansion.

## Accepted Review Pressure

| Pressure | Parent Decision |
| --- | --- |
| Route language drifted between Kuhn-only and Kuhn-plus-Leduc. | Keep `Local Arena CLI v0`; demote games to fixture names. |
| Runtime root and CLI command shape were missing. | Recommend `src/poker_agent_arena/` and `paa doctor/run/eval/replay`. |
| Timing and fallback were prose-level. | Recommend 5s decision timeout, 10s process cleanup, monotonic clock, and passive deterministic fallback. |
| Replay, redaction, diagnostics, and canary scope were not schema-level. | Make these blockers for MVP acceptance. |
| Agent author path was conceptual. | Add sample agents, canonical JSON examples, diagnostics examples, and quickstart as MVP requirements. |

## Blockers Before Runtime Code

Runtime implementation remains blocked until `SWU-PAA-001R` and `SWU-PAA-001` pass. The next task-session must not start by writing the runner; it must first freeze the contract files that make the runner testable.

Required pre-code contracts:

- `spec/l0/runtime/cli.md`
- `spec/l0/runtime/match-config.md`
- `spec/l0/runtime/process-lifecycle.md`
- `spec/l0/protocol/decision-envelope.md`
- `spec/l0/protocol/action-envelope.md`
- `spec/l0/protocol/legal-actions.md`
- `spec/l0/protocol/invalid-events.md`
- `spec/l0/protocol/deadline-policy.md`
- `spec/l0/protocol/fallback-policy.md`
- `spec/l0/transcript/referee-transcript.md`
- `spec/l0/transcript/public-replay.md`
- `spec/l0/transcript/redaction-policy.md`
- `spec/l0/diagnostics/report-schema.md`
- `spec/l0/fixtures/kuhn-hidden-info.md`

## MVP Acceptance Gate

The first accepted MVP proof is a local run that:

- runs bundled sample agents through Kuhn,
- produces private transcript material,
- exports redacted public replay,
- replays deterministically,
- reports clean EV and fallback-inclusive EV separately,
- records invalid/timeout/fallback diagnostics,
- passes hidden-information canary scans,
- shows that abuse fixtures cannot improve displayed rank through protocol failure.

## Follow-On Work

Leduc board reveal, Hold'em engine parity, calibrated leaderboard scoring, and time-bank or other novelty mechanics remain useful, but they are not part of the first implementation line. They should be invoked only after Local Arena CLI v0 reaches MVP acceptance or after an explicit operator override.
