# Agent Author Experience Critic Receipt

Agent id: `019ee093-90b5-7a43-944d-09a42330da24`
Role id: `agent-author-experience-critic`
Agent name: `Fong, Brendan`
Status: `flag`

## Findings

| Severity | File | Evidence | Proposed fix |
| --- | --- | --- | --- |
| major | `README.md`, `docs/AGENT-AUTHOR-GUIDE.md` | README "Start Here" only routes to docs; author guide says it is for "before the L0 protocol files exist." | Add an MVP quickstart path: run bundled Kuhn match, validate a custom agent, replay transcript, inspect diagnostics. |
| major | `docs/AGENT-AUTHOR-GUIDE.md`, `WORK-PACK.md` | Guide lists fields, while examples are only future acceptance: "Example decision envelope and action envelope exist." | Put canonical minimal Kuhn decision/action JSON examples and invalid examples directly in the author guide or linked `spec/l0/` docs. |
| major | `REFINE-DISPATCH.json`, `README.md`, `docs/AGENT-AUTHOR-GUIDE.md` | Selected MVP is "Local Kuhn CLI MVP," but public/author docs still say M0 uses "Kuhn and Leduc fixtures." | Split wording into `MVP0: Kuhn-first local CLI` and later `M0/L0 fixture expansion: Kuhn + Leduc`, so authors know the first target. |
| major | `REFINE-SEED-PROPOSAL.md`, `IMPLEMENTATION-LAYERING.md` | Seed says MVP likely includes "minimal sample agents," but `legal-random` and reference bots appear under L2 leaderboard work. | Move minimal onboarding agents into L0/MVP acceptance: legal-random, check/fold, timeout, invalid-output, crash/EOF. Keep calibrated reference-bot ranking in L2. |
| major | `AGENT-RULES.md`, `DESIGN.md`, `WORK-PACK.md` | Diagnostics are named, but no author-facing event-code/output shape exists. | Add diagnostics examples: event code, cause, stdout/stderr snippet, fallback action, transcript path, and suggested fix. |
| major | `SPEC.md`, `AGENT-RULES.md` | Timing defaults remain open while rules already require deadline behavior. | Freeze MVP author defaults for soft/hard timeout, grace, clock source, and local timeout test fixture before first-run docs claim usability. |
| minor | `docs/COMPETITOR-GUIDE.md`, `DESIGN.md` | "Eventually, a submitted entry is an executable agent process," but runner inputs mention package/argv/env without author syntax. | Define one submission shape: command string or manifest, argv/env allowlist, cwd, exit/EOF behavior, and sample invocation. |

## First-Run Path For An Agent Author

Current path is conceptual, not runnable: README points to rule/docs, the author guide explains the loop, then the author must infer schema details from `AGENT-RULES.md`, `SPEC.md`, `DESIGN.md`, and `WORK-PACK.md`. A credible first-run path should be: read README quickstart, run bundled Kuhn match with sample agents, inspect one decision envelope, run a custom agent through validation, replay the transcript, then read diagnostics for invalid/timeout behavior.

## Missing Diagnostics Or Examples

Missing: concrete decision JSON, action JSON, legal action representation, CLI command examples, custom-agent validation command, minimal valid sample agent, invalid-output sample agent, timeout sample agent, diagnostic event schema, replay artifact example, public-vs-referee transcript example, and a troubleshooting table that maps failures to fixes.

## Human/Product Vs Engineer/Agent View Drift

The human/product docs communicate a polished contract-first arena, but the engineer/agent path still requires internal planning context to answer "what do I run first?" The biggest drift is MVP naming: the refine dispatch selects a one-game local Kuhn CLI MVP, while README/spec/author guide still describe Kuhn plus Leduc as the active M0 fixture shape.

## Handoff To Parent Synthesis

Treat this as a `flag`, not a scope rejection: the local Kuhn CLI MVP is the right author-friendly cut, but parent synthesis should make first-run usability a gate for the next executable plan. Require the first MVP SWU to ship quickstart commands, sample agents, JSON examples, diagnostic examples, and timing defaults alongside the protocol/replay contract.
