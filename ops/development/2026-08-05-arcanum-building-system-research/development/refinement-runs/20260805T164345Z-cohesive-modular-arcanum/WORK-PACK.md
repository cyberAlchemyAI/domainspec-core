# Work Pack — Cohesive Modular Arcanum

Work-Pack ID: `WP-ABP-001`  
Status: `blocked-before-selection`  
Plan evidence: `plan-evidence-pending`  
Admission timing: `selected-unit-at-task-session`  
Selected SWU: `none`  
Next owner: `decision-gate:resolve:DECISION-ABP-OWNERS`

## Objective

Incrementally prove and then govern an owner-preserving Arcanum building protocol without replacing current capability authority or claiming runtime/product evidence before it exists.

## Delivery boundary

- L0 and L1 start private-parent-local under the research package.
- Public `arcanum/` paths are unavailable until capability type, lifecycle owner, public-source reconstruction, and exact authorization are established.
- No registry, publication, release, deployment, or production action is part of this Work Pack.

## Execution-entry projection

```yaml
admissionTiming: selected-unit-at-task-session
frontier:
  - TASK-ABP-READINESS
  - TASK-ABP-L0
  - TASK-ABP-L1
  - TASK-ABP-RUNTIME
  - TASK-ABP-SERIES
  - TASK-ABP-VERIFY
  - TASK-ABP-PUBLIC-READINESS
allowedRoutes:
  - decision-gate:resolve:DECISION-ABP-OWNERS
  - task-session:execute:SWU-ABP-001
  - sigil-development:design-or-create:transition-contract
  - spellcraft:update:task-session-until-blocker
allowedRoutesDigest: 8f23f9a55d4fa6a9a564730bff2112ac79fe7fb08fdcf8fda7a771766ed5253c
automaticDecisions:
  - exact internal validator routing
  - declared reversible local fallback
  - one typed same-route retry only for REPAIRABLE_OWNER_CONDITION
  - fresh Task Session resumption under current receipts
stopDecisions:
  - semantic owner choice
  - scope expansion
  - public/private boundary crossing
  - lifecycle, registry, publication, release, deployment, or production effect
  - destructive or irreversible action
  - failed acceptance-critical validation
entryState: blocked
blocker: DECISION-ABP-OWNERS
```

## Blocking decisions

| ID | Question | Recommendation | Required owner evidence |
|---|---|---|---|
| `DECISION-ABP-SERIES` | Who owns ordered frontier/visited/retry/join/stop state? | Implementation Readiness; Task Session Until Blocker becomes stateless profile/facade. | Decision Gate plus affected lifecycle-owner acceptance |
| `DECISION-ABP-PROTOCOL` | What capability class and non-authoritative steward owns OBTC schemas? | candidate Formulae/sigil package with owner-local version acceptance | Decision Gate then Sigil Development or selected lifecycle owner |
| `DECISION-ABP-PRODUCER` | Which exact capability produces material packages? | no default; bind an existing owner or design a separate producer capability | owner decision plus real producer receipt contract |
| `DECISION-ABP-REGISTRY` | Which owner releases registry entries? | keep release unavailable until bound | registry-owner decision/receipt |
| `DECISION-ABP-EVENTS` | Where are causal projections persisted? | reuse an existing local observability/runtime event owner where possible | local owner declaration; no mandatory global store |

Producer and registry decisions may remain deferred for L0 because L0 performs no product mutation or release. Series and protocol ownership must resolve before public/runtime consolidation.

## Task board

| Task | Layer | Contract | State | Depends on |
|---|---|---|---|---|
| `TASK-ABP-READINESS` | pre-L0 | `work-pack/tasks/TASK-ABP-READINESS.md` | blocked decision gate | none |
| `TASK-ABP-L0` | L0 | `work-pack/tasks/TASK-ABP-L0.md` | waiting | admitted protocol route |
| `TASK-ABP-L1` | L1 | `work-pack/tasks/TASK-ABP-L1.md` | waiting | L0 pass |
| `TASK-ABP-RUNTIME` | L2 | `work-pack/tasks/TASK-ABP-RUNTIME.md` | waiting | L1 and current canonical identity |
| `TASK-ABP-SERIES` | L2 | `work-pack/tasks/TASK-ABP-SERIES.md` | blocked owner decision | series Decision Gate and L1 |
| `TASK-ABP-VERIFY` | L2 | `work-pack/tasks/TASK-ABP-VERIFY.md` | waiting | runtime, series, producer, real owner availability |
| `TASK-ABP-PUBLIC-READINESS` | L3 | `work-pack/tasks/TASK-ABP-PUBLIC-READINESS.md` | blocked lifecycle/public gate | all prior proof plus lifecycle authorization |

## SWU manifest

| SWU | Parent | Primary behavior | Acceptance boundary | Write scope |
|---|---|---|---|---|
| `SWU-ABP-001` | L0 | project WPRA selection into non-authoritative OBTC | exact field map and native handle/digest preserved | `ops/development/2026-08-05-arcanum-building-system-research/prototype/build-protocol/adapters/wpra-task-session/` |
| `SWU-ABP-002` | L0 | validate OBTC structure without semantic decisions | stable diagnostics; forbidden calls absent | `ops/development/2026-08-05-arcanum-building-system-research/prototype/build-protocol/protocol/` |
| `SWU-ABP-003` | L0 | shadow-compare current native fixtures | field/diagnostic preservation passes; any semantic-preservation claim also requires a Task Session owner-native shadow acceptance receipt; native bytes unchanged | `ops/development/2026-08-05-arcanum-building-system-research/prototype/build-protocol/fixtures/l0/` |
| `SWU-ABP-004` | L1 | project Task Session closeout into Refresh input | pre-state and expected owner receipt preserved | `ops/development/2026-08-05-arcanum-building-system-research/prototype/build-protocol/adapters/task-session-refresh/` |
| `SWU-ABP-005` | L1 | classify/reconcile outcome-unknown | no automatic retry; three reconciliation results | `ops/development/2026-08-05-arcanum-building-system-research/prototype/build-protocol/reconciliation/` |
| `SWU-ABP-006` | L1 | project non-authoritative causal events | fixture-only ephemeral emission unless `DECISION-ABP-EVENTS` binds an admitted local persistence owner; no ownerless durable journal | `ops/development/2026-08-05-arcanum-building-system-research/prototype/build-protocol/events/` |
| `SWU-ABP-007` | L1 | test crash and baseline conflict behavior | declared first stops and forbidden effects | `ops/development/2026-08-05-arcanum-building-system-research/prototype/build-protocol/fixtures/failure/` |
| `SWU-ABP-008` | L1 | test version/privacy/one-writer migration | unsafe cases fail closed | `ops/development/2026-08-05-arcanum-building-system-research/prototype/build-protocol/fixtures/compatibility/` |
| `SWU-ABP-009` | Runtime | restrict reduction to exact receipt manifest | unrelated JSON cannot affect wave | `arcanum/runtime/orchestrate/` |
| `SWU-ABP-010` | Runtime | allocate run-global action IDs pre-spawn | no cross-wave collision | `arcanum/runtime/orchestrate/` |
| `SWU-ABP-011` | Runtime | prove canonical/generated package parity | byte and behavior matrix closes or blocks | unavailable until exact package contract |
| `SWU-ABP-012` | Series | add until-real-blocker profile to selected owner | one frontier/retry/join/stop state machine | selected owner package after Decision Gate |
| `SWU-ABP-013` | Series | convert Task Session Until Blocker to stateless facade | no independent chain state/reducer writes | `arcanum/spells/task-session-until-blocker/` |
| `SWU-ABP-014` | Series | replay legacy chain fixtures against canonical owner | parity or named incompatibility | selected fixture roots after owner plan |
| `SWU-ABP-015` | Verify | execute real Invoke-to-Refresh owner-chain witness | real join, synchronized result, cursor | unavailable until exact safe target |
| `SWU-ABP-016` | Public | reconstruct public candidate and scan payloads | zero private paths/prose/payload fields | unavailable until lifecycle decision |
| `SWU-ABP-017` | Public | sync generated package and prove parity | exact package and behavior receipt | unavailable until lifecycle decision |

No SWU is selected. Unavailable paths remain blocked rather than represented by placeholder globs.

## Shared Task Session closeout contract

Every mutation-capable SWU must instantiate these fields before admission:

```yaml
terminalSourceReceipt: task-session execution-terminal receipt for exact SWU/attempt
synchronizationTargets:
  - WORK-PACK.md
  - exact parent task contract
  - evidence-index.json
baselineBinding: exact pre-attempt sha256 for every synchronization target
admittedDeltaClasses:
  - evidence_added
  - blocker_opened
  - blocker_resolved
  - status_changed
  - route_changed
ownerValidation: invoke refresh apply-approved over exact inventory
expectedOwnerReceipt: separate current Refresh owner receipt or validated no-op
successorPolicy: exact unique dependency-ready SWU, otherwise none
onFailure: preserve execution terminal; block synchronized completion and successor
```

Task Session revalidates live baselines before product mutation and again before closeout.

## Validation strategy

- Schema validation for every new record.
- Current owner fixture suites unchanged before adapters.
- Positive and one-fault negative protocol fixtures.
- Forbidden-operation tests for the structural validator.
- Crash-after-effect and concurrent-baseline tests.
- Version downgrade/unknown-field/rollback/one-writer tests.
- Public payload allowlist and private-marker scan.
- Separate Orchestrate regressions for exact receipt set and run-global IDs.
- Generated byte plus behavioral parity.
- One later real owner-chain witness; synthetic fixtures cannot substitute.
- Scoped `git diff --check`.

## Current blockers

All residue from `findings.md` remains, plus protocol stewardship, crash/replay, compatibility, and payload privacy. The current approval covers Refine only and does not approve any SWU execution.
