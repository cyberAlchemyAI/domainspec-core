# Shared Context

## Authoritative planning sources

- `../../DEFINE.md`
- `../../DESIGN.md`
- `../../GLOSSARY.md`
- `../../GAPS.md`
- `../../IMPLEMENTATION-LAYERING.md`
- `../../WORK-PACK.md`

## Current implementation contracts

- `../../../../../arcanum/spells/invoke/plan.md`
- `../../../../../arcanum/spells/invoke/refresh.md`
- `../../../../../arcanum/spells/invoke/schemas/material-package.schema.json`
- `../../../../../arcanum/spells/invoke/schemas/material-package-receipt.schema.json`
- `../../../../../arcanum/spells/invoke/scripts/material_package_validator.py`
- `../../../../../arcanum/arcana/task-session/SKILL.md`
- `../../../../../arcanum/arcana/task-session/schemas/mutation-admission-request.schema.json`
- `../../../../../arcanum/arcana/task-session/scripts/verify-mutation-readiness.py`

## Private evidence boundary

The accepted candidate findings remain in:

- `../../../2026-07-23-invoke-lifecycle-churn-research/findings.md`
- `../../../2026-07-23-invoke-lifecycle-churn-research/research.md`

They may be used to validate causality and scope. Public Arcanum changes must
use only the generic requirements in `../../LIFECYCLE-HANDOFF.md`.

## Execution rules

- Re-read live sources and inspect scoped diffs before each SWU.
- Select exactly one SWU.
- Do not use Inventory, telemetry, status, or continuity cursors as readiness
  authority.
- Do not modify public source until its lifecycle owner accepts the SWU.
- Synchronize canonical source before generated `.agents`/`.claude` surfaces.
- Stop on any undeclared controlling path; a successor epoch is required.
