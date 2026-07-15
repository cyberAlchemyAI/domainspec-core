# SWU Manifest Projection

`WORK-PACK.md#swu-execution-manifest` is canonical for status and gate-bearing
fields. This file is a navigational projection; task contracts own deep local
implementation rules.

| SWUs | Task contract | Layer/wave |
| --- | --- | --- |
| 001–002 | [Contracts](../tasks/TASK-RDL-CONTRACTS.md) | L0/W0 |
| 003–004 | [Builder](../tasks/TASK-RDL-BUILDER.md) | L0/W1 |
| 005–006 | [Guided surface](../tasks/TASK-RDL-GUIDED-SURFACE.md) | L0/W1 |
| 007–008 | [History](../tasks/TASK-RDL-HISTORY.md) | L1/W2 |
| 009–010 | [Governed handoff](../tasks/TASK-RDL-GOVERNED-HANDOFF.md) | L2/W3 |
| 011–012 | [Round trip](../tasks/TASK-RDL-ROUNDTRIP.md) | L2/W3 and L3/W4 |
| 013–014 | [Verify](../tasks/TASK-RDL-VERIFY.md) | L3/W4 |

Selection rule: choose one `ready-unselected` unit from the canonical manifest,
confirm its exact write scope against the live worktree, then invoke Task
Session with only that SWU's contract and source anchors.

