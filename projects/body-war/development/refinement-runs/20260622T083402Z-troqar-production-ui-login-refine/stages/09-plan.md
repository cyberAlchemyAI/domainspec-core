# Stage 09 - Invoke Plan

Status: pass
Capability handle: `invoke`
Mode: `plan`
Receipt kind: parent-native-stage-artifact

## Non-Executed Implementation Plan

### SWU-PUI-001 - Spec And Selector Contract

Write scope:

- `projects/body-war/docs/features/troqar-product-architecture/UI-SPEC.md`
- `projects/body-war/docs/features/troqar-product-architecture/TEST-SPEC.md`
- `projects/body-war/docs/features/troqar-product-architecture/VISUAL-DEFINITIONS.md`

Tasks:

- Add anonymous login-first route contract.
- Add new selectors:
  - `login.hero`
  - `login.trust-copy`
  - `login.preview-card`
  - `auth.error-message`
- Record Strava-only visible MVP login decision.

Validation:

```sh
git diff --check -- projects/body-war/docs/features/troqar-product-architecture
```

### SWU-PUI-002 - Studio Live Baseline

Write scope:

- `projects/ui-prototyping-studio/development/prototype-gate/troqar-product-architecture/**`
- `projects/body-war/docs/features/troqar-product-architecture/prototype-handoff/**`

Tasks:

- Capture live anonymous and connected BodyWar page baselines.
- Register in Studio.
- Annotate current and new selectors.
- Export accepted handoff with the BodyWar profile.

Validation:

```sh
pnpm --dir projects/ui-prototyping-studio/backend run check
pnpm --dir projects/ui-prototyping-studio/backend run test
```

### SWU-PUI-003 - Production Static UI

Write scope:

- `projects/body-war/app/static/index.html`
- `projects/body-war/app/static/app.js`
- `projects/body-war/app/static/styles.css`

Tasks:

- Split anonymous and connected render states.
- Replace anonymous dashboard panels with login-first entry page.
- Preserve connected operational dashboard after login.
- Add polished loading/error/empty/submit states.
- Preserve no-token and preview-evidence caveats.
- Escape or DOM-build all dynamic track and submission content instead of
  trusting template-string HTML for data returned by APIs.
- Add production-state anchors:
  - `auth.login-first`
  - `auth.callback-status`
  - `auth.error.banner`
  - `auth.reconnect.cta`
  - `profile.privacy-card`
  - `activity.loading`
  - `activity.empty`
  - `activity.error`
  - `track.geometry-status`
  - `evidence.status-chip`
  - `evidence.submission-list`
  - `evidence.submit.error`

Validation:

```sh
npm --prefix projects/body-war/app run build
npm --prefix projects/body-war/app run check
```

### SWU-PUI-004 - Browser Falsification

Write scope:

- `projects/body-war/app/e2e/troqar-product-architecture/ui.spec.ts`
- optional Playwright screenshot output under ignored test artifacts

Tasks:

- Assert anonymous login page:
  - one visible `Continue with Strava` CTA;
  - no empty dashboard panels;
  - no visible `Profile`, `Logout`, activity list, submission list, or evidence
    submit controls before login;
  - trust/privacy copy visible;
  - no raw auth terms.
- Assert Strava-only MVP:
  - no Google/email/password/guest/multiple-provider login.
- Assert callback status:
  - `/?connected=1` shows safe success copy;
  - `/?auth_error=access_denied` shows safe retry copy.
- Assert connected runner home:
  - public Strava link;
  - redacted activity summary;
  - preview submit;
  - logout.
- Assert mobile fit at 390px and 320px for anonymous and connected states.
- Assert no verified/scoring/control overclaim before real verification exists.

Validation:

```sh
npm --prefix projects/body-war/app run test:ui
```

### SWU-PUI-005 - Review Receipt

Write scope:

- `projects/body-war/docs/features/troqar-product-architecture/UI-REVIEW.md`
- work-pack/session receipt path selected by the implementation route

Tasks:

- Record screenshots or Playwright evidence.
- Record package decision.
- Record open residue.

Validation:

```sh
git diff --check -- projects/body-war projects/ui-prototyping-studio
```

## Full Validation Bundle

```sh
pnpm --dir projects/ui-prototyping-studio/backend run check
pnpm --dir projects/ui-prototyping-studio/backend run test
npm --prefix projects/body-war/app run build
npm --prefix projects/body-war/app run check
npm --prefix projects/body-war/app run test:ui
git diff --check -- projects/body-war projects/ui-prototyping-studio
```

## Stop Conditions

- Real Strava secrets are required.
- UI package choice requires network research not approved by the operator.
- Studio cannot register/capture the live page baseline.
- Static app structure becomes too tangled to split anonymous and connected
  states without a framework decision.
