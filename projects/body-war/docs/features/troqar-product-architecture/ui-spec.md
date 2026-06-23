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
updatedAt: 2026-06-21
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

1. See Strava/auth connection state.
2. Connect through fake or real Strava flow.
3. See safe runner profile and Strava profile link.
4. Import redacted run summaries.
5. Select a pilot track and submit one activity as preview evidence.
6. See submitted evidence without verified-geometry claims.
7. Logout.

Deferred app-wide pages from `ui-spec.md` stay design-defined but are not L0
implementation blockers.

## Route Table

| Route | Page Title | Layout | Auth Required | Capability | L0 Status |
| --- | --- | --- | --- | --- | --- |
| `/` | Online Runner Profile | Static App Shell | optional | CAP-AUTH, CAP-ACTIVITY, CAP-TRACK, CAP-EVIDENCE | active |
| `/profile` | Online Runner Profile | Static App Shell fallback | optional for shell, session for profile API | CAP-AUTH, CAP-SCORE | active |
| `/api/auth/strava/start` | Strava OAuth Start | redirect | no | CAP-AUTH | active |
| `/api/auth/strava/callback` | Strava OAuth Callback | redirect | state cookie | CAP-AUTH | active |
| `/activities` | Activity Import | future route | yes | CAP-ACTIVITY | deferred |
| `/routes` | Routes And Tracks | future route | optional | CAP-TRACK | deferred |
| `/routes/:trackId` | Route Detail / Claim | future route | optional view, session submit | CAP-EVIDENCE | deferred |
| `/profile/privacy` | Consent And Privacy | future route | yes | CAP-AUTH | deferred |

## Page Layout: `/` And `/profile`

```text
Topbar
  Product eyebrow
  Page title
  Account actions: Profile, Connect Strava, Logout

Main grid
  Connection panel
    Connection copy
    Safe athlete summary/link
  Profile panel
    Runner identity
    Provider connection
    Privacy promise
    Validation caveat
  Activities panel
    Redacted summary receipt
    Activity cards with track select + submit
  Pilot tracks panel
    Track cards and controller metric
  Submitted evidence panel
    Preview submission history
```

## Component Inventory

| Component | Type | Location | Purpose |
| --- | --- | --- | --- |
| `TopbarAccountActions` | Navigation | `static/index.html`, `static/app.js` | Shows profile, connect, and logout actions based on auth state. |
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
| `troqar.shell` | Online Runner Profile Page | `static/index.html` |
| `topbar.account.actions` | TopbarAccountActions | `static/index.html` |
| `auth.connect.cta` | Connect Strava CTA | `static/index.html` |
| `profile.safe-athlete-card` | SafeAthleteCard/ProfileGrid | `static/index.html`, `static/app.js` |
| `profile.strava-link` | Strava public profile link | `static/app.js` |
| `activity.recent-summary` | ActivityList receipt panel | `static/index.html`, `static/app.js` |
| `evidence.submit.cta` | SubmitEvidenceButton | `static/index.html`, `static/app.js` |

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
| `anonymous` | Primary fire-orange `Connect Strava` action is visible. |
| `connected` | Territory-green status copy and safe athlete card are visible. |
| `not_connected` | Activity panel explains connect requirement. |
| `empty` | Activity panel says no recent runs found. |
| `ready` | Activity cards show distance, time, pace, track selector, and submit button. |
| `preview-accepted` | Submission tag may show preview authority; never render as `verified`. |
| `geometryStatus=missing|placeholder` | Activity receipt states route geometry and scoring are not claimed. |

## Error Code Mapping

| API Error Code | HTTP | UI Message |
| --- | --- | --- |
| `auth_required` | 401 | Connect Strava to continue. |
| `csrf_required` | 403 | Refresh the page and retry the action. |
| `not_connected` | 401 | Connect Strava before importing activity summaries. |
| `invalid_activity` | 400 | This activity cannot be submitted for the selected track. |
| `track_geometry_missing` | 409 | Route geometry is not verified for this claim yet. |

## Accessibility Requirements

| Surface | Requirement |
| --- | --- |
| Topbar actions | Semantic `nav` with visible action labels and keyboard focus. |
| Connection panel | Status text must not rely on color. |
| Athlete/profile links | External links use visible text and `rel="noreferrer"`. |
| Activity rows | Track select and submit button remain reachable by keyboard. |
| Mobile layout | No action button, select, or profile text overlaps at 390px width. |

## Security And Privacy Requirements

- UI must not render `access_token`, `refresh_token`, OAuth `code`, or token
  expiry internals.
- Strava profile URL may render only as a public athlete link.
- Public profile link text must be `Open public Strava profile`.
- Activity rows must use redacted summaries; no maps, notes, private payloads,
  or raw provider objects.
- Submission copy must preserve the distinction between preview evidence,
  verified evidence, and missing geometry.

## UI Concept Registry

| Concept | ID | Type |
| --- | --- | --- |
| Online Runner Profile Page | ui.troqar.onlineRunnerProfile | Page |
| Connection Panel | ui.troqar.ConnectionPanel | Component |
| Safe Athlete Card | ui.troqar.SafeAthleteCard | Component |
| Profile Grid | ui.troqar.ProfileGrid | Component |
| Activity List | ui.troqar.ActivityList | Component |
| Submit Evidence Button | ui.troqar.SubmitEvidenceButton | Action |
| Track Grid | ui.troqar.TrackGrid | Component |
| Submission List | ui.troqar.SubmissionList | Component |
