# Repository Map For v2 Structure Work

ID: repository-map
Type: synthesis
Status: candidate
Tags: repo-map, knowledge-system, v2-repo, submodule-boundary, public-private-boundary
Confidence: medium

## Source Refs

- `AGENTS.md`
- `CLAUDE.md`
- `.gitmodules`
- `README.md`
- `projects/domainspec-v2/README.md`
- `projects/domainspec-v2/research/`
- `arcanum/README.md`
- `arcanum/arcana/README.md`
- `.arcanum/necronomicon/README.md`
- `.arcanum/observability/README.md`
- `implementation/domainspec/ARCHITECTURE.md`

## Current Shape

The parent repository is a private umbrella. It composes public Arcanum, private
DomainSpec implementation, private validation, project workspaces, research
towers, runtime adapters, generated skill mirrors, and operational ledgers.

The v2 project currently lives under `projects/domainspec-v2/` as a
pre-implementation research program. Its README says v1 evidence comes from
`implementation/domainspec`, v2 research writes stay under
`projects/domainspec-v2/research/`, and no template, validator, ontology,
registry, or runtime change should happen without later approved execution.

## Useful Structure Signals

| Signal | Source refs | v2 implication |
| --- | --- | --- |
| Private umbrella composes public + private submodules | `AGENTS.md`, `.gitmodules` | A v2 repo should make public/private boundaries visible at the top level. |
| Arcanum separates framework, registry, formulae, transmutations, arcana, spells, research | `arcanum/README.md` | v2 can borrow a tiered capability layout without copying public Arcanum internals into private implementation space. |
| Inventory is an Arcana capability, not raw source authority | `arcanum/arcana/README.md`, `.agents/skills/inventory/SKILL.md` | v2 should include compiled read models, but keep raw/source authority elsewhere. |
| Necronomicon is local harness state, not a definition store | `.arcanum/necronomicon/README.md` | v2 should distinguish operational harness state from canonical design assets. |
| Observability is a first-class local package | `.arcanum/observability/README.md` | v2 should include telemetry and reflection from the start if agents will mutate it. |
| Research towers are non-canonical until promoted | `projects/domainspec-v2/README.md` | v2 should keep research towers separate from promoted specs and runtime contracts. |

## Candidate v2 Repository Skeleton

This is a synthesis from inspected sources, not a promoted design.

```text
domainspec-v2/
  README.md
  AGENTS.md
  docs/
    glossary.md
    decisions/
    registry.md
  research/
    towers/
    lanes/
    synthesis/
    source-records/
  specs/
    feature/
    ontology/
    runtime/
    validators/
  runtime/
    adapters/
    commands/
    skills/
  implementation/
    packages/
    examples/
    migrations/
  validation/
    fixtures/
    harnesses/
    reports/
  inventory/
    index.md
    entries/
    evidence-cards/
    evidence-sets/
  observability/
    signals/
    runs/
    reflections/
  ops/
    work-packs/
    task-sessions/
    dispatch/
```

## Boundary Notes

- `research/` is where ideas are tested.
- `specs/` is where promoted design contracts live.
- `runtime/` is where executable agent/runtime adapters live.
- `implementation/` is where product code or reusable packages live after
  promotion.
- `validation/` is where executable evidence and reports live.
- `inventory/` is a compiled lookup layer, not the source of truth.
- `observability/` is runtime evidence, not design authority.
- `ops/` is the work execution trail and should not become the spec.

## Open Questions

- Should v2 be a standalone repo now, or remain a project folder until one
  tower promotes an implementation boundary?
- Should public-safe Arcanum-like framework pieces live in the v2 repo, or be
  upstreamed to `arcanum` after boundary scrub?
- Should `inventory/` be repo root `inventory/` in v2, or stay hidden under
  `.arcanum/inventory/` when v2 is still mostly Arcanum-operated?
- Which v2 towers are promotion candidates versus durable research references?
