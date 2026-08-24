# Execution Pack: Agent Consultation API

This schedules one frozen candidate-local L0 frontier. Exact material is
prepared, but implementation remains unapproved until the emitted epoch digest
receives human Decision Gate approval.

## Planning Control Fields

| Field | Value |
| --- | --- |
| planningGateStatus | approval-pending |
| complexity | medium |
| baselineWave | W0 |
| activePlanRef | `one-go/ONE-GO-HANDOFF.md` |
| workPackManifest | `WORK-PACK.md` |
| layeringArtifact | `IMPLEMENTATION-LAYERING.md` |
| specRef | `stages/08-distill-repair.md` |
| activeLayerWindow | L0 |
| lastPlannedAt | 2026-08-03T18:32:47Z |
| readinessProfile | frozen-input-contractual-readiness |
| finiteFrontier | `SWU-ACAPI-000` -> `001` -> `002` -> `003` -> `004` -> `005` -> `006` -> terminal |
| requestBudget | 7 |
| stopCondition | first blocker or frontier complete |

## Wave Order

1. [W0 Contract](work-pack/waves/W0-CONTRACT.md): SWU-000 through 003.
2. [W1 Fixture service](work-pack/waves/W1-FIXTURE-SERVICE.md): SWU-004
   through 006.
3. [W2 Host and hardening](work-pack/waves/W2-HOST-HARDENING.md): SWU-007
   through 011 plus SWU-013 after owner gates.
4. [W3 Optional packaging](work-pack/waves/W3-PACKAGING.md): SWU-012 only
   after one explicit selection.

## Execution Rules

- The outer `task-session-until-blocker` chain may expose only one exact
  selector at a time; every selector still receives a fresh Task Session.
- W0 may start only after the exact WPRA epoch is approved.
- The chain budget is seven and cannot expand during execution.
- Every transition must pass the project-local semantic wrapper before the
  canonical chain state advances.
- No `workspace-resonant` write occurs before B-002 and B-003 are resolved.
- Promotion to each wave cites executed receipts from the prior wave.
- Parallel execution is forbidden inside this epoch.
- The pack never schedules deployment or release.

## Current Next Action

Review and approve or reject the exact epoch in `one-go/DECISION-GATE.md` after
WPRA v1 and v2 pass. Approval may authorize one serial run of SWU-ACAPI-000
through SWU-ACAPI-006 only. It does not authorize L1, deployment, or release.
