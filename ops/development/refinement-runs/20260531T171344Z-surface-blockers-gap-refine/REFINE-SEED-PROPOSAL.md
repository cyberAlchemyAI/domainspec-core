# Refine Seed Proposal: Surface Blockers And Gaps

Date: 2026-05-31
Preset: compact
Research: no-research
Target: Arcanum and DomainSpec repository surface cleanup blockers and gaps

## Objective

Refine the current blocker and gap set before continuing runtime/package cleanup, then route all consequential unresolved choices through a decision gate.

## Source Context

- `ops/ARCANUM-SURFACE-MAP-AND-PLAN.md`
- `docs/decisions/install-profile-contract.md`
- `docs/decisions/native-runtime-skill-surface.md`
- `docs/decisions/personal-codex-skill-refresh.md`
- `ops/RUNTIME-SURFACE-INVENTORY.md`
- `ops/development/TASK-SESSION-ROOT-GITHUB-SKILLS-CLASSIFICATION.md`
- `ops/REPOSITORY-ORGANIZATION-DESIGN.md`
- `ops/REPOSITORY-ORGANIZATION-INVOKE-PLAN.md`

## Write Scope

- `ops/development/refinement-runs/20260531T171344Z-surface-blockers-gap-refine/*`
- `docs/decisions/surface-cleanup-blocker-decisions.md`

No runtime package, command, skill, `.github/skills`, `.arcanum`, or machine-global Codex mutation is allowed during this refinement.

## Done Criteria

- Visible blockers and gaps are classified as blocker, deferrable, assumption, or resolved.
- Blocker decisions have concrete options and trade-offs.
- A durable decision artifact is written.
- Downstream work remains blocked until the user selects options or explicitly overrides the gate.

## Research Decision

No external research. The needed evidence is local repository planning and decision artifacts.
