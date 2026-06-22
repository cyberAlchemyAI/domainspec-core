# Implementation Layering - TROQAR Frontend UX

Status: `invoke-plan-pass`
Generated: `20260621T160132Z`

## Layer Thesis

Do not jump from the current static app to a full game UI. Prove the online
runner profile loop in the browser first, then harden, then promote routing or
framework structure only when the L0 evidence path is stable.

## Layers

| Layer | Question | Scope | Exit Evidence |
| --- | --- | --- | --- |
| L0 - Spec And Browser Test Scaffold | Can the existing static app be governed by a UI contract and test obligations? | UI architecture, UI-SPEC, TEST-SPEC, Playwright scaffold. | Docs exist; build still passes; scaffold is isolated from Node E2E. |
| L1 - Playwright Runtime Wiring | Can browser tests run repeatably against fake-Strava local server? | Install/configure Playwright, webServer, test script, fake env. | `npm --prefix projects/body-war/app run test:ui` passes locally. |
| L2 - Static UI Hardening | Does the UI meet the contract across auth/profile/activity/submit/logout/mobile? | Improve DOM semantics, status rendering, error states, mobile fit, no-overlap details. | Playwright tests plus `npm run check` pass; visual audit has no blockers. |
| L3 - Route/Framework Promotion | Is the UI complex enough to justify Vite/React/routes? | Optional framework migration plan and component split. | Separate decision/work-pack with migration proof and no regression in L2 tests. |

## Deferred Scope

- app-wide game pages beyond the online profile/evidence flow;
- real route geometry and maps;
- operator console;
- sponsor/store/economy UI;
- production deploy/browser smoke on VPS.

## Promotion Rules

- L1 cannot start until the generated UI docs and scaffold validate by build
  isolation.
- L2 cannot claim done until Playwright is executable.
- L3 cannot start without an explicit framework promotion decision.
