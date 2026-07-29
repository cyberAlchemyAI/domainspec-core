# SuggestedTrack Testable-Prototype Gap Research

Verbatim explorer returns for dispatch
`2026-07-27-body-war-suggested-track-prototype-gap`. These returns are evidence
inputs, not final findings or implementation authority.

## Agent 1 — van Lamsweerde, Axel

# SuggestedTrack implemented-versus-specified gap matrix

Direct answer: the current bytes are already sufficient for local fake-Strava prototype testing. No material item must be fixed before that testing begins. The prototype is not ready for a real friend’s Strava activity: the activity path is still synthetic, and the browser silently asserts consent instead of asking for it. Those are product-code gaps, not merely deployment paperwork.

Body War application bytes remain the authority for this assessment; the Inventory entry was used only as an ownership guardrail and explicitly says Body War authority stays under `projects/body-war/` and that the read model does not authorize production (`.arcanum/inventory/entries/domainspec-v2-fpr02-integrated-consumer-proof-refresh.md:49-58`).

| Material capability / obligation | Current implementation | Proof status | Classification |
|---|---|---|---|
| Connected-runner list and create loop | The contract requires authenticated list/create and `needs_evidence` creation (`projects/body-war/docs/features/parque-taquaral-online-mvp/SPEC.md:23-27`; `interfaces.md:5-39`). Runtime authenticates a connected runner, checks permissions, lists, validates inputs, and creates the record (`projects/body-war/app/server.ts:560-637`). | **Executed:** current `npm run validate` and standalone `npm test` passed; the 3/3 Node suite exercised fake login, list, CSRF rejection, and creation (`projects/body-war/app/tests/auth-consumer.test.ts:15-109`). | **test-now** |
| Idempotent Taquaral seed and honest initial authority | Spec requires `volta-do-taquaral`, `needs_evidence`, memory and Postgres availability (`operations.md:47-63`). Memory preserves an existing seed’s status while refreshing its metadata (`projects/body-war/app/src/auth/memory-repository.ts:33-55`); Postgres upserts the same seed and only assigns initial authority on insert (`projects/body-war/app/src/auth/drizzle-repository.ts:44-80`). Unique slug is schema-enforced (`projects/body-war/app/src/infrastructure/postgres/schema.ts:92-117`). | **Executed** for memory seed; **observed** for current Postgres code. Earlier managed-Postgres execution passed (`projects/body-war/development/task-sessions/20260629T061500Z-suggested-track-one-go-build/TASK-SESSION-RESULT.md:21-29`). | **test-now** |
| Candidate attach API, activity ownership check, redaction, and state transition | The operation requires consent, a currently visible activity, allow-listed summary fields, and no promotion (`operations.md:25-45`). Server rejects missing consent, refetches activities for the authenticated principal, matches the requested ID, constructs an allow-listed summary, and returns non-authoritative labels (`projects/body-war/app/server.ts:392-402`; `server.ts:672-725`). Both repositories create `submitted` evidence and move only `needs_evidence` to `evidence_submitted` (`projects/body-war/app/src/auth/memory-repository.ts:192-218`; `src/auth/drizzle-repository.ts:266-295`). | **Executed:** missing consent, attach, status transition, no-token response, and claim ceilings passed (`projects/body-war/app/tests/auth-consumer.test.ts:111-144`). | **test-now** with fake activity |
| Detail/readback and evidence summary | Contract requires the selected track, current runner’s candidates, a redacted count, and non-claims (`queries.md:19-36`). Runtime separately reads all candidates and principal-filtered candidates, then publishes redaction and authority posture (`projects/body-war/app/server.ts:640-669`; `server.ts:374-389`). Browser loads each detail and renders the current runner’s redacted submissions (`projects/body-war/app/static/app.js:423-459`). | **Observed:** implementation exists; no direct API assertion for the detail payload was found in the current Node/Postgres tests. The prior Playwright receipt covers the visible flow but not every detail field (`projects/body-war/development/task-sessions/20260629T061500Z-suggested-track-one-go-build/TASK-SESSION-RESULT.md:27-28`). | **test-now**, add a focused detail test during hardening |
| Browser list/create/help/submission loop | Required UI includes list, create form, help action, evidence summary, honest copy, and responsive controls (`ui-spec.md:3-37`). Current browser renders tracks, creates suggestions, offers track selection beside each activity, submits evidence, and renders owned candidates (`projects/body-war/app/static/app.js:255-337`; `app.js:361-459`). The Playwright flow creates “Lago extra,” selects it, and submits one candidate (`projects/body-war/app/e2e/troqar-product-architecture/ui.spec.ts:78-97`); 320px/390px checks exist (`ui.spec.ts:108-130`). | **Observed:** prior receipt says 7/7 Playwright passed (`TASK-SESSION-RESULT.md:28`); not rerun in this explorer lane. One minor spec drift remains: the spec places SuggestedTrack after profile and before recent activities (`ui-spec.md:5-6`), while HTML places activities first (`projects/body-war/app/static/index.html:89-147`). | **test-now**; use testing to decide whether UI or spec ordering should win |
| Affirmative browser consent | Contract says the runner attaches activity “with explicit consent” and stores the phrase shown at submit time (`operations.md:27-35`; `ui-spec.md:12-23`). The API enforces supplied fields (`server.ts:687-692`), but the browser has no consent control: clicking “Enviar candidata” sends `consent_acknowledged: true` plus a hard-coded phrase automatically (`projects/body-war/app/static/app.js:386-418`). The Playwright test clicks submit without acknowledging any consent surface (`ui.spec.ts:89-96`). | **Observed gap:** server validation is executed, but real affirmative user action is **unverified and absent**. | **must-fix-before-real-friend-test** |
| Live real-Strava activity consult | The module and operation require live, ephemeral Strava activity summaries (`SPEC.md:5-7`; `SPEC.md:69-74`; `operations.md:27-43`). OAuth token exchange exists (`projects/body-war/app/src/auth/strava-oauth.ts:91-159`), but `listActivitySummaries` never calls Strava: it delegates to the repository (`strava-oauth.ts:172-189`), and both repository backends manufacture one fixed synthetic summary (`projects/body-war/app/src/auth/memory-repository.ts:135-147`; `src/auth/drizzle-repository.ts:202-214`). The repository interface can store provider tokens but has no token read/refresh operation (`projects/body-war/app/src/auth/body-war-repository.ts:27-70`). | **Observed gap / real path unverified.** All current API, Postgres, and UI tests explicitly set `BODY_WAR_STRAVA_FAKE=1` (`projects/body-war/app/package.json:13-17`; `playwright.config.ts:18-27`). | **must-fix-before-real-friend-test** |
| Hosted real-person witness | The authoritative blocker closes only when a real Strava run imports and submits without token exposure (`projects/body-war/.craft/ledger.yml:636-653`). The ledger’s current next move is manual hosted deployment followed by real Strava evidence (`ledger.yml:88-94`; `ledger.yml:143-150`). | **Unverified:** no real activity submission receipt exists in the assigned evidence. | **must-fix-before-real-friend-test** |
| Operator review, source-backed geometry, acceptance/rejection, scoring | These are explicitly outside the current build (`SPEC.md:76-81`; `states.md:15-30`; `TEST-SPEC.md:30-40`). Runtime preserves `route_geometry`, scoring, and pilot readiness as not claimed (`projects/body-war/app/server.ts:332-389`). | **Observed and intentionally unimplemented.** | **deferred** |
| BWOI ontology/DomainSpec proof | BWOI proves reproducibility and claim-ceiling preservation for one experimental CT-2 seam only; it does not establish production parity or deployment (`projects/body-war/development/task-sessions/TASK-BWOI-VERIFY/VERIFICATION-REPORT.md:10-15`; `VERIFICATION-REPORT.md:33-46`). The ledger preserves the same ceiling (`projects/body-war/.craft/ledger.yml:1034-1044`). | **Observed receipt:** 11/11 twice and four stable receipt hashes; this is not whole-feature evidence. | **deferred** from prototype completion |
| Planning-state synchronization | The canonical ledger marks the one-go handoff completed and its receipt passed (`projects/body-war/.craft/ledger.yml:879-906`; `ledger.yml:985-1000`), but the feature work-pack still labels `TASK-SGT-ONE-GO` “in-progress” (`projects/body-war/docs/features/parque-taquaral-online-mvp/WORK-PACK.md:53-63`). | **Observed drift.** It does not stop runtime testing but prevents clean “finished” closeout. | **deferred** from local testing; reconcile before declaring feature closed |

## Smallest finish plan for real-friend testing

1. Implement the real Strava activity adapter: retrieve/decrypt the server-held token, refresh it when necessary, call Strava’s athlete activities endpoint, and normalize only the existing `ActivitySummary` allow-list. Keep the current synthetic repository summary strictly behind `BODY_WAR_STRAVA_FAKE=1`.
2. Add a visible per-submission consent control showing the exact stored phrase. Disable submission until affirmative action; never manufacture `consent_acknowledged: true`.
3. Extend tests with a recorded/fake HTTP Strava gateway test, token-expiry/refresh behavior, detail-response assertions, and a Playwright negative test proving no candidate is submitted before consent.
4. Deploy the resulting bytes, run one consented redacted real-Strava submission, preserve a no-secret receipt, and only then close `BLK-STRAVA-ACTIVITY-001`.
5. Reconcile `WORK-PACK.md` with the completed one-go ledger state. Keep operator promotion, source-backed geometry, scoring, and BWOI promotion outside this prototype.

Local fake-Strava usability testing can begin immediately; it should be described as fake-provider prototype testing, not real-Strava or pilot-ready evidence.

## Agent 2 — Alexander, Christopher

## Direct answer

The local fake-Strava prototype is suitable for moderated formative testing after two blocking UX fixes: visible affirmative consent and exact track-to-activity binding. A real participant should not use real Strava data yet: the current UI silently sends consent as `true`, and “Tenho essa corrida” can leave a different route selected. Both are directly observed in current source (`projects/body-war/app/static/app.js:289-295`, `projects/body-war/app/static/app.js:381-418`).

Proof legend: **observed** means current bytes inspected; **executed** means run in this lane; **unverified** means runtime or backend behavior was not inspected. No tests were executed by this explorer. Existing API and browser happy-path tests are present, but execution status is not independently current here (`projects/body-war/app/e2e/body-war-auth.e2e.ts:87-103`, `projects/body-war/app/e2e/troqar-product-architecture/ui.spec.ts:78-97`).

## Ranked defects

### P0 — Consent is asserted by software, not the participant

**Observed.** The contract requires explicit consent and a visible statement that only a redacted summary is stored (`projects/body-war/docs/features/parque-taquaral-online-mvp/operations.md:25-35`, `projects/body-war/docs/features/parque-taquaral-online-mvp/ui-spec.md:12-13`, `projects/body-war/docs/features/parque-taquaral-online-mvp/ui-spec.md:22-23`). The activity UI has only a route selector and submit button; no checkbox, confirmation, or displayed consent statement exists (`projects/body-war/app/static/app.js:381-408`). Submission unconditionally sends `consent_acknowledged: true` and a constant the participant never sees (`projects/body-war/app/static/app.js:9-10`, `projects/body-war/app/static/app.js:413-418`).

Required closure: show the exact storage statement beside an unchecked control, keep submit disabled until affirmative selection, and send `true` only from that selection. Explain the concrete retained fields and exclusions from EC-2/EC-3, not merely “resumo seguro” (`projects/body-war/docs/features/parque-taquaral-online-mvp/operations.md:41-45`). Add a browser test proving unchecked cannot submit and checked consent can.

### P1 — Help does not preserve the route the participant intended

**Observed.** “Tenho essa corrida” only scrolls to `#activities` (`projects/body-war/app/static/app.js:289-295`). Each activity independently creates a selector whose initial value is the first SuggestedTrack, not the track whose Help action was clicked (`projects/body-war/app/static/app.js:381-399`). This permits a confident but wrong-track submission.

The document order worsens this on mobile: recent activities precede SuggestedTrack (`projects/body-war/app/static/index.html:100-147`), although the UI contract places SuggestedTrack after profile and before recent activities (`projects/body-war/docs/features/parque-taquaral-online-mvp/ui-spec.md:3-6`). At 320/390px, tapping Help therefore scrolls backward and loses the route context.

Required closure: reorder SuggestedTrack before activities, bind Help to that track ID, preselect or lock that route in the activity step, move focus to a labelled prompt such as “Escolha um treino para Volta do Taquaral,” and preserve the selection through consent and submission.

### P1 — Duplicate and partial-success submission risk

**Observed at UI level; backend deduplication unverified.** The evidence button is disabled only during the request and always re-enabled afterward (`projects/body-war/app/static/app.js:394-405`). After success, the activity remains actionable; loaded evidence candidates are not used to disable an already-submitted activity/track pair (`projects/body-war/app/static/app.js:413-458`). The inspected interface documents only 201/400/404, with no idempotency or duplicate response (`projects/body-war/docs/features/parque-taquaral-online-mvp/interfaces.md:53-72`).

A more dangerous ambiguity exists if the POST succeeds but either refresh fails: the entire operation enters the error path, the button re-enables, and the participant may retry a mutation that already persisted (`projects/body-war/app/static/app.js:394-420`).

Required closure: enforce backend idempotency or uniqueness for participant + track + activity, disable submitted pairs in the UI, and distinguish “submission accepted; refresh failed” from “submission failed.” A delayed double-click and POST-success/detail-failure test must produce one candidate.

### P2 — Completion and state copy are too indirect

**Observed.** Success has no action-local confirmation or live announcement; the UI reloads distant lists (`projects/body-war/app/static/app.js:413-420`). The submission card says only “enviado - candidato,” while track geometry is rendered as the raw enum `needs_evidence` (`projects/body-war/app/static/app.js:281-287`, `projects/body-war/app/static/app.js:446-458`). The contract requires evidence state and pending geometry/source posture to remain distinct (`projects/body-war/docs/features/parque-taquaral-online-mvp/ui-spec.md:15-23`).

Required closure: announce “Candidata enviada; isto ainda não confirma a geometria da rota,” retain a visible retry-safe success state, translate geometry posture, and expose the candidate count required by the Evidence Summary contract. Current detail loading ignores `evidence_summary` and renders only individual candidates (`projects/body-war/app/static/app.js:430-458`).

### P2 — Error recovery and narrow-screen proof are incomplete

**Observed.** Activity loading has a local error, but submission-detail loading uses uncaught `Promise.all`; a single detail failure bubbles to the global boot handler and changes connection copy rather than offering local retry (`projects/body-war/app/static/app.js:339-358`, `projects/body-war/app/static/app.js:423-485`).

Responsive CSS collapses activity and form layouts below 560px (`projects/body-war/app/static/styles.css:626-671`). The Playwright source checks horizontal bounds at 320/390px, but omits Help, the route selector, error/retry state, and the absent consent control; it also checks only the first matching control and does not prove the Help journey remains contextual or clickable (`projects/body-war/app/e2e/troqar-product-architecture/ui.spec.ts:13-18`, `projects/body-war/app/e2e/troqar-product-architecture/ui.spec.ts:108-130`). Thus 320/390 reachability is partially specified but runtime-unverified in this lane.

## Smallest meaningful local usability test

**Recommendation/inference:** run three moderated 15-minute sessions using fake Strava data, split across 320px and 390px viewports. This is formative evidence, not statistical validation.

Give participants no implementation explanation and ask them to:

1. Find “Volta do Taquaral” and explain “Precisa de evidencia” versus pending geometry.
2. Use “Tenho essa corrida” and select one named recent activity.
3. Explain what will and will not be stored before affirming consent.
4. Submit exactly once and identify whether the route is now proven.
5. Create another suggestion and attach a different activity.
6. Recover from one injected refresh failure without creating a duplicate.

Record task completion, wrong-route selections, consent comprehension, repeat-submit attempts, recovery behavior, and whether every control is reachable at the assigned width. Passing means all participants attach to the intended route, affirm consent knowingly, interpret the result as candidate evidence only, and recover without duplicate submission.

## Unresolved gaps

- Backend uniqueness/idempotency is unverified because repository implementation outside the assigned UI/contracts corpus was not inspected.
- Actual browser rendering, keyboard/screen-reader announcement, and current test-suite results were not executed in this lane.
- Hosted OAuth, deployment security, retention, and real-Strava operational readiness require the operations/security research lane; this UI finding does not establish them.
- Prior memory records the original SuggestedTrack build and full-suite closeout, but that older result may be stale relative to current bytes.

## Agent 3 — Beer, Stafford

## Direct answer

SuggestedTrack is ready for local fake-Strava prototype testing, including the candidate creation and evidence-submission journey. It is not ready for a real-person Strava test: hosted infrastructure, production OAuth, consent evidence, and a receipt covering the actual SuggestedTrack submission are still unverified. The existing ontology/DomainSpec experiment does not authorize deployment, release, or stronger SuggestedTrack claims (`projects/body-war/.craft/ledger.yml:1034-1044`).

Proof labels below mean:

- **Observed**: present in current repository bytes.
- **Executed**: a retained receipt records a prior successful execution; this explorer did not rerun it.
- **Unverified**: only a template, manual, or blocker exists.

## Dependency-ordered readiness map

| Order | Owner / action | Proof status | Evidence and exit condition |
|---|---|---|---|
| 1 | **Application:** preserve the bounded prototype claim. SuggestedTrack may become `evidence_submitted`; this does not prove geometry or scoring. | **Executed locally** | The retained one-go receipt records validation, managed-Postgres e2e, UI tests, and scoped checks as PASS, while keeping real activity and source-backed geometry open (`projects/body-war/.craft/ledger.yml:985-1000`). |
| 2 | **Application:** add or prove an explicit, affirmative consent interaction before a person submits an activity. Add a negative browser/API test showing submission is rejected when consent is absent. | **Unverified gap** | The API e2e sends `consent_acknowledged: true` and consent text (`projects/body-war/app/e2e/body-war-auth.e2e.ts:87-103`), but the browser journey clicks submit without exercising a consent control (`projects/body-war/app/e2e/troqar-product-architecture/ui.spec.ts:78-97`). This evidence therefore does not prove meaningful in-product consent. |
| 3 | **Operator-private:** select the stable host, point DNS, confirm Traefik network/entrypoint/resolver names, create the server-owned env and secrets, and configure the Strava callback domain. | **Unverified / blocked** | Required host inputs are listed at `projects/body-war/docs/ONLINE-DEPLOY-MANUAL.md:16-21`; private values and file protection at `:75-109`; callback-domain rules at `:111-129`. The current blocker explicitly names DNS, env, callback, and Traefik values at `:270-277`. Agents must not receive or print production secrets (`:10-14`). |
| 4 | **Operator-private:** perform the first manual deploy, including Postgres startup, migrations, and app startup. | **Unverified** | The first-deploy commands are specified at `projects/body-war/docs/ONLINE-DEPLOY-MANUAL.md:238-250`. The retained task session is `BLOCK`: local harness validation passed, but the real VPS still requires operator-private configuration (`projects/body-war/development/task-sessions/20260622T140208Z-traefik-secret-blind-deploy/TASK-SESSION-RESULT.md:1-15`). |
| 5 | **Safe agent after operator completion:** run the public online smoke against the selected HTTPS host. | **Observed script; hosted execution unverified** | The script checks `/api/status`, the `Bora correr` page marker, and absence of obvious token terms (`projects/body-war/infra/scripts/smoke-online.sh:4-24`). The manual requires this only after deploy (`projects/body-war/docs/ONLINE-DEPLOY-MANUAL.md:131-143`). |
| 6 | **Operator + safe observer:** complete hosted Strava login with an operator-owned account first and fill the deployment receipt without secrets. | **Unverified** | The hosted login checks are callback return, profile, public profile link, and no tokens (`projects/body-war/docs/ONLINE-DEPLOY-MANUAL.md:145-158`). The receipt additionally requires route, status, callback, login start, connected profile, CSRF, and secret-scan evidence (`projects/body-war/infra/deployment-receipts/TEMPLATE.md:10-20`). The identity choice remains open; operator account, consented friend, or skipped activity are the named options (`projects/body-war/development/task-sessions/20260622T140208Z-traefik-secret-blind-deploy/TASK-SESSION-RESULT.md:78-87`). |
| 7 | **Participant/operator-private:** obtain explicit consent before using a friend’s activity; keep identity mapping and raw evidence outside tracked artifacts. | **Unverified; template blank** | The template is explicitly blank and forbids tracked private details without agreement (`projects/body-war/docs/validation/FRIEND-ACTIVITY-CONSENT-TEMPLATE.md:1-7`). It bounds use to connection and redacted import, excludes route proof/scoring/publication, and provides revocation (`:9-19`); explicit confirmation is required (`:21-30`). |
| 8 | **Evidence check:** import one real activity and produce a redacted import receipt. | **Unverified** | The receipt must omit tokens, raw payloads, maps, and notes and retain `route_geometry: not_claimed` and `scoring: not_claimed` (`projects/body-war/docs/validation/ACTIVITY-IMPORT-RECEIPT.md:6-31`). Forbidden tracked fields include tokens, OAuth codes, raw payloads, maps, and unconsented friend data (`:48-56`). |
| 9 | **Evidence check:** submit that imported activity to a SuggestedTrack and retain a separate redacted submission witness. | **Unverified; receipt-shape gap** | The active blocker closes only when a real Strava run both imports **and submits** without token exposure (`projects/body-war/.craft/ledger.yml:636-653`). The current activity receipt supports only “activity import works” (`projects/body-war/docs/validation/ACTIVITY-IMPORT-RECEIPT.md:58-61`), while the deployment receipt stops at login/profile/CSRF (`projects/body-war/infra/deployment-receipts/TEMPLATE.md:10-20`). A bounded submission receipt must therefore record the candidate selector or redacted ID, before/after status, consent handle, response result, and leak scan without private payloads. |

## What can be tested locally now

- Fake-Strava API flow with managed Postgres: `npm run e2e:all`; the package binds fake Strava to the Postgres e2e path (`projects/body-war/app/package.json:10-16`), and the harness starts, tests, then removes the disposable database (`projects/body-war/app/scripts/e2e.sh:6-10`, `:23-57`).
- Browser usability with fake Strava and memory auth: `npm run test:ui` (`projects/body-war/app/package.json:17-18`; `projects/body-war/app/playwright.config.ts:18-30`).
- The browser suite covers login-first UI, safe profile/activity rendering, SuggestedTrack creation, evidence submission, logout, and 320/390px reachability (`projects/body-war/app/e2e/troqar-product-architecture/ui.spec.ts:20-131`).

These paths are **currently observed and previously executed**, not re-executed by this read-only lane. The deploy task session retained local build/runtime smoke PASS (`projects/body-war/development/task-sessions/20260622T140208Z-traefik-secret-blind-deploy/TASK-SESSION-RESULT.md:51-62`).

## Exact real-person stop conditions

Do not begin friend testing if any of these is true:

1. DNS/TLS, server env, Traefik names, or Strava callback remain unresolved.
2. The hosted deployment receipt has not passed route, status, OAuth/profile, CSRF, and secret-scan checks.
3. Explicit participant consent for the exact use and storage boundary is absent.
4. The product does not present or prove affirmative consent before evidence submission.
5. Any token, OAuth code, raw payload, map/polyline, note, private URL, or unapproved identity data would enter logs or tracked artifacts.
6. There is no redacted witness for both real activity import and SuggestedTrack submission.
7. The test result would be described as source-backed geometry, scoring authority, pilot-ready, production-ready, promoted, or released. The Craft view keeps those claims outside the completed prototype (`projects/body-war/CRAFT.md:46-55`, `:199-205`).

The Inventory entry is discovery-only: it says Body War application authority remains in `projects/body-war/` and explicitly denies production authority (`.arcanum/inventory/entries/domainspec-v2-fpr02-integrated-consumer-proof-refresh.md:49-57`).
