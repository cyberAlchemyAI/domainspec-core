# Plan: Verification Weaver

## Phase 1: Public Candidate Skeleton

Write public candidate files under `arcanum/arcana/verification-weaver/`:

- `README.md`
- `SKILL.md`
- `development/OUTPUT-CONTRACT.md`
- `development/QUALITY-BAR.md`
- `development/ANTI-PATTERNS.md`
- `development/VALIDATION-EXPERIMENT.md`
- `development/fixtures/`
- `development/negative-controls/`
- `development/run-validation-fixtures.sh`

Do not update registry or generated runtime surfaces in this phase.

## Phase 2: Receipt Schema

Implement a minimal parent receipt schema for `VERIFICATION-WEAVE`.

Validation must check:

- required target fields;
- valid `target_kind`;
- valid owner lane references;
- valid status;
- required evidence references or explicit gaps;
- no promotion action other than `none` or `candidate-request`;
- no private path in public-safe receipts.

## Phase 3: Synthetic Fixtures

Create synthetic/public-safe fixtures:

- deterministic spec derivation fixture;
- frontend UX fixture;
- execution adapter fixture;
- architecture gap fixture;
- research evidence fixture;
- mixed target fixture;
- unsupported target fixture.

Fixtures must be realistic enough to exercise routing but must not copy private
DomainSpec or poker-team examples.

## Phase 4: Negative Controls

Add the twelve negative controls from
`negative-controls/NEGATIVE-CONTROLS.md`.

Each control must have:

- fixture input;
- expected status;
- expected gap or residue;
- validation assertion.

## Phase 5: Validation Harness

Create `development/run-validation-fixtures.sh` that is shell-first and may call
TypeScript for structured validation if shell is not enough.

The runner must:

- check fixture files exist;
- validate positive and negative fixtures;
- scan for private path leakage;
- verify generated-output exclusions;
- write a timestamped report under `development/runs/`;
- return non-zero on blockable contract violations.

## Phase 6: Experiment Evidence

Use `experiment-harness` standards before promotion:

- realistic fixtures pass;
- negative controls fail closed;
- quality bar status is recorded;
- anti-pattern hits are recorded;
- generated outputs remain ignored unless promoted as durable fixtures.

## Phase 7: Promotion Review

Only after the candidate package passes validation:

- run public-boundary scan;
- run Distill validation against the implementation unit and work-pack;
- run sigil-development review;
- run experiment-harness validation;
- decide whether to add registry/generated runtime exposure.

## Stop Conditions

Stop and report `block` if:

- public package needs private examples to pass;
- target classifier cannot distinguish owner lanes;
- receipt schema can promote owner artifacts;
- no negative controls exist;
- no public-boundary scan exists;
- UX evidence is treated as implemented before calibrated harness evidence.

## Per-Slice Validation Strategy

| Slice | Validation |
| --- | --- |
| Public docs | `git diff --check`; private-path scan; owner-boundary wording scan. |
| Receipt schema | Positive fixture parse; negative fixture block assertions. |
| Classifier | One fixture per `target_kind`; mixed target split/block assertion. |
| Public safety | Private-path, generated-output, and local-log denylist scan. |
| Experiment harness alignment | Fixture runner writes a report and does not treat generated reports as source authority. |
