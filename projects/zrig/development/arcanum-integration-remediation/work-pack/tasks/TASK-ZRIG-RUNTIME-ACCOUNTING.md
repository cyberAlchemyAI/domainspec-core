# Task: Runtime Accounting And Spec Drift

SWU: `SWU-ZRIG-F9-F14-RUNTIME-ACCOUNTING`
Findings: F9, F10, F11, F12, F13, F14
Status: pending

## Goal

Bring runtime accounting, failure routing, mode specification, and metrics status under explicit orchestrator authority.

## Write Scope

- `projects/zrig/z-rig-turbo-v5.5.3-engine/z-rig-orchestrator/src/zrig/dispatch.py`
- `projects/zrig/z-rig-turbo-v5.5.3-engine/z-rig-orchestrator/src/zrig/pipeline.py`
- `projects/zrig/z-rig-turbo-v5.5.3-engine/z-rig-orchestrator/src/zrig/metrics.py`
- `projects/zrig/z-rig-turbo-v5.5.3-engine/z-rig-orchestrator/src/zrig/config.py`
- Operator docs/tests as required.

## Acceptance

- Failover cap is shared per wave under concurrent seats.
- Clean-run policy, logs, and skipped waves agree.
- W6/W7 routing semantics are explicit and tested.
- `waves_completed` and `waves_skipped` have distinct meanings.
- `AUTO` is either promoted into product spec or marked as extension.
- Metrics are wired into run completion or declared prototype/non-product.

## Check

```bash
cd projects/zrig/z-rig-turbo-v5.5.3-engine/z-rig-orchestrator
PYTHONPATH=src python3 -m pytest tests/test_dispatch.py tests/test_pipeline.py -k "failover or clean or skipped or AUTO or metrics or W6 or W7"
```
