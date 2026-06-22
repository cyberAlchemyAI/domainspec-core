# Codex Goal Profile - Studio Prototype Gate Interface One-Shot

Generated: 2026-06-21
Source work-pack: `projects/ui-prototyping-studio/development/refinement-runs/20260621T172725Z-ui-pipeline-integration/stages/09-invoke-plan.md`
Selected unit: `STUDIO-PROTOTYPE-GATE-INTERFACE-ONE-SHOT`
Readiness: `pass`
Goal budget: `1916/4000 characters; pass`
One-shot mode: `yes`

## Native Goal

```text
/goal Complete STUDIO-PROTOTYPE-GATE-INTERFACE-ONE-SHOT using sidecar projects/ui-prototyping-studio/development/refinement-runs/20260621T172725Z-ui-pipeline-integration/goal-profiles/20260621T-ui-interface-one-shot/GOAL-PROFILE.md and strict handoff pack projects/ui-prototyping-studio/development/refinement-runs/20260621T172725Z-ui-pipeline-integration/stages/01-context-builder.md plus stages/01-context-builder.index.json. Outcome: UI Prototyping Studio has a reusable Prototype Gate interface/contract and handoff convention, TROQAR has a real Studio prototype session/handoff for the online runner profile, and BodyWar static UI/browser tests consume that handoff through the existing UI pipeline. Verification: pnpm --dir projects/ui-prototyping-studio/backend run check; pnpm --dir projects/ui-prototyping-studio/backend run test; pnpm --dir projects/ui-prototyping-studio/backend run test:e2e when backend/preview changes; npm --prefix projects/body-war/app run build; npm --prefix projects/body-war/app run build:e2e; npm --prefix projects/body-war/app run check; add/run npm --prefix projects/body-war/app run test:ui when Playwright UI runtime is wired; git diff --check -- projects/ui-prototyping-studio projects/body-war. Boundaries: write only Studio docs/development/backend as needed, BodyWar docs/features/troqar-product-architecture, BodyWar app, and this goal/run evidence; no auth package, arcanum, validation/poker-team, real deploy, real Strava secrets, friend/private activity, track/scoring. Iterate UPS-GATE-001, UPS-GATE-002 if needed, BW-TUI-PROT-001, BW-TUI-PROT-002, BW-TUI-PROT-003 plus BodyWar SWU-TUI-002..005 only when needed for final interface validation. Stop blocked if canonical spec authority, handoff export semantics, Playwright/runtime dependency, data/privacy, or write-scope decision cannot be resolved from the pack; report blocker, extra sources, and validation state.
```

## Readiness Basis

- The refine result for `ui-prototyping-studio` is `pass`.
- The dispatch route validated with `prototype-gate` selected.
- Stage 01 context coverage is strict `pass`.
- Stage 09 names the ordered work-pack shape and validation surfaces.
- BodyWar `SWU-TUI-001` already established the generated UI artifact baseline.
- No blocker currently prevents a bounded one-shot stream, as long as runtime execution stops for unresolved authority, privacy, or write-scope decisions.

## Handoff Pack

- Markdown: `projects/ui-prototyping-studio/development/refinement-runs/20260621T172725Z-ui-pipeline-integration/stages/01-context-builder.md`
- Index: `projects/ui-prototyping-studio/development/refinement-runs/20260621T172725Z-ui-pipeline-integration/stages/01-context-builder.index.json`
- Evidence index: `projects/ui-prototyping-studio/development/refinement-runs/20260621T172725Z-ui-pipeline-integration/evidence-index.json`
- Source plan: `projects/ui-prototyping-studio/development/refinement-runs/20260621T172725Z-ui-pipeline-integration/stages/09-invoke-plan.md`

## Execution Order

1. `UPS-GATE-001`: write the reusable Studio Prototype Gate integration contract.
2. `UPS-GATE-002`: define or implement a stable handoff export convention only if the current export shape is not sufficient.
3. `BW-TUI-PROT-001`: run the first TROQAR Studio prototype session for the online runner profile and safe Strava connection state.
4. `BW-TUI-PROT-002`: sync BodyWar feature docs/work-pack so the prototype handoff is an optional input to static UI hardening.
5. `BW-TUI-PROT-003`: consume the handoff in BodyWar interface work. Include BodyWar `SWU-TUI-002` through `SWU-TUI-005` only as needed to wire Playwright runtime, harden static UI, expand browser coverage, and produce visual audit evidence.

## Write Scope

Allowed:

- `projects/ui-prototyping-studio/docs/**` if a reusable contract home is created.
- `projects/ui-prototyping-studio/development/**` for prototype-gate docs, run evidence, generated variants, and handoff examples.
- `projects/ui-prototyping-studio/backend/**` only when needed to make the handoff convention or preview interface work and when Studio validation is run.
- `projects/body-war/docs/features/troqar-product-architecture/**`.
- `projects/body-war/docs/UI-ARCHITECTURE.md`.
- `projects/body-war/development/invoke-runs/20260621T160132Z-troqar-frontend-ui-ux-plan/**`.
- `projects/body-war/app/**` for static UI, Playwright runtime, and browser tests.
- This goal profile folder.

Read-only unless a fresh operator instruction widens scope:

- `arcanum/**`
- `implementation/domainspec/**`
- `validation/poker-team/**`
- `projects/auth-user-management/**`
- unrelated project folders and submodule gitlinks

## Capability Policy

Allowed:

- Native Codex execution for the selected one-shot stream.
- Pack-first execution from the refine result, context pack, context index, and source plan.
- `task-session`-style receipt discipline for each SWU.
- `invoke refresh` only to sync BodyWar work-pack/docs with prototype evidence when a named sync gap exists.
- `refine` only to repair or re-scope a named design/plan gap discovered during execution.
- `decision-gate` only for blocker-level authority, privacy, Playwright runtime, or write-scope decisions.
- `craft` only if the scoped project ledger must record a durable blocker, decision, gap, or next move.

Not allowed without fresh operator approval:

- Subagents.
- Real VPS deploy, DNS, or public origin changes.
- Real Strava callback settings, client secrets, access tokens, or refresh tokens.
- Friend consent/private activity evidence handling.
- Track, route geometry, scoring, rewards, or game-loop implementation.
- Public `arcanum` mutation.
- Mutating `validation/poker-team` or `implementation/domainspec`.

## Verification Surface

Studio checks:

```sh
pnpm --dir projects/ui-prototyping-studio/backend run check
pnpm --dir projects/ui-prototyping-studio/backend run test
pnpm --dir projects/ui-prototyping-studio/backend run test:e2e
```

BodyWar checks:

```sh
npm --prefix projects/body-war/app run build
npm --prefix projects/body-war/app run build:e2e
npm --prefix projects/body-war/app run check
npm --prefix projects/body-war/app run test:ui
```

Repository hygiene:

```sh
git diff --check -- projects/ui-prototyping-studio projects/body-war
```

Validation notes:

- `test:e2e` is required when Studio backend, preview, or handoff behavior changes.
- `test:ui` may need to be added by the BodyWar Playwright runtime slice before it can be run.
- If a validation command cannot run because a prerequisite is missing, repair it inside the selected write scope or report blocked.

## Invariants

- Studio is a prototype gate, not the canonical UI pipeline.
- `UI-SPEC.md` and `TEST-SPEC.md` remain source inputs unless explicitly refreshed.
- Studio handoff export is evidence, not automatic source mutation.
- Accepted prototype output must map components to stable `data-od-id` where possible and flag fallback selectors.
- BodyWar source implementation must be validated in the target app, not only in Studio preview.
- No tracked real secrets, tokens, OAuth codes, client secrets, refresh tokens, private athlete data, or friend activity payloads.
- TypeScript remains the application language; shell is acceptable for scripts.
- SQL work remains Drizzle/Postgres by default if SQL is touched, but this interface stream should not widen into schema/auth work unless a named BodyWar validation dependency requires it.

## Fallback Exploration

Fallback exploration is limited to named gaps from the pack:

- handoff export path or schema convention;
- Studio preview or CLI behavior needed to prove the gate;
- BodyWar Playwright runtime wiring needed for UI validation;
- `data-od-id` mapping from UI concepts to prototype HTML;
- BodyWar static UI conformance to the UI-SPEC.

Any extra source used outside the handoff pack, evidence index, source plan, and listed work-pack references must be named in the final report with the gap that justified it and whether it changed the result.

## Stop Condition

Stop and report `blocked` if execution requires:

- deciding canonical UI spec authority beyond the selected prototype gate;
- changing handoff export semantics in a way the current Studio architecture cannot justify;
- real deploy/VPS/DNS/public-origin access;
- real Strava secrets or callback configuration;
- friend consent/private activity evidence;
- track/game/scoring work;
- mutation outside the write scope;
- a Playwright/runtime decision that cannot be resolved locally;
- committing any secret, token, OAuth code, or private payload.

## Audit

- Decision profile: none.
- One-shot mode: yes.
- Strict coverage: pass.
- Fallback exploration: named gaps only.
- Extra-source reporting: required.
- Subagent authorization: none.
