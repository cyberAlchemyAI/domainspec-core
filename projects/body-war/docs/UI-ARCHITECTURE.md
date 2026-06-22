---
project: body-war
product-name: TROQAR
status: draft-pass
framework: static-node-l0
ui-framework: vanilla-js-l0
styling: plain-css
created: 2026-06-21
updated: 2026-06-21
source: domainspec-ui-pipeline
---

# Frontend Architecture Constitution

> Governing document for BodyWar/TROQAR frontend decisions.
> Feature UI contracts must conform to these conventions.

## Stack

| Layer | L0 Choice | Promotion Path | Notes |
| --- | --- | --- | --- |
| Delivery | TypeScript Node static server | Vite when app complexity needs routing/build tooling | Current app serves `static/index.html`, `static/app.js`, and `static/styles.css`. |
| UI framework | Vanilla browser JavaScript | React only through an explicit work-pack | Do not introduce framework state without route/component plan. |
| Styling | Plain CSS custom properties | Design tokens before component library | TROQAR palette comes from feature visual definitions. |
| Icons | Text labels in L0 | Lucide icons after React/Vite adoption | Avoid bespoke SVG icon systems in L0. |
| Data fetching | Fetch API | Typed client hooks after frontend module split | Same-origin `/api/*`; no CORS dependency in L0. |
| Forms | Native controls | Typed form helpers after component split | CSRF header comes from `bw_csrf` cookie for unsafe methods. |
| E2E | Node integration tests plus Playwright scaffold | Playwright runtime after browser dependency install | Browser tests must prove UI redaction and responsive flows. |

## Product UX Principles

1. First screen is the working app, not a landing page.
2. A runner should immediately see connection state, profile state, activity state, and evidence action.
3. Preview, geometry, and verification caveats must stay visible when relevant.
4. Strava/provider tokens, token expiry internals, OAuth codes, and raw private activity payloads are never rendered.
5. Mobile and desktop must preserve the connect -> profile -> activity -> submit path without hidden required controls.

## Visual System

| Token | Role | Usage |
| --- | --- | --- |
| `--bg` / `sand-light` | calm app background | page body and empty states |
| `--ink` / `asphalt-ink` | primary text and app shell | headers, labels, dense data |
| `--accent` / `fire-orange` | primary action and contested energy | connect, submit, urgent actions |
| `--green` / `territory-green` | connected, controlled, verified-like success | provider connected, accepted states |
| `--blue` / `route-blue` | route and neutral utility | links, route metadata, track cards |
| `--line` | boundaries | panels, repeated items, form controls |

Typography uses system UI in L0. Future display/body brand fonts are allowed
only when they do not block data scanning or mobile fit.

## Layout Contract

```text
-----------------------------------------------------+
| Topbar: product, page title, profile/connect/logout |
+-----------------------------------------------------+
| Connection status + safe athlete summary            |
+------------------------------+----------------------+
| Profile cards                | Activity import      |
| Pilot tracks                 | Submitted evidence   |
+------------------------------+----------------------+
```

Mobile contract:

- topbar actions stack without overlap;
- activity rows collapse to one column;
- profile cards collapse to one column;
- submit controls remain adjacent to selected track;
- no text should overflow cards or buttons.

## Route Model

Current L0 uses static fallback routing: `/`, `/profile`, and other non-API
paths serve the same app shell. Feature-specific UI specs may name future
routes, but implementation tasks must distinguish existing L0 surfaces from
deferred routed pages.

## Data And Auth Contract

| UI Concern | Source |
| --- | --- |
| Connection status | `GET /api/status` |
| Runner profile | `GET /api/profile` |
| Activity summaries | `GET /api/activities` |
| Tracks | `GET /api/tracks` |
| Submission list | `GET /api/submissions` |
| Evidence submit | `POST /api/submissions` with `X-CSRF-Token` |
| Logout | `POST /api/auth/logout` with `X-CSRF-Token` |

Unsafe requests must include the CSRF token from the `bw_csrf` cookie. Browser
UI must never read, display, or infer provider access/refresh token values.

## Component Organization

L0 static files:

```text
app/static/
  index.html
  app.js
  styles.css
```

Future component split:

```text
app/src/ui/
  components/
  hooks/
  pages/
  query-keys.ts
```

Do not create the future tree until a work-pack explicitly promotes beyond L0.

## Accessibility Requirements

- Use semantic headings in visual order.
- Use semantic `nav` for account actions.
- All buttons and links must have visible text labels.
- Status changes must have text, not color-only meaning.
- Activity submit controls must be keyboard reachable.
- External Strava profile links use `rel="noreferrer"` and visible link text.

## Test Requirements

Browser E2E must cover:

- anonymous status and connect CTA;
- fake-Strava login redirect to connected state;
- safe Strava profile link;
- profile redaction with no token-like text;
- activity list redaction and geometry caveat;
- evidence submission through UI with CSRF;
- logout clears authenticated UI state;
- mobile viewport no critical control overlap.

## Do Not

- Do not replace the app with a marketing hero or explainer page.
- Do not hide route geometry caveats.
- Do not show `verified` for preview-accepted evidence.
- Do not introduce a frontend framework without updating this constitution and
  the work-pack validation surface.
- Do not add dark mode, decorative background blobs, or one-hue-only styling in
  L0.
