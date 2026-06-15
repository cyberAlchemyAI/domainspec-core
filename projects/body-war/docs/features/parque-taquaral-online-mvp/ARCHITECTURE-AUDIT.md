# Architecture Audit - Parque Taquaral Online MVP

## Verdict

`pass-for-architecture-boundary-selection`

The architecture/import-boundary blocker is resolved enough to proceed to implementation
planning. This artifact does not implement the app and does not prove runtime readiness.

## Selected Boundary

Body War will use a **Body War-owned TypeScript workspace/app with a DomainSpec path alias**.

Body War owns:

- MVP app source,
- product-specific domain model,
- Strava integration adapters,
- Parque Taquaral MVP UI,
- tests and local runtime wiring.

DomainSpec owns:

- architecture method source,
- pattern-library guidance,
- dependency rules,
- testing alignment,
- observability alignment.

Body War may import or reference DomainSpec methods through explicit TypeScript aliases or
source references. It must not copy DomainSpec pattern-library content and claim ownership.

## Import / Reference Mechanism

Initial implementation should use project-local TypeScript configuration similar to:

```json
{
  "compilerOptions": {
    "baseUrl": ".",
    "paths": {
      "@body-war/*": ["src/*"],
      "@domainspec/methods/*": ["../../implementation/domainspec/architecture/*"]
    }
  }
}
```

The exact relative path may change with the final app location, but the rule is stable:
DomainSpec method references are explicit, typed or path-addressed, and read as external
authority.

## Governing DomainSpec Sources

| Source | Use |
| --- | --- |
| `implementation/domainspec/architecture/ARCHITECTURE.md` | Architecture index and Functional TypeScript model. |
| `implementation/domainspec/architecture/pattern-library/LAYERING-REFERENCE.md` | Domain, application, infrastructure, and interface layer responsibilities. |
| `implementation/domainspec/architecture/pattern-library/DEPENDENCY-RULES.md` | Import direction and architecture drift checks. |
| `implementation/domainspec/architecture/pattern-library/TESTING-ALIGNMENT.md` | Test obligation mapping. |
| `implementation/domainspec/architecture/pattern-library/OBSERVABILITY-ALIGNMENT.md` | Observability obligation mapping. |
| `implementation/domainspec/architecture/pattern-library/concepts/ui/` | Page, layout, component, hook, guard, adapter, state-indicator guidance. |
| `implementation/domainspec/architecture/pattern-library/concepts/backend/` | Interface, operation, query, mapping, rule, policy guidance. |

## Body War Layer Map

| Layer | Body War MVP responsibility |
| --- | --- |
| Domain | Track, runner, Strava activity evidence, control claim, submission status, public controller metric. |
| Application | Connect Strava, list activities, submit evidence, review evidence, compute current controller. |
| Infrastructure | Strava gateway, local persistence adapter, later geometry/map adapter. |
| Interface | HTTP/API routes, DTO validation, UI adapters. |
| UI | Parque Taquaral pilot page, Strava connection state, activity list, submission panel, evidence review state. |

## Dependency Rules

- Domain imports only local domain/shared domain files and TypeScript built-ins.
- Application imports domain only.
- Infrastructure imports domain and application contracts only.
- Interface imports application API only.
- UI pages compose layouts, guards, components, hooks, and adapters; business logic stays out of page components.

## Required Checks Before Implementation Is Marked Ready

1. `tsconfig` path aliases exist for Body War local source and DomainSpec method references.
2. Architecture audit cites DomainSpec method sources without copying their content.
3. Static TypeScript check runs with `strict` semantics.
4. Architecture tests or lint rules check import direction.
5. API contract tests cover Strava status, activities, tracks, and submissions.
6. UI smoke covers disconnected, connected, zero-activity, and submitted-evidence states.

## Blocker Closure

Closed:

- `DEC-ARCH-BOUNDARY-001`: selected Body War-owned TypeScript workspace with DomainSpec path alias.
- `BLK-ARCH-BOUNDARY-001`: closure condition satisfied by this audit and the decision record.
- `GAP-DOMAINSPEC-EXPORT-001`: resolved for MVP by path-alias/source-reference consumption; shared typed package remains deferred.

Still open:

- `BLK-STRAVA-ACTIVITY-001`: real Strava activity import/submission evidence is still missing.
- `GAP-TAQUARAL-GEOMETRY-001`: sourced track geometry remains deferred.

## Next Route

Proceed to implementation planning with `invoke` or `task-session` only for a bounded MVP slice.

Recommended next artifact:

```text
projects/body-war/docs/features/parque-taquaral-online-mvp/WORK-PACK.md
```

That work-pack should translate this architecture audit into the first build slice without
adding monetization, full anti-cheat, mobile app scope, or GPS polygon automation.
