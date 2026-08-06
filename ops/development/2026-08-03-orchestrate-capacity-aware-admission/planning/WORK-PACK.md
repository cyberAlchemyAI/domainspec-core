---
module: orchestrate-capacity-aware-admission
version: candidate-v0
status: authored-plan
updatedAt: 2026-08-03
docType: work-pack
---

# WORK-PACK: Orchestrate Capacity-Aware Admission

## Control fields

| Field | Value | Notes |
| --- | --- | --- |
| workPackGateStatus | pass | Authoring gate only; Task Session must independently preflight the selected SWU. |
| complexity | high | Strict schema evolution, host boundary, canonical/generated surfaces, and deferred host gates. |
| outputMode | split | Task and wave files are required. |
| executionPackRef | [EXECUTION-PACK.md](EXECUTION-PACK.md) | Cross-task choreography. |
| layeringArtifactRef | [IMPLEMENTATION-LAYERING.md](IMPLEMENTATION-LAYERING.md) | L0-L3 decisions. |
| dispatchTechniqueTrace | [PLAN-TECHNIQUE-TRACE.md](PLAN-TECHNIQUE-TRACE.md) | Required technique binding. |
| distillValidationStatus | pass | Four bounded rounds; see [PLAN-DISTILL.md](PLAN-DISTILL.md). |
| swuAtomicityStatus | pass | Five SWUs; task-shaped count 0. |
| firstUnitNarrownessStatus | pass | `SWU-OCA-001` is the snapshot-only reversible trust-building seam. |
| closeoutSyncStatus | pass | Every mutation SWU has exact lifecycle-changing planning targets. |
| activeLayerWindow | L0 | L1 waits for L0 receipts. |
| lastUpdatedAt | 2026-08-03T20:04:14Z | Final Distill close timestamp. |
| readinessProfile | pilot | No release or production claim. |

## Objective summary

- Objective: prevent predictable partial native waves through whole-wave
  capacity admission, repair the no-agent failure evidence branch, bind honest
  Codex degraded behavior, and regenerate supported Orchestrate surfaces.
- Primary inputs: Design result digest
  `f1ac2c8335335691d4d0087696ca593a22cd2ddbb1e40c6edd60d8a53cd2a336`,
  canonical Orchestrate source, incident trace, and host profile.
- Success condition: all five SWUs and the read-only verification task pass
  current exact tests; a capacity block emits no actions/spawns; a late failed
  spawn validates causally; generated support paths match canonical bytes.

## Delivery slices

| Slice | Outcome | Layer | Wave | Dependencies | Validation |
| --- | --- | --- | --- | --- | --- |
| S-001 | whole-wave admission seam | L0 | [W1](work-pack/waves/W1-L0-ADMISSION.md) | W0 | capacity fixture matrix and preflight regression |
| S-002 | valid pre-agent failure branch | L0 | [W2](work-pack/waves/W2-L0-FAILURE-EVIDENCE.md) | S-001 | canonical causal validator plus partial-wave tests |
| S-003 | honest Codex provider ceiling | L1 | [W3](work-pack/waves/W3-L1-CODEX-PROVIDER.md) | S-001, S-002 | provider matrix; no inferred limit |
| S-004 | owner-safe route alternatives | L1 | [W4](work-pack/waves/W4-L1-ROUTE-OPTIONS.md) | S-003 | topology/approval fixture matrix |
| S-005 | generated projection parity | L1 | [W5](work-pack/waves/W5-L1-GENERATED-PARITY.md) | S-001..S-004 | bootstrap generation parity |
| S-006 | integrated read-only verification | L2 boundary | [W6](work-pack/waves/W6-VERIFY.md) | S-001..S-005 | exact full test list, boundary scan, diff check |

## Task status board

| Task | Goal | Layer | Complexity | Wave | Gate | Status |
| --- | --- | --- | --- | --- | --- | --- |
| [TASK-OCA-01](work-pack/tasks/TASK-OCA-01-ADMISSION-SEAM.md) | add whole-wave admission seam | L0 | high | W1 | ready-first | not-started |
| [TASK-OCA-02](work-pack/tasks/TASK-OCA-02-FAILURE-EVIDENCE.md) | repair failed-spawn causal evidence | L0 | high | W2 | after OCA-001 | not-started |
| [TASK-OCA-03](work-pack/tasks/TASK-OCA-03-CODEX-PROVIDER.md) | bind Codex evidence ceiling | L1 | high | W3 | after L0 | not-started |
| [TASK-OCA-04](work-pack/tasks/TASK-OCA-04-ROUTE-OPTIONS.md) | project safe route alternatives | L1 | medium | W4 | after provider result | not-started |
| [TASK-OCA-05](work-pack/tasks/TASK-OCA-05-GENERATED-PARITY.md) | regenerate exact supported projections | L1 | medium | W5 | after canonical changes | not-started |
| [TASK-OCA-VERIFY](work-pack/tasks/TASK-OCA-VERIFY.md) | independently verify recomposition and boundaries | L2 boundary | high | W6 | after all SWUs | not-started |

## SWU manifest summary

| SWU | Parent | Primary behavior | Independent acceptance | Owner | Status |
| --- | --- | --- | --- | --- | --- |
| `SWU-OCA-001` | TASK-OCA-01 | a complete wave is admitted or blocked before actions | missing/stale/insufficient/unknown produce zero actions; sufficient emits exact full plan | subagent or local fallback | selected; mutation not authorized |
| `SWU-OCA-002` | TASK-OCA-02 | a failed spawn without agent ID closes causally as block | canonical event/receipt/validator accept the branch and never gate-pass it | subagent or local fallback | ready-after-001 |
| `SWU-OCA-003` | TASK-OCA-03 | Codex profile returns authoritative evidence or honest unknown/advisory | inventory alone cannot produce numeric capacity or release | subagent or local fallback | ready-after-002 |
| `SWU-OCA-004` | TASK-OCA-04 | a block yields feasible offers without route mutation | option fixtures preserve validation and confirmation requirements | subagent or local fallback | ready-after-003 |
| `SWU-OCA-005` | TASK-OCA-05 | generated surfaces reproduce canonical contract/support bytes | all three generated packages pass manifest parity | local fallback | ready-after-004 |

Full machine contract: [SWU-MANIFEST.json](SWU-MANIFEST.json).

## SWU atomicity review

| SWU | Candidate child units | Retained-boundary rationale | Verdict |
| --- | --- | --- | --- |
| OCA-001 | input schema; output schema; evaluator; preflight wiring | none is executable or independently proves zero-action whole-wave behavior without the others | pass |
| OCA-002 | receipt conditional; event kind; validator branch | splitting would leave a schema-valid but causally invalid branch or the inverse | pass |
| OCA-003 | host profile prose; provider result; preflight mapping | one behavior is the Codex evidence ceiling; profile and fixtures jointly define it | pass |
| OCA-004 | option schema; feasibility rules; approval flags | an option without both feasibility and approval semantics is unsafe and not independently useful | pass |
| OCA-005 | Codex, local, Claude package regeneration | one projection-parity behavior across the manifest-declared supported set | pass |

## First-unit narrowness

`SWU-OCA-001` is narrower than “fix capacity management.” It accepts a frozen
fixture input and changes only the pre-action snapshot decision seam. It does
not obtain live capacity, verify or reserve slots, emit route handles, change
native spawn/join, project user UI, or regenerate consumers. Reservation-required
inputs block as unsupported. It is reversible through new versioned contracts
and isolated tests.

## Task Session closeout sync contract

Shared exact rows: [CLOSEOUT-SYNC-INVENTORY.json](CLOSEOUT-SYNC-INVENTORY.json).

| SWU | Lifecycle owner | Terminal source receipt | Declared target inventory | Baseline | Allowed deltas | Owner validation | Expected owner receipt | Successor |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| OCA-001 | `invoke:refresh:apply-approved` | Task Session receipt + capacity fixture result | OCA-001 row in shared inventory | target digests + Arcanum HEAD captured before mutation | evidence/status/blocker/route only | OCA-001 tests, JSON schemas, diff check | `work-pack/session-evidence/SWU-OCA-001/<attempt-id>/refresh-receipt.json` | OCA-002 iff pass |
| OCA-002 | same | Task Session receipt + causal validator result | OCA-002 row | same rule | same classes | OCA-002 and regression tests | `work-pack/session-evidence/SWU-OCA-002/<attempt-id>/refresh-receipt.json` | OCA-003 iff L0 pass |
| OCA-003 | same | Task Session receipt + provider matrix | OCA-003 row | same rule | same classes | provider/preflight/regression tests | `work-pack/session-evidence/SWU-OCA-003/<attempt-id>/refresh-receipt.json` | OCA-004 iff pass or declared conservative block |
| OCA-004 | same | Task Session receipt + option matrix | OCA-004 row | same rule | same classes | option and dispatch validation | `work-pack/session-evidence/SWU-OCA-004/<attempt-id>/refresh-receipt.json` | OCA-005 iff pass |
| OCA-005 | same | Task Session receipt + parity matrix | OCA-005 row | canonical and generated tree digests captured before mutation | same classes | bootstrap parity and protected-tree scan | `work-pack/session-evidence/SWU-OCA-005/<attempt-id>/refresh-receipt.json` | TASK-OCA-VERIFY iff pass |

Closeout never infers a target, admits another SWU, commits, pushes, publishes,
or changes authority. A source failure keeps the current SWU selected or opens
a blocker; it does not auto-select its successor.

## Blockers and gaps

| ID | Class | Description | Owner | Effect | Repair path |
| --- | --- | --- | --- | --- | --- |
| G-OCA-001 | deferred host gate | no authoritative Codex total-capacity provider is currently evidenced | native host owner | L1 may return honest unknown; blocks “capacity known” claim | admit a provider contract and fixtures |
| G-OCA-002 | deferred host gate | no atomic reservation/lease operation exists | native host owner | blocks race-free multi-slot claim and L2 | add host lease contract through separate design/plan |
| G-OCA-003 | deferred host gate | logical close does not prove physical release or safe reuse | native host owner | blocks release/reuse optimization and L2 | add physical lifecycle evidence contract |
| G-OCA-004 | generated workflow gap | selective skill sync does not directly address Orchestrate runtime package | Arcanum generation owner | requires temp generation plus exact-package sync in OCA-005 | validate package-only sync and parity |

These gaps do not block OCA-001 or OCA-002. They block only the claims and
layers named above.

## Validation and handoff

- Validation strategy: [VALIDATION-STRATEGY.md](VALIDATION-STRATEGY.md)
- Mutation admission contract: [MUTATION-ADMISSION-CONTRACT.json](MUTATION-ADMISSION-CONTRACT.json)
- Selected SWU: `SWU-OCA-001`
- Mutation authorized: false
- Next owner: Task Session preflight for exactly `SWU-OCA-001`, after an
  execution-time Context Builder pack and material binding are created
