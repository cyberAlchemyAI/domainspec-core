# Invoke one-shot workflow synthesis

## Evidence status

- Status: PASS
- Validation: PASS
- Blockers: none for synthesis
- Implementation remains gated on an approved capability-design/migration route
  and fixtures.
- `invoke validate` is deferred and is not current enforcement.

## 1. Plain-language root cause

The workflow bounces because the authored Plan and the object Task Session
actually admits are not yet the same exact, versioned thing.

Invoke can validly finish Plan while executable material, runtime-admission
data, receipt semantics, closeout baselines, or continuation projections remain
absent or unevaluated. Task Session is then the first component that compares
those details with the live mutation boundary. Predictable contract defects are
consequently detected one owner too late. Generic Refresh has become an
overloaded recovery lane for three unlike operations—planning repair,
projection synchronization, and executable handoff materialization—so a
sequence can contain many locally valid transitions without advancing product
execution. [Explorer local: Plain-language finding;
`arcanum/spells/invoke/README.md:24-26,51-70,95-107`;
`arcanum/arcana/task-session/SKILL.md:33-39,100-111`]

This is not evidence that Task Session is too strict. Its digest, admission, and
one-SWU boundaries protected safety in both Body War bounces. Nor does it
justify claiming that compilation can predict concurrent drift, command
failures, unavailable tools, or other empirical runtime facts. [Explorer local:
Strict classification; Body War timestamped owner-hop graph; Explorer
precedents: Transferable invariants 3-5]

## 2. Current and target lifecycle

Current:

```text
Invoke Define → Design → Plan
                         │
                         ├─ locally valid authored plan
                         │  runtime readiness may be unevaluated
                         ▼
                Task Session preflight
                         │
          deterministic gap first detected here
                         ▼
                  generic Refresh
        ┌────────────────┼────────────────┐
 planning repair   projection sync   handoff/material work
        └────────────────┼────────────────┘
                         ▼
                Task Session retry
                         │
               empirical runtime residue
                  or bounded completion
```

[Explorer local: timestamped Body War graph; Explorer protocol: Root conclusion]

Target:

```text
Invoke Define ── objective closure
      ▼
Invoke Design ── concern, owner, dependency closure
      ▼
Invoke Plan ── executable decomposition and contract authoring
      ▼
Execution-Admission Compiler ── normalize/reference-check; choose nothing
      ▼
Work Pack Readiness Audit ── immutable snapshot and adversarial proof
      ▼
Human/Decision Gate ── approve exact epoch, frontier, risk and budget
      ▼
Task Session Until Blocker ── durable finite-frontier coordinator
      ├─ fresh Task Session(SWU-1) → joined closeout
      ├─ fresh Task Session(SWU-2) → joined closeout
      └─ fresh Task Session(SWU-n) → joined closeout
      ▼
terminal chain receipt
```

Refresh remains the receipt-bound owner for admitted lifecycle
bookkeeping/closeout and genuine drift synchronization. It neither repairs the
Plan in the normal path nor launches the next SWU. [Explorer protocol: Target
protocol 1-10; Explorer precedents: Transferable invariants 1-5]

## 3. Blocker first-knowable versus first-detected matrix

| Blocker | First knowable | First detected | Correct owner/gate |
|---|---|---|---|
| Body War SWU-001 material package, producer receipt/schema, closeout contract absent | Plan/handoff compilation after SWU and routed-mutation profile were known | First Task Session, 09:01:59Z | Plan authors requirements; material producer supplies package; compiler/audit rejects incomplete binding before route |
| Continuation omitted Context Builder | Initial continuation emission | Operator projection-sync | Invoke continuation projection validator |
| Projection-only edit invalidated byte-bound closeout baseline | When mutable projection was selected as semantic join input | After projection sync | Semantic-digest classifier/epoch gate |
| OEW lock ownership absent | Work-pack ownership closure | `013B` attempt 001 | Design/Plan ownership closure |
| OEW build order incomplete after `--ignore-scripts` | Command-graph compilation/dry run | `013B` attempt 002 | Plan plus deterministic audit |
| OEW 48 strict TypeScript errors | Exact immutable-overlay build witness | `013B` attempt 003 | Pre-admission build witness routes ordinary product defect to source owner |
| Body War concurrent three-target drift | Event itself unknowable beforehand; drift policy knowable | Immediately-before-write digest recheck, 16:45:38Z | External/unknown writer is residue owner; Task Session correctly detects and blocks |
| Future command/tool/environment/browser failure | Only when executed unless a declared prerequisite can be checked | Runtime | Task Session terminal residue |

[Explorer local: Blocker matrix; Strict classification; OEW runtime rebuild
findings selectors cited by explorer local]

The decisive distinction is deterministic knowability, not whether a failure
feels “technical.” A compiler/build error reproducible from frozen inputs is
preflight-discoverable; a future concurrent write event is not.

## 4. Candidate verdicts

| Candidate | Verdict | Boundary |
|---|---|---|
| Harden Plan | Required but insufficient | Require compiler-ready SWU, write, validation, receipt, closeout, material-reference, and successor fields. Do not make Plan inspect live runtime state, freeze epochs, or execute proof. |
| Add closure | Harden existing closure owners; reject a duplicate stage | Define/Interrogation own objective and questions; Design owns concern/owner/dependency closure; Decision Gate owns consequential choices. Strengthen their exits. |
| Add execution-admission compiler/materializer | Recommend, with a necessary split | The compiler may materialize only the normalized derived manifest/configuration. It must not synthesize missing product post-images or repair source artifacts. Executable material bytes remain owned by the declared material producer and must be referenced before compilation/audit. |
| Retain generic Refresh | Retain capability, narrow normal-path use | Keep genuine evidence-backed synchronization and receipt-bound closeout. Reject generic Refresh as automatic Plan repair, admission discovery, execution, or successor routing. |

The explorer wording conflicts over “materializer”: local forensics says a
materializer produced the Body War staged bytes, whereas the formal protocol
says the new compiler/materializer only normalizes and never repairs.
Resolution: distinguish `material producer` from `admission-manifest
materializer`; encode both owners explicitly. This preserves exact Body War
requirements without granting the compiler product authority. [Explorer local:
earliest deterministic gate and 09:15 materialization; Explorer protocol:
Target protocol 5 and Candidate comparison; Explorer precedents: Bazel and LLVM
transfer boundaries]

## 5. Normalized objective-execution manifest

```yaml
schemaVersion:
manifestId:

objective:
  statement:
  deliveryBoundary:
  acceptanceObligations:
    - {id, claim, evidenceRequired, artifactRef, validatorOwner}
  constraints: []
  nonGoals: []
  authorityClass:
  publicationClass:

sourceClosure:
  refs:
    - {path, selectors: [], sha256, size, authorityOwner, semanticClass}
  defineReceipt:
  designScopeManifest:
  designDenominatorReceipt:
  designSelectionResult:
  planReceipt:

questionClosure:
  questions:
    - {id, owner, status: resolved|deferred-nonblocking|blocked, artifactRef}
decisionClosure:
  decisions:
    - {id, consequence, reversibility, optionsReceipt, decisionRef, status}

ownership:
  concerns:
    - {id, accountableOwner, contributingOwners: [], artifactOwner, validatorOwner}
  lifecycleOwners:
    objectiveAuthor:
    designAuthor:
    planAuthor:
    materialProducer:
    manifestCompiler:
    readinessAuditor:
    approvalOwner:
    outerRunner:
    unitExecutor:
    closeoutOwner:
    promotionOwner:

graph:
  units:
    - {id, parentTask, primaryBehavior, dependencies: [], successor, closureKind}
  frontier: []

executionContracts:
  - unitId:
    taskClass:
    argv: []
    cwd:
    environment: {}
    timeout:
    expectedExit:
    riskClass:
    materialWrites: []
    executionOutputs: []
    allowedWrites: []
    immutablePaths: []
    validation: []
    attemptPolicy:
      {identity, collision, retention, successTeardown, failureTeardown}
    materialPackageRef:
      {producerOwner, receiptRef, schemaRef, sha256}
    dependencyReceipts: []

receiptContracts:
  terminalSchema:
  semanticValidator:
  expectedReceipts:
    - {unitId, owner, path, semanticAssertions: []}

closeoutContracts:
  - unitId:
    targetInventory: []
    baselines: [{path, sha256, semanticDigest}]
    allowedDeltaClasses: []
    ownerValidation: []
    expectedOwnerReceipt:
    successorPolicy:

runtimeBinding:
  taskSessionRequestSchema:
  runtimeIdentityPolicy:
  executionMode:

readiness:
  planContractStatus: pass|flag|block
  runtimeAdmissionStatus: pass|block
  receiptSemanticStatus: pass|block
  frontierStatus: pass|block
  snapshotStatus: pass|block
  verdict: pass|flag|block
  blockers: []

epoch:
  epochId:
  manifestDigest:
  canonicalSemanticDigest:
  snapshotDigest:
  approvedFrontier: []
  runBudget:
  approvalRef:
  status: draft|compiled|audited|approved|running|complete|invalidated|blocked

invalidation:
  semanticInputs: []
  preservedProjectionClasses: []
  lastCheckedAt:
  reason:

continuity:
  cursor:
  completedUnits: []
  joinedCloseouts: []
  nextDeclaredSuccessor:
  blockerFingerprint:

residue:
  empiricalRuntimeUnknowns: []
  noncritical: []
  compensationOrRepairOwners: []
```

Owner transitions are exactly:

```text
Define → Design → Plan → Compiler → Readiness Audit → Human Approval
→ Outer Runner → Task Session → Refresh Closeout → Outer Runner
→ terminal closeout / separately gated promotion
```

No transition transfers canonical authority merely because it consumes an
artifact. [Explorer protocol: Normalized Objective-Execution Manifest;
Invariants; Explorer precedents: LLVM invalidation, Bazel action graph, ReqIF
typed relations]

## 6. Plan-epoch and semantic invalidation protocol

1. Compiler binds all authoritative source selectors, digests, sizes, owners,
   manifest digest, semantic digest, and finite frontier.
2. Audit re-reads the snapshot, checks graph/write/command/receipt/closeout
   semantics, and preserves separate plan-contract and runtime-admission
   verdicts.
3. Human approval binds exact manifest digest, source snapshot, frontier,
   runtime identity, risk ceiling, and budget.
4. Before every SWU admission and immediately before its first write, re-read
   semantic inputs and recompute digests.
5. Invalidate on changes to objective/acceptance, design dispositions,
   accountable owners, dependency/successor edges, SWU boundaries, write
   partitions, material references, validation/receipt semantics, closeout
   targets/baselines/delta policy, runtime schema/identity, authority/publication
   class, frontier, or budget.
6. Do not invalidate for timestamps, observability-only fields, or regenerated
   projections whose canonical semantic digest is provably identical.
7. On invalidation, stop before mutation; route to the earliest owning stage,
   generate a new epoch, re-audit, and reapprove.
8. Never attach newly discovered work to a running epoch.

This applies Terraform-style stale-plan rejection, LLVM-style explicit
preservation/invalidation, Bazel-style derived keys, and Temporal-style
version-bound replay without importing a monolithic runtime. [Explorer
precedents: Terraform, LLVM, Bazel, Temporal rows; Explorer protocol: Semantic
invalidation]

## 7. One-shot outer work-pack algorithm

```text
require approved epoch E with finite frontier F
cursor := epoch-start
completed := {}

while an uncompleted unit exists:
  verify E remains approved and semantic/snapshot digests match
  choose only the single dependency-ready successor declared by the manifest
  if zero unexpectedly or more than one: BLOCK
  if successor not in F: BLOCK FRONTIER_EXPANSION

  launch one fresh Task Session for exactly that SWU
  Task Session rechecks admission and immediately-before-write digests
  Task Session executes, validates, and emits one terminal unit receipt

  if terminal BLOCK/FAIL:
    preserve residue and stop; do not reinterpret it as planning failure
  join exact Refresh closeout receipt or NO_OP proof
  if closeout join fails: BLOCK

  derive new continuity cursor from unit receipt + closeout + epoch
  if cursor repeats or blocker fingerprint is unchanged across a return: BLOCK CURSOR_REPEAT
  record unit complete and continue only to its one declared ready successor

emit terminal chain receipt when all captured units are complete
do not promote automatically
```

Each SWU therefore remains a separate Task Session with separate admission,
mutation boundary, validation, receipt, and closeout. The outer loop coordinates
durable progress; it does not produce a combined execution receipt. [Explorer
protocol: Target protocol 8-10; Invariants; Explorer precedents: Temporal,
Sagas, Transferable invariant 5]

## 8. Capability ownership and migration map

| Concern | Existing/future owner | Migration |
|---|---|---|
| Objective and ambiguity | Invoke Define + Interrogation | Strengthen exit receipt |
| Consequential choice/approval | Decision Gate/human | Bind decision and epoch digests |
| Concern denominator, owners, dependencies | Invoke Design | Require total typed ownership/edges |
| SWUs, commands, writes, validation, closeout contracts | Invoke Plan | Emit compiler-ready references |
| Product/staged executable material | Declared material producer | Emit package/schema/receipt; never delegate silently to compiler |
| Normalized manifest | New admission compiler | Public project-agnostic schema; read source, write derived artifact only |
| Immutable frontier proof | Work Pack Readiness Audit | Consume manifest; remain read-only |
| Finite-frontier coordination | Task Session Until Blocker | Bind approved epoch and cursor |
| One-unit mutation | Task Session | Preserve exact admission and one-SWU ceiling |
| Bookkeeping/closeout synchronization | Invoke Refresh | Restrict to approved deltas and genuine evidence-backed sync |
| Promotion | Goal/Craft/human gate where applicable | Remains separate |
| Observability | Existing observability surfaces | Add first-knowable/detected, invalidation, return, cursor, unit metrics |

The manifest schema may be public and project-agnostic in Arcanum; private
DomainSpec/Saturn prose and `cyberAlchemy-v2` authority vocabulary must not be
copied into it. [Explorer protocol: Migration boundaries 1-8; Explorer
precedents: root classification “build-from-owned”]

## 9. Deterministic replay fixtures, including Body War

Positive:

- `P1-linear-two-swu`: closed decisions/owners; two-node DAG; exact
  command/runtime/write/material/receipt/closeout contracts. Expected: audit
  PASS, approved E1, two fresh Task Sessions, two joined closeouts, stable
  semantic digest, `COMPLETE`.
- `P2-projection-equivalence`: regenerate a noncanonical view with different
  bytes but the same canonical semantic digest. Expected: preservation receipt;
  E1 remains valid.

Single-fault negatives:

- `N1-open-decision` → Decision Gate block before compilation.
- `N2-owner-gap` → Design block.
- `N3-missing-closeout-baseline` → Plan/compiler block.
- `N4-write-union-mismatch` → audit block; assert
  `materialWrites ∪ executionOutputs = allowedWrites` and disjoint subsets.
- `N5-stale-material` → admission block before write.
- `N6-semantic-false-pass` → schema-valid receipt claiming pass while
  validation is not run; semantic validator blocks.
- `N7-snapshot-drift` → invalidate before run.
- `N8-ambiguous-successor` → outer runner blocks without choosing.
- `N9-runtime-command-failure` → all preflight gates pass; Task Session emits
  empirical BLOCK and evidence.
- `N10-frontier-expansion` → new SWU excluded from E1; requires E2.
- `N11-projection-only-regeneration` → no invalidation with equivalence proof.
- `N12-owner-semantic-change` → invalidate despite superficially similar bytes.
- `N13-cursor-repeat` → identical cursor/blocker fingerprint after owner return;
  stop loop.
- `N14-closeout-join-missing` → stop before successor.
- `N15-concurrent-write-drift` → mutate target after final prewrite baseline;
  Task Session blocks and does not overwrite/adopt.

Machine-checkability requires each fixture to provide: frozen input tree;
manifest and expected digest; one injected fault; expected first-knowable stage;
expected first-detected gate; expected owner route; expected terminal code;
allowed write set; expected receipt count; and forbidden transition assertions.

Body War counterfactual:

```text
Original:
Plan pass
→ Task Session detects missing SWU-001 material/receipt/schema/closeout
→ Refresh projection sync
→ Refresh materialization
→ Task Session
→ concurrent drift block

Target replay:
Plan authors SWU-001 contract and declares material producer
→ material producer emits exact three-target package + receipt/schema
→ compiler rejects if package, target inventory, baselines,
  allowed deltas, owner receipt, or successor policy is absent
→ audit binds exact package and epoch
→ human approves
→ fresh SWU-001 Task Session
→ immediately-before-write digest check

Expected branch A:
all bindings stable → execute SWU-001 → joined closeout → successor

Expected branch B:
three targets change after baseline → empirical SNAPSHOT/WRITE_DRIFT block,
no overwrite, no adoption, writer attribution remains unknown residue
```

The replay fails non-vacuity if missing material first appears inside Task
Session. It also fails honesty if the compiler claims to predict branch B.
[Explorer protocol: Fixtures and Body War acceptance witness; Explorer local:
Body War graph and blocker matrix]

## 10. Progress metrics and loop detection

Record per epoch:

- `units_completed / approved_frontier_units`
- admitted, blocked-before-write, runtime-blocked, and closeout-joined unit counts
- first-knowable stage versus first-detected stage distance
- owner-return count by `(blockerFingerprint, fromOwner, toOwner)`
- generic Refresh repair returns; target normal-path value is zero
- epoch invalidations by semantic class
- projection-equivalence preservations
- time/transition count from Plan authored to first admitted mutation
- governance/projection writes versus implementation writes
- cursor novelty rate
- repeated blocker fingerprints
- browser/runtime witnesses where required, without treating their absence as
  planning evidence unless required by the admitted contract

Deterministic loop rules:

- Stop on repeated continuity cursor.
- Stop when the same blocker fingerprint returns to the same owner without a
  changed semantic input, new evidence, or changed admissibility verdict.
- Stop on ambiguous successor, frontier expansion, missing closeout join,
  exhausted attempt/run budget, or epoch invalidation.
- Count a bounce when a deterministic blocker is first detected later than its
  first-knowable owner.
- Count progress only when a unit closes, a blocker fingerprint changes through
  owner-valid evidence, or a new epoch is explicitly approved—not merely when
  artifacts are rewritten.

These rules distinguish the Body War projection-only Refresh (no progress) from
material-package production (blocker-changing progress), while retaining
concurrent drift as valid empirical residue. [Explorer local: scoped counts and
no-progress classification; Explorer protocol: Typed blockers; Explorer
precedents: replay and effect-aware resume invariants]

## Source binding

- `research.md#Explorer-return-1:-local-owner-hop-forensics`
- `research.md#Explorer-return-2:-primary-source-precedents`
- `research.md#Explorer-return-3:-formal-protocol`
- `receipts/explorer-local-forensics.json`
- `receipts/explorer-precedents.json`
- `receipts/explorer-protocol.json`

Started at: `2026-07-30T17:09:01Z`

Finished at: `2026-07-30T17:13:32Z`
