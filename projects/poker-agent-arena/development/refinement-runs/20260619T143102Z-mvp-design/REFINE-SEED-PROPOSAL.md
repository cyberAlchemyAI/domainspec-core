# Refine Seed Proposal - Poker Agent Arena MVP Design

Run id: `20260619T143102Z-mvp-design`
Target: `projects/poker-agent-arena`
Preset: `standard`
Research mode: `research-if-gap-appears`
Mutation mode: strategy proposal only; no runtime-backed stages or subagents have been executed.

## Operator Intent

Use DomainSpec/Arcanum refinement to design everything necessary for a Poker Agent Arena MVP.

## Desired Outcome

Produce an MVP-ready, non-executed design and plan that tells a future `task-session` exactly what to build, what to leave out, and how to prove the MVP works.

## Current Evidence Baseline

The target already has:

- Product and agent-facing documentation: `README.md`, `RULES.md`, `AGENT-RULES.md`, `docs/COMPETITOR-GUIDE.md`, `docs/AGENT-AUTHOR-GUIDE.md`.
- Core specification and architecture: `SPEC.md`, `DESIGN.md`, `IMPLEMENTATION-LAYERING.md`, `WORK-PACK.md`.
- Prior mechanics dispatch evidence under `development/dispatches/20260619-agent-arena-mechanics/`.
- Prior refinement evidence under `development/refinement-runs/20260619T022414Z-current-spec-architecture-plan/`.
- Whisper voice preset under `development/whisper/presets/quiet-table-stakes.md`.

## MVP Boundary Hypothesis

The MVP should be a local, toy-game-first CLI arena, not a hosted tournament, full Hold'em implementation, or final leaderboard.

The likely MVP includes:

1. Agent process runner with stdin/stdout JSON lines.
2. Versioned decision and action envelopes.
3. Observation allowlist and referee-only denial list.
4. A minimal game authority for at least Kuhn poker, with Leduc either included or explicitly staged behind the first working path.
5. Legal-action generation owned by the referee.
6. Timeout, invalid-output, crash, and EOF handling with deterministic fallback.
7. Referee transcript and redacted public replay split.
8. Replay verifier for deterministic reproduction of payouts and diagnostics.
9. Raw diagnostic scoring: chip EV, timeout rate, invalid-decision rate, fallback count, replay determinism.
10. Fixture pack for hidden-information canaries, invalid output, timeout fallback, fallback abuse, and seat rotation.
11. Minimal sample agents: legal-random, always-check/fold where legal, timeout, invalid-output, crash/EOF.
12. CLI commands for running a match/evaluation and writing artifacts.

The likely MVP excludes:

- Full no-limit Hold'em.
- Hosted matchmaking.
- Real-money play.
- Composite `arena_score`.
- Penalty coefficient calibration.
- Novelty mechanics in primary ranking.

## DomainSpec Component Families

The refinement should produce a domain design across these families:

| Domain | MVP Question | Evidence Needed |
| --- | --- | --- |
| Product promise | What does the MVP let a reader or entrant understand and try? | Human/agent docs and non-goals remain aligned. |
| Agent protocol | What must an agent read and write? | Decision/action schemas and examples. |
| Game authority | Which rules are authoritative in MVP? | Toy game rules, legal-action tables, payout formulas. |
| Hidden information | What is visible, private, or referee-only? | Observation allowlist, namespace matrix, canary fixtures. |
| Runtime CLI | How does a user run local matches? | CLI command contract, input/output paths, process lifecycle. |
| Transcript/replay | What gets recorded and what can be shared? | Referee transcript schema, public replay schema, redaction policy. |
| Failure handling | What happens on bad output or no output? | Invalid event catalog, timeout policy, deterministic fallback. |
| Evaluation | What is measured before leaderboard claims? | Raw EV and diagnostics, no composite score. |
| Fixtures | How is correctness falsified cheaply? | Kuhn fixture gate first, staged Leduc board-reveal expansion, golden transcripts, abuse agents. |
| Developer experience | What does an agent author need first? | Sample agents, README path, local run instructions. |

## Done Criteria For The Full Refine Run

The confirmed run should produce:

- MVP boundary decision and rejected alternatives.
- MVP domain model and component catalog.
- MVP architecture with module/interface ownership.
- MVP protocol and transcript artifact plan.
- MVP fixture and validation plan.
- MVP work-pack with SWUs small enough for task-session execution.
- A final recommendation for the first executable route.

## Validation Surface

The full run should validate:

- Dispatch route shape with `dispatch-spec`.
- All ten Refine stages have artifacts or blocked reasons.
- Subagent receipts are collected if approved.
- MVP scope excludes Hold'em, hosting, real money, and composite scoring unless explicitly deferred.
- Every proposed MVP component has at least one acceptance check.
- The final plan preserves public/private repository boundaries and the two rule views.

## Planned Stage Configuration

Use the canonical ten-stage Refine loop:

1. Context Builder evidence baseline.
2. Invoke Define.
3. Interrogation refine-review.
4. Research decision.
5. Distill.
6. Invoke Redefine / Design.
7. Interrogation refine-design-review.
8. Distill Repair.
9. Invoke Plan.
10. Final Interrogation and Refine-owned synthesis.

Runtime execution is blocked until operator confirmation.
