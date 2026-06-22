# API E2E Scenario Matrix

## Harness Contract

The E2E program must import from `./src/index.js` when compiled inside the package, not from deep private paths unless it is using package-owned E2E setup helpers. This proves that consumers can use the exported API surface.

Database setup is allowed to import `authAccessControlSchema` and use raw SQL setup helpers because schema ownership belongs to this package.

## Scenario A - Bootstrap And Catalog

Capabilities:

- `seedSystemBootstrap`
- `getPermissionCatalogUseCase`
- Drizzle principal and grant repositories

Assertions:

- Bootstrap creates an admin principal when none exists.
- Bootstrap hashes the supplied admin password with PBKDF2.
- Bootstrap upserts all supplied role definitions.
- Re-running bootstrap is idempotent for existing grants.
- Password refresh updates the credential when `adminPassword` is supplied for an existing admin.
- Permission catalog deduplicates repeated grants.
- Permission catalog namespace filtering returns only matching permissions.
- No console output includes plaintext passwords.

## Scenario B - Login Success And Token Issuance

Capabilities:

- `loginUseCase`
- `issueAccessTokenUseCase`
- `createPbkdf2PasswordService`
- `createHmacTokenCodec`
- Drizzle principal, grant, session, and token repositories

Assertions:

- Login with valid credentials creates one active session.
- Effective permissions include role grants and direct principal permissions with duplicates removed.
- Login emits `TokenIssued` and `LoginSucceeded` events.
- Token row persists `tokenId`, `sessionId`, `expiresAt`, and scope.
- Issuing a second access token for the active session works within TTL bounds.
- TTL below minimum throws `FORBIDDEN`.
- TTL above maximum throws `FORBIDDEN`.
- Issuing a token for a missing or terminated session throws `AUTH_REQUIRED`.

## Scenario C - Login Denial And Risk Policy

Capabilities:

- `loginUseCase`
- login risk policy through public input

Assertions:

- Missing identifier or secret throws `INVALID_CREDENTIALS`.
- Unknown principal throws `PRINCIPAL_DISABLED`, matching current package behavior.
- Disabled principal throws `PRINCIPAL_DISABLED`.
- Wrong password throws `INVALID_CREDENTIALS`.
- Blocked IP reputation throws `FORBIDDEN`.
- Missing user-agent risk context throws the expected denial if current policy requires it.

## Scenario D - Authentication

Capabilities:

- `authenticateRequestUseCase`
- `createHmacTokenCodec`
- Drizzle session and token repositories

Assertions:

- Valid bearer token returns an `AuthContext` with principal, session, token, permission, issued-at, and expires-at data.
- Missing authorization header throws `AUTH_REQUIRED`.
- Non-bearer or malformed token throws `INVALID_TOKEN`.
- Expired signed token throws `TOKEN_EXPIRED`.
- Signed token with unknown `jti` throws `INVALID_TOKEN`.
- Revoked token throws `TOKEN_REVOKED`.
- Token tied to terminated session throws `AUTH_REQUIRED`.
- Token tied to expired session throws `AUTH_REQUIRED`.

## Scenario E - Authorization

Capabilities:

- `authorizeRequestUseCase`
- permission resolution and deny override

Assertions:

- Exact permission grants allow the request.
- Wildcard role grants allow scoped child permissions.
- Principal-level deny grant overrides an allowed session permission.
- Denial emits `AccessDenied`.
- Non-canonical permission keys throw `FORBIDDEN`.

## Scenario F - Logout And Revocation

Capabilities:

- `logoutUseCase`
- Drizzle session and token repositories

Assertions:

- Session owner can revoke a targeted token.
- Targeted logout marks the token revoked and terminates the session.
- Admin permission can revoke another principal's session.
- Caller without ownership or admin permission throws `FORBIDDEN`.
- All-session-token logout revokes every active token for the session.
- Logout for missing, expired, or terminated session throws `AUTH_REQUIRED`.
- Revocation emits `TokenRevoked` and `LogoutCompleted` events.

## Scenario G - Token Introspection

Capabilities:

- `introspectTokenUseCase`
- inactive reason policy through persisted token and session state

Assertions:

- Active token returns `active: true`, principal id, `iat`, `exp`, and scopes.
- `includeScopes: false` omits scopes.
- Malformed token returns `NOT_FOUND`.
- Unknown `jti` returns `NOT_FOUND`.
- Revoked token returns `TOKEN_REVOKED`.
- Expired token returns `TOKEN_EXPIRED` unless revocation has precedence in current policy.
- Token with terminated or expired session returns the current session inactive reason.

## Scenario H - Public Export Smoke

Capabilities:

- `src/index.ts` package export surface

Assertions:

- E2E program imports only public auth functions and types from `src/index.js`.
- `createMemoryAuthRepositories` remains importable but is not the primary E2E persistence path.
- Drizzle schema and repository factory are importable from the public package surface.
