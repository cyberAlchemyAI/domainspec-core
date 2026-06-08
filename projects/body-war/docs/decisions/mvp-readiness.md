# Body War MVP Readiness Decisions

## Decision Gate Result

- Target scope: Body War / TROQAR MVP readiness
- Result: BLOCK
- Decisions resolved: 5
- Blockers remaining: 2
- Decision artifact: `projects/body-war/docs/decisions/mvp-readiness.md`
- Deferred decisions: monetization can be deferred for L0 if the operator accepts a no-economy pilot; physical park/city selection is deferred until the real-world TROQAR runner pilot.
- Assumptions recorded: Park Track Control is the product L0 candidate from commit `6d2ff7c`; Craft is the internal refinement pilot context for closing MVP decisions and gaps.
- Validation: current branch and git history checked; runtime command resolution checked; scaffold restored from `6d2ff7c`.
- Next step: ask remaining decision

## Current Blocker Decisions

### DG-001 - Project State Anchor

Question: Should the full `projects/body-war` scaffold from commit `6d2ff7c` / `master` be restored before the refine run executes?

Options:

- Restore scaffold first. Benefit: refine runs against live project files. Cost: introduces a large project tree into the current branch and may interact with branch scope. Choose when this branch is allowed to carry Body War work.
- History-backed refine first. Benefit: avoids broad branch mutation. Cost: final plan must include a rehydration step before implementation. Choose when this branch should remain narrow.

Selected: Restore scaffold first.

Rationale: The operator answered "yes" to restoring the full `projects/body-war` scaffold from commit `6d2ff7c` / `master` before running the refinement loop. This lets subsequent refinement mutate live project files rather than planning against history-only evidence.

Source: operator answer, 2026-06-08.

### DG-002 - L0 Pilot Location

Question: What city and first park should the L0 pilot use?

Options:

- Campinas local park. Benefit: likely practical for local recruiting and manual operation. Cost: needs exact park and track boundaries.
- Sao Paulo neighborhood park. Benefit: larger runner density. Cost: higher coordination burden.
- Defer location and design generic track-card templates. Benefit: faster artifact work. Cost: implementation cannot start.

Selected: Use `arcanum/development/craft/` as the pilot context for this refinement run.

Rationale: The operator explicitly selected Craft as the pilot. Craft has a mature local evidence surface with MVP design, ledger schema, validation examples, task sessions, prior refine runs, and current blocker evidence. This makes it suitable for proving the decision/refine/interrogation route before applying the same governance pattern to a real-world TROQAR park pilot.

Scope clarification: this resolves the pilot context for the current MVP-readiness refinement. It does not select the future physical city/park for runner recruitment; that decision is deferred until the Body War product pilot exits the internal governance pilot.

Source: operator answer, 2026-06-08.

### DG-003 - Craft Pilot Slice

Question: Which Craft slice should be the pilot for this run?

Options:

- Aggregate Refine receipt / Distill blocker. Benefit: directly tests the active Refine blocker and the route we need for Body War readiness. Cost: narrower than the whole Craft package.
- Recursive ledger MVP. Benefit: stable validated artifact model with schema, fixture, and validation evidence. Cost: already passed as an MVP, so it is less useful as the active blocker.
- Validation guide. Benefit: strong recomposition and validation surface. Cost: more review-oriented than execution-oriented.
- Missing-work live test. Benefit: close to recent live execution. Cost: can become broad unless bounded to one blocker.

Selected: Aggregate Refine receipt / Distill blocker as the active pilot, with Recursive Ledger MVP as the fixture and recomposition substrate.

Rationale: The operator answered "1 and 2". This keeps the active pilot focused on the current aggregate Refine receipt and Distill blocker while grounding the test in the recursive ledger MVP's validated schema and fixture. The pair tests the same governance path needed by Body War: a route can carry unresolved decisions, refine blockers, validation evidence, and recomposition back into an MVP plan.

Source: operator answer, 2026-06-08.

### DG-004 - L0 Scoring Authority

Question: What metric decides the current controller in L0?

Options:

- Fastest verified time. Benefit: easiest to explain and manually verify. Cost: may over-reward speed over repeat presence.
- Composite Zone Score. Benefit: closer to TROQAR gamification source. Cost: harder to explain and operate manually.
- Fastest time for public controller plus hidden composite score analysis. Benefit: simple pilot plus learning. Cost: extra operator work.
  Selected: Hybrid pattern.

Rationale: The operator selected option 3. For Body War L0, fastest verified time is the public track-control authority because it is simple to explain and manually verify, while composite score is recorded in parallel as hidden analysis for fairness and future balancing. For Craft, aggregate Refine receipt status is the public readiness controller, while recursive-ledger MVP evidence remains the richer substrate for recomposition and review.

Source: operator answer, 2026-06-08.

### DG-005 - L0 Validation Channel

Question: How do runners submit evidence in L0?

Options:

- WhatsApp plus Strava screenshots. Benefit: lowest build cost. Cost: manual review and screenshot ambiguity.
- No-code form plus Strava link/screenshot. Benefit: cleaner log. Cost: setup overhead.
- App-backed MVP. Benefit: closer to final product. Cost: too heavy before behavior is proven.

Selected: App/runtime-backed MVP with Strava API integration.

Rationale: The operator said the project needs a web app with Strava API linking and a backend. This upgrades the validation channel from no-code/manual capture to an app-backed pilot. The first implementation remains deliberately small: a Python standard-library backend, Strava OAuth, recent activity fetch, and a track evidence submission flow. This satisfies app-backed validation without prematurely building the full mobile app, map engine, anti-cheat system, or monetization layer.

Source: operator answer, 2026-06-08.

### DG-006 - L0 Monetization Scope

Question: Does MVP include economy or monetization?

Options:

- Defer all monetization. Benefit: protects behavior test from reward distortion. Cost: no revenue learning in L0.
- XP-only visible progression. Benefit: adds motivation without payments. Cost: still requires scoring clarity.
- Premium/sponsor/RunCoins hooks. Benefit: tests commercial story. Cost: distracts from core loop.

Selected: unresolved.

### DG-007 - Runtime Execution Surface

Question: How should the refine route run when some repo-local command handles do not resolve?

Options:

- Repair repo-local command surface first. Benefit: clean Arcanum execution contract. Cost: extra setup work before refinement.
- Use installed native skill fallback. Benefit: lets refinement proceed now. Cost: command-surface proof remains incomplete.

Selected: unresolved.

## Deferrable Decisions

- Clan mechanics.
- XP values and economy balance.
- Hex grid geometry.
- Automated anti-cheat.
- Sponsor rewards.
- App architecture.

These should stay outside L0 unless the operator explicitly expands the MVP.
