# TASK-BW-INV-003 Context

## Task

Add Body War selector/link/index example templates.

## Sources Reviewed

| Source | Evidence Used |
| --- | --- |
| `docs/features/inventory-interface-indexing/WORK-PACK.md` | `TASK-BW-INV-003` and `SWU-BW-INV-004` were ready; done criterion is JSON parse. |
| `docs/features/inventory-interface-indexing/SPEC.md` | Cards/indexes must cite selectors; generated links must use non-authority read-model language; gaps must preserve open decisions. |
| `docs/features/inventory-interface-indexing/ARCHITECTURE.md` | Source docs stay read-only; generated cards are not canonical game-rule authority; first pilot path must not be created yet. |
| `docs/features/park-track-pilot/DISTILL.md` | Park Track Control is the first candidate and should preserve controller/challenge/defense loop. |
| `docs/features/park-track-pilot/implementation-layering.md` | L0 scope is one park, two or three tracks, manual evidence, controller/challenge/defense loop; first city, park, and track boundary format remain open. |
| `docs/features/game-rules/SPEC.md` | First candidate note and unresolved rule decisions constrain generated examples. |
| `docs/PROJECT-DECISIONS.md` | Hybrid scoring and app-backed validation are selected; pilot city and first park/track set remain unresolved. |
| `arcanum/arcana/inventory/development/LINKING-DISCIPLINE.md` | Reused controlled edge vocabulary and non-authority link rule. |
| `arcanum/arcana/inventory/templates/evidence-card-schema.md` | Reused Evidence Card field vocabulary for example card shape. |

## Boundaries

- Do not create `pilot/park-track-control/`.
- Do not mutate Body War canonical source docs.
- Do not promote cards or links into definitions, ontology, or game rules.
- Keep JSON examples under the feature-local `templates/` path.

## Completion Criteria

- Selector/link/index examples exist in the feature template path.
- Examples parse as JSON.
- Examples include source selectors, non-authority links, gaps, risks, and a retrieval fixture.
- `WORK-PACK.md` marks `TASK-BW-INV-003` and `SWU-BW-INV-004` completed and exposes `TASK-BW-INV-004` as the next ready task.
