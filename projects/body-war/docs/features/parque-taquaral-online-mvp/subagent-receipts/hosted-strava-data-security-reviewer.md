---
dispatch_id: body-war-pilot-domainspec-subagent-strategy-20260614
role_id: hosted-strava-data-security-reviewer
agent_id: 019ec50d-82f6-7911-84e9-6050e2788998
spawn_status: spawned
join_status: completed
close_status: closed
validation_result: pass
status: complete
last_updated: 2026-06-14
---

# Receipt: Hosted Strava Data Security Reviewer

## Scope

Audit hosted preview, Strava OAuth, managed storage, sealed secrets, token
storage, friend privacy, and deployment contracts.

## Key Findings

- Hosted public preview is selected, but no deployment contract names the
  provider, callback URL, secret store, runtime, or env inventory.
- Managed storage is selected as a category, but no provider/schema has been
  chosen.
- Existing Strava prototype assumptions are local-only: `.env`, localhost
  callback, and local JSON token/submission storage.
- Auto-accept and preview-only validation are acceptable only with guardrails
  that prevent pilot-ready, GPS-validation, or anti-cheat claims.

## Missing Security/Deployment Specs

| Contract | Risk Controlled | Priority |
| --- | --- | --- |
| Hosted preview provider | Callback/HTTPS/runtime/env mismatch. | P0 |
| Hosted Strava OAuth | Redirect URI, scopes, session state, token refresh, consent. | P0 |
| Managed storage provider | Where tokens, submissions, controller state, and audit records live. | P0 |
| Token/sealed-secret storage | Refresh-token leakage, repo leakage, log leakage, rotation/revocation. | P0 |
| Environment inventory | Deploy reproducibility and committed `.env` drift. | P0 |
| Privacy/redaction | What friend activity data may appear in docs, UI, API, logs, observability. | P0 |
| Retention/deletion | How long friend activity evidence and tokens persist. | P1 preview, P0 pilot-ready |
| Access control | Open/unlisted/password/restricted preview behavior. | P1 preview, P0 pilot-ready |

## Tensions

- The decision gate says no product-choice blockers remain, but provider/schema
  choice remains a P0 implementation-spec gap.
- `DISCOVERY.md` and `ARCHITECTURE-AUDIT.md` still describe local persistence as
  if it were the next runtime shape; hosted preview now needs managed storage.
- The dispatch declares protected namespaces, but no privacy/retention spec
  exists yet.

## Backlog Contribution

1. Add `DEPLOYMENT-SECURITY.md` or equivalent security section before code
   mutation.
2. Select hosted app/runtime and managed storage provider.
3. Define token, athlete, activity summary, submission, controller state, audit
   log, retention, deletion, and revocation contracts.
4. Add hosted OAuth/API contract for scopes, state/session handling,
   redactions, and error states.
5. Gate TypeScript implementation on provider/schema/env contract.

