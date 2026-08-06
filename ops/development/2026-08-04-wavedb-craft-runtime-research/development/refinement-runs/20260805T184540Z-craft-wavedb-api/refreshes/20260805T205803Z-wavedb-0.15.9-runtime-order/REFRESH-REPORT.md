# Invoke Refresh Report: WaveDB 0.15.9 Runtime Order

- mode: `refresh`
- phase status: `pass`
- mutation handoff: `ready`
- target lifecycle: `blocked`
- activation source: `direct-user`
- mutation mode: `apply-approved` (`default-direct-user`)
- material package: `capi-refresh-wavedb-0.15.9-runtime-order-20260805T205803Z`
- material digest: `35a10a74ea21a0bca322ca850ec9715d85c3953483e64d1d872c6a3cfb45a98b`

## Outcome

The current Craft API Work Pack now makes the WaveDB `0.15.9` runtime transition explicit without starting ingestion or API implementation:

1. `SWU-CAPI-000` must regenerate a new immutable Craft ledger snapshot with the verified `wavedb@0.15.9` npm artifact under Node `26.6.0` and prove the expected `27` ledgers and `55` records or block on drift.
2. `SWU-CAPI-001` must launch a separate fresh process and read the closed `0.15.9` snapshot.
3. Before `SWU-CAPI-002`, the API runtime must pin the exact Node version, package version, tarball digest, npm integrity string, and native addon digest.
4. Only then may `SWU-CAPI-002` through `SWU-CAPI-007` implement the L0 core `get`/`read` API, followed by the separately bounded L1 units `SWU-CAPI-008` and `SWU-CAPI-009`.

The prior `0.15.8` snapshot remains historical evidence and was not relabeled as `0.15.9` evidence.

## Applied Targets

- `WORK-PACK.md` — `499c2f102b0485b0450fd0bc8bf1895817f7704793789a839b864a491071669d`
- `work-pack/tasks/TASK-RUNTIME.md` — `e635aa9fd50b70ad16423801f0b44f7668bba318e31820c2da42cdf66431e13f`
- `work-pack/waves/W1.md` — `76d0c87a122506deb7326c5d1cc182296f93eef124f86f26f600fc47f06147f8`
- `EXECUTION-PACK.md` — `cdcb56bf0568b7afcc41dcd32d97fbc1c9c5e9316f9e6cb95f9b3bfbe01d6aa7`

## Validation

- The Dispatch Spec validates with no flags or blocks after one documented metadata repair.
- The material package schema, patch verdict, dependencies, owner boundary, publication boundary, and mutation handoff all pass.
- All four applied targets are byte-identical to the validated material outputs.
- The Work Pack contains the stable IDs `SWU-CAPI-000` through `SWU-CAPI-009`.
- `workPackGateStatus=block`, `executionEntry.state=blocked`, and `allowedRoutes=[]` remain unchanged.
- The exact `0.15.9` package, tarball, integrity, addon, and Node pins are present.
- All refresh JSON parses and scoped trailing-whitespace checks pass.
- Prior diagnostic and Craft import receipt hashes remain unchanged.
- No Craft ledger, API implementation, public Arcanum, Git history, publication, or deployment mutation occurred.

## Remaining Gates

- `CAPI-B001`: the owner has not selected the next bounded work unit.
- `CAPI-B002`: no Task Session admission authorizes product mutation.
- `CAPI-B003`: the `0.15.9` Craft snapshot and its independent fresh-process evidence do not exist yet.
- `CAPI-B004`: L1 subtree behavior remains deferred until the L0 core passes.

`handoffStatus=ready` applies only to this validated refresh mutation. It is not API implementation readiness and does not open the Work Pack execution gate.

## Next Route

Resolve the owner selection through `decision-gate`. If the owner selects the new runtime predecessor, separately authorize a `task-session` for `SWU-CAPI-000` only.

## Helper Closeout

One bounded read-only background helper reviewed the refresh delta. It made no repository changes and is closed. This was not a governed multi-agent dispatch.
