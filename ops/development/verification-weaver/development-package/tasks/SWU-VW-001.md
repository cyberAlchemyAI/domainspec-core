# SWU-VW-001: Candidate Public Testing Router

Status: `ready`

## Objective

Create the candidate public package at `arcanum/arcana/verification-weaver/`
with docs, receipt schema, synthetic fixtures, negative controls, and a local
validation runner.

## Owned Write Scope

- `arcanum/arcana/verification-weaver/`

## Inputs

- `ops/development/verification-weaver/development-package/DEFINE.md`
- `ops/development/verification-weaver/development-package/DESIGN.md`
- `ops/development/verification-weaver/development-package/OUTPUT-CONTRACT.md`
- `ops/development/verification-weaver/development-package/QUALITY-BAR.md`
- `ops/development/verification-weaver/development-package/ANTI-PATTERNS.md`
- `ops/development/verification-weaver/development-package/negative-controls/NEGATIVE-CONTROLS.md`

## Deliverables

- Candidate `README.md` and `SKILL.md`.
- Development output contract, quality bar, anti-patterns, and validation
  experiment files.
- Synthetic fixtures for all target kinds.
- Runnable negative controls.
- Shell-first validation runner.
- Validation report and residue ledger.

## Acceptance Criteria

- Positive fixtures pass.
- Negative controls fail closed or flag expected residue.
- Private-path and generated-output scans pass.
- Parent receipt cannot promote owner outputs.
- No registry or generated runtime exposure is added.
- Handoff names `sigil-development` as next promotion owner.

## Validation

```bash
bash arcanum/arcana/verification-weaver/development/run-validation-fixtures.sh
git diff --check -- arcanum/arcana/verification-weaver
```
