# Execution Pack: Selected SWU

Status: invoke handoff for later task-session
Selected SWU: `SWU-ZRIG-F1-GATE-PROOF`
Execution scope: one bounded private remediation SWU only

## Selected Objective

Make spec-governed Z-Rig gates fail closed when no specific evaluator exists, or add specific evaluator coverage for the selected product waves. The first proof must show failed W10 deploy and W11 sentinel payloads no longer pass through generic gate behavior.

This does not prove product-mode readiness. It proves only bounded F1 remediation progress.

## Why This SWU First

F1 is the only critical finding in the review. The source maps W10/W11 to G10/G11, but only G0/G1/G2/G3/G5.5/G6/G7 have specific evaluators. Missing evaluators fall through to `_generic_gate`, which checks registry, timeout, and output presence. The review reproduced failed W10/W11 payloads passing as `PASS GENERIC`.

## Required Read Context

- `projects/zrig/development/arcanum-integration-remediation/SPEC.md`
- `projects/zrig/development/arcanum-integration-remediation/DESIGN.md`
- `projects/zrig/development/arcanum-integration-remediation/WORK-PACK.md`
- `projects/zrig/development/arcanum-integration-remediation/work-pack/tasks/TASK-ZRIG-F1-GATE-PROOF.md`
- `projects/zrig/review/2026-06-17-zrig-engine-product-mode/findings.md`
- `projects/zrig/z-rig-turbo-v5.5.3-engine/z-rig-orchestrator/src/zrig/gates.py`
- `projects/zrig/z-rig-turbo-v5.5.3-engine/z-rig-orchestrator/tests/test_pipeline.py`

## Allowed Write Scope

- `projects/zrig/z-rig-turbo-v5.5.3-engine/z-rig-orchestrator/src/zrig/gates.py`
- `projects/zrig/z-rig-turbo-v5.5.3-engine/z-rig-orchestrator/tests/test_pipeline.py`
- A new focused test file under `projects/zrig/z-rig-turbo-v5.5.3-engine/z-rig-orchestrator/tests/`
- Optional update to this execution pack with evidence after the SWU completes

No other code, docs, public Arcanum surfaces, runtime adapters, or generated packages are in scope.

## Done Criteria

- A regression test asserts a failed W10 deploy payload does not pass.
- A regression test asserts a failed W11 sentinel payload does not pass.
- Missing/generic gate behavior is fail-closed for product/spec-governed waves, or W10/W11 have specific evaluators that fail the reproduced failed payloads.
- Test output or blocker output is recorded.
- The completion note states that this is not product-mode assurance.

## Verification Command

```bash
cd projects/zrig/z-rig-turbo-v5.5.3-engine/z-rig-orchestrator
PYTHONPATH=src python3 -m pytest tests/test_pipeline.py -k "gate or W10 or W11"
```

If `pytest` or another dependency is unavailable, run:

```bash
cd projects/zrig/z-rig-turbo-v5.5.3-engine/z-rig-orchestrator
python3 -m pytest --version
```

Record that blocker under F8 and do not mark F1 complete until the F1 behavior is verified.

## Out Of Scope

- Live bridge execution.
- Deploying anything.
- Running sentinel against a service.
- Signal Observer bridge.
- Experiment Harness.
- Public Arcanum command/sigil/spell/runtime package.
