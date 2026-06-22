# Check Tension Sheet - Poker Agent Arena MVP Review Dispatch

Dispatch id: `2026-06-19-poker-agent-arena-mvp-review`
Schema version: `0.6.0`
Dispatch type: `review`
Working folder: `projects/poker-agent-arena/development/refinement-runs/20260619T143102Z-mvp-design/review-dispatch`
Final approver: `parent`
Max loops: `1`

## Goal

Review the approved Poker Agent Arena MVP refine strategy and existing project artifacts before parent synthesis. Produce concrete change requests for MVP scope, runtime architecture, fixture validation, and first-run agent-author experience.

## Context

The operator approved the proposed Refine subagent strategy by saying `run spawn subagents`. The current selected MVP route is `local-kuhn-cli-mvp`: a local CLI arena around one toy poker game with protocol, transcript, replay, diagnostics, and sample agents. Existing artifacts are planning/docs surfaces, not implementation proof; the review must keep public/product views separate from engineer/agent rule views and must avoid slipping into Hold'em-first, hosted tournaments, or composite leaderboard claims.

## Target Artifacts

- `projects/poker-agent-arena/README.md`
- `projects/poker-agent-arena/RULES.md`
- `projects/poker-agent-arena/AGENT-RULES.md`
- `projects/poker-agent-arena/SPEC.md`
- `projects/poker-agent-arena/DESIGN.md`
- `projects/poker-agent-arena/IMPLEMENTATION-LAYERING.md`
- `projects/poker-agent-arena/WORK-PACK.md`
- `projects/poker-agent-arena/docs/COMPETITOR-GUIDE.md`
- `projects/poker-agent-arena/docs/AGENT-AUTHOR-GUIDE.md`
- `projects/poker-agent-arena/development/refinement-runs/20260619T143102Z-mvp-design/REFINE-DISPATCH.json`
- `projects/poker-agent-arena/development/refinement-runs/20260619T143102Z-mvp-design/REFINE-SEED-PROPOSAL.md`
- `projects/poker-agent-arena/development/refinement-runs/20260619T143102Z-mvp-design/RUN-MANIFEST.md`
- `projects/poker-agent-arena/development/refinement-runs/20260619T143102Z-mvp-design/RUNTIME-HANDOFF.md`

## Group

Group id: `mvp-reviewers`
Anti-bias axis: `attack-vector`
Robot talks: `false`
Agents run independently. Parent collects and synthesizes receipts.

| Role id | Agent name | Role | Angle | Token budget |
| --- | --- | --- | --- | --- |
| `mvp-scope-cutter` | `Banach, Stefan` | `explorer` | `scope-minimality gate: rejects MVP creep into Hold'em, hosting, composite scoring, or nonessential polish` | 1400 |
| `runtime-architecture-mapper` | `Grothendieck, Alexander` | `explorer` | `runtime-boundary gate: maps missing CLI, referee, transcript, replay, diagnostics, and module ownership contracts` | 1600 |
| `fixture-validation-skeptic` | `Capucci, Matteo` | `explorer` | `fixture-abuse gate: attacks hidden-information safety, invalid action handling, timeout fallback, replay determinism, and scoring fixtures` | 1600 |
| `agent-author-experience-critic` | `Fong, Brendan` | `explorer` | `first-run-usability gate: checks whether a fresh agent author can run, debug, and improve a bot without internal context` | 1400 |

## Predicted Pairwise Disagreements

- `mvp-scope-cutter` runs a scope-minimality attack while `runtime-architecture-mapper` runs a runtime-boundary attack on the `attack-vector` axis; a bias toward under-building scope would be exposed by the runtime mapper's missing-contract findings.
- `mvp-scope-cutter` runs a scope-minimality attack while `fixture-validation-skeptic` runs a fixture-abuse attack on the `attack-vector` axis; a bias toward accepting too few gates would be exposed by hidden-info, fallback, and replay abuse cases.
- `mvp-scope-cutter` runs a scope-minimality attack while `agent-author-experience-critic` runs a first-run-usability attack on the `attack-vector` axis; a bias toward cutting docs and diagnostics too hard would be exposed by first-run friction findings.
- `runtime-architecture-mapper` runs a runtime-boundary attack while `fixture-validation-skeptic` runs a fixture-abuse attack on the `attack-vector` axis; a bias toward tidy module diagrams would be exposed by adversarial fixture cases that require executable checks.
- `runtime-architecture-mapper` runs a runtime-boundary attack while `agent-author-experience-critic` runs a first-run-usability attack on the `attack-vector` axis; a bias toward over-abstract architecture would be exposed by CLI and debugging friction findings.
- `fixture-validation-skeptic` runs a fixture-abuse attack while `agent-author-experience-critic` runs a first-run-usability attack on the `attack-vector` axis; a bias toward punitive validation would be exposed by missing diagnostics that prevent authors from fixing their agents.

## Agent Prompt: mvp-scope-cutter

You are the `mvp-scope-cutter` reviewer for Poker Agent Arena. Work read-only. Do not edit files. Attack the approved `local-kuhn-cli-mvp` from a scope-minimality lens.

Read the target artifacts named in `projects/poker-agent-arena/development/refinement-runs/20260619T143102Z-mvp-design/review-dispatch/check-tension-sheet.md`, especially `SPEC.md`, `DESIGN.md`, `WORK-PACK.md`, `RULES.md`, `AGENT-RULES.md`, and `REFINE-DISPATCH.json`.

Return a markdown receipt only, with:

- Status: `pass`, `flag`, or `block`
- Findings table: severity, file, evidence, proposed fix
- Smallest credible MVP boundary
- Premature features to defer
- Acceptance gates that must remain
- One paragraph handoff to parent synthesis

Prioritize concrete file-backed change requests. Quote short evidence snippets and cite paths. Do not propose implementation work beyond the design/plan level.

## Agent Prompt: runtime-architecture-mapper

You are the `runtime-architecture-mapper` reviewer for Poker Agent Arena. Work read-only. Do not edit files. Attack the MVP from a runtime-boundary lens.

Read the target artifacts named in `projects/poker-agent-arena/development/refinement-runs/20260619T143102Z-mvp-design/review-dispatch/check-tension-sheet.md`, especially `DESIGN.md`, `IMPLEMENTATION-LAYERING.md`, `WORK-PACK.md`, `SPEC.md`, `AGENT-RULES.md`, and `REFINE-DISPATCH.json`.

Return a markdown receipt only, with:

- Status: `pass`, `flag`, or `block`
- Findings table: severity, file, evidence, proposed fix
- Minimum component catalog for CLI, runner, protocol adapter, referee, transcript, replay, fixtures, diagnostics, and sample agents
- Interface gaps or ownership ambiguities
- File-tree recommendation for an MVP implementation
- One paragraph handoff to parent synthesis

Prioritize concrete file-backed change requests. Quote short evidence snippets and cite paths. Do not implement code.

## Agent Prompt: fixture-validation-skeptic

You are the `fixture-validation-skeptic` reviewer for Poker Agent Arena. Work read-only. Do not edit files. Attack the MVP from a fixture-abuse lens.

Read the target artifacts named in `projects/poker-agent-arena/development/refinement-runs/20260619T143102Z-mvp-design/review-dispatch/check-tension-sheet.md`, especially `AGENT-RULES.md`, `SPEC.md`, `DESIGN.md`, `WORK-PACK.md`, `RULES.md`, and `REFINE-DISPATCH.json`.

Return a markdown receipt only, with:

- Status: `pass`, `flag`, or `block`
- Findings table: severity, file, evidence, proposed fix
- Abuse cases for hidden information, invalid actions, stdout/stderr protocol drift, timeout fallback, replay determinism, and scoring
- Minimum golden transcripts and fixture agents
- Validation gates that should block MVP acceptance
- One paragraph handoff to parent synthesis

Prioritize concrete file-backed change requests. Quote short evidence snippets and cite paths. Do not implement code.

## Agent Prompt: agent-author-experience-critic

You are the `agent-author-experience-critic` reviewer for Poker Agent Arena. Work read-only. Do not edit files. Attack the MVP from a first-run usability lens.

Read the target artifacts named in `projects/poker-agent-arena/development/refinement-runs/20260619T143102Z-mvp-design/review-dispatch/check-tension-sheet.md`, especially `README.md`, `docs/AGENT-AUTHOR-GUIDE.md`, `AGENT-RULES.md`, `RULES.md`, `SPEC.md`, `DESIGN.md`, and `WORK-PACK.md`.

Return a markdown receipt only, with:

- Status: `pass`, `flag`, or `block`
- Findings table: severity, file, evidence, proposed fix
- First-run path for an agent author
- Missing diagnostics or examples
- Human/product view vs engineer/agent view drift
- One paragraph handoff to parent synthesis

Prioritize concrete file-backed change requests. Quote short evidence snippets and cite paths. Do not implement code.
