---
module: wavedb-craft-projection-experiment
version: current
status: active
updatedAt: 2026-08-04
docType: work-pack
---

# WORK-PACK: WaveDB Craft Projection Experiment

## Control fields

| Field | Value | Notes |
| --- | --- | --- |
| workPackGateStatus | pass | Authored Plan and selected read-only SWU only; no native mutation admission |
| complexity | high | Native dependency, durable isolated state, failure controls, eight SWUs |
| outputMode | split | Task and wave contracts are separate |
| executionPackRef | `EXECUTION-PACK.md` | Serial execution and stop policy |
| layeringArtifactRef | `IMPLEMENTATION-LAYERING.md` | L0-L3 claim ceiling |
| dispatchTechniqueTrace | `DISPATCH-TECHNIQUE-TRACE.md` | Sequence, owner, validation, rollback, SWU, recomposition |
| distillValidationStatus | pass | Authored-plan coherence only |
| swuAtomicityStatus | pass | Eight independently reviewable units |
| firstUnitNarrownessStatus | pass | Read-only provenance gate before install/build |
| closeoutSyncStatus | pass | Exact closeout rows below |
| activeLayerWindow | L0 | Candidate-local feasibility only |
| lastUpdatedAt | 2026-08-04T18:28:25Z | SWU-WCP-001 terminal BLOCK synchronized |
| readinessProfile | pilot | Candidate evidence profile; no deployment meaning |
| selectedSWU | SWU-WCP-001 | Exactly one selected unit |
| nativeMutationAdmission | block | Requires a passing SWU-WCP-001 provenance receipt |

## Objective summary

- Objective: execute the finite WP-0 through WP-6 WaveDB/Craft projection
  experiment without changing Craft authority or canonical sources.
- Inputs: audited research findings, closed Define, design-validator-pass
  architecture, exact registry/source evidence, synthetic fixture.
- Success: eight passing Task Session receipts and closeout joins; exact positive
  and negative oracles; unchanged YAML; preserved HOLD/KILL residue.
- Stop rule: first blocker or captured-frontier completion.

## Planning mapping

| Research work | Work-Pack unit | Boundary |
| --- | --- | --- |
| WP-0 package/toolchain pin | SWU-WCP-001 | provenance decision before install |
| WP-0 fixture/codec freeze | SWU-WCP-002 | WaveDB-independent constants |
| WP-1 adapter | SWU-WCP-003 | bounded API and manifest-last construction |
| WP-2 normal path | SWU-WCP-004 | exact import, query, derived comparisons, B1 |
| WP-3 iterator visibility | SWU-WCP-005 | old/new complete streams only |
| WP-4 negative controls | SWU-WCP-006 | stable zero-output oracles |
| WP-5 recovery/receipts | SWU-WCP-007 | quarantine and exact sibling rebuild |
| WP-6 closeout | SWU-WCP-008 | honest L0 verdict and next-owner route |

## Captured frontier

`SWU-WCP-001 -> SWU-WCP-002 -> SWU-WCP-003 -> SWU-WCP-004 ->
SWU-WCP-005 -> SWU-WCP-006 -> SWU-WCP-007 -> SWU-WCP-008`

The frontier is finite and ordered. A successor is legal only after the prior
unit and its closeout join pass. No newly discovered work joins this frontier.

## Delivery slices

| Slice | Outcome | Layer | Wave | Dependencies | Validation |
| --- | --- | --- | --- | --- | --- |
| S-WCP-01 | exact admissible inputs | L0 | W0 | none | provenance and fixture receipts |
| S-WCP-02 | verified candidate projection | L0 | W1 | S-WCP-01 | adapter and exact normal-path receipts |
| S-WCP-03 | bounded failure/recovery observations | L0 | W2 | S-WCP-02 | iterator, negative, quarantine/rebuild receipts |
| S-WCP-04 | recomposed experiment verdict | L0 | W3 | S-WCP-03 | acceptance audit and claim-ceiling scan |

## Task status board

| Task | Goal | Layer | Wave | Gate | Status |
| --- | --- | --- | --- | --- | --- |
| [TASK-WCP-01](work-pack/tasks/TASK-WCP-01-INPUT-CLOSURE.md) | close package and fixture identities | L0 | [W0](work-pack/waves/W0-INPUT-CLOSURE.md) | SWU-WCP-001 selected; SWU-WCP-002 dependency-blocked | blocked |
| [TASK-WCP-02](work-pack/tasks/TASK-WCP-02-ADAPTER.md) | construct bounded projection adapter | L0 | [W1](work-pack/waves/W1-CONSTRUCTION.md) | blocked by SWU-WCP-002 | not-started |
| [TASK-WCP-03](work-pack/tasks/TASK-WCP-03-POSITIVE-OBSERVATIONS.md) | exact normal and iterator paths | L0 | W1/W2 | blocked by adapter | not-started |
| [TASK-WCP-04](work-pack/tasks/TASK-WCP-04-NEGATIVE-CONTROLS.md) | execute non-vacuous failure controls | L0 | [W2](work-pack/waves/W2-FAILURE-EVIDENCE.md) | blocked by normal path | not-started |
| [TASK-WCP-05](work-pack/tasks/TASK-WCP-05-RECOVERY.md) | prove quarantine and sibling rebuild | L0 | W2 | blocked by negative controls | not-started |
| [TASK-WCP-06](work-pack/tasks/TASK-WCP-06-CLOSEOUT.md) | audit and close L0 evidence | L0 | [W3](work-pack/waves/W3-CLOSEOUT.md) | blocked by all observations | not-started |

## SWU atomicity review

| SWU | Primary behavior | Independent boundary | Split considered | Retained rationale | Verdict |
| --- | --- | --- | --- | --- | --- |
| SWU-WCP-001 | decide exact package/source provenance | one pass/block receipt before install | registry read vs tarball/source comparison | neither alone answers correspondence | pass |
| SWU-WCP-002 | freeze parser/serializer/fixture/key-value constants | exact immutable fixture manifest | parser freeze vs fixture freeze | constants are mutually digest-bound | pass |
| SWU-WCP-003 | construct bounded adapter | API plus unit tests and YAML guards | build vs query facade | adapter contract must compile as one semantic boundary | pass |
| SWU-WCP-004 | execute exact B0/B1 normal path | complete exact positive-path receipt | import vs query vs render | one generation is useful only when all admission outputs agree | pass |
| SWU-WCP-005 | observe iterator visibility | old/new streams match frozen manifests | old vs new stream | hybrid detection needs both streams | pass |
| SWU-WCP-006 | execute negative controls | every named trigger has stable zero-output oracle | one SWU per control | same immutable harness and no independent adoption value | pass |
| SWU-WCP-007 | quarantine and rebuild | suspect generation never served and sibling exact | quarantine vs rebuild | recovery claim needs both refusal and fresh reconstruction | pass |
| SWU-WCP-008 | recompose and close | every acceptance maps to exact receipt or named residue | audit vs owner handoff | handoff must consume the audited verdict | pass |

## SWU execution handoff

| SWU | Parent | Dependencies | Write scope | Done criteria | Validation | Owner | Status |
| --- | --- | --- | --- | --- | --- | --- | --- |
| SWU-WCP-001 | TASK-WCP-01 | none | `experiment/execution/wp0-provenance/**`, Work Pack closeout fields | exact metadata/tarball/source comparison and pass/block receipt; no install | receipt schema, hashes, source-version comparison, no addon/install artifacts | Task Session local | blocked |
| SWU-WCP-002 | TASK-WCP-01 | 001 pass | `experiment/runtime/fixtures/**`, `execution/wp0-fixture/**` | exact L0/C0/S0/I0/payload manifests and hashes frozen independently | fixture validator twice from clean inputs | Task Session local | blocked |
| SWU-WCP-003 | TASK-WCP-02 | 002 pass | `experiment/runtime/src/**`, tests, isolated package files | bounded API, closed codec, unit tests, no writeback/active pointer | unit tests, YAML guard, key allowlist, native smoke test | Task Session local | blocked |
| SWU-WCP-004 | TASK-WCP-03 | 003 pass | `experiment/execution/runs/<run>/normal/**`, isolated stores | B0/B1 exact bytes/hashes/counts/queries/views | integration command and manifest comparator | Task Session local | blocked |
| SWU-WCP-005 | TASK-WCP-03 | 004 pass | `experiment/execution/runs/<run>/iterator/**`, isolated stores | old/new streams each exact, no hybrid | barrier/event validator and byte comparator | Task Session local | blocked |
| SWU-WCP-006 | TASK-WCP-04 | 005 pass | `experiment/execution/runs/<run>/negative/**`, isolated copies | every named control triggers exact zero-output code and unchanged YAML | negative-control matrix validator | Task Session local | blocked |
| SWU-WCP-007 | TASK-WCP-05 | 006 pass | `experiment/execution/runs/<run>/recovery/**`, isolated sibling stores | quarantine external, suspect never served, sibling exact | recovery validator and complete manifest comparator | Task Session local | blocked |
| SWU-WCP-008 | TASK-WCP-06 | 007 pass | `experiment/execution/CLOSEOUT.md`, receipts, Work Pack status fields | all acceptance rows audited; bounded verdict and next-owner route | closeout checker, boundary scan, source digest audit | Task Session local | blocked |

## Task Session closeout sync contract

The lifecycle owner route for planning/evidence synchronization is
`invoke:refresh:apply-approved`. It may update only the declared Work Pack
status/evidence fields and create the exact owner receipt. It never performs the
next SWU.

| SWU | Terminal source receipt | Target inventory | Baseline | Allowed deltas | Owner validation | Expected owner receipt | Successor |
| --- | --- | --- | --- | --- | --- | --- | --- |
| 001 | `execution/task-sessions/SWU-WCP-001/terminal-receipt.json` | `WORK-PACK.md`, `execution/task-sessions/SWU-WCP-001/**` | pre-session SHA-256 inventory | evidence_added, status_changed, blocker_opened | schema, hash, scope, no-install checks | `execution/task-sessions/SWU-WCP-001/invoke-refresh-receipt.json` | 002 only on pass; none on block |
| 002 | `execution/task-sessions/SWU-WCP-002/terminal-receipt.json` | `WORK-PACK.md`, fixture/evidence paths, session path | pre-session SHA-256 inventory | evidence_added, status_changed, blocker_opened | fixture validator and scope scan | `execution/task-sessions/SWU-WCP-002/invoke-refresh-receipt.json` | 003 only on pass |
| 003 | `execution/task-sessions/SWU-WCP-003/terminal-receipt.json` | `WORK-PACK.md`, runtime source/test/package paths, session path | pre-session SHA-256 inventory | implementation_added, dependency_lock_added, evidence_added, status_changed, blocker_opened | unit/integration tests and YAML guard | `execution/task-sessions/SWU-WCP-003/invoke-refresh-receipt.json` | 004 only on pass |
| 004 | `execution/task-sessions/SWU-WCP-004/terminal-receipt.json` | `WORK-PACK.md`, normal run/store/session paths | pre-session SHA-256 inventory | evidence_added, isolated_store_added, status_changed, blocker_opened | exact comparator and YAML guard | `execution/task-sessions/SWU-WCP-004/invoke-refresh-receipt.json` | 005 only on pass |
| 005 | `execution/task-sessions/SWU-WCP-005/terminal-receipt.json` | `WORK-PACK.md`, iterator run/store/session paths | pre-session SHA-256 inventory | evidence_added, isolated_store_added, status_changed, blocker_opened | event/barrier/stream validation | `execution/task-sessions/SWU-WCP-005/invoke-refresh-receipt.json` | 006 only on pass |
| 006 | `execution/task-sessions/SWU-WCP-006/terminal-receipt.json` | `WORK-PACK.md`, negative run/copy/session paths | pre-session SHA-256 inventory | evidence_added, isolated_copy_added, status_changed, blocker_opened | control matrix and YAML guard | `execution/task-sessions/SWU-WCP-006/invoke-refresh-receipt.json` | 007 only on pass |
| 007 | `execution/task-sessions/SWU-WCP-007/terminal-receipt.json` | `WORK-PACK.md`, recovery/sibling/session paths | pre-session SHA-256 inventory | evidence_added, isolated_store_added, status_changed, blocker_opened | recovery and exact rebuild checks | `execution/task-sessions/SWU-WCP-007/invoke-refresh-receipt.json` | 008 only on pass |
| 008 | `execution/task-sessions/SWU-WCP-008/terminal-receipt.json` | `WORK-PACK.md`, `execution/CLOSEOUT.md`, closeout/session receipts | pre-session SHA-256 inventory | evidence_added, status_changed, route_changed, blocker_opened | acceptance audit and boundary scan | `execution/task-sessions/SWU-WCP-008/invoke-refresh-receipt.json` | none |

## Validation strategy

1. Input validators bind every local source and external package artifact by
   digest before use.
2. Fixture compilation runs twice from clean inputs and must produce identical
   canonical bytes and manifests.
3. Adapter tests cover key encoding, closed manifests, YAML guards, stable
   errors, no active pointer, no writeback, and no receipt key family.
4. Normal/iterator/negative/recovery runs preserve raw events and exact
   comparators.
5. Every run hashes canonical YAML before and after.
6. Final closeout maps each research acceptance item to a terminal receipt and
   keeps every HOLD/KILL item open.

## Current blockers

| ID | Scope | Description | Owner | Next action |
| --- | --- | --- | --- | --- |
| B-WCP-PROV-001 | SWU-WCP-001 and all successors | npm `0.15.8` metadata declares `gitHead=54832130...`, whose source package version is `0.15.7`; reviewed `0.15.8` source is `01c77e8b...` | package/security owner | select a corrected registry artifact/provenance record or explicitly authorize a newly designed source-build route |
| B-WCP-RUNTIME-001 | mutation-ready handoff | reviewed Invoke package has no generic candidate Plan provenance validator or mode-runtime receipt issuer | Task Session owner | independently admit each selected SWU; do not synthesize readiness |

`B-WCP-PROV-001` is expected to make the first Task Session terminal `BLOCK`.
That result preserves the remaining frontier and prohibits native install.

## Deferred residue

See `work-pack/shared/cross-task-gaps.md`. True mid-apply atomicity,
multi-writer operation, power durability, migration/downgrade, encryption
lifecycle, platform support, dependency/license closure, prefix deletion,
in-place repair, canonical replacement, and publication remain outside L0.

## Gate checks

- Design selection: pass.
- Split artifact navigability: pass.
- SWU atomicity: pass.
- First-unit narrowness: pass.
- Closeout contracts: pass.
- Distill authored-plan validation: pass.
- Selected SWU: exactly one.
- SWU-WCP-001 terminal receipt: `execution/task-sessions/SWU-WCP-001/terminal-receipt.json`; `PACKAGE_PROVENANCE_MISMATCH`; no successor.
- Native mutation: blocked pending provenance.
- Experiment completion: not run.

## Change log

| Date | Change | Author |
| --- | --- | --- |
| 2026-08-04 | Initial high-complexity Work Pack and selected provenance SWU | Codex Invoke Plan |
