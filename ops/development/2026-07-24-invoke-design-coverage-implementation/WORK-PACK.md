# WORK-PACK: Invoke Design Coverage

## Control fields

| Field | Value |
| --- | --- |
| phaseStatus | `pass`; Define, Design, and Plan artifacts are authored |
| targetEvidenceState | `design-validator-pass`; Plan evidence remains separate |
| workPackGateStatus | `pass`; 14/14 implementation SWUs have terminal passing receipts |
| handoffStatus | `implementation-complete`; known path findings repaired, promotion flagged by broader consumer-adapter residue |
| complexity | `high` |
| outputMode | `split` |
| executionPackRef | `EXECUTION-PACK.md` |
| layeringArtifactRef | `IMPLEMENTATION-LAYERING.md` |
| dispatchTechniqueTrace | `DISPATCH-TECHNIQUE-TRACE.md` |
| dispatchValidation | `dispatch-validation.json` must be `pass` |
| distillValidationStatus | `pass` |
| swuAtomicityStatus | `pass`; task-shaped count 0 |
| firstUnitNarrownessStatus | `pass` |
| closeoutSyncStatus | `pass`; exact rows are in `work-pack/shared/CLOSEOUT-CONTRACT.md` |
| activeLayerWindow | `L3` |
| selectedSWU | none; chain complete |
| selectedExecutionMode | complete |
| lastUpdatedAt | `2026-07-24` |

## Objective

Implement a deterministic, independently-denominated Invoke Design-selection
gate that closes scope, prevents false N/A and circular readiness, selects
architecture depth and UX by exact predicates, and keeps Design validation
separate from Plan evidence.

## Delivery slices

| Slice | Outcome | Layer | Wave | Dependencies | Validation |
| --- | --- | --- | --- | --- | --- |
| S0 | implementation-independent expected behavior is frozen | L0 | [W0](work-pack/waves/W0.md) | none | corpus parses, IDs are unique, expected selections/diagnostics complete |
| S1 | schemas, extractor, validator, and runner reproduce the corpus | L1 | [W1](work-pack/waves/W1.md) | S0 | schema/unit/mutation/bounded-selection suites pass |
| S2 | Invoke Design and companion templates consume the new result safely | L2 | [W2](work-pack/waves/W2.md) | S1 | contract fixtures, evidence-state, UX, and architecture checks pass |
| S3 | generated runtimes and a generic live route preserve behavior | L3 | [W3](work-pack/waves/W3.md) | S2 | parity, live Define→Design→Plan, leakage scan, and final audit pass |

## Task board

| Task | Outcome | Layer | Wave | Owner | Gate | Status |
| --- | --- | --- | --- | --- | --- | --- |
| [TASK-DVC-001](work-pack/tasks/TASK-DVC-001-FIXTURE-DENOMINATOR.md) | freeze independent fixture denominator | L0 | W0 | Spellcraft | dispatch pass | complete |
| [TASK-DVC-002](work-pack/tasks/TASK-DVC-002-SCHEMAS.md) | add three exact public schemas | L1 | W1 | Spellcraft | SWU-DVC-001 receipt | complete |
| [TASK-DVC-003](work-pack/tasks/TASK-DVC-003-EXTRACTOR.md) | extract denominator signals deterministically | L1 | W1 | Spellcraft | schema receipts | complete |
| [TASK-DVC-004](work-pack/tasks/TASK-DVC-004-VALIDATOR.md) | validate binding, ownership, dispositions, fixed point, and evidence state | L1 | W1 | Spellcraft | extractor and schema receipts | complete |
| [TASK-DVC-005](work-pack/tasks/TASK-DVC-005-FIXTURE-RUNNER.md) | run frozen controls and predicate mutations | L1 | W1 | Spellcraft | validator receipt | complete |
| [TASK-DVC-006](work-pack/tasks/TASK-DVC-006-CONTRACTS-AND-TEMPLATES.md) | integrate Design, architecture, and UX contracts | L2 | W2 | Spellcraft | W1 receipt set | complete |
| [TASK-DVC-007](work-pack/tasks/TASK-DVC-007-GENERATED-PARITY.md) | synchronize generated runtime projections | L3 | W3 | Spellcraft + bootstrap owner | canonical validation receipt | complete |
| [TASK-DVC-008](work-pack/tasks/TASK-DVC-008-LIVE-PROOF.md) | prove generic composed behavior and boundaries | L3 | W3 | Spellcraft | parity receipt | complete |
| [TASK-DVC-VERIFY](work-pack/tasks/TASK-DVC-VERIFY.md) | recompose requirements and assess promotion readiness | L3 | W3 | Spellcraft + human maintainer | all implementation receipts | complete with promotion flag |

## Shared SWU manifest

Machine view: `work-pack/swu-manifest.json`.

| SWU | Parent | Primary behavior | Independent acceptance | State |
| --- | --- | --- | --- | --- |
| SWU-DVC-001 | TASK-DVC-001 | freeze source-backed fixture denominator and exact expectations | corpus digest and all expected result fields are stable before implementation | complete |
| SWU-DVC-002A | TASK-DVC-002 | validate one closed scope manifest | invalid closure or digest cannot pass schema checks | complete |
| SWU-DVC-002B | TASK-DVC-002 | validate one denominator receipt | stale, incomplete, or self-issued receipt cannot validate | complete |
| SWU-DVC-002C | TASK-DVC-002 | validate one selection result | illegal disposition, owner, fixed-point, or evidence state cannot validate | complete |
| SWU-DVC-003 | TASK-DVC-003 | extract normalized signals from exact manifest selectors | omissions and duplicates produce exact deterministic diagnostics | complete |
| SWU-DVC-004 | TASK-DVC-004 | compute one total two-pass selection result | every signal binds once and pass-two change blocks | complete |
| SWU-DVC-005 | TASK-DVC-005 | execute frozen and mutation fixture matrices | every case matches exact selection and diagnostic expectations | complete |
| SWU-DVC-006A | TASK-DVC-006 | integrate Design mode and evidence-state contracts | authored-only cannot route as validator-passed or Plan-evidenced | complete |
| SWU-DVC-006B | TASK-DVC-006 | integrate six-view concern trace and architecture extensions | baseline remains mandatory while triggered depth is exact | complete |
| SWU-DVC-006C | TASK-DVC-006 | integrate the human semantic UX trigger and output contract | human semantic positives select UX; backend/style negatives do not | complete |
| SWU-DVC-006D | TASK-DVC-006 | integrate root Invoke evidence-state and handoff reporting | root output cannot collapse authored, registry, runtime, Design, or Plan evidence axes | complete |
| SWU-DVC-006E | TASK-DVC-006 | connect the Design-selection runner to aggregate validation | aggregate failure preserves exact child diagnostics and blocks | complete |
| SWU-DVC-007 | TASK-DVC-007 | regenerate and prove canonical/runtime parity | generated profiles match accepted canonical source | complete |
| SWU-DVC-008 | TASK-DVC-008 | run one generic composed proof and boundary audit | exact evidence states, selections, diagnostics, privacy, and recomposition pass | complete |

## Atomicity review

| SWU | Candidate splits | Retained boundary | Verdict |
| --- | --- | --- | --- |
| 001 | fixture IDs; inputs; expectations; digest | none independently constrain implementation without the complete corpus contract | pass |
| 002A | manifest fields; closure; digest | one schema-valid manifest decision | pass |
| 002B | identity; signals; receipt digest | one schema-valid denominator receipt decision | pass |
| 002C | concerns; fixed point; evidence state | one schema-valid selection result decision | pass |
| 003 | selector read; signal normalization; diagnostics | conjuncts of one deterministic extraction result | pass |
| 004 | precedence; ownership; dispositions; pass comparison | conjuncts of one total selection verdict | pass |
| 005 | fixture invocation; mutation generation; expected comparison | one runner behavior over a frozen corpus | pass |
| 006A | mode order; gates; evidence states | one Design-mode admission contract | pass |
| 006B | baseline; trace; extensions | one architecture output contract | pass |
| 006C | actor predicate; semantic change; UX output | one UX-selection contract | pass |
| 006D | root evidence states; result fields; handoff | one Invoke root reporting contract | pass |
| 006E | child runner invocation; result propagation | one aggregate validation integration behavior | pass |
| 007 | regenerate; compare; scan | one canonical-to-runtime parity decision | pass |
| 008 | live route; evidence ceiling; boundary audit | one end-to-end recomposition proof | pass |

Task-shaped SWU count: 0.

## Validation strategy

| Layer | Required evidence |
| --- | --- |
| L0 | JSON/YAML parse, unique IDs, complete expected outcomes, source trace, frozen corpus digest |
| L1 | JSON Schema checks; extractor/validator unit tests; omission, stale, self-issued, unbound, false-N/A, pass-two, bounded-selection, and mutation fixtures |
| L2 | Design mode block/pass fixtures; architecture trace/extension checks; UX positive/negative/rendered diagnostic checks; aggregate runner |
| L3 | canonical/generated parity, generic composed live run, evidence-state ceiling, private-path/name scan, full Invoke regression, final lifecycle audit |

## Blockers and gaps

See `GAPS.md`. DVC-G01 gates only later SWUs that overlap dirty canonical
sources. The selected fixture-only SWU writes a new isolated directory and may
proceed after Spellcraft rechecks its exact absence/baseline.

## Gate checks

1. Define and Design authoring: pass.
2. Dispatch validation: pass.
3. Distill validation: pass.
4. All non-exempt tasks have implementation-detail and SWU contracts.
5. Every mutation SWU has exact closeout synchronization.
6. First unit is fixture-only, reversible, and narrow.
7. No source implementation occurred in this Invoke run.
8. Spellcraft must recheck dirty baselines before every overlapping SWU.
9. Target evidence advances to `design-validator-pass` only from the complete
   validator and live-proof receipts; Plan evidence remains independent.

## Final handoff

- Next owner: public-hygiene owner, then human promotion maintainer.
- Selected unit: none; the implementation chain is complete.
- Completed evidence: SWU-DVC-001 froze 28 cases and 27 mutations at corpus
  digest `347618abe9ae700fb515a127d4d5a75a78665013dbc68fd637bd5bd7200a5c74`.
- Completed L1 evidence: 28/28 frozen cases and 27/27 mutations pass without
  changing the W0 corpus digest.
- Completed L2 evidence: Design, architecture, UX, and root reporting contracts
  pass the deterministic contract probe; a whitespace-sensitive UX probe
  defect was repaired and the full 28-case/27-mutation suite re-passed.
- Completed aggregate evidence: the full Invoke runner invokes the
  Design-selection child, surfaces its report, preserves child output, and
  passes every existing fixture.
- Completed generated evidence: repo-codex and Claude Invoke surfaces exactly
  match fresh staged generation; the DVC/generated public scan, aggregate
  regression, and `make bump-check` pass.
- Completed live evidence: all four composed cases pass across canonical,
  repo-codex, and Claude runtimes; positive and negative Plan routing preserves
  the exact evidence ceiling.
- Final lifecycle audit: `flag`, not `block`; implementation acceptance passes
  and the four original path findings are repaired, but promotion remains false
  until historical `projects/ide-extension` fixture and receipt bindings are
  extracted behind a governed consumer adapter.
- No commit, push, release, or promotion was performed.
