# Decision: Body War TypeScript Architecture Import Boundary

## Decision Gate Result

- Target scope: `DEC-ARCH-BOUNDARY-001`
- Result: `PASS`
- Decisions resolved: 1
- Blockers remaining: 0 for the architecture/import-boundary selection
- Decision date: 2026-06-11
- Decision artifact: `projects/body-war/docs/decisions/architecture-import-boundary.md`

## Question

Which TypeScript architecture/import boundary will Body War use to consume DomainSpec methods?

## Considered Options

| Option | Benefit | Cost / Risk | Downstream Impact |
| --- | --- | --- | --- |
| Body War-owned TypeScript workspace with DomainSpec path alias | Fastest implementation path; Body War owns app code while DomainSpec remains source authority; enforceable with `tsconfig` aliases and architecture checks. | Requires care not to treat DomainSpec docs as Body War-owned canonical content. | Unblocks `ARCHITECTURE-AUDIT.md` and future task-session planning. |
| Shared DomainSpec method package | Clean long-term package boundary and reusable typed API. | Higher upfront cost; requires designing/exporting a DomainSpec package before Body War can build. | Good future hardening target, but too slow for MVP. |
| Documentation-only reference until exports exist | Lowest code risk; useful for audit-only reasoning. | Does not provide an enforceable TypeScript import boundary. | Keeps implementation blocked. |

## Selected Option

`body-war-own-typescript-workspace-with-domainspec-path-alias`

## Rationale

The user selected option `1`. This gives Body War a local TypeScript app/package boundary
that can implement the MVP without waiting for a formal shared DomainSpec methods package.
DomainSpec remains the method authority; Body War consumes it through explicit path aliases
and source references, not by copying or re-owning the pattern library.

## Architecture Rule

Future Body War implementation should create a Body War-owned TypeScript workspace or app
with:

- local Body War source under a project-owned package/app boundary,
- `tsconfig` aliases or explicit source references to approved DomainSpec architecture
  method sources,
- architecture tests or static checks for dependency direction,
- no copied DomainSpec pattern-library content as Body War-owned canonical methods.

## Remaining Deferred Work

- A later hardening pass may promote DomainSpec methods into a shared typed package.
- Parque Taquaral route geometry remains deferred until a sourced track-boundary artifact exists.
- Strava activity submission readiness remains blocked until a real run imports and submits.

## Source

- User selected `1`, 2026-06-11.
- Craft blocker: `projects/body-war/.craft/ledger.yml`, `DEC-ARCH-BOUNDARY-001`.
- Review spec: `projects/body-war/development/dispatches/20260610-body-war-parque-taquaral-review-audit.spec.md`.
