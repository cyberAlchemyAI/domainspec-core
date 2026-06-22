# Interfaces

Status: `draft-pass`

## External Provider Interfaces

### Strava Provider Boundary

Owned implementation: Body War adapter modules consume
`@domainspec/auth-user-management` core auth use cases.

Responsibilities:

- OAuth start and callback.
- Provider account and token custody.
- Token refresh.
- Redacted activity summaries.

Forbidden:

- returning access tokens to the browser,
- committing provider tokens,
- storing raw private activity payloads in project docs.

## HTTP Interface Table

| Route | Method | Capability | Auth | Returns / Mutates |
| --- | --- | --- | --- | --- |
| `/api/status` | GET | CAP-AUTH | optional | `AuthStatus` |
| `/api/auth/strava/start` | GET | CAP-AUTH | optional | redirect |
| `/api/auth/strava/callback` | GET | CAP-AUTH | state cookie | session and redirect |
| `/api/auth/logout` | POST | CAP-AUTH | session + CSRF | revoked session |
| `/api/activities` | GET | CAP-ACTIVITY | session | `ActivityList` |
| `/api/tracks` | GET | CAP-TRACK | optional | `TrackList` |
| `/api/tracks/:trackId` | GET | CAP-TRACK | optional | `TrackDetail` |
| `/api/submissions` | POST | CAP-EVIDENCE | session + CSRF | `EvidenceSubmission` |
| `/api/submissions` | GET | CAP-EVIDENCE | operator or owner | `SubmissionList` |
| `/api/controller/:territoryId` | GET | CAP-CONTROL | optional | `ControllerState` |
| `/api/profile/me` | GET | CAP-SCORE | session | `ProfileSummary` |
| `/api/challenges` | GET | CAP-CHALLENGE | optional | `ChallengeList` |
| `/api/challenges/:id/join` | POST | CAP-CHALLENGE | session + CSRF | challenge entry |
| `/api/clans` | GET | CAP-CLAN | optional | clan discovery |
| `/api/clans` | POST | CAP-CLAN | session + CSRF | clan |
| `/api/rankings` | GET | CAP-SEASON | optional | `RankingBoard` |
| `/api/notifications` | GET | CAP-NOTIFY | session | `NotificationInbox` |
| `/api/operator/review-queue` | GET | CAP-OPERATOR | operator | `OperatorQueue` |
| `/api/operator/submissions/:id/review` | POST | CAP-OPERATOR | operator + CSRF | review decision |

## Internal Module Interfaces

| Interface | Layer | Exposes | Consumed By |
| --- | --- | --- | --- |
| `AuthPort` | application | auth context, principal id, permissions | all protected operations |
| `ActivityProviderGateway` | infrastructure | list activity summaries | activity import use cases |
| `TerritoryRepository` | infrastructure | tracks, geometry, territory metadata | track queries, control operations |
| `EvidenceRepository` | infrastructure | submissions and audit events | evidence/control/operator modules |
| `ControllerProjection` | application | current controller read model | UI/API queries |
| `ProgressionLedger` | application/infrastructure | XP and season snapshots | profile/ranking modules |
| `NotificationGateway` | infrastructure | dispatch messages | notification use cases |

## Error Code Contract

| Error Code | HTTP | Meaning | UI Mapping |
| --- | --- | --- | --- |
| `auth_required` | 401 | Session required. | Connect Strava / log in. |
| `csrf_required` | 403 | Unsafe method missing CSRF. | Refresh page and retry. |
| `not_connected` | 401 | Provider account not connected. | Connect Strava. |
| `no_run_activities` | 200 | Empty provider result. | Empty state, not crash. |
| `track_geometry_missing` | 409 | Geometry claim unavailable. | Show draft/missing geometry copy. |
| `invalid_activity` | 400 | Activity cannot support territory claim. | Show ineligible activity explanation. |
| `preview_only` | 409 | Attempted verified-only operation in preview mode. | Explain preview limitation. |
| `operator_required` | 403 | Operator role required. | Hide/restrict operator UI. |
