# WORK-PACK: Strava-Linked Pilot Test

## Invoke Result

- Mode: plan
- Spell: invoke
- Canonical ID: invoke
- Scope: Body War / TROQAR Strava-linked pilot testing
- Phase status: pass
- Mode contract: `arcanum/spells/invoke/plan.md`
- Outputs: `IMPLEMENTATION-LAYERING.md`, `WORK-PACK.md`
- Implementation layering: `IMPLEMENTATION-LAYERING.md`
- Work-pack: single-file
- Complexity: low
- Per-layer planning: compact L0-L3
- Implementation detail: inline
- Smallest working units: n/a, each task is already the smallest executable test step
- Target artifact: `projects/body-war/app/`, feature test plan
- Next route: task-session

## Objective

Test the Strava-linked pilot app enough to decide whether the app-backed validation channel is ready for a real runner pilot.

## Source Contracts

| Source                                              | Role                                                                       |
| --------------------------------------------------- | -------------------------------------------------------------------------- |
| `SPEC.md`                                           | Feature contract and acceptance criteria.                                  |
| `projects/body-war/app/README.md`                   | Local setup and API surface.                                               |
| `projects/body-war/app/server.py`                   | Backend OAuth/API implementation under test.                               |
| `projects/body-war/app/static/`                     | Frontend under test.                                                       |
| `projects/body-war/docs/decisions/mvp-readiness.md` | Decision authority for app-backed validation and hybrid scoring/readiness. |
| Strava Authentication docs                          | OAuth, callback, token exchange, token refresh, scope handling.            |
| Strava Activities API docs                          | `/athlete/activities` behavior, parameters, and scope requirements.        |

## Environment Requirements

Create `projects/body-war/app/.env` from `.env.example` with:

```text
STRAVA_CLIENT_ID=<from Strava app>
STRAVA_CLIENT_SECRET=<from Strava app>
STRAVA_REDIRECT_URI=http://127.0.0.1:5174/api/auth/strava/callback
BODY_WAR_PUBLIC_BASE_URL=http://127.0.0.1:5174
BODY_WAR_HOST=127.0.0.1
BODY_WAR_PORT=5174
BODY_WAR_SESSION_SECRET=<random local secret>
```

Strava app setting:

```text
Authorization Callback Domain: 127.0.0.1
```

Required OAuth scope for this plan:

```text
read,activity:read
```

Use `activity:read_all` only if the test athlete needs to import private or Only Me activities.

## Delivery Slices

| Slice | Layer | Outcome                                                                |
| ----- | ----- | ---------------------------------------------------------------------- |
| S-001 | L0    | Local unauthenticated smoke passes.                                    |
| S-002 | L1    | Strava OAuth link succeeds for one test athlete.                       |
| S-003 | L2    | A real Strava run is submitted as track evidence.                      |
| S-004 | L3    | Token refresh and failure states are safely handled.                   |
| S-005 | L3    | Evidence is reviewed and the next implementation decision is recorded. |

## Task Board

| Task ID         | Goal                                                  | Layer | Status                             |
| --------------- | ----------------------------------------------------- | ----- | ---------------------------------- |
| STRAVA-TEST-001 | Run local smoke tests without credentials.            | L0    | ready                              |
| STRAVA-TEST-002 | Configure Strava app credentials and complete OAuth.  | L1    | blocked until credentials exist    |
| STRAVA-TEST-003 | Fetch activities and submit one run to a pilot track. | L2    | blocked until OAuth passes         |
| STRAVA-TEST-004 | Test token refresh and error states.                  | L3    | blocked until OAuth passes         |
| STRAVA-TEST-005 | Review evidence and decide readiness.                 | L3    | blocked until test evidence exists |

## Task Contracts

### STRAVA-TEST-001 - Local Smoke

Goal:

Prove the app starts locally and returns safe unauthenticated responses.

Steps:

1. From `projects/body-war/app`, run `python3 server.py`.
2. In another shell, run:

```bash
python3 -m py_compile projects/body-war/app/server.py
python3 -c "import urllib.request; print(urllib.request.urlopen('http://127.0.0.1:5174/api/status').read().decode())"
python3 -c "import urllib.request; print(urllib.request.urlopen('http://127.0.0.1:5174/api/tracks').read().decode())"
python3 -c "import urllib.request; data=urllib.request.urlopen('http://127.0.0.1:5174/').read().decode(); print(data[:120])"
```

Acceptance:

- Backend compiles.
- `/api/status` returns `configured=false` when `.env` is absent.
- `/api/tracks` returns at least `craft-distill-blocker` and `park-track-alpha`.
- `/` returns the HTML app shell.

Evidence:

- Command output pasted or saved in task-session result.

### STRAVA-TEST-002 - OAuth Link

Goal:

Connect one Strava test athlete through the local OAuth flow.

Steps:

1. Create `.env` from `.env.example`.
2. Set the Strava app callback domain to `127.0.0.1`.
3. Start `python3 server.py`.
4. Open `http://127.0.0.1:5174`.
5. Click `Connect Strava`.
6. Authorize with a consenting test athlete.
7. Verify `/api/status`.

Acceptance:

- OAuth redirects back to `/api/auth/strava/callback`.
- `/api/status` returns `connected=true`.
- Athlete identity is visible.
- `data/strava-tokens.json` exists locally but is ignored by git.
- Accepted scope includes `activity:read`; if not, record blocker.

Evidence:

- Redacted `/api/status` JSON.
- Screenshot or note that token files are ignored by git.

### STRAVA-TEST-003 - Activity Import And Track Submission

Goal:

Submit one real Strava run as pilot evidence.

Steps:

1. After OAuth, call `/api/activities?per_page=12` or use the UI.
2. Confirm at least one run activity is listed.
3. Select `park-track-alpha` for Body War runner evidence, or `craft-distill-blocker` for internal pilot evidence.
4. Submit the activity.
5. Verify `/api/submissions`.

Acceptance:

- Activity list returns Strava `SummaryActivity` records.
- Only run-like sport types are shown in the UI.
- Submission includes `track_id`, `activity_id`, athlete, distance, moving time, status, and hybrid authority fields.
- Submission does not expose access or refresh tokens.

Evidence:

- Redacted `/api/activities` sample.
- Redacted `/api/submissions` sample.

### STRAVA-TEST-004 - Token Refresh And Failure States

Goal:

Prove the pilot fails safely around auth/API edge cases.

Steps:

1. With a connected athlete, edit local `data/strava-tokens.json` and set `expires_at` to a past epoch.
2. Call `/api/activities`.
3. Confirm the backend refreshes the token or returns a clear Strava error.
4. Test `/api/auth/strava/start` with missing `.env` in a separate clean run.
5. Test denied OAuth if convenient.

Acceptance:

- Expired-token path attempts refresh before activity fetch.
- Missing credentials return `strava_not_configured`.
- Invalid/denied auth returns visible `auth_error` path.
- No tokens appear in UI or API responses.

Evidence:

- Redacted command output and before/after token timestamp notes.

### STRAVA-TEST-005 - Readiness Review

Goal:

Decide whether the Strava-linked validation channel is ready for a real runner pilot.

Review checklist:

| Check      | Pass Condition                                                      |
| ---------- | ------------------------------------------------------------------- |
| OAuth      | One test athlete connects.                                          |
| Activities | At least one run imports.                                           |
| Submission | One activity submits to a pilot track.                              |
| Privacy    | No token or secret appears in API/UI output.                        |
| Data       | Token/submission files stay ignored by git.                         |
| UX         | Test user can understand the connect, refresh, submit flow.         |
| Scope      | No monetization, full anti-cheat, or map automation sneaks into L0. |

Acceptance:

- Record result as `pass`, `flag`, or `block`.
- Update `docs/decisions/mvp-readiness.md` only if a blocker decision changes.
- Create follow-up task if the app needs fixes before pilot use.

Evidence:

- Short readiness note with pass/flag/block and next route.

## Validation Strategy

| Validation      | Command Or Review                                                                                                                                                       |
| --------------- | ----------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| Backend syntax  | `python3 -m py_compile projects/body-war/app/server.py`                                                                                                                 |
| Dispatch route  | `python3 arcanum/formulae/dispatch-spec/scripts/validate-dispatch.py projects/body-war/development/refinement-runs/20260608T005429Z-mvp-readiness/REFINE-DISPATCH.json` |
| Local API smoke | `/api/status`, `/api/tracks`, `/` via `urllib.request`                                                                                                                  |
| Live OAuth      | Browser flow with Strava test athlete                                                                                                                                   |
| Activity import | `/api/activities?per_page=12`                                                                                                                                           |
| Evidence submit | `POST /api/submissions` through UI                                                                                                                                      |
| Data safety     | `git status --ignored --short -- projects/body-war/app` review                                                                                                          |

## Blockers And Gaps

| ID               | Severity | Description                                                 | Next Action                                                     |
| ---------------- | -------- | ----------------------------------------------------------- | --------------------------------------------------------------- |
| STRAVA-BLOCK-001 | blocker  | Strava credentials are operator-owned and absent from repo. | Operator creates Strava app and local `.env`.                   |
| STRAVA-BLOCK-002 | blocker  | Live OAuth cannot be fully tested without browser consent.  | Run STRAVA-TEST-002 interactively.                              |
| STRAVA-GAP-001   | flag     | Track boundary validation is not implemented.               | Keep out of L0; add later geometry task if runner pilot passes. |
| STRAVA-GAP-002   | flag     | Token storage is local JSON, not production secure storage. | Accept for local pilot only; harden before broader rollout.     |
| STRAVA-GAP-003   | flag     | No automated test harness yet.                              | Add after the live OAuth path is proven.                        |

## Current State

Already completed before this plan:

- Backend compiled once.
- Local smoke checks returned page/status/track responses without credentials.
- Dispatch validation returned `VALIDATION=pass`.

Still needed:

- Real Strava credentials.
- Browser OAuth.
- Live activity fetch.
- Live submission evidence.

## Recommended Next Route

Run `task-session` against `STRAVA-TEST-001` first if you want a clean evidence record, then continue task-by-task through `STRAVA-TEST-005`.
