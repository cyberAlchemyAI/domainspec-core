# Refine Seed Proposal: Repository Zone Taxonomy

Date: 2026-05-27
Target: `domainspec-core` repository organization zone taxonomy
Preset: standard
Research mode: research-if-gap-appears
Status: seed-ready

## Intent

Refine the repository zone taxonomy and select the best repository shape for the current `domainspec-core` workspace.

The output should improve on the prior invoke-plan artifact by resolving the broad zones into a practical shape that can guide future path moves, admission rules, generated-state policy, and validation checks.

## Source Context

- `README.md`: original unified three-project model.
- `ops/REPOSITORY-ORGANIZATION-PLAN.md`: research containment and dependency plan.
- `ops/ASSET-OWNERSHIP-POLICY.md`: automation asset ownership and propagation policy.
- `ops/REPOSITORY-ORGANIZATION-INVOKE-PLAN.md`: distill -> invoke plan that selected "Repository Zone Contract" as the smallest coherent unit.
- `.gitmodules`: current submodule declarations for `implementation/domainspec`, `validation/poker-team`, and `arcanum`.
- Current top-level folders include root docs, ops, implementation, validation, research, Arcanum lifecycle assets, reusable sigil library assets, local product projects, generated output/runtime state, and candidate/legacy workspaces.

## Refinement Questions

1. What repository shape best fits the current workspace without forcing premature migration?
2. Which zones are stable canonical families, and which should be transitional or candidate zones?
3. What admission rules prevent future drift?
4. What should be executed next, and what should remain a decision gate?

## Constraints

- Preserve canonical paths only by default.
- Do not add compatibility aliases or redirect shims.
- Do not move files during refinement.
- Do not mutate submodules during refinement.
- Treat dirty worktree and submodule anomalies as blockers for migration, not blockers for taxonomy design.
- Keep research projects self-contained under `research/projects/*`.
- Keep Arcanum lifecycle ownership distinct from DomainSpec research ownership.

## Done Criteria

- Final synthesis names the best repository shape.
- Every top-level path family has a proposed zone or a decision-gated status.
- The taxonomy distinguishes canonical, transitional, generated, and external/nested zones.
- The plan includes admission rules and next-route recommendations.

## Planned Stage Configuration

1. Context Builder evidence baseline: command `context-builder`, mode `standard`.
2. Invoke Define: command `invoke`, mode `define`.
3. Interrogation refine-review: command `interrogation`, mode `refine-review`.
4. Research decision: Refine-owned, mode `research-if-gap-appears`.
5. Distill: command `distill`, mode `standard`.
6. Invoke Redefine / Design: command `invoke`, mode `design`.
7. Interrogation refine-design-review: command `interrogation`, mode `refine-design-review`.
8. Distill Repair: command `distill`, mode `validate`.
9. Invoke Plan: command `invoke`, mode `plan`.
10. Final Interrogation and Synthesis: command `interrogation`, mode `refine-final`, followed by Refine-owned synthesis.

