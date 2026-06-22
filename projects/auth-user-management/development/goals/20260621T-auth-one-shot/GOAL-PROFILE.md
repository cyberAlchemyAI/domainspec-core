# Codex Goal Profile - Auth One-Shot

- Profile id: `ONE-SHOT-AUTH-FOUNDATION-001`
- Created: 2026-06-21
- Skill: `codex-goal-profile`
- Source work-pack: `projects/auth-user-management/development/refinement-runs/20260621T025133Z-auth-strava-foundation/stages/09-invoke-plan/PLAN.md`
- Handoff pack: `projects/auth-user-management/development/refinement-runs/20260621T025133Z-auth-strava-foundation/RUNTIME-HANDOFF.md`
- Context index: `projects/auth-user-management/development/refinement-runs/20260621T025133Z-auth-strava-foundation/evidence-index.json`
- Result synthesis: `projects/auth-user-management/development/refinement-runs/20260621T025133Z-auth-strava-foundation/RESULT.md`

## Readiness

- Readiness: `pass`
- One-shot mode: `yes`
- Selected stream: `SWU-AUTH-001..SWU-AUTH-006`, with `SWU-BW-AUTH-001` as the terminal Body War consumer adapter when it can be done without a new architecture/runtime decision.
- Strict coverage: `pass`; the refine handoff, evidence index, design, plan, and final synthesis all exist.
- Fallback exploration: `named gaps only`
- Extra-source reporting: `required`

## Outcome

Finish the auth implementation stream in one governed Codex goal:

1. Define reusable auth core domain and ports.
2. Implement browser cookie session guard and denial tests.
3. Implement bearer `sid` guard and denial tests.
4. Implement storage adapter contract and migration notes.
5. Implement Strava provider adapter with server-owned token custody and fixture-only tests.
6. Write copy/adoption guide.
7. Wire Body War as first consumer for login, server-owned session, Strava connection, recent activity summary import, and redacted submission handoff if safe inside the existing pilot boundary.

## Work Order

Run prerequisite units before runtime/consumer units:

| Order | Unit | Stop gate |
|---|---|---|
| 1 | `SWU-AUTH-001` | Core domain and ports compile/test before guards. |
| 2 | `SWU-AUTH-002` | Browser guard denial tests pass before Body War browser use. |
| 3 | `SWU-AUTH-003` | Bearer guard tests pass before documenting service/API use. |
| 4 | `SWU-AUTH-004` | Storage/provider token contract exists before Strava adapter. |
| 5 | `SWU-AUTH-005` | Strava fixture tests pass without real tokens/secrets. |
| 6 | `SWU-AUTH-006` | Adoption docs describe copy boundary and env/storage expectations. |
| 7 | `SWU-BW-AUTH-001` | Only proceed if Body War integration does not require track/game work or a new app-runtime decision. |

## Write Scope

Allowed:

- `projects/auth-user-management/src/**`
- `projects/auth-user-management/tests/**`
- `projects/auth-user-management/docs/**`
- `projects/auth-user-management/package.json`, test/type config, and local package support files as needed
- `projects/auth-user-management/.craft/ledger.yml`
- `projects/auth-user-management/CRAFT.md`
- `projects/body-war/app/**` only for the auth consumer adapter
- `projects/body-war/.craft/ledger.yml`
- `projects/body-war/CRAFT.md`
- task-session or goal evidence under `projects/auth-user-management/development/**`

Not allowed:

- `validation/poker-team/**`
- `projects/savvy_legal-studio-ai/**`
- `arcanum/**`
- track geometry, scoring, game mechanics, anti-cheat, payments, RunCoins, premium, sponsor mechanics
- real Strava secrets, access tokens, refresh tokens, auth codes, or raw athlete private data in repo artifacts

## Source Context

Read pack-first:

- `RUNTIME-HANDOFF.md`
- `evidence-index.json`
- `RESULT.md`
- `stages/06-invoke-design/DESIGN.md`
- `stages/09-invoke-plan/PLAN.md`

Then inspect only named implementation references needed for a gap:

- `validation/poker-team/docs/features/auth-access-control/SPEC.md`
- `validation/poker-team/backend/src/domain/auth-access-control/**`
- `validation/poker-team/backend/src/use-cases/auth-access-control/**`
- `projects/savvy_legal-studio-ai/frontend/savvy-legal-studio/lib/auth/savvy-auth.ts`
- `projects/savvy_legal-studio-ai/frontend/savvy-legal-studio/tests/auth/savvy-auth.test.ts`
- `projects/body-war/app/server.py`
- `projects/body-war/app/static/**`

## Capability Policy

- `task-session`: allowed as execution style, but do not create broad unrelated task packs.
- `craft`: allowed only to update scoped auth/body-war ledger state and human views after implementation validation.
- `refine`: allowed only if the pack has a named design/plan gap that blocks safe implementation.
- `invoke`: allowed only to author a missing handoff/plan artifact named by the pack.
- `decision-gate`: required before selecting a new storage/deployment/runtime architecture not already implied by the pack.
- Subagents: not authorized by this profile. Ask before spawning implementation agents.

## Verification Surface

The implementation run must create or select concrete project-local validation commands and run them before marking the goal complete. Minimum required checks:

```bash
git diff --check -- projects/auth-user-management projects/body-war
python3 -m py_compile projects/body-war/app/server.py
python3 -m json.tool projects/auth-user-management/development/refinement-runs/20260621T025133Z-auth-strava-foundation/evidence-index.json >/dev/null
python3 - <<'PY'
from pathlib import Path
import yaml
for path in [Path('projects/auth-user-management/.craft/ledger.yml'), Path('projects/body-war/.craft/ledger.yml')]:
    yaml.safe_load(path.read_text())
print('yaml ok')
PY
```

If `projects/auth-user-management/package.json` is created, it must expose a test command and the run must execute it. If Body War tests are added, run the project-local Python test command and report it.

## Acceptance Gates

- Forged client auth state cannot access protected routes.
- Expired, revoked, inactive, malformed, unknown, or orphaned sessions fail.
- Unsafe browser methods require same-origin and valid CSRF binding.
- Missing permission or resource mismatch returns deterministic forbidden.
- Bearer token expiry, revocation, missing `sid`, and inactive/missing session fail.
- Strava callback validates state and stores tokens only server-side.
- Strava activity import redacts tokens and avoids broad scope by default.
- Body War can consume login/session/Strava connection without owning token custody.
- Adoption docs describe copy boundary, env vars, storage, permissions, provider adapters, and test expectations.

## Stop Conditions

Stop and report a blocked result if:

- implementation requires real Strava credentials, tokens, auth codes, or raw private athlete data;
- Body War integration requires track/game/scoring work;
- safe completion requires choosing a new hosted app runtime, database, secret manager, or deployment provider not already selected by the pack;
- test infrastructure cannot be made project-local without broad repo dependency churn;
- unrelated dirty submodule state would need to be modified or reverted;
- the native goal exceeds its write boundary.

## Native Goal

```text
/goal Finish ONE-SHOT-AUTH-FOUNDATION-001 using sidecar projects/auth-user-management/development/goals/20260621T-auth-one-shot/GOAL-PROFILE.md: implement ordered auth stream SWU-AUTH-001..006 and, if safe within the existing Body War Python pilot, SWU-BW-AUTH-001. Verify with the auth package tests you add, py_compile/unittest for Body War changes, JSON/YAML parse for planning surfaces, markdown link checks, and git diff --check scoped to projects/auth-user-management and projects/body-war. Constraints: pack-first; no real Strava tokens/secrets/athlete raw data; no writes to validation/poker-team, Savvy, or public arcanum; no track/game/scoring work. Iterate in SWU order and update evidence/ledger only after passing checks. Stop and report if a blocker-level runtime/storage/framework decision, real credential need, unrelated dirty submodule mutation, or scope expansion appears.
```

## Audit

- Decision profile: none provided.
- Private profile contents copied: none.
- Goal budget: default 4000 characters; native goal is intentionally sidecar-backed.
- Extra-source report required in final runtime response: yes.
