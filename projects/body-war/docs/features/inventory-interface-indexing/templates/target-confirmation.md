# Inventory Target Confirmation

## Inferred Target

| Field | Value |
| --- | --- |
| targetLabel | `{{target_label | default: Park Track Control Inventory Slice}}` |
| targetId | `{{target_id | default: park-track-control}}` |
| targetType | `{{target_type | default: body-war-inventory-slice}}` |
| confidence | `{{confidence | default: medium}}` |
| inferredFrom | `{{prompt_or_request_summary}}` |
| reason | `{{reason_for_target_choice}}` |

## Included Sources

Inventory will read only this bounded source corpus unless the operator changes
the target:

| Source | Inclusion Reason |
| --- | --- |
| `docs/PROJECT-OVERVIEW.md` | Project identity, source policy, audience, and scope. |
| `docs/PROJECT-DECISIONS.md` | Selected decisions and unresolved pilot decisions. |
| `docs/features/game-rules/SPEC.md` | Game-rule objects, scoring/conquest/defense language, and rule gaps. |
| `docs/features/park-track-pilot/DISTILL.md` | Smallest coherent pilot concept. |
| `docs/features/park-track-pilot/implementation-layering.md` | L0-L3 pilot layers, promotion gates, and open pilot decisions. |
| `docs/research/source-notes/` | Curated research notes when present and relevant to the target. |

## Excluded Sources

Inventory will not read or mutate these areas for this target:

| Excluded Area | Reason |
| --- | --- |
| `.codex/` | Local assistant/runtime state, not project evidence. |
| `.arcanum/` | Generated observability/runtime state except task telemetry. |
| `domainspec/` | Project-local tooling bundle, not Body War product evidence for this slice. |
| raw/source assets outside curated notes | Raw material is not part of the curated evidence corpus yet. |
| app/prototype code | No app implementation is part of this Inventory slice. |
| unrelated feature folders | First slice must stay bounded to Park Track Control. |

## Proposed Write Path

```text
docs/features/inventory-interface-indexing/pilot/park-track-control/
```

## Generated Files

If confirmed, Inventory may create these generated read-model files under the
proposed write path:

| File | Purpose |
| --- | --- |
| `target-confirmation.md` | Saved confirmation record for the slice. |
| `cards.json` | Source-backed Evidence Cards. |
| `index.json` | Compact slice summary and object index. |
| `retrieval.json` | Lookup fixture with selected and excluded records. |
| `COVERAGE.md` | Human-readable coverage, omissions, and warnings. |
| `indexes/selector-index.json` | Source selector to card/index mapping. |
| `indexes/link-index.json` | Read-model relationships between cards, sources, and gaps. |
| `indexes/gap-risk-index.json` | Unresolved decisions, risks, and next owners. |

## Will Not Do

- Do not inventory the whole Body War repository.
- Do not edit source docs such as `PROJECT-DECISIONS.md` or `game-rules/SPEC.md`.
- Do not decide first city, first park, track boundaries, scoring authority, or
  validation channel inside generated Inventory files.
- Do not mutate `.codex/`, `.arcanum/`, or `domainspec/` except task telemetry.
- Do not promote generated links into canonical rules, definitions, or ontology.

## Known Risks

| Risk | Handling |
| --- | --- |
| First park and track boundaries remain unresolved. | Preserve as `gap` records with owner `body-war/product`. |
| Pilot validation city remains unresolved. | Preserve as `gap` records with owner `body-war/product`. |
| Hybrid scoring is selected, but active pilot scoring details still need operational shape. | Separate selected project decision from unresolved execution details. |
| App-backed validation channel is selected, but no implementation is in scope for this slice. | Link as decision evidence; do not create app tasks here. |
| Generated cards are read models, not canonical game rules. | Mark generated artifacts as Inventory outputs and cite sources. |

## Confirmation

Confirm this target before mutation:

```text
yes - generate the bounded Park Track Control Inventory slice
no - do not generate anything
change target - provide a different target, source corpus, or write path
```
