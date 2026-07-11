# Execution Pack: L0 Human Approval Desk

## Planning Control Fields

| Field | Value |
| --- | --- |
| planningGateStatus | pass |
| complexity | medium |
| baselineWave | W0 |
| activePlanRef | [WORK-PACK.md](WORK-PACK.md) |
| workPackManifest | [WORK-PACK.md](WORK-PACK.md) |
| layeringArtifact | [IMPLEMENTATION-LAYERING.md](IMPLEMENTATION-LAYERING.md) |
| specRef | [SPEC.md](../../SPEC.md) |
| activeLayerWindow | L0 |
| lastPlannedAt | 2026-07-11 |
| readinessProfile | pilot |

## Wave Schedule

| Wave | Outcome | Tasks | Entry Gate | Exit Gate | Parallelism |
| --- | --- | --- | --- | --- | --- |
| [W0](work-pack/waves/W0.md) | Reproducible failure baseline. | TASK-REGRESSION-HARNESS | Current smoke passes. | All accepted L0 defects have deterministic named regressions. | none |
| [W1](work-pack/waves/W1.md) | Trusted lifecycle and contract boundary. | TASK-TRUSTED-KERNEL | W0 evidence exists. | Replay, queue, grants, attribution, and schema hostile tests pass. | SWU-004 may proceed beside SWU-002 after SWU-001; merge before SWU-005. |
| [W2](work-pack/waves/W2.md) | Recoverable persistence and resolvable receipts. | TASK-PERSISTENCE-EVIDENCE | W1 passes. | Race/restart/reference tests pass with no divergent committed state. | none; shared persistence write scope |
| [W3](work-pack/waves/W3.md) | Human workflow, browser proof, and closure. | TASK-HUMAN-WORKBENCH, TASK-VERIFY-READINESS | W2 passes. | Full suite and closure matrix pass. | verification follows UI evidence |

## Dependency Spine

```text
001 -> 002 -> 003 ----> 005 -> 006 -> 007 -> 008 -> 009 -> VERIFY
  \----------> 004 --/
```

## Merge Rules

- SWU-002 and SWU-004 may run concurrently only if they use separate branches/worktrees and do not both edit shared test or package files.
- The default route is sequential local execution because the project is small and W1 converges in `src/server.mjs`.
- No W2 or W3 work begins from a partially merged W1.
- Every wave returns a validation receipt before the next wave is selected.

## Stop Conditions

- A repair requires effectful capability, external identity, network, provider, browser-act, shell, Git, or IDE authority.
- Event replay cannot deterministically reconstruct the documented read model.
- Receipt references cannot be validated before authoritative append.
- The UI can only claim human identity by trusting caller-provided text.
- An accepted review finding lacks a reproducible test or a documented non-testable review check.
