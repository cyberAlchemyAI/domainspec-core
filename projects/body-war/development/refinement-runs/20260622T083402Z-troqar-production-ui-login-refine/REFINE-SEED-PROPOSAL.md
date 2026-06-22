# Refine Seed Proposal

## Target

`projects/body-war/app` and
`projects/body-war/docs/features/troqar-product-architecture`

## Operator Intent

Make the TROQAR first page and login experience production ready while using
the UI Prototyping Studio live loop to edit and validate the page. The current
VS Code local browser view shows a functional but internal-looking surface.

## Desired Outcome

An implementation-ready, non-executed plan that defines:

- a production-quality anonymous first screen;
- a Strava-only MVP login decision with future provider extensibility;
- the connected runner profile/home screen after login;
- Studio live-edit workflow for the real BodyWar page;
- package/theme choices that fit TROQAR without overbuilding the current static
  app;
- browser test obligations for anonymous, fake-Strava login, connected, mobile,
  error, and token-redaction states.

## Source Context

- `projects/body-war/app/static/index.html`
- `projects/body-war/app/static/app.js`
- `projects/body-war/app/static/styles.css`
- `projects/body-war/app/e2e/troqar-product-architecture/ui.spec.ts`
- `projects/body-war/docs/features/troqar-product-architecture/UI-SPEC.md`
- `projects/body-war/docs/features/troqar-product-architecture/VISUAL-DEFINITIONS.md`
- `projects/body-war/docs/features/troqar-product-architecture/prototype-handoff/STUDIO-PROTOTYPE-HANDOFF.md`
- `projects/ui-prototyping-studio/docs/PROTOTYPE-GATE.md`
- `projects/ui-prototyping-studio/docs/HANDOFF-CONVENTION.md`
- `projects/ui-prototyping-studio/development/prototype-gate/troqar-product-architecture/run/studio.json`

## Current Findings

- The current UI is working but reads like a plain internal admin/control page.
- Anonymous pre-login state should be a real app entry screen, not a sparse
  dashboard with empty panels.
- For MVP, Strava should be the only login method because TROQAR's value starts
  from running identity and activity permissions.
- Auth architecture should remain provider-ready internally: the public UI shows
  only Strava, but backend abstractions should not forbid future providers.
- BodyWar is currently plain static HTML/CSS/JS, with Playwright installed for
  browser tests. No frontend component library is selected yet.
- UI Prototyping Studio can already generate and export a handoff, but this run
  should refine how to use Studio for live editing against the local page rather
  than only detached HTML variants.

## Write Scope For Future Execution

- BodyWar app static frontend:
  - `projects/body-war/app/static/index.html`
  - `projects/body-war/app/static/app.js`
  - `projects/body-war/app/static/styles.css`
- BodyWar UI/browser tests:
  - `projects/body-war/app/e2e/troqar-product-architecture/ui.spec.ts`
  - optional focused Playwright screenshots or snapshot fixtures
- TROQAR feature docs:
  - `projects/body-war/docs/features/troqar-product-architecture/UI-SPEC.md`
  - `projects/body-war/docs/features/troqar-product-architecture/TEST-SPEC.md`
  - `projects/body-war/docs/features/troqar-product-architecture/VISUAL-DEFINITIONS.md`
  - `projects/body-war/docs/features/troqar-product-architecture/UI-REVIEW.md`
  - `projects/body-war/docs/features/troqar-product-architecture/prototype-handoff/**`
- UI Prototyping Studio integration docs/development artifacts only if needed.

## Out Of Scope

- Real Strava production app registration or secrets.
- Additional login providers in the MVP UI.
- Track/gameplay/scoring/map production work.
- VPS deploy changes.
- Auth package rewrites.
- React/Vite migration unless the refine result proves it is required for this
  specific production-readiness step.

## Decision Questions

1. Should the MVP expose only `Continue with Strava`?
   - Recommended: yes, because the product's first proof is runner identity and
     redacted activity summaries.
   - Preserve future provider extensibility in backend/domain docs.
2. Should we keep static HTML/CSS/JS for this production polish pass?
   - Recommended: yes, unless Studio/package comparison identifies a concrete
     component need that plain CSS cannot satisfy.
3. Which UI package/theme help is allowed?
   - Recommended now: no framework migration; add a lightweight icon package
     only if the app build can support it cleanly, otherwise use accessible text
     and CSS tokens.
   - Candidate next packages for comparison: lucide icons if a bundling path is
     added; plain CSS design tokens; possible future Lit/Web Components or Vite
     only if repeated interactive components become expensive.
4. How should Studio edit the page live?
   - Recommended: register the live local page HTML as a Studio baseline,
     annotate the production selectors, export a handoff, then apply the accepted
     changes to BodyWar source with Playwright validation.

## Done Criteria For The Refine Run

- A final plan defines the anonymous login page, connected home/profile state,
  and error states.
- The plan answers the Strava-only MVP login question.
- The plan selects a UI implementation route and rejects at least two
  alternatives with reasons.
- The plan defines how UI Prototyping Studio is used for live page iteration.
- The plan lists exact app/doc/test mutations for a later Task Session.
- The plan includes validation commands:
  - `npm --prefix projects/body-war/app run build`
  - `npm --prefix projects/body-war/app run check`
  - `npm --prefix projects/body-war/app run test:ui`
  - `git diff --check -- projects/body-war projects/ui-prototyping-studio`

## Preset And Research

- Preset: `standard`
- Research: `research-if-gap-appears`
- External research: not authorized in this seed; use local evidence first.

## Planned Stage Configuration

Canonical ten-stage Refine loop:

1. Context Builder evidence baseline.
2. Invoke Define.
3. Interrogation `refine-review`.
4. Research decision.
5. Distill.
6. Invoke Redefine / Design.
7. Interrogation `refine-design-review`.
8. Distill Repair.
9. Invoke Plan.
10. Final Interrogation and Refine-owned synthesis.

## Confirmation State

This packet is a strategy proposal. Do not execute runtime-backed stages,
subagents, or UI mutations until the operator confirms.
