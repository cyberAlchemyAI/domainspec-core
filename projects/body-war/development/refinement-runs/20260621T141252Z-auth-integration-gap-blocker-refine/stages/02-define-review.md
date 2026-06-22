# Invoke Define Review

Stage: `s02-invoke-define-review`
Owner: `invoke`
Status: `flag`
Mode: `define-review`
Mode contract: `spells/invoke/define.md`

## Review Target

Existing define/spec artifact:

- `projects/body-war/development/invoke-runs/20260621T131933Z-auth-user-management-integration/AUTH-INTEGRATION-SPEC.md`

## Verdict

The spec defines the correct ownership boundary and is usable for downstream
execution, but it carries known non-blocking documentation repair residue.

## Passed Define Points

- Core auth stays in `@domainspec/auth-user-management`.
- BodyWar owns browser cookies, CSRF, origin checks, Strava OAuth, provider
  token custody, profile projection, activity import, HTTP routes, and UI.
- The new package ask is generic: `createTrustedSessionUseCase`, not a Strava
  or browser helper.
- Acceptance criteria are local-first and do not require VPS access, real Strava
  credentials, or friend activity evidence.
- Security invariants explicitly prohibit token/OAuth-code leakage and raw
  private provider payloads in tracked receipts.

## Flags

| Flag | Owner | Repair Path |
| --- | --- | --- |
| Existing BodyWar docs still contain stale ownership claims from earlier auth work. | BodyWar docs | `SWU-BWAUTH-007` |
| The current app and tests still import non-exported package helpers. | BodyWar app plus auth package integration | `SWU-BWAUTH-001` through `SWU-BWAUTH-003` |

## Invoke Result

- Mode: `define-review`
- Spell: `invoke`
- Canonical ID: `invoke`
- Scope: `library`
- Phase status: `flag`
- Outputs: `AUTH-INTEGRATION-SPEC.md`
- Template selection: existing BodyWar auth integration spec, no new template needed.
- Dispatch techniques: `artifact_contract_bridge`, `owner_boundary_check`.
- Distill validation: deferred to stage 05.
- Decisions: no new operator decision required before `SWU-BWAUTH-001`.
- Unresolved gaps: stale docs and current broken imports.
- Next route: `design-review`

## Receipt

```yaml
run_id: 20260621T141252Z-auth-integration-gap-blocker-refine
session_id: session-20260621T141252Z
capability_ref: invoke
receipt_kind: native-stage
artifact: stages/02-define-review.md
status: flag
validation_result: spec usable; flags named and routed
blockers:
  - none for SWU-BWAUTH-001
handoff_note: Preserve package/BodyWar ownership split during design review.
```
