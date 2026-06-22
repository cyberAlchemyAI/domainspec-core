# Domain Model

Status: `draft-pass`
Scope: app-wide TROQAR domain concepts

## Bounded Contexts

| Context | Responsibility | In Scope | Out Of Scope |
| --- | --- | --- | --- |
| Identity And Consent | Runner identity, provider account, session, privacy consent. | Runner, provider account, consent, privacy settings. | Shared package owns generic auth primitives; Body War owns Strava exchange/profile semantics. |
| Activity Evidence | Redacted imported activities and evidence submissions. | Activity summary, submission, preview acceptance, audit. | GPS sensor validation and anti-cheat. |
| Territory Catalog | Tracks now, hex zones later, geometry status. | TerritoryUnit, TrackGeometry, map metadata. | Final city-wide geospatial indexing. |
| Control And Competition | Controller state, invasion/defense windows, transfer policy. | ControllerState, DefenseWindow, ContestedClaim. | Economy and sponsor effects. |
| Progression | XP, badges, league, season, streaks. | ZoneScore, XPLedger, Badge, League, Season. | Payment and paid boosts until economy opens. |
| Community | Clan membership, coordinated actions, clan contribution. | Clan, Membership, ClanContribution. | Public social feed moderation. |
| Pilot Operations | Operator review, health, and evidence governance. | ReviewQueue, AuditDecision, DataHealth. | Full internal admin platform. |

## Entities And Aggregates

### Runner

Public player identity. The runner owns display profile and progression, but
does not expose provider tokens.

Fields:

- `runnerId`
- `displayName`
- `profileImageUrl`
- `providerLinks[]`
- `xpTotal`
- `league`
- `activeClanId?`
- `privacySettings`

Invariants:

- A runner can revoke provider access without deleting profile history.
- Public profile never includes access tokens, refresh tokens, or raw private activity payloads.

### ProviderAccount

Server-side provider link for Strava or future activity providers.

Fields:

- `provider`
- `providerUserId`
- `runnerId`
- `scope`
- `status`
- `linkedAt`
- `tokenReference`

Invariants:

- Token custody is backend-only.
- Provider scope must be visible to the runner in privacy/settings.

### RunActivity

Redacted activity summary that can support evidence submission.

Fields:

- `activityId`
- `provider`
- `runnerId`
- `name`
- `sportType`
- `distanceMeters`
- `movingTimeSeconds`
- `averageSpeed`
- `startedAt`
- `summaryOnly`

Invariants:

- Activity summaries omit tokens, maps, notes, private raw payloads, and unneeded provider metadata.
- Only run-like activity types can be submitted for territory effects.

### TerritoryUnit

Generic play territory. L0 uses a park track; later versions can use hex zones.

Fields:

- `territoryId`
- `kind`: `park-track | hex-zone | event-zone | sponsored-zone`
- `name`
- `status`
- `geometryStatus`
- `controllerMetric`
- `sourceRefs[]`

Invariants:

- `geometryStatus=placeholder` cannot support GPS-validation claims.
- `park-track` is a valid L0 replacement for city-wide hex territory.

### TrackGeometry

Source-backed geometry definition for a track or zone.

Fields:

- `geometryId`
- `territoryId`
- `format`: `geojson | gpx | kml | manual-trace | none`
- `sourceAuthority`
- `status`: `missing | draft | source-backed | validated`
- `caveats[]`

Invariants:

- UI must label draft/missing geometry explicitly.
- `validated` requires a source and validation evidence.

### EvidenceSubmission

Aggregate for one runner's submitted activity against one territory unit.

Fields:

- `submissionId`
- `runnerId`
- `activityId`
- `territoryId`
- `status`
- `authority`
- `submittedAt`
- `redactedMetrics`
- `auditTrail[]`

Invariants:

- `preview-accepted` is not `verified`.
- Submission status changes must append audit events.
- Rejection must include a stable reason code.

### ControllerState

Read model for who currently controls a track/zone.

Fields:

- `territoryId`
- `controllerRunnerId?`
- `controllerDisplayName?`
- `metric`
- `metricValue`
- `basis`: `preview | verified | manual`
- `lastUpdatedAt`
- `sourceSubmissionId?`

Invariants:

- Must cite the metric and evidence basis.
- Preview controller cannot be rendered as verified ownership.

### ZoneScore

Composite score from the JSX source while the composite model remains selected.

Formula:

- Pace Score: 40%
- Distance Score: 35%
- Frequency Score: 25%
- Display cap: 550 points

Invariants:

- Same-day duplicate runs count once for frequency.
- Score window is 14 days unless later balancing changes it.

### XPLedger

Append-only progression ledger.

Invariants:

- Profile XP persists across season resets.
- XP grants must cite source operation and source evidence.

### Clan

Social aggregate for coordinated attack/defense and shared progression.

Invariants:

- A runner has one active clan membership unless a later policy changes it.
- Clan contribution does not reduce individual XP.

### Season

Competitive cycle.

Invariants:

- Seasonal rankings reset.
- Profile XP, badges, titles, and clan coffer do not reset.

## Value Objects

| Value Object | Values / Shape | Notes |
| --- | --- | --- |
| `SubmissionStatus` | `draft`, `submitted`, `preview-accepted`, `verified`, `rejected` | Preview and verified are distinct. |
| `GeometryStatus` | `missing`, `placeholder`, `draft`, `source-backed`, `validated` | Controls map/claim wording. |
| `ControllerMetric` | `fastest_verified_time`, `fastest_preview_time`, `zone_score` | L0 uses preview/verified distinction. |
| `ActivitySportType` | `Run`, `TrailRun`, `VirtualRun`, future provider types | Non-run types excluded from territory effects. |
| `LeagueTier` | `Recruta`, `Guerreiro`, `Comandante`, `General` | Seeded from game-rules spec. |
| `ConsentStatus` | `granted`, `revoked`, `expired` | Drives auth and privacy UI. |

## Domain Invariants

1. Real provider tokens are never domain read-model data.
2. Preview evidence can update preview UI but cannot claim final GPS verification.
3. Geometry status controls every route/map claim.
4. Profile XP persistence is independent from seasonal ranking resets.
5. Operator review and automatic preview acceptance are separate authority paths.
6. TerritoryUnit keeps park-track and hex-zone under one abstraction without forcing city-wide hex work into L0.
