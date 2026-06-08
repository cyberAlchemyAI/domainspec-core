# Body War MVP Readiness Refine Seed

## Target

`projects/body-war` / TROQAR, the GPS-based territorial running game project.

## Operator Intent

Create a strategy so the project can be refined into an MVP-ready plan with decisions and gaps closed through `decision-gate` and one-question-at-a-time `interrogation`.

## Current Evidence Baseline

- Current branch: `codex/goldenquill-client-package`.
- `projects/body-war` is absent from `HEAD` on the current branch.
- Git history contains scaffold commit `6d2ff7c` on `master`: `Add Body War project scaffold`.
- Scaffold commit evidence says the product brand is TROQAR, project id is `body-war`, and the first feature slice is `game-rules`.
- Scaffold commit evidence says the first candidate is `Park Track Control`: one selected park, two or three delimited tracks, manual run evidence, current controller, challenge, and a 48h defense window.
- Scaffold commit evidence records unresolved project decisions: conquest metric, pilot city, validation channel, monetization scope, and first park/track set.
- Operator selected `arcanum/development/craft/` as the internal pilot context for this MVP-readiness refinement.
- Operator selected the aggregate Refine receipt / Distill blocker plus recursive ledger MVP fixture as the bounded Craft pilot slice.

## Desired Outcome

An MVP-ready non-executed plan that first proves the refine/decision/interrogation route against Craft as an internal pilot, then recomposes the resulting governance pattern into TROQAR L0: one park, two or three delimited tracks, manual evidence submission, controller/challenge/defense loop, and acceptance criteria for whether to continue, pivot, or stop.

## Preset

`standard`

## Research Mode

`research-if-gap-appears`

Use local repository and recovered commit evidence first. External research is deferred unless a named gap appears during interrogation or distill and the operator approves bounded research.

## Write Scope

Allowed before confirmation:

- This refinement run folder.
- Decision gate artifact for Body War MVP readiness.
- Interrogation kickoff artifact.

Blocked before confirmation:

- Restoring or merging the full `projects/body-war` scaffold from `master`.
- Implementing app or prototype code.
- Changing canonical project decisions beyond recording operator answers.

## Done Criteria For The Refine Run

- Project state is rehydrated or explicitly blocked.
- Blocker-level MVP decisions are resolved or recorded as blocking.
- L0 MVP scope is reduced to a coherent, testable unit.
- Interrogation has collected enough human answers to close pilot assumptions.
- Final plan names artifacts, workflows, validation surface, exit evidence, and next route.

## Planned Stage Configuration

1. Context Builder evidence baseline over current branch plus commit `6d2ff7c`.
2. Invoke Define for MVP-ready scope.
3. Interrogation `refine-review`.
4. Research decision.
5. Distill coherent L0 unit.
6. Invoke Design.
7. Interrogation `refine-design-review`.
8. Distill Repair.
9. Invoke Plan.
10. Final Interrogation and Refine-owned synthesis.

## Initial Blockers

- The current branch does not contain the project scaffold that exists on `master`.
- The deterministic command surface resolves `context-builder`, `distill`, and `decision-gate`, but not `invoke`, `interrogation`, or `refine` through `arcanum/tools/arcanum --resolve`.
- MVP implementation should not begin until scoring authority, validation channel, monetization scope, and runtime execution surface are resolved.
