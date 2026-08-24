---
module: wavedb-reviewed-source-build
version: candidate-local-1
status: blocked-upstream-runtime
updatedAt: 2026-08-04
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
| layeringArtifactRef | `IMPLEMENTATION-LAYERING.md` | L0–L3 decision boundaries |
| dispatchTechniqueTrace | `DISPATCH-TECHNIQUE-TRACE.md` | Full dispatch validates separately |
| dispatchValidation | `dispatch-validation.json` | Must be `pass` before execution |
| distillValidationStatus | pass | `PLAN-DISTILL-VALIDATION.md` |
| swuAtomicityStatus | pass | Two independently accepted units; zero task-shaped SWUs |
| firstUnitNarrownessStatus | pass | Runner/validator before any network/native build |
| closeoutSyncStatus | pass | Both SWUs have exact owner closeout contracts |
| activeLayerWindow | L0 | Only local feasibility proof is authorized |
| selectedSWU | `none` | Failed SWU has no same-pack successor |
| nativeBuildAdmission | block | Upstream concurrent-write acceptance stalled |
| lastUpdatedAt | `2026-08-04T20:36:53Z` | SWU-WCSB-002 blocked closeout |
| readinessProfile | pilot | Candidate-local evidence only |

## Objective summary

- Objective: produce one verified local WaveDB addon from reviewed commit
  `01c77e8b...` using exact recursive submodules, lockfile dependencies, and
  the observed Linux toolchain.
- Primary inputs: source-build Define/Design, deterministic Design selection,
  parent provenance decision, reviewed WaveDB build contracts.
- Success: both SWUs pass, the terminal source-build receipt binds all inputs
  and outputs, and no forbidden effect occurs.
- Claim ceiling: one local Linux x86_64 source-build observation; not npm,
  package, cross-platform, Craft, publication, deployment, or production proof.

## Delivery slices

| Slice | Outcome | Layer | Wave | Dependencies | Validation |
| --- | --- | --- | --- | --- | --- |
| S-WCSB-01 | deterministic source-build runner and validator | L0 | [W0](work-pack/waves/W0-SOURCE-BUILD.md) | Design pass | fixture suite and static checks |
| S-WCSB-02 | one verified local source-build receipt | L0 | [W0](work-pack/waves/W0-SOURCE-BUILD.md) | SWU-WCSB-001 pass | live source/build/test validator |
| S-WCSB-L1 | repeatability decision | L1 | [W1](work-pack/waves/W1-REPEATABILITY.md) | L0 owner promotion | deferred |
| S-WCSB-L2 | security/license governance | L2 | [W2](work-pack/waves/W2-GOVERNANCE.md) | L1 owner promotion | deferred |
| S-WCSB-L3 | packaging/platform matrix | L3 | [W3](work-pack/waves/W3-PACKAGING.md) | L2 owner promotion | deferred |

## Task status board

| Task | Goal | Layer | Wave | Gate | Status |
| --- | --- | --- | --- | --- | --- |
| [TASK-WCSB-01](work-pack/tasks/TASK-WCSB-01-RUNNER.md) | implement deterministic runner, validator, schema, and fixtures | L0 | W0 | closed-pass | completed |
| [TASK-WCSB-02](work-pack/tasks/TASK-WCSB-02-EXECUTE.md) | execute one exact reviewed-source build and verify addon | L0 | W0 | closed-block | blocked |

## SWU manifest

| SWU | Parent | Primary behavior | Dependencies | Write scope | Acceptance | Owner | Status |
| --- | --- | --- | --- | --- | --- | --- | --- |
| SWU-WCSB-001 | [TASK-WCSB-01](work-pack/tasks/TASK-WCSB-01-RUNNER.md) | implement and fixture-prove one deterministic source-build protocol | Design pass | `.gitignore`, `runtime/**`, Task Session evidence | static checks plus pass/fail fixtures | Task Session local | pass |
| SWU-WCSB-002 | [TASK-WCSB-02](work-pack/tasks/TASK-WCSB-02-EXECUTE.md) | execute protocol and bind one verified local addon | SWU-WCSB-001 pass | `.work/**`, `execution/source-build/**`, Task Session evidence | exact live receipt validator and scope audit | Task Session local | blocked |

## SWU atomicity review

| SWU | Candidate child units | Retained-boundary rationale | Independent acceptance | Verdict |
| --- | --- | --- | --- | --- |
| SWU-WCSB-001 | runner, schema, validator, fixtures | none is safely executable/reviewable without the shared protocol and its positive/negative validator proof | complete protocol can pass without running a native build | pass |
| SWU-WCSB-002 | source fetch, dependency install, `c_src`, compile, load, tests | intermediate stages cannot produce an admissible addon; all are acceptance stages of one artifact identity | terminal source-build receipt passes independently of parent consumption | pass |

The first unit is the narrowest reversible trust-building step: it creates and
tests orchestration code but performs no external fetch, dependency
materialization, native compilation, or addon load.

## Task Session closeout synchronization contract

| SWU | Owner route | Terminal receipt | Exact synchronization targets | Baseline binding | Delta classes | Owner validation | Expected owner receipt | Successor |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| SWU-WCSB-001 | `invoke:refresh:apply-approved` | `execution/task-sessions/SWU-WCSB-001/terminal-receipt.json`; pass/block, exact files, commands, validation and blocker | `plan/WORK-PACK.md`; `plan/work-pack/tasks/TASK-WCSB-01-RUNNER.md`; `plan/work-pack/waves/W0-SOURCE-BUILD.md` | Task Session preflight records live SHA-256 for all present targets | `evidence_added`, `blocker_opened`, `status_changed`, `route_changed` | JSON/schema/static/fixture checks plus target digest comparison | `execution/task-sessions/SWU-WCSB-001/invoke-refresh-receipt.json` | select SWU-WCSB-002 only on pass; none on block |
| SWU-WCSB-002 | `invoke:refresh:apply-approved` | `execution/task-sessions/SWU-WCSB-002/terminal-receipt.json`; pass/block, manifests, addon identity, tests, side effects and blocker | `plan/WORK-PACK.md`; `plan/work-pack/tasks/TASK-WCSB-02-EXECUTE.md`; `plan/work-pack/waves/W0-SOURCE-BUILD.md` | Task Session preflight records live SHA-256 for all targets and passed SWU-WCSB-001 receipt | `evidence_added`, `blocker_opened`, `status_changed`, `route_changed` | terminal receipt validator, scope scan, dependency/attempt check, target digest comparison | `execution/task-sessions/SWU-WCSB-002/invoke-refresh-receipt.json` | no same-pack successor; return parent Invoke Refresh route on pass, none on block |

Closeout authorization is bookkeeping-only. It cannot execute another SWU,
change Craft authority, publish, deploy, clean build state, or silently admit
the addon to the parent plan.

## Validation strategy

| Boundary | Acceptance-critical evidence |
| --- | --- |
| Plan | Dispatch Spec pass, Distill pass, navigable two-SWU contracts, closeout rows |
| Runner | Python syntax/help, JSON schema parse, fixture pass case, each declared negative fixture rejected with stable code |
| Source | exact root commit, clean tracked baseline, recursive gitlinks, complete source manifest |
| Dependencies | exact lockfile hash, `npm ci --ignore-scripts`, integrity-resolved tree, unchanged lockfile |
| Generated source | complete `c_src` manifest after reviewed copy script |
| Toolchain/build | exact live identities, explicit OpenSSL mode, expected addon exists once and hashes |
| Verification | addon loads, upstream tests pass, empty-value canary passes, only temporary stores touched |
| Scope | no Craft, Git-history, registry publication, deployment, or out-of-scope workspace writes |

Every obligation is acceptance-critical. No unavailable or substitute check is
treated as pass.

## Current blockers and risks

No planning blocker remains after explicit source-build authorization.

Execution blocker `WCSB-UPSTREAM-CONCURRENT-WRITE-STALL` is open. The reviewed
source compiled and loaded, but the first upstream WaveDB Integration
concurrent-write case did not complete and the suite was terminated after more
than 16 minutes. The addon is partial evidence only; canary and final scope
audit did not run.

| Risk | Trigger | Behavior |
| --- | --- | --- |
| Node/node-gyp/Python incompatibility | configure or build failure | block exact attempt; do not substitute toolchain |
| OpenSSL/header/link mismatch | build or load failure | block exact attempt; no implicit no-OpenSSL fallback |
| dependency unavailability/integrity failure | `npm ci` failure | block; no alternate package or lock rewrite |
| upstream test failure | any test/canary failure | block addon handoff |
| unexpected filesystem effect | scope audit detects path | block even if tests pass |

## Gate checks

- Define: pass.
- Design: `design-validator-pass`, fixed point, no diagnostics.
- Plan templates: standalone layering, split Work Pack, Execution Pack selected.
- Full Dispatch Spec: required and must validate pass.
- Distill: pass, zero task-shaped SWUs.
- Closeout contracts: complete for both SWUs.
- Selected unit: none after SWU-WCSB-002 blocked.
- Native build: failed attempt preserved; retry requires source-owner diagnosis
  and a newly planned immutable attempt ID.

## Required links

- [Execution Pack](EXECUTION-PACK.md)
- [Implementation Layering](IMPLEMENTATION-LAYERING.md)
- [Architecture](../design/ARCHITECTURE.md)
- [Shared context](work-pack/shared/context.md)
- [Traceability](work-pack/shared/traceability.md)
- [Cross-task gaps](work-pack/shared/cross-task-gaps.md)

## Change log

| Date | Change | Author |
| --- | --- | --- |
| 2026-08-04 | SWU-WCSB-002 blocked in upstream concurrent-write test; cleared selection | Codex Invoke Refresh |
| 2026-08-04 | SWU-WCSB-001 passed; selected exact live-build successor | Codex Invoke Refresh |
| 2026-08-04 | Initial source-build Work Pack; selected runner SWU | Codex Invoke Plan |
