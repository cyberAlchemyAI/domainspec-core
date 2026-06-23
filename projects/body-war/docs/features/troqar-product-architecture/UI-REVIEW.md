# TROQAR Production Login UI Review

Status: pass
Date: 2026-06-22
Task session: `projects/body-war/development/task-sessions/20260622T125002Z-production-ui-login/`

## Evidence

| Evidence | Result |
| --- | --- |
| Studio visual discipline | `disciplines/cards/troqar-ui-visual-discipline.md` and `troqar-ui-guidelines.json` are referenced by the export profile. |
| Browser runner | `npm --prefix projects/body-war/app run test:ui` passed 7 Playwright tests. |
| Anonymous login | One visible `Entrar com Strava` CTA; no profile, logout, activity, submission, or evidence submit controls before login. |
| Callback states | `?connected=1` and `?auth_error=access_denied` render safe success/retry copy. |
| Connected profile | Public Strava profile link, server-side token custody copy, redacted activity summary, and preview submit are visible. |
| Mobile fit | 390px and 320px viewport assertions passed for topbar actions, connect CTA, profile card, activity panel, and preview submit CTA. |
| Screenshot artifacts | Ignored Playwright outputs: `projects/body-war/app/test-results/troqar-anonymous-login.png`, `projects/body-war/app/test-results/troqar-connected-runner.png`. |

## Visual Audit

| Surface | Result | Notes |
| --- | --- | --- |
| Login-first shell | pass | Anonymous first viewport uses dark asphalt TROQAR shell and Strava-only action. |
| Topbar | pass | TROQAR mark/wordmark remain visible and account actions fit 390px/320px widths. |
| Profile | pass | Connected profile keeps public Strava link and explicit server-side credential custody copy. |
| Activity | pass | Activity summary panel preserves redaction and no-geometry-proof language. |
| Track cards | pass | Geometry placeholder status is visible and distinct from verified state. |
| Evidence CTA | pass | Submit action says `Enviar preview`; status chips are preview/enviado, not verified. |
| Mobile | pass | Critical elements have measurable boxes within 390px and 320px viewport widths. |

## Open Residue

- Full map/track gameplay remains deferred.
- Real Strava credentials and friend activity evidence remain outside this UI gate.
- Parque Taquaral sourced geometry remains a product gap, not a UI blocker.
