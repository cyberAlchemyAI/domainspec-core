# Context Pack - TROQAR Production Login UI

Status: pass
Mode: standard
Task: `SWU-PUI-001` through `SWU-PUI-005`
Source plan: `projects/body-war/development/refinement-runs/20260622T083402Z-troqar-production-ui-login-refine/stages/09-plan.md`

## Obligation Coverage

| ID | Obligation | Controlling Evidence | Status |
| --- | --- | --- | --- |
| O1 | Add anonymous login-first route contract and production selectors. | `UI-SPEC.md`, `TEST-SPEC.md`, `VISUAL-DEFINITIONS.md` | covered |
| O2 | Use Studio profile/guidelines before production acceptance. | `troqar-ui-guidelines.json`, `export-profile.json`, Studio prototype gate docs | covered |
| O3 | Split anonymous and connected states in static HTML/CSS/JS. | `app/static/index.html`, `app/static/app.js`, `app/static/styles.css` | covered |
| O4 | Preserve Strava-only visible MVP login and provider extensibility boundary. | `UI-SPEC.md`, `app/e2e/troqar-product-architecture/ui.spec.ts` | covered |
| O5 | Preserve no-token, public profile, redacted activity, and preview evidence copy. | `UI-SPEC.md`, `TEST-SPEC.md`, `ui.spec.ts` | covered |
| O6 | Add loading, empty, error, callback, reconnect, geometry, status, and submit-error anchors. | `index.html`, `app.js`, `UI-SPEC.md` | covered |
| O7 | Validate with build/check/UI Playwright and whitespace checks. | `package.json`, `playwright.config.ts`, task-session result | covered |
| O8 | Record review receipt and synchronize evidence. | `UI-REVIEW.md`, `RESULT.md`, handoff docs | covered |

## Selected Sources

- `projects/body-war/development/refinement-runs/20260622T083402Z-troqar-production-ui-login-refine/stages/09-plan.md`
  - Defines SWU-PUI-001 through SWU-PUI-005, write scopes, selectors, validation commands, and stop conditions.
- `projects/body-war/docs/features/troqar-product-architecture/UI-SPEC.md`
  - Governs route, component, data-flow, state, accessibility, and privacy obligations.
- `projects/body-war/docs/features/troqar-product-architecture/TEST-SPEC.md`
  - Governs Playwright obligations and selector coverage.
- `projects/body-war/docs/features/troqar-product-architecture/VISUAL-DEFINITIONS.md`
  - Governs TROQAR image-derived palette, logo, typography, composition, and do-not-use constraints.
- `projects/ui-prototyping-studio/development/prototype-gate/troqar-product-architecture/troqar-ui-guidelines.json`
  - Machine-readable Studio constraints for TROQAR variants.
- `projects/body-war/app/static/index.html`
  - Static shell and `data-od-id` anchors.
- `projects/body-war/app/static/app.js`
  - Auth state, safe rendering, API consumption, and UI state transitions.
- `projects/body-war/app/static/styles.css`
  - Dark TROQAR visual system and mobile layout constraints.
- `projects/body-war/app/e2e/troqar-product-architecture/ui.spec.ts`
  - Browser falsification suite.

## Gates

- No blocker-level decision remains for this production UI pass.
- Static HTML/CSS/JS remains the selected implementation route.
- Real Strava secrets are not required because fake Strava is the validation surface.
- Studio handoff is evidence only; it does not promote prototype HTML to production source.

## Validation Surface

```sh
pnpm --dir projects/ui-prototyping-studio/backend run check
pnpm --dir projects/ui-prototyping-studio/backend run test
npm --prefix projects/body-war/app run build
npm --prefix projects/body-war/app run check
npm --prefix projects/body-war/app run test:ui
git diff --check -- projects/body-war projects/ui-prototyping-studio disciplines
```
