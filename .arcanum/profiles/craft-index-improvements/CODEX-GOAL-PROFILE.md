# Codex Goal Profile: Craft Index Improvements

## Codex Goal Profile Result

- Source work-pack:
  `arcanum/arcana/craft/development/invoke-runs/20260615T123257Z-craft-index-improvements/WORK-PACK.md`
- Selected unit: `TASK-CII-ONEGO`
- Readiness: pass

## Native Goal

```text
/goal Execute TASK-CII-ONEGO from arcanum/arcana/craft/development/invoke-runs/20260615T123257Z-craft-index-improvements/WORK-PACK.md in one gated Codex session. Outcome: implement Craft readiness indexes plus generated .craft/index.json and .craft/projections/*.csv support according to the selected task contract, preserving .craft/ledger.yml as source of truth and keeping CSV import dry-run-only until fixture proof passes. Verification surface: read .arcanum/profiles/craft-index-improvements/CONTEXT-PACK.md and context-index.json first; then run the task-local validation surfaces for each SWU, including YAML parse for schema/fixtures, JSON parse for generated index fixtures, CSV header/row-count checks, targeted rg checks for readiness/projection terms, projection tool fixture checks if tooling is added, public-boundary scan for generated outputs, and git -C arcanum diff --check -- arcana/craft. Constraints: execute SWUs in order SWU-CII-001 through SWU-CII-007; use the private decision profile only for execution posture and do not copy its contents into public artifacts; do not make generated JSON or CSV authoritative over YAML; do not enable direct CSV writeback; do not commit, push, open PRs, or move the parent gitlink; do not touch unrelated public arcanum files or private/product submodules. Boundaries: write only the paths allowed by .arcanum/profiles/craft-index-improvements/context-index.json and the active SWU; generated runtime mirrors may be refreshed only after canonical source validation passes; publication checks stop at report-ready state unless explicitly requested. Iteration policy: after each SWU, run its validation, update the work-pack/profile evidence only when scope or blockers changed, continue to the next SWU only if validation passes or the repair is inside write scope, and report all files touched plus any extra sources used outside the handoff pack with the named gap that justified each source. Blocked stop condition: stop and report pass/flag/block if validation fails outside write scope, public-boundary scan finds private data, an SWU needs an unstated decision or broader scope, generated outputs would become authority, CSV import requires direct mutation, or publication/parent-gitlink movement is needed.
```

## Verification Surface

- `python3` YAML parse for schema and fixture files.
- `python3 -m json.tool` for generated JSON fixtures and indexes.
- CSV header and row-count checks.
- Targeted `rg` checks for readiness/projection terms.
- Projection tool fixture run if `craft-index.py` is added.
- Public-boundary scan for generated fixtures/outputs.
- `git -C arcanum diff --check -- arcana/craft`.
- `make bump-check` only if publication is explicitly requested.

## Boundaries

- Write scope is restricted to the active SWU in
  `.arcanum/profiles/craft-index-improvements/context-index.json`.
- Private decision-profile contents stay private.
- Public `arcanum` changes must remain public-safe.
- No commit, push, PR, or parent gitlink movement.

## Handoff Pack

- Markdown: `.arcanum/profiles/craft-index-improvements/CONTEXT-PACK.md`
- JSON/index: `.arcanum/profiles/craft-index-improvements/context-index.json`

## Strict Coverage

pass

## Fallback Exploration

named gaps only:

- generated runtime mirror locations;
- generator/bootstrap command;
- Python/YAML validation dependency availability;
- current public fixture conventions.

## Extra-Source Reporting

required

## Stop Condition

Stop with a blocked report when validation fails outside write scope, private
data would enter public artifacts, scope must broaden, direct CSV writeback is
needed, generated artifacts would become authoritative, or publication is
required.

## Validation

Created from selected `TASK-CII-ONEGO` work-pack contract and private handoff
pack. JSON/index validation must pass before use.
