# Operations

Status: `draft-pass`

## OP-AUTH-START-STRAVA

Starts Strava OAuth for a runner.

Inputs:

- requested scope
- redirect URI
- anonymous or existing session context

Outputs:

- authorization URL
- signed/recorded OAuth state

Failure modes:

- provider not configured
- invalid redirect
- state creation failed

## OP-AUTH-CALLBACK

Completes OAuth callback and creates or links a runner session.

Rules:

1. Verify OAuth state is present, current, and unused.
2. Exchange code server-side.
3. Validate granted scope.
4. Store provider token through backend custody only.
5. Create or update Runner and ProviderAccount.
6. Create browser session and CSRF binding.

## OP-ACT-REFRESH

Imports recent redacted activity summaries.

Rules:

- Refresh provider token when expired and refresh token exists.
- Return only summary fields needed by UI and evidence submission.
- Map provider empty response to a non-error empty state.

## OP-TRACK-UPSERT

Publishes territory metadata and geometry status.

Rules:

- `geometryStatus=missing|placeholder` cannot produce GPS-validated language.
- Track/source changes append audit notes.

## OP-EVIDENCE-SUBMIT

Submits one run activity as evidence for one territory unit.

Inputs:

- authenticated runner
- activity id and redacted metrics
- territory id

Rules:

1. Runner must be authenticated.
2. Activity must belong to the runner's provider account.
3. Territory must exist and be preview-visible.
4. Persist `submitted`.
5. In preview mode, route to `OP-EVIDENCE-AUTO-ACCEPT`.

## OP-EVIDENCE-AUTO-ACCEPT

Marks evidence as accepted for preview-controller display.

Rules:

- Result status is `preview-accepted`.
- Never writes `verified`.
- Emits `EvidencePreviewAccepted`.

## OP-OPERATOR-REVIEW

Operator verifies or rejects submitted evidence.

Rules:

- Only operator role can write `verified` or `rejected`.
- Rejection requires reason code.
- Verification requires evidence basis and reviewer id.

## OP-CONTROL-COMPUTE

Computes current controller read model for a territory unit.

Rules:

- L0 preview controller uses fastest preview time unless verified data exists and is selected.
- Later full game may select `zone_score`; that must be a decision, not silent replacement.
- Read model records basis and source submission id.

## OP-CONTROL-OPEN-INVASION

Opens contested state for an owned territory unit.

Rules:

- Requires valid submitted evidence in a mode that supports competition.
- Common zones default to 48h defense window.
- Strategic zones may use 72h window.

## OP-CONTROL-DEFEND

Owner or eligible clan member responds during defense window.

Rules:

- Actor eligibility depends on ownership/clan policy.
- Late defense fails deterministically.
- Successful defense appends ownership event.

## OP-SCORE-CALCULATE

Calculates Zone Score.

Rules:

- Pace 40%, distance 35%, frequency 25%.
- Same-day duplicate visits collapse for frequency.
- 14-day scoring window.
- Display cap 550.

## OP-XP-AWARD

Awards profile XP from a domain event.

Rules:

- XP grant cites source event.
- Profile XP does not reset.
- Seasonal ranking contribution may reset by season.

## OP-CHALLENGE-JOIN

Enrolls runner in an active challenge or mission.

Rules:

- Runner must meet eligibility.
- Challenge progress begins after enrollment unless challenge says retroactive.

## OP-CHALLENGE-COMPLETE

Completes challenge and grants rewards.

Rules:

- Completion evidence must map to challenge criteria.
- Rewards emit XP/reward events.

## OP-CLAN-CREATE

Creates a clan.

Rules:

- Creator becomes leader.
- Name must be unique in active clans.
- Payment/RunCoin gates are deferred.

## OP-CLAN-JOIN

Adds runner to clan.

Rules:

- One active clan membership at a time.
- Clan capacity policy applies.

## OP-SEASON-SNAPSHOT

Closes a ranking cycle.

Rules:

- Snapshot rankings are immutable.
- Profile XP and permanent badges persist.

## OP-NOTIFY-DISPATCH

Dispatches notification.

Rules:

- Push payload avoids private activity details.
- Defense and challenge notifications cite domain event id.
