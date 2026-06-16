# Decision: Parque Taquaral Online MVP One-Shot

## Decision Gate Result

- Target scope: Body War / Parque Taquaral online MVP one-shot
- Result: `PASS`
- Decisions resolved: 9
- Blockers remaining: 0
- Decision artifact: `projects/body-war/docs/decisions/parque-taquaral-online-mvp-oneshot.md`
- Source forecast: `projects/body-war/docs/features/parque-taquaral-online-mvp/MVP-ONESHOT-FORECAST.md`
- Last updated: 2026-06-14

## Resolved Decisions

### D-OS-001 - Implementation Posture

Question: What implementation posture should the one-shot MVP use?

Considered options:

| Option | Benefit | Cost / Risk | Downstream Impact |
| --- | --- | --- | --- |
| New TypeScript MVP app | Matches the closed architecture/import-boundary decision and keeps the MVP aligned with the future app direction. | More setup before visible progress. | Planning and implementation target a Body War-owned TypeScript app/workspace; the Python app remains prototype evidence. |
| Harden existing Python prototype | Fastest path to visible behavior using already-working Strava OAuth prototype. | Conflicts with the selected TypeScript architecture boundary and may create throwaway work. | Planning continues in `projects/body-war/app/`; architecture debt remains unresolved. |
| Hybrid migration | Preserves working Strava behavior while moving contracts and UI toward TypeScript. | Two surfaces to reason about during one-shot work. | Python stays as live reference while TypeScript ports the minimum flow. |

Selected: `new-typescript-mvp-app`

Rationale: The operator selected option `1`. This follows the already-closed architecture/import-boundary decision: Body War should own a TypeScript app/workspace and consume DomainSpec methods through explicit aliases or source references.

Source of decision: operator answer `1`, 2026-06-14.

### D-OS-002 - App Location And Package Shape

Question: Where should the new TypeScript MVP live?

Considered options:

| Option | Benefit | Cost / Risk | Downstream Impact |
| --- | --- | --- | --- |
| New sibling app folder: `projects/body-war/app-ts/` | Preserves the Python prototype untouched and gives the TypeScript MVP a clean boundary. | Creates a slightly awkward folder name if the TypeScript app becomes the long-term canonical app. | Implementation writes to `app-ts/`; `app/` remains prototype evidence. |
| New canonical app folder: `projects/body-war/app/`, remove Python prototype from live app path | Gives the TypeScript MVP the obvious canonical app path and avoids a long-running split. | Deletes or moves the existing Python prototype and loses the convenience of a working reference surface in-place. | Implementation replaces `projects/body-war/app/` with the TypeScript MVP surface. |
| Package workspace under `projects/body-war/packages/mvp-app/` | Scales better if multiple TypeScript packages are expected soon. | Heavier structure for an MVP and slower to navigate. | Implementation creates a package workspace and may require extra package-management decisions. |

Selected: `canonical-app-folder-replace-python`

Rationale: The operator said "delete python start ts". This selects the canonical app path for the TypeScript MVP and treats the Python prototype as disposable implementation evidence rather than a surface to preserve. Actual file deletion remains deferred until the decision gate passes, because downstream blocker decisions are still open.

Source of decision: operator answer "delete python start ts", 2026-06-14.

### D-OS-003 - Demo States Versus Real Strava Display

Question: Should the TypeScript MVP allow fixture/demo activity states, or only show real Strava data?

Considered options:

| Option | Benefit | Cost / Risk | Downstream Impact |
| --- | --- | --- | --- |
| Allow labeled fixture/demo data plus live Strava | Lets the full UI flow be shown and tested even if Strava returns zero activities. | Requires clear labeling so nobody mistakes demo runs for pilot evidence. | The app can prove UX flow before live data is available. |
| Real Strava data only for the runner-facing MVP | Ensures every visible activity belongs to a consenting runner. | The MVP can block if friend login or Strava activity access fails. | Runner-facing page must use live Strava login/activity data; internal automated tests may still mock API boundaries without showing fake runner data. |
| Fixture only until Strava is reconnected later | Fastest frontend route. | Delays integration risk and weakens the Strava-backed claim. | Useful for product mockups, not sufficient for the intended friend-data page. |

Selected: `real-friend-strava-data-for-runner-facing-mvp`

Rationale: The operator said they want "a page so we can have a friend logging in and providing his data" and that "we already have the data there." This resolves the runner-facing MVP toward live consenting Strava data, not fake activity data presented as evidence.

Source of decision: operator answer "i want a page so we can have a friend logging in and providing his data, we already have the data there", 2026-06-14.

Follow-on impact: D-OS-009 deployment/access is now a blocker rather than a local-first assumption, because friend login requires a reachable page, valid Strava callback configuration, and safe secret/token handling.

### D-OS-004 - Track Geometry Claim Level

Question: What may the MVP page claim about Parque Taquaral track geometry?

Considered options:

| Option | Benefit | Cost / Risk | Downstream Impact |
| --- | --- | --- | --- |
| Context-only park page, no route geometry claims | Safest; the page can name Parque Taquaral as the pilot context without implying a validated track. | Less concrete and less product-like. | Friend submits to a general park context; track-control behavior remains under-specified. |
| Named draft track card with explicit "not GPS-validated yet" status | Gives the page a concrete track/control object while staying careful about geometry. | Still requires careful wording and later geometry completion. | App can show track-control UI, but GPS validation remains flagged. |
| Use existing Parque Taquaral track data as the MVP pilot boundary and finish the full track geometry | Strongest product feel and aligns the pilot with the real intended track. | Requires completing and validating the full track geometry artifact before claiming GPS validation is done. | Implementation should model the whole Parque Taquaral track as the pilot track; geometry completion becomes part of MVP scope rather than a later vague gap. |

Selected: `existing-parque-taquaral-track-as-pilot-geometry`

Rationale: The operator said they want the geometry next and that the MVP "needs to finish the whole Parque Taquaral track"; because the track already exists, it is easier to make that track the pilot. This selects the real Parque Taquaral track as the MVP pilot target instead of a generic park context or purely draft card.

Source of decision: operator answer "i think i want the geomotry for next, now it needs to finish the whole parque taquaral track, there track alredy exists so it easier to make th track as the pilot", 2026-06-14.

Guardrail: this decision does not close `GAP-TAQUARAL-GEOMETRY-001` by itself. The gap closes only when the full track geometry artifact exists and the app clearly distinguishes submitted activity evidence from validated GPS boundary proof.

### D-OS-005 - Evidence Acceptance And Review Status Model

Question: When should a friend's submitted Strava activity affect the public controller state?

Considered options:

| Option | Benefit | Cost / Risk | Downstream Impact |
| --- | --- | --- | --- |
| Auto-accept matching Strava activity for preview | Fastest friend flow: login, pick activity, submit, and see controller update. | Weak review and anti-cheat; the submitted activity may not actually match the full track geometry until geometry validation is implemented. | Hosted preview can update controller state immediately from friend Strava data, while validation claims remain limited. |
| Submitted first, operator verifies before controller update | Safer and closer to the evidence-review loop. | Requires an operator review action before the page changes controller. | More trustworthy pilot operation, but slower friend demo. |
| Geometry match required before controller update | Strongest correctness claim. | Blocks controller updates until full geometry validation exists. | Best for validated track-control proof, too heavy for quick preview. |

Selected: `auto-accept-matching-strava-activity-for-preview`

Rationale: The operator selected option `1`. The hosted MVP should make the friend flow immediate: a friend logs in with Strava, submits an activity for the Parque Taquaral pilot track, and the preview controller state updates without waiting for manual review.

Source of decision: operator answer `1`, 2026-06-14.

Guardrail: auto-acceptance is for the hosted preview controller loop only. It must not be described as complete anti-cheat, operator verification, or final GPS geometry validation.

### D-OS-008 - Validation Proof Level

Question: What validation proof is required before we call the one-shot implementation acceptable?

Considered options:

| Option | Benefit | Cost / Risk | Downstream Impact |
| --- | --- | --- | --- |
| Preview validation only | Fastest path to the friend-facing outcome: app builds, hosted preview deploys, Strava login works, friend activity appears, and controller updates. | Weaker architecture and automated test proof. | Acceptance centers on the hosted flow working end to end for the friend preview. |
| Preview plus engineering checks | Balances speed with reliability by adding TypeScript typecheck, basic API tests, no-secret checks, and smoke tests. | More implementation time. | Reduces risk of a shaky MVP while still staying one-shot friendly. |
| Full readiness validation | Strongest confidence, including geometry artifact validation, architecture import-boundary check, token persistence review, and pilot-ready evidence. | May delay or block the quick hosted preview. | Better for pilot readiness than for a fast preview. |

Selected: `preview-validation-only`

Rationale: The operator selected option `1`. The one-shot implementation should be judged primarily by whether the hosted friend-facing flow works: deploy, Strava login, friend activity visibility, submission, and preview controller update.

Source of decision: operator answer `1`, 2026-06-14.

Guardrail: this validation level is not enough to claim full engineering readiness, final GPS validation, or anti-cheat readiness.

### D-OS-012 - MVP Success Definition

Question: What label should count as success for this one-shot?

Considered options:

| Option | Benefit | Cost / Risk | Downstream Impact |
| --- | --- | --- | --- |
| Hosted friend preview succeeds | Matches the current goal exactly: hosted TypeScript app, friend Strava login, activity appears, submission works, and controller updates. | Does not prove full pilot readiness, engineering readiness, anti-cheat readiness, or final GPS geometry validation. | The implementation can proceed toward a hosted friend-facing preview and stop when that flow works. |
| Pilot-ready MVP succeeds | Stronger product confidence: hosted flow plus geometry and validation strong enough to claim real pilot readiness. | Likely larger than the one-shot and may block quick delivery. | Requires closing geometry validation and stronger evidence review before success. |
| Engineering-ready MVP succeeds | Safer build quality: hosted flow plus tests, architecture checks, no-secret checks, and managed persistence verification. | More engineering time than preview-only. | Better for maintainability, but heavier than the requested friend-preview target. |

Selected: `hosted-friend-preview-succeeds`

Rationale: The operator selected option `1`. Success for this one-shot is the hosted friend preview: the TypeScript app is hosted, a friend can log in with Strava, activity data appears, submission works, and controller state updates.

Source of decision: operator answer `1`, 2026-06-14.

Guardrail: this success label must not be renamed to pilot-ready or engineering-ready unless later work closes the additional geometry, validation, persistence verification, and test obligations.

### D-OS-009 - Deployment / Access Surface For Friend Login

Question: How should the friend access the Strava login page?

Considered options:

| Option | Benefit | Cost / Risk | Downstream Impact |
| --- | --- | --- | --- |
| Hosted public preview URL | Easiest for the friend: they open a URL, log in, and provide data. | Requires HTTPS, a public Strava callback URL, deployment setup, environment secrets, and safer token handling. | The MVP must include deployable TypeScript app/runtime configuration and hosted-preview security checks. |
| Local machine with tunnel URL | Faster than full hosting and enough for one live remote test. | Fragile; depends on local machine uptime, tunnel stability, and temporary callback URLs. | Good for a one-off live proof but weaker as an MVP access surface. |
| Friend logs in on operator's local machine | Simplest infrastructure and easiest secret control. | Friend must be physically present or screen-shared; does not prove remote access. | Useful for data capture only, not for a shareable friend login page. |

Selected: `hosted-public-preview-url`

Rationale: The operator selected option `1`. The one-shot MVP should provide a public hosted preview URL so a friend can open the page, complete Strava login, and provide real activity data.

Source of decision: operator answer `1`, 2026-06-14.

Follow-on impact: D-OS-006 persistence and token handling must be resolved before implementation because hosted friend login cannot rely on local JSON token files or committed environment files.

### D-OS-006 - Persistence And Token Handling

Question: How should the hosted MVP store Strava tokens and submitted activity evidence?

Considered options:

| Option | Benefit | Cost / Risk | Downstream Impact |
| --- | --- | --- | --- |
| Hosted managed storage with encrypted/sealed secrets | Appropriate for a public preview URL with real friend login and Strava token/data handling. | Requires choosing and configuring a hosted persistence path. | Implementation must use hosted environment secrets and managed persistence; local JSON token files are not acceptable for the hosted MVP. |
| Ephemeral server memory only | Fastest and avoids writing tokens to disk. | Login/data disappears on restart; OAuth and evidence review can be brittle. | Useful for a one-session throwaway test, but weak for a usable friend preview. |
| Local/dev JSON files even in hosted preview | Simplest port from the Python prototype. | Poor fit for hosted token safety and deployment; easy to mishandle secrets/data. | Keeps implementation cheap but fails the safety bar for real friend data. |

Selected: `hosted-managed-storage-with-sealed-secrets`

Rationale: The operator selected option `1`. Because the MVP will be accessed through a hosted public preview URL by a friend using real Strava data, the implementation must use hosted environment secrets and managed persistence rather than committed files, local JSON token stores, or process memory as the authoritative store.

Source of decision: operator answer `1`, 2026-06-14.

## Remaining Blocker Decisions

None.

## Deferrable Decisions And Assumptions

- D-OS-007 runner/operator UI boundary is assumed to be one compact web UI unless later work reveals a strong reason to split surfaces.
- D-OS-010 monetization and economy remain out of scope.
- D-OS-011 anti-cheat and GPS automation remain out of scope beyond manual plausibility review and metadata preservation.

## Next Gate

All blocker decisions are resolved. Proceed to the Parque Taquaral online MVP `WORK-PACK.md` and implementation planning.
