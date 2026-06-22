# Context Pack - Auth Work-Pack One-Shot

Task Session ID: `20260621T-auth-workpack-oneshot`
Mode: `standard`
Strict coverage: `pass`
Runtime: `local`

## Selected Scope

Operator-approved one-shot execution of the related auth work-pack:

- `SWU-AUTH-001`
- `SWU-AUTH-002`
- `SWU-AUTH-003`
- `SWU-AUTH-004`
- `SWU-AUTH-005`
- `SWU-INV-001`
- `SWU-BW-001`
- `SWU-AUTH-008`

This intentionally expands from the work-pack's recommended first-SWU route. The expansion is accepted because the user explicitly asked to one-shot all auth work.

## Controlling Constraints

1. Shell first where shell is sufficient.
2. TypeScript for runtime/domain/application/infrastructure/interface behavior.
3. Python auth runtime is superseded drift and must not remain the selected auth foundation.
4. DomainSpec Functional TypeScript layering controls package shape.
5. Body War auth work stays limited to login/session/Strava/auth consumer boundaries; track and game mechanics remain deferred.
6. Provider tokens and secrets must not be returned to clients or committed to tracked data.
7. Existing unrelated Python projects are legacy surfaces; they are not part of this one-shot migration.

## Source Evidence

| Source | Why Included |
| --- | --- |
| `WORK-PACK.md` | SWU list, dependencies, write scopes, done criteria, validation surfaces. |
| `IMPLEMENTATION-LAYERING.md` | L0-L3 progression and promotion gates. |
| `implementation/domainspec/architecture/pattern-library/ARCHITECTURE-FOUNDATIONS.md` | Functional TypeScript principles. |
| `implementation/domainspec/architecture/pattern-library/LAYERING-REFERENCE.md` | Layer responsibilities and folder blueprint. |
| `implementation/domainspec/architecture/pattern-library/DEPENDENCY-RULES.md` | Inward-only dependency rules. |
| `implementation/domainspec/architecture/pattern-library/TESTING-ALIGNMENT.md` | Required test mapping. |
| `validation/poker-team/backend/src/domain/auth-access-control/` | TypeScript auth domain reference. |
| `validation/poker-team/backend/src/use-cases/auth-access-control/` | Authenticate/authorize/logout use-case reference. |
| `validation/poker-team/backend/src/infrastructure/http/auth/auth.guard.ts` | Route guard reference. |
| `projects/savvy_legal-studio-ai/frontend/savvy-legal-studio/lib/auth/savvy-auth.ts` | Browser cookie/session/CSRF/audit reference. |
| `projects/savvy_legal-studio-ai/frontend/savvy-legal-studio/tests/auth/savvy-auth.test.ts` | Denial matrix reference. |
| `projects/auth-user-management/src/auth_user_management/` | Python drift to replace. |
| `projects/body-war/app/server.py` | Python auth consumer to replace. |

## Write Scope

Allowed:

- `projects/auth-user-management/`
- `projects/body-war/app/`
- `development/invariants/`
- `tools/check-runtime-language-policy.sh`
- `development/refinement-runs/20260621T-typescript-domainspec-invariant/`

Not allowed:

- public `arcanum`
- unrelated projects
- Body War track/game mechanics beyond preserving existing data routes
- tracked Strava token stores or secrets

## Decisions

| Decision | Selected | Classification |
| --- | --- | --- |
| Execute all related auth SWUs in one Task Session | yes, sequentially | operator-approved scope expansion |
| Runtime implementation language | TypeScript | binding |
| Validation/orchestration language | shell where sufficient | binding |
| Body War migration shape | TypeScript server/package boundary for auth pilot | implementation assumption |
| Production secret/live Strava smoke | documented but secret-gated | deferred |

## Validation Surface

- `bash projects/auth-user-management/scripts/validate.sh`
- `bash tools/check-runtime-language-policy.sh`
- `npm --prefix projects/body-war/app run check`
- `python3 -m json.tool development/refinement-runs/20260621T-typescript-domainspec-invariant/evidence-index.json`
- `python3 -m json.tool development/refinement-runs/20260621T-typescript-domainspec-invariant/task-session/20260621T-auth-workpack-oneshot/context-index.json`
- `python3 arcanum/formulae/dispatch-spec/scripts/validate-dispatch.py development/refinement-runs/20260621T-typescript-domainspec-invariant/REFINE-DISPATCH.json`
- YAML parse for `projects/auth-user-management/.craft/ledger.yml` and `projects/body-war/.craft/ledger.yml`
- `git diff --check -- projects/auth-user-management projects/body-war/app development/invariants tools/check-runtime-language-policy.sh development/refinement-runs/20260621T-typescript-domainspec-invariant`

## Gate Verdict

Gate status: `pass`

The scope is broad but related, explicitly authorized, and still bounded to auth/user-management, language policy, and Body War auth consumption. Execute sequentially and stop on validation failure.
