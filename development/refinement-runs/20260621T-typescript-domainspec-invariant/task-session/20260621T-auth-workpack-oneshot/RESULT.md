# Task Session Result - Auth Work-Pack One-Shot

Task Session ID: `20260621T-auth-workpack-oneshot`
Status: `pass`
Execution mode: operator-approved one shot

## Scope Completed

| SWU | Result |
| --- | --- |
| `SWU-AUTH-001` | Replaced the Python auth runtime with `@domainspec/auth-user-management`, a TypeScript package with build/test/validate scripts. |
| `SWU-AUTH-002` | Added auth domain types and deny-overrides permission behavior. |
| `SWU-AUTH-003` | Added session create/authenticate/revoke use cases. |
| `SWU-AUTH-004` | Added browser cookie/CSRF guard, bearer `sid` guard, HMAC codec, memory store, and JSON store. |
| `SWU-AUTH-005` | Added Strava OAuth start/callback/scope validation/token refresh/activity summary adapter with mocked tests. |
| `SWU-INV-001` | Added `development/invariants/runtime-language-policy.md` and `tools/check-runtime-language-policy.sh`. |
| `SWU-BW-001` | Moved Body War auth consumer from `server.py` to `server.ts` and linked it to the shared TypeScript auth package. |
| `SWU-AUTH-008` | Updated active auth adoption docs, Body War app docs, and Craft runtime references; live Strava smoke remains secret-gated. |

## Runtime Outputs

- `projects/auth-user-management/package.json`
- `projects/auth-user-management/src/`
- `projects/auth-user-management/tests/`
- `projects/auth-user-management/scripts/validate.sh`
- `projects/body-war/app/package.json`
- `projects/body-war/app/server.ts`
- `projects/body-war/app/tests/auth-consumer.test.ts`
- `development/invariants/runtime-language-policy.md`
- `tools/check-runtime-language-policy.sh`

## Validation Evidence

| Command | Status |
| --- | --- |
| `npm run validate` from `projects/auth-user-management` | pass, 10 tests |
| `npm run check` from `projects/body-war/app` | pass, 2 tests |
| `bash tools/check-runtime-language-policy.sh` | pass |
| `python3 -m json.tool development/refinement-runs/20260621T-typescript-domainspec-invariant/evidence-index.json` | pass |
| `python3 -m json.tool development/refinement-runs/20260621T-typescript-domainspec-invariant/task-session/20260621T-auth-workpack-oneshot/context-index.json` | pass |
| `python3 arcanum/formulae/dispatch-spec/scripts/validate-dispatch.py development/refinement-runs/20260621T-typescript-domainspec-invariant/REFINE-DISPATCH.json` | pass |
| YAML parse for `projects/auth-user-management/.craft/ledger.yml` and `projects/body-war/.craft/ledger.yml` | pass |
| `git diff --check -- projects/auth-user-management projects/body-war/app development/invariants tools/check-runtime-language-policy.sh development/refinement-runs/20260621T-typescript-domainspec-invariant` | pass |

## Boundaries Preserved

- No writes to public `arcanum`.
- No writes to `validation/poker-team` or `projects/savvy_legal-studio-ai`.
- Track/game/scoring mechanics remained deferred.
- Strava provider tests use fixtures and do not require live secrets.
- Local token/session JSON data remains ignored.

## Residue

- Hosted production still needs a selected durable session/token store and provider-token encryption backend.
- Live Strava smoke proof requires operator-supplied credentials and a consenting account.
- Existing unrelated Python surfaces remain legacy debt outside this auth one-shot.
