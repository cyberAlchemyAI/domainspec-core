# TASK-BW-INV-004 Context

## Task

Add validator checks or fixtures for Body War source refs, links, and gaps.

## Sources Reviewed

| Source | Evidence Used |
| --- | --- |
| `docs/features/inventory-interface-indexing/WORK-PACK.md` | `TASK-BW-INV-004` and `SWU-BW-INV-005` were ready; done criterion is bad refs/edges/missing gaps fail. |
| `docs/features/inventory-interface-indexing/IMPLEMENTATION-PLAN.md` | Validator must catch bad refs, unknown edges, and missing gaps. |
| `docs/features/inventory-interface-indexing/SPEC.md` | Generated cards/indexes cite selectors; generated links use non-authority read-model language; open decisions become gaps. |
| `docs/features/inventory-interface-indexing/ARCHITECTURE.md` | Source docs remain read-only and generated links are not game-rule authority. |
| `docs/features/inventory-interface-indexing/templates/*.example.json` | Positive examples to validate. |
| `arcanum/arcana/inventory/scripts/validate-evidence-card-fixtures.sh` | Existing Inventory validator style reused for local feature validation. |

## Boundaries

- Do not create `pilot/park-track-control/`.
- Do not mutate Body War canonical source docs.
- Keep validator local to the feature folder.
- Preserve pilot target confirmation as the next blocker after validation.

## Completion Criteria

- Validator exists under the feature folder.
- Positive JSON examples pass.
- Negative fixtures prove bad source refs, bad link edges, and missing required gaps fail.
- `WORK-PACK.md` marks `TASK-BW-INV-004` complete and stops at the target confirmation blocker for `TASK-BW-INV-005`.
