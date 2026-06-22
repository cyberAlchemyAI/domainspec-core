# Stage 02 - Invoke Define

Status: pass
Capability handle: `invoke`
Mode: `define`
Receipt kind: parent-native-stage-artifact

## Definition

TROQAR needs a production-quality first-page and login experience for the
current BodyWar static app. The current implementation proves backend/session
integration, fake-Strava login, safe profile rendering, activity import, and
preview evidence submission, but the anonymous screen still presents empty
dashboard panels and internal validation language.

The refined product surface should split the UI into two intentional states:

1. Anonymous entry: a focused product/app entry screen with one primary login
   method, `Continue with Strava`.
2. Connected runner home: a dense but polished operational view showing runner
   identity, public Strava link, redacted activity summaries, pilot track
   selection, preview evidence submission, and visible caveats.

## MVP Login Decision

Visible MVP login method: Strava only.

Reason:

- TROQAR's first value depends on runner identity and activity summaries.
- Extra login providers create account-linking complexity before the product
  has proven the runner loop.
- Strava-only login keeps the first page honest: "connect the running data
  source that powers the app."

Constraint:

- Backend/domain abstractions should remain provider-extensible.
- UI copy must not imply Strava tokens or private route data render client-side.

## Production Readiness Meaning

Production-ready means:

- no raw backend errors in user-facing copy;
- clear anonymous, loading, connected, disconnected, error, empty, submit
  success, submit failure, and logout states;
- mobile layout at 390px without overlap or horizontal scroll;
- visible privacy and preview-evidence caveats;
- branded visual hierarchy using TROQAR visual definitions;
- browser tests prove the critical states and no-token contract;
- Studio handoff anchors stay stable.

## Non-Goals

- No real Strava secrets.
- No new providers in MVP UI.
- No full gameplay/map/scoring route.
- No React/Vite migration unless the design plan proves static UI is the wrong
  surface for this step.
