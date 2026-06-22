# Work Pack: Verification Weaver Candidate Arcana

Work pack ID: `WP-VERIFICATION-WEAVER-001`

Status: `ready-for-task-session`

## Objective

Create a candidate public Arcana package at
`arcanum/arcana/verification-weaver/` that routes testing targets to owner
lanes and emits a parent `VERIFICATION-WEAVE` receipt without copying private code
or examples.

## Scope

Create:

- `arcanum/arcana/verification-weaver/README.md`
- `arcanum/arcana/verification-weaver/SKILL.md`
- `arcanum/arcana/verification-weaver/development/OUTPUT-CONTRACT.md`
- `arcanum/arcana/verification-weaver/development/QUALITY-BAR.md`
- `arcanum/arcana/verification-weaver/development/ANTI-PATTERNS.md`
- `arcanum/arcana/verification-weaver/development/VALIDATION-EXPERIMENT.md`
- `arcanum/arcana/verification-weaver/development/fixtures/`
- `arcanum/arcana/verification-weaver/development/negative-controls/`
- `arcanum/arcana/verification-weaver/development/run-validation-fixtures.sh`

Do not create registry rows or generated runtime packages in this work pack.

## Implementation Requirements

- Use shell scripts where possible.
- Use TypeScript only where shell is not enough for structured validation.
- Keep all examples synthetic and public-safe.
- Build fresh public code; do not port private `implementation/domainspec`
  engine code.
- Use abstracted deterministic derivation precedent, not private path or
  private result claims, in public package prose.
- Define and validate `VERIFICATION-WEAVE` parent receipts.
- Preserve owner lane boundaries for:
  - `test-derivation`;
  - `ux-evidence-validator`;
  - `experiment-harness`;
  - `architecture-pattern-inventory`;
  - `research-evidence-harness`.

## Tasks

1. Execute `tasks/SWU-VW-001.md`.
2. Author the candidate `README.md` and `SKILL.md`.
3. Add the output contract, quality bar, and anti-patterns.
4. Add synthetic positive fixtures for each owner lane.
5. Add negative controls listed in `negative-controls/NEGATIVE-CONTROLS.md`.
6. Add a validation runner that checks fixture shape, expected status, and
   public-boundary rules.
7. Add validation report output under `development/runs/` and ignore generated
   reports by default.
8. Run validation.
9. Record residual gaps and the next promotion route.

## Acceptance Criteria

- Public package exists and is self-contained.
- Validation runner passes positive fixtures and fails negative controls.
- Private path scan passes.
- Parent receipt cannot promote owner artifacts.
- No registry/generated runtime exposure is added.
- Distill validation remains `pass` or any `flag` is explained with owner and
  repair route.
- `git diff --check` passes for touched files.

## Validation Commands

Expected commands after implementation:

```bash
bash arcanum/arcana/verification-weaver/development/run-validation-fixtures.sh
git diff --check -- arcanum/arcana/verification-weaver
rg -n "implementation/domainspec|validation/poker-team|/home/vrondelli|\\.arcanum/observability|example-outputs|example-runs|development/runs" arcanum/arcana/verification-weaver
```

The `rg` command may find documentation that names blocked patterns only if the
context explicitly says they are blocked, not copied evidence.

## Blockers

Block if:

- validation needs private examples to pass;
- no target classifier exists;
- no negative controls exist;
- parent receipt can promote owner outputs;
- generated runtime exposure is added before experiment evidence.
