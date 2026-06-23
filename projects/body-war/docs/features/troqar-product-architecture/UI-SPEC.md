---
id: troqar-product-architecture-ui
feature: troqar-product-architecture
title: "TROQAR Frontend UI Specification"
summary: Browser presentation contract for the BodyWar/TROQAR online runner profile and first evidence flow.
status: draft-pass
pillar: frontend
domain: troqar-ui
audience:
  - developers
  - product
priority: p0
lang: en
owners:
  - body-war
updatedAt: 2026-06-22
dependencies:
  - SPEC.md
  - interfaces.md
  - operations.md
  - queries.md
  - states.md
  - VISUAL-DEFINITIONS.md
constitution: ../../UI-ARCHITECTURE.md
source: domainspec-ui-pipeline
---

# UI Specification: TROQAR Frontend

> Governs the frontend presentation of the first BodyWar/TROQAR authenticated
> runner loop. Constrained by [UI-ARCHITECTURE.md](../../UI-ARCHITECTURE.md).

## Scope

L0 covers the online runner profile and first evidence loop:

1. Anonymous runner lands on a login-first TROQAR screen.
2. Strava is the only visible MVP login method.
3. Runner connects through fake or real Strava flow.
4. Connected runner sees safe profile and public Strava profile link.
5. Connected runner imports redacted run summaries.
6. Connected runner selects a pilot track and submits one activity as preview evidence.
7. Connected runner sees submitted evidence without verified-geometry claims.
8. Runner can logout back to the anonymous login screen.

Deferred app-wide pages from `ui-spec.md` stay design-defined but are not L0
implementation blockers.

## Route Table

| Route | Page Title | Layout | Auth Required | Capability | L0 Status |
| --- | --- | --- | --- | --- | --- |
| `/` | Perfil Online do Corredor | Static App Shell | optional | CAP-AUTH, CAP-ACTIVITY, CAP-TRACK, CAP-EVIDENCE | active |
| `/profile` | Perfil Online do Corredor | Static App Shell fallback | optional for shell, session for profile API | CAP-AUTH, CAP-SCORE | active |
| `/api/auth/strava/start` | Strava OAuth Start | redirect | no | CAP-AUTH | active |
| `/api/auth/strava/callback` | Strava OAuth Callback | redirect | state cookie | CAP-AUTH | active |
| `/activities` | Activity Import | future route | yes | CAP-ACTIVITY | deferred |
| `/routes` | Routes And Tracks | future route | optional | CAP-TRACK | deferred |
| `/routes/:trackId` | Route Detail / Claim | future route | optional view, session submit | CAP-EVIDENCE | deferred |
| `/profile/privacy` | Consent And Privacy | future route | yes | CAP-AUTH | deferred |

## Page Layout: `/` And `/profile`

```text
App shell
  Topbar
    TROQAR mark / wordmark
    Account actions: Perfil, Sair (connected only)

Anonymous login-first state
  Login hero
    TROQAR value line
    Strava-only connect CTA
    Privacy / preview evidence trust copy
    Callback success and provider error banners
  Preview card
    Mobile app-style activity/territory preview

Connected runner state
  Connection panel
    Connection copy
    Safe athlete summary/link
  Profile panel
    Runner identity
    Provider connection
    Privacy promise
    Validation caveat
  Activities panel
    Loading / empty / error states
    Redacted summary receipt
    Activity cards with track select + submit
  Pilot tracks panel
    Track cards, geometry status, and controller metric
  Submitted evidence panel
    Preview submission history and preview status chips
```

## Component Inventory

| Component | Type | Location | Purpose |
| --- | --- | --- | --- |
| `TopbarAccountActions` | Navigation | `static/index.html`, `static/app.js` | Shows profile, connect, and logout actions based on auth state. |
| `LoginHero` | Page section | `static/index.html`, `static/app.js` | Anonymous first screen with TROQAR identity and Strava-only login. |
| `CallbackStatus` | Status banner | `static/index.html`, `static/app.js` | Shows safe success or retry copy for callback query states. |
| `ConnectionPanel` | State panel | `static/index.html`, `static/app.js` | Renders provider configured/authenticated/connected states. |
| `SafeAthleteCard` | Component | `static/app.js` | Renders name/image/Strava profile link without tokens. |
| `ProfileGrid` | Component group | `static/index.html`, `static/app.js` | Shows runner, provider, privacy, and validation cards. |
| `ActivityList` | List/form hybrid | `static/index.html`, `static/app.js` | Renders redacted run-like activities with track selector. |
| `SubmitEvidenceButton` | Action | `static/app.js` | Posts selected activity/track with CSRF header. |
| `TrackGrid` | Card grid | `static/app.js` | Lists pilot tracks and controller metric. |
| `SubmissionList` | List | `static/app.js` | Shows submitted preview evidence history. |

## Prototype Gate Evidence

The L0 UI consumed the accepted Studio prototype gate handoff in
[`prototype-handoff/STUDIO-PROTOTYPE-HANDOFF.md`](prototype-handoff/STUDIO-PROTOTYPE-HANDOFF.md).
The accepted session is `ups-session-0001`, revision `rev-0001`, with export
profile `troqar-product-architecture`.

| `data-od-id` | Component | Production Location |
| --- | --- | --- |
| `troqar.shell` | Perfil Online do Corredor Page | `static/index.html` |
| `topbar.account.actions` | TopbarAccountActions | `static/index.html` |
| `auth.login-first` | Anonymous login-first page | `static/index.html` |
| `login.hero` | Anonymous hero copy | `static/index.html` |
| `login.trust-copy` | Privacy and preview evidence trust copy | `static/index.html` |
| `login.preview-card` | TROQAR app preview card | `static/index.html` |
| `auth.connect.cta` | Connect Strava CTA | `static/index.html` |
| `auth.callback-status` | Safe callback success copy | `static/index.html`, `static/app.js` |
| `auth.error.banner` | Safe provider error copy | `static/index.html`, `static/app.js` |
| `auth.reconnect.cta` | Retry Strava connection CTA | `static/index.html` |
| `profile.safe-athlete-card` | SafeAthleteCard/ProfileGrid | `static/index.html`, `static/app.js` |
| `profile.strava-link` | Strava public profile link | `static/app.js` |
| `profile.privacy-card` | Safe custody copy | `static/app.js` |
| `activity.recent-summary` | ActivityList receipt panel | `static/index.html`, `static/app.js` |
| `activity.loading` | Activity loading state | `static/app.js` |
| `activity.empty` | Empty activity state | `static/app.js` |
| `activity.error` | Activity error state | `static/app.js` |
| `track.geometry-status` | Track geometry/preview status | `static/app.js` |
| `evidence.status-chip` | Preview submission status chip | `static/app.js` |
| `evidence.submission-list` | Submitted evidence list | `static/index.html`, `static/app.js` |
| `evidence.submit.cta` | SubmitEvidenceButton | `static/index.html`, `static/app.js` |
| `evidence.submit.error` | Submit error state | `static/app.js` |

## Data Flow

| API Call | UI Function | Trigger | UI Obligation |
| --- | --- | --- | --- |
| `GET /api/status` | `loadStatus()` | boot, after auth changes | Toggle connect/logout/profile actions and render safe athlete summary. |
| `GET /api/profile` | `loadProfile()` | boot, after auth changes | Render runner profile or connect prompt; no token internals. |
| `GET /api/tracks` | `loadTracks()` | boot | Populate track cards and activity track selectors. |
| `GET /api/activities?per_page=12` | `loadActivities()` | boot, refresh button | Render run-like summaries only; show geometry/scoring caveat. |
| `GET /api/submissions` | `loadSubmissions()` | boot, after submit | Show preview evidence history. |
| `POST /api/submissions` | `submitActivity()` | activity submit click | Send activity metrics and selected track with CSRF. |
| `POST /api/auth/logout` | logout handler | logout click | Revoke session and return to anonymous UI. |

## Form Contracts

### Activity Evidence Submit

| Field | Source | Validation | Error UI |
| --- | --- | --- | --- |
| `track_id` | selected track option | required, existing track | inline alert or retry copy |
| `activity_id` | activity summary | required | activity row stays visible |
| `activity_name` | activity summary | optional display value | fallback to activity id |
| `moving_time` | activity summary | numeric if present | pace/time may show unavailable |
| `distance` | activity summary | numeric if present | distance may show unavailable |
| `average_speed` | activity summary | numeric if present | not displayed as proof |

Unsafe POST requests must include `X-CSRF-Token` from `bw_csrf`.

## State-To-UI Mapping

| Domain/UI State | Representation |
| --- | --- |
| `unconfigured` | Connection copy names missing Strava configuration and hides connect CTA. |
| `anonymous` | Login-first screen is visible; one fire-orange `Entrar com Strava` action is visible. |
| `callback=connected` | Safe success banner says Strava is connected and safe profile/summaries are ready. |
| `auth_error` | Safe retry banner is visible with no provider internals. |
| `connected` | Territory-green status copy and safe athlete card are visible. |
| `not_connected` | Activity panel explains connect requirement. |
| `loading` | Activity panel shows loading copy with `activity.loading`. |
| `empty` | Activity panel says no recent runs found. |
| `error` | Activity or submit state shows safe retry copy without raw provider payloads. |
| `ready` | Activity cards show distance, time, pace, track selector, and submit button. |
| `preview-accepted` | Submission tag may show preview authority; never render as `verified`. |
| `geometryStatus=missing|placeholder` | Activity receipt states route geometry and scoring are not claimed. |

## Error Code Mapping

| API Error Code | HTTP | UI Message |
| --- | --- | --- |
| `auth_required` | 401 | Conecte o Strava para continuar. |
| `csrf_required` | 403 | Atualize a pagina e tente novamente. |
| `not_connected` | 401 | Conecte o Strava antes de importar resumos seguros dos treinos. |
| `invalid_activity` | 400 | Este treino nao pode ser enviado para a pista selecionada. |
| `track_geometry_missing` | 409 | Geometria da rota ainda nao foi confirmada para esta evidencia. |

## Accessibility Requirements

| Surface | Requirement |
| --- | --- |
| Topbar actions | Semantic `nav` with visible action labels and keyboard focus. |
| Connection panel | Status text must not rely on color. |
| Athlete/profile links | External links use visible text and `rel="noreferrer"`. |
| Activity rows | Track select and submit button remain reachable by keyboard. |
| Mobile layout | No action button, select, or profile text overlaps at 390px or 320px width. |

## Security And Privacy Requirements

- UI must not render `access_token`, `refresh_token`, OAuth `code`, or token
  expiry internals.
- Anonymous MVP login must show Strava only; no Google, email/password, guest,
  Apple, or other provider CTAs are visible.
- Strava profile URL may render only as a public athlete link.
- Public profile link text must be `Open public Strava profile`.
- Activity rows must use redacted summaries; no maps, notes, private payloads,
  or raw provider objects.
- Submission copy must preserve the distinction between preview evidence,
  verified evidence, and missing geometry.

## UI Concept Registry

| Concept | ID | Type |
| --- | --- | --- |
| Perfil Online do Corredor Page | ui.troqar.onlineRunnerProfile | Page |
| Connection Panel | ui.troqar.ConnectionPanel | Component |
| Safe Athlete Card | ui.troqar.SafeAthleteCard | Component |
| Profile Grid | ui.troqar.ProfileGrid | Component |
| Activity List | ui.troqar.ActivityList | Component |
| Submit Evidence Button | ui.troqar.SubmitEvidenceButton | Action |
| Track Grid | ui.troqar.TrackGrid | Component |
| Submission List | ui.troqar.SubmissionList | Component |
