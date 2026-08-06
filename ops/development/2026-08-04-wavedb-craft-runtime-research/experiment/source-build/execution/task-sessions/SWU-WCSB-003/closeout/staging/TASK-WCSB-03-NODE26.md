# TASK-WCSB-03: diagnose the source build on Node 26

## Execution status

- Status: `blocked`.
- Selected: no.
- Direct authorization: user request `update to node 26` on 2026-08-05.
- Attempt: `wcsb-20260805-node26-01`; preserved and closed.
- Toolchain delta: Node `v26.6.0` and npm `11.18.0` only.
- Source identity: WaveDB `0.15.8` at
  `01c77e8b70f71de9b72480e73a3a179f6e93a009`.
- Terminal receipt: `../../../execution/task-sessions/SWU-WCSB-003/terminal-receipt.json`.
- Result: source, dependencies, generation, native compilation, addon identity,
  and addon load passed; the same upstream concurrent-write case observed under
  Node 22 made no progress under Node 26.
- Handoff: none; `addon_handoff` is null and no pass receipt exists.

## Objective and mapping

- Slice: S-WCSB-03.
- Layer/wave: L0 / W0.
- Objective: run the validated protocol once under the exact Node 26
  toolchain to determine whether the concurrent-write stall reproduces.
- Observation: the stall reproduced at the same named case. This is evidence
  against a Node-22-only explanation in this environment, not root-cause proof.
- Claim ceiling: partial local Linux x86_64 Node 26 source-build evidence.

## Bound identities

- WaveDB commit: `01c77e8b70f71de9b72480e73a3a179f6e93a009`.
- Node/npm: `v26.6.0` / `11.18.0`.
- Source manifest: `d86e76152a157fb31c5d4ff60453631798a041b6586dac80216366b4086f6456`.
- Dependency manifest: `bd0983eba16498accf8d88af1fe7d37fe4eae93fea7f9e3d91a8ab022ac25f1b`.
- Generated-source manifest: `75887675eb823fbd0e2f3e850acdc51df111d205404ad4b0a970c8cd58308512`.
- Build manifest: `b3ebebc851290976322982dd52321158d174b52ce4f3004e0bc89c95d798eda7`.
- Addon: `cbd5ebdab82635cf95ced5b0d3d3b50de7c224a6d99ebc2aa1dad57afb2ea8c9`,
  1,223,576 bytes; load observation passed; handoff forbidden.
- Block receipt: `de939bc2d617f522c45fb4739c7509cac8c6d934d9063c5a3b38197cecefa753`.
- Upstream log: `012e05ee5e912ca1d09027680981809e576134511920c4fc90dd804e729b5f13`.

## Blocker

`WCSB-NODE26-CONCURRENT-WRITE-LIVELOCK` is open. The verified Mocha child
reached `WaveDB Integration -> concurrent operations -> should handle concurrent
writes`, remained near one core of CPU with nine threads, and stopped changing
the fresh DB/WAL files. After 338.233 seconds of this liveness observation, the
operator sent SIGTERM only to that verified child.

Exit `-15` therefore records the controlled termination. It is not an upstream
assertion, timeout summary, or crash. Terminating outside the runner deviated
from the task's preferred stop mechanism, so this attempt cannot support a pass
even independently of the observed livelock.

Smallest unblock: the WaveDB source owner instruments or debugs the concurrent-
write native runtime path and provides a reviewed source change or diagnosis.
Any later execution requires a newly planned immutable attempt; changing Node
again is not an evidenced next step.

## Acceptance result

| Gate | Result |
| --- | --- |
| source and recursive submodules | pass |
| lockfile-only dependencies | pass |
| exact toolchain | pass |
| generated source | pass |
| native build | pass |
| addon cardinality/hash/load | pass |
| upstream tests | block |
| empty-value canary | not run after blocker |
| test manifest/final receipt validator | not run; pass receipt absent |
| addon handoff | null |

The Node 22 receipt, log, and addon hashes remained unchanged. The NVM default
alias remained `22 -> v22.13.0`. No Craft mutation, publication, deployment,
destructive cleanup, or Git-history mutation was observed.

## Preserved residue

- `.work/wcsb-20260805-node26-01/**`;
- `execution/source-build-node26/**`;
- `/tmp/wavedb-integration-1785944869024-2isb9brlg`;
- the separately preserved Node 22 attempt and evidence.

Execution owner: Task Session local. Closeout returns no same-pack successor and
does not admit a parent refresh because the source-build result is BLOCK.
