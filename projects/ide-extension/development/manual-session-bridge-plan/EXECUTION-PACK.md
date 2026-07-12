# Execution Pack: Manual Session Bridge

## Planning Control Fields

| Field | Value |
| --- | --- |
| planningGateStatus | pass |
| complexity | medium |
| baselineWave | W0 |
| activePlanRef | [WORK-PACK.md](WORK-PACK.md) |
| workPackManifest | [WORK-PACK.md](WORK-PACK.md) |
| layeringArtifact | [IMPLEMENTATION-LAYERING.md](IMPLEMENTATION-LAYERING.md) |
| specRef | [SPEC.md](../../SPEC.md) plus approved design patch obligation |
| activeLayerWindow | L0 |
| lastPlannedAt | 2026-07-12 |
| readinessProfile | pilot |

## Wave Schedule

| Wave | Outcome | Tasks | Entry gate | Exit gate | Parallelism |
| --- | --- | --- | --- | --- | --- |
| [W0](work-pack/waves/W0.md) | Complete versioned contract and replay baseline. | TASK-CONTRACT-MIGRATION | Approved design/decisions. | v1 replay and v2 schema/typestate fixtures pass. | none |
| [W1](work-pack/waves/W1.md) | Kernel-owned target, claim, recovery, result, and receipts. | TASK-BRIDGE-KERNEL | W0 passes. | API/binding/concurrency/artifact tests pass. | none; shared projector/server scope |
| [W2](work-pack/waves/W2.md) | One-shot session protocol and human workbench. | TASK-SESSION-PROTOCOL, TASK-HUMAN-WORKBENCH | SWU-005 passes. | CLI/protocol and UI state/action tests pass. | SWU-006 and SWU-007 may run in parallel; join before 008. |
| [W3](work-pack/waves/W3.md) | Hostile, browser, manual witness, and readiness evidence. | TASK-VALIDATION-WITNESS, TASK-VERIFY-READINESS | W2 passes. | Automated/browser/manual evidence and closure matrix pass. | sequential evidence chain |

## Dependency Spine

```text
001 -> 002 -> 003 -> 004 -> 005 -> 006 --\
                                  \-> 007 ---> 008 -> 009 -> 010 -> 011 -> VERIFY
```

## Merge Rules

- Default execution is sequential local Task Session.
- SWU-006 and SWU-007 may run in parallel only on separate worktrees because
  one owns session tooling and one owns initial HTML language/evidence display.
- Neither may edit the other's focused test file; both join before SWU-008.
- No partial W1 state merges into UI or witness work.
- Every SWU returns the expected result shape before its dependent is selected.

## Stop Conditions

- v1 history cannot replay without mutation.
- The v2 receipt union cannot distinguish authorization, execution, and legacy
  shapes deterministically.
- More than one ready target can exist after any race/restart.
- A pre-claim response exposes the skill.
- A session can self-release/requeue or mint its own receipt.
- L0 requires write/network tools, authentication, timers, workers, or external
  adapters to satisfy acceptance.
- A required validation cannot run and has no accepted substitute.
