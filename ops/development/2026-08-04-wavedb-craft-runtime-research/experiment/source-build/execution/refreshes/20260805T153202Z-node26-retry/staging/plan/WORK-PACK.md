---
module: wavedb-reviewed-source-build
version: candidate-local-1
status: active-node26-diagnostic
updatedAt: 2026-08-05
docType: work-pack
---

# WORK-PACK: WaveDB reviewed-source build

## Control fields

| Field | Value | Notes |
| --- | --- | --- |
| workPackGateStatus | pass | Authoring gates pass for selected SWU only |
| complexity | medium | Native build, external locked dependencies, multiple material/evidence artifacts |
| outputMode | split | Task and wave contracts are execution-bearing |
| executionPackRef | `EXECUTION-PACK.md` | Cross-task choreography |
| layeringArtifactRef | `IMPLEMENTATION-LAYERING.md` | L0-L3 decision boundaries |
| dispatchTechniqueTrace | `DISPATCH-TECHNIQUE-TRACE.md` | Original route plus separate Node 26 retry dispatch |
| dispatchValidation | `dispatch-validation.json`; Node 26 retry must validate separately | Both routes are serial and fail closed |
| distillValidationStatus | pass | Original plan passed; Node 26 delta is one controlled-variable SWU |
| swuAtomicityStatus | pass | Three independently accepted units; zero task-shaped SWUs |
| firstUnitNarrownessStatus | pass | Runner/validator passed before either native attempt |
| closeoutSyncStatus | pass | All three SWUs have exact owner closeout contracts |
| activeLayerWindow | L0 | Only local feasibility proof is authorized |
| selectedSWU | `SWU-WCSB-003` | Exact Node 26 diagnostic selected by direct user request |
| nativeBuildAdmission | pending-task-session | Requires live Task Session admission and exact toolchain identity |
| lastUpdatedAt | `2026-08-05T15:32:02Z` | Direct-user Node 26 retry refresh |
| readinessProfile | pilot | Candidate-local evidence only |

## Objective summary

- Objective: produce one verified local WaveDB addon from reviewed commit
  `01c77e8b...` using exact recursive submodules, lockfile dependencies, and
  a pinned Linux toolchain.
- Diagnostic extension: determine whether the Node 22 concurrent-write stall
  reproduces under Node `v26.6.0` and npm `11.18.0`.
- Primary inputs: source-build Define/Design, deterministic Design selection,
  parent provenance decision, passed runner protocol, and the preserved Node 22
  block receipt.
- Success: the selected SWU passes every runner stage, its terminal receipt
  binds all inputs and outputs, and no forbidden effect occurs.
- Claim ceiling: one local Linux x86_64 Node 26 source-build observation; not
  npm provenance, package support, cross-platform, Craft, publication,
  deployment, or production proof.

## Delivery slices

| Slice | Outcome | Layer | Wave | Dependencies | Validation |
| --- | --- | --- | --- | --- | --- |
| S-WCSB-01 | deterministic source-build runner and validator | L0 | [W0](work-pack/waves/W0-SOURCE-BUILD.md) | Design pass | fixture suite and static checks |
| S-WCSB-02 | Node 22 reviewed-source observation | L0 | [W0](work-pack/waves/W0-SOURCE-BUILD.md) | SWU-WCSB-001 pass | blocked at upstream concurrent writes |
| S-WCSB-03 | Node 26 controlled diagnostic observation | L0 | [W0](work-pack/waves/W0-SOURCE-BUILD.md) | protocol pass and preserved Node 22 result | exact live receipt validator and scope audit |
| S-WCSB-L1 | repeatability decision | L1 | [W1](work-pack/waves/W1-REPEATABILITY.md) | L0 owner promotion | deferred |
| S-WCSB-L2 | security/license governance | L2 | [W2](work-pack/waves/W2-GOVERNANCE.md) | L1 owner promotion | deferred |
| S-WCSB-L3 | packaging/platform matrix | L3 | [W3](work-pack/waves/W3-PACKAGING.md) | L2 owner promotion | deferred |

## Task status board

| Task | Goal | Layer | Wave | Gate | Status |
| --- | --- | --- | --- | --- | --- |
| [TASK-WCSB-01](work-pack/tasks/TASK-WCSB-01-RUNNER.md) | implement deterministic runner, validator, schema, and fixtures | L0 | W0 | closed-pass | completed |
| [TASK-WCSB-02](work-pack/tasks/TASK-WCSB-02-EXECUTE.md) | execute exact reviewed-source build under Node 22 | L0 | W0 | closed-block | blocked |
| [TASK-WCSB-03](work-pack/tasks/TASK-WCSB-03-NODE26.md) | diagnose the unchanged build under exact Node 26 | L0 | W0 | selected | ready |

## SWU manifest

| SWU | Parent | Primary behavior | Dependencies | Write scope | Acceptance | Owner | Status |
| --- | --- | --- | --- | --- | --- | --- | --- |
| SWU-WCSB-001 | [TASK-WCSB-01](work-pack/tasks/TASK-WCSB-01-RUNNER.md) | implement and fixture-prove one deterministic source-build protocol | Design pass | `.gitignore`, `runtime/**`, Task Session evidence | static checks plus pass/fail fixtures | Task Session local | pass |
| SWU-WCSB-002 | [TASK-WCSB-02](work-pack/tasks/TASK-WCSB-02-EXECUTE.md) | execute protocol under Node 22 and bind the observation | SWU-WCSB-001 pass | `.work/wcsb-20260804-01/**`, `execution/source-build/**`, Task Session evidence | exact live receipt validator and scope audit | Task Session local | blocked |
| SWU-WCSB-003 | [TASK-WCSB-03](work-pack/tasks/TASK-WCSB-03-NODE26.md) | execute the unchanged protocol under exact Node 26 | SWU-WCSB-001 pass, SWU-WCSB-002 terminal receipt, retry dispatch pass | `.work/wcsb-20260805-node26-01/**`, `execution/source-build-node26/**`, Task Session evidence | exact toolchain, live receipt validator, and scope audit | Task Session local | selected |

## SWU atomicity review

| SWU | Candidate child units | Retained-boundary rationale | Independent acceptance | Verdict |
| --- | --- | --- | --- | --- |
| SWU-WCSB-001 | runner, schema, validator, fixtures | none is safely executable/reviewable without the shared protocol and its positive/negative validator proof | complete protocol can pass without running a native build | pass |
| SWU-WCSB-002 | source fetch, dependencies, generated source, build, load, tests | intermediate stages cannot produce an admissible addon | terminal Node 22 observation is independently reviewable | pass |
| SWU-WCSB-003 | Node installation, source fetch, build, tests, receipt | changing only the Node/npm identity is the experiment; partial stages cannot establish compatibility | terminal Node 26 observation is independently reviewable against SWU-WCSB-002 | pass |

The first unit remains the narrowest reversible trust-building step. The new
third unit is the smallest coherent controlled-variable diagnostic: it changes
only Node/npm identity and uses a fresh namespace.

## Task Session closeout synchronization contract

| SWU | Owner route | Terminal receipt | Exact synchronization targets | Baseline binding | Delta classes | Owner validation | Expected owner receipt | Successor |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| SWU-WCSB-001 | `invoke:refresh:apply-approved` | `execution/task-sessions/SWU-WCSB-001/terminal-receipt.json` | Work Pack, task, W0 | live SHA-256 | evidence/blocker/status/route | protocol validations | `execution/task-sessions/SWU-WCSB-001/invoke-refresh-receipt.json` | SWU-WCSB-002 on pass |
| SWU-WCSB-002 | `invoke:refresh:apply-approved` | `execution/task-sessions/SWU-WCSB-002/terminal-receipt.json` | Work Pack, task, W0 | live SHA-256 and SWU-WCSB-001 receipt | evidence/blocker/status/route | receipt/scope/attempt validations | `execution/task-sessions/SWU-WCSB-002/invoke-refresh-receipt.json` | none on block |
| SWU-WCSB-003 | `invoke:refresh:apply-approved` | `execution/task-sessions/SWU-WCSB-003/terminal-receipt.json`; pass/block, exact toolchain, manifests, addon identity, tests, effects, and blocker | `plan/WORK-PACK.md`; `plan/EXECUTION-PACK.md`; `plan/work-pack/tasks/TASK-WCSB-03-NODE26.md`; `plan/work-pack/waves/W0-SOURCE-BUILD.md`; `plan/work-pack/shared/traceability.md`; `plan/work-pack/shared/cross-task-gaps.md` | Task Session preflight records live SHA-256 for all targets and retry-dispatch validation | `evidence_added`, `blocker_opened`, `blocker_resolved`, `status_changed`, `route_changed` | terminal receipt validator, exact Node/npm check, previous-attempt immutability, scope scan, target digest comparison | `execution/task-sessions/SWU-WCSB-003/invoke-refresh-receipt.json` | no same-pack successor; parent Invoke Refresh only on pass |

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
| Verification | addon loads, same upstream tests pass, empty-value canary passes |
| Scope | previous attempts, NVM default, Craft, Git history, registry publication, deployment, and out-of-scope paths unchanged |

Every obligation is acceptance-critical. No unavailable or substitute check is
treated as pass.

## Current blockers and risks

Historical blocker `WCSB-UPSTREAM-CONCURRENT-WRITE-STALL` remains open for the
Node 22 attempt. The Node 26 task is a direct-user-authorized diagnostic, not a
claim that this blocker is resolved.

| Risk | Trigger | Behavior |
| --- | --- | --- |
| Node 26 unavailable or wrong npm | installation/identity mismatch | block before source execution; do not substitute a different 26.x |
| node-gyp/Python/compiler incompatibility | configure or build failure | block exact attempt; do not substitute toolchain |
| OpenSSL/header/link mismatch | build or load failure | block; no implicit no-OpenSSL fallback |
| dependency integrity failure | `npm ci` failure | block; no alternate package or lock rewrite |
| concurrent-write stall or other test failure | upstream test does not pass | block addon handoff and preserve evidence |
| unexpected filesystem effect | scope audit detects path | block even if tests pass |

## Gate checks

- Define and Design: existing pass, unchanged.
- Original Plan/Dispatch/Distill: existing pass, unchanged historical evidence.
- Node 26 refresh context: strict 8/8 obligation coverage.
- Node 26 retry dispatch: required pass before Task Session.
- Selected unit: `SWU-WCSB-003` only.
- Attempt identity: `wcsb-20260805-node26-01`, fresh and single-use.
- Native build: pending Task Session mutation admission and exact NVM toolchain.
- Subagents: none; the route is one serial controlled-variable experiment.

## Required links

- [Execution Pack](EXECUTION-PACK.md)
- [Implementation Layering](IMPLEMENTATION-LAYERING.md)
- [Architecture](../design/ARCHITECTURE.md)
- [Node 26 retry dispatch](node26-retry.dispatch.json)
- [Shared context](work-pack/shared/context.md)
- [Traceability](work-pack/shared/traceability.md)
- [Cross-task gaps](work-pack/shared/cross-task-gaps.md)

## Change log

| Date | Change | Author |
| --- | --- | --- |
| 2026-08-05 | Added exact Node 26 diagnostic SWU and fresh attempt; corrected stale Execution Pack selector | Codex Invoke Refresh |
| 2026-08-04 | SWU-WCSB-002 blocked in upstream concurrent-write test; cleared selection | Codex Invoke Refresh |
| 2026-08-04 | SWU-WCSB-001 passed; selected exact live-build successor | Codex Invoke Refresh |
| 2026-08-04 | Initial source-build Work Pack; selected runner SWU | Codex Invoke Plan |
