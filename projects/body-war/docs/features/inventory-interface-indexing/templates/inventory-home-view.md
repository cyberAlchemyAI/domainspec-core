# Inventory Home View

## Current Package

| Field | Value |
| --- | --- |
| feature | `inventory-interface-indexing` |
| activeTarget | `{{active_target | default: none-confirmed}}` |
| inventoryRoot | `docs/features/inventory-interface-indexing/` |
| generatedRoot | `{{generated_root | default: not-created}}` |
| state | `{{state | default: awaiting-target-confirmation}}` |

## Available Actions

| Action | Status | Notes |
| --- | --- | --- |
| infer target | available | Infer Body War or Park Track Control from the prompt. |
| confirm target | available | Required before any generated slice mutation. |
| generate slice | blocked | Waits for confirmation, index examples, and validator checks. |
| lookup evidence | limited | Can explain planned source scope before generated cards exist. |
| explain state | available | Use `explain-view.md`. |
| status | available | Use `status-view.md`. |

## Included Sources

{{included_sources_table}}

Default source corpus:

- `docs/PROJECT-OVERVIEW.md`
- `docs/PROJECT-DECISIONS.md`
- `docs/features/game-rules/SPEC.md`
- `docs/features/park-track-pilot/DISTILL.md`
- `docs/features/park-track-pilot/implementation-layering.md`
- `docs/research/source-notes/`

## Excluded Sources

{{excluded_sources_table}}

Default exclusions:

- `.codex/`
- `.arcanum/` except task telemetry
- `domainspec/`
- raw/source assets outside curated notes
- unrelated feature folders
- app/prototype code

## Open Gaps

{{gap_summary_table}}

Minimum gaps to preserve:

- Pilot validation city.
- First park and track set.
- Track boundary description format.
- Pilot scoring operation details.
- App-backed validation implementation path.

## Next Safe Action

{{next_safe_action | default: ask operator to confirm or change the target}}

## Next Owner

{{next_owner | default: operator/inventory}}
