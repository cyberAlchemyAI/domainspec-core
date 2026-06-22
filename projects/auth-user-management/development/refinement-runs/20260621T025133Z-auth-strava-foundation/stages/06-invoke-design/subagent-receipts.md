# Delegated Lane Receipts

## auth-domain-porter

- Agent id: `019ee81e-8c50-70f1-89ab-ebfbe83e3969`
- Status: `flag`
- Artifacts considered:
  - `validation/poker-team/docs/features/auth-access-control/SPEC.md`
  - `validation/poker-team/docs/features/auth-access-control/interfaces.md`
  - `validation/poker-team/docs/features/auth-access-control/domain.md`
  - `validation/poker-team/docs/features/auth-access-control/operations.md`
  - `validation/poker-team/docs/features/auth-access-control/states.md`
  - `validation/poker-team/docs/features/auth-access-control/TEST-SPEC.md`
  - `validation/poker-team/backend/src/domain/auth-access-control/*.ts`
  - `validation/poker-team/backend/src/use-cases/auth-access-control/*.ts`
- Transfer: Principal, Session, AccessToken, PermissionGrant, AuthContext,
  AuthErrorCode, `sid` as session authority, login/session/token flow,
  authenticate-before-authorize, deny-by-default permissions, token
  introspection, P0 test gates.
- Do not transfer: poker roles, poker permission namespaces, fixed TTLs,
  bootstrap password logging, bearer-only assumption, `JWT_SECRET` fallback.
- Lane recommendation: bearer is proven locally, but parent should reconcile
  with browser-session lane before final transport.

## browser-session-security

- Agent id: `019ee81e-8ce7-7980-a8ba-ae5b851dbce8`
- Status: `flag`
- Artifacts considered:
  - `projects/savvy_legal-studio-ai/frontend/savvy-legal-studio/lib/auth/savvy-auth.ts`
  - `projects/savvy_legal-studio-ai/frontend/savvy-legal-studio/tests/auth/savvy-auth.test.ts`
  - `projects/savvy_legal-studio-ai/frontend/savvy-legal-studio/app/api/auth/verify-2fa/route.ts`
  - `projects/savvy_legal-studio-ai/research/production-readiness/2026-06-17-understanding/findings.md`
  - `projects/savvy_legal-studio-ai/research/production-readiness/2026-06-17-understanding/research.md`
- Transfer: cookie session id, server session store lookup, session
  expiry/revocation, permission check, resource scope, audit context,
  same-origin and CSRF binding, deny-by-default errors, guard tests.
- Do not transfer: mock 2FA route, client-supplied `authStatus`, privileged
  localStorage state, JSON fixture session store as production backing.
- Lane recommendation: extract a generic cookie-session/CSRF guard contract and
  port the tests first.

## strava-provider-integration

- Agent id: `019ee81e-8e04-74b2-a1f8-63c2f6183f63`
- Status: `flag`
- Artifacts considered:
  - `projects/body-war/.craft/ledger.yml`
  - `projects/body-war/CRAFT.md`
  - `projects/body-war/docs/features/strava-linked-pilot/SPEC.md`
  - `projects/body-war/docs/features/strava-linked-pilot/IMPLEMENTATION-LAYERING.md`
  - `projects/body-war/docs/features/strava-linked-pilot/WORK-PACK.md`
  - `projects/body-war/docs/features/parque-taquaral-online-mvp/WORK-PACK.md`
  - `projects/auth-user-management/CRAFT.md`
- Recommendation: select `link-identity-and-import-recent-activity-summaries`
  for the first Body War consumer. Default OAuth scope is
  `read,activity:read`; escalate to `activity:read_all` only for consenting
  private or Only Me activity import.
- Provider contract: auth owns user/session/provider link; Strava adapter owns
  OAuth start/callback, scope verification, athlete id, connection status,
  activity summary import, refresh/revoke/disconnect, and redacted outputs.
- Token custody: no real secrets or tokens in repo artifacts; store provider
  tokens server-side in sealed managed storage for hosted preview.

## Parent Join

All lanes completed and closed. Their content verdicts are `flag` because they
correctly identify implementation blockers and anti-patterns. The lifecycle
join is complete and usable for parent synthesis.
