# Auth User Management Craft Ledger

Human-readable view of [.craft/ledger.yml](.craft/ledger.yml). The ledger is
the source of truth; this page is an indexed navigation surface.

## Quick Links

- Current next move: [select production custody backend](#next-move).
- Closed transport decision: [DEC-AUTH-TRANSPORT-001](#decision-dec-auth-transport-001).
- Closed provider decision: [DEC-AUTH-STRAVA-SCOPE-001](#decision-dec-auth-strava-scope-001).
- Resolved gaps: [GAP-AUTH-COPY-BOUNDARY-001](#gap-gap-auth-copy-boundary-001), [GAP-STRAVA-PROVIDER-CONTRACT-001](#gap-gap-strava-provider-contract-001).
- Refine packet: [REFINE-SEED-PROPOSAL.md](development/refinement-runs/20260621T025133Z-auth-strava-foundation/REFINE-SEED-PROPOSAL.md), [REFINE-DISPATCH.json](development/refinement-runs/20260621T025133Z-auth-strava-foundation/REFINE-DISPATCH.json), [RUNTIME-HANDOFF.md](development/refinement-runs/20260621T025133Z-auth-strava-foundation/RUNTIME-HANDOFF.md).
- Runtime implementation: [GOAL-PROFILE.md](development/goals/20260621T-auth-one-shot/GOAL-PROFILE.md), [goal RESULT.md](development/goals/20260621T-auth-one-shot/RESULT.md), [ADOPTION.md](docs/ADOPTION.md).
- Key references: [poker-team auth spec](../../validation/poker-team/docs/features/auth-access-control/SPEC.md), [Savvy cookie guard](../savvy_legal-studio-ai/frontend/savvy-legal-studio/lib/auth/savvy-auth.ts), [Body War Strava work-pack](../body-war/docs/features/strava-linked-pilot/WORK-PACK.md).

## Contexts

### <a id="context-ctx-auth-um-root"></a>CTX-AUTH-UM-ROOT - Auth User Management Foundation

- Stage: `implemented`
- Gate: `pass`
- Purpose: design a reusable login, session, permission, user-management, and provider-connection foundation that Body War can consume first for Strava OAuth before track and game features resume.

#### <a id="next-move"></a>Next Move

Select a production database/secret backend before hosted deployment. For local
reuse and Body War pilot integration, use [ADOPTION.md](docs/ADOPTION.md).

## Enablers

### ENA-POKER-AUTH-REFERENCE-001

- Lane: `architecture`
- Summary: `validation/poker-team` provides the strongest local auth domain and use-case reference: server sessions, `sid`-based token claims, revocation, authorization, permissions, and telemetry.
- Boundary: reuse concepts and patterns, not poker-specific roles or product assumptions.

### ENA-SAVVY-COOKIE-GUARD-001

- Lane: `security`
- Summary: Savvy provides a useful browser-session guard proof with cookie, CSRF, server session store, resource scope, deny-by-default behavior, and tests.
- Boundary: keep the cookie/session safety proof; do not copy mock 2FA or client-asserted `authStatus` weaknesses.

## Decisions

### <a id="decision-dec-auth-transport-001"></a>DEC-AUTH-TRANSPORT-001

- Question: What production session transport should the reusable foundation standardize first?
- Status: `closed`
- Selected: `hybrid-cookie-for-browser-bearer-for-service-api`
- Options: `http-only-cookie-session-with-csrf-and-server-session-store`, `bearer-jwt-with-sid-and-server-session-token-records`, `hybrid-cookie-for-browser-bearer-for-service-api`
- Rationale: browser flows use HttpOnly cookie sessions, CSRF binding, same-origin checks, and server session lookup; service/API flows may use bearer JWTs only when the server-backed `sid` remains authoritative.

### <a id="decision-dec-auth-strava-scope-001"></a>DEC-AUTH-STRAVA-SCOPE-001

- Question: What is the minimum Strava provider capability for Body War's first auth consumer slice?
- Status: `closed`
- Selected: `link-identity-and-import-recent-activity-summaries`
- Options: `link-strava-identity-only`, `link-identity-and-import-recent-activity-summaries`, `link-identity-and-store-refreshable-activity-access`
- Scope: default `read,activity:read`; escalate to `activity:read_all` only for explicit consenting-athlete private activity import.

## Gaps

### <a id="gap-gap-auth-copy-boundary-001"></a>GAP-AUTH-COPY-BOUNDARY-001

- Severity: `flag`
- Treatment: `refine`
- Status: `resolved`
- Summary: The copyable package boundary is not defined yet; the project must separate reusable auth core, app adapter, provider adapter, storage adapter, migrations, tests, and adoption docs.

### <a id="gap-gap-strava-provider-contract-001"></a>GAP-STRAVA-PROVIDER-CONTRACT-001

- Severity: `flag`
- Treatment: `refine`
- Status: `resolved`
- Summary: The Strava OAuth provider contract needs state/PKCE, callback, token custody, refresh, revocation, scope minimization, redacted audit, and test fixtures before implementation.

### GAP-AUTH-PRODUCTION-CUSTODY-001

- Severity: `note`
- Treatment: `defer`
- Status: `deferred`
- Summary: hosted production deployment still needs an explicit database and
  managed secret/token custody backend; the JSON store is local-pilot only.

## Runtime Package

- Core domain: `src/modules/auth/domain/`
- Browser guard: `src/modules/auth/interface/browser-session.ts`
- Bearer guard: `src/modules/auth/interface/bearer-token.ts`
- Storage adapters: `src/modules/auth/infrastructure/`
- Strava provider: `src/modules/providers/strava/`
- Tests: `tests/`
- Adoption guide: [ADOPTION.md](docs/ADOPTION.md)

## Route Evidence

- Seed proposal: [REFINE-SEED-PROPOSAL.md](development/refinement-runs/20260621T025133Z-auth-strava-foundation/REFINE-SEED-PROPOSAL.md)
- Dispatch route: [REFINE-DISPATCH.json](development/refinement-runs/20260621T025133Z-auth-strava-foundation/REFINE-DISPATCH.json)
- Runtime handoff: [RUNTIME-HANDOFF.md](development/refinement-runs/20260621T025133Z-auth-strava-foundation/RUNTIME-HANDOFF.md)
- Run manifest: [RUN-MANIFEST.md](development/refinement-runs/20260621T025133Z-auth-strava-foundation/RUN-MANIFEST.md)
- Evidence index: [evidence-index.json](development/refinement-runs/20260621T025133Z-auth-strava-foundation/evidence-index.json)
- Result: [RESULT.md](development/refinement-runs/20260621T025133Z-auth-strava-foundation/RESULT.md)
- One-shot profile: [GOAL-PROFILE.md](development/goals/20260621T-auth-one-shot/GOAL-PROFILE.md)
- One-shot result: [RESULT.md](development/goals/20260621T-auth-one-shot/RESULT.md)

Important boundary: the refine packet is planning evidence; the one-shot result
and runtime package are implementation evidence.

## Recomposition

This context has recomposed into Body War through the TypeScript pilot server:
reusable login/session/user-management plus a Strava provider connection. Track
geometry and game mechanics remain deferred.

Next parent move: validate with a real consenting Strava activity in the pilot
environment without exposing tokens.
