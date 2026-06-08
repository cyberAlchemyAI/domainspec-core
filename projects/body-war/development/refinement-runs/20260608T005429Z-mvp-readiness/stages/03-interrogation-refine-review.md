# Interrogation Kickoff - Refine Review

## Structured Interview Result

- Target scope: Body War / TROQAR MVP readiness
- Mode: `refine-review`
- Questions asked: 5
- Decisions recorded: 5
- Artifacts updated: `projects/body-war/docs/decisions/mvp-readiness.md`
- Remaining ambiguities: monetization scope, runtime execution surface
- Verdict: block
- Next step: ask the next blocker question

## First Question

Context: the Body War scaffold exists in git history at commit `6d2ff7c` on `master`, but `projects/body-war` is absent from the current branch `codex/goldenquill-client-package`.

Why this matters: a full refine run can either operate on restored live project files or stay history-backed and produce a plan that includes rehydration later. Restoring first is cleaner for artifacts, but it is a bigger branch mutation.

Recommended default: restore the scaffold first if this branch is allowed to carry Body War work; otherwise choose history-backed refine first.

Unresolved risk if unanswered: downstream artifacts may be written against a target folder that is not the actual project source of truth.

Target artifact: `projects/body-war/docs/decisions/mvp-readiness.md`

Question: should I restore the full `projects/body-war` scaffold from commit `6d2ff7c` / `master` before running the refinement loop, or keep this run history-backed for now?

Answer: restore the scaffold first.

Decision recorded: DG-001 in `projects/body-war/docs/decisions/mvp-readiness.md`.

## Next Question

Context: the L0 MVP candidate is Park Track Control: one selected park, two or three delimited tracks, manual evidence, current controller, challenge, and 48h defense window. The project cannot become implementation-ready until the pilot has a concrete place or we explicitly choose to produce only generic templates.

Why this matters: the first park determines track boundaries, recruiting, safety, manual operator burden, and whether the pilot can actually run.

Recommended default: choose a Campinas local park if you want the fastest path to a real manual pilot; choose "generic templates first" only if the exact park is not knowable today.

Unresolved risk if unanswered: the MVP plan can define mechanics, but it cannot create track cards, recruitment instructions, or a real control board.

Target artifact: `projects/body-war/docs/decisions/mvp-readiness.md`

Question: what should be the L0 pilot location: Campinas local park, Sao Paulo neighborhood park, another specific park/city, or generic track-card templates first?

Answer: use `arcanum/development/craft/` as the pilot.

Decision recorded: DG-002 in `projects/body-war/docs/decisions/mvp-readiness.md`.

## Next Question

Context: Craft is not a physical park; it is an internal Arcanum development package. Its README says the recursive-ledger MVP has passed, promotion remains deferred, and the current next move is to continue under the aggregate Refine receipt model. The latest Refine validation is blocked because internal Refine work remains incomplete, with Distill called out as the first remaining blocker.

Why this matters: to use Craft as a pilot, we need one bounded Craft slice. Otherwise "use Craft" is too large and will blur recursive ledger MVP, validation guide, aggregate receipt, and missing-work live test into one mushy pilot.

Recommended default: use the current aggregate Refine receipt / Distill-blocker slice, because it matches this Body War route's need to test Refine, Decision Gate, Interrogation, and Distill before implementation.

Unresolved risk if unanswered: the pilot will be too broad to yield a clear MVP readiness result.

Target artifact: `projects/body-war/docs/decisions/mvp-readiness.md`

Question: which Craft slice should be the pilot for this run: aggregate Refine receipt / Distill blocker, recursive ledger MVP, validation guide, missing-work live test, or another specific Craft artifact?

Answer: aggregate Refine receipt / Distill blocker and recursive ledger MVP.

Decision recorded: DG-003 in `projects/body-war/docs/decisions/mvp-readiness.md`.

## Next Question

Context: Body War's product pilot still needs a controller metric, and the Craft internal pilot needs an equivalent scoring/evaluation rule so the route can say what counts as control, progress, or readiness. The project already offers three product options: fastest verified time, Composite Zone Score, or a hybrid. Craft gives us a useful analogy: a simple public pass/block controller plus richer hidden evidence analysis.

Why this matters: without a scoring authority, the MVP plan cannot decide who controls a track in the Body War pilot, or what evidence promotes the Craft pilot from blocker to ready.

Recommended default: use the hybrid pattern. For Body War, fastest verified time decides public track control in L0 while composite score is recorded in parallel. For Craft, aggregate Refine receipt status is the public readiness controller while recursive-ledger evidence is recorded as the richer substrate.

Unresolved risk if unanswered: the pilot may look complete while hiding whether we optimized for simplicity, fairness, or evidence depth.

Target artifact: `projects/body-war/docs/decisions/mvp-readiness.md`

Question: should the scoring/readiness authority be fastest/simple public controller, composite/richer evidence score, or the hybrid pattern?

Answer: hybrid pattern.

Decision recorded: DG-004 in `projects/body-war/docs/decisions/mvp-readiness.md`.

## Next Question

Context: the selected pilot shape now has two layers. Body War L0 needs a runner evidence channel for manual track-control proof. Craft needs an equivalent artifact/receipt channel for aggregate Refine receipt status plus recursive-ledger evidence. The route can stay lightweight, but it needs a validation channel before planning can be implementation-ready.

Why this matters: validation channel determines whether the next plan is operations-first, no-code workflow, or app/runtime-backed. It also decides how evidence is captured, audited, and recomposed.

Recommended default: use the lightweight/no-code channel. For Body War, use a no-code form or spreadsheet plus Strava link/screenshot, with WhatsApp only for coordination. For Craft, use structured receipt artifacts plus the recursive ledger fixture. This keeps evidence cleaner than WhatsApp-only without jumping to app-backed MVP.

Unresolved risk if unanswered: the pilot may collect evidence that is too messy to audit or too expensive to operate.

Target artifact: `projects/body-war/docs/decisions/mvp-readiness.md`

Question: should the validation channel be WhatsApp/manual screenshots, no-code/structured evidence capture, or app/runtime-backed MVP?

Answer: app/runtime-backed MVP with Strava API link and backend.

Decision recorded: DG-005 in `projects/body-war/docs/decisions/mvp-readiness.md`.

Implementation started: `projects/body-war/app/`.

## Next Question

Context: the validation channel is now app-backed, but monetization is still open. Adding payments, RunCoins, sponsor rewards, or premium hooks now would widen the backend beyond the Strava evidence loop.

Why this matters: monetization can distort the behavior test if runners chase rewards instead of proving whether track control and defense create repeat activity.

Recommended default: defer all monetization for this app-backed L0. Keep the backend focused on Strava linking, activity evidence, track control submissions, and auditability.

Unresolved risk if unanswered: the web app may grow payment/economy scope before validating the core loop.

Target artifact: `projects/body-war/docs/decisions/mvp-readiness.md`

Question: should L0 defer monetization entirely, include XP-only visible progression, or include premium/sponsor/RunCoins hooks?
