# Queries

Status: `draft-pass`

## Read Model Principles

- Queries return UI-safe data only.
- Provider tokens, refresh tokens, raw private activity payloads, and secrets are never query fields.
- Each read model includes enough status to render empty, loading, error, and degraded states.

## Query Catalog

| Query ID | Read Model | Fields | Page Consumers |
| --- | --- | --- | --- |
| Q-AUTH-STATUS | `AuthStatus` | configured, authenticated, connected, athlete summary, scope | `/`, `/connect`, `/profile/privacy` |
| Q-HOME-SUMMARY | `HomeSummary` | weekly distance, active challenge, featured route, controller summary, next action | `/` |
| Q-ACT-LIST | `ActivityList` | activity summaries, provider status, empty reason | `/activities`, `/routes/:trackId` |
| Q-TRACK-LIST | `TrackList` | track cards, geometry status, controller metric | `/routes`, `/map` |
| Q-TRACK-DETAIL | `TrackDetail` | track, geometry, controller, leaderboard, submit eligibility | `/routes/:trackId` |
| Q-CONTROL-CURRENT | `ControllerState` | controller, basis, metric, last accepted evidence | `/`, `/map`, `/routes/:trackId` |
| Q-EVIDENCE-LIST | `SubmissionList` | submissions, status, audit state | `/operator`, `/profile/activity` |
| Q-PROFILE-SUMMARY | `ProfileSummary` | XP, league, badges, streak, clan, privacy status | `/profile` |
| Q-CHALLENGE-ACTIVE | `ChallengeList` | active missions, progress, rewards, enrollment | `/`, `/challenges` |
| Q-CLAN-SUMMARY | `ClanSummary` | current clan, members, contribution, alerts | `/community`, `/clans/:clanId` |
| Q-RANKINGS | `RankingBoard` | league, season, runner rows, clan rows | `/rankings` |
| Q-NOTIFICATIONS | `NotificationInbox` | notifications, unread count, action links | `/notifications` |
| Q-OPERATOR-QUEUE | `OperatorQueue` | pending submissions, review decisions, health warnings | `/operator` |

## Page Aggregates

### HomeSummary

Composes:

- `AuthStatus`
- weekly distance from activity/progression
- active challenge
- featured route
- current controller summary

Primary action:

- unauthenticated: connect Strava
- authenticated without activities: refresh activities
- authenticated with activity: submit to featured route

### TrackDetail

Composes:

- territory metadata
- geometry status
- controller state
- route leaderboard
- eligible activities
- evidence submission state

Primary action:

- submit run evidence or view why submission is blocked.

### ProfileSummary

Composes:

- identity and privacy state
- XP/league/streak/badges
- recent submissions
- provider connection status
