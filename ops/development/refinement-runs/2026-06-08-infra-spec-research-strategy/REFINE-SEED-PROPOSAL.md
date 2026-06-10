# Refine Seed Proposal: Infra-Spec Research Strategy

Date: 2026-06-08
Target: `ops/` runtime-surface convergence program — the research/governance strategy that drives it
Desired outcome: a refined, MVP-ready research strategy materialized as a validated dispatch route at `ops/development/infra-spec-research-strategy.dispatch.json`, plus Refine `RESULT.md` synthesis
Preset: full
Research mode: research-if-gap-appears
Status: seed-ready

## Intent

Refine the research strategy for the Arcanum/DomainSpec **runtime-surface convergence** program (the "infra spec") and see if we can make it better.

Today the program exists as a sprawl of `ops/` policy, map, inventory, and per-task artifacts plus several prior refine/invoke/task-session runs, but there is **no single governing research strategy** that says: what questions the program is answering, in what order, with which owners, against which evidence, and how convergence is decided. The operator request — "infra spec research strategy, see if we can make it better" — names the strategy itself as the refinement target and a concrete output path for the result.

The output should improve on the scattered prior artifacts by producing one coherent, owner-aware, source-backed research strategy that reconciles the three currently-unreconciled workstreams into a single migration track and records the open tensions as governed residue rather than losing them.

## Source Context

- `ops/RUNTIME-SURFACE-CONVERGENCE-REFINE.md`: prior compact refine that found the workstreams convergent-but-unreconciled and listed explicit tension points and remaining work. Primary input.
- `ops/SKILLS-FIRST-RUNTIME-POLICY.md`: skills-are-default-surface decision and validation rules.
- `ops/SURFACE-OWNER-BOUNDARIES.md`: owner map protecting nested Arcanum, DomainSpec, project, and validation surfaces from parent sweep.
- `ops/ARCANUM-SURFACE-MAP-AND-PLAN.md`, `ops/RUNTIME-SURFACE-INVENTORY.md`, `ops/ARCANUM-STATE-CLASSIFICATION.md`: existing surface mapping and classification evidence.
- `ops/CODEX-SKILL-SURFACE-POLICY.md`, `ops/ROOT-GITHUB-SKILLS-CLASSIFICATION.md`, `ops/DUPLICATE-SKILL-PRUNING-PLAN.md`: skill-surface and pruning policy inputs.
- `ops/REPOSITORY-ORGANIZATION-DESIGN.md`, `ops/REPOSITORY-ORGANIZATION-INVOKE-PLAN.md`: broader repo-organization design the runtime policy narrows.
- `ops/development/TASK-SESSION-RUNTIME-00*.md`, `ops/development/TASK-SESSION-SURFACE-00*.md`: prior bounded execution sessions (memory/residue source).
- `arcanum/formulae/dispatch-spec/development/ORCHESTRATION-RUNTIME-PLAN.md` (referenced): the orchestration runtime plan the cleanup must reconcile with (read if present; treat as a named external-to-ops input).
- Existing dispatch routes as shape references: `ops/development/domainspec-lean-formalization-glossary-refresh.dispatch.json`, `projects/ontologize/ontologize-research.dispatch.json`.

## Refinement Questions

1. What is the single migration track that unifies skill-surface cleanup, new-user install profiles, and orchestration-runtime convergence — and what research questions does each lane own?
2. Which of the recorded tensions (one-Codex-surface vs new-user install; `.github/skills` cleanup vs Copilot distribution; deleted commands vs ORCH write scopes; Refine `tools/arcanum --exec` vs native receipts; unpackaged new-user setup) are decidable now, and which must persist as governed residue?
3. What is the evidence/owner-boundary discipline the strategy must enforce so research never mutates child-owned surfaces or treats command wrappers as install proof?
4. What is the smallest MVP-ready strategy unit that is genuinely better than the status quo, and what is the next route after it?

## Constraints

- Preserve owner boundaries from `ops/SURFACE-OWNER-BOUNDARIES.md`: this refinement may write only parent-owned `ops/` strategy artifacts; it must not mutate nested Arcanum, DomainSpec, project, or validation surfaces.
- Do not execute any cleanup, pruning, install, or migration action during refinement — strategy/design only.
- Local-first: external research only if a named gap appears and the operator confirms.
- Do not treat command surfaces as canonical; honor the skills-first policy.
- Preserve, do not flatten, the recorded tensions — unresolved tensions become residue with an owner or next route.
- The dispatch route artifact must validate against `dispatch.schema.yml` before any runtime-backed stage execution.

## Done Criteria

- Final synthesis names one unified research strategy / migration track with per-lane owned research questions.
- Each recorded tension is classified decide-now vs residue, with an owner or next route.
- The strategy enforces owner-boundary and evidence discipline explicitly.
- A validated `infra-spec-research-strategy.dispatch.json` route is produced (or its blocked fields recorded).
- Next-route recommendations are given but not executed.

## Planned Stage Configuration (canonical ten-stage loop)

1. Context Builder evidence baseline: capability `context-builder`, mode `standard` (`--strict --emit both --handoff runtime --persist <run-folder>/context-builder`).
2. Invoke Define: capability `invoke`, mode `define`.
3. Interrogation refine-review: capability `interrogation`, mode `refine-review`.
4. Research decision: Refine-owned, mode `research-if-gap-appears`.
5. Distill: capability `distill`, mode `standard` (tournament over candidate strategy framings).
6. Invoke Redefine / Design: capability `invoke`, mode `design`.
7. Interrogation refine-design-review: capability `interrogation`, mode `refine-design-review`.
8. Distill Repair: capability `distill`, mode `validate`.
9. Invoke Plan: capability `invoke`, mode `plan` (non-executed; emits the strategy dispatch route).
10. Final Interrogation and Synthesis: capability `interrogation`, mode `refine-final`, then Refine-owned synthesis.
