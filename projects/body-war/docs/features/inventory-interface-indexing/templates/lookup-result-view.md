# Inventory Lookup Result View

## Query

```text
{{query}}
```

## Result Summary

{{result_summary}}

## Selected Evidence

| Card Or Record | Source Selector | Why Selected |
| --- | --- | --- |
| `{{card_or_record_id}}` | `{{source_selector}}` | `{{selection_reason}}` |

## Selected Links

| From | Edge | To | Confidence | Notes |
| --- | --- | --- | --- | --- |
| `{{from_id}}` | `{{edge_type}}` | `{{to_id}}` | `{{confidence}}` | `{{notes}}` |

## Excluded Nearby Evidence

| Source Or Record | Why Excluded |
| --- | --- |
| `{{excluded_id_or_selector}}` | `{{exclusion_reason}}` |

## Gaps

| Gap | Owner | Next Action |
| --- | --- | --- |
| `{{gap_id_or_label}}` | `{{owner}}` | `{{next_action}}` |

## Risks

| Risk | Handling |
| --- | --- |
| `{{risk_label}}` | `{{risk_handling}}` |

## Next Owner

{{next_owner}}

## Next Route

{{next_route}}

## Authority Note

This answer is generated from Inventory read models. Treat it as a retrieval and
orientation result, not as a canonical update to Body War rules or decisions.
