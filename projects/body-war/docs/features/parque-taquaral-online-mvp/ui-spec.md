# UI Spec: SuggestedTrack Route Expansion

## Connected Runner Surface

The connected home page shows a SuggestedTrack section after profile and before
the recent activity list.

| UI Element | Requirement |
| --- | --- |
| Suggested track list | Shows name, place, status chip, geometry authority, distance hint, and note. |
| Create suggestion form | Requires route name, place, and city; optional distance and note. |
| Help action | Lets the runner pick one recent Strava activity and attach it with consent. |
| Evidence summary | Shows submitted candidate count and the current runner's attached candidates. |

## Copy Rules

| Context | Required Copy Posture |
| --- | --- |
| `needs_evidence` | Portuguese copy should say `Precisa de evidencia`. |
| `evidence_submitted` | Portuguese copy should say `Evidencia enviada`. |
| `operator_review` | Portuguese copy should say `Em analise`. |
| Geometry | Say geometry/source backing is still pending. |
| Evidence attach | State that only a redacted summary is stored after consent. |

## Interaction Rules

1. Anonymous users see the login page only.
2. Connected runners can list suggestions.
3. SuggestedTrack creation uses the existing CSRF cookie/header path.
4. Evidence attach uses the live activity summaries already loaded from Strava.
5. The UI must not include `verified scoring`, `verified control`, `pilot ready`,
   provider tokens, or raw OAuth terms.

## Responsive Rules

Critical controls must remain inside the viewport at 320px and 390px widths:
topbar actions, create form controls, help buttons, and activity submit buttons.
