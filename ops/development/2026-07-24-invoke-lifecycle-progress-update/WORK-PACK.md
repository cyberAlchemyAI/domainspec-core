# WORK-PACK: Invoke Lifecycle Progress Protocol

## Control fields

| Field | Value |
| --- | --- |
| phaseStatus | `pass`; Define, Design, and Plan artifacts are complete |
| workPackGateStatus | `block`; mutation execution is gated by `ILP-G01` |
| handoffStatus | `gated`; next route is Spellcraft design/authority ratification |
| authoredPlanValidity | `pass` |
| mutationHandoffReadiness | `blocked` |
| complexity | `high` |
| outputMode | `split` |
| executionPackRef | `EXECUTION-PACK.md` |
| layeringArtifactRef | `IMPLEMENTATION-LAYERING.md` |
| dispatchTechniqueTrace | `DISPATCH-TECHNIQUE-TRACE.md` |
| dispatchValidation | `dispatch-validation.json` must be `pass` |
| distillValidationStatus | `pass` |
| swuAtomicityStatus | `pass`; task-shaped count 0 |
| firstUnitNarrownessStatus | `pass` |
| activeLayerWindow | `L0` |
| selectedSWU | `SWU-ILP-001` |
| selectedExecutionMode | `lifecycle-decision`; non-mutating |
| selectedExecutionEpoch | none; epoch issuance is not authorized before `ILP-G01` closes |
| lastUpdatedAt | `2026-07-24` |

## Objective

Implement a generic selected-unit lifecycle protocol that prevents Plan from
routing Task Session before compatible admission material exists, separates
exact drift from semantic invalidation, and makes progress depend on admitted
append-only transitions rather than run activity.

Success requires ILP-R01 through ILP-R10 to close through lifecycle-owner
receipts and a generic live proof. A complete work-pack does not make the
mutation handoff ready.

## Delivery slices

| Slice | Outcome | Layer | Wave | Dependencies | Validation |
| --- | --- | --- | --- | --- | --- |
| S0 | one legitimate transition owner and source boundary are ratified | L0 | [W0](work-pack/waves/W0.md) | none | decision artifact answers every ILP-G01 acceptance question |
| S1 | deterministic epoch, transition, and readiness contracts reject false-ready and in-place-repair states | L1 | [W1](work-pack/waves/W1.md) | S0 | schema plus causal red/green fixtures |
| S2 | Plan, Refresh, and Task Session exchange owner-bound receipts without authority collapse | L2 | [W2](work-pack/waves/W2.md) | S1 | focused capability suites, generated parity, stale/mismatch checks |
| S3 | legacy admission, observational progress, live proof, and recomposition close | L3 | [W3](work-pack/waves/W3.md) | S2 | legacy controls, churn fixture, live run, privacy scan, terminal audit |

## Task board

| Task | Outcome | Layer | Wave | Lifecycle owner | Gate | Status |
| --- | --- | --- | --- | --- | --- | --- |
| [TASK-ILP-001](work-pack/tasks/TASK-ILP-001-AUTHORITY-DECISION.md) | ratify transition owner and source placement | L0 | W0 | Spellcraft + Arcanum governance | design decision receipt | selected, gated |
| [TASK-ILP-002](work-pack/tasks/TASK-ILP-002-EPOCH-CONTRACT.md) | validate immutable epoch and declared control graph | L1 | W1 | Spellcraft | SWU-ILP-001 receipt | pending |
| [TASK-ILP-003](work-pack/tasks/TASK-ILP-003-TRANSITION-VALIDATOR.md) | validate append-only edges, supersession, and churn | L1 | W1 | ratified transition owner + Spellcraft | SWU-ILP-002 receipt | pending |
| [TASK-ILP-004](work-pack/tasks/TASK-ILP-004-MODE-READINESS.md) | validate local/external/delegated/reusable producer roles and readiness | L1 | W1 | Spellcraft + Sigil Development | SWU-ILP-002/003 receipts | pending |
| [TASK-ILP-005](work-pack/tasks/TASK-ILP-005-PLAN-INTEGRATION.md) | make Plan emit separate epoch/readiness artifacts and gate routes | L2 | W2 | Spellcraft | W1 receipts | pending |
| [TASK-ILP-006](work-pack/tasks/TASK-ILP-006-REFRESH-AND-DRIFT.md) | classify drift independently and enforce one Refresh transition kind | L2 | W2 | Spellcraft | SWU-ILP-003/005 receipts | pending |
| [TASK-ILP-007](work-pack/tasks/TASK-ILP-007-TASK-SESSION-CONSUMPTION.md) | consume ready epoch while preserving live pre-write admission | L2 | W2 | Sigil Development | SWU-ILP-004/005 receipts | pending |
| [TASK-ILP-008](work-pack/tasks/TASK-ILP-008-LEGACY-AND-PROGRESS.md) | re-admit legacy plans and project progress/churn without authority | L3 | W3 | Spellcraft + Workflow Reflect | W2 receipts | pending |
| [TASK-ILP-009](work-pack/tasks/TASK-ILP-009-LIVE-PROOF.md) | prove repaired topology in a generic live run | L3 | W3 | bounded Task Session + lifecycle owners | SWU-ILP-008A/008B receipts | pending |
| [TASK-ILP-VERIFY](work-pack/tasks/TASK-ILP-VERIFY.md) | recompose ILP-R01..R10 and assess promotion readiness | L3 | W3 | Spellcraft + Sigil Development + transition owner | all implementation receipts | pending |

## Shared SWU manifest

Machine view: [work-pack/swu-manifest.json](work-pack/swu-manifest.json).

| SWU | Parent | Primary behavior/decision | Independent acceptance boundary | State |
| --- | --- | --- | --- | --- |
| SWU-ILP-001 | TASK-ILP-001 | choose transition-admission owner and public source placement | one decision receipt names owner, paths, writer exclusions, and promotion boundary | selected, gated |
| SWU-ILP-002 | TASK-ILP-002 | accept or reject one immutable epoch candidate against its declared control graph | incomplete graph or changed control field cannot produce an issuance receipt | pending |
| SWU-ILP-003 | TASK-ILP-003 | admit only one allowed monotonic transition | unlisted edges, unchanged churn, and in-place control repair deterministically reject | pending |
| SWU-ILP-004 | TASK-ILP-004 | compute one mode-compatible handoff-readiness verdict | missing/incompatible/self-validating roles cannot produce `ready`; valid local and packaged modes can | pending |
| SWU-ILP-005 | TASK-ILP-005 | make Plan route only a ready epoch while preserving authored validity | authored-pass plus gated/blocked readiness never routes Task Session | pending |
| SWU-ILP-006A | TASK-ILP-006 | classify changed paths independently of the projection writer | controlling, projection-only, unrelated, unclassified, and writer-conflict fixtures are causal | pending |
| SWU-ILP-006B | TASK-ILP-006 | enforce one Refresh transition kind and postcondition | mixed kinds and target implementation reject; projection synchronization admits no lifecycle edge | pending |
| SWU-ILP-007 | TASK-ILP-007 | bind Task Session admission to one ready epoch without weakening live checks | absent/stale/mismatched epoch evidence blocks before write; current evidence still undergoes live admission | pending |
| SWU-ILP-008A | TASK-ILP-008 | make every legacy plan freshly revalidate instead of inheriting readiness | legacy plan without a current epoch remains `legacy_unadmitted`; successful migration creates new evidence only | pending |
| SWU-ILP-008B | TASK-ILP-008 | project admitted progress and repeated churn as non-authoritative telemetry | counts derive from admitted transition IDs; unchanged churn never increments progress | pending |
| SWU-ILP-009 | TASK-ILP-009 | demonstrate one live selected unit reaches admission without repair Refresh | live receipt chain crosses ready/admitted and exact drift still blocks an obsolete join | pending |

## Atomicity review

| SWU | Candidate child units | Retained-boundary rationale | Verdict |
| --- | --- | --- | --- |
| 001 | choose owner; choose paths; declare exclusions | all fields form one authority decision; a partial answer cannot authorize source work | pass |
| 002 | schema; graph traversal; canonical digest; fixtures | none has an acceptance meaning without one epoch-issuance verdict | pass |
| 003 | edge table; successor rule; churn rejection | conjuncts of one transition-admission decision | pass |
| 004 | local contract; packaged-mode adapter; role separation; readiness | rows of one mode-dispatched readiness function and one verdict | pass |
| 005 | Plan fields; route gate; output fixtures | one Plan handoff-decision behavior | pass |
| 006A | path intersection; identity conflict; verdict | conjuncts of one change-impact classification | pass |
| 006B | kind enum; postconditions; target-implementation prohibition | one Refresh request-admission behavior | pass |
| 007 | ready receipt check; live admission; receipt binding | conjuncts of one Task Session mutation-admission decision | pass |
| 008A | legacy marker; revalidation; new epoch | one migration/admission behavior; no historical evidence rewrite | pass |
| 008B | progress denominator; churn key; event fields | one observational projection behavior | pass |
| 009 | live happy path; exact-drift negative control | one topology proof requires both progress and retained safety | pass |

Task-shaped SWU count: 0.

## Validation strategy

| Layer | Required evidence |
| --- | --- |
| L0 | owner decision, authority exclusions, exact source placement, public/private review |
| L1 | JSON Schema checks, deterministic validators, all research negative fixtures, valid local and packaged positive controls |
| L2 | Plan authored/readiness matrix, Refresh kind matrix, drift classifier matrix, Task Session absent/stale/mismatch/current matrix, generated parity |
| L3 | legacy no-inference fixture, transition-derived progress/churn fixture, generic live receipt chain, exact drift block, privacy scan, full regression |

## Blockers and gaps

See [GAPS.md](GAPS.md).

`ILP-G01` blocks all canonical mutation. `ILP-G02` through `ILP-G06` are owned by
planned SWUs. `ILP-G07` is rechecked per task and never authorizes absorbing
unrelated changes.

## Gate checks

1. Define and Design are complete: pass.
2. Dispatch Spec route validation: must pass in `dispatch-validation.json`.
3. Distill plan validation: pass.
4. Every non-exempt task has implementation detail and one or more atomic SWUs.
5. Every mutation SWU uses the shared predeclared closeout contract.
6. The first unit is non-mutating and narrow: pass.
7. No execution epoch exists yet; no Task Session mutation route is selected.
8. Canonical mutation remains blocked until `ILP-G01` closes and the applicable
   predecessor receipts exist.

## Current handoff

Next owner: Spellcraft, `design`/lifecycle assessment for `SWU-ILP-001`.

Expected result: one decision receipt that either:

- names the transition-admission owner and exact public source placement,
  allowing `SWU-ILP-002` to be selected; or
- blocks with one precise authority question and route.

No canonical edit is authorized by this handoff.

