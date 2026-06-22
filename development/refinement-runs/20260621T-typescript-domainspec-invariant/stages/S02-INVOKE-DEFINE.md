# S02 - Invoke Define

Owner: `invoke`
Mode: `define`
Verdict: `pass`

## Definition

The auth/user-management foundation is a reusable private workspace package for login, server-owned sessions, authorization, and Strava account linking. Its implementation language is TypeScript unless the work is deterministic orchestration or validation that can be expressed clearly as shell.

## Spec Baseline

### Capability

`auth-user-management` owns:

- users/principals,
- server sessions,
- browser cookie + CSRF session transport,
- bearer-token service transport when a service/API consumer needs it,
- permission and resource authorization,
- provider account links,
- Strava OAuth state/callback/token custody/activity summary import,
- audit identity context,
- local pilot storage adapters and production-ready port contracts.

### Invariant

New `domainspec-core` project implementation should follow this order:

1. shell script for deterministic setup, validation, scanning, bootstrap, and simple glue;
2. TypeScript for runtime/application/domain behavior;
3. no Python as default new runtime/application language unless a decision gate grants an explicit scoped exception.

### First Consumer

Body War consumes the auth package only for login/session/Strava/activity authorization. Track geometry, scoring, game mechanics, payments, and competitive loop design are deferred.

## Domain Vocabulary

| Term | Definition |
| --- | --- |
| Principal | Workspace/app actor identity after upstream login or local pilot bootstrap. |
| Session | Server-owned active/revoked/expired/inactive continuity record. |
| Browser Session | Secure cookie transport backed by server-side session lookup and CSRF binding. |
| Auth Context | Server-derived actor/session/permissions/resource/audit stamp passed to application routes. |
| Permission | Canonical action key evaluated deny-by-default. |
| Provider Account | External account link, beginning with Strava athlete identity. |
| Provider Token | Server-held access/refresh token record; never returned to the browser. |
| OAuth State | One-use CSRF/state record for provider callback validation. |
| Runtime Language Policy | Repo-private invariant that shell precedes TypeScript only when shell can do the job safely. |

## Decisions

| Decision | Selected | Rationale |
| --- | --- | --- |
| Runtime language | TypeScript | Matches DomainSpec implementation model and user's correction. |
| Script language | POSIX-ish shell where sufficient | Fits repo invariant for validation/orchestration. |
| Browser transport | httpOnly SameSite cookie + readable CSRF binding | Aligns with Savvy production-readiness lesson and browser ergonomics. |
| API/service transport | bearer token optional, server-backed by `sid`/`jti` | Carries poker-team use-case pattern without forcing browser token storage. |
| Authorization | app-owned permission/resource checks | Provider identity is not enough for app authority. |
| Strava scope | `read,activity:read` by default | Smallest useful scope for activity import. |

## Non-Goals

- No game/track implementation.
- No production IdP vendor selection in this pass.
- No Python auth patching.
- No public `arcanum` mutation.

## Dispatch Technique Trace

| Technique | Applied To | Status |
| --- | --- | --- |
| `sequence` | Context -> define -> review -> design -> plan | pass |
| `owner_boundary_check` | DomainSpec architecture, private parent, auth package, Body War consumer | pass |
| `route_menu` | Reject Python patch and policy-only route | pass |
| `concrete_path_evidence` | Source anchors and drift paths | pass |
| `state_namespace_boundary` | Parent evidence, project code, submodules | pass |

## Invoke Result

- Mode: define
- Spell: invoke
- Canonical ID: invoke
- Scope: library
- Phase status: pass
- Mode contract: `.agents/skills/invoke/define.md`
- Outputs: this define artifact
- Template selection: DomainSpec implementation profile with standalone implementation-layering/work-pack companions
- Distill validation: required downstream because the scope spans reusable package, consumer integration, and repo invariant
- Next route: design
