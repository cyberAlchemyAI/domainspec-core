---
task_id: TASK-DSD1-LEDGER
feature_code: DSD1
layer: L0
status: not-started
gate_status: ready
updatedAt: 2026-07-03
---

# TASK-DSD1-LEDGER: Align DS-D1 Maturity Language

## Objective

Make every DS-D1 planning and read-model surface say the same thing:
backend `DS-D1.1..14` are shape/fixture-backed candidates, UI `DS-D1.15..25`
are formation-deferred, and DS-D8 endpoint use is evidence pressure only.

## Source Anchors

- `projects/domainspec-v2/development/r3-research/ds-d1-metatype-category-boundary/findings.md`
- `projects/domainspec-v2/definitions/meta-types/meta-types.yml`
- `projects/domainspec-v2/definitions/meta-types/meta-types.md`
- `projects/domainspec-v2/development/meta-type-definitions/CANDIDATES.md`
- `projects/domainspec-v2/development/meta-type-definitions/WORK-PACK.md`
- `projects/domainspec-v2/development/meta-type-formalization/WORK-PACK.md`
- `projects/domainspec-v2/CRAFT.md`

## SWUs

| SWU | Purpose | Write Scope | Gate |
| --- | --- | --- | --- |
| SWU-DSD1-001 | Align staged-authority status language. | DS-D1 status/read-model docs only. | selected-first |
| SWU-DSD1-002 | Audit and fix projection drift. | Projection docs only. | after SWU-DSD1-001 |

## Implementation Notes

- Prefer explicit lifecycle words: `shape-candidate`, `semantic-hardening`,
  `formation-deferred`, `endpoint-used`, `promoted`.
- Do not rename or delete schemas in this task.
- Do not treat "active-harden" as proof of semantic authority.
- Keep root definitions as the authority; implementation views are only
  necessary implementation projections.

## Acceptance Evidence

- Docs and projections no longer imply that all 25 candidates are equally
  promoted.
- UI labels remain visible as candidates without gaining DS-D1 formation
  authority from DS-D8 references.
- Validation command: `npm --prefix projects/domainspec-v2/impl run validate:docs`.
- Diff hygiene: `git diff --check -- projects/domainspec-v2`.
