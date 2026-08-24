# Runtime Handoff

- Dispatch: `20260804-agent-consultation-work-episodes-api`
- Route: Route 2, Arcanum Refine full preset
- Status: planning-only Refine run; no implementation authorization
- Repository revision: `ab46061bf14db23a01054c2fd3fafec60fb5eb2f`
- Evidence date: `2026-08-04`

## Objective

Produce a closed API design and medium-complexity Work Pack for agents to query the Anime.js vault and append evidence-bearing WorkEpisodes without combining read and write authority or automatically promoting Lessons.

## Strict boundaries

- Read API: immutable neutral projection only.
- Write API: separately authorized append-only event journal.
- Derived state: deterministic reducer output; never the canonical event source.
- Lesson status: outside this API and owned by later review.
- Current run: design and plan evidence only.

## Write scope

- `projects/animejs/development/refinement-runs/20260804-agent-consultation-work-episodes-api/`
- Mandatory append-only governed dispatch ledger records only.

## Forbidden scope

- `projects/animejs/ontology/agent-knowledge-vault/`
- `projects/augmentor/ontology/unified-agent/`
- `/home/vrondelli/projects/workspace-resonant/`
- Git commit/push, deployment, promotion, release, public publication

## Validation

- Dispatch Spec validation must pass before stages.
- Review sheet schema validation and two independent tension checks must pass before critic spawn.
- Both critics must join and close before repair.
- Final JSON parses, links, hashes, SWU atomicity, and claim ceilings must pass.
