# Body War Craft Ledger

Human-readable view of [.craft/ledger.yml](.craft/ledger.yml). The ledger is the
source of truth; this page is an indexed navigation surface.

## Quick Links

- Current next move: [execute the W0 spec baseline](#next-move).
- Active blocker: [BLK-STRAVA-ACTIVITY-001](#blocker-blk-strava-activity-001).
- Active gap: [GAP-TAQUARAL-GEOMETRY-001](#gap-gap-taquaral-geometry-001).
- Closed architecture decision: [DEC-ARCH-BOUNDARY-001](#decision-dec-arch-boundary-001).
- One-shot forecast: [MVP-ONESHOT-FORECAST.md](docs/features/parque-taquaral-online-mvp/MVP-ONESHOT-FORECAST.md).
- Invoke design/plan: [DESIGN.md](docs/features/parque-taquaral-online-mvp/DESIGN.md), [WORK-PACK.md](docs/features/parque-taquaral-online-mvp/WORK-PACK.md), [EXECUTION-PACK.md](docs/features/parque-taquaral-online-mvp/EXECUTION-PACK.md).
- Key artifacts: [architecture decision](docs/decisions/architecture-import-boundary.md), [architecture audit](docs/features/parque-taquaral-online-mvp/ARCHITECTURE-AUDIT.md), [discovery summary](docs/features/parque-taquaral-online-mvp/DISCOVERY.md), [DomainSpec coverage](docs/features/parque-taquaral-online-mvp/PILOT-DOMAINSPEC-COVERAGE.md), [DomainSpec backlog](docs/features/parque-taquaral-online-mvp/PILOT-DOMAINSPEC-BACKLOG.md).

## Contexts

### <a id="context-ctx-body-war-root"></a>CTX-BODY-WAR-ROOT - Body War MVP Readiness

- Stage: `review-audit`
- Gate: `flag`
- Purpose: track Body War MVP decisions, blockers, gaps, route evidence, and recomposition while the product moves from prototype evidence to governed architecture.

#### <a id="next-move"></a>Next Move

Execute the Parque Taquaral online MVP W0 spec baseline from
`WORK-PACK.md`: write the P0 specs and contracts before mutating
`projects/body-war/app/`.

### <a id="context-ctx-body-war-arch-audit"></a>CTX-BODY-WAR-ARCH-AUDIT - Parque Taquaral Architecture Review Audit

- Stage: `closed`
- Gate: `pass`
- Closure evidence: [ARCHITECTURE-AUDIT.md](docs/features/parque-taquaral-online-mvp/ARCHITECTURE-AUDIT.md)
- Selected boundary: Body War-owned TypeScript workspace with DomainSpec path alias.

## Blockers

### <a id="blocker-blk-strava-activity-001"></a>BLK-STRAVA-ACTIVITY-001

- Lane: `validator`
- Status: `active`, `refined`
- Summary: OAuth has passed, but real activity import/submission evidence is still missing.
- Closure: import and submit one real Strava run without exposing tokens.
- Route: `task-session`

## Decisions

### <a id="decision-dec-arch-boundary-001"></a>DEC-ARCH-BOUNDARY-001

- Question: Which TypeScript architecture/import boundary will Body War use to consume DomainSpec methods?
- Status: `closed`, no longer blocking MVP implementation planning.
- Selected: Body War-owned TypeScript workspace with a DomainSpec path alias.
- Rationale: fastest MVP path while preserving DomainSpec as method authority through explicit path aliases or source references.
- Impact: MVP implementation can proceed in a Body War-owned TypeScript workspace; shared DomainSpec package extraction remains future hardening.
- Evidence: [architecture-import-boundary.md](docs/decisions/architecture-import-boundary.md), [ARCHITECTURE-AUDIT.md](docs/features/parque-taquaral-online-mvp/ARCHITECTURE-AUDIT.md)

## Gaps

### <a id="gap-gap-taquaral-geometry-001"></a>GAP-TAQUARAL-GEOMETRY-001

- Severity: `flag`
- Treatment: `defer`
- Summary: Parque Taquaral has no sourced track geometry or lap boundary yet.

### <a id="gap-gap-domainspec-export-001"></a>GAP-DOMAINSPEC-EXPORT-001

- Severity: `flag`
- Treatment: `defer`
- Status: `resolved` for MVP by path-alias/source-reference consumption.
- Summary: shared typed package remains future hardening.

## Route Evidence

- Dispatch validation pass: [20260610-body-war-parque-taquaral-review-audit.dispatch.json](development/dispatches/20260610-body-war-parque-taquaral-review-audit.dispatch.json)
- Craft refine/validate/summary dispatch: [20260610-body-war-craft-refine-validate-summary.dispatch.json](development/dispatches/20260610-body-war-craft-refine-validate-summary.dispatch.json)
- Audit spec: [20260610-body-war-parque-taquaral-review-audit.spec.md](development/dispatches/20260610-body-war-parque-taquaral-review-audit.spec.md)
- Victor-style discovery summary: [DISCOVERY.md](docs/features/parque-taquaral-online-mvp/DISCOVERY.md)
- One-shot decision/spec forecast: [MVP-ONESHOT-FORECAST.md](docs/features/parque-taquaral-online-mvp/MVP-ONESHOT-FORECAST.md)
- DomainSpec gap coverage: [PILOT-DOMAINSPEC-COVERAGE.md](docs/features/parque-taquaral-online-mvp/PILOT-DOMAINSPEC-COVERAGE.md)
- DomainSpec spec backlog: [PILOT-DOMAINSPEC-BACKLOG.md](docs/features/parque-taquaral-online-mvp/PILOT-DOMAINSPEC-BACKLOG.md)
- Invoke design: [DESIGN.md](docs/features/parque-taquaral-online-mvp/DESIGN.md)
- Invoke implementation layering: [IMPLEMENTATION-LAYERING.md](docs/features/parque-taquaral-online-mvp/IMPLEMENTATION-LAYERING.md)
- Invoke work-pack: [WORK-PACK.md](docs/features/parque-taquaral-online-mvp/WORK-PACK.md)
- Invoke execution pack: [EXECUTION-PACK.md](docs/features/parque-taquaral-online-mvp/EXECUTION-PACK.md)
- Architecture decision: [architecture-import-boundary.md](docs/decisions/architecture-import-boundary.md)
- Architecture audit: [ARCHITECTURE-AUDIT.md](docs/features/parque-taquaral-online-mvp/ARCHITECTURE-AUDIT.md)

Important boundary: dispatch pass is route-shape evidence only. It is not
implementation readiness.

## Recomposition

[CTX-BODY-WAR-ARCH-AUDIT](#context-ctx-body-war-arch-audit) recomposed into
[CTX-BODY-WAR-ROOT](#context-ctx-body-war-root) with the selected TypeScript
boundary and architecture audit evidence. Remaining residue:
[BLK-STRAVA-ACTIVITY-001](#blocker-blk-strava-activity-001) and
[GAP-TAQUARAL-GEOMETRY-001](#gap-gap-taquaral-geometry-001).
