---
taskId: TASK-HALP-DECISIONS
docType: work-pack-task
status: blocked-human
layer: L0
slice: S-000
---

# TASK-HALP-DECISIONS — Freeze Protocol Decisions

## Objective

Produce five independently approved, machine-readable decision records. This
task owns project choices only; it cannot rewrite source-backed research facts.

## Dependencies And Blockers

- Dependencies: none for SWU 001; SWU 002–005 depend on 001.
- Blocker: human owners have not approved any record.
- Source contracts: [SPEC readiness](../../SPEC.md#protocol-readiness),
  [research unresolved decisions](../../../experiment-protocol-research/findings.md#unresolved-human-decisions),
  [cross-task decisions](../shared/cross-task-decisions.md).
- Related context for every SWU: [shared execution context](../shared/context.md),
  [cross-task gaps](../shared/cross-task-gaps.md), and
  [traceability](../shared/traceability.md).

## Smallest Working Units

### SWU-HALP-001 — Claim Boundary And Primary Estimands

- Primary decision: freeze exactly what the pilot may claim and which named
  estimands are primary.
- Independent acceptance boundary: one owner-approved record can pass without
  any threshold, platform, or workload record.
- Split analysis: checkpoint scope and estimands were considered separately,
  but neither is executable or reviewable without the other; together they
  define one semantic claim.
- Inputs: research verdict matrix and repaired constructs.
- Output/write scope: `configs/decisions/claim-estimands.json` only.
- Procedure:
  1. Present the recommended within-family, stack-specific claim.
  2. Record selected checkpoints as a family role (`smaller`, `larger`), not an
     immutable revision yet.
  3. Select primary outcomes from retention, direct checkpoint contrast,
     difference-in-retention, added-evidence behavior, middle loss, and false
     support.
  4. Record forbidden causal/general/mechanism claims.
  5. Capture approval, alternatives, and rationale.
- Edge/failure cases: an owner request for parameter causality or generic
  mechanism proof blocks and reroutes to new research/design.
- Done criteria: schema-valid decision; `selected != unresolved`; owner approval
  handle exists; typed KILLs are quoted as constraints.
- Acceptance evidence: reviewed decision record.
- Validation: `jq -e '.decision_id == "HALP-DEC-001" and .approval.status == "approved" and (.forbidden_claims | length > 0)' configs/decisions/claim-estimands.json`.
- Execution owner: manual via decision-gate/interrogation.
- Handoff note: ask exactly one claim-boundary question; do not batch later
  numeric/platform choices into this approval.

### SWU-HALP-002 — Inference And Allocation Policy

- Primary decision: freeze margins, uncertainty, multiplicity, N, allocation,
  repetitions, exclusions, and power/precision rationale.
- Acceptance boundary: one statistical review record.
- Split analysis: individual numbers cannot pass independently because they
  jointly determine error and decision behavior for one primary outcome family.
- Dependencies: SWU 001.
- Source anchors: findings mandatory-closure checklist; `operations.md#analyzephase`.
- Output/write scope: `configs/decisions/inference.json`.
- Procedure: name experimental unit and pairing; choose scale-specific margins;
  declare N/repetitions; state uncertainty/multiplicity; freeze exclusion and
  missing-cell policy; attach precision/power rationale.
- Edge/failure cases: post-hoc thresholds, independent-trial analysis of paired
  cells, or undefined false-support denominator block.
- Done criteria: all numeric fields and analysis families are explicit and
  reviewed; diagnostics are separated from confirmatory outcomes.
- Acceptance evidence: decision record plus independent statistical review.
- Validation: `jq -e '.approval.status == "approved" and .sample_size > 0 and (.repetitions > 0)' configs/decisions/inference.json` plus reviewer sign-off.
- Execution owner: manual.
- Handoff note: do not infer values from the research's candidate defaults.

### SWU-HALP-003 — Workload And Trial Matrix

- Primary decision: freeze task families, arms, rotations, context lengths,
  interference, output budget, and retrieval role.
- Acceptance boundary: one matrix decision whose projection is finite.
- Split analysis: task/arm/length can be edited separately, but a partial set
  cannot define a trial matrix or budget; the matrix is the smallest meaningful
  approval object.
- Dependencies: SWU 001.
- Source anchors: `SPEC.md#normative-experiment-boundary`, `domain.md#promptarm`,
  findings smallest specification target.
- Output/write scope: `configs/decisions/workload-matrix.json`.
- Procedure: select procedural families; select required arms; freeze rotations;
  select short/long bins subject to admission; declare interference/output
  budgets; defer or justify oracle/retrieved arms; calculate planned cell count.
- Edge/failure cases: different evidence across compact/full, arm-specific
  semantics collapsed into subtraction, or 128K without admission blocks.
- Done criteria: finite matrix projection, explicit exclusions, approved owner.
- Acceptance evidence: JSON record and human-readable matrix preview.
- Validation: `node src/validate/project-matrix.mjs configs/decisions/workload-matrix.json --dry-run` after SWU 006; manual finite-cross-product review before then.
- Execution owner: manual.
- Handoff note: recommended starting matrix is not authorized until recorded.

### SWU-HALP-004 — Platform Admission Policy

- Primary decision: freeze admissible checkpoint roles, immutable identity
  requirements, runtime/backend/precision/KV policy, decoding, hardware class,
  and prohibited fallbacks.
- Acceptance boundary: one platform-owner approval.
- Split analysis: runtime and model choices are coupled by compatibility and
  capacity; separate approvals could admit an invalid tuple.
- Dependencies: SWU 001.
- Source anchors: `domain.md#modelstack`, `operations.md#admitmodelstack`,
  findings platform requirements.
- Output/write scope: `configs/decisions/platform-admission.json`.
- Procedure: name candidate family/revisions or immutable-selection rule;
  declare tokenizer/template; runtime/backend; precision/KV; decode; hardware;
  capacity assertions; incompatibility policy.
- Edge/failure cases: architecture support treated as compatibility, advertised
  context treated as capacity, or hidden fallback permitted blocks.
- Done criteria: exact admission fields and failure policy approved.
- Acceptance evidence: platform decision record.
- Validation: `jq -e '.approval.status == "approved" and (.prohibited_fallbacks | length >= 5)' configs/decisions/platform-admission.json`.
- Execution owner: manual/platform owner.
- Handoff note: actual revisions remain unadmitted until SWU 009 receipts.

### SWU-HALP-005 — Resource, Evidence, License, Publication Boundary

- Primary decision: freeze measurement boundary, resource authorization policy,
  evidence storage/retention, provenance/licenses, and claim publication scope.
- Acceptance boundary: one cross-owner record with all required approvals.
- Split analysis: energy, evidence, and publication owners differ, but a run
  cannot safely start with any one boundary absent; the record keeps separate
  approvals inside one run-authorization contract.
- Dependencies: SWU 001.
- Source anchors: `domain.md#resourcefrontier`, architecture storage layout,
  findings budget/license requirements.
- Output/write scope: `configs/decisions/resource-publication.json`.
- Procedure: declare hardware access; energy/cost boundary; tracked/ignored/
  external state namespaces; raw-output retention; license manifest rules;
  publication claim boundary; secret/PII policy.
- Edge/failure cases: unbounded external cost, unapproved raw outputs, missing
  license, or cost claims without dated accounting block.
- Done criteria: all owner approvals and state namespaces recorded.
- Acceptance evidence: resource/publication decision record.
- Validation: schema plus repository/resource/publication owner review.
- Execution owner: manual.
- Handoff note: a GPU allocation is a separate execution authorization even
  after this policy is approved.

## Synchronization

After each approved SWU, update the corresponding row in
`../shared/cross-task-decisions.md` and blockers in
`../shared/cross-task-gaps.md`. Do not change `SPEC.md` silently; submit an
explicit patch request if an approved decision contradicts it.

## Completion Evidence

Five approved records, decision index/hash, and work-pack blocker update.
