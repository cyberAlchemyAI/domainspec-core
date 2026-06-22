# Task: F1 Gate Authority Proof

SWU: `SWU-ZRIG-F1-GATE-PROOF`
Findings: F1, with F2 assurance-boundary awareness
Status: selected next

## Goal

Prevent spec-governed waves from passing through generic gate behavior when their semantic condition failed or when no specific evaluator exists.

## Evidence

- Review F1 says W10/W11 failed payloads passed `PASS GENERIC`.
- `src/zrig/gates.py` maps W10/W11 to G10/G11 but does not register G10/G11 evaluators.
- `_generic_gate` checks registry, timeout, and output presence, not deploy/sentinel semantics.

## Write Scope

- `projects/zrig/z-rig-turbo-v5.5.3-engine/z-rig-orchestrator/src/zrig/gates.py`
- `projects/zrig/z-rig-turbo-v5.5.3-engine/z-rig-orchestrator/tests/test_pipeline.py`
- Optional focused test file under `projects/zrig/z-rig-turbo-v5.5.3-engine/z-rig-orchestrator/tests/`

## Implementation Expectations

- Add tests for failed W10 and W11 payloads.
- Either add specific G10/G11 evaluators or make missing spec-governed gate evaluators fail closed in relevant modes.
- Keep passthrough behavior limited to explicitly declared passthrough waves.
- Preserve dry-run/stub usefulness while refusing product-gate false positives.

## Check

```bash
cd projects/zrig/z-rig-turbo-v5.5.3-engine/z-rig-orchestrator
PYTHONPATH=src python3 -m pytest tests/test_pipeline.py -k "gate or W10 or W11"
```

## Done Criteria

- Failed W10 payload does not pass.
- Failed W11 payload does not pass.
- Test output is captured.
- If dependencies block pytest, F8 is recorded and this task remains incomplete.
- Completion note says this is bounded F1 proof only.
