# Context Pack: Craft Index Improvements One-Go Execution

## Coverage Status

- Strict coverage: pass
- Selected unit: `TASK-CII-ONEGO`
- Source work-pack:
  `arcanum/arcana/craft/development/invoke-runs/20260615T123257Z-craft-index-improvements/WORK-PACK.md`
- Selected task contract:
  `arcanum/arcana/craft/development/invoke-runs/20260615T123257Z-craft-index-improvements/work-pack/tasks/TASK-CII-ONEGO.md`
- Decision profile:
  `.arcanum/profiles/decision-profile.yml`

## Pack-First Rule

Before editing, read:

1. this context pack;
2. `context-index.json`;
3. the selected task contract;
4. the public Invoke architecture and plan artifacts.

Do not start broad repository discovery unless a named gap in this pack requires
it. Any extra source used must be reported with the gap that justified it.

## Execution Outcome

Implement Craft readiness indexes plus generated JSON/CSV projection support in
one native Codex Goal session, following the SWU order from `TASK-CII-ONEGO`.

## Source Anchors

| Anchor | Purpose |
| --- | --- |
| `arcanum/arcana/craft/SKILL.md` | Craft operating contract and all-status behavior. |
| `arcanum/arcana/craft/README.md` | Public storage model and user-facing docs. |
| `arcanum/arcana/craft/templates/ledger.schema.yml` | Canonical ledger schema contract. |
| `arcanum/arcana/craft/examples/` | Current public examples for compatibility checks. |
| `arcanum/arcana/craft/development/refinement-runs/20260614T200439Z-craft-feature-readiness-indexes/RESULT.md` | Readiness-index source design. |
| `arcanum/arcana/craft/development/refinement-runs/20260615T121512Z-craft-ledger-csv-json-indexes/RESULT.md` | Projection-index source design. |
| `arcanum/arcana/craft/development/invoke-runs/20260615T123257Z-craft-index-improvements/INVOKE-DESIGN-ARCHITECTURE.md` | Combined architecture. |
| `arcanum/arcana/craft/development/invoke-runs/20260615T123257Z-craft-index-improvements/IMPLEMENTATION-LAYERING.md` | Layer gates. |
| `arcanum/arcana/craft/development/invoke-runs/20260615T123257Z-craft-index-improvements/WORK-PACK.md` | Execution manifest. |

## Write Scope

Allowed only if the matching SWU is active:

- `arcanum/arcana/craft/templates/ledger.schema.yml`
- `arcanum/arcana/craft/SKILL.md`
- `arcanum/arcana/craft/README.md`
- `arcanum/arcana/craft/fixtures/craft-index-improvements/`
- `arcanum/arcana/craft/scripts/`
- generated Craft runtime mirrors after canonical validation passes
- this run's work-pack artifacts only when synchronizing execution evidence

Blocked:

- private `.arcanum/profiles/decision-profile.yml` mutation;
- unrelated public `arcanum` files;
- product/private submodules;
- commits, pushes, PRs, and parent gitlink updates.

## Validation Surface

Required checks are evidence-driven. Use exact available commands after
implementation, including:

- YAML parse for `ledger.schema.yml` and fixtures;
- `python3 -m json.tool` for generated JSON fixtures;
- CSV header/row-count checks;
- targeted `rg` checks for readiness/projection terms;
- generated tool fixture run if `craft-index.py` is added;
- public-boundary scan for generated fixture/output content;
- `git -C arcanum diff --check -- arcana/craft`;
- parent `make bump-check` only if publication is explicitly requested.

## Named Gaps For Fallback Exploration

Fallback exploration is limited to:

- exact generated runtime mirror locations if source validation passes;
- existing generator/bootstrap command to refresh runtime mirrors;
- Python/YAML dependency availability for validation commands;
- current public fixture conventions if `arcana/craft/fixtures/` does not exist.

## Stop Conditions

Stop and report `block` if:

- any validation command fails and the repair is outside write scope;
- public-boundary scan finds private paths, names, or unpublished project details;
- generated outputs would become authoritative over YAML;
- CSV import would need direct writeback instead of dry-run;
- commit/push/PR/parent-gitlink publication is required;
- an SWU requires an unstated decision or broad scope expansion.
