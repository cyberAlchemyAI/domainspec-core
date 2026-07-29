# Candidate Synthesis

## 1. One-sentence answer

The current bytes support unmoderated developer testing of the fake-Strava prototype now; the smallest honest gate for moderated local participant testing is visible affirmative consent plus exact Help-to-track binding, while a hosted real-friend test additionally requires retry-safe submission, a real Strava activity adapter, operator-private deployment/OAuth work, external consent, and redacted import-and-submission receipts.

## 2. Prototype frontier

| Frontier | Exact scope |
|---|---|
| **test-now** | Unmoderated developer/expert testing with fake Strava: login, list/create SuggestedTrack, inspect detail, attach the synthetic activity, confirm `needs_evidence → evidence_submitted`, and exercise memory/Postgres/browser paths. Existing receipts record 3/3 Node, managed-Postgres, and 7/7 Playwright success, but this synthesis did not rerun them. |
| **must-fix-before-moderated-local-participant-test** | **(a)** Display the exact retention statement beside an unchecked affirmative-consent control; disable submission until checked and derive `consent_acknowledged` from that action. **(b)** Bind “Tenho essa corrida” to the clicked track ID, carry that track into the activity step, label/focus the prompt, and preselect or lock the intended track at 320/390px. This resolves the explorers’ apparent conflict: developer testing may start now, but a participant should not be asked to interpret or exercise a journey that silently asserts consent or can submit to the wrong route. |
| **must-fix-before-hosted-real-friend-test** | Enforce participant+track+activity idempotency and distinguish mutation success from refresh failure; implement server-side token read/decrypt/refresh and a real Strava athlete-activities gateway with the existing allow-list; retain synthetic activity only behind `BODY_WAR_STRAVA_FAKE=1`; complete DNS/TLS, server env, Traefik, callback and deploy privately; pass public smoke and hosted OAuth checks; obtain external consent; execute one real import and SuggestedTrack submission; preserve separate redacted receipts and a leak scan. |
| **defer** | Source-backed geometry, operator accept/reject, scoring, promotion, pilot/production readiness, and broader BWOI authority. A direct detail-payload assertion, translated state/count copy, local retry UX, accessibility execution, UI/spec ordering decision, and work-pack/ledger synchronization are valuable hardening/closeout but do not block the first narrowly moderated fake-provider session once consent and binding are fixed. |

The first moderated session must exclude injected refresh-failure recovery from its pass criterion until idempotency is closed; it may record repeat-submit behavior as discovery, not claim retry safety.

## 3. Smallest bounded implementation SWUs

### SWU-LP-01 — Participant-safe local journey

Scope: visible exact consent statement and unchecked control; request derives consent from the control; Help carries the clicked track ID; intended route remains selected through submit; contextual prompt/focus works at 320/390px; add negative and positive browser assertions.

Acceptance:

```sh
cd projects/body-war/app
npm run validate
npm test
npm run test:ui
```

Observable criteria: unchecked consent cannot issue the POST; the clicked track is the submitted track; checked consent submits exactly one candidate in the happy path; controls remain reachable at 320px and 390px.

### SWU-RF-01 — Retry-safe evidence submission

Scope: backend uniqueness/idempotency for principal+track+activity, stable duplicate response, submitted-pair UI state, and separate “accepted but refresh failed” handling.

Acceptance:

```sh
cd projects/body-war/app
npm run validate
npm test
npm run e2e:all
npm run test:ui
```

Observable criteria: delayed double-click and POST-success/detail-failure scenarios leave exactly one evidence candidate and do not invite an unsafe retry.

### SWU-RF-02 — Real Strava activity boundary

Scope: server-only token retrieval/decryption, expiry refresh, Strava athlete-activities call, normalization to the existing `ActivitySummary` allow-list, no raw payload persistence, and synthetic activity reachable only when fake mode is explicit.

Acceptance:

```sh
cd projects/body-war/app
npm run validate
npm test
npm run e2e:all
```

Add deterministic gateway tests for success, token refresh, provider failure, allow-listing, and fake/real mode separation. These commands prove adapter behavior against controlled HTTP evidence, not a live account.

### SWU-OPS-01 — Hosted operator bring-up

Scope: operator selects host, DNS, Traefik values, protected env/secrets and callback; performs first deploy and migration; safe observer runs public smoke and records the deployment receipt.

Acceptance after operator-private setup:

```sh
bash projects/body-war/infra/scripts/smoke-online.sh https://HOST
```

The exact host is operator-supplied; no production secret enters agent context or tracked output.

### SWU-EVIDENCE-01 — Consented real-friend witness

Scope: blank-template consent completed outside tracked identity data; one real activity imported and attached to one SuggestedTrack; deployment, import and submission receipts remain redacted and preserve all claim ceilings.

Acceptance:

```sh
! rg -n 'access_token|refresh_token|authorization_code|raw_payload|polyline' \
  projects/body-war/infra/deployment-receipts \
  projects/body-war/docs/validation
```

This scan is necessary but insufficient: the parent must also inspect the filled receipt selectors, before/after status, consent handle and hosted response result.

## 4. Local test protocol

### Test-now developer pass

Run the four acceptance commands from SWU-LP-01 plus `npm run e2e:all`; manually exercise fake login, seeded track detail, new suggestion, synthetic activity attachment and evidence readback. Record defects only as fake-provider/local findings.

### First moderated participant pass, after SWU-LP-01

Run three 15-minute formative sessions split across 320px and 390px. Give no implementation explanation. Ask each participant to:

1. Find “Volta do Taquaral” and explain evidence status versus geometry status.
2. Use “Tenho essa corrida.”
3. Identify the intended route and named activity.
4. Explain what is and is not retained before checking consent.
5. Submit once and explain whether the route is now proven.
6. Create a second suggestion and attach a different synthetic activity.

Record intended-route accuracy, consent comprehension, single-submit behavior, candidate-only interpretation and control reachability. Passing permits another formative fake-provider round only; it does not prove accessibility, retry safety, real Strava, hosting or pilot readiness.

## 5. Hosted dependency and owner route

1. **Application owner:** close SWU-LP-01, SWU-RF-01 and SWU-RF-02.
2. **Test executor:** rerun validation, Node, managed-Postgres and Playwright suites; retain current receipts.
3. **Operator-private owner:** configure stable host, DNS/TLS, Traefik, protected env/secrets and Strava callback; deploy and migrate.
4. **Safe agent/observer:** run public smoke; inspect public status/page/token-term checks; never handle secrets.
5. **Operator account first:** complete hosted OAuth/profile/CSRF checks and the deployment receipt.
6. **Participant/operator-private owner:** obtain consent for the exact import, retention and revocation boundary.
7. **Evidence owner:** import one real activity, attach it to SuggestedTrack, capture separate redacted import and submission witnesses, and run the leak scan.
8. **Parent authority:** inspect receipts and decide whether `BLK-STRAVA-ACTIVITY-001` closes. No other promotion follows automatically.

Stop if any infrastructure input, product consent, real adapter, external consent, receipt field, or leak check is unresolved.

## 6. Claim ceilings

- Local fake-provider execution is not live-Strava proof.
- Prior retained test success is not a current rerun.
- Moderated formative usability is not accessibility validation or statistical usability evidence.
- Managed-Postgres execution is not hosted deployment.
- Real activity import is not SuggestedTrack submission unless both have separate witnesses.
- `evidence_submitted` means candidate evidence only; it does not establish geometry, route truth, scoring or acceptance.
- Hosted friend testing is not pilot-ready, production-ready, promoted or released.
- BWOI reproducibility covers its bounded experimental seam, not whole-feature or deployment authority.
- Inventory is discovery-only; current Body War bytes and receipts are load-bearing.

## 7. Cited-synthesis evidence matrix

| Claim ID | Immutable source identity | Source-local selector | Explorer return | Evidence scope | Proof status |
|---|---|---|---|---|---|
| C1 | `projects/body-war/app/server.ts`; `projects/body-war/app/tests/auth-consumer.test.ts` | `server.ts:560-725`; `auth-consumer.test.ts:15-144` | Agent 1, “implemented-versus-specified gap matrix,” list/create and candidate-attach rows | Fake-provider API, auth, CSRF, create, attach and state boundary | **executed** |
| C2 | `projects/body-war/development/task-sessions/20260629T061500Z-suggested-track-one-go-build/TASK-SESSION-RESULT.md`; `projects/body-war/app/e2e/troqar-product-architecture/ui.spec.ts` | result `:21-29`; UI spec `:78-130` | Agent 1, browser-loop row; Agent 3, “What can be tested locally now” | Retained Postgres/browser execution and narrow-width assertions; not rerun here | **executed** |
| C3 | `projects/body-war/app/static/app.js`; `projects/body-war/docs/features/parque-taquaral-online-mvp/operations.md` | `app.js:386-418`; operations `:25-45` | Agent 1, “Affirmative browser consent”; Agent 2, “P0” | Browser manufactures consent while contract requires explicit consent | **observed** |
| C4 | `projects/body-war/app/static/app.js`; `projects/body-war/app/static/index.html`; `projects/body-war/docs/features/parque-taquaral-online-mvp/ui-spec.md` | `app.js:289-295,381-399`; HTML `:100-147`; UI spec `:3-6` | Agent 2, “P1 — Help does not preserve…” | Help loses clicked-track context and mobile ordering worsens the ambiguity | **observed** |
| C5 | `projects/body-war/app/static/app.js`; `projects/body-war/docs/features/parque-taquaral-online-mvp/interfaces.md` | `app.js:394-420,413-458`; interfaces `:53-72` | Agent 2, “P1 — Duplicate and partial-success…” | UI permits retry ambiguity; backend idempotency contract was not established | **unverified** |
| C6 | `projects/body-war/app/src/auth/strava-oauth.ts`; `projects/body-war/app/src/auth/memory-repository.ts`; `projects/body-war/app/src/auth/drizzle-repository.ts`; `projects/body-war/app/package.json` | OAuth `:172-189`; memory `:135-147`; Drizzle `:202-214`; package `:13-17` | Agent 1, “Live real-Strava activity consult” | Current activity summaries are synthetic and all admitted tests select fake mode | **observed** |
| C7 | `projects/body-war/docs/ONLINE-DEPLOY-MANUAL.md`; `projects/body-war/development/task-sessions/20260622T140208Z-traefik-secret-blind-deploy/TASK-SESSION-RESULT.md` | manual `:16-21,75-158,238-277`; result `:1-15` | Agent 3, readiness orders 3–6 | Hosted DNS/env/Traefik/callback/deploy/OAuth work remains operator-bound | **unverified** |
| C8 | `projects/body-war/.craft/ledger.yml`; `projects/body-war/docs/validation/ACTIVITY-IMPORT-RECEIPT.md`; `projects/body-war/docs/validation/FRIEND-ACTIVITY-CONSENT-TEMPLATE.md` | ledger `:636-653`; import receipt `:6-31,48-61`; consent `:1-30` | Agent 3, readiness orders 7–9 | Blocker needs real import and submission; existing templates do not yet witness either | **unverified** |
| C9 | `projects/body-war/docs/features/parque-taquaral-online-mvp/SPEC.md`; `projects/body-war/docs/features/parque-taquaral-online-mvp/states.md`; `projects/body-war/app/server.ts` | spec `:76-81`; states `:15-30`; server `:332-389` | Agent 1, “Operator review…” | Geometry, scoring, acceptance and pilot readiness are explicitly outside the prototype | **observed** |
| C10 | `projects/body-war/.craft/ledger.yml`; `projects/body-war/docs/features/parque-taquaral-online-mvp/WORK-PACK.md` | ledger `:879-906,985-1000`; work-pack `:53-63` | Agent 1, “Planning-state synchronization” | Runtime-testing readiness and planning closeout are distinct; projection is stale | **observed** |

## 8. Unresolved evidence and typed repair owners

| Evidence row | Unresolved point | Typed repair owner | Closure evidence |
|---|---|---|---|
| U1 | Current-head validation/Postgres/Playwright status was not rerun by explorers. | **test executor** | Fresh command outputs and retained receipt for `validate`, `test`, `e2e:all`, `test:ui` |
| U2 | Backend uniqueness/idempotency is not established. | **application repository/schema owner** | Constraint/operation proof plus duplicate and partial-success tests |
| U3 | Detail payload fields and `evidence_summary` lack a focused current assertion. | **API test owner** | Direct response assertions for owned candidates, redacted count and non-claims |
| U4 | Actual keyboard/screen-reader behavior and live 320/390 Help/consent journey were not executed. | **UX/accessibility test owner** | Browser execution receipt including focus, announcement and contextual selection |
| U5 | Real token read/refresh and live activity normalization do not exist in current evidence. | **Strava adapter owner** | Deterministic gateway tests, then operator-owned hosted witness |
| U6 | DNS, TLS, protected env, Traefik and callback values remain unknown by design. | **deployment operator** | Secret-free deployment receipt and passing public smoke |
| U7 | No receipt shape currently covers the real SuggestedTrack submission itself. | **evidence/receipt owner** | Redacted submission receipt with candidate selector, before/after status, consent handle, response and leak scan |
| U8 | Participant consent is still a blank template and no real-person action is authorized. | **participant plus operator-private consent owner** | Explicit bounded consent handle kept without tracked private identity data |
