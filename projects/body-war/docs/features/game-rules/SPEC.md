# Game Rules Spec

## Summary

Game Rules defines the first TROQAR DomainSpec feature slice: how real runs become validated game actions, how zones are conquered or defended, how XP and seasons progress, and how clan mechanics affect territory play.

This spec is a discovery-level draft. It captures seed rules from the GDD and JSX sources and explicitly marks conflicts that need a product decision before implementation.

## Source Evidence

| Source | Used For |
| ------ | -------- |
| `docs/research/source-notes/runwar-gdd.md` | Hex model, invasion loop, defense windows, anti-cheat, monetization, roadmap. |
| `docs/research/source-notes/troqar-gamificacao-jsx.md` | Zone Score formula, XP sources, conquest types, recovery rules, clans, seasons. |
| `docs/research/source-notes/troqar-visual-identity.md` | Brand framing and product language. |

## Goals

- Define the minimum game rule language for TROQAR's territory-running loop.
- Separate selected rules from unresolved balancing decisions.
- Give later specs enough structure to model entities, state machines, policies, calculations, and validation gates.

## Non-Goals

- No mobile app implementation.
- No exact geospatial indexing implementation.
- No payment, sponsor dashboard, or wearable integration.
- No final economy balancing.

## Actors

| Actor | Responsibility |
| ----- | -------------- |
| Runner | Records runs, conquers zones, defends territory, earns XP, joins clans. |
| Zone Owner | Runner currently controlling a zone. |
| Invader | Runner attempting to take a zone. |
| Clan Member | Runner who can contribute to coordinated attack or mutual defense. |
| Pilot Operator | Manual operator for early WhatsApp/Strava validation. |
| Anti-Cheat Reviewer | Human or automated review function for suspicious runs. |

## Core Objects

| Object | Type | Notes |
| ------ | ---- | ----- |
| Run | Event | GPS activity submitted for validation. |
| Hex Zone | Entity | Map unit, roughly 400m point-to-point in the GDD. |
| Zone Type | Value Object | Common, strategic, event, legendary, sponsored, neutral. |
| Zone Ownership | State | Neutral, owned, contested, transferred, expired. |
| Zone Score | Calculation | Composite strength score from JSX. |
| Reference Time | Calculation | Fastest/owner-held time from GDD. |
| Invasion | Workflow | Attempt to take an owned zone. |
| Defense Window | Policy | Timed response period, usually 48h for common zones. |
| Clan | Aggregate | Social group with coordinated mechanics. |
| XP | Metric | Permanent profile progression. |
| RunCoins | Currency | Economy and item currency. |
| League | State Machine | Monthly tier based on active zones. |
| Season | Cycle | Quarterly competitive reset for rankings, not profile XP. |

## Run Validity

| Rule | Status | Description |
| ---- | ------ | ----------- |
| Coverage threshold | draft | A run must cover at least 60% of a hex perimeter to affect that zone. |
| Validation delay | draft | GDD allows a 2-5 minute validation delay before conquest is final. |
| Anti-cheat gate | draft | A run must pass automated validation before it changes ownership, XP, or ranking. |
| Pilot fallback | draft | In pre-MVP, Strava screenshots and operator review may stand in for app validation. |

## Zone Types

| Type | Status | Behavior |
| ---- | ------ | -------- |
| Neutral Zone | draft | First valid runner can conquer it. If multiple runners complete in the same validation cycle, higher selected metric wins. |
| Common Zone | draft | Base territory. Can be invaded and defended through common rules. |
| Strategic Zone | draft | Harder to invade; grants adjacent-zone XP benefits. |
| Event Zone | draft | Weekly activated zone with exclusive rewards. |
| Legendary Zone | draft | One per neighborhood; weekend-focused competition; grants visible titles. |
| Sponsored Zone | draft | Brand-linked zone with vouchers or real-world rewards. |

## Zone Score

The JSX source defines a composite Zone Score:

| Factor | Weight | Draft Rule |
| ------ | ------ | ---------- |
| Pace Score | 40% | Faster average pace in valid zone runs increases score. |
| Distance Score | 35% | More kilometers inside the hex during the current cycle increase score, capped. |
| Frequency Score | 25% | Unique visit days in a 14-day cycle increase score, capped. |

Draft properties:

- Score cycle lasts 14 days.
- Same-day duplicate runs count as one visit for frequency.
- Score is intended to reward speed, consistency, and presence.
- The displayed max from JSX is 550 points.

Unresolved:

- Whether Zone Score replaces the GDD reference-time model or augments it.
- Whether conquest winner is highest score, fastest reference time, or a hybrid.

## Conquest And Defense

| Rule | Status | Description |
| ---- | ------ | ----------- |
| Neutral conquest | draft | A valid run in a neutral zone grants ownership after validation. |
| Common invasion | draft | Invader runs inside an owned zone and must exceed the owner's selected defense metric. |
| Common defense window | draft | Owner has 48h to defend after a successful invasion trigger. |
| Strategic invasion | draft | Strategic zones require a harder margin and may use a 72h defense window. |
| Legendary competition | draft | Legendary zones are primarily contested on weekends; best selected metric wins the weekly ownership period. |
| Cooldown | draft | Common zones have a 6h same-zone invasion cooldown after attack or ownership exchange. |
| Caducity | draft | Zones not defended/revisited for 14 days return to neutral. |

## Recovery And Reconquest

| Scenario | Status | Draft Rule |
| -------- | ------ | ---------- |
| Common reconquest | draft | Owner or clan can defend within 48h; successful response prevents transfer or keeps ownership. |
| Strategic reconquest | draft | Owner and clan can respond within 72h; up to three clan members may contribute depending on selected rule. |
| Vengeance bonus | draft | Fast or strong reconquest can grant temporary XP bonus/status. |
| Legendary zone | draft | No exclusive recovery window; weekend competition determines owner. |

## XP And Rewards

| Source | Status | Draft Reward Logic |
| ------ | ------ | ------------------ |
| Neutral conquest | draft | Grants base conquest XP. |
| Invasion success | draft | Grants higher XP than neutral conquest. |
| Reconquest | draft | Grants high XP and possible Vinganca status. |
| Defense | draft | Grants defense XP. |
| Distance | draft | Grants per-kilometer XP for valid runs. |
| Personal record | draft | Grants smaller performance XP. |
| Mission/Battle Pass | draft | Grants variable XP and items. |
| Referral | draft | Grants XP or RC after active-user threshold. |
| Sponsored zone | draft | Grants XP plus potential real voucher. |

Selected principle:

- Profile XP is permanent and never resets.

Unresolved:

- Exact XP values differ between sources and should be balanced after pilot evidence.

## Clans

| Rule | Status | Description |
| ---- | ------ | ----------- |
| Membership | draft | GDD standard is up to 5 members, expandable through premium or RC. |
| Roles | draft | Leader, captain, and soldier roles appear in GDD. |
| XP contribution | draft | JSX says 30% of individual XP contributes to clan score without reducing individual XP. |
| Coffer | draft | GDD says 10% of RunCoins spent by members goes to clan coffer. |
| Mutual defense | draft | Clan members can defend an ally's zone during the defense window. |
| Coordinated attack | draft | Clan leader can declare a target; multiple members participate for bonuses. |
| Clan war | draft | Monthly or 72h conflict where zones taken from rival clans score points. |

## Leagues And Seasons

| Mechanic | Status | Description |
| -------- | ------ | ----------- |
| League tiers | draft | Recruta, Guerreiro, Comandante, General. |
| League basis | draft | Active zones, not raw speed, determine monthly league placement. |
| Active zone | draft | Owned and defended/revisited within the active window. |
| Season duration | draft | Three months in GDD/JSX framing. |
| Seasonal reset | draft | Seasonal ranking resets; profile XP, badges, titles, and clan coffer persist. |
| Rewards | draft | Top seasonal performers receive items, RC, badges, and Hall of Fame recognition. |

## Anti-Cheat Validation Gates

| Gate | Status | Description |
| ---- | ------ | ----------- |
| Fake GPS detection | draft | Reject or flag mock-location and suspicious GPS app signals. |
| Sensor fusion | draft | Compare GPS with accelerometer, gyroscope, and barometer. |
| Vehicle detection | draft | Flag sustained speeds, smooth acceleration, road-only route behavior, and unnatural pace consistency. |
| Presence proof | draft | Optional presence challenge or social proof for suspicious cases. |
| Social reporting | draft | Reports can trigger review; false reports should have penalties. |
| Backend validation | draft | All runs pass automatic checks before game state mutation. |

## Open Decisions

| Decision | Options | Required Before |
| -------- | ------- | --------------- |
| Conquest authority metric | Composite Zone Score; reference time; hybrid | Implementing conquest logic. |
| Pilot validation method | Manual Strava/WhatsApp; no-code app; technical MVP | Running first user experiment. |
| Initial economy scope | No economy; XP only; XP plus RC; premium hooks | Monetization experiments. |
| Anti-cheat strictness | Manual review; basic automated checks; full sensor fusion | App-backed MVP. |

## First Candidate Note

The first candidate is not city-wide hex zones. It is `Park Track Control`: selected parks with two or three delimited tracks, manual run evidence, a current controller per track, challenge events, and a 48h defense window.

For this candidate, `Park Track` is the pilot form of a broader `Territory Unit`. Hex zones remain a later territory-unit geometry if the park-track loop proves repeat behavior and defense motivation.

## Acceptance Criteria

- A later planner can derive feature stories for conquest, defense, XP, clans, seasons, and validation.
- All unresolved rule conflicts are named explicitly.
- No implementation depends on hidden source material outside the curated source notes.

