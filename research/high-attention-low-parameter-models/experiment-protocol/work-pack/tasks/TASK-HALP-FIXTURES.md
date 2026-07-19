---
taskId: TASK-HALP-FIXTURES
docType: work-pack-task
status: blocked-by-contracts
layer: L0
slice: S-001
---

# TASK-HALP-FIXTURES — Generator, Renderer, And Scorer

## Objective

Create deterministic procedural fixtures and exact render/score contracts for
the approved primary matrix without invoking a model.

Related context: [shared execution context](../shared/context.md),
[cross-task gaps](../shared/cross-task-gaps.md), and
[traceability](../shared/traceability.md).

## Smallest Working Units

### SWU-HALP-007 — Semantic Fixtures And Provenance

- Primary behavior: generate stable semantic plans, family-level splits, ground
  truth, decoys, and provenance from explicit seed/config.
- Acceptance boundary: byte-identical corpus and manifest across clean builds.
- Split analysis: generator/split/provenance cannot pass separately because an
  unmanifested or cross-split fixture is not admissible.
- Dependencies: SWU 006.
- Source anchors: findings workload matrix; `mappings.md#fixturetoprompt`;
  `domain.md#fixtureinstance`.
- Write scope: `src/fixtures/`, `fixtures/semantic/`,
  `manifests/fixture-manifest.json`.

Implementation algorithm:

1. Derive a family seed from master seed + family + split + instance index.
2. Generate semantic facts and gold answer/evidence independently of position.
3. Generate controlled decoys/interference without leaking the gold answer.
4. Assign family-level train/dev/test (or pilot/validation/holdout) split before
   rendering variants.
5. Canonically serialize and hash every plan.
6. Emit source/generator/dependency/license provenance.

Edge cases: accidental answer in filler, duplicate semantic family across
splits, contradiction ambiguity, non-unique evidence IDs, seed/platform drift.

- Done: all selected fixture families have valid examples and negative fixtures.
- Evidence: two clean build hashes and provenance manifest.
- Validation: `node src/fixtures/build.mjs --config configs/protocol.json --out fixtures/semantic --check-determinism`.
- Owner: subagent or local fallback.
- Handoff note: do not apply model chat templates in this SWU.

### SWU-HALP-008 — Rendering And Deterministic Scoring

- Primary behavior: render exact arm/position variants and score stored outputs
  under one versioned output grammar.
- Acceptance boundary: positive/negative/metamorphic render-score fixture suite.
- Split analysis: renderer and scorer could be coded independently, but the
  output grammar and evidence IDs are their shared semantic boundary; acceptance
  requires an end-to-end stored-output witness.
- Dependencies: SWU 006, 007.
- Source anchors: `domain.md#promptarm`, `operations.md#rendertrialcell`,
  `operations.md#scoretrial`, `mappings.md#runtoscore`.
- Write scope: `src/render/`, `src/score/`, `fixtures/render-score/`.

Implementation algorithm:

1. Render constant instruction envelope plus arm-specific context from one plan.
2. Rotate identical evidence/decoys into approved positions.
3. For each admitted template adapter, record rendered bytes, token IDs,
   evidence spans, and hashes; before admission use a template-neutral fixture.
4. Parse strict answer/evidence/support fields.
5. Score answer, evidence, abstention/support, false-support eligibility, and
   parse status separately.
6. Assert metamorphic invariants: rotation changes position not truth; compact
   and full preserve identical answer evidence; evidence-absent removes it.

Edge cases: overflow, Unicode normalization, repeated evidence IDs, extra prose,
partial output, invalid abstention, contradictory evidence, parser ambiguity.

- Done: fixture suite covers each family/arm/rotation and parser failure.
- Evidence: render manifest and score receipts.
- Validation: `node src/score/test-render-score.mjs fixtures/render-score`.
- Owner: subagent or local fallback.
- Handoff note: no qualitative judge or fuzzy evidence matching without a new
  approved scorer decision.

## Synchronization

Task completion unlocks SWU 010 only; it does not admit a model stack.
