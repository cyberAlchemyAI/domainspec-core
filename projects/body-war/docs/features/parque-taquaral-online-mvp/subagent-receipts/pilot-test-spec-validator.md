---
dispatch_id: body-war-pilot-domainspec-subagent-strategy-20260614
role_id: pilot-test-spec-validator
agent_id: 019ec50d-7fce-72e3-b122-f9cc0b1f51fd
spawn_status: spawned
join_status: completed
close_status: closed
validation_result: pass
status: complete
last_updated: 2026-06-14
---

# Receipt: Pilot Test Spec Validator

## Scope

Audit missing `TEST-SPEC.md` and preview-validation coverage for the hosted
friend preview target.

## Key Findings

- No feature-local `TEST-SPEC.md` exists for Parque Taquaral online MVP.
- The required proof bar is preview-only: hosted URL loads, friend completes
  Strava login, activity appears, submission works, and controller updates.
- The proof bar must not claim anti-cheat, final GPS validation, pilot-ready, or
  engineering-ready status.
- Existing validation evidence is local/Python-prototype oriented and blocked at
  activity import because the connected athlete returned zero activities.
- Local `.env` and ignored JSON checks are not enough for hosted sealed-secret
  validation.

## Missing TEST-SPEC Coverage

| Check | Evidence Needed | Priority |
| --- | --- | --- |
| Hosted URL reachable | HTTPS preview URL loads app shell; callback URL uses same hosted origin. | P0 |
| Friend OAuth | Redacted evidence of Strava login and connected status; no tokens exposed. | P0 |
| Activity import/list | One live friend run appears, with no-secret mock/fixture preflight allowed only as support. | P0 |
| Track submission | Selected activity posts to the Parque track with redacted response. | P0 |
| Preview controller update | Controller state visibly changes after auto-accepted submission. | P0 |
| No visible secret leakage | Repo docs, API/UI output, logs, screenshots, and observability omit tokens/secrets/raw private activity. | P0 |
| No-secret mocks | Mock Strava/OAuth/token-store adapters for pre-secret checks. | P1 |
| Later pilot readiness | Geometry proof, anti-cheat, operator verification, persistence audit, engineering suite. | P2 |

## Tensions

- Forecast validation mentions fixtures/local checks, but final preview success
  requires live hosted friend proof.
- Current runtime appends `submitted` evidence; the test spec needs an assertion
  for actual controller-state mutation.
- Old test docs include direct local token-store manipulation; that must not be
  reused as hosted preview validation.

## Backlog Contribution

1. Create `TEST-SPEC.md` with stable IDs and `Validates` links.
2. Add P0 hosted-preview smoke matrix.
3. Add no-secret fixture/mocking coverage as supportive, not final proof.
4. Add redaction/no-leak checklist.
5. Split deferred pilot-ready and engineering-ready tests.

