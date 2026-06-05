---
feature: park-track-pilot
version: current
status: draft
updatedAt: 2026-05-26
docType: implementation-layering
owners:
  - body-war
---

# Park Track Pilot Implementation Layering

This document defines a progressive implementation layering model for TROQAR's first candidate: selected parks with delimited tracks.

Scope note: Layer 0 is a minimum working unit POC that proves whether real runners care about controlling and defending named tracks in a real park. Every later layer improves the previous layer without invalidating the core guarantee: a runner can run a known route, become controller, be challenged, and have a reason to return.

## Layering Method

- POC-first: prove the park-track control loop with manual evidence before building app infrastructure.
- Progressive hardening: add repeatability, policy depth, automation, and scale only after behavior is observed.
- Non-regression: later layers must preserve the L0 controller/challenge/defense loop.

## Layer Boundary Heuristic

A layer ends at the smallest slice that changes what the team can responsibly decide next.

```text
Layer value = decision unlocked + user-visible outcome + risk reduced
Layer cost = implementation time + verification time + coordination burden
```

Stop a layer when the next unit of work adds less value-per-cost to the current decision than starting the next decision layer.

## Layer Decision Framing

| Layer | Decision Question | Minimum Working Unit | Deferred Scope | Promotion Decision |
| ----- | ----------------- | -------------------- | -------------- | ------------------ |
| L0 (POC) | After this layer, we know whether runners care about controlling and defending named park tracks at all. | One park, 2-3 delimited tracks, manual run evidence, current controller, challenge, and 48h defense window. | Hex grid, app GPS, composite score, clans, XP economy, anti-cheat automation. | Continue if challenged controllers return or challengers repeat. |
| L1 | After this layer, we know whether the park-track loop is repeatable with low operator burden. | Repeat the same workflow across multiple sessions and formalize track cards, run submission, and results log. | Multiple parks, app implementation, advanced scoring, sponsor/reward loops. | Harden if admin can run the loop without confusion. |
| L2 | After this layer, we know whether scoring and dispute policy can stay trusted under real competition. | Add simple policy depth: score rule decision, tie handling, invalid run handling, evidence review, and dispute log. | Sensor fusion, automated GPS validation, monetization, clans. | Scale if disputes are rare and decisions are accepted. |
| L3 | After this layer, we know whether park tracks can expand into a city pilot without losing clarity. | Add multiple selected parks, a territory-unit registry, lightweight automation, and recurring weekly standings. | City-wide hexes, full mobile app, marketplace/economy, sponsor dashboard. | Move to app/hex design if repeat behavior and operator workflow both hold. |

## Capability-To-Layer Progression

| Capability | Layer 0 (POC Proof) | Layer 1 (Repeatability) | Layer 2 (Policy Trust) | Layer 3 (Pilot Scale) |
| ---------- | ------------------- | ----------------------- | ---------------------- | --------------------- |
| Territory Unit | Named park track | Standard track card | Track registry with rule fields | Multi-park territory registry |
| Run Evidence | Strava screenshot/manual confirmation | Submission template and result log | Evidence review/dispute rules | Lightweight form or app-assisted capture |
| Control | Current controller per track | Historical controller log | Tie/invalid-run policies | Weekly standings across parks |
| Challenge/Defense | Challenge opens 48h defense window | Repeatable notification template | Defense outcome rules | Recurring weekly operating cadence |
| Scoring | Fastest verified time by default | Compare optional composite score offline | Select scoring authority | Prepare for app/zone abstraction |

## Layer Definitions

| Layer | Objective | Builds On | Primary Scope | Exit Evidence | Value/Cost Notes |
| ----- | --------- | --------- | ------------- | ------------- | ---------------- |
| L0 (POC) | Prove the track-control behavior exists. | none | One park, 2-3 tracks, manual controller/challenge/defense loop. | Defense attempts, repeat submissions, runner feedback. | Highest value per cost because no map/app infrastructure is needed. |
| L1 | Prove the loop can be operated repeatedly. | L0 | Repeat sessions, track cards, submission template, results log. | Operator time per run, fewer clarification messages, repeatable standings. | Adds structure only where L0 friction appears. |
| L2 | Prove trust under competition. | L1 | Score authority, tie rules, invalid-run policy, dispute log. | Low dispute rate, accepted rulings, clear rule comprehension. | Worth it only after people compete enough to care. |
| L3 | Prove city pilot expansion. | L2 | Multiple parks, territory-unit registry, lightweight automation, weekly standings. | Activity across parks, operator capacity, readiness for app/hex decision. | Scale work waits until repeatability and trust are proven. |

## Layer 0 - Minimum Working Unit POC

### Goal

Run a manual pilot in one selected park with two or three delimited tracks to test whether runners value controlling, challenging, and defending a known place.

### Included Scope

- Select one city park.
- Define two or three named tracks with clear start/end or route boundaries.
- Create a simple public control board: track, current controller, current time/score, challenge status, defense deadline.
- Accept run evidence manually, initially through Strava screenshot or equivalent proof.
- Use fastest verified time as the default L0 scoring metric for cognitive simplicity.
- Notify the current controller when challenged.
- Give the controller 48h to defend.
- Record whether the controller returns, challenger repeats, or both disengage.

### Explicitly Deferred Beyond L0

- Hex zones and map tiling.
- App GPS capture.
- Composite score authority.
- XP, RunCoins, badges, leagues, seasons.
- Clan mechanics.
- Anti-cheat beyond manual plausibility review.
- Sponsor rewards and monetization.
- Multi-park automation.

### User-Visible Or Operator-Visible Outcome

- Runners can see who controls each track.
- A runner can challenge a controller by running the delimited track.
- A controller has a concrete reason to return within 48h.
- The operator can see whether the loop creates repeat activity.

### Risk Reduced

- Reduces risk of overbuilding hex/map infrastructure before proving behavior.
- Reduces cognitive load for early runners.
- Reduces implementation cost while preserving territorial meaning.

### Main Cost Drivers

- Selecting and describing safe/clear tracks.
- Recruiting a small runner cohort.
- Manual evidence review.
- Maintaining the control board and notifications.

### Exit Evidence

- At least one challenged controller attempts a defense, or a clear reason why they did not.
- At least one challenger repeats or challenges another track.
- Operator can update the board without ambiguity.
- Runner feedback shows they understood controller/challenge/defense language.

### Promotion Decision

- Continue when: runners understand the loop and at least some challenged controllers return.
- Pivot when: runners like track rankings but do not care about defense; consider leaderboard-only or event format.
- Stop when: runners do not submit repeat runs and do not care about controller status.

## Layer-By-Layer Improvements

### Layer 1 Improvements Over L0

- Added scope: repeat the same pilot cadence for multiple days or weeks.
- Hardening delta: track cards, submission template, result log, notification copy, and operator checklist.
- Verification delta: measure operator time, submission clarity, and repeated challenge/defense events.

### Layer 2 Improvements Over Layer 1

- Added scope: scoring and dispute policy depth.
- Hardening delta: choose fastest time, composite score, or hybrid for active pilot; add tie, invalid-run, and manual-review rules.
- Verification delta: track disputes, accepted rulings, and runner comprehension.

### Layer 3 Improvements Over Layer 2

- Added scope: selected multi-park pilot and territory-unit registry.
- Hardening delta: lightweight automation and weekly standings.
- Verification delta: compare activity across parks and assess readiness for app-backed territory units.

## Implementation Wave Backbone

| Wave | Target Layer | Goal | Key Artifacts | Verification |
| ---- | ------------ | ---- | ------------- | ------------ |
| W0 | L0 | Complete one-park manual proof. | `DISTILL.md`, `implementation-layering.md`, track control board, pilot notes. | Manual run log and runner feedback. |
| W1 | L1 | Make the workflow repeatable. | Track card template, submission template, operator checklist. | Operator time and fewer ambiguous submissions. |
| W2 | L2 | Make scoring and disputes trusted. | Scoring decision, dispute policy, invalid-run policy. | Low dispute rate and accepted rulings. |
| W3 | L3 | Prepare selected park expansion. | Territory-unit registry, weekly standings, lightweight automation notes. | Multi-park activity and app/hex readiness decision. |

## Source-Of-Truth References

- `DISTILL.md`
- `../game-rules/SPEC.md`
- `../../PROJECT-OVERVIEW.md`
- `../../PROJECT-DECISIONS.md`
- `../../EXPERIMENT-CANDIDATES.md`

## Open Decisions

- First city and first selected park.
- Exact track boundary description format.
- Whether L0 uses fastest verified time only or records composite score in parallel as hidden analysis.
- Notification channel for challenge/defense during L0.
