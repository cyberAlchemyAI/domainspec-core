# Invoke Result: Poker Agent Arena

Mode: composed define/design/plan first artifacts, refreshed via `invoke refresh`
Status: `flag`

## Inputs

- User intent: create first Invoke artifacts from the existing poker-agent arena mechanics work.
- Dispatch packet: `development/dispatches/20260619-agent-arena-mechanics/poker-agent-arena-mechanics.dispatch.json`
- Synthesis: `development/dispatches/20260619-agent-arena-mechanics/subagent-run/findings.md`
- Explorer research: `development/dispatches/20260619-agent-arena-mechanics/subagent-run/research.md`
- Review repair: `development/dispatches/20260619-agent-arena-mechanics/subagent-run/REVIEW-REPAIR.md`

## Outputs

- `SPEC.md`
- `RULES.md`
- `AGENT-RULES.md`
- `GLOSSARY.md`
- `DESIGN.md`
- `IMPLEMENTATION-LAYERING.md`
- `NAMING.md`
- `WORK-PACK.md`
- `INVOKE-RESULT.md`

## Phase Judgment

The first artifact bundle was reviewed by Refine and refreshed. The status remains `flag`, not `pass`, because the next route is a root-artifact repair (`SWU-PAA-001R`) before the bounded `Local Arena CLI v0` task-session (`SWU-PAA-001`).

## Accepted Baseline

- `Local Arena CLI v0` is the first executable local CLI arena route.
- Kuhn is the first fixture gate; Leduc board reveal is the staged expansion.
- Agent transport is line-delimited JSON over stdin/stdout.
- The referee emits authoritative legal actions.
- Observation projection is allowlist-based.
- Invalid output and timeout continue through deterministic fallback but remain diagnostic events.
- Local Arena CLI v0 scoring is raw toy EV plus timeout, invalid-decision, fallback, and replay diagnostics.
- Hold'em engine parity, adjusted leaderboard scoring, adaptation, and novelty mechanics are follow-up gates.

## Refresh Update

Source: `development/refinement-runs/20260619T022414Z-current-spec-architecture-plan/RESULT.md`

Applied refresh deltas:

- Added L0 output tree expectations.
- Added two rule views: human/product and engineer/agent.
- Added component and state namespace requirements.
- Split referee transcript from public replay.
- Added project naming convention in `NAMING.md`.
- Split fixture language into Kuhn fixture gate and staged Leduc board-reveal expansion.
- Added fallback-abuse, broad canary, and timing policy requirements.
- Changed the immediate next route from `SWU-PAA-001` to `SWU-PAA-001R`.

## Next Route

Use `task-session` for `SWU-PAA-001R: Repair Local Arena CLI v0 Handoff`.

After `SWU-PAA-001R` passes, use `task-session` for `SWU-PAA-001: Freeze Local Arena CLI v0 Contract`. Neither route should implement a full Hold'em engine or enable composite leaderboard scoring.
