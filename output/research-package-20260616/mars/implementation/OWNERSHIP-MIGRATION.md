# MARS Ownership Model

## Current State

MARS now uses an implementation-first canonical model.

Canonical source paths:

- `/implementation/mars/definitions/*`
- `/implementation/mars/templates/*`
- `/implementation/mars/copilot/*` (pack-scoped reusable assets, including `copilot/skills/*`)
- `/implementation/mars/.github/*` (pack installation targets)

Research execution paths (projection and evidence):

- `/research/projects/mars/**`

Orchestration-local operator assets:

- `/.github/agents/mars-research-*.agent.md`
- `/.github/skills/mars-research-*/SKILL.md`

Note: root `/.github` currently hosts the active runtime copies used by this repository. Canonical reusable skill content should be authored in `implementation/mars/copilot/skills` and then mirrored to runtime copies.

## Generalization Principle

`research/projects/mars` is the generalized research-project application of MARS patterns.

- `implementation/mars` defines canonical reusable contracts and templates.
- `research/projects/mars` carries project-scoped execution state, evidence, and run-time artifacts.

## Synchronization Contract

1. Canonical edits for MARS definitions/templates must be made under `implementation/mars` first.
2. Canonical reusable skill edits must be made under `implementation/mars/copilot/skills` first.
3. Projection/runtime copies are refreshed via `./tools/sync_mars_canonical_assets.sh`.
4. Structure checks run after sync via `./tools/check_research_structure.sh`.
5. Drift in canonical vs projection/runtime paths is treated as a governance defect.

## Guardrails

1. Do not introduce semantic-only changes directly in projection copies under `research/projects/mars/definitions` or `research/projects/mars/templates`.
2. Keep experiment run data, results, and adjudications only in `research/projects/mars/experiments`.
3. Keep root `/.github` focused on orchestration behavior, not canonical contract storage.
