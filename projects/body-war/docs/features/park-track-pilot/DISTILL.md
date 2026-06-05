# Park Track Pilot Distill Result

## Target Context

Body-War/TROQAR needs a first candidate that can prove the territory-running loop before city-wide hex maps, automated geospatial indexing, native GPS validation, clans, monetization, or full anti-cheat exist.

The user proposed selected parks in the city with delimited tracks instead of starting with hex zones. This is the seed point for the distillation.

## Objective And Output Artifact

- Objective: reduce the broad TROQAR territory game into the smallest coherent candidate that still proves real-world running competition, place attachment, defense pressure, and repeat activity.
- Output artifact: a navigable candidate design plus implementation layering route.
- Optimization goal: clarity and first-test readiness.

## Mode And Budget

- Mode: Standard.
- Budget: one proposal track, role-simulated Proposer and Balancer, two recursive rounds, one reconciliation.
- Assumption: user did not specify Compact, Standard, Tournament, Deep, or Validate; Standard was selected by default.

## Discovery Baseline

Evidence already in the project:

- `docs/PROJECT-OVERVIEW.md` frames TROQAR as a real-world territorial running game.
- `docs/features/game-rules/SPEC.md` captures hex zones, conquest, defense windows, scoring, XP, clans, seasons, and anti-cheat.
- `docs/research/source-notes/runwar-gdd.md` says the pre-MVP can use WhatsApp, Strava screenshots, manual admin registration, and first mapped areas before code.
- `docs/research/source-notes/troqar-gamificacao-jsx.md` gives a composite score pattern: pace, distance, and frequency.

New user constraint:

- Do not start with hex zones.
- Start with selected parks in the city.
- Use delimited tracks.

## Role Conversation Trace

### Round 1

Proposer claim: The first coherent unit should be "one selected park, one delimited track, one leaderboard/control loop."

Evidence or assumption:

- It preserves the real place, running action, competitive ownership, and repeat-defense loop.
- It avoids exact city-wide hex partitioning and 60% perimeter validation.
- It can be validated manually with Strava screenshots and admin review.

Balancer objection category: scope-risk.

Objection:

- A single park track may prove leaderboard competition but not territory conquest if there is only one asset to control.

Reconciliation:

- Revise the unit to "one selected park with two or three named delimited tracks or segments." This keeps territory meaningful without requiring hex infrastructure.

### Round 2

Proposer claim: The smallest coherent unit is "Park Track Control": selected parks contain named tracks; runners submit runs for a named track; the current controller is determined by one simple metric; an invasion notice creates a defense window.

Evidence or assumption:

- Tracks act as concrete territory objects.
- The game loop is still conquer, get challenged, defend, and repeat.
- Track boundaries are easier to explain and inspect than abstract hexes.

Balancer objection category: recomposition-risk.

Objection:

- If the candidate uses park tracks, it may not recompose into the later hex-zone model.

Reconciliation:

- Treat `Track` as the pilot form of `Territory Unit`. Later, `Hex Zone` becomes another territory-unit geometry. The same ownership, challenge, defense, scoring, and validity concepts can recompose upward.

Stable disagreement:

- Whether the first score authority should be fastest reference time or composite score remains unresolved. The candidate can start with fastest verified time for cognitive simplicity and record composite score as L1/L2 evolution.

## Current Smallest Coherent Unit

**Park Track Control**

Responsibility: prove that runners care about controlling a named real-world running track enough to return, challenge, and defend within a simple time window.

Inputs:

- A selected park.
- Two or three named delimited tracks.
- A small runner cohort.
- Submitted run evidence, initially Strava screenshot/manual confirmation.
- A simple scoring metric for each track.

Outputs:

- Current controller per track.
- Challenge/defense status per track.
- Defense attempts and outcomes.
- Retention and repeat-run evidence.

## Optimization Point

Park Track Control is smaller than city hex territory but larger than a generic leaderboard. It is the best first size because it retains the meaning of territorial control while cutting the hard parts that would slow the first proof:

- no city-wide hex generation,
- no adjacency graph,
- no automatic GPS polygon coverage,
- no complex zone taxonomy,
- no sponsor/economy layer,
- no full anti-cheat stack.

## Concept Layer Map

| Layer | Concept | Notes |
| ----- | ------- | ----- |
| Broad product | TROQAR territorial running game | Real-world places become competitive assets. |
| Game system | Territory control loop | Run, claim, challenge, defend, repeat. |
| Candidate unit | Park Track Control | Tracks are the first territory units. |
| Minimum proof | One park, 2-3 tracks, manual evidence | Enough to test behavior before infrastructure. |

## Technique Pack Trace

| Technique | Activation Reason | Output | Decision | Readiness Effect |
| --------- | ----------------- | ------ | -------- | ---------------- |
| Abstraction-level guard | Needed to avoid reducing to a mere leaderboard. | Keep territory unit plus defense loop. | pass | Candidate remains game-shaped. |
| Recomposition proof | Needed because hexes are deferred. | Track is a pilot `Territory Unit`; hex can be later geometry. | pass | Avoids throwaway model. |
| Evolution profile | Future path includes parks, city areas, hexes, app GPS. | Preserve geometry boundary and scoring boundary. | pass | Keeps extension light. |
| Frame-expiry note | Candidate depends on manual/local pilot. | Expires when testing requires multiple neighborhoods or automated app validation. | pass | Prevents overclaiming. |
| Navigable result check | User asked for first candidate. | Route to implementation layering. | pass | Ready for staged plan. |
| Cognitive load check | Triggered by user concern that hexes may be too much. | Use named park tracks and fastest verified time for L0. | pass | Simpler runner/operator explanation. |
| Premortem | Triggered by pilot/product risk. | Failure likely if runners see tracks as leaderboard only. | flag | Add defense window and controller status in L0. |

## Closure And Recomposition Proof

Closure:

- Responsibility is bounded to one park pilot.
- Inputs and outputs are named.
- The unit produces evidence without app implementation.
- It has a visible user outcome: track controller status.
- It has a decision outcome: whether to continue, pivot, or stop.

Recomposition:

- `Park Track` later becomes one implementation of `Territory Unit`.
- `Controller`, `Challenge`, `Defense Window`, and `Run Evidence` map directly into later zone/hex concepts.
- Composite score, clans, seasons, and anti-cheat can attach after the control loop proves behavior.

## Evolution Profile

Expected evolution:

1. One park with manually delimited tracks.
2. Multiple parks with repeated operator workflow.
3. App-assisted track submission and validation.
4. Territory unit abstraction that supports both tracks and hex zones.
5. City-wide map expansion only after repeat behavior is proven.

Smallest extension boundary:

- Define `Territory Unit` as a concept with `id`, `name`, `geometry kind`, `rules`, and `current controller`.
- For L0, only instantiate it as `Park Track`.

## Deferred Complexity

- Hex grid generation.
- Adjacency and kingdom mechanics.
- Zone type taxonomy beyond "park track."
- Clans and clan defense.
- XP economy and RunCoins.
- Automated GPS validation.
- Sensor-fusion anti-cheat.
- Sponsorship and monetization.

Deferred because none of these are required to decide whether real runners care about controlling and defending a known track.

## Tension Ledger

| Tension | Status | Resolution |
| ------- | ------ | ---------- |
| Hex zones vs park tracks | resolved for first candidate | Start with park tracks; preserve territory-unit abstraction. |
| Leaderboard vs territory | resolved | Require current controller plus challenge/defense window, not only rankings. |
| Fastest time vs composite score | unresolved | Use fastest verified time in L0 for simplicity; revisit in L1/L2. |
| Manual evidence vs app validation | resolved for L0 | Manual Strava/operator evidence is enough for first proof. |

## Premortem

Likely failure reason:

- Runners treat it as a casual leaderboard and do not feel ownership or loss.

Guardrail:

- Every track must show one current controller, every challenge must notify the controller, and every challenge must create a clear defense window.

## Frame-Expiry Note

This optimization point expires when:

- the pilot spans multiple parks with enough activity to require automation,
- runner disputes exceed what manual review can resolve,
- or the team needs to validate city-scale exploration rather than repeat behavior on known tracks.

## Navigation Guide

Start here:

- Use `docs/features/park-track-pilot/implementation-layering.md`.
- Treat the L0 target as one park, 2-3 delimited tracks, manual evidence, and a controller/defense loop.

What changed:

- First candidate is park-track control, not hex-zone conquest.

What remains unresolved:

- Primary scoring metric after L0.
- Pilot city and first park selection.
- Whether L1 introduces composite score or simply makes fastest-time proof repeatable.

## Next Route

implementation-layering
