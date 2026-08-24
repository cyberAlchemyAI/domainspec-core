# Context Pack: Craft–WaveDB Read-Only Experiment

## Control metadata

- Pack ID: `CRAFT-WAVEDB-READONLY-EXPERIMENT-001`
- Mode: proposed one-shot stream
- Status: `proposal-complete; runtime-blocked`
- Authority effect: none
- Execution authorization: absent
- Decision profile: none
- Runtime owner: native Codex Goal after admission
- Bounded execution owner: one Task Session per node
- Subagents: prohibited unless a later Work Pack explicitly admits them

## Outcome

Produce one closed, repository-local experiment showing that separate Node
processes can read the accepted WaveDB-derived Craft snapshot without modifying
the canonical Craft ledgers or the accepted original store. Add only a minimal
read-only experiment interface, verify positive and negative behavior, and close
with one terminal receipt.

“Closed” means a finite work-and-acceptance envelope. It does not mean a
hermetic, vendored, portable, published, or deployable package.

## Bound source contracts

| Source | SHA-256 | Role |
|---|---|---|
| `ops/development/2026-08-04-wavedb-craft-runtime-research/development/refinement-runs/20260805T184540Z-craft-wavedb-api/WORK-PACK.md` | `72ca5698a2bbcba8dc70c707c5cfac914d36cebc4efeadea41df11cab49f1174` | Live plan frontier, route state, blockers, and claim boundary |
| `ops/development/2026-08-04-wavedb-craft-runtime-research/development/refinement-runs/20260805T184540Z-craft-wavedb-api/work-pack/tasks/TASK-RUNTIME.md` | `9fd826b1086b9647e665438d16e70662a3da3107d755740505e1f44937543cc6` | Accepted runtime unit and fresh-process witness contract |
| `ops/development/2026-08-04-wavedb-craft-runtime-research/experiment/craft-ledger-import/execution/wcli-20260805-node26-0.15.9-03/receipt.json` | `544e6bcd81ede733c2e313e18f04ca61a6b5da76e2cc21aff15ddde5d26f046f` | Accepted snapshot identity and evidence |

Any hash drift blocks execution and requires a reviewed profile refresh. No
fallback discovery is authorized from this pack.

## Accepted input evidence

The accepted `-03` receipt proves only the following relevant facts:

- environment: Node `v26.6.0`, Linux x64;
- dependency: npm `@vijayee/wavedb@0.15.9`;
- tarball SHA-256:
  `e8156c107117c8bc7f3394ceb16dff439c87c0cb4f8991033dad960b13ae396f`;
- tarball SRI:
  `sha512-qoRqZUti9Rjs9UT4rj8cQKNv2Gdr8bJ25p6miU4dKojLeBMfzkgQqp+D/fd2PsaItXyhgMLrlx/wQUmyj/W8hA==`;
- native addon SHA-256:
  `4846a91117cfeaee42011e401e65448216d85c0ebd04fc860585e3a32e17bb3b`;
- exact selected authority inventory: 28 `.craft/ledger.yml` files totaling
  814,003 bytes;
- derived snapshot: 57 records under `craft/manifest/v2`;
- manifest SHA-256:
  `780aa8e586eab13bb7478e47783a95017162b41f4834a6be1c7f097aad155014`;
- accepted store tree: 3 files, 947,034 bytes, digest
  `7ce467aa44b6504347eaef89f601eb04b49647613649314f09fffbe8862289b2`;
- 426 assertions passed for package identity, selected inventory, lossless input,
  immediate readback, same-process reopen, and source/protected-scope
  immutability.

This evidence does not prove fresh-process access, a stable API, portability,
deployment, or production readiness.

## Read-only runtime inputs

Execution may read, but never mutate:

- accepted store:
  `ops/development/2026-08-04-wavedb-craft-runtime-research/experiment/craft-ledger-import/.work/wcli-20260805-node26-0.15.9-03/store/`;
- accepted receipt and its exact 28 source-ledger members;
- locally resolved WaveDB module:
  `ops/development/2026-08-04-wavedb-craft-runtime-research/experiment/source-build/.work/wcnd-20260805-node26-02/consumer/node_modules/@vijayee/wavedb/lib/wavedb.js`;
- the local native addon resolved from that module, only after its digest matches
  the accepted addon digest.

The local `.work/` inputs make this a checkout-local experiment. If any input is
missing, moved, or mismatched, stop. Do not download, reinstall, vendor, rebuild,
or substitute a dependency.

## Proposed finite graph

The graph is strictly serial: `CWE-001 -> CWE-002 -> CWE-003`. A node may start
only after the prior node has an accepted receipt. Failure closes the Goal as
blocked; no successor is selected automatically.

### CWE-001 — Independent reader proof

- Adopt the evidence obligations of current `SWU-CAPI-001` without claiming it
  is presently selected.
- Create isolated copies of the accepted store inside the admitted experiment
  root.
- Launch two separate Node `v26.6.0` reader processes, one per isolated copy,
  after the builder process is absent.
- Verify the manifest key and digest plus all 57 exact record lengths and
  SHA-256 values, normalizing observed string/buffer values only to exact bytes.
- Compare pre/post hashes of all canonical sources and the accepted original
  store.
- Emit a node receipt. Do not write to WaveDB or the original store.

### CWE-002 — Minimal read-only experiment interface

Create an experiment-local adapter and CLI exposing exactly:

- `status` — report bound runtime/snapshot identity and availability;
- `verify` — verify manifest closure and every expected record;
- `list-ledgers` — list only manifest-declared Craft ledger members;
- `get-raw` — return exact bytes only for a manifest-declared record key.

The adapter must not export or make reachable any WaveDB writer, mutation method,
or `Subtree` surface. It must not normalize Craft domain rows, write back to
Craft, listen on a socket, or add an HTTP/authentication layer. Unknown keys and
read failures return a typed non-success result without partial data.

### CWE-003 — Negative controls and terminal closeout

- Exercise missing-key, damaged-manifest/record, and open/read-failure cases only
  on disposable isolated copies.
- Fail closed: no partial-success receipt, no fallback source, and no continued
  reads from a failed handle within this experiment process.
- Re-run complete verification against a clean isolated copy.
- Prove canonical source and accepted original-store digests are unchanged.
- Validate every JSON receipt and emit one terminal Goal receipt.
- Leave all API/product units unselected.

These checks are experiment evidence only. They do not satisfy or claim the
product invalidation behavior planned by `SWU-CAPI-003`.

## Proposed write boundary

After admission, all new implementation, disposable copies, fixtures, logs, and
receipts must remain below this single root:

`ops/development/2026-08-04-wavedb-craft-runtime-research/experiment/craft-wavedb-readonly-experiment/`

No path under that root exists as an authorized runtime target today. An applied
Invoke Refresh must own the exact subpaths and validation commands before Goal
execution.

## Capability policy

After admission and separate execution authorization:

- native Goal may control the ordered frontier and terminal status;
- `task-session` may execute exactly one admitted node at a time;
- `decision-gate` may only report a newly encountered blocker and stop;
- `invoke`, `refine`, `craft`, and subagents are not ambient runtime authority;
- no network, dependency installation, npm publication, Docker work, Git
  mutation, deployment, or external transport is allowed.

Any needed capability or path outside this policy requires a new reviewed
refresh and operator authorization.

## Terminal acceptance contract

The Goal may complete only when one terminal receipt proves:

1. every bound source and dependency identity matched before execution;
2. both independent readers passed against separate isolated copies;
3. the manifest and all 57 records matched exact lengths and SHA-256 values;
4. the four-command interface passed positive, missing-key, and failure controls;
5. no writer or `Subtree` surface was reachable from the adapter;
6. every JSON receipt validated;
7. the exact 28 canonical sources and accepted original store were unchanged;
8. all writes remained inside the admitted experiment root; and
9. no API, successor, publication, Docker, deployment, or production claim was
   made.

Maximum terminal claim:

> A repeatable checkout-local, read-only experiment independently accessed the
> accepted derived Craft snapshot without changing canonical source or accepted
> store bytes.

## Current blockers and exact unblock action

Runtime readiness is `block` because:

1. the current Work Pack has `allowedRoutes: []`;
2. `SWU-CAPI-001` is dependency-ready but not selected;
3. `CRAFT-WAVEDB-READONLY-EXPERIMENT-001` is not an admitted one-shot stream;
4. the proposed experiment root and exact validation commands are not owned; and
5. the operator authorized proposal creation only, not execution.

Unblock by applying a reviewed Invoke Refresh that admits this exact stream,
capability policy, write root, node bindings, validation commands, and terminal
receipt contract. Then obtain separate operator authorization to execute the
closed Goal.

`CAPI-B001`, `CAPI-B002`, and `CAPI-B004` remain product/API/deployment blockers.
They do not become resolved through this experiment.
