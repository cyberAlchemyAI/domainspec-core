# Task: F3/F8 Auditability And Dependency Proof

SWU: `SWU-ZRIG-F3-F8-AUDITABILITY`
Findings: F3, F8
Status: pending

## Goal

Make residue persistence and verification dependencies trustworthy enough for later product-mode claims.

## Evidence

- Pipeline constructs `PerWaveResidue(..., entries=...)`.
- `PerWaveResidue` requires `rejected_alternatives`, `dead_ends`, `minority_dissent`, `lessons`, and `timestamp`.
- The residue exception is logged as non-fatal while the run can complete.
- `pyproject.toml` does not declare runtime/test dependencies.

## Write Scope

- `projects/zrig/z-rig-turbo-v5.5.3-engine/z-rig-orchestrator/src/zrig/residue.py`
- `projects/zrig/z-rig-turbo-v5.5.3-engine/z-rig-orchestrator/src/zrig/pipeline.py`
- `projects/zrig/z-rig-turbo-v5.5.3-engine/z-rig-orchestrator/pyproject.toml`
- Focused tests under `projects/zrig/z-rig-turbo-v5.5.3-engine/z-rig-orchestrator/tests/`

## Check

```bash
cd projects/zrig/z-rig-turbo-v5.5.3-engine/z-rig-orchestrator
PYTHONPATH=src python3 -m pytest tests/test_residue.py tests/test_pipeline.py -k "residue or dependency"
```

## Done Criteria

- Residue write path no longer raises the constructor mismatch.
- Product/live fatality or degraded-assurance policy is explicit and tested.
- Required runtime/test dependencies are declared.
- A blocked dependency command is represented as F8 until fixed.
