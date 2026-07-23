# WORK-PACK: Whisper Editorial Gate Hardening

## Control fields

| Field | Value |
| --- | --- |
| workPackGateStatus | `pass` |
| complexity | `high` |
| outputMode | `split` |
| executionPackRef | `EXECUTION-PACK.md` |
| layeringArtifactRef | `IMPLEMENTATION-LAYERING.md` |
| dispatchTechniqueTrace | `DISPATCH-TECHNIQUE-TRACE.md` |
| distillValidationStatus | `pass` |
| swuAtomicityStatus | `pass`, task-shaped count 0 |
| firstUnitNarrownessStatus | `pass` |
| activeLayerWindow | `L1` |
| readinessProfile | `release-candidate` for generic gates; transport remains candidate |
| lastUpdatedAt | `2026-07-22` |

## Objective

Revise Whisper so its runtime cannot convert structural success into editorial readiness, transfer approval across different surfaces, continue full derivative generation after volatile corrections, or lose repository-local presets during canonical regeneration.

Success requires causal red/green evidence for the typed receipt, admission evaluators, surface binding, correction replay, packaging boundary, and private integration witness. It does not require transport promotion.

## Delivery slices

| Slice | Outcome | Layer | Wave | Dependencies | Validation |
| --- | --- | --- | --- | --- | --- |
| S0 | False-positive shapes become executable fixtures and a typed final-status ceiling. | L0 | [W0](work-pack/waves/W0.md) | none | schema parse; red/green evaluator results |
| S1 | Exact-surface approval and volatile intent govern full generation. | L1 | [W1](work-pack/waves/W1.md) | S0 | digest substitution and volatile-generation controls |
| S2 | Applied-output corrections invalidate readiness and emit separate evidence. | L2 | [W2](work-pack/waves/W2.md) | S1 | correction replay and observability checks |
| S3 | Canonical, generated, and local packages remain distinct and full regimes pass. | L3 | [W3](work-pack/waves/W3.md) | S2 | public/private sweep, drift validation, full experiment report |

## Task board

| Task | Goal | Layer | Wave | Gate | Status |
| --- | --- | --- | --- | --- | --- |
| [TASK-WEG-001](work-pack/tasks/TASK-WEG-001-FIXTURE-BASELINE.md) | Freeze generic failure and control fixtures. | L0 | W0 | completed | completed |
| [TASK-WEG-002](work-pack/tasks/TASK-WEG-002-RECEIPT-SCHEMA.md) | Define and validate the run-receipt envelope. | L0 | W0 | completed | completed |
| [TASK-WEG-003](work-pack/tasks/TASK-WEG-003-STATUS-CEILING.md) | Compute final status without cross-axis substitution. | L0 | W0 | completed | completed |
| [TASK-WEG-004](work-pack/tasks/TASK-WEG-004-DIGEST-BINDING.md) | Bind human evidence to the exact surface. | L1 | W1 | selected | not-started |
| [TASK-WEG-005](work-pack/tasks/TASK-WEG-005-GENERATION-ADMISSION.md) | Block disallowed full derivative generation. | L1 | W1 | after 004 | not-started |
| [TASK-WEG-006](work-pack/tasks/TASK-WEG-006-FIRST-SURFACE.md) | Add candidate technical-explainer and first-surface contract. | L1 | W1 | after 003,004 | not-started |
| [TASK-WEG-007](work-pack/tasks/TASK-WEG-007-SURFACE-DELTA.md) | Make retell and added blocks accountable. | L1 | W1 | after 006 | not-started |
| [TASK-WEG-008](work-pack/tasks/TASK-WEG-008-CORRECTION-REPLAY.md) | Invalidate false-positive readiness and route observation. | L2 | W2 | after 003,005 | not-started |
| [TASK-WEG-009](work-pack/tasks/TASK-WEG-009-LOCAL-PRESET.md) | Externalize the local preset and regenerate safely. | L3 | W3 | after 006,008 | not-started |
| [TASK-WEG-VERIFY](work-pack/tasks/TASK-WEG-VERIFY.md) | Run full regimes and issue Spellcraft validation receipt. | L3 | W3 | all prior tasks | ready-after-implementation | not-started |

## Shared SWU manifest

The machine-readable manifest is [work-pack/swu-manifest.json](work-pack/swu-manifest.json). Every non-exempt task has one SWU and therefore one independently reviewable boundary. The verification task uses the allowed `VERIFY` closure exemption.

| SWU | Parent | Primary behavior | Acceptance boundary | Owner | State |
| --- | --- | --- | --- | --- | --- |
| SWU-WEG-001 | TASK-WEG-001 | Fixture corpus records expected outcomes without behavior changes. | Generic fixtures parse, include red/green controls, and leak no private text. | local-fallback | completed |
| SWU-WEG-002 | TASK-WEG-002 | Receipt schema rejects incomplete or cross-axis evidence envelopes. | Schema fixture suite passes independently of evaluator policy. | local-fallback | completed |
| SWU-WEG-003 | TASK-WEG-003 | Final status is capped by applicable evidence. | Evaluator table tests return exact ceiling reasons. | local-fallback | completed |
| SWU-WEG-004 | TASK-WEG-004 | Human evidence is valid only for matching digests and approval kind. | Substitution and ambient-approval fixtures fail. | local-fallback | selected |
| SWU-WEG-005 | TASK-WEG-005 | Full generation is blocked by volatile/unapproved/unaccounted state. | Admission fixtures return exact allow/block decisions. | local-fallback | ready-after-004 |
| SWU-WEG-006 | TASK-WEG-006 | A newcomer technical explainer declares a role-complete first surface. | Profile and manifest fixtures validate; transport remains candidate. | local-fallback | ready-after-003,004 |
| SWU-WEG-007 | TASK-WEG-007 | Audience additions have replacement/distinct-job accounting. | Unowned block and rendered-retell negative controls fail. | local-fallback | ready-after-006 |
| SWU-WEG-008 | TASK-WEG-008 | Corrections append, invalidate prior readiness, and update state/routing. | Replay test preserves old receipt and changes current pointer/state. | local-fallback | ready-after-003,005 |
| SWU-WEG-009 | TASK-WEG-009 | Local preset survives canonical native regeneration outside the generated body. | Drift and preset resolution tests pass with no private public diff. | local-fallback | ready-after-006,008 |

## Atomicity review

| SWU | Candidate child units considered | Why the retained unit is smallest coherent | Verdict |
| --- | --- | --- | --- |
| 001 | red fixtures; green fixtures; baseline note | A causal fixture regime needs both controls and one baseline interpretation to be reviewable. | pass |
| 002 | schema files; schema tests | A schema without its parse/negative fixtures has no acceptance closure. | pass |
| 003 | candidate ceiling; comprehension ceiling; post-apply ceiling | These are rows in one pure status function; each is independently table-tested within the same behavior. | pass |
| 004 | artifact binding; surface binding; approval-kind binding | All are conjuncts of one evidence-admissibility decision; splitting creates unusable partial approval. | pass |
| 005 | volatile gate; approval gate; change-manifest gate | All decide one output: full-derivative permission. | pass |
| 006 | profile; role set; manifest example | A transport first-surface contract is unusable if any of these is absent; no renderer behavior is included. | pass |
| 007 | retell default; added-block accounting | Both are one rendered-surface ownership policy and share one negative control family. | pass |
| 008 | append event; invalidate pointer; state/route update | These are one atomic correction transaction; partial application would leave contradictory current state. | pass |
| 009 | move local preset; generic lookup rule; regenerate native package | The migration is unsafe unless lookup and regeneration close in the same unit. | pass |

## Validation strategy

| Slice | Required evidence |
| --- | --- |
| S0 | JSON/YAML/schema parse; table-driven red/green tests; existing draft validator still passes its own fixtures. |
| S1 | Digest substitution, ambient approval, volatile generation, incomplete first-surface, candidate-pass, unowned surface, and rendered-retell controls. |
| S2 | Post-apply prior-digest rejection; append-only correction replay; signal contains four axes and invalidation reference; reflect-now trigger. |
| S3 | canonical/generated drift check; local preset resolution; public/private string/path sweep; low/medium/complex Experiment Harness reports; private BTE integration receipt. |

## Gaps and blockers

- Blockers: none.
- GAP-WEG-01: semantic quality and comprehension remain human judgments. Owner: operator/intended reader. Repair: required digest-bound record, not automation.
- GAP-WEG-02: `interactive_technical_explainer` remains candidate after this work pack. Owner: Spellcraft/human promotion decision. Repair: additional transport evidence outside this plan.
- GAP-WEG-03: generalized bootstrap overlay merging remains deferred. Owner: bootstrap lifecycle if later needed. Current repair: local preset discovery contract.
- GAP-WEG-04: the private BTE witness may reveal additional transport-specific roles. Owner: Spellcraft. Repair: record as residue; do not silently widen the public base contract.

## Gate checks

1. Dispatch route validates: pass in `dispatch-validation.json`, with zero flags or blocks.
2. Distill validation: pass in `DISTILL-VALIDATION.md`.
3. First bounded implementation unit: SWU-WEG-001 only; its fixture-baseline receipt now passes.
4. Every later SWU has exact sources, write scope, acceptance evidence, and verification in its task file.
5. No implementation task may start directly from this Invoke result; Spellcraft must accept the lifecycle handoff first.
6. Any public/private leakage, candidate `pass`, digest substitution, or volatile full generation blocks promotion and closeout.

## Current next action

W0 is complete. Task Session may execute `SWU-WEG-004` to bind human evidence to exact artifact and surface digests before generation admission opens.
