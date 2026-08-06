---
module: wavedb-reviewed-source-build
version: candidate-local-1
status: blocked-node26-runtime
updatedAt: 2026-08-05
docType: work-pack
---

# WORK-PACK: WaveDB reviewed-source build

## Control fields

| Field | Value | Notes |
| --- | --- | --- |
| workPackGateStatus | pass | Authoring gates passed; execution is now acceptance-blocked |
| complexity | medium | Native build, external locked dependencies, multiple material/evidence artifacts |
| outputMode | split | Task and wave contracts are execution-bearing |
| executionPackRef | `EXECUTION-PACK.md` | Cross-task choreography |
| layeringArtifactRef | `IMPLEMENTATION-LAYERING.md` | L0-L3 decision boundaries |
| dispatchTechniqueTrace | `DISPATCH-TECHNIQUE-TRACE.md` | Original route plus separate Node 26 retry dispatch |
| dispatchValidation | `dispatch-validation.json`; `node26-dispatch-validation.json` | Both serial routes passed their planning checks |
| distillValidationStatus | pass | Original plan passed; Node 26 delta was one controlled-variable SWU |
| swuAtomicityStatus | pass | Three independently accepted units; zero task-shaped SWUs |
| firstUnitNarrownessStatus | pass | Runner/validator passed before either native attempt |
| closeoutSyncStatus | pass | All three SWUs have exact owner closeout contracts |
| activeLayerWindow | L0 | Only local feasibility evidence was authorized |
| selectedSWU | none | Node 26 task closed BLOCK; there is no same-pack successor |
| nativeBuildAdmission | block | Both Node 22 and Node 26 compiled/loaded, then blocked in concurrent writes |
| lastUpdatedAt | `2026-08-05T15:55:54Z` | SWU-WCSB-003 terminal block closeout |
| readinessProfile | pilot | Candidate-local evidence only |

## Objective summary

- Objective: produce one verified local WaveDB addon from reviewed commit
  `01c77e8b...` using exact recursive submodules, lockfile dependencies, and
  a pinned Linux toolchain.
- Diagnostic extension: determine whether the Node 22 concurrent-write stall
  reproduces under Node `v26.6.0` and npm `11.18.0`.
- Observed result: both Node versions compile and load the addon, and both
  block in the upstream concurrent-write path; no addon is admitted.
- Primary inputs: source-build Define/Design, deterministic Design selection,
  parent provenance decision, passed runner protocol, and preserved Node 22
  and Node 26 block receipts.
- Claim ceiling: two local Linux x86_64 source-build observations; not root-cause,
  npm provenance, package support, cross-platform, Craft, publication,
  deployment, or production proof.

## Delivery slices

| Slice | Outcome | Layer | Wave | Dependencies | Validation |
| --- | --- | --- | --- | --- | --- |
| S-WCSB-01 | deterministic source-build runner and validator | L0 | [W0](work-pack/waves/W0-SOURCE-BUILD.md) | Design pass | fixture suite and static checks |
| S-WCSB-02 | Node 22 reviewed-source observation | L0 | [W0](work-pack/waves/W0-SOURCE-BUILD.md) | SWU-WCSB-001 pass | blocked at upstream concurrent writes |
| S-WCSB-03 | Node 26 controlled diagnostic observation | L0 | [W0](work-pack/waves/W0-SOURCE-BUILD.md) | protocol pass and preserved Node 22 result | blocked at the same upstream concurrent-write case |
| S-WCSB-L1 | repeatability decision | L1 | [W1](work-pack/waves/W1-REPEATABILITY.md) | L0 owner promotion | deferred |
| S-WCSB-L2 | security/license governance | L2 | [W2](work-pack/waves/W2-GOVERNANCE.md) | L1 owner promotion | deferred |
| S-WCSB-L3 | packaging/platform matrix | L3 | [W3](work-pack/waves/W3-PACKAGING.md) | L2 owner promotion | deferred |

## Task status board

| Task | Goal | Layer | Wave | Gate | Status |
| --- | --- | --- | --- | --- | --- |
| [TASK-WCSB-01](work-pack/tasks/TASK-WCSB-01-RUNNER.md) | implement deterministic runner, validator, schema, and fixtures | L0 | W0 | closed-pass | completed |
| [TASK-WCSB-02](work-pack/tasks/TASK-WCSB-02-EXECUTE.md) | execute exact reviewed-source build under Node 22 | L0 | W0 | closed-block | blocked |
| [TASK-WCSB-03](work-pack/tasks/TASK-WCSB-03-NODE26.md) | diagnose the unchanged build under exact Node 26 | L0 | W0 | closed-block | blocked |

## SWU manifest

| SWU | Parent | Primary behavior | Dependencies | Write scope | Acceptance | Owner | Status |
| --- | --- | --- | --- | --- | --- | --- | --- |
| SWU-WCSB-001 | [TASK-WCSB-01](work-pack/tasks/TASK-WCSB-01-RUNNER.md) | implement and fixture-prove one deterministic source-build protocol | Design pass | `.gitignore`, `runtime/**`, Task Session evidence | static checks plus pass/fail fixtures | Task Session local | pass |
| SWU-WCSB-002 | [TASK-WCSB-02](work-pack/tasks/TASK-WCSB-02-EXECUTE.md) | execute protocol under Node 22 and bind the observation | SWU-WCSB-001 pass | `.work/wcsb-20260804-01/**`, `execution/source-build/**`, Task Session evidence | exact live receipt validator and scope audit | Task Session local | blocked |
| SWU-WCSB-003 | [TASK-WCSB-03](work-pack/tasks/TASK-WCSB-03-NODE26.md) | execute the unchanged protocol under exact Node 26 | SWU-WCSB-001 pass, SWU-WCSB-002 terminal receipt, retry dispatch pass | `.work/wcsb-20260805-node26-01/**`, `execution/source-build-node26/**`, Task Session evidence | exact toolchain, live receipt validator, and scope audit | Task Session local | blocked |

## SWU atomicity review

| SWU | Candidate child units | Retained-boundary rationale | Independent acceptance | Verdict |
| --- | --- | --- | --- | --- |
| SWU-WCSB-001 | runner, schema, validator, fixtures | none is safely executable/reviewable without the shared protocol and its positive/negative validator proof | complete protocol can pass without running a native build | pass |
| SWU-WCSB-002 | source fetch, dependencies, generated source, build, load, tests | intermediate stages cannot produce an admissible addon | terminal Node 22 observation is independently reviewable | pass |
| SWU-WCSB-003 | Node installation, source fetch, build, tests, receipt | changing only the Node/npm identity is the experiment; partial stages cannot establish compatibility | terminal Node 26 observation is independently reviewable against SWU-WCSB-002 | pass |

The Node 26 unit established a bounded comparison even though acceptance
blocked: the build/load boundary passes and the runtime test boundary does not.

## Task Session closeout synchronization contract

| SWU | Owner route | Terminal receipt | Exact synchronization targets | Baseline binding | Delta classes | Owner validation | Expected owner receipt | Successor |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| SWU-WCSB-001 | `invoke:refresh:apply-approved` | `execution/task-sessions/SWU-WCSB-001/terminal-receipt.json` | Work Pack, task, W0 | live SHA-256 | evidence/blocker/status/route | protocol validations | `execution/task-sessions/SWU-WCSB-001/invoke-refresh-receipt.json` | SWU-WCSB-002 on pass |
| SWU-WCSB-002 | `invoke:refresh:apply-approved` | `execution/task-sessions/SWU-WCSB-002/terminal-receipt.json` | Work Pack, task, W0 | live SHA-256 and SWU-WCSB-001 receipt | evidence/blocker/status/route | receipt/scope/attempt validations | `execution/task-sessions/SWU-WCSB-002/invoke-refresh-receipt.json` | none on block |
| SWU-WCSB-003 | `invoke:refresh:apply-approved` | `execution/task-sessions/SWU-WCSB-003/terminal-receipt.json`; pass/block, exact toolchain, manifests, addon identity, tests, effects, and blocker | `plan/WORK-PACK.md`; `plan/EXECUTION-PACK.md`; `plan/work-pack/tasks/TASK-WCSB-03-NODE26.md`; `plan/work-pack/waves/W0-SOURCE-BUILD.md`; `plan/work-pack/shared/traceability.md`; `plan/work-pack/shared/cross-task-gaps.md` | Task Session preflight records live SHA-256 for all targets and retry-dispatch validation | `evidence_added`, `blocker_opened`, `blocker_resolved`, `status_changed`, `route_changed` | terminal/block receipt hashes, exact Node/npm check, previous-attempt immutability, Craft/NVM/process scope checks, target digest comparison | `execution/task-sessions/SWU-WCSB-003/invoke-refresh-receipt.json` | none on block |

Closeout authorization is bookkeeping-only. It cannot execute another SWU,
change Craft authority, publish, deploy, clean build state, change NVM default,
or silently admit an addon to the parent plan.

## Validation strategy

| Boundary | Acceptance-critical evidence |
| --- | --- |
| Plan | original Dispatch/Distill pass plus Node 26 retry Dispatch pass, navigable SWU contract, closeout row |
| Runner | existing syntax/help/schema/fixture/static proof remains unchanged |
| Source | exact root commit, clean tracked baseline, recursive gitlinks, complete source manifest |
| Dependencies | exact lockfile hash, `npm ci --ignore-scripts`, integrity-resolved tree, unchanged lockfile |
| Toolchain | Node `v26.6.0`, npm `11.18.0`, existing Python/GCC/G++/Make/linker/OpenSSL pins |
| Generated source/build | complete `c_src`, exactly one addon, live addon hash |
| Verification | addon load passed; upstream concurrent-write case blocked; canary did not run |
| Scope | previous attempts, NVM default, Craft, Git history, registry publication, deployment, and out-of-scope paths unchanged |

Every obligation is acceptance-critical. Partial compilation/load evidence is
not promoted into compatibility or handoff evidence.

## Current blockers and risks

Historical blocker `WCSB-UPSTREAM-CONCURRENT-WRITE-STALL` remains open for the
Node 22 attempt. Node 26 reproduced the same test location and opened
`WCSB-NODE26-CONCURRENT-WRITE-LIVELOCK`; this narrows the version hypothesis but
does not establish a root cause.

| Risk | Observed trigger | Behavior |
| --- | --- | --- |
| concurrent-write native livelock | same upstream case under Node 22 and Node 26 | block addon handoff; source owner diagnosis required |
| operator termination of verified test child | no file progress and near-one-core CPU for 338.233 seconds | record `-15` as operator SIGTERM, not crash/assertion proof |
| test manifest/canary absent | upstream tests did not pass | no compatibility or empty-value claim |
| Node 26 is non-LTS | exact diagnostic runtime only | no general support recommendation |

## Gate checks

- Define and Design: existing pass, unchanged.
- Original Plan/Dispatch/Distill: existing pass, unchanged historical evidence.
- Node 26 refresh context: strict 8/8 obligation coverage.
- Node 26 retry dispatch: pass.
- Selected unit: none; SWU-WCSB-003 closed BLOCK.
- Attempt identity: `wcsb-20260805-node26-01`, preserved and single-use.
- Native build/load: pass under Node 26; runtime acceptance: block.
- Addon handoff: null; pass receipt: absent.
- Subagents: none; the route was one serial controlled-variable experiment.

## Required links

- [Execution Pack](EXECUTION-PACK.md)
- [Implementation Layering](IMPLEMENTATION-LAYERING.md)
- [Architecture](../design/ARCHITECTURE.md)
- [Node 26 retry dispatch](node26-retry.dispatch.json)
- [Shared context](work-pack/shared/context.md)
- [Traceability](work-pack/shared/traceability.md)
- [Cross-task gaps](work-pack/shared/cross-task-gaps.md)
- [Node 26 terminal receipt](../execution/task-sessions/SWU-WCSB-003/terminal-receipt.json)

## Change log

| Date | Change | Author |
| --- | --- | --- |
| 2026-08-05 | Closed Node 26 diagnostic BLOCK at the same upstream concurrent-write case; no addon handoff or successor | Codex Invoke Refresh |
| 2026-08-05 | Added exact Node 26 diagnostic SWU and fresh attempt; corrected stale Execution Pack selector | Codex Invoke Refresh |
| 2026-08-04 | SWU-WCSB-002 blocked in upstream concurrent-write test; cleared selection | Codex Invoke Refresh |
| 2026-08-04 | SWU-WCSB-001 passed; selected exact live-build successor | Codex Invoke Refresh |
| 2026-08-04 | Initial source-build Work Pack; selected runner SWU | Codex Invoke Plan |
