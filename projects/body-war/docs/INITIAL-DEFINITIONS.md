# Initial Definitions

## Glossary Seed

| Term | Working Definition | Category | Status | Evidence Type |
| ---- | ------------------ | -------- | ------ | ------------- |
| TROQAR | User-facing product brand for the running territory game. | brand | selected | stated |
| Body-War | Internal project id for this DomainSpec/Arcanum workspace. | project | selected | stated |
| Runner | Player who records real-world runs to conquer, defend, and progress. | role | draft | observed |
| Run | GPS-recorded activity submitted for validation and game effects. | domain event | draft | observed |
| Hex Zone | Hexagonal map unit that can be neutral, owned, contested, strategic, legendary, event-based, or sponsored. | entity | draft | observed |
| Zone Ownership | Current runner or clan association that controls a zone. | state | draft | observed |
| Zone Score | Composite strength value for a runner in a zone, based on pace, distance, and frequency in the JSX source. | calculation | draft | observed |
| Reference Time | Time/pace target held by the current owner in the GDD source. | calculation | unresolved | observed |
| Invasion | Attempt to take an owned zone by outperforming the current owner. | workflow | draft | observed |
| Defense Window | Period after invasion where the owner or clan can respond before transfer. | workflow | draft | observed |
| Reconquest | Owner response that prevents or reverses territory loss. | workflow | draft | observed |
| Clan | Small social group that coordinates attacks, defenses, wars, bonuses, and collective score. | aggregate | draft | observed |
| XP | Permanent profile progression earned through conquest, defense, performance, missions, and social actions. | metric | draft | observed |
| RunCoins | Virtual currency used for items, clan creation, power-ups, and monetization. | currency | draft | observed |
| League | Monthly competitive tier based primarily on active zones. | progression | draft | observed |
| Season | Longer competitive cycle, usually three months, with seasonal ranking and rewards. | progression | draft | observed |
| Badge | Permanent or semi-permanent recognition such as Pioneiro, Vinganca, Lorde de Bairro, or seasonal titles. | reward | draft | observed |
| Sponsored Zone | Zone linked to a brand partner, with vouchers or real-world rewards. | monetization | draft | observed |

## Bounded Context Definitions

| Context | Responsibility | In Scope | Out Of Scope | Status |
| ------- | -------------- | -------- | ------------ | ------ |
| Runner Identity And Progression | Own runner profile, XP, badges, league, and seasonal identity. | Runner profile, permanent XP, badges, league placement, progression display. | GPS validation, map ownership, payment processing. | candidate |
| Territory Hex Map | Own map partitioning and zone metadata. | Hex size, density, zone type, adjacency, neighborhood labels, sponsored/event flags. | Activity validation and ownership transfer rules. | candidate |
| Run Validation And Anti-Cheat | Decide whether a submitted run can affect game state. | GPS coverage, speed checks, sensor fusion, mock-location detection, risk score, review queue. | UI rendering, monetization, clan ranking. | candidate |
| Zone Conquest And Defense | Own conquest, invasion, defense windows, transfer, cooldown, and caducity. | Neutral conquest, invasion, contested state, defense, reconquest, cooldowns, ownership transfer. | Payment, sponsor sales, account identity. | candidate |
| XP, Rewards, And Seasons | Own XP rewards, multipliers, item rewards, season resets, and reward tiers. | XP sources, multipliers, profile XP permanence, ranking resets, rewards. | Map geometry and raw GPS validation. | candidate |
| Clans And Alliances | Own clans, roles, coordinated attacks, mutual defense, clan wars, and clan score. | Clan membership, hierarchy, score, coffer, wars, alliances/rivals. | Individual GPS capture and sponsored-zone sales. | candidate |
| Monetization And Sponsored Zones | Own premium, RunCoins, battle pass, sponsored zones, events, and B2B offers. | Pricing concepts, conversion triggers, RC packs, sponsor tiers, event revenue. | Core run validation and territory correctness. | candidate |
| Pilot Operations | Own manual or no-code validation before full implementation. | WhatsApp group, manual hex mapping, Strava screenshots, spreadsheets, pilot city. | Production mobile app implementation. | candidate |

## Core Concepts

| Concept | Suggested Meta-Type | Context | Description | Status |
| ------- | ------------------- | ------- | ----------- | ------ |
| Runner | Entity | Runner Identity And Progression | Player identity with profile XP, league, badges, and clan affiliation. | draft |
| Run | Event | Run Validation And Anti-Cheat | Recorded physical activity submitted for validation. | draft |
| Hex Zone | Entity | Territory Hex Map | Territorial unit of play, roughly 400m point-to-point in the GDD. | draft |
| Zone Type | Value Object | Territory Hex Map | Common, strategic, event, legendary, sponsored, or neutral classification. | draft |
| Zone Ownership | State | Zone Conquest And Defense | Current owner and control status of a zone. | draft |
| Zone Score | Calculation | Zone Conquest And Defense | Composite score from pace, distance, and frequency. | draft |
| Invasion | Workflow | Zone Conquest And Defense | Competitive attempt to take a zone. | draft |
| Defense Window | Policy | Zone Conquest And Defense | Timed response period, usually 48h for common zones. | draft |
| Clan | Aggregate | Clans And Alliances | Group of runners that can coordinate defense, attack, wars, and bonuses. | draft |
| XP | Metric | XP, Rewards, And Seasons | Permanent progression points earned from activities. | draft |
| RunCoins | Value Object | Monetization And Sponsored Zones | Virtual currency used for items and premium loops. | draft |
| League | State Machine | Runner Identity And Progression | Recruta, Guerreiro, Comandante, or General based on active zone count. | draft |
| Season | Cycle | XP, Rewards, And Seasons | Three-month competitive period with reset seasonal ranking and persistent XP. | draft |
| Badge | Value Object | Runner Identity And Progression | Visible title or achievement marker. | draft |
| Sponsored Zone | Entity | Monetization And Sponsored Zones | Brand-linked zone with vouchers, rewards, or sponsor analytics. | draft |

## Rules And Policies

| Name | Type | Description | Source | Status |
| ---- | ---- | ----------- | ------ | ------ |
| Hex Coverage Rule | rule | A run must cover at least 60% of a hex perimeter to count for that zone. | GDD/JSX | draft |
| Zone Caducity Policy | policy | A zone not defended or revisited for 14 days returns to neutral. | GDD/JSX | draft |
| Zone Score Formula | calculation | JSX uses Pace Score 40%, Distance Score 35%, Frequency Score 25%, max 550 points. | JSX | draft |
| Common Invasion Window | policy | Common invasion opens a 48h defense/reconquest period. | GDD/JSX | draft |
| Strategic Zone Window | policy | Strategic zones use a harder defense/invasion model and may use a 72h response window. | JSX | draft |
| Invasion Margin Policy | policy | GDD uses minimum 3s/km improvement; JSX uses score margins such as 5 or 15 points. | GDD/JSX | unresolved |
| Invasion Cooldown Policy | policy | Same-zone attacks have cooldowns, commonly 6h for common zones. | GDD/JSX | draft |
| XP Permanence Policy | policy | Profile XP never resets; rankings and score cycles may reset. | GDD/JSX | draft |
| Clan Contribution Policy | policy | JSX says 30% of individual XP contributes to clan score without reducing individual XP. | JSX | draft |
| Clan Coffer Policy | policy | GDD says 10% of RunCoins spent by members go to the clan coffer. | GDD | draft |
| Anti-Cheat Validation Gate | gate | A run must pass automatic validation before affecting territory, XP, or rankings. | GDD | draft |

## External Interfaces

| Interface | Purpose | Owner | Dependency Type | Status |
| --------- | ------- | ----- | --------------- | ------ |
| Mobile GPS Tracking | Capture route, pace, speed, and location stream. | TROQAR app / OS | platform | candidate |
| Mobile Sensors | Provide accelerometer, gyroscope, barometer, and presence evidence. | TROQAR app / OS | platform | candidate |
| Push Notifications | Alert invasion, defense, rewards, and reminders. | Firebase/OneSignal-like provider | partner | candidate |
| Map Provider | Render zones, routes, and city map. | MapBox/Google Maps-like provider | partner | candidate |
| Strava Screenshot Or Activity | Pre-MVP manual validation input. | Runner / Strava | pilot | candidate |
| WhatsApp Group | Pre-MVP pilot coordination and public social loop. | Pilot operator | pilot | candidate |
| Payment Provider | Premium, battle pass, RunCoins, and event fee processing. | Stripe/Mercado Pago-like provider | partner | deferred |
| Sponsor Dashboard | Brand placement and performance reporting. | Sponsor/partner | B2B | deferred |
| Wearable Integrations | Garmin, Apple Health, Google Fit, Samsung Health inputs. | external platforms | partner | deferred |

## Resolved Ambiguities

| Topic | Resolution | Status |
| ----- | ---------- | ------ |
| Project id vs brand | Use `body-war` as internal project id and TROQAR as product brand. | selected |
| First pass scope | Discovery baseline plus game-rules spec, no prototype code. | selected |
| Source policy | GDD, JSX, and images are seed evidence; conflicts are decisions. | selected |
| DomainSpec location | Keep local project bundle at `projects/body-war/domainspec`. | selected |
| Arcanum posture | Initialize local `.arcanum` observability, Necronomicon, and Codex command surface. | selected |

## Unresolved Ambiguities

| Topic | Options | Impact |
| ----- | ------- | ------ |
| Primary competition primitive | Composite Zone Score vs fastest reference time | Affects conquest fairness, balancing, UI, and anti-cheat thresholds. |
| Initial pilot city | Specific city/neighborhood not selected | Blocks concrete map sizing and pilot recruiting plan. |
| MVP posture | Manual pre-MVP vs no-code MVP vs React Native MVP | Affects roadmap and artifact priority. |
| Brand naming | TROQAR app name vs RunWar mechanics lineage | Affects public copy and legal/brand review. |

