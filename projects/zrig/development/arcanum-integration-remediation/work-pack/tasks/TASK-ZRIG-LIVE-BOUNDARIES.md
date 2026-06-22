# Task: Live Identity, Bridge, Deploy, And Sentinel Boundaries

SWU: `SWU-ZRIG-F4-F7-LIVE-BOUNDARIES`
Findings: F4, F5, F6, F7
Status: pending

## Goal

Make live bridge identity, operator docs, deploy/sentinel reachability, and deploy command trust boundaries explicit and testable.

## Write Scope

- `projects/zrig/z-rig-turbo-v5.5.3-engine/z-rig-orchestrator/src/zrig/live_executor.py`
- `projects/zrig/z-rig-turbo-v5.5.3-engine/z-rig-orchestrator/src/zrig/deploy_config_schema.py`
- `projects/zrig/z-rig-turbo-v5.5.3-engine/z-rig-orchestrator/src/zrig/deploy_adapter.py`
- `projects/zrig/z-rig-turbo-v5.5.3-engine/z-rig-orchestrator/QUICKSTART.md`
- Tests under `projects/zrig/z-rig-turbo-v5.5.3-engine/z-rig-orchestrator/tests/`

## Acceptance

- Bridge-reported identity cannot spoof trusted seat identity.
- QuickStart documents live manifest/envelope expectations.
- W10/W11 either receive intentional config through normal context or fail closed when absent.
- Deploy command configuration uses constrained operations or explicit trust/approval policy.

## Check

```bash
cd projects/zrig/z-rig-turbo-v5.5.3-engine/z-rig-orchestrator
PYTHONPATH=src python3 -m pytest tests/test_deploy_adapter.py tests/test_sentinel_monitor.py tests/test_pipeline.py -k "live or deploy or sentinel or identity"
```

## Handoff Note

Do not run real deploy or sentinel side effects in this task. Use validation, previews, fakes, and focused tests.
