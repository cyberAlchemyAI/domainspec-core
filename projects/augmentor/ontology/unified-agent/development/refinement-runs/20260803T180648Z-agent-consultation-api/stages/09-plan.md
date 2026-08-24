# Stage 9: Non-executed Implementation Plan

## Plan Outcome

The implementation plan is complete and navigable, but mutation handoff is
blocked. The first future action is not “build the API”; it is to select the
candidate contract owner and admit only `SWU-ACAPI-001` through Task Session.

## Planning Artifacts

- `IMPLEMENTATION-LAYERING.md`: L0 fixture proof, L1 host integration, L2
  hardening, and L3 optional packaging.
- `WORK-PACK.md`: canonical task, SWU, gate, closeout, and validation plan.
- `EXECUTION-PACK.md`: wave order without implementation authority.
- `work-pack/shared/`: common context, decisions, gaps, and traceability.
- `work-pack/tasks/`: six task-local implementation contracts.
- `work-pack/waves/`: four evidence-gated waves.
- `stages/09-plan-distill.md`: automatic Distill validation.

## Implementation Sequence

### L0: Candidate-local proof

1. Validate the closed model-visible query schema.
2. Validate the status-tagged response and atomic evidence statements.
3. Validate the neutral projection and compiler manifest schemas.
4. Build one deterministic fixture projection and leakage validator.
5. Implement effective caps and mechanical status precedence.
6. Implement one `consult` pipeline for lookup, search, and context over the
   fixture and run QS-01-QS-14.

L0 writes only the proposed private candidate package:

`projects/augmentor/ontology/unified-agent/development/consultation-api/`

It does not integrate with ResonantOS and does not project private bytes into a
consumer repository.

### L1: Owner-approved host integration

7. Inject principal and policy context outside model-visible arguments.
8. Add the answering-agent result policy, including untrusted-evidence rules.
9. Prove one host question-to-evidence-to-answer or abstention flow.

L1 remains blocked until the principal, policy, projection, and answer-policy
owners are selected and the neutral field allowlist is approved.

### L2: Hardening

10. Add access-isolated evidence caching.
11. Add deadline and cancellation propagation.
12. Run denial, drift, timeout, conflict, cap, and prompt-injection failures.

Production caps remain unset until this layer produces measurements.

### L3: Optional extension

13. Select exactly one later extension: typed traversal, typed comparison,
stored explanation, or an HTTP wrapper. Do not combine them in one SWU.

## Core Algorithms

### Query processing

```text
verify host context
-> validate closed query
-> load exact policy and projection manifests
-> calculate effective caps
-> normalize logical selectors
-> read bounded candidates
-> apply policy before text hydration
-> calculate reproducible relevance
-> bind atomic statements and safe sources
-> calculate manifest-based freshness
-> reduce mechanical status
-> validate tagged result
-> return without writes or side effects
```

### Answering-agent processing

```text
validate result variant
-> treat all returned text as untrusted data
-> inspect source posture, freshness, confidence, and claim ceiling
-> apply owner-authored answer policy
-> answer | qualify | clarify | abstain
-> cite safe handles
```

The consultation service never runs the second algorithm.

## Validation Strategy

L0 future commands:

```bash
node projects/augmentor/ontology/unified-agent/development/consultation-api/scripts/validate-contract.mjs
node projects/augmentor/ontology/unified-agent/development/consultation-api/scripts/build-fixture-projection.mjs --check
node --test projects/augmentor/ontology/unified-agent/development/consultation-api/tests/*.test.mjs
node projects/augmentor/ontology/unified-agent/scripts/validate.mjs
```

L1-L2 future consumer commands:

```bash
npm test -- src/core/augmentor-consultation
npm run build
```

These commands are planned validation surfaces. They were not run because the
implementation files do not exist.

## Gate Status

- Design selection: pass.
- Independent design review: flag, repaired by stage 8.
- Plan Distill: pass.
- SWU atomicity: pass; one public `consult` behavior is preserved.
- First-unit narrowness: pass.
- Task Session closeout contracts: pass.
- Work-pack mutation gate: block.
- Reason: B-001 through B-005 remain explicit; no Task Session or owner
  selection is authorized by Refine.

## Invoke Result

- Mode: `plan`.
- Spell: `invoke`.
- Canonical ID: `invoke`.
- Scope: library, authoring this target-local plan.
- Phase status: `block` for mutation handoff; plan artifact authored complete.
- Mode contract: `.agents/skills/invoke/plan.md`.
- Outputs: `IMPLEMENTATION-LAYERING.md`, `WORK-PACK.md`,
  `EXECUTION-PACK.md`, task and wave files, and this transport artifact.
- Design views: all six in `stages/06-design.md` plus required stage-8 repairs.
- Glossary consistency: pass; query, projection, statement, relevance,
  confidence, freshness, and abstention meanings remain distinct.
- Dispatch techniques: sequence, SCU/SWU reduction, recomposition proof,
  validation loop, owner-boundary check, handle handoff, residue ledger, and
  execution-receipt handoff.
- Distill validation: pass for plan structure; mutation remains blocked by
  separate owner and authorization gates.
- Implementation layering: four layers, L0 recommended.
- Work-pack: split, medium complexity.
- Implementation detail: task specs complete for L0-L2; L3 exact paths remain
  blocked until one alternative is selected.
- Smallest working units: 13 complete planning contracts.
- SWU atomicity: pass, task-shaped count 0.
- First-unit narrowness: pass for SWU-ACAPI-001.
- Task Session closeout sync: pass.
- Template/profile selection: standalone implementation-layering, split
  work-pack, and execution-pack templates selected by medium complexity.
- Validation strategy: exact candidate and consumer command families recorded.
- Decisions: native tool first, fixture L0, host integration L1, hardening L2,
  one optional L3 extension.
- Unresolved gaps: B-001-B-005.
- Capability ceilings: plan authored; registry release and mutation-runtime
  readiness were not evaluated and remain false.
- Next route: a separately admitted Task Session for SWU-ACAPI-001 after B-001,
  otherwise deferred.
- Observer status: prepared for post-run observation.

