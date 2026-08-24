# Revised Invoke one-shot workflow synthesis

Status: PASS  
Validation: PASS  
Evidence ceiling: `frozen-input-contractual-readiness`

Implementation remains gated on an approved capability-design/migration route
and passing fixtures. `invoke validate` remains deferred and is not current
enforcement.

## Definitional repairs

| Blocker | Correction |
|---|---|
| Standalone admission compiler duplicates Work Pack Readiness Audit | Removed as a capability/lifecycle owner. Deterministic projection generation and reference checking move inside Work Pack Readiness Audit phases 1–4 with `authorityEffect: none`. |
| Abstract `materialProducer` | Removed. Every SWU binds an exact immutable `materialPackageRef.producerOwnerRef`, package, receipt, schema, target inventory, and digest. WPRA never creates product/staged bytes. |
| Aggregate readiness/lifecycle status | Removed. Authored, registry release, mutation runtime, audit, approval, and chain statuses keep separate owner-produced receipts. |
| Generic outer runner | Replaced with existing `task-session-until-blocker`. |
| Copied question/decision state | Replaced with immutable Structured Interview and Decision Gate receipt refs. |
| Requested and admitted runtime mode collapsed | Split into `requestedTaskSessionExecutionMode` and `taskSessionAdmissionReceiptRef`. |
| Generated successor treated as authority | Replaced with `projectedNextSuccessor`, canonical Plan successor binding, equivalence validator, Continuation Router verification, and `authorityEffect: none`. |
| Canonical sources/projections/baselines/semantic hashes mixed | Split into four typed collections with producer, validator, authority effect, and invalidation effect. |
| Readiness implied future certainty | Explicitly limited to frozen-input contractual readiness; empirical runtime failures remain Task Session residue. |

## Root cause

The loop is an exact-binding gap between canonical Plan authoring and Task
Session admission. Invoke Plan can be valid while material, receipt semantics,
byte baselines, closeout contracts, or continuation bindings remain absent or
runtime-unevaluated. Task Session then becomes the first owner to detect
deterministic omissions already knowable from frozen inputs. Generic Refresh
has been used for planning repair, projection synchronization, and material
production, allowing locally valid transitions without execution progress.

Evidence:

- `research.md#Explorer-return-1:-local-owner-hop-forensics`
- `arcanum/spells/invoke/README.md:20-26,46-70,98-107,280-324`
- `arcanum/arcana/task-session/SKILL.md:216-289`
- `reviews/non-vacuity.md#Body-War-counterfactual`

## Corrected target lifecycle

```text
Invoke Define
  ├─ Context Builder evidence bindings
  └─ Structured Interview receipt refs
        ↓
Invoke Design
  ├─ canonical concern denominator
  ├─ accountable/contributing/artifact/validator ownership
  └─ dependency/interface closure
        ↓
Decision Gate for consequential choices
  └─ immutable decision receipt refs
        ↓
Invoke Plan / canonical WORK-PACK.md graph and contracts
  ├─ SWUs, dependencies, canonical successors
  ├─ commands, writes, validation, receipts
  ├─ closeout targets/baselines/delta policies
  └─ per-SWU material-producer obligations
        ↓
Exact per-SWU producers supply material packages
  └─ package + producerOwnerRef + receipt + schema + digest
        ↓
Work Pack Readiness Audit
  phases 1–4:
    generate normalized derived admission projection
    reference-check canonical inputs
    authorityEffect: none
  remaining audit:
    freeze/recheck snapshot
    validate graph/contracts
    reconcile Task Session admission
    challenge receipt semantics
    simulate closeout
    emit independent audit result
        ↓
Decision Gate / human epoch approval
  └─ binds projection digest, canonical snapshot, frontier,
     runtime identity, risk ceiling, and budget
        ↓
Task Session Until Blocker
  ├─ finite approved frontier, cursor, chainStatus
  └─ one fresh Task Session per SWU
        ↓
Task Session
  ├─ one-SWU admission and mutation
  ├─ semantic and immediately-before-write byte checks
  └─ empirical terminal receipt
        ↓
Continuation Router
  └─ verifies exact closeout/continuation route
        ↓
Invoke Refresh
  └─ receipt-bound bookkeeping/closeout deltas only
        ↓
Continuation Router joins closeout
        ↓
Task Session Until Blocker chooses one dependency-ready canonical successor
or emits chainStatus complete|blocked
```

No generated manifest/projection gains canonical authority. Only Task Session
Until Blocker emits `chainStatus: complete`, meaning all captured units closed.
Promotion remains separate. [Work Pack Readiness Audit
`README.md:56-146,194-214`; Task Session Until Blocker
`README.md:64-168`; `reviews/definitional.md#Exact-merge-targets`]

## Candidate verdicts

| Candidate | Verdict | Owner-preserving outcome |
|---|---|---|
| Harden Invoke Plan alone | KILL as sufficient; retain exit hardening | Plan authors complete canonical contracts, but WPRA independently binds and proves them. |
| Add a closure stage | KILL | Strengthen Define/Design/Plan, Structured Interview, and Decision Gate exits. |
| Standalone compiler/materializer | KILL | Derived projection generation is a WPRA internal step with no authority; product bytes stay with exact SWU producers. |
| Admission projection plus WPRA | PASS, conditional | Must reject every missing binding before a Task Session request and never repair Plan/material. |
| Generic Refresh repair/admission | KILL | Refresh remains for genuine synchronization and receipt-bound closeout. |
| Approved finite-frontier one-shot execution | PASS, conditional | Extend Task Session Until Blocker with approved epoch/digest, cursor, invalidation, and closeout-join checks. |

## Non-collapsing manifest

```yaml
schemaVersion:
manifestId:
evidenceCeiling: frozen-input-contractual-readiness

objectiveRef:
  canonicalRef:
  authorityOwnerRef:
  acceptanceObligationRefs: []
  authorityClassRef:
  publicationClassRef:

closureReceiptRefs:
  structuredInterviewReceiptRefs: []
  decisionGateReceiptRefs: []
  defineExitReceiptRef:
  designDenominatorReceiptRef:
  designSelectionReceiptRef:
  planReceiptRef:

authorityBindings:
  canonicalAuthorityRefs:
    - ref:
      selectors: []
      sha256:
      size:
      producerOwnerRef:
      validatorOwnerRef:
      authorityEffect: references-existing-canonical-authority
      invalidationEffect: invalidate-epoch-on-canonical-semantic-change

  derivedProjectionRefs:
    - ref:
      projectionClass:
      sha256:
      producerOwnerRef: work-pack-readiness-audit
      validatorOwnerRef:
      canonicalBindingRefs: []
      classifierVersion:
      preservationReceiptRef:
      authorityEffect: none
      invalidationEffect: >
        preserve only when equivalence is proven against unchanged canonical
        bindings; otherwise block projection consumption and invalidate the
        bound audit projection

  executionByteBaselines:
    - unitId:
      path:
      sha256:
      capturedAt:
      producerOwnerRef:
      validatorOwnerRef: task-session
      authorityEffect: none
      invalidationEffect: >
        pre-route mismatch invalidates audit/approval; post-approval or
        immediately-before-write mismatch blocks Task Session without overwrite
        or adoption

  semanticBindings:
    - bindingId:
      canonicalInputRefs: []
      semanticDigest:
      classifierVersion:
      producerOwnerRef: work-pack-readiness-audit
      validatorOwnerRef:
      authorityEffect: none
      invalidationEffect: >
        invalidate audit and approval on canonical semantic change; preserve
        only through explicit equivalence receipt

ownershipRefs:
  objectiveOwnerRef:
  designOwnerRef:
  planOwnerRef:
  readinessAuditOwnerRef: work-pack-readiness-audit
  approvalOwnerRef:
  taskSessionUntilBlockerOwnerRef: task-session-until-blocker
  taskSessionOwnerRef: task-session
  continuationRouterOwnerRef: continuation-router
  closeoutOwnerRef: invoke-refresh
  promotionOwnerRef:

canonicalPlanGraph:
  workPackRef:
  graphSelector:
  frontierSelector:
  units:
    - unitId:
      canonicalUnitRef:
      canonicalDependencyRefs: []
      canonicalSuccessorRef:
      executionContractRef:
      validationContractRef:
      closeoutContractRef:

executionBindings:
  - unitId:
    argv: []
    cwd:
    environmentBindingRef:
    timeout:
    expectedExit:
    riskClass:
    materialWrites: []
    executionOutputs: []
    allowedWrites: []
    immutablePaths: []
    validationRefs: []
    attemptPolicyRef:
    dependencyReceiptRefs: []
    materialPackageRef:
      packageRef:
      producerOwnerRef:
      producerReceiptRef:
      schemaRef:
      sha256:
      targetInventoryRef:

receiptBindings:
  terminalSchemaRef:
  semanticValidatorRef:
  expectedReceiptRefs:
    - {unitId, ownerRef, pathRef, semanticAssertionRefs: []}

closeoutBindings:
  - unitId:
    targetInventoryRef:
    executionByteBaselineRefs: []
    allowedDeltaPolicyRef:
    ownerValidationRefs: []
    expectedOwnerReceiptContractRef:
    closeoutRouteRef:

runtimeBinding:
  taskSessionRequestSchemaRef:
  runtimeIdentityPolicyRef:
  requestedTaskSessionExecutionMode:
  taskSessionAdmissionReceiptRef:

statusReceiptRefs:
  artifactAuthoredStatus: {ownerRef, receiptRef}
  registryReleasedStatus: {ownerRef, receiptRef}
  mutationRuntimeReadyStatus: {ownerRef: task-session, receiptRef}
  auditVerdict: {ownerRef: work-pack-readiness-audit, receiptRef}

lifecycleStatusRefs:
  planArtifactStatus: {ownerRef: invoke-plan, receiptRef}
  auditStatus: {ownerRef: work-pack-readiness-audit, receiptRef}
  approvalStatus: {ownerRef, receiptRef}
  chainStatus: {ownerRef: task-session-until-blocker, receiptRef}

epochBinding:
  epochId:
  auditProjectionDigest:
  canonicalSemanticDigest:
  sourceSnapshotDigest:
  approvedFrontierRef:
  runBudgetRef:
  decisionGateApprovalReceiptRef:

continuityProjection:
  cursor:
  completedUnitReceiptRefs: []
  joinedCloseoutReceiptRefs: []
  projectedNextSuccessor:
    unitId:
    canonicalSuccessorRef:
    projectionOwnerRef:
    equivalenceValidatorRef:
    continuationRouterVerificationReceiptRef:
    authorityEffect: none
  blockerFingerprint:
```

The manifest carries closure receipt references; it never recomputes question
or decision status. WPRA cannot populate missing material bytes. Required
write-partition invariant:

```text
materialWrites ∩ executionOutputs = ∅
materialWrites ∪ executionOutputs = allowedWrites
```

Every material ref, owner, dependency, validator, receipt, closeout target, and
canonical successor must resolve before approval.

## Exact owner map

| Concern | Owner | Change |
|---|---|---|
| Objective baseline | Invoke Define | Strengthen exit receipt; retain Context Builder bindings. |
| Question closure | Structured Interview | Manifest references immutable receipts only. |
| Consequential choice/approval | Decision Gate/human | Bind projection/source/frontier/risk/budget digests. |
| Concern/owner/dependency closure | Invoke Design | Total selection/ownership receipts. |
| Canonical SWU graph/contracts | Invoke Plan / `WORK-PACK.md` | Remains authoritative; emits audit-ready refs. |
| Product/staged material | Exact per-SWU `producerOwnerRef` | No generic owner; no WPRA byte creation. |
| Derived admission projection | WPRA phases 1–4 | Deterministic, `authorityEffect: none`. |
| Immutable proof | Work Pack Readiness Audit | Independent audit status/verdict and evidence ceiling. |
| Finite-frontier sequencing | Task Session Until Blocker | Approved epoch, cursor, frontier, joined closeouts. |
| One-SWU execution | Task Session | Admission, prewrite check, mutation, validation, residue. |
| Continuation verification | Continuation Router | Canonical route verification; projection is non-authoritative. |
| Bookkeeping closeout | Invoke Refresh | Approved delta classes only. |
| Promotion | Existing Goal/Craft/human route | Separate approval gate. |
| Metrics/history | Existing observability/chain receipts | First-knowable/detected, cursor, invalidation, bounce. |

The public schema must remain project-agnostic; private DomainSpec, Saturn, and
`cyberAlchemy-v2` prose cannot cross into Arcanum.

## Epoch and invalidation

1. WPRA captures canonical refs and generates the no-authority projection.
2. WPRA validates graph closure, exact material, writes, commands, receipts,
   closeout semantics, Task Session schema compatibility, and frozen snapshot.
3. Decision Gate/human approval binds projection digest, semantic digest,
   snapshot, frontier, runtime identity, risk, and budget.
4. Task Session Until Blocker rechecks epoch bindings before each request.
5. Task Session rechecks semantic bindings at admission and byte baselines
   immediately before the first write.
6. Changes to objective/acceptance, design disposition, accountable owner,
   dependency/successor, SWU boundary, material, write partition,
   validation/receipt semantics, closeout, runtime identity/schema,
   authority/publication, frontier, or budget invalidate audit and approval.
7. Projection-only regeneration preserves only with pinned canonical inputs,
   classifier version, and an explicit preservation receipt.
8. Projection mismatch blocks consumption but cannot override canonical source.
9. New work cannot join an approved frontier.
10. Post-baseline drift is empirical Task Session residue.

## One-shot algorithm

```text
require independent audit pass|allowed flag, approval receipt,
finite frontier F, unchanged semantic/snapshot digests

Task Session Until Blocker owns cursor and chainStatus.

repeat:
  revalidate epoch bindings
  Continuation Router verifies one dependency-ready successor
  against canonicalSuccessorRef
  block on none-when-expected, ambiguity, frontier expansion,
  invalidation, exhausted budget, or repeated cursor

  launch exactly one fresh Task Session for that SWU
  Task Session verifies admission receipt and digests
  Task Session checks target bytes immediately before first write
  execute, validate, emit one terminal receipt

  on Task Session BLOCK/FAIL:
    preserve empirical residue; chainStatus=blocked; stop

  Continuation Router verifies exact closeout route
  Invoke Refresh applies only approved receipt-bound deltas
  Continuation Router joins closeout receipt or NO_OP proof
  block if join absent/invalid

  derive novel cursor from epoch + terminal receipt + closeout
  continue

when every unit in F has joined closeout:
  Task Session Until Blocker emits chainStatus=complete
```

## Body War fixture set

Every fixture supplies a frozen input tree, at most one fault, expected
first-knowable stage, expected first-detected gate, owner, terminal code,
receipt count, allowed writes, and forbidden-transition assertions.

Positive `PBW-01-body-war-swu-001-stable` binds the exact 09:15 handoff:

- `TASK-SESSION-HANDOFF.json` selectors `admission_probe`, `material`,
  `context_pack`, `closeout_owner_contract`, `mutation_ready`, and
  `live_product_mutation_started`
- three-target package, target inventory, exact producer receipt/schema,
  digests, allowed deltas, closeout receipt contract, canonical successor
- approved frontier containing SWU-001
- stable bytes through immediately-before-write check

Expected: WPRA PASS → approval → one Task Session Until Blocker request → Task
Session completion → joined closeout → canonical successor verification; zero
generic repair Refresh returns.

| Fixture | Single fault | Expected first gate | Forbidden transition |
|---|---|---|---|
| `NBW-01-package-ref` | package ref absent | WPRA phases 1–4 | no Task Session Until Blocker request |
| `NBW-02-producer-owner` | owner absent/unresolved | WPRA phases 1–4 | no request/selector |
| `NBW-03-producer-receipt` | receipt absent | WPRA phases 1–4 | no request/selector |
| `NBW-04-schema-binding` | schema absent | WPRA phases 1–4 | no request/selector |
| `NBW-05-target-inventory` | inventory absent | WPRA audit | no request/selector |
| `NBW-06-byte-baseline` | baseline absent | WPRA audit | no request/selector |
| `NBW-07-delta-policy` | delta policy absent | WPRA audit | no request/selector |
| `NBW-08-closeout-receipt` | closeout contract absent | WPRA audit | no request/selector |
| `NBW-09-successor-binding` | successor absent/non-unique | WPRA graph audit | no request/selector |
| `NBW-10-preroute-material-digest` | digest mismatch before approval | WPRA snapshot recheck | no request/selector |

For deterministic faults, first-knowable stage must equal first-detected gate.

`NBW-11-post-approval-concurrent-drift` changes one target only after
approval/baseline and before first write. Task Session must block without
overwrite, adoption, or attribution; this is runtime residue.

Additional controls:

- `P-PROJ-01`: equivalent projection regeneration requires pinned canonical
  inputs/classifier and preservation receipt; no invalidation.
- `N-SEM-01..05`: owner, material, validation, receipt, or closeout semantic
  change invalidates audit/approval.
- `N-RUN-01`: contracts pass but command fails; Task Session blocks empirically.

## Progress and loop detection

Track completed/frontier SWUs, requests, admissions, prewrite/runtime blocks,
joined/missing closeouts, first-knowable/detected distance, owner bounces,
generic Refresh repairs, semantic invalidations, equivalence preservations,
cursor/blocker repetition, Plan-to-mutation transitions, and
governance/projection versus implementation writes.

Stop on repeated cursor/fingerprint without changed evidence, ambiguous or
out-of-frontier successor, missing closeout, invalidated epoch, or exhausted
budget. Progress means a joined SWU closeout, evidence-valid changed blocker
fingerprint, or newly approved epoch—not a rewritten generated view.

Acceptance:

- one approved Body War frontier run;
- zero predictable generic-Refresh repair returns;
- deterministic single faults block before any Task Session request;
- stable SWU-001 completes with joined closeout;
- equivalent projection regeneration is preserved;
- semantic changes invalidate;
- post-baseline drift blocks without overwrite/adoption;
- no future empirical certainty claim.

## Citation bindings

| Claim | Local binding | Primary precedent and limit |
|---|---|---|
| WPRA owns projection and proof | `work-pack-readiness-audit/README.md:56-146,194-214` | Bazel action graph/key/analysis/execution: transfer declared graph/key invalidation, not undeclared hermeticity |
| Explicit preservation/invalidation | WPRA semantic bindings | LLVM `Passes.html#introduction`; facts are limited to the model |
| Exact epoch/stale rejection | Decision Gate + Task Session Step 5A | Terraform saved plan and remote staleness; no apply-success guarantee |
| Durable one-shot replay | Task Session Until Blocker `README.md:64-168` | Temporal Replays/Commands/Status + Worker Versioning; external effects still fail |
| Typed traces | Context Builder | ReqIF 1.1 identities/relations only, not readiness |
| Recovery metadata | Plan/Task Session/closeout | Sagas, SIGMOD 1987; live-definition versioning is a modern inference |
| One-SWU empirical residue | Task Session `SKILL.md:216-289` | Runtime failure remains possible after admission |
| Question/choice closure | Structured Interview and Decision Gate | No new external mechanism |

Started: `2026-07-30T17:20:08Z`  
Finished: `2026-07-30T17:24:56Z`
