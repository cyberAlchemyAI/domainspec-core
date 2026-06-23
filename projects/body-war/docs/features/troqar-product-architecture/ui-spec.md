# UI/UX Specification: TROQAR App

Status: `draft-pass`
Visual source: `docs/research/source-notes/troqar-visual-identity.md`

## UX Principle

Every logged-in screen should answer three questions without instructional
copy: where can I run, what can I win or defend, and what changes if I submit
this activity?

## Route Table

| Route | Page | Primary Actor | Auth | Capability |
| --- | --- | --- | --- | --- |
| `/` | Home Command | Runner | optional | CAP-AUTH, CAP-CHALLENGE, CAP-CONTROL |
| `/connect` | Connect Strava | Runner | optional | CAP-AUTH |
| `/map` | Territory Map | Runner | optional | CAP-TRACK, CAP-CONTROL |
| `/routes` | Routes And Tracks | Runner | optional | CAP-TRACK |
| `/routes/:trackId` | Route Detail / Claim | Runner | optional for view, required for submit | CAP-EVIDENCE, CAP-CONTROL |
| `/activities` | Activity Import | Runner | required | CAP-ACTIVITY |
| `/challenges` | Challenges | Runner | optional for list, required for join | CAP-CHALLENGE |
| `/community` | Community / Clans | Runner | optional for discovery, required for membership | CAP-CLAN |
| `/clans/:clanId` | Clan Detail | Runner | optional/member-aware | CAP-CLAN |
| `/rankings` | Rankings And Seasons | Runner | optional | CAP-SEASON |
| `/profile` | Profile And Progress | Runner | required | CAP-SCORE |
| `/notifications` | Notifications | Runner | required | CAP-NOTIFY |
| `/profile/privacy` | Consent And Privacy | Runner | required | CAP-AUTH |
| `/operator` | Pilot Operator Console | Operator | operator | CAP-OPERATOR |
| `/sponsor` | Sponsor Zones | Sponsor/operator | restricted | CAP-SPONSOR, deferred |
| `/store` | Store / RunCoins | Runner | required | CAP-ECONOMY, deferred |

## Navigation Model

Primary mobile bottom navigation:

1. Home
2. Routes
3. Challenges
4. Community
5. Profile

Secondary actions:

- Map is reachable from Home and Routes.
- Notifications is an icon button in the app header.
- Privacy is inside Profile.
- Operator and Sponsor surfaces are role-gated and not in runner nav.

## Page Layouts

### `/` - Home Command

Job: compress the runner's current situation into one scan.

Components:

- `WeeklyDistanceSummary`
- `CurrentTerritoryStrip`
- `ActiveChallengeCard`
- `FeaturedRouteCard`
- `NextRunAction`
- `RecentChangeFeed`

Data:

- Q-HOME-SUMMARY
- Q-AUTH-STATUS
- Q-CONTROL-CURRENT
- Q-CHALLENGE-ACTIVE

### `/connect` - Connect Strava

Job: explain consent and start the provider flow.

Components:

- `ConsentSummary`
- `ProviderScopeList`
- `ConnectStravaButton`
- `PrivacyLink`
- `ConnectionErrorBanner`

### `/map` - Territory Map

Job: show territory control, available routes, and status caveats.

Components:

- `MapViewport`
- `TerritoryFilterBar`
- `GeometryStatusBadge`
- `ControllerLegend`
- `RoutePreviewDrawer`

State rules:

- `geometryStatus=missing|placeholder` shows non-GPS caveat.
- `preview-controlled` uses preview styling distinct from verified control.

### `/routes` - Routes And Tracks

Job: let runner choose where to compete next.

Components:

- `FeaturedRouteCard`
- `RouteGrid`
- `RouteDifficultyFilter`
- `GeometryStatusBadge`
- `ControllerMetricChip`

### `/routes/:trackId` - Route Detail / Claim

Job: convert a route into a run evidence action.

Components:

- `RouteHero`
- `ControllerPanel`
- `ActivityPicker`
- `SubmitEvidenceButton`
- `LeaderboardPreview`
- `GeometryCaveat`
- `RecentSubmissions`

Actions:

- OP-EVIDENCE-SUBMIT

### `/activities` - Activity Import

Job: show real run summaries and why any activity cannot be used.

Components:

- `ProviderStatusCard`
- `ActivityList`
- `RunTypeFilter`
- `EmptyActivitiesState`
- `RefreshActivitiesButton`

### `/challenges` - Challenges

Job: show active objectives and immediate rewards.

Components:

- `ActiveChallengeList`
- `MissionProgressCard`
- `RewardBadge`
- `JoinChallengeButton`
- `ExpiredChallengeArchive`

### `/community` - Community / Clans

Job: make clan membership and local competition visible.

Components:

- `ClanStatusCard`
- `NearbyClansList`
- `CommunityActivityFeed`
- `CreateClanButton`
- `JoinClanButton`

### `/clans/:clanId` - Clan Detail

Job: support coordination and shared identity.

Components:

- `ClanHeader`
- `MemberRoster`
- `ClanContributionPanel`
- `DefenseAlerts`
- `ClanRankingCard`

### `/rankings` - Rankings And Seasons

Job: make league and season status legible.

Components:

- `SeasonHeader`
- `LeagueTabs`
- `RunnerLeaderboard`
- `ClanLeaderboard`
- `HallOfFameLink`

### `/profile` - Profile And Progress

Job: show identity, XP, badges, streaks, and account state.

Components:

- `ProfileHeader`
- `XPProgressBar`
- `LeagueCard`
- `BadgeShelf`
- `StreakCard`
- `RecentEvidenceList`

### `/notifications`

Job: collect action-needed events.

Components:

- `NotificationList`
- `DefenseWindowAlert`
- `ChallengeReminder`
- `RewardNotice`

### `/profile/privacy`

Job: make consent, provider access, and data use inspectable.

Components:

- `ProviderConnectionCard`
- `ScopeList`
- `RevokeAccessButton`
- `DataRetentionSummary`

### `/operator`

Job: let an operator review pilot evidence without touching raw tokens.

Components:

- `ReviewQueue`
- `SubmissionAuditTimeline`
- `VerifyRejectControls`
- `DataHealthPanel`

## Component Inventory

| Component | Type | Purpose |
| --- | --- | --- |
| `AppShell` | Layout | Header, bottom nav, auth-aware route chrome. |
| `GeometryStatusBadge` | State Indicator | Shows missing/draft/source-backed/validated geometry. |
| `ControllerPanel` | Component | Shows current controller and evidence basis. |
| `ActivityPicker` | Form | Lets runner choose eligible activity. |
| `SubmitEvidenceButton` | Action | Submits evidence with CSRF/session. |
| `ActiveChallengeCard` | Component | Highlights current challenge. |
| `RouteHero` | Component | Branded route/territory header. |
| `XPProgressBar` | State Indicator | Shows permanent XP progress. |
| `ConsentSummary` | Component | Shows provider scope and privacy promise. |
| `ReviewQueue` | Operator Component | Lists submissions needing review. |

## State-To-UI Mapping

| Domain Value | UI Representation |
| --- | --- |
| `anonymous` | Orange connect action. |
| `connected` | Green status chip with athlete summary. |
| `preview-accepted` | Orange/green mixed chip labeled `Preview accepted`. |
| `verified` | Solid green chip labeled `Verified`. |
| `geometryStatus=missing` | Neutral caveat row, no route line. |
| `geometryStatus=source-backed` | Route map visible with source note. |
| `contested` | Fire/orange alert with deadline. |
| `expired` | Muted territory state. |

## Accessibility Requirements

| Surface | Requirement |
| --- | --- |
| Bottom navigation | Use semantic nav, visible focus, current page state. |
| Map | Provide list/table fallback for territory data. |
| Activity picker | Label distance, time, pace, and eligibility. |
| Controller state | Text label must not rely on color alone. |
| Operator controls | Review buttons need explicit confirmation and reason capture. |
| Alerts | Use role/status where live updates occur. |

## UX Guardrails

- Do not use "verified" when state is `preview-accepted`.
- Do not hide geometry caveats on map/route pages.
- Do not expose token expiry or provider token internals in runner UI.
- Keep first-run path short: connect, choose activity, choose route, submit.
- Keep deferred pages visible in architecture but disabled or absent in L0 builds.
