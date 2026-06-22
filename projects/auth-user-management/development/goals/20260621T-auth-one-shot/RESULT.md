# Goal Result - Auth One-Shot

- Goal: `ONE-SHOT-AUTH-FOUNDATION-001`
- Status: `implemented`
- Runtime package: `projects/auth-user-management/src/auth_user_management/`
- Body War consumer: `projects/body-war/app/server.py`

## Implemented Units

| Unit | Result |
|---|---|
| `SWU-AUTH-001` | Added core Principal, Session, AccessToken, PermissionGrant, AuthContext, ProviderAccount, ProviderToken, AuditEvent, and permission behavior. |
| `SWU-AUTH-002` | Added browser cookie session guard with signed session cookie, CSRF cookie/header binding, same-origin check, permission/resource guard, logout revocation, and tests. |
| `SWU-AUTH-003` | Added bearer `sid` guard with HMAC token, persisted `jti`, expiry, revocation, missing `sid`, and inactive-session tests. |
| `SWU-AUTH-004` | Added in-memory and JSON-backed storage adapter contract with session/token/provider/OAuth-state records. |
| `SWU-AUTH-005` | Added Strava adapter with OAuth state, callback, scope validation, server-side token custody, refresh, and redacted activity summaries. |
| `SWU-AUTH-006` | Added adoption guide, validation commands, and copy-boundary notes. |
| `SWU-BW-AUTH-001` | Wired Body War Python pilot to reusable browser guard and Strava provider adapter without track/game/scoring changes. |

## Validation Evidence

Validation commands are recorded in the final runtime response and should include:

- auth unittest discovery,
- Body War `py_compile`,
- Body War unittest discovery,
- JSON/YAML parse checks,
- markdown link checks,
- scoped `git diff --check`.

## Boundaries Preserved

- No real Strava tokens, secrets, authorization codes, or raw private athlete
  data were added to tracked artifacts.
- `validation/poker-team`, Savvy, and public `arcanum` were not modified.
- Track geometry, scoring, game mechanics, anti-cheat, payments, RunCoins,
  premium, and sponsor mechanics stayed out of scope.

## Residue

Production deployment still needs a selected database or managed secret store.
The local JSON store is a pilot adapter and must remain behind `.gitignore` when
it contains real provider tokens.
