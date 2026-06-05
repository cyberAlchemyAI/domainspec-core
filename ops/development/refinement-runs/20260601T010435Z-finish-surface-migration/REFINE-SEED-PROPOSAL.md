# Refine Seed Proposal: Finish Surface Migration

Date: 2026-06-01
Preset: compact
Research: no-research
Target: finish Arcanum repository organization and runtime surface migration

## Objective

Resolve the remaining blocker and convert accepted cleanup policies into a clear finish path for:

- GitHub/Copilot Arcanum package regeneration,
- `.arcanum/runtimes/github-copilot` cache handling,
- legacy command adapter cleanup,
- root `.arcanum` generated-state cleanup,
- legacy Arcanum-name cleanup such as `sigils-library`.

## Current State

Already passed:

- `TASK-SURFACE-001`: native-first contract recorded.
- `TASK-SURFACE-002`: personal Codex skills regenerated, backed up, and promoted.
- `TASK-PKG-001`: generated native packages now copy support directories for canonical packages while aliases remain thin.

Current blocker:

- `TASK-SURFACE-003`: root GitHub/Copilot regeneration is blocked by package naming shape.

## Source Context

- `ops/ARCANUM-SURFACE-MAP-AND-PLAN.md`
- `ops/development/TASK-SESSION-SURFACE-003.md`
- `docs/decisions/surface-cleanup-blocker-decisions.md`
- `docs/decisions/native-runtime-skill-surface.md`
- `docs/decisions/install-profile-contract.md`
- `ops/ROOT-GITHUB-SKILLS-CLASSIFICATION.md`
- `ops/ARCANUM-STATE-CLASSIFICATION.md`
- `ops/development/refinement-runs/2026-05-27-zone-taxonomy/DELETION-CANDIDATE-PASS.md`

## Refined Problem

The current root GitHub/Copilot Arcanum surface uses historical discovery names:

- `arcanum-sigil-*`
- `arcanum-spell-*`
- selected root-level Arcanum names such as `arcanum-orchestrate`, `arcanum-necronomicon`, and `arcanum-necronomicon-session`

The generator currently emits flattened names:

- `arcanum-refine`
- `arcanum-invoke`
- `arcanum-task-session`
- unprefixed aliases such as `invoke`, `refine`, and `task-session`

Replacing root `.github/skills` with the staged output would rename the GitHub/Copilot discovery surface and introduce unprefixed aliases into a root collaboration runtime that also contains DomainSpec and GSD skills.

## Done Criteria

- GitHub/Copilot naming policy is accepted.
- Root Arcanum GitHub packages can be regenerated without renaming discovery handles unless explicitly chosen.
- `.arcanum/runtimes/github-copilot` can be untracked/regenerated on demand after root packages no longer depend on it.
- Root legacy command adapter deletions can be finalized.
- Generated observability state policy can be applied.
- Legacy Arcanum-name cleanup can proceed through targeted diff evidence.

## Research Decision

No external research. Local runtime surface evidence is sufficient.
