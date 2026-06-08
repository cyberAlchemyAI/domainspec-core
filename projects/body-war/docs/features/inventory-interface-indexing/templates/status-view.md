# Inventory Status View

## Summary

| Field | Value |
| --- | --- |
| inventoryState | `{{inventory_state}}` |
| activeTarget | `{{active_target}}` |
| generatedRoot | `{{generated_root}}` |
| lastUpdated | `{{last_updated}}` |
| nextOwner | `{{next_owner}}` |

## Coverage

| Source | Status | Notes |
| --- | --- | --- |
| `docs/PROJECT-OVERVIEW.md` | `{{overview_status}}` | `{{overview_notes}}` |
| `docs/PROJECT-DECISIONS.md` | `{{decisions_status}}` | `{{decisions_notes}}` |
| `docs/features/game-rules/SPEC.md` | `{{game_rules_status}}` | `{{game_rules_notes}}` |
| `docs/features/park-track-pilot/DISTILL.md` | `{{distill_status}}` | `{{distill_notes}}` |
| `docs/features/park-track-pilot/implementation-layering.md` | `{{layering_status}}` | `{{layering_notes}}` |
| `docs/research/source-notes/` | `{{source_notes_status}}` | `{{source_notes_notes}}` |

## Indexes

| Index | Status | Notes |
| --- | --- | --- |
| `cards.json` | `{{cards_status}}` | Source-backed Evidence Cards. |
| `index.json` | `{{index_status}}` | Slice summary and object index. |
| `retrieval.json` | `{{retrieval_status}}` | Lookup fixture. |
| `indexes/selector-index.json` | `{{selector_index_status}}` | Selector coverage. |
| `indexes/link-index.json` | `{{link_index_status}}` | Read-model edges. |
| `indexes/gap-risk-index.json` | `{{gap_risk_index_status}}` | Gaps, risks, and owners. |

## Selected Evidence

{{selected_evidence_table}}

## Excluded Nearby Evidence

{{excluded_nearby_evidence_table}}

## Gaps

{{gap_table}}

## Blockers

{{blocker_table}}

## Next Safe Action

{{next_safe_action}}

## Next Owner

{{next_owner}}
