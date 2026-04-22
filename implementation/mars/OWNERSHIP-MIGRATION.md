# MARS Ownership Migration Note

## Current State

MARS remains a Type B research orchestration pack.

Active source-of-truth paths:
- `/.github/agents/mars-research-*.agent.md`
- `/.github/skills/mars-research-*/SKILL.md`
- `/research/projects/mars/**`

Reserved implementation-facing scaffold paths:
- `/implementation/mars/.github/`
- `/implementation/mars/copilot/`

## Why The Scaffold Exists

The scaffold lets MARS grow toward an installable implementation pack without duplicating active ownership today.

## Migration Trigger

Promote MARS into an implementation-pack ownership model only when all of the following are true:

1. MARS assets are intended for reuse outside the root research orchestration repository.
2. The pack has a stable public boundary for agents, skills, and templates.
3. The install/sync mechanism is defined the same way DomainSpec Type A assets are managed.

## Proposed Migration Shape

1. Canonical reusable assets move to `implementation/mars/copilot/`.
2. Install targets move to `implementation/mars/.github/`.
3. Root `/.github/` keeps only orchestration-local Type B assets that are not meant for distribution.
4. Ownership policy and drift checks are updated before migration lands.

## Guardrail

Until that migration is explicitly approved, do not create mirrored active copies of MARS agents or skills in `implementation/mars/`.