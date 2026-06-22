# Stage 06 - Invoke Redefine / Design

Status: pass
Capability handle: `invoke`
Mode: `design`
Receipt kind: parent-native-stage-artifact

## Recommended UI Route

Route: static HTML/CSS/JS production hardening with Studio-gated visual
iteration.

Do not migrate to React/Vite for this step. Do not add a component library yet.
Use the current static app, stronger layout/CSS tokens, explicit state classes,
and Playwright evidence. Add an icon package only after a bundling path exists
or if icons become necessary for usability; for now, text labels are acceptable.

## Information Architecture

### Anonymous First Page

Purpose: convert a new runner into an authenticated Strava-connected session.

Required elements:

- compact topbar with TROQAR / Body War brand;
- primary headline focused on running + territory;
- one primary CTA: `Continue with Strava`;
- short trust line: public profile link only, tokens stay server-side, activity
  summaries are redacted;
- preview card showing what appears after login:
  - runner profile;
  - redacted activity summary;
  - preview evidence;
- setup/error area only when needed:
  - Strava unconfigured;
  - auth error;
  - callback/state failure.

Avoid:

- empty profile/activity/submission panels before login;
- internal words like bearer token, OAuth code, principal id;
- marketing hero that hides the actual app.

### Connected Runner Home

Purpose: let the runner inspect identity/activity data and submit preview
evidence.

Required elements:

- account/status bar: connected runner, public Strava link, logout;
- profile/security row: runner name, session privacy, Strava scope, validation
  caveat;
- activity panel: run-like summaries only, route geometry/scoring caveat;
- pilot track/evidence panel: select track, submit preview, show submission
  result;
- submitted evidence list: preview/hybrid authority, never verified.

### Error And Empty States

| State | UI Behavior |
| --- | --- |
| `strava_unconfigured` | Show setup warning and hide login CTA. |
| `auth_error` | Show retryable login error above CTA. |
| `anonymous` | Show login-first page, not empty dashboard panels. |
| `connected_no_activities` | Keep profile visible; show calm empty activity state. |
| `submit_pending` | Disable the submit button and show progress copy. |
| `submit_failed` | Keep selected activity/track visible and show retry copy. |
| `logout_success` | Return to anonymous login-first page. |

## Studio Live-Edit Workflow

1. Start BodyWar app locally with fake Strava and memory auth.
2. Capture anonymous and connected DOM/HTML baselines from the live page.
3. Register those baselines in UI Prototyping Studio as variants or a session
   baseline.
4. Annotate production selectors:
   - `troqar.shell`
   - `topbar.account.actions`
   - `auth.connect.cta`
   - `profile.safe-athlete-card`
   - `profile.strava-link`
   - `activity.recent-summary`
   - `evidence.submit.cta`
   - new `login.hero`
   - new `login.trust-copy`
   - new `login.preview-card`
   - new `auth.error-message`
5. Synthesize accepted changes and export a Studio handoff.
6. Apply changes to BodyWar source in a Task Session.
7. Validate with BodyWar Playwright and screenshots.

## Package Direction

| Option | Verdict | Reason |
| --- | --- | --- |
| Plain CSS/design-token hardening | selected | Matches current app, fastest path, lowest dependency risk. |
| Add icons later | deferred | Useful, but current static app has no bundling path. |
| Component framework now | rejected for this step | Adds migration work before first UI proof. |

## Visual Direction

- Preserve asphalt shell, fire-orange primary action, territory green status,
  route blue utility, and light neutral surfaces.
- Make the first viewport intentional and action-forward.
- Cards are allowed for repeated preview/activity/evidence items, but page
  sections should not become nested card stacks.
- Maintain 8px or less border radius.
