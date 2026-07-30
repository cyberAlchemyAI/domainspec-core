# Invoke one-shot workflow findings

Status: PASS  
Validation: PASS  
Evidence ceiling: `frozen-input-contractual-readiness`

## Plain-language answer

Plans and Refreshes block in the middle because the current workflow lets a Plan
be valid before anyone has proved that its first SWU has exact executable
material, an accountable producer receipt and schema, stable target bytes,
closed validation and closeout contracts, and one canonical successor. Task
Session is therefore the first owner to check omissions that were already
knowable from frozen planning inputs. A generic Refresh then gets asked to do
three unlike jobs—repair planning, synchronize a projection, and produce
executable handoff bytes—so individual transitions can pass while the work
does not advance.

The realistic improvement is narrower than “finish everything up front.”
Move deterministic question, decision, owner, dependency, material,
command/write, validation, receipt, continuation, and closeout closure ahead of
any Task Session request. Do **not** move empirical execution there: concurrent
post-baseline writes, tool/environment failures, browser behavior, and product
defects discovered only by executing remain fail-closed Task Session residue.
The Body War history demonstrates both sides: the missing SWU-001 package and
contracts were pre-route omissions, while the later unattributed target drift
could only be detected at the immediately-before-write check
([local forensics](research.md#explorer-return-1-local-owner-hop-forensics);
`arcanum/spells/invoke/README.md:20-26,46-70,98-107,280-324`;
`arcanum/arcana/task-session/SKILL.md:216-289`).

## Current and target architecture

Current:

```text
Invoke Define → Design → Plan (runtime readiness may remain unevaluated)
  → Task Session Until Blocker
  → Task Session discovers deterministic admission gaps
  → generic Invoke Refresh repairs/synchronizes/materializes
  → retry
  → Task Session may still block on honest empirical drift
```

Target:

```text
Invoke Define + Structured Interview receipts
  → Invoke Design ownership/dependency closure
  → Decision Gate receipts for consequential choices
  → Invoke Plan canonical WORK-PACK graph and exact SWU contracts
  → exact per-SWU producers supply material bytes and receipts
  → Work Pack Readiness Audit phases 1–4 generate and check a derived,
    no-authority admission projection; the remaining phases audit it
  → Decision Gate/human approves the exact epoch
  → Task Session Until Blocker coordinates the finite frontier
  → one fresh, one-SWU Task Session at a time
  → Continuation Router verifies route; Invoke Refresh performs only
    receipt-bound closeout bookkeeping; Continuation Router joins it
```

There is no standalone admission compiler or materializer. Projection
generation is internal to Work Pack Readiness Audit (WPRA), has
`authorityEffect: none`, and cannot create or repair product/staged material.
Generated projections never acquire canonical authority. Task Session Until
Blocker owns outer sequencing; Task Session retains one-SWU admission,
mutation, validation, and empirical residue
(`arcanum/spells/work-pack-readiness-audit/README.md:56-146,194-214`;
`arcanum/spells/task-session-until-blocker/README.md:64-168`;
[definitional recheck](reviews/definitional-recheck.md)).

## Normalized objective-execution manifest

The manifest is a digest-bound projection of owned evidence, not a new source
of truth. Its minimum non-collapsing shape is:

```yaml
schemaVersion:
manifestId:
evidenceCeiling: frozen-input-contractual-readiness
objectiveRef: {canonicalRef, authorityOwnerRef, acceptanceObligationRefs: []}
closureReceiptRefs:
  structuredInterviewReceiptRefs: []
  decisionGateReceiptRefs: []
  defineExitReceiptRef:
  designDenominatorReceiptRef:
  designSelectionReceiptRef:
  planReceiptRef:
authorityBindings:
  canonicalAuthorityRefs: []   # immutable selectors/digests; existing authority
  derivedProjectionRefs: []    # WPRA-produced; authorityEffect: none
  executionByteBaselines: []   # per unit/path/digest
  semanticBindings: []         # canonical inputs/classifier/semantic digest
canonicalPlanGraph:
  workPackRef:
  frontierSelector:
  units: []                    # dependencies, canonical successor, contracts
executionBindings:
  - unitId:
    argv: []
    cwd:
    materialWrites: []
    executionOutputs: []
    allowedWrites: []
    materialPackageRef:
      {packageRef, producerOwnerRef, producerReceiptRef, schemaRef, sha256,
       targetInventoryRef}
receiptBindings: {terminalSchemaRef, semanticValidatorRef, expectedReceiptRefs: []}
closeoutBindings: []           # baselines, delta policy, owner receipt contract
runtimeBinding:
  requestedTaskSessionExecutionMode:
  taskSessionAdmissionReceiptRef:
statusReceiptRefs:
  artifactAuthoredStatus: {}
  registryReleasedStatus: {}
  mutationRuntimeReadyStatus: {}
  auditVerdict: {}
lifecycleStatusRefs:
  planArtifactStatus: {}
  auditStatus: {}
  approvalStatus: {}
  chainStatus: {}
epochBinding:
  {epochId, auditProjectionDigest, canonicalSemanticDigest,
   sourceSnapshotDigest, approvedFrontierRef, runBudgetRef,
   decisionGateApprovalReceiptRef}
continuityProjection:
  cursor:
  completedUnitReceiptRefs: []
  joinedCloseoutReceiptRefs: []
  projectedNextSuccessor:
    {unitId, canonicalSuccessorRef, projectionOwnerRef,
     equivalenceValidatorRef, continuationRouterVerificationReceiptRef,
     authorityEffect: none}
```

Question and decision statuses are never recomputed; the manifest carries the
owning receipts. Authored, registry-release, mutation-runtime, audit, approval,
and chain statuses remain independently owned and witnessed. In particular,
an authored artifact is not thereby registry-released or runtime-ready; an
audit pass is not approval; and only Task Session Until Blocker may emit
`chainStatus: complete`. For each SWU:

```text
materialWrites ∩ executionOutputs = ∅
materialWrites ∪ executionOutputs = allowedWrites
```

Every owner, dependency, material ref, validator, receipt, closeout target, and
canonical successor must resolve before approval
([revised synthesis, non-collapsing manifest](synthesis-revised.md#non-collapsing-manifest);
[definitional repair](reviews/definitional.md#required-repairs)).

## Blocker, question, and decision closure contract

Structured Interview owns unresolved questions and emits immutable closure
receipts. Invoke Define owns the objective and acceptance baseline. Invoke
Design owns the concern denominator, accountable ownership, dependencies, and
interfaces. Decision Gate/human owns consequential choices and approval.
Invoke Plan owns the canonical SWU graph and contracts. WPRA may normalize,
reference-check, and reject those inputs, but may neither answer questions,
make choices, edit Plan, nor manufacture missing bytes.

Typed routing should return an omission to its earliest owner:
objective ambiguity to Define/Interrogation; open consequential decisions to
Decision Gate; owner/interface gaps to Design; atomicity, command, validation,
receipt, successor, or closeout gaps to Plan; material absence/staleness to the
exact `materialPackageRef.producerOwnerRef`; projection/reference/audit defects
to WPRA or the referenced producer. No deterministic blocker may cause a Task
Session request. Empirical command, environment, product, or post-baseline
drift failures terminate in Task Session evidence
([protocol return](research.md#explorer-return-3-formal-protocol);
`arcanum/arcana/structured-interview-kits/SKILL.md:35-53,93-107`;
`arcanum/arcana/decision-gate/SKILL.md:51-88,176-192`).

## Plan epoch and invalidation

WPRA freezes canonical refs, produces the no-authority projection, and checks
graph, contracts, exact material, writes, receipt semantics, closeout, Task
Session schema compatibility, and snapshot. Approval binds projection and
semantic digests, source snapshot, finite frontier, runtime identity, risk, and
budget. Task Session Until Blocker rechecks these before each request; Task
Session rechecks semantic bindings at admission and byte baselines immediately
before its first write.

Invalidate audit and approval on semantic changes to objective/acceptance,
design disposition, accountable owner, dependencies/successors, SWU boundary,
material, write partition, validation or receipt meaning, closeout, runtime
identity/schema, authority/publication, frontier, or budget. Equivalent
projection regeneration preserves the epoch only when canonical inputs and
classifier version are pinned and an equivalence receipt proves preservation.
Projection mismatch blocks consumption but cannot override canonical Plan.
New work requires a new epoch. Post-approval drift remains an empirical Task
Session block.

This transfers explicit invalidation without overclaiming: LLVM separates
analysis facts from transforms and invalidates stale analysis
([LLVM](https://llvm.org/docs/Passes.html#introduction)); Bazel distinguishes
the derived action graph/key from execution
([Bazel](https://docs.bazel.build/versions/5.1.1/glossary.html)); Terraform
binds a saved plan and rejects stale remote plans without guaranteeing apply
success ([plan](https://developer.hashicorp.com/terraform/cli/commands/plan),
[remote saved plans](https://developer.hashicorp.com/terraform/enterprise/workspaces/run/cli#remote-saved-plans)).

## Material-owner decision and capability owner map

There is intentionally no generic materializer. The exact per-SWU producer
named by `producerOwnerRef` owns material bytes, package, receipt, schema,
inventory, and digest. WPRA only verifies them.

| Concern | Exact owner |
|---|---|
| Objective baseline | Invoke Define |
| Question closure | Structured Interview |
| Consequential choice and epoch approval | Decision Gate/human |
| Concern, owner, dependency closure | Invoke Design |
| Canonical SWU graph/contracts | Invoke Plan / `WORK-PACK.md` |
| Product/staged material bytes | exact per-SWU `producerOwnerRef` |
| Derived admission projection | WPRA phases 1–4, no authority |
| Frozen-input contractual readiness proof | WPRA |
| Finite-frontier cursor and chain status | Task Session Until Blocker |
| One-SWU execution and empirical residue | Task Session |
| Canonical continuation verification/join | Continuation Router |
| Receipt-bound bookkeeping closeout | Invoke Refresh |
| Promotion | existing Goal/Craft/human route, separately gated |
| Metrics/history | observability and chain receipts, non-authority |

The schema must remain public and project-agnostic; private DomainSpec, Saturn,
or `cyberAlchemy-v2` prose must not cross into Arcanum.

## One-shot outer route, with preserved single-SWU sessions

Given independent audit pass (or an explicitly allowed flag), an approval
receipt, finite frontier, unchanged epoch, and budget, Task Session Until
Blocker owns the cursor. It asks Continuation Router to verify exactly one
dependency-ready canonical successor, then launches one fresh Task Session for
that SWU. Task Session admits, rechecks, writes, validates, and emits one
terminal receipt. A block/fail stops the chain with residue. On success,
Continuation Router verifies the exact closeout route, Invoke Refresh applies
only approved receipt-bound deltas, and Continuation Router joins the receipt
or a valid `NO_OP` proof. Only a novel cursor may continue. Ambiguity, missing
join, frontier expansion, invalidation, repeated cursor/fingerprint, or budget
exhaustion stops fail-closed. Completion means every approved-frontier unit has
a joined closeout, not promotion or production readiness.

Temporal supplies a bounded precedent for durable history, deterministic replay,
and version binding, while leaving activity failures explicit
([workflow execution](https://docs.temporal.io/workflow-execution),
[worker versioning](https://docs.temporal.io/production-deployment/worker-deployments/worker-versioning)).
ReqIF supports typed identities and relations, not readiness
([ReqIF 1.1](https://www.omg.org/spec/ReqIF/1.1/)). Sagas support explicit
subtransaction/recovery structure; treating live-definition migration as a
versioning requirement is a modern inference, not a claim of the 1987 paper
([Garcia-Molina and Salem](https://doi.org/10.1145/38713.38742)).

## Migration sequence

1. Specify a project-agnostic manifest and semantic-digest rules.
2. Strengthen Define, Design, Structured Interview, Decision Gate, and Plan exit
   receipts without giving Invoke execution authority.
3. Add the deterministic, no-authority projection generator inside WPRA phases
   1–4 and preserve WPRA's independent audit verdict.
4. Require exact per-SWU producers to supply package, receipt/schema,
   inventory, and digests; WPRA must never synthesize these bytes.
5. Bind Decision Gate approval to the audited epoch and finite frontier.
6. Extend Task Session Until Blocker to consume the approved epoch, retain a
   durable cursor, recheck invalidation, and require closeout joins.
7. Preserve Task Session's one-SWU admission/mutation boundary and narrow
   Refresh to synchronization and receipt-bound closeout.
8. Add first-knowable/first-detected, bounce, invalidation, cursor, and closeout
   metrics.
9. Run the proposed fixtures and one bounded Body War replay before registry,
   promotion, or enforcement claims. Deferred `invoke validate` is not current
   enforcement.

Use a bounded Spellcraft route to design, install, and validate this composition
across the existing owners. That route should treat WPRA plus Task Session Until
Blocker as the spell backbone and require the fixture suite as its admission
evidence. This finding does not author another Invoke plan and does not
authorize capability changes.

## Stop doing

- Stop treating Plan PASS as runtime readiness.
- Stop adding a duplicate closure stage.
- Stop proposing a standalone compiler or compiler/materializer.
- Stop letting a generated projection gain authority or invalidate an epoch by
  byte change alone.
- Stop using generic Refresh as the normal repair/admission lane.
- Stop asking Task Session to discover deterministic material/owner/closeout
  omissions.
- Stop merging authored, registry, runtime, audit, approval, and chain states.
- Stop expanding an approved frontier or silently adopting drift.
- Stop claiming preflight predicts future runtime success.

## Progress metrics

Track approved-frontier and completed SWUs; Task Session requests/admissions;
prewrite and runtime blocks; joined/missing closeouts; first-knowable versus
first-detected distance; owner bounces and generic-Refresh repairs; semantic
invalidations and equivalence preservations; cursor/blocker repetition;
Plan-to-mutation transitions; and governance/projection versus implementation
writes. Progress is a joined SWU closeout, an evidence-valid changed blocker
fingerprint, or a newly approved epoch—not a rewritten generated view. Body
War's observed baseline was three Refreshes before the ready handoff, two Task
Session bounces overall, two staleness/drift events, and one strict no-progress
owner return ([counts and scope](research.md#explorer-return-1-local-owner-hop-forensics)).

## Exact Body War replay and fixtures

The positive replay `PBW-01-body-war-swu-001-stable` binds the exact 09:15:22Z
handoff's `admission_probe`, `material`, `context_pack`,
`closeout_owner_contract`, `mutation_ready`, and
`live_product_mutation_started`; the three-target package, exact producer
receipt/schema, inventory, digests, baselines, deltas, closeout contract,
canonical successor, and a frontier containing SWU-001; and stable bytes through
the immediately-before-write check. Expected: WPRA PASS, approval, exactly one
outer request, one SWU-001 Task Session completion, joined closeout, verified
canonical successor, and zero generic repair Refresh returns.

`PBW-01` is **proposed and unverified; it has not been executed**. The following
single-fault negatives are likewise **proposed and unverified**, and each must
forbid **any Task Session Until Blocker request/selector and therefore any Task
Session request**:

| Fixture | Single fault | Expected first gate |
|---|---|---|
| `NBW-01-package-ref` | package ref absent | WPRA phases 1–4 |
| `NBW-02-producer-owner` | producer owner absent/unresolved | WPRA phases 1–4 |
| `NBW-03-producer-receipt` | producer receipt absent | WPRA phases 1–4 |
| `NBW-04-schema-binding` | schema absent | WPRA phases 1–4 |
| `NBW-05-target-inventory` | inventory absent | WPRA audit |
| `NBW-06-byte-baseline` | baseline absent | WPRA audit |
| `NBW-07-delta-policy` | allowed-delta policy absent | WPRA audit |
| `NBW-08-closeout-receipt` | closeout receipt contract absent | WPRA audit |
| `NBW-09-successor-binding` | successor absent/non-unique | WPRA graph audit |
| `NBW-10-preroute-material-digest` | pre-approval digest mismatch | WPRA snapshot recheck |

For each deterministic fault, first-knowable must equal first-detected.
`NBW-11-post-approval-concurrent-drift` is a separate proposed runtime fixture:
change one target after approval/baseline but before first write; Task Session
must block without overwrite, adoption, or attribution. Controls
`P-PROJ-01`, `N-SEM-01..05`, and `N-RUN-01` respectively test equivalent
projection preservation, semantic invalidation for owner/material/validation/
receipt/closeout changes, and empirical command failure. None has been executed
([fixture specification](synthesis-revised.md#body-war-fixture-set);
[non-vacuity acceptance](reviews/non-vacuity.md#measurable-acceptance)).

### Serialized fixture contracts

The following YAML is a proposed fixture specification, not an execution
receipt. Every `frozenInputRefs` entry resolves into `frozenInputs`; the resolved
path, JSON Pointer selector, and SHA-256 triple is immutable. A fault's
`bindingRef` resolves the exact input and selector it alters. `allowedWrites`
means writes permitted during the expected fixture result, not fixture setup.

```yaml
schemaVersion: arcanum.research-fixture-contract.v0.1
evidenceStatusEnum: [proposed-unverified-unexecuted]
fixtureContractRequired:
  - fixtureId
  - evidenceStatus
  - frozenInputRefs
  - injectedFault
  - firstKnowableStage
  - firstDetectedGate
  - expectedOwner
  - terminalCode
  - expectedReceiptCount
  - allowedWrites
  - forbiddenTransitions
constraints:
  injectedFaultCardinality: 0..1
  frozenInputResolution: frozenInputRefs -> frozenInputs[id]
  noImplicitFixtureExecution: true

frozenInputs:
  BW-HANDOFF:
    path: projects/body-war/development/invoke-runs/20260730T062453Z-business-ontology-atlas-arrows/refreshes/20260730T090724Z-swu-bwaa-001-material-admission/TASK-SESSION-HANDOFF.json
    selector: ""
    sha256: 5ece8a61bdc2fc367051a82170eaf7f5d49234c715a159a0bad03823eb50e41e
  BW-ADMISSION:
    path: projects/body-war/development/invoke-runs/20260730T062453Z-business-ontology-atlas-arrows/refreshes/20260730T090724Z-swu-bwaa-001-material-admission/TASK-SESSION-ADMISSION-PROBE-RECEIPT.json
    selector: ""
    sha256: b57852262772e8c2fc707356028a0915a64f391be0ada94aa6ee9f14890fee5d
  BW-PACKAGE:
    path: projects/body-war/development/invoke-runs/20260730T062453Z-business-ontology-atlas-arrows/refreshes/20260730T090724Z-swu-bwaa-001-material-admission/material/MATERIAL-PACKAGE.json
    selector: ""
    sha256: a99e33d185e87896515309ee73424d8d58af4a4c5998d02112764c9ec3b3045b
  BW-RECEIPT:
    path: projects/body-war/development/invoke-runs/20260730T062453Z-business-ontology-atlas-arrows/refreshes/20260730T090724Z-swu-bwaa-001-material-admission/material/MATERIAL-RECEIPT.json
    selector: ""
    sha256: 56a77500e3692a369a421c246c59fa983d7f3fea6f89edee44bb546e9e679e95
  BW-SCHEMA:
    path: .agents/skills/invoke/schemas/material-package-receipt.schema.json
    selector: ""
    sha256: 2c4ef7c0529f419278a3af530783383d05ccf8e144a40e895f26c2c2d6b77b6b
  BW-CONTEXT:
    path: projects/body-war/development/invoke-runs/20260730T062453Z-business-ontology-atlas-arrows/refreshes/20260730T090724Z-swu-bwaa-001-material-admission/CONTEXT-PACK.json
    selector: ""
    sha256: 6b54fa2b3310b5685087904de8b570b90c953dffeb36ad2cb03d71cf443fba0d
  BW-CLOSEOUT:
    path: projects/body-war/development/invoke-runs/20260730T062453Z-business-ontology-atlas-arrows/refreshes/20260730T090724Z-swu-bwaa-001-material-admission/CLOSEOUT-OWNER-CONTRACT.json
    selector: ""
    sha256: 357b45c72cac995d167de307926aa3d633fd53bdaa77775c9dadcd6d852e4b34
  BW-PACKAGE-REF:
    path: projects/body-war/development/invoke-runs/20260730T062453Z-business-ontology-atlas-arrows/refreshes/20260730T090724Z-swu-bwaa-001-material-admission/TASK-SESSION-HANDOFF.json
    selector: /material/package
    sha256: 5ece8a61bdc2fc367051a82170eaf7f5d49234c715a159a0bad03823eb50e41e
  BW-PRODUCER-OWNER:
    path: projects/body-war/development/invoke-runs/20260730T062453Z-business-ontology-atlas-arrows/refreshes/20260730T090724Z-swu-bwaa-001-material-admission/material/MATERIAL-PACKAGE.json
    selector: /lifecycle_owner
    sha256: a99e33d185e87896515309ee73424d8d58af4a4c5998d02112764c9ec3b3045b
  BW-PRODUCER-RECEIPT:
    path: projects/body-war/development/invoke-runs/20260730T062453Z-business-ontology-atlas-arrows/refreshes/20260730T090724Z-swu-bwaa-001-material-admission/TASK-SESSION-HANDOFF.json
    selector: /material/receipt
    sha256: 5ece8a61bdc2fc367051a82170eaf7f5d49234c715a159a0bad03823eb50e41e
  BW-SCHEMA-BINDING:
    path: projects/body-war/development/invoke-runs/20260730T062453Z-business-ontology-atlas-arrows/refreshes/20260730T090724Z-swu-bwaa-001-material-admission/TASK-SESSION-HANDOFF.json
    selector: /material/producer_receipt_schema
    sha256: 5ece8a61bdc2fc367051a82170eaf7f5d49234c715a159a0bad03823eb50e41e
  BW-TARGET-INVENTORY:
    path: projects/body-war/development/invoke-runs/20260730T062453Z-business-ontology-atlas-arrows/refreshes/20260730T090724Z-swu-bwaa-001-material-admission/material/MATERIAL-PACKAGE.json
    selector: /target_inventory
    sha256: a99e33d185e87896515309ee73424d8d58af4a4c5998d02112764c9ec3b3045b
  BW-TARGET-DIGESTS:
    path: projects/body-war/development/invoke-runs/20260730T062453Z-business-ontology-atlas-arrows/refreshes/20260730T090724Z-swu-bwaa-001-material-admission/material/MATERIAL-PACKAGE.json
    selector: /changes
    sha256: a99e33d185e87896515309ee73424d8d58af4a4c5998d02112764c9ec3b3045b
    resolvedTargets:
      - path: projects/body-war/ontology/business/scripts/view-atlas-projection.mjs
        stagedSha256: 2552fcee789edba182d86ce906ea20214c4f9fa43a71095094da5e2f3c23e1e6
      - path: projects/body-war/ontology/business/scripts/validate-view-atlas.mjs
        stagedSha256: 0479bb0c7f4c3fa25e77f2127a972c87f71b08844304ef7b6e22456875a007bd
      - path: projects/body-war/ontology/business/tests/business-view-atlas-projection.test.mjs
        stagedSha256: 3e4f1a8f26d6f4bf0067460b2ca0f262e53b3ab19282cb13289a1d02c622aadd
  BW-VALIDATION:
    path: projects/body-war/development/invoke-runs/20260730T062453Z-business-ontology-atlas-arrows/refreshes/20260730T090724Z-swu-bwaa-001-material-admission/TASK-SESSION-HANDOFF.json
    selector: /validation_commands
    sha256: 5ece8a61bdc2fc367051a82170eaf7f5d49234c715a159a0bad03823eb50e41e
  BW-EXECUTION-OUTPUTS:
    path: projects/body-war/development/invoke-runs/20260730T062453Z-business-ontology-atlas-arrows/refreshes/20260730T090724Z-swu-bwaa-001-material-admission/TASK-SESSION-HANDOFF.json
    selector: /execution_outputs
    sha256: 5ece8a61bdc2fc367051a82170eaf7f5d49234c715a159a0bad03823eb50e41e
  BW-CANONICAL-DIGEST:
    path: projects/body-war/development/invoke-runs/20260730T062453Z-business-ontology-atlas-arrows/refreshes/20260730T090724Z-swu-bwaa-001-material-admission/TASK-SESSION-HANDOFF.json
    selector: /material/canonical_package_digest
    sha256: 5ece8a61bdc2fc367051a82170eaf7f5d49234c715a159a0bad03823eb50e41e
    value: 905e2b76c704f0ed114b5601ae230e7fc8f3e812c68851bcd8b8164313e49e13

writeSets:
  BW-SWU-001:
    - projects/body-war/ontology/business/scripts/view-atlas-projection.mjs
    - projects/body-war/ontology/business/scripts/validate-view-atlas.mjs
    - projects/body-war/ontology/business/tests/business-view-atlas-projection.test.mjs
    - projects/body-war/ontology/business/receipts/view-atlas-coverage-receipt.json
    - projects/body-war/development/invoke-runs/20260730T062453Z-business-ontology-atlas-arrows/work-pack/closeout/SWU-BWAA-001.receipt.json

fixtureDefaults:
  evidenceStatus: proposed-unverified-unexecuted
  frozenInputRefs: [BW-HANDOFF, BW-ADMISSION, BW-PACKAGE, BW-RECEIPT,
    BW-SCHEMA, BW-CONTEXT, BW-CLOSEOUT, BW-TARGET-DIGESTS]

fixtures:
  - fixtureId: PBW-01-body-war-swu-001-stable
    evidenceStatus: proposed-unverified-unexecuted
    frozenInputRefs: [BW-HANDOFF, BW-ADMISSION, BW-PACKAGE, BW-RECEIPT,
      BW-SCHEMA, BW-CONTEXT, BW-CLOSEOUT, BW-TARGET-DIGESTS,
      BW-VALIDATION, BW-EXECUTION-OUTPUTS, BW-CANONICAL-DIGEST]
    injectedFault: null
    firstKnowableStage: work-pack-readiness-audit
    firstDetectedGate: work-pack-readiness-audit-pass
    expectedOwner: task-session-until-blocker
    terminalCode: CHAIN_COMPLETE
    expectedReceiptCount: 3
    allowedWrites: {ref: writeSets.BW-SWU-001}
    forbiddenTransitions: [generic-refresh-repair, frontier-expansion,
      second-task-session-request, unverified-successor-selection]

  - fixtureId: NBW-01-package-ref
    evidenceStatus: proposed-unverified-unexecuted
    frozenInputRefs: [BW-HANDOFF, BW-PACKAGE-REF, BW-TARGET-DIGESTS]
    injectedFault: {bindingRef: BW-PACKAGE-REF, operation: remove}
    firstKnowableStage: work-pack-readiness-audit-phases-1-4
    firstDetectedGate: work-pack-readiness-audit-phases-1-4
    expectedOwner: work-pack-readiness-audit
    terminalCode: MATERIAL_PACKAGE_REF_MISSING
    expectedReceiptCount: 1
    allowedWrites: []
    forbiddenTransitions: &noTaskSession [task-session-until-blocker-request,
      task-session-request, task-session-selector, product-write]
  - fixtureId: NBW-02-producer-owner
    evidenceStatus: proposed-unverified-unexecuted
    frozenInputRefs: [BW-HANDOFF, BW-PRODUCER-OWNER, BW-PACKAGE]
    injectedFault: {bindingRef: BW-PRODUCER-OWNER, operation: remove}
    firstKnowableStage: work-pack-readiness-audit-phases-1-4
    firstDetectedGate: work-pack-readiness-audit-phases-1-4
    expectedOwner: work-pack-readiness-audit
    terminalCode: MATERIAL_PRODUCER_OWNER_UNRESOLVED
    expectedReceiptCount: 1
    allowedWrites: []
    forbiddenTransitions: *noTaskSession
  - fixtureId: NBW-03-producer-receipt
    evidenceStatus: proposed-unverified-unexecuted
    frozenInputRefs: [BW-HANDOFF, BW-PRODUCER-RECEIPT, BW-RECEIPT]
    injectedFault: {bindingRef: BW-PRODUCER-RECEIPT, operation: remove}
    firstKnowableStage: work-pack-readiness-audit-phases-1-4
    firstDetectedGate: work-pack-readiness-audit-phases-1-4
    expectedOwner: work-pack-readiness-audit
    terminalCode: MATERIAL_PRODUCER_RECEIPT_MISSING
    expectedReceiptCount: 1
    allowedWrites: []
    forbiddenTransitions: *noTaskSession
  - fixtureId: NBW-04-schema-binding
    evidenceStatus: proposed-unverified-unexecuted
    frozenInputRefs: [BW-HANDOFF, BW-SCHEMA-BINDING, BW-SCHEMA]
    injectedFault: {bindingRef: BW-SCHEMA-BINDING, operation: remove}
    firstKnowableStage: work-pack-readiness-audit-phases-1-4
    firstDetectedGate: work-pack-readiness-audit-phases-1-4
    expectedOwner: work-pack-readiness-audit
    terminalCode: MATERIAL_RECEIPT_SCHEMA_MISSING
    expectedReceiptCount: 1
    allowedWrites: []
    forbiddenTransitions: *noTaskSession
  - fixtureId: NBW-05-target-inventory
    evidenceStatus: proposed-unverified-unexecuted
    frozenInputRefs: [BW-PACKAGE, BW-TARGET-INVENTORY, BW-TARGET-DIGESTS]
    injectedFault: {bindingRef: BW-TARGET-INVENTORY, operation: remove}
    firstKnowableStage: work-pack-readiness-audit
    firstDetectedGate: work-pack-readiness-audit
    expectedOwner: work-pack-readiness-audit
    terminalCode: TARGET_INVENTORY_MISSING
    expectedReceiptCount: 1
    allowedWrites: []
    forbiddenTransitions: *noTaskSession
  - fixtureId: NBW-06-byte-baseline
    evidenceStatus: proposed-unverified-unexecuted
    frozenInputRefs: [BW-PACKAGE, BW-TARGET-DIGESTS, BW-CANONICAL-DIGEST]
    injectedFault: {bindingRef: BW-TARGET-DIGESTS, operation: remove-baselines}
    firstKnowableStage: work-pack-readiness-audit
    firstDetectedGate: work-pack-readiness-audit
    expectedOwner: work-pack-readiness-audit
    terminalCode: EXECUTION_BYTE_BASELINE_MISSING
    expectedReceiptCount: 1
    allowedWrites: []
    forbiddenTransitions: *noTaskSession
  - fixtureId: NBW-07-delta-policy
    evidenceStatus: proposed-unverified-unexecuted
    frozenInputRefs: [BW-HANDOFF, BW-CLOSEOUT, BW-TARGET-DIGESTS]
    injectedFault: {bindingRef: BW-CLOSEOUT, operation: remove-allowed-delta-policy}
    firstKnowableStage: work-pack-readiness-audit
    firstDetectedGate: work-pack-readiness-audit
    expectedOwner: work-pack-readiness-audit
    terminalCode: ALLOWED_DELTA_POLICY_MISSING
    expectedReceiptCount: 1
    allowedWrites: []
    forbiddenTransitions: *noTaskSession
  - fixtureId: NBW-08-closeout-receipt
    evidenceStatus: proposed-unverified-unexecuted
    frozenInputRefs: [BW-HANDOFF, BW-CLOSEOUT, BW-EXECUTION-OUTPUTS]
    injectedFault: {bindingRef: BW-CLOSEOUT, operation: remove}
    firstKnowableStage: work-pack-readiness-audit
    firstDetectedGate: work-pack-readiness-audit
    expectedOwner: work-pack-readiness-audit
    terminalCode: CLOSEOUT_RECEIPT_CONTRACT_MISSING
    expectedReceiptCount: 1
    allowedWrites: []
    forbiddenTransitions: *noTaskSession
  - fixtureId: NBW-09-successor-binding
    evidenceStatus: proposed-unverified-unexecuted
    frozenInputRefs: [BW-HANDOFF, BW-CONTEXT, BW-CLOSEOUT]
    injectedFault: {bindingRef: BW-CONTEXT, operation: make-successor-non-unique}
    firstKnowableStage: work-pack-readiness-audit-graph
    firstDetectedGate: work-pack-readiness-audit-graph
    expectedOwner: work-pack-readiness-audit
    terminalCode: CANONICAL_SUCCESSOR_NON_UNIQUE
    expectedReceiptCount: 1
    allowedWrites: []
    forbiddenTransitions: *noTaskSession
  - fixtureId: NBW-10-preroute-material-digest
    evidenceStatus: proposed-unverified-unexecuted
    frozenInputRefs: [BW-HANDOFF, BW-PACKAGE, BW-CANONICAL-DIGEST,
      BW-TARGET-DIGESTS]
    injectedFault: {bindingRef: BW-CANONICAL-DIGEST, operation: replace-with-mismatch}
    firstKnowableStage: work-pack-readiness-audit-snapshot-recheck
    firstDetectedGate: work-pack-readiness-audit-snapshot-recheck
    expectedOwner: work-pack-readiness-audit
    terminalCode: PREROUTE_MATERIAL_DIGEST_MISMATCH
    expectedReceiptCount: 1
    allowedWrites: []
    forbiddenTransitions: *noTaskSession
  - fixtureId: NBW-11-post-approval-concurrent-drift
    evidenceStatus: proposed-unverified-unexecuted
    frozenInputRefs: [BW-HANDOFF, BW-PACKAGE, BW-TARGET-DIGESTS,
      BW-CANONICAL-DIGEST]
    injectedFault: {bindingRef: BW-TARGET-DIGESTS, operation: mutate-one-target-after-approval}
    firstKnowableStage: task-session-immediately-before-write
    firstDetectedGate: task-session-immediately-before-write
    expectedOwner: task-session
    terminalCode: POST_APPROVAL_BYTE_DRIFT
    expectedReceiptCount: 2
    allowedWrites: []
    forbiddenTransitions: [product-overwrite, staged-byte-adoption,
      unattributed-write-claim, second-task-session-request]

  - fixtureId: P-PROJ-01
    evidenceStatus: proposed-unverified-unexecuted
    frozenInputRefs: [BW-HANDOFF, BW-PACKAGE, BW-CONTEXT,
      BW-CANONICAL-DIGEST]
    injectedFault: null
    firstKnowableStage: work-pack-readiness-audit-projection-equivalence
    firstDetectedGate: work-pack-readiness-audit-projection-equivalence
    expectedOwner: work-pack-readiness-audit
    terminalCode: PROJECTION_EQUIVALENCE_PRESERVED
    expectedReceiptCount: 2
    allowedWrites: []
    forbiddenTransitions: [epoch-invalidation, canonical-source-mutation,
      task-session-request]
  - fixtureId: N-SEM-01-owner
    evidenceStatus: proposed-unverified-unexecuted
    frozenInputRefs: [BW-PACKAGE, BW-PRODUCER-OWNER, BW-CANONICAL-DIGEST]
    injectedFault: {bindingRef: BW-PRODUCER-OWNER, operation: replace-owner}
    firstKnowableStage: work-pack-readiness-audit-semantic-recheck
    firstDetectedGate: work-pack-readiness-audit-semantic-recheck
    expectedOwner: work-pack-readiness-audit
    terminalCode: EPOCH_INVALIDATED_OWNER_CHANGE
    expectedReceiptCount: 1
    allowedWrites: []
    forbiddenTransitions: *noTaskSession
  - fixtureId: N-SEM-02-material
    evidenceStatus: proposed-unverified-unexecuted
    frozenInputRefs: [BW-PACKAGE, BW-CANONICAL-DIGEST, BW-TARGET-DIGESTS]
    injectedFault: {bindingRef: BW-CANONICAL-DIGEST, operation: replace-material-digest}
    firstKnowableStage: work-pack-readiness-audit-semantic-recheck
    firstDetectedGate: work-pack-readiness-audit-semantic-recheck
    expectedOwner: work-pack-readiness-audit
    terminalCode: EPOCH_INVALIDATED_MATERIAL_CHANGE
    expectedReceiptCount: 1
    allowedWrites: []
    forbiddenTransitions: *noTaskSession
  - fixtureId: N-SEM-03-validation
    evidenceStatus: proposed-unverified-unexecuted
    frozenInputRefs: [BW-HANDOFF, BW-VALIDATION, BW-CANONICAL-DIGEST]
    injectedFault: {bindingRef: BW-VALIDATION, operation: replace-command-semantics}
    firstKnowableStage: work-pack-readiness-audit-semantic-recheck
    firstDetectedGate: work-pack-readiness-audit-semantic-recheck
    expectedOwner: work-pack-readiness-audit
    terminalCode: EPOCH_INVALIDATED_VALIDATION_CHANGE
    expectedReceiptCount: 1
    allowedWrites: []
    forbiddenTransitions: *noTaskSession
  - fixtureId: N-SEM-04-receipt
    evidenceStatus: proposed-unverified-unexecuted
    frozenInputRefs: [BW-HANDOFF, BW-RECEIPT, BW-SCHEMA-BINDING, BW-SCHEMA]
    injectedFault: {bindingRef: BW-SCHEMA-BINDING, operation: replace-receipt-semantics}
    firstKnowableStage: work-pack-readiness-audit-semantic-recheck
    firstDetectedGate: work-pack-readiness-audit-semantic-recheck
    expectedOwner: work-pack-readiness-audit
    terminalCode: EPOCH_INVALIDATED_RECEIPT_CHANGE
    expectedReceiptCount: 1
    allowedWrites: []
    forbiddenTransitions: *noTaskSession
  - fixtureId: N-SEM-05-closeout
    evidenceStatus: proposed-unverified-unexecuted
    frozenInputRefs: [BW-HANDOFF, BW-CLOSEOUT, BW-EXECUTION-OUTPUTS]
    injectedFault: {bindingRef: BW-CLOSEOUT, operation: replace-closeout-semantics}
    firstKnowableStage: work-pack-readiness-audit-semantic-recheck
    firstDetectedGate: work-pack-readiness-audit-semantic-recheck
    expectedOwner: work-pack-readiness-audit
    terminalCode: EPOCH_INVALIDATED_CLOSEOUT_CHANGE
    expectedReceiptCount: 1
    allowedWrites: []
    forbiddenTransitions: *noTaskSession
  - fixtureId: N-RUN-01
    evidenceStatus: proposed-unverified-unexecuted
    frozenInputRefs: [BW-HANDOFF, BW-ADMISSION, BW-PACKAGE,
      BW-VALIDATION, BW-TARGET-DIGESTS]
    injectedFault: {bindingRef: BW-VALIDATION, operation: force-command-nonzero}
    firstKnowableStage: task-session-command-execution
    firstDetectedGate: task-session-command-execution
    expectedOwner: task-session
    terminalCode: EMPIRICAL_COMMAND_FAILURE
    expectedReceiptCount: 2
    allowedWrites: {ref: writeSets.BW-SWU-001}
    forbiddenTransitions: [chain-complete, generic-refresh-repair,
      runtime-failure-reclassified-as-preflight]
```

Receipt counts are assertions over fixture output: one WPRA block/invalidation
receipt for pre-route negatives; a Task Session terminal plus outer-chain block
receipt for runtime negatives; a preservation plus audit receipt for
`P-PROJ-01`; and Task Session terminal, joined closeout, and chain completion
receipts for `PBW-01`. Those artifacts do not exist yet. The frozen input
digests above are observed source bindings, while every expected fixture result
remains `proposed-unverified-unexecuted`.

## Required five-column verdict matrix

| candidate | owner (precedent) | witnessed? (non-vacuity) | sound? (definitional) | verdict |
|---|---|---|---|---|
| Harden Invoke Plan alone | Invoke Plan; existing authoring owner | No; Body War Plan passed before exact material closure | No as a sufficient mechanism; retain stronger exit contracts | **KILL** |
| Add duplicate closure stage | Define/Design, Structured Interview, Decision Gate already own closure | No evidence that a renamed stage moves first detection | No; duplicates existing owners | **KILL** |
| Standalone admission compiler/materializer | WPRA already owns normalization/audit; exact SWU producer owns bytes | Initial synthesis proposed it; no deployed witness | No; duplicates WPRA and abstracts byte ownership | **KILL** |
| Generic Refresh repair/admission lane | Invoke Refresh owns synchronization/closeout | Yes, negatively: projection-only Refresh changed no blocker/executable evidence | No as normal admission path | **KILL** |
| WPRA internal admission projection | WPRA phases 1–4; Bazel/LLVM derived-fact precedent | Proposed Body War fixture would witness pre-route rejection; not yet executed | Yes only with `authorityEffect: none`, exact refs, and no repair/material creation | **PASS, conditional** |
| Approved finite-frontier execution | Task Session Until Blocker; Temporal replay/version precedent | Existing chain proves fail-closed coordination, but approved-epoch replay is not yet executed | Yes if cursor, invalidation, unique successor, closeout join, and one-SWU sessions remain | **PASS, conditional** |

The matrix has six candidate rows. Its load-bearing verdicts are bound to the
precedent review, non-vacuity review, definitional repair, and successful
recheck ([precedent](reviews/precedent.md#verdict-matrix);
[non-vacuity](reviews/non-vacuity.md#candidate-verdicts);
[definitional](reviews/definitional.md#blockers);
[recheck](reviews/definitional-recheck.md)).

## Unresolved decisions and evidence limits

Implementation remains blocked on a confirmed capability-design/migration
route, exact public schema/version ownership, named validator owners for every
binding, the approval owner/risk and budget policy, allowed WPRA flag classes,
cursor persistence details, closeout `NO_OP` semantics, compensation metadata
scope, and fixture execution. The research does not prove runtime success,
deployment, promotion, publication, or production readiness. It proves only
that the corrected architecture is evidence-closed enough to recommend a
bounded Spellcraft design route, with an explicit
`frozen-input-contractual-readiness` ceiling
([evidence closure](receipts/evidence-closure.json);
[revised synthesis](synthesis-revised.md)).

Started: `2026-07-30T17:32:32Z`  
Finished: `2026-07-30T17:40:08Z`
