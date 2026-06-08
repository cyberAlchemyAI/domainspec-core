# TASK-BW-INV-002 Context

## Task

Add target proposal and chat-view templates for Body War.

## Sources Reviewed

| Source | Evidence Used |
| --- | --- |
| `docs/features/inventory-interface-indexing/WORK-PACK.md` | `TASK-BW-INV-002`, `SWU-BW-INV-002`, and `SWU-BW-INV-003` were ready. |
| `docs/features/inventory-interface-indexing/SPEC.md` | Confirmation must list included/excluded/write path/generated files/risks; chat views must show selected evidence, exclusions, gaps, next owner. |
| `docs/features/park-track-pilot/implementation-layering.md` | First park, track boundaries, L0 score operation, and notification/channel concerns must remain visible. |
| `docs/PROJECT-DECISIONS.md` | Hybrid scoring and app-backed validation are selected; pilot city and first park/track set remain unresolved. |

## Boundaries

- Do not create the pilot slice.
- Do not inventory the whole Body War repository.
- Do not edit canonical project source docs.
- Do not mutate `.codex`, `.arcanum`, or `domainspec` except observability telemetry.
- Do not promote generated Inventory links into rules, definitions, or ontology.

## Completion Criteria

- `target-confirmation.md` names included sources, excluded sources, write path,
  generated files, and known risks.
- Chat view templates show selected evidence, excluded nearby evidence, gaps,
  and next owner.
- `WORK-PACK.md` marks `TASK-BW-INV-002`, `SWU-BW-INV-002`, and
  `SWU-BW-INV-003` completed while leaving `TASK-BW-INV-003` ready.
- No `pilot/` slice is created.
