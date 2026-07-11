---
task_id: TASK-SGRM-IMPLEMENTATION
feature_code: SGRM
layer: L1-L2
status: not-started
---

# TASK-SGRM-IMPLEMENTATION: Migrate Workflow And Validators

## Objective

Make Workflow accept intra-feature and cross-feature orchestration, delete active
Saga implementation artifacts, and replace Saga-specific validation with
generic invariants.

## SWU-SGRM-003: Attribute-One-Of Rule

### Inputs And Outputs

Inputs: validate-content.ts, instances.ts, meta-type-noncollapse.ts, their tests,
and workflow.schema.yml.

Outputs: one supported criterion rule and focused tests.

### Algorithm

For criterion rule attribute-one-of:

1. Validate key is non-empty and values is a non-empty string array.
2. Read the concept Attribute/Value table.
3. Find key case-insensitively.
4. Normalize actual and each allowed token by trim plus lowercase.
5. Pass iff actual equals one allowed token.
6. Emit a precise missing-key, empty-values, or unexpected-value error.
7. Instance generation chooses values[0] deterministically.
8. Instance validation uses the same membership semantics.
9. Add attribute-one-of to the non-collapse attestation set and total
   classification guard.
10. Test intra-feature pass, cross-feature pass, unknown fail, missing fail,
    deterministic generation, and attestation permutation behavior.

### Contract

- Dependencies: SGRM-001.
- Write scope: the three tool modules and focused test files.
- Done: no unsupported-rule skip; all focused tests and typecheck pass.
- Evidence: test output and receipt.
- Validation: tools:test, instances round trip, typecheck.
- Owner: local-fallback.

## SWU-SGRM-004: Schema And Fixture Migration

### Ordered Rules

1. Update Workflow schema criterion to attribute-one-of with
   intra-feature/cross-feature values.
2. Update Workflow card/code pattern to cover ordered orchestration within or
   across feature boundaries.
3. Remove Saga distinguisher language.
4. Add a cross-feature Workflow positive fixture.
5. Keep an intra-feature Workflow positive fixture.
6. Replace workflow-bad cross-feature rejection with missing or unknown scope.
7. Delete active saga.md, saga.schema.yml, saga-ok.md, and saga-bad.md only after
   the Workflow focused tests pass.
8. Regenerate or validate generated instances.

### Contract

- Dependencies: SGRM-002 and SGRM-003.
- Write scope: behavioral Workflow/Saga files and mt fixtures only.
- Done: no active Saga implementation file; valid scope variants pass; invalid
  scope fails.
- Evidence: file census, fixture output, receipt.
- Validation: validate:content, instances generate/validate, validate:docs.
- Owner: local-fallback.

## SWU-SGRM-005: Relationship And Non-Collapse Migration

### Ordered Rules

1. Rewrite active relationship fixtures from Saga source to cross-feature
   Workflow source.
2. Add a negative relationship fixture or unit case proving Saga source is
   unconstructible after registry removal.
3. Remove Saga-specific endpoint obligations from validator expectations.
4. Remove MUST fire Saga~Workflow and sole-collapse acceptance locks.
5. Preserve generic fresh-duplicate, anti-attestation, exception-lane,
   structural-witness, and classification-totality tests.
6. Set the baseline registry expectation from the execution-time schema set;
   after Saga removal the current backend baseline should report zero collapse
   candidates unless another independently evidenced pair appears.
7. Run focused tests, then the full validation suite.

### Contract

- Dependencies: SGRM-002 and SGRM-004.
- Write scope: relationship fixtures, relationship/content/non-collapse tests,
  and the non-collapse CLI acceptance checks.
- Done: cross-feature Workflow passes; Saga source fails; no Saga hard-code;
  generic gate behavior remains.
- Evidence: focused/full test output and receipt.
- Validation: validate:rels, tools:test, typecheck, validate.
- Owner: local-fallback.

## Failure Modes

- Unsupported rule silently skipped: block.
- Allowed scope normalization accepts partial strings: block.
- Workflow becomes scope-unconstrained: block.
- Saga files deleted before replacement fixtures pass: restore and block.
- Generic non-collapse tests removed to make the suite green: block.
