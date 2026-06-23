# TROQAR Studio Prototype Handoff

Status: accepted prototype gate
Session: `ups-session-0001`
Accepted revision: `rev-0001`
Baseline: variant `B`

## Sources

| Artifact | Path |
| --- | --- |
| Prototype gate contract | `projects/ui-prototyping-studio/docs/PROTOTYPE-GATE.md` |
| Handoff convention | `projects/ui-prototyping-studio/docs/HANDOFF-CONVENTION.md` |
| Export profile | `projects/ui-prototyping-studio/development/prototype-gate/troqar-product-architecture/export-profile.json` |
| Studio visual guidelines | `projects/ui-prototyping-studio/development/prototype-gate/troqar-product-architecture/troqar-ui-guidelines.json` |
| Studio run store | `projects/ui-prototyping-studio/development/prototype-gate/troqar-product-architecture/run/studio.json` |
| Accepted prototype | `projects/ui-prototyping-studio/development/prototype-gate/troqar-product-architecture/run/artifacts/committed/33fa5f2100c3cdf5338b751d004f56027484f6338a7482cf0c04300d65a4d94f.html` |
| Bundle mirror | `projects/body-war/docs/features/troqar-product-architecture/prototype-handoff/HANDOFF-BUNDLE.json` |
| Production login bundle | `projects/body-war/docs/features/troqar-product-architecture/prototype-handoff/PRODUCTION-LOGIN-HANDOFF-BUNDLE.json` |

## Handoff Bundle

- Export profile: `troqar-product-architecture`
- Candidate HTML hash: `33fa5f2100c3cdf5338b751d004f56027484f6338a7482cf0c04300d65a4d94f`
- Missing refs: none
- Story refs: `SPEC.md`, `ONLINE-AUTH-PROFILE-INFRA.md`
- Requirement refs: `UI-SPEC.md#page-layout-and-profile`, `UI-SPEC.md#security-and-privacy-requirements`
- Acceptance refs: `TEST-SPEC.md#browser-e2e-obligations`

## Accepted Prototype Tasks

| Task | `data-od-id` | Accepted Change |
| --- | --- | --- |
| `task-3ca09cd843` | `profile.safe-athlete-card` | Make token privacy explicit in the connected profile card. |
| `task-25c077d10f` | `profile.strava-link` | Copy says public Strava profile so the link is display data, not auth data. |
| `task-92dd181c6d` | `activity.recent-summary` | Activity summaries are redacted and route geometry is outside this proof. |
| `task-94816fde47` | `evidence.submit.cta` | CTA says preview evidence and avoids verified scoring language. |

## Production Selector Contract

| `data-od-id` | BodyWar Surface | Browser Assertion |
| --- | --- | --- |
| `troqar.shell` | Main online runner profile shell | Shell is visible on first load. |
| `topbar.account.actions` | Account navigation | Profile/connect/logout actions fit mobile width. |
| `auth.connect.cta` | Connect Strava CTA | Anonymous runner can start fake-Strava login. |
| `profile.safe-athlete-card` | Connected profile panel | Token privacy copy is visible. |
| `profile.strava-link` | Public athlete link | Link text is `Open public Strava profile`. |
| `activity.recent-summary` | Recent activity panel | Redaction and no-geometry-proof copy is visible. |
| `evidence.submit.cta` | Activity submission CTA | Button submits preview evidence only. |

## Downstream Consumption

BodyWar consumes this handoff in:

- `projects/body-war/app/static/index.html`
- `projects/body-war/app/static/app.js`
- `projects/body-war/app/e2e/troqar-product-architecture/ui.spec.ts`
- `projects/body-war/docs/features/troqar-product-architecture/UI-SPEC.md`
- `projects/body-war/docs/features/troqar-product-architecture/TEST-SPEC.md`

The handoff does not promote Studio HTML into production. It promotes the
reviewed selector and copy obligations into the real app and browser tests.

## Production Login Handoff

Status: accepted task-session evidence
Session data: `projects/body-war/development/task-sessions/20260622T125002Z-production-ui-login/studio/studio.json`
Accepted revision: `rev-0001`
Baseline: variant `B`
Accepted prototype: `projects/body-war/development/task-sessions/20260622T125002Z-production-ui-login/studio/artifacts/committed/94bfb30acfacb8d3fa853fba8a0c0a8db15893a81fb9f7c2fb1ae1ede1ab8a96.html`

The production login handoff consumes the Studio visual guideline file and adds
the login-first selectors required by the production static UI:

| `data-od-id` | Production Surface |
| --- | --- |
| `auth.login-first` | Anonymous login-first page. |
| `login.hero` | First-viewport TROQAR page identity. |
| `login.trust-copy` | Privacy and preview-evidence copy. |
| `login.preview-card` | Dark mobile-app preview card. |
| `auth.callback-status` | Safe Strava callback success copy. |
| `auth.error.banner` | Safe provider retry copy. |
| `auth.reconnect.cta` | Retry Strava CTA. |
| `profile.privacy-card` | Server-side credential custody copy. |
| `activity.loading` | Activity loading state. |
| `activity.empty` | Empty recent-run state. |
| `activity.error` | Safe activity error copy. |
| `track.geometry-status` | Placeholder/preview geometry status. |
| `evidence.status-chip` | Preview/submitted evidence status. |
| `evidence.submission-list` | Submitted preview evidence list. |
| `evidence.submit.error` | Safe submission error copy. |
