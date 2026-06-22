# Backend Spec

Status: `draft-pass`

## Backend Boundary

The backend is a TypeScript application boundary inside `projects/body-war/app`
or a later Body War-owned package. Domain and application modules stay
framework-agnostic. Interface and infrastructure modules adapt HTTP, storage,
provider APIs, and deployment.

## Module Layout

```text
src/
  modules/
    identity/
      domain/
      application/
      interface/
    activity/
    territory/
    evidence/
    control/
    progression/
    community/
    operator/
  shared/
    result.ts
    clock.ts
    ids.ts
```

## Dependency Rules

| From | May Import | Must Not Import |
| --- | --- | --- |
| Domain | shared primitives | HTTP, storage, provider SDKs, UI |
| Application | domain, ports, shared | concrete adapters, DOM |
| Infrastructure | application ports, provider SDKs, storage clients | UI components |
| Interface | application use cases, auth guard | domain mutation shortcuts |
| UI | HTTP client/query hooks | server secrets, provider SDKs |

## Storage Areas

| Store | Records | Notes |
| --- | --- | --- |
| Auth store | principals, sessions, roles, permissions | Owned by `@domainspec/auth-user-management` migrations/repositories. |
| Body War identity store | OAuth state, provider accounts, provider tokens, runner profiles | Owned by Body War Drizzle schema and adapters. |
| Territory store | tracks, zones, geometry status, source refs | Geometry source status is explicit. |
| Evidence store | submissions, audit trail, review decisions | No raw private provider payload. |
| Controller projection | current controller per territory | Rebuildable from accepted/verified evidence. |
| Progression ledger | XP, badges, league, season snapshots | Append-only. |
| Notification store | inbox and delivery status | No private payload. |

## API Layer Responsibilities

- Authenticate and authorize every protected operation.
- Validate CSRF on unsafe browser requests.
- Parse request payloads into application inputs.
- Return stable error codes from `interfaces.md`.
- Keep provider tokens and secrets out of logs and response payloads.

## Application Services

| Service | Owns |
| --- | --- |
| `AuthFacade` | Adapts auth-user-management core use cases to Body War browser/session permissions. |
| `ActivityImportService` | Lists and filters provider activity summaries. |
| `TerritoryCatalogService` | Reads/publishes track and geometry metadata. |
| `EvidenceSubmissionService` | Submits and transitions evidence status. |
| `ControllerService` | Computes controller read models. |
| `ProgressionService` | Calculates XP, badges, and ranking effects. |
| `ChallengeService` | Enrollment, progress, completion. |
| `ClanService` | Membership and contribution. |
| `OperatorReviewService` | Review queue and verification decisions. |

## Security Requirements

- Session cookies are HttpOnly and signed.
- CSRF binding is required for unsafe browser operations.
- Strava tokens stay server-side.
- Hosted preview uses managed secrets and storage, not committed `.env` or JSON token stores.
- Logs and evidence artifacts must not contain tokens, secrets, authorization codes, or raw private athlete data.
- Operator routes require role/permission checks.

## Observability

| Signal | Purpose |
| --- | --- |
| `auth.provider.connected` | Confirm connection path without exposing tokens. |
| `activity.import.empty` | Distinguish no runs from provider failure. |
| `evidence.submitted` | Audit runner evidence flow. |
| `evidence.preview_accepted` | Track preview-only controller updates. |
| `controller.updated` | Verify UI-visible state change. |
| `geometry.claim_blocked` | Catch route/map claims without geometry source. |
| `secret.redaction_check` | Confirm no secret leakage in validation artifacts. |

## Backend Acceptance Bar

The backend is acceptable for the next hosted preview only when:

1. Auth/session/CSRF tests pass.
2. Strava activity summaries are redacted.
3. Submission can update preview controller.
4. `preview-accepted` and `verified` stay separate.
5. Geometry status controls route/map wording.
6. No tokens/secrets/raw private payloads appear in logs or tracked artifacts.
