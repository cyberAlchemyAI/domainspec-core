# Work Pack - TROQAR Frontend UX And Tests

Status: `invoke-plan-pass`
Next owner: `task-session`
Recommended first SWU: `SWU-TUI-001`

## Objective

Execute the frontend UX/test hardening path for the current BodyWar static app,
starting from the generated DomainSpec UI architecture, UI spec, test spec, and
Playwright scaffold.

## Write Scope

- `projects/body-war/docs/UI-ARCHITECTURE.md`
- `projects/body-war/docs/features/troqar-product-architecture/UI-SPEC.md`
- `projects/body-war/docs/features/troqar-product-architecture/TEST-SPEC.md`
- `projects/body-war/app/static/**`
- `projects/body-war/app/e2e/troqar-product-architecture/**`
- `projects/body-war/app/package.json`
- `projects/body-war/app/package-lock.json`
- `projects/body-war/app/playwright.config.ts`
- `projects/body-war/app/tsconfig.e2e.json`
- `projects/body-war/app/.gitignore`
- `projects/body-war/development/invoke-runs/20260621T160132Z-troqar-frontend-ui-ux-plan/**`
- `projects/body-war/docs/features/troqar-product-architecture/prototype-handoff/**`

## Constraints

- Runtime application code stays TypeScript or plain browser JavaScript in L0.
- Shell is orchestration only.
- Do not replace the static app with React/Vite in this work-pack.
- Do not add real Strava secrets, VPS deployment, or friend activity evidence.
- Do not hide preview/geometry/verification caveats.
- Do not make a marketing landing page.

## SWU Manifest

| SWU | Goal | Dependencies | Verification |
| --- | --- | --- | --- |
| `SWU-TUI-001` | Validate generated UI docs/scaffold and keep Node E2E build isolated from Playwright spec files. | none | `npm --prefix projects/body-war/app run build:e2e` |
| `SWU-TUI-002` | Add Playwright dependency, config, fake-Strava webServer, and `test:ui` script. | SWU-TUI-001 | `npm --prefix projects/body-war/app run test:ui -- --list` |
| `SWU-TUI-003` | Harden static UI to satisfy UI-SPEC auth/profile/activity/submission/logout states. | SWU-TUI-002 | `npm --prefix projects/body-war/app run check` and `npm --prefix projects/body-war/app run test:ui` |
| `SWU-TUI-004` | Expand Playwright tests for mobile fit, token redaction, CSRF submit, and logout. | SWU-TUI-003 | `npm --prefix projects/body-war/app run test:ui` |
| `SWU-TUI-005` | Produce visual audit report and sync docs with results. | SWU-TUI-004 | `git diff --check -- projects/body-war` and visual audit report with no BLOCK items |
| `BW-TUI-PROT-003` | Consume accepted Studio Prototype Gate handoff in real BodyWar selectors, copy, and browser assertions. | SWU-TUI-002 | `npm --prefix projects/body-war/app run test:ui` |

## Task Details

### SWU-TUI-001 - Generated Artifact Baseline

Write scope:

- generated UI docs and scaffold;
- `tsconfig.e2e.json`;
- `.gitignore`.

Done criteria:

- `docs/UI-ARCHITECTURE.md` exists.
- feature `UI-SPEC.md` and `TEST-SPEC.md` exist.
- Playwright scaffold exists under `app/e2e/troqar-product-architecture/`.
- Existing TypeScript E2E build excludes `.spec.ts` browser tests until Playwright is wired.

### SWU-TUI-002 - Playwright Runtime

Implementation detail:

- Add `@playwright/test` dev dependency.
- Add `playwright.config.ts`.
- Configure webServer to run the built BodyWar app with:
  - `BODY_WAR_STRAVA_FAKE=1`
  - `BODY_WAR_AUTH_BACKEND=memory`
  - local host/port
- Add `test:ui` script.
- Keep browser install instructions separate from tracked secrets.

### SWU-TUI-003 - Static UI Hardening

Implementation detail:

- Ensure each panel has semantic labels and stable selectors where needed.
- Add explicit UI state handling for anonymous, connected, empty activity,
  provider error, submit success, submit error, and logout.
- Preserve current auth/profile/activity API contracts.
- Improve mobile controls if Playwright exposes overlap or unreachable actions.
- Preserve accepted Studio handoff anchors:
  `troqar.shell`, `topbar.account.actions`, `auth.connect.cta`,
  `profile.safe-athlete-card`, `profile.strava-link`,
  `activity.recent-summary`, and `evidence.submit.cta`.

### SWU-TUI-004 - Browser E2E Coverage

Implementation detail:

- Convert scaffolded tests into required tests.
- Add assertions for no token-like strings in DOM.
- Add submission and logout assertions.
- Add mobile viewport screenshot or layout checks.

### SWU-TUI-005 - Visual Audit And Docs Sync

Implementation detail:

- Create `projects/body-war/docs/features/troqar-product-architecture/UI-REVIEW.md`.
- Record copywriting, visuals, color, typography, spacing, and registry safety.
- Sync any accepted changes back to UI-SPEC/TEST-SPEC.

## Validation Bundle

Current generated-artifact validation:

```sh
npm --prefix projects/body-war/app run build
npm --prefix projects/body-war/app run build:e2e
git diff --check -- projects/body-war
```

Post-Playwright validation:

```sh
npm --prefix projects/body-war/app run check
npm --prefix projects/body-war/app run test:ui
git diff --check -- projects/body-war
```

## Residue

- Playwright tests are scaffolded but not executable until `SWU-TUI-002`.
- Full app routing and React/Vite promotion remain deferred.
- Visual audit is planned, not completed, until browser runtime exists.

## Execution Receipts

| Unit | Status | Evidence | Validation |
| --- | --- | --- | --- |
| `SWU-TUI-001` | complete | `projects/body-war/development/task-sessions/20260621T172253Z-swu-tui-001-generated-ui-baseline/SESSION-REPORT.md` | `npm --prefix projects/body-war/app run build:e2e`; `git diff --check -- projects/body-war` |
| `SWU-TUI-002` | complete | `projects/body-war/app/playwright.config.ts`; `projects/body-war/app/package.json` | `npm --prefix projects/body-war/app run test:ui -- --list` |
| `SWU-TUI-003` | complete | `projects/body-war/app/static/index.html`; `projects/body-war/app/static/app.js` | `npm --prefix projects/body-war/app run check`; `npm --prefix projects/body-war/app run test:ui` |
| `SWU-TUI-004` | complete | `projects/body-war/app/e2e/troqar-product-architecture/ui.spec.ts` | `npm --prefix projects/body-war/app run test:ui` |
| `SWU-TUI-005` | complete | `projects/body-war/docs/features/troqar-product-architecture/UI-REVIEW.md` | `git diff --check -- projects/body-war` |
| `BW-TUI-PROT-003` | complete | `projects/body-war/docs/features/troqar-product-architecture/prototype-handoff/STUDIO-PROTOTYPE-HANDOFF.md` | `npm --prefix projects/body-war/app run test:ui` |
