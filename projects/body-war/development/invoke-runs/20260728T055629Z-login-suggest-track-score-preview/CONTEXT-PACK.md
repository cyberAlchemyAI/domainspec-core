---
module: body-war-login-suggest-track-score-preview
version: current
status: authored
updatedAt: 2026-07-28
docType: invoke-context-pack
contextMode: standard
runtimeHandoff: false
---

# Context Pack

## Task

Map a bounded Body War journey from anonymous login through Strava connection,
SuggestedTrack creation or selection, explicit runner confirmation, candidate
geometry derivation from the selected activity, score-preview calculation, and
web projection.

This pack supports Invoke Define, Design, and Plan authoring. It is not an
implementation authorization or a Task Session runtime handoff.

## Obligation Matrix

| ID | Obligation | Selected evidence | Status |
| --- | --- | --- | --- |
| O1 | Preserve the Body War SuggestedTrack lifecycle and its owner ceiling. | `.craft/ledger.yml`; feature `domain.md`, `states.md`, `operations.md` | covered |
| O2 | Reuse the current login, activity-summary, suggestion, and evidence surfaces. | `app/server.ts`; `app/src/auth/types.ts`; feature interfaces and queries | covered |
| O3 | Make the real-versus-fake Strava boundary explicit. | current gap research; `strava-oauth.ts`; official Strava API reference | covered |
| O4 | Treat route geometry as private candidate evidence until a separate promotion. | feature contract and current redaction receipts | covered |
| O5 | Produce a numeric score only from a versioned, ratified policy and disclose its basis. | game-rules draft; score-authority refinement; product architecture | covered with decision gate |
| O6 | Map business meaning, system realization, bridge evidence, drift, and ownership separately. | ontology-vault contract; immutable historical BWOI CT-2 proof-track boundary with exact selector/digest | covered as historical context only |
| O7 | Produce a layered prototype route that supports usability testing without inflating it into real-provider or release evidence. | current prototype-gap findings; Invoke Plan contract | covered |

## Selected Context

| Source | Selectors | Obligations |
| --- | --- | --- |
| `projects/body-war/.craft/ledger.yml` | `CTX-BODY-WAR-SUGGESTED-TRACKS`; active blockers and gaps | O1, O7 |
| `projects/body-war/development/research/20260727-suggested-track-testable-prototype-gap/findings.md` | outcome; exact boundary; LP-01, RF-02, HOST-01 | O2, O3, O7 |
| `projects/body-war/docs/features/parque-taquaral-online-mvp/domain.md` | `SuggestedTrack`; `ActivityEvidenceCandidate`; statuses | O1, O4 |
| `projects/body-war/docs/features/parque-taquaral-online-mvp/states.md` | track and evidence lifecycles | O1, O4 |
| `projects/body-war/docs/features/parque-taquaral-online-mvp/operations.md` | create and consented evidence attachment | O1, O2, O4 |
| `projects/body-war/docs/features/parque-taquaral-online-mvp/interfaces.md` | HTTP and repository boundaries | O2 |
| `projects/body-war/docs/features/parque-taquaral-online-mvp/ui-spec.md` | login visibility, Help, responsive and claim-copy rules | O2, O7 |
| `projects/body-war/app/src/auth/types.ts` | current activity and SuggestedTrack types | O2, O3 |
| `projects/body-war/app/src/auth/strava-oauth.ts` | OAuth scopes and synthetic activity boundary | O2, O3 |
| `projects/body-war/app/server.ts` | public authority labels and current endpoints | O2, O4 |
| `projects/body-war/docs/features/game-rules/SPEC.md` | composite-score weights, 14-day cycle, unresolved authority | O5 |
| `projects/body-war/development/refinement-runs/20260629-troqar-score-authority/RESULT.md` | sealed zone-control candidate and unresolved metric decisions | O5 |
| `projects/body-war/development/invoke-runs/20260727T172835Z-suggested-track-ontology-domainspec-integration/SPEC.md` | ontology/DomainSpec separation and prior experimental ceiling | O6 |
| Strava official API reference and authentication documentation, retrieved 2026-07-28 | activity list/detail/streams; `activity:read` and `activity:read_all` visibility | O3, O4 |

## External Contract Snapshot

- `GET /athlete/activities` lists athlete activities with `activity:read`;
  Only Me activities require `activity:read_all`.
- `GET /activities/{id}` returns the authenticated athlete's detailed activity
  under the same visibility distinction.
- `GET /activities/{id}/streams` can return `latlng`, `distance`, `time`, and
  related streams; `activity:read_all` is required for Only Me activities.
- This run recommends keeping the current least-privilege
  `read,activity:read` scope for the first prototype. Private activities are
  excluded until the owner explicitly selects a broader consent scope.
- Source:
  `https://developers.strava.com/docs/reference/` and
  `https://developers.strava.com/docs/authentication/`.

## Excluded Context

- Private token values, provider payloads, and files under `app/data/`.
- City-wide hex-zone geometry, anti-cheat, clans, economy, and production
  territory control.
- CyberAlchemy ontology promotion and DomainSpec v2 release admission.
- Public map publication, official-route claims, and source-backed promotion.
- Host/operator secrets and deployment execution.

## Context Builder Result

- Mode: standard
- Selected local files: 13
- External contract pages: 2
- Obligation coverage: 100%
- Strict selector coverage: pass
- Runtime handoff: none
- Authoring blockers: none
- Implementation blockers carried forward: score normalization decision, real
  token read/refresh gateway, geometry privacy/consent policy, hosted admission
