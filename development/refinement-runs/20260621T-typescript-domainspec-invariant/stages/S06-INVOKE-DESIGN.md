# S06 - Invoke Design

Owner: `invoke`
Mode: `design`
Verdict: `pass`

## Design Summary

Build `projects/auth-user-management` as a DomainSpec-style Functional TypeScript package. Use shell scripts for deterministic validation and repo policy checks. Use TypeScript for all runtime/domain/application/provider behavior.

## Six Required Design Views

### 1. Context View

```text
---------------------+       +----------------------------+
| Browser Consumer   | ----> | auth-user-management       |
| Body War first     |       | TypeScript package         |
+---------------------+       +-------------+--------------+
                                           |
                                           v
                              +------------+-------------+
                              | Strava OAuth/API         |
                              | via provider gateway     |
                              +--------------------------+
```

Body War needs login, session continuity, Strava linking, activity import authorization, and logout. Tracks/game mechanics remain separate consumers of the resulting auth context later.

### 2. High-Level Structure View

```text
projects/auth-user-management/
  package.json
  tsconfig.json
  scripts/
    validate.sh
  src/
    modules/
      auth/
        domain/
        application/
        infrastructure/
        interface/
      providers/
        strava/
          domain/
          application/
          infrastructure/
          interface/
    shared/
  tests/
```

### 3. Low-Level Components View

Domain:

- `principal.entity.ts`
- `session.entity.ts`
- `access-token.entity.ts`
- `permission.type.ts`
- `authorization.policy.ts`
- `session-lifecycle.policy.ts`
- `oauth-state.entity.ts`
- `provider-account.entity.ts`
- `ports/*.port.ts`

Application:

- `create-browser-session.use-case.ts`
- `authenticate-browser-request.use-case.ts`
- `authorize-request.use-case.ts`
- `logout-session.use-case.ts`
- `start-strava-oauth.use-case.ts`
- `complete-strava-oauth.use-case.ts`
- `list-strava-activity-summaries.use-case.ts`

Infrastructure:

- `json-auth-store.adapter.ts` for local pilots only.
- `memory-auth-store.adapter.ts` for tests.
- `strava-http-gateway.adapter.ts`.
- future database/secret-store adapters behind ports.

Interface:

- cookie/CSRF helpers,
- Fetch/Request guard functions,
- Body War route adapter,
- optional bearer-token guard for service/API consumers.

### 4. Workflow Process View

Browser auth:

1. Server creates principal/session.
2. Server sets httpOnly signed session cookie and readable CSRF cookie.
3. Unsafe requests require same-origin and matching CSRF header/cookie/session binding.
4. Protected route derives auth context from server-side session lookup.
5. Route checks permission/resource scope.
6. Logout revokes session and clears cookies.

Strava:

1. Authenticated user starts OAuth.
2. Server creates one-use OAuth state record.
3. Callback consumes state and exchanges code server-side.
4. Granted scope is validated.
5. Provider account and token records are stored server-side.
6. Activity summaries are imported with redaction and never expose raw provider tokens.

### 5. Decision Flow View

| Decision | Rule |
| --- | --- |
| Is shell enough? | Use shell only for deterministic orchestration/checking. |
| Is behavior/runtime logic involved? | Use TypeScript. |
| Is a request authenticated? | Only after server-owned session/token lookup succeeds. |
| Is a request authorized? | Permission/resource check must allow; deny overrides allow. |
| Is browser method unsafe? | Require origin + CSRF binding. |
| Is Strava state valid? | One-use state must exist, match principal/session intent, and be unexpired. |
| Can Body War trust request body auth? | No. It must consume server-derived auth context. |

### 6. Dependency Interface View

Allowed imports:

- domain imports only domain/shared and TypeScript built-ins,
- application imports domain ports/types,
- infrastructure imports domain/application contracts and external libraries,
- interface imports application APIs and boundary helpers,
- Body War imports public package exports only.

Forbidden:

- domain importing HTTP/cookie/Strava libraries,
- application importing concrete JSON/DB adapters,
- Body War importing internal module files,
- Python auth runtime remaining as the production auth authority.

## Source Contracts

- DomainSpec architecture: `implementation/domainspec/architecture/pattern-library/*.md`
- Poker-team auth reference: `validation/poker-team/backend/src/domain/auth-access-control/`, `use-cases/auth-access-control/`, `infrastructure/http/auth/`
- Savvy browser auth reference: `projects/savvy_legal-studio-ai/frontend/savvy-legal-studio/lib/auth/savvy-auth.ts`
- Current drift: `projects/auth-user-management/src/auth_user_management/`, `projects/body-war/app/server.py`

## Risks

| Risk | Mitigation |
| --- | --- |
| Copying poker-team product permissions | Copy patterns, not product terms. |
| Browser token leakage | Use httpOnly session cookie and server token custody. |
| CSRF bypass | Same-origin + cookie/header/session binding tests. |
| Strava secrets in repo | Stores ignored by git; provider tokens never tracked or returned. |
| TypeScript package exists but Body War still uses Python | Work-pack includes Body War consumer SWU and validation. |

## Invoke Result

- Mode: design
- Spell: invoke
- Phase status: pass
- Design views: all six covered
- Template/profile selection: DomainSpec architecture profile
- Distill validation: pass, selected `SWU-AUTH-001` as first unit
- Implementation layering: emit companion artifact in plan
- Work-pack: n/a at design stage
- Next route: plan
