# Body War Craft Ledger

Human-readable view of [.craft/ledger.yml](.craft/ledger.yml). The ledger is the
source of truth; this page is an indexed navigation surface.

## Quick Links

- Current next move: [configure Hostinger Traefik deploy for online testing](#next-move).
- Active blocker: [BLK-STRAVA-ACTIVITY-001](#blocker-blk-strava-activity-001).
- Active gaps: [GAP-TAQUARAL-GEOMETRY-001](#gap-gap-taquaral-geometry-001), [GAP-TROQAR-PAGE-PRIORITY-001](#gap-gap-troqar-page-priority-001), [GAP-TROQAR-SCORE-AUTHORITY-001](#gap-gap-troqar-score-authority-001), [GAP-TROQAR-BACKEND-PROVIDER-001](#gap-gap-troqar-backend-provider-001), [GAP-TROQAR-GLOSSARY-PROMOTION-001](#gap-gap-troqar-glossary-promotion-001).
- Closed architecture decision: [DEC-ARCH-BOUNDARY-001](#decision-dec-arch-boundary-001).
- Auth-first decision: [DEC-BODY-WAR-AUTH-FIRST-001](#decision-dec-body-war-auth-first-001).
- Auth/user-management route: [REFINE-DISPATCH.json](../auth-user-management/development/refinement-runs/20260621T025133Z-auth-strava-foundation/REFINE-DISPATCH.json), [RESULT.md](../auth-user-management/development/refinement-runs/20260621T025133Z-auth-strava-foundation/RESULT.md), [TypeScript one-shot result](../../development/refinement-runs/20260621T-typescript-domainspec-invariant/task-session/20260621T-auth-workpack-oneshot/RESULT.md).
- TROQAR product architecture: [packet README](docs/features/troqar-product-architecture/README.md), [operations/capabilities](docs/features/troqar-product-architecture/OPERATIONS-CAPABILITIES.md), [DomainSpec SPEC](docs/features/troqar-product-architecture/SPEC.md), [UI/UX](docs/features/troqar-product-architecture/ui-spec.md), [backend](docs/features/troqar-product-architecture/backend.md), [gap review](docs/features/troqar-product-architecture/GAP-BLOCKER-REVIEW.md).
- TROQAR refine route: [REFINE-DISPATCH.json](development/refinement-runs/20260621T-troqar-product-architecture-gap-review/REFINE-DISPATCH.json), [RESULT.md](development/refinement-runs/20260621T-troqar-product-architecture-gap-review/RESULT.md).
- TROQAR production login UI: [task-session RESULT.md](development/task-sessions/20260622T125002Z-production-ui-login/RESULT.md), [UI-REVIEW.md](docs/features/troqar-product-architecture/UI-REVIEW.md), [production handoff bundle](docs/features/troqar-product-architecture/prototype-handoff/PRODUCTION-LOGIN-HANDOFF-BUNDLE.json).
- TROQAR online deploy: [manual](docs/ONLINE-DEPLOY-MANUAL.md), [Traefik task session](development/task-sessions/20260622T140208Z-traefik-secret-blind-deploy/TASK-SESSION-RESULT.md), [secret inventory](infra/SECRET-INVENTORY.md).
- Suggested track expansion child node: [CTX-BODY-WAR-SUGGESTED-TRACKS](#context-ctx-body-war-suggested-tracks), [architecture plan](development/refinement-runs/20260624T010822Z-suggested-track-expansion-route/ARCHITECTURE-PLAN.md), [decision-build result](development/refinement-runs/20260629T050046Z-suggested-track-decision-build-route/RESULT.md), [one-go Task Session result](development/task-sessions/20260629T061500Z-suggested-track-one-go-build/TASK-SESSION-RESULT.md).
- One-shot forecast: [MVP-ONESHOT-FORECAST.md](docs/features/parque-taquaral-online-mvp/MVP-ONESHOT-FORECAST.md).
- Invoke design/plan: [DESIGN.md](docs/features/parque-taquaral-online-mvp/DESIGN.md), [WORK-PACK.md](docs/features/parque-taquaral-online-mvp/WORK-PACK.md), [EXECUTION-PACK.md](docs/features/parque-taquaral-online-mvp/EXECUTION-PACK.md).
- Key artifacts: [architecture decision](docs/decisions/architecture-import-boundary.md), [architecture audit](docs/features/parque-taquaral-online-mvp/ARCHITECTURE-AUDIT.md), [discovery summary](docs/features/parque-taquaral-online-mvp/DISCOVERY.md), [DomainSpec coverage](docs/features/parque-taquaral-online-mvp/PILOT-DOMAINSPEC-COVERAGE.md), [DomainSpec backlog](docs/features/parque-taquaral-online-mvp/PILOT-DOMAINSPEC-BACKLOG.md).

## Contexts

### <a id="context-ctx-body-war-root"></a>CTX-BODY-WAR-ROOT - Body War MVP Readiness

- Stage: `auth-consumer-implemented`
- Gate: `flag`
- Purpose: track Body War MVP decisions, blockers, gaps, route evidence, and recomposition while the product moves from prototype evidence to governed architecture.

#### <a id="next-move"></a>Next Move

Use the production login UI as the hosted preview entry surface. Next, configure
the Hostinger Traefik deployment manually from [ONLINE-DEPLOY-MANUAL.md](docs/ONLINE-DEPLOY-MANUAL.md),
then run the online deploy receipt before validating real Strava activity
import/submission without exposing tokens. Keep sourced geometry and game
mechanics deferred until real evidence is available.

### <a id="context-ctx-body-war-arch-audit"></a>CTX-BODY-WAR-ARCH-AUDIT - Parque Taquaral Architecture Review Audit

- Stage: `closed`
- Gate: `pass`
- Closure evidence: [ARCHITECTURE-AUDIT.md](docs/features/parque-taquaral-online-mvp/ARCHITECTURE-AUDIT.md)
- Selected boundary: Body War-owned TypeScript workspace with DomainSpec path alias.

### <a id="context-ctx-body-war-suggested-tracks"></a>CTX-BODY-WAR-SUGGESTED-TRACKS - Suggested Track Expansion

- Stage: `one-go-build-complete`
- Gate: `flag`
- Purpose: govern user-suggested tracks, live Strava consult, consented evidence attachment, and eventual promotion from suggestion to source-backed track.
- Next move: use the implemented SuggestedTrack flow in hosted preview testing to collect real consented Strava activity evidence; keep source-backed geometry and pilot-ready promotion deferred.
- Evidence: [ARCHITECTURE-PLAN.md](development/refinement-runs/20260624T010822Z-suggested-track-expansion-route/ARCHITECTURE-PLAN.md), [original route result](development/refinement-runs/20260624T010822Z-suggested-track-expansion-route/RESULT.md), [decision-build RESULT.md](development/refinement-runs/20260629T050046Z-suggested-track-decision-build-route/RESULT.md), [decision-build RUNTIME-HANDOFF.md](development/refinement-runs/20260629T050046Z-suggested-track-decision-build-route/RUNTIME-HANDOFF.md), [S09 Invoke Plan](development/refinement-runs/20260629T050046Z-suggested-track-decision-build-route/stages/S09-INVOKE-PLAN.md), [one-go Task Session result](development/task-sessions/20260629T061500Z-suggested-track-one-go-build/TASK-SESSION-RESULT.md)

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

### <a id="decision-dec-body-war-auth-first-001"></a>DEC-BODY-WAR-AUTH-FIRST-001

- Question: What should Body War prioritize before track geometry and game mechanics?
- Status: `closed`, not blocking.
- Selected: `auth-user-management-first`
- Rationale: login/auth and Strava connection are the smallest production
  prerequisite for a usable hosted preview, and the reusable auth project can
  serve later projects.
- Impact: the next move shifts from broad track/game W0 execution to real
  Strava activity validation through the auth-backed pilot.
- Evidence: [auth-user-management result](../auth-user-management/development/refinement-runs/20260621T025133Z-auth-strava-foundation/RESULT.md)

## TROQAR Product Architecture

The app-wide TROQAR design packet now lists operations and capabilities first,
then anchors the DomainSpec domain, page inventory, UI/UX, visual definitions,
backend contracts, and local gap/blocker review.

- Packet: [README.md](docs/features/troqar-product-architecture/README.md)
- Operations: [OPERATIONS-CAPABILITIES.md](docs/features/troqar-product-architecture/OPERATIONS-CAPABILITIES.md)
- DomainSpec: [SPEC.md](docs/features/troqar-product-architecture/SPEC.md), [domain.md](docs/features/troqar-product-architecture/domain.md), [operations.md](docs/features/troqar-product-architecture/operations.md), [queries.md](docs/features/troqar-product-architecture/queries.md), [states.md](docs/features/troqar-product-architecture/states.md), [interfaces.md](docs/features/troqar-product-architecture/interfaces.md), [events.md](docs/features/troqar-product-architecture/events.md), [mappings.md](docs/features/troqar-product-architecture/mappings.md)
- Product design: [ARCHITECTURE.md](docs/features/troqar-product-architecture/ARCHITECTURE.md), [ui-spec.md](docs/features/troqar-product-architecture/ui-spec.md), [VISUAL-DEFINITIONS.md](docs/features/troqar-product-architecture/VISUAL-DEFINITIONS.md), [backend.md](docs/features/troqar-product-architecture/backend.md)
- Refine residue: [GAP-BLOCKER-REVIEW.md](docs/features/troqar-product-architecture/GAP-BLOCKER-REVIEW.md), [REFINE-DISPATCH.json](development/refinement-runs/20260621T-troqar-product-architecture-gap-review/REFINE-DISPATCH.json)
- Production login UI: [task-session RESULT.md](development/task-sessions/20260622T125002Z-production-ui-login/RESULT.md), [UI-REVIEW.md](docs/features/troqar-product-architecture/UI-REVIEW.md), [PRODUCTION-LOGIN-HANDOFF-BUNDLE.json](docs/features/troqar-product-architecture/prototype-handoff/PRODUCTION-LOGIN-HANDOFF-BUNDLE.json)

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

### <a id="gap-gap-troqar-page-priority-001"></a>GAP-TROQAR-PAGE-PRIORITY-001

- Severity: `flag`
- Treatment: `invoke-plan`
- Summary: app-wide pages are defined, but the first implementation order is
  not selected.

### <a id="gap-gap-troqar-score-authority-001"></a>GAP-TROQAR-SCORE-AUTHORITY-001

- Severity: `flag`
- Treatment: `decision-gate`
- Summary: Zone Score and fastest-time controller authority need an explicit
  rule before full territory scoring implementation.

### <a id="gap-gap-troqar-backend-provider-001"></a>GAP-TROQAR-BACKEND-PROVIDER-001

- Severity: `flag`
- Treatment: `invoke-plan`
- Summary: hosted runtime, managed storage, secret store, and provider/schema
  choices are not selected.

### <a id="gap-gap-troqar-glossary-promotion-001"></a>GAP-TROQAR-GLOSSARY-PROMOTION-001

- Severity: `note`
- Treatment: `definitions-governance`
- Summary: app-wide TROQAR product architecture terms remain local candidate
  definitions until promoted to a canonical glossary.

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
- Auth/user-management strategy: [REFINE-DISPATCH.json](../auth-user-management/development/refinement-runs/20260621T025133Z-auth-strava-foundation/REFINE-DISPATCH.json)
- Auth/user-management result: [RESULT.md](../auth-user-management/development/refinement-runs/20260621T025133Z-auth-strava-foundation/RESULT.md)
- Auth/user-management implementation: [TypeScript one-shot RESULT.md](../../development/refinement-runs/20260621T-typescript-domainspec-invariant/task-session/20260621T-auth-workpack-oneshot/RESULT.md)
- TROQAR product architecture packet: [README.md](docs/features/troqar-product-architecture/README.md)
- TROQAR local gap/blocker review: [GAP-BLOCKER-REVIEW.md](docs/features/troqar-product-architecture/GAP-BLOCKER-REVIEW.md)
- TROQAR formal refine route: [REFINE-DISPATCH.json](development/refinement-runs/20260621T-troqar-product-architecture-gap-review/REFINE-DISPATCH.json)
- TROQAR production login task-session: [RESULT.md](development/task-sessions/20260622T125002Z-production-ui-login/RESULT.md)
- TROQAR production login review: [UI-REVIEW.md](docs/features/troqar-product-architecture/UI-REVIEW.md)
- TROQAR production Studio handoff: [PRODUCTION-LOGIN-HANDOFF-BUNDLE.json](docs/features/troqar-product-architecture/prototype-handoff/PRODUCTION-LOGIN-HANDOFF-BUNDLE.json)
- Suggested track architecture plan: [ARCHITECTURE-PLAN.md](development/refinement-runs/20260624T010822Z-suggested-track-expansion-route/ARCHITECTURE-PLAN.md)
- Suggested track refine route: [REFINE-DISPATCH.json](development/refinement-runs/20260624T010822Z-suggested-track-expansion-route/REFINE-DISPATCH.json)
- Suggested track runtime handoff: [RUNTIME-HANDOFF.md](development/refinement-runs/20260624T010822Z-suggested-track-expansion-route/RUNTIME-HANDOFF.md)
- Suggested track one-go build result: [TASK-SESSION-RESULT.md](development/task-sessions/20260629T061500Z-suggested-track-one-go-build/TASK-SESSION-RESULT.md)

Important boundary: dispatch pass is route-shape evidence only. It is not
implementation readiness.

## Recomposition

[CTX-BODY-WAR-ARCH-AUDIT](#context-ctx-body-war-arch-audit) recomposed into
[CTX-BODY-WAR-ROOT](#context-ctx-body-war-root) with the selected TypeScript
boundary and architecture audit evidence. Remaining residue:
[BLK-STRAVA-ACTIVITY-001](#blocker-blk-strava-activity-001) and
[GAP-TAQUARAL-GEOMETRY-001](#gap-gap-taquaral-geometry-001).

The auth/user-management implementation has recomposed into Body War as a first
consumer slice: login, server-owned session, user identity, Strava connection,
and recent activity summary import. Track geometry and game mechanics remain
deferred.

The TROQAR product architecture packet has recomposed into Body War as the
current app-wide design surface. The production login-first UI task-session has
now implemented and validated the hosted-preview entry surface with Studio
handoff evidence and 7 Playwright checks. Remaining residue is not UI-blocking:
real Strava activity evidence, sourced geometry, score authority, backend
provider choice, broader page order, and glossary promotion remain open.

Suggested track expansion is now a child node under Body War. It keeps Taquaral
as the first seeded suggestion. The confirmed decision-build route now supersedes
the Slice 1-only next move: the next Task Session starts with a docs/work-pack
preflight gate, then builds docs, Drizzle schema, generated migration, seed, API,
UI, and tests in one pass. Source-backed geometry, pilot-ready status, territory
scoring, and real activity evidence remain outside that build until separate
evidence closes them.
