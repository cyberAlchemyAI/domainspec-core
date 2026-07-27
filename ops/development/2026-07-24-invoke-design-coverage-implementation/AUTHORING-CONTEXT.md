# Authoring Context: Invoke Design Coverage

Mode: `lean`, strict obligation mapping, authoring-only.

## Obligations

| ID | Obligation | Evidence status |
| --- | --- | --- |
| CTX-01 | Preserve the accepted research claim boundary. | covered |
| CTX-02 | Separate six-view navigation from concern sufficiency. | covered |
| CTX-03 | Define a closed manifest and independent denominator. | covered |
| CTX-04 | Define deterministic four-state, two-pass selection. | covered |
| CTX-05 | Broaden UX only for changed human semantic contracts. | covered |
| CTX-06 | Strengthen architecture with triggered extensions, not universal families. | covered |
| CTX-07 | Keep Design declarations separate from Plan evidence. | covered |
| CTX-08 | Produce an executable Spellcraft handoff without editing canonical sources. | covered |

## Selected evidence

| Source | Selectors | Obligations |
| --- | --- | --- |
| `../2026-07-24-invoke-lifecycle-progress-update/research/2026-07-24-design-phase-coverage/findings.md` | `Closed scope and denominator proposal`; `Deterministic two-pass selection`; `Architecture and bounded UX contracts`; `Design versus Plan evidence states`; `Validator and frozen-fixture requirements` | CTX-01..07 |
| `../2026-07-24-invoke-lifecycle-progress-update/DEFINE.md` | `Problem`; `Actors and authority`; `Open decision` | CTX-01, CTX-08 |
| `../2026-07-24-invoke-lifecycle-progress-update/DESIGN.md` | six views; `Risks and controls`; `Design gate` | CTX-02, CTX-06, CTX-08 |
| `../../../arcanum/spells/invoke/design.md` | activation gate; template selection; mode gates; evidence capability contract | CTX-02..08 |
| `../../../arcanum/spells/invoke/templates/domainspec-spec/architecture-bundle.md` | required view set; design rules | CTX-02, CTX-06 |
| `../../../arcanum/spells/invoke/templates/architecture/architecture.md` | six views; decisions; risks | CTX-02, CTX-06 |
| `../../../arcanum/spells/invoke/templates/ux-plan/ux-plan.md` | actors; journeys; surfaces; accessibility; acceptance | CTX-05 |
| `../../../arcanum/spells/invoke/development/run-validation-fixtures.sh` | validation runner and fixture registration | CTX-03, CTX-04, CTX-07, CTX-08 |

## Excluded nearby evidence

- BTE and financial-settlement packages: useful consumers, but not needed to
  define the generic Invoke Design-selection contract.
- Private product specifications: excluded from the public implementation
  boundary.
- Generated `.agents/`, `.claude/`, and `.codex/` Invoke surfaces: downstream
  projections, not canonical design sources.

## Context result

- Files selected: 8.
- Obligation coverage: 100%.
- Runtime handoff pack: not generated; planning must leave execution-time
  Context Builder evidence to Spellcraft or Task Session.
- Blockers: none for authoring.

