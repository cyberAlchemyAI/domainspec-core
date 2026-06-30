# TASK-CONTRACTS-VALIDATORS

## Objective

Carry the public-safe evidence-card contracts, validators, Review Queue mapping, and scope-tag
fixture model into the standalone package.

## Layer And Slice

- Layer: L1.
- Slices: S-002 and S-003.
- Wave: W1.

## Source Contracts

- `development/resonantos-integration/owned-base/BASE-FOR-VICTOR.md`
- `development/resonantos-integration/findings.md`
- `work-pack/shared/context.md`

## Dependencies

- `SWU-RCI-001`.

## Blocker State

Resolved. Validator scripts and schemas were copied into the package.

## Completion State

Completed in `task-session-20260629T164831Z-standalone-package`.

## Smallest Working Units

### SWU-RCI-002

- Goal: add schema and validator carry-forward policy plus a synthetic evidence-card fixture.
- Dependencies: `SWU-RCI-001`.
- Source anchors: `owned-base/BASE-FOR-VICTOR.md` section 1 and section 4.
- Related context: public Arcanum inventory schemas and validators.
- Write scope:
  - `standalone-package/contracts/evidence-card.schema.yml`
  - `standalone-package/contracts/evidence-set.schema.yml`
  - `standalone-package/contracts/index.schema.yml`
  - `standalone-package/tools/`
  - `standalone-package/fixtures/evidence-card/`
  - `standalone-package/docs/validator-policy.md`
- Done criteria:
  - Contract files are copied or referenced with a clear policy.
  - Synthetic fixture is public-safe.
  - Validator command or review check is documented.
- Acceptance evidence:
  - Validator run if scripts are copied.
  - Otherwise explicit review note explaining why the package references public Arcanum validators.
- Validation surface:
  - `bash standalone-package/tools/validate-evidence-card-fixtures.sh ...` when copied.
  - YAML/JSON parse checks for fixture files.
- Execution owner: local-fallback.
- Handoff note: preserve MIT/public provenance and avoid private source paths in package files.

### SWU-RCI-003

- Goal: add Review Queue lifecycle mapping and scope-tag adapter contract.
- Dependencies: `SWU-RCI-001`.
- Source anchors: `findings.md` sections 2 and 4, integration guide scope-tag section.
- Related context: candidate -> review -> decide -> promote lifecycle.
- Write scope:
  - `standalone-package/docs/review-queue-mapping.md`
  - `standalone-package/docs/scope-tags.md`
  - `standalone-package/fixtures/review-queue/`
- Done criteria:
  - Mapping uses ResonantOS's existing Review Queue and decide enum.
  - Each candidate fixture has exactly one scope tag.
  - No direct trusted write is represented in candidate fixtures.
- Acceptance evidence:
  - Fixture maps to intake, review, decide, and promote states.
  - Scope-tag review confirms exactly one scope per fixture.
- Validation surface:
  - JSON/YAML parse checks for fixtures.
  - Markdown contract review.
- Execution owner: local-fallback.
- Handoff note: do not introduce a parallel promotion queue.

## Synchronization Rules

Update `work-pack/shared/traceability.md` if contract paths change.

## Completion Receipt

- Copied contracts: `contracts/evidence-card.schema.yml`, `contracts/evidence-set.schema.yml`,
  and `contracts/index.schema.yml`.
- Copied tools: `tools/validate-evidence-card-slice.sh`,
  `tools/validate-evidence-card-fixtures.sh`, and `tools/validate-index-json.sh`.
- Evidence-card fixture validator passed.
