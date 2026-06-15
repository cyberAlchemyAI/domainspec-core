# Body War Parque Taquaral Review Audit Spec

Dispatch: `body-war-parque-taquaral-review-audit-20260610`

## Scope

This is a review/audit spec pass only.

No app code, deployment, backend implementation, Strava integration changes, or UI build work is authorized by this artifact.

## Current Audit Position

- Body War has a Python/static prototype app with a real Strava OAuth/backend path.
- OAuth connection has passed, but activity import/submission readiness is not proven.
- Parque Taquaral, Campinas is selected as pilot context.
- Parque Taquaral track geometry is not sourced and must not be claimed.
- The future architecture should follow DomainSpec Functional TypeScript methods instead of extending the Python/static prototype as the target architecture.

## DomainSpec Method Imports

Future Body War architecture should consume DomainSpec methods through a governed TypeScript boundary.

Required source authorities:

- `implementation/domainspec/architecture/ARCHITECTURE.md`
- `implementation/domainspec/architecture/pattern-library/README.md`
- `implementation/domainspec/architecture/pattern-library/LAYERING-REFERENCE.md`
- `implementation/domainspec/architecture/pattern-library/DEPENDENCY-RULES.md`
- `implementation/domainspec/architecture/pattern-library/TESTING-ALIGNMENT.md`
- `implementation/domainspec/architecture/pattern-library/OBSERVABILITY-ALIGNMENT.md`
- UI concept cards under `implementation/domainspec/architecture/pattern-library/concepts/ui/`
- backend/interface concept cards under `implementation/domainspec/architecture/pattern-library/concepts/backend/`

Acceptable future import/reference mechanisms:

- TypeScript package dependency on a DomainSpec methods package, if one is created.
- `tsconfig` path alias from a Body War TypeScript workspace to approved DomainSpec method exports.
- Generated typed method/index module that references DomainSpec source paths and preserves ownership.
- Documentation-only source references for audit until code-level exports exist.

Rejected mechanisms:

- Copying DomainSpec pattern-library docs into Body War as if Body War owns them.
- Treating the current Python/static prototype as the target architecture.
- Implementing TypeScript architecture before the import/reference boundary is selected.

## Review Lanes

The audit route uses four review lenses:

- Body War MVP product: checks the runner/operator story and Parque Taquaral pilot framing.
- DomainSpec architecture: checks Functional TypeScript layering, imports, dependency direction, and concept-card selection.
- Strava evidence: checks OAuth, activity import, submission, token privacy, and readiness claims.
- Context honesty: checks that park context, geometry, scoring, and future evidence are not overstated.

## Pass/Flag/Block Rules

Pass:

- Dispatch route validates.
- App implementation remains untouched.
- DomainSpec TypeScript import/reference boundary is named as required future work.
- Prototype evidence is separated from target architecture readiness.

Flag:

- Parque Taquaral is referenced without geometry source.
- Strava OAuth is connected but activity submission remains unproven.
- DomainSpec methods are available as docs but not yet exported as typed package APIs.

Block:

- Any implementation starts before architecture/import boundary selection.
- Any DomainSpec pattern content is copied into Body War as canonical Body War-owned method content.
- Any readiness claim treats OAuth success as full Strava evidence readiness.

## Next Route

Next route is an architecture review/audit, not implementation.

Recommended next artifact:

`projects/body-war/docs/features/parque-taquaral-online-mvp/ARCHITECTURE-AUDIT.md`

That artifact should answer:

1. What Body War TypeScript package/app boundary will exist?
2. Which DomainSpec method exports or path aliases will it import/reference?
3. Which UI/backend concept cards govern the MVP screens and APIs?
4. Which dependency rules must be enforceable by TypeScript checks?
5. Which tests prove architecture conformance before app implementation begins?
