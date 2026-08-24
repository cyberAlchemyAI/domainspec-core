# Definitional skeptic review

Status: BLOCK  
Validation: BLOCK

## Blockers

1. The distinct `Execution-Admission Compiler` duplicates Work Pack Readiness
   Audit phases 1–4.
2. `materialProducer` is abstract rather than an exact per-SWU producer
   reference.
3. The proposed manifest collapses separate authority/lifecycle axes.

## Required repairs

- **KILL** the compiler as a new lifecycle owner. If needed, add a deterministic
  `readiness-audit projection generator` inside Work Pack Readiness Audit with
  `authorityEffect: none`. Plan stays canonical; Audit proves; Decision
  Gate/human approves.
- **KILL** `compiler/materializer`. Product/staged bytes use an exact
  `materialPackageRef.producerOwnerRef`; the audit projection never creates
  them.
- Replace generic `outerRunner` with the exact existing
  `task-session-until-blocker` owner.
- The manifest carries only immutable references to Structured Interview and
  Decision Gate receipts; it does not recompute question or decision status.
- **KILL** aggregate `readiness.verdict`. Preserve independently produced
  `artifactAuthoredStatus`, `registryReleasedStatus`,
  `mutationRuntimeReadyStatus`, and `auditVerdict`.
- **KILL** aggregate `epoch.status: complete`. Preserve `planArtifactStatus`,
  `auditStatus`, `approvalStatus`, and `chainStatus`; only Task Session Until
  Blocker may emit `chainStatus: complete`.
- Rename `executionMode` to `requestedTaskSessionExecutionMode` plus a live
  `taskSessionAdmissionReceiptRef`.
- Rename `nextDeclaredSuccessor` to `projectedNextSuccessor` and bind
  `canonicalSuccessorRef`, projection owner/equivalence validator, and
  `authorityEffect: none`.
- Split `sourceClosure.refs` and closeout baselines into
  `canonicalAuthorityRefs`, `derivedProjectionRefs`,
  `executionByteBaselines`, and `semanticBindings`, each with producer,
  validator, invalidation, and authority effects.
- Add `evidenceCeiling: frozen-input-contractual-readiness`; never claim future
  empirical certainty.

## Exact merge targets

- Projection normalization/reference checking → Work Pack Readiness Audit
  phases 1–4.
- Outer sequencing → Task Session Until Blocker.
- Question closure → Structured Interview.
- Consequential choice/epoch approval → Decision Gate.
- Canonical SWU graph/contracts → Invoke Plan / `WORK-PACK.md`.
- One-SWU mutation/empirical validation → Task Session.
- Bookkeeping sync → Invoke Refresh.
- Continuation dispatch/join → Continuation Router, never a generated view.
- Material bytes → exact target-specific per-SWU producer; unresolved in the
  initial synthesis.

Exact source anchors:

- `arcanum/spells/work-pack-readiness-audit/README.md:56-146,194-214`
- `arcanum/spells/task-session-until-blocker/README.md:64-168`
- `arcanum/arcana/task-session/SKILL.md:216-289`
- `arcanum/spells/invoke/README.md:20-26,46-70,98-107,280-324`
- `arcanum/spells/invoke/plan.md:9-32,155-171,189-207`
- `arcanum/arcana/structured-interview-kits/SKILL.md:35-53,93-107`
- `arcanum/arcana/decision-gate/SKILL.md:51-88,176-192`

Started: `2026-07-30T17:14:00Z`  
Finished: `2026-07-30T17:20:07Z`
