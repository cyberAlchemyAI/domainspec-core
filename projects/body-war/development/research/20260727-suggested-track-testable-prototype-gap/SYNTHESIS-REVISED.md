# Revised SuggestedTrack Prototype Frontier

## 1. One-Sentence Answer

At commit `b7d60c96d5ace267f5aed8eb9921756aad1f66d3`, the
fake-provider local path is current-executed and open for developer testing
now; moderated local participation waits for the consent-and-route-binding
gate, while one supervised hosted real-Strava witness may be admitted after the
real adapter, immutable deployment identity, operator rehearsal, exact external
consent, and receipt-schema prevalidation—without making retry, repeat,
unmoderated, geometry, scoring, or release claims.

## 2. Research-Local Frontier Labels

These labels classify the research recommendation only. They are not Craft
states, promotion states, deployment authority, or release decisions.

| Research-local label | Exact boundary |
|---|---|
| `current-executed-local-developer-path` | Fake-provider local execution by developers/researchers. At the named commit, the scoped app worktree was clean; validation passed; Node passed 3/3; disposable local Docker Postgres e2e passed and cleaned up; Playwright passed 7/7. Existing tests still exercise manufactured consent and manual track selection, so this evidence does not admit participant testing. |
| `admit-moderated-local-participant-test` | Opens only after LP-01 proves displayed, affirmed, transmitted, and persisted consent-text identity plus exact Help-to-track binding. It admits three supervised fake-provider formative sessions, not unmoderated use. |
| `admit-hosted-supervised-single-witness` | Opens only after LP-01, RF-02, immutable deployed-artifact identity, `fake_mode: false`/real-adapter attestation, operator deploy/OAuth rehearsal, exact external consent for one named SuggestedTrack attachment, structurally prevalidated receipt forms, and a one-attempt/no-retry protocol. |
| `single-witness-execution-and-closure` | The participant performs one real OAuth/activity selection/affirmation/submission attempt. The real import, submission, and filled receipts are outputs of this stage, not admission prerequisites. Parent closure requires the exact passing threshold below. |
| `must-fix-before-hosted-repeat-or-unmoderated-testing` | RF-01 idempotency and partial-success recovery are mandatory before any hosted retry-capable or repeat use. This research does not admit unmoderated participant use, even after RF-01. |
| `defer` | Source-backed geometry, operator accept/reject, scoring, promotion, pilot, production, release, broader BWOI authority, and work-pack synchronization remain outside this prototype frontier. |

## 3. Exact Frontier Matrix

| Item | Current local developer | Moderated local participant | Hosted supervised single witness | Hosted repeat/retry or unmoderated | Deferred |
|---|---:|---:|---:|---:|---:|
| Fake login, list/create/detail, and synthetic evidence attach | **Current-executed** | Available after LP-01 | Not live-provider proof | Not sufficient | — |
| Visible affirmative consent with concrete retained fields/exclusions | Existing implementation fails | **LP-01 gate** | **Required** | **Required** | — |
| Displayed/affirmed/submitted/persisted consent-text equality | Unproven | **LP-01 gate** | **Required** | **Required** | — |
| Help on a non-first track preserves exact track through submission | Existing implementation fails | **LP-01 gate** | **Required** | **Required** | — |
| Real token read/refresh and Strava activity gateway | Synthetic only | Not needed | **RF-02 gate** | **Required** | — |
| Immutable deployed-artifact identity and `fake_mode: false` attestation | Not hosted evidence | Not needed | **Admission gate** | **Required** | — |
| Operator deploy/OAuth rehearsal | Not hosted evidence | Not needed | **Admission gate** | **Required** | — |
| External consent for one named track-candidate attachment | Not applicable | Fake data only | **Admission gate** | **Required** | — |
| Structurally prevalidated import/submission receipt schemas | Templates incomplete for submission | Not needed | **Admission gate** | **Required** | — |
| Real import, one submission, and filled receipts | Not applicable | Not applicable | **Produced during execution** | Required evidence | — |
| Idempotency and partial-success recovery | Unverified | Not required for first supervised formative round under no-retry rule | Not required for the one-attempt witness | **RF-01 gate** | — |
| Source-backed geometry, scoring, promotion, pilot/production/release | No claim | No claim | No claim | No claim | **Yes** |
| Work-pack/ledger synchronization | Runtime unaffected | Runtime unaffected | Runtime unaffected | Runtime unaffected | **Closeout only** |

## 4. Bounded SWUs And Acceptance Surfaces

### LP-01 — Moderated-Local Consent-And-Binding Gate

Scope:

- Display the exact consent statement before affirmation.
- Name the concrete retained allow-listed activity fields and excluded
  raw/private fields.
- Start unchecked and issue zero submission POSTs while unchecked.
- Derive `consent_acknowledged` from the participant's action.
- Prove the displayed text, submitted `consent_statement`, and persisted
  statement are byte-identical or canonically equal under an explicit
  deterministic rule.
- From Help on a non-first SuggestedTrack, carry that exact track identity into
  the activity step.
- Focus a labelled prompt, preserve the selection through consent/submission,
  and prove it at 320px and 390px.
- Checked submission issues exactly one POST and persists exactly one candidate
  in the normal happy path.

Acceptance:

```sh
cd projects/body-war/app
npm run validate
npm test
npm run e2e:all
npm run test:ui
```

Required browser witness: non-first-track Help → correct focused selection at
320/390 → zero POST unchecked → exact consent text affirmed → exactly one POST
checked → submitted candidate references that same track.

### RF-02 — Real Strava Activity Boundary

Scope:

- Server-only token retrieval/decryption and refresh.
- Real Strava athlete-activities call.
- Normalize only the current `ActivitySummary` allow-list.
- Persist no raw provider payload.
- Synthetic activity remains available only under explicit fake mode.
- Produce a redacted runtime signal or operator attestation that the hosted
  witness ran with `fake_mode: false` and the real adapter selected.

Acceptance:

```sh
cd projects/body-war/app
npm run validate
npm test
npm run e2e:all
npm run test:ui
```

Tests must cover gateway success, refresh, provider failure, allow-listing, and
fake/real separation. These controlled tests do not themselves prove a live
account.

### HOST-01 — Supervised Single-Witness Admission Package

Scope:

- Freeze the deployed source commit and container/artifact digest.
- Operator completes deploy and OAuth rehearsal without sharing secrets.
- External consent explicitly names the one SuggestedTrack and permits one
  activity import plus one candidate attachment.
- Define machine-checkable import and submission receipt schemas.
- Prevalidate blank/redacted forms before participant execution.
- Freeze a one-attempt/no-retry protocol.
- Define operator-side secret-value and private-log inspection that emits only
  a redacted pass/fail result.

Proposed acceptance interface, to be implemented by this SWU rather than
presumed current:

```sh
git rev-parse HEAD
git status --short -- projects/body-war/app
docker image inspect --format '{{.Id}}' BODY_WAR_IMAGE
node projects/body-war/infra/scripts/validate-hosted-witness-receipts.cjs \
  --schema-only \
  --import projects/body-war/docs/validation/ACTIVITY-IMPORT-RECEIPT.json \
  --submission projects/body-war/docs/validation/SUGGESTED-TRACK-SUBMISSION-RECEIPT.json
bash projects/body-war/infra/scripts/smoke-online.sh https://HOST
```

Admission receipt must bind commit, artifact ID, host, callback rehearsal,
`fake_mode: false`, real-adapter signal, exact consent handle, receipt-schema
versions, and the frozen no-retry protocol.

### WITNESS-01 — One Supervised Real-Strava Execution

This is execution and evidence closure, not a pre-test implementation gap.

Participant actions:

1. Complete OAuth.
2. Select the one consented activity.
3. Verify the one named SuggestedTrack.
4. Read and affirm the displayed consent.
5. Submit once.

Operator-private owner handles deployment, secrets, private provider state, and
private readback. Safe observer performs public smoke only. Evidence validator
receives redacted receipts only.

Passing threshold requires all of:

- Pre-state is `needs_evidence`.
- `fake_mode` is false and real-adapter signal is present.
- Activity, participant/session, and SuggestedTrack identities match the
  consent and receipt bindings.
- Exactly one submission POST occurs.
- Response is successful.
- Post-state is `evidence_submitted`.
- Candidate count increases by exactly one.
- Displayed, affirmed, transmitted, and persisted consent identities match.
- Import and submission receipts pass structural validation.
- Operator-side scan reports zero forbidden secret/private values, exposing
  only the redacted result.

If any identity, response, count, state, consent, or receipt result is
ambiguous, stop without retry. The witness is inconclusive and the blocker
remains open.

Structural validation:

```sh
node projects/body-war/infra/scripts/validate-hosted-witness-receipts.cjs \
  --import REDACTED_IMPORT_RECEIPT \
  --submission REDACTED_SUBMISSION_RECEIPT
```

A self-matching repository grep is not a secret-leak proof. The operator
performs the secret-value/log scan privately and returns only its redacted
verdict.

### RF-01 — Hosted Repeat/Retry Safety Gate

Scope:

- Enforce principal+track+activity uniqueness/idempotency.
- Return a stable duplicate result.
- Disable already-submitted pairs.
- Distinguish “mutation accepted; refresh failed” from mutation failure.
- Prove delayed double-click and accepted-POST/failed-refresh scenarios leave
  one candidate.

Acceptance:

```sh
cd projects/body-war/app
npm run validate
npm test
npm run e2e:all
npm run test:ui
```

RF-01 is not required for WITNESS-01 because that witness is supervised,
one-attempt, and stop-without-retry. It is mandatory before hosted repeat or
retry-capable use. No unmoderated use is admitted by this research.

## 5. Moderated Local Protocol

After LP-01, run exactly three supervised 15-minute sessions across 320px and
390px using fake-provider data.

Ask each participant to:

1. Find a non-first SuggestedTrack and use its Help action.
2. Identify the route and named activity now selected.
3. State every displayed retained-field category and exclusion in their own
   words.
4. Affirm consent deliberately.
5. Submit once.
6. Explain whether the candidate proves the route geometry.
7. Create another suggestion without reusing the first evidence pair.

Admission threshold is **3/3** for every criterion:

- Intended non-first track remains selected.
- Participant identifies retained fields and exclusions correctly.
- Consent is visibly deliberate.
- Exactly one POST occurs.
- Candidate attaches to the intended track.
- Participant states that submission is candidate evidence, not geometry
  proof.
- Required controls remain reachable at the assigned width.

The moderator stops immediately on consent ambiguity, route ambiguity, or any
apparent partial success. No participant retries. A stopped session is
inconclusive, not a failure the participant should repair.

## 6. Hosted Dependency And Ownership Route

### Admission

1. **Application owner:** close LP-01 and RF-02.
2. **Test executor:** rerun all four local commands against the frozen commit.
3. **Build/deploy owner:** record commit and immutable image/artifact ID.
4. **Operator-private owner:** configure DNS/TLS, protected env, Traefik, and
   callback; deploy; rehearse OAuth with an operator-owned account; privately
   verify real mode.
5. **Safe observer:** run public smoke only.
6. **Participant plus operator-private consent owner:** bind consent to one
   named SuggestedTrack candidate attachment.
7. **Evidence validator:** structurally prevalidate blank import/submission
   receipts.
8. **Parent:** admit or reject WITNESS-01.

### Execution And Closure

1. **Participant:** OAuth, select, affirm, and submit once.
2. **Operator-private owner:** observe private state/readback and perform
   secret-value/log inspection.
3. **Safe observer:** repeat public smoke if required.
4. **Evidence validator:** validate redacted filled receipts.
5. **Parent:** compare the exact threshold and decide whether
   `BLK-STRAVA-ACTIVITY-001` closes.

No automatic retry occurs. No geometry, scoring, promotion, or release decision
follows.

## 7. Claim Ceilings

- Research-local frontier labels are not lifecycle or promotion states.
- Current execution proves only the named commit's local fake-provider paths.
- Disposable local Docker Postgres is not managed infrastructure or hosted
  deployment.
- Passing tests that manufacture consent do not prove participant consent.
- Moderated 3/3 formative completion is not statistical usability or
  accessibility validation.
- A real import is not a SuggestedTrack submission; both need separate redacted
  witnesses.
- One supervised witness does not prove retry safety, repeatability, or
  unmoderated suitability.
- `evidence_submitted` means candidate evidence only.
- No result establishes source-backed geometry, scoring authority, operator
  acceptance, pilot readiness, production readiness, promotion, release, or
  shipment.
- BWOI evidence remains bounded to its experimental seam.
- Inventory remains discovery-only.
- Work-pack drift remains deferred closeout, not runtime evidence.

## 8. Revised Cited-Synthesis Evidence Matrix

All current-byte identities below are bound to commit
`b7d60c96d5ace267f5aed8eb9921756aad1f66d3`.

| Claim ID | Immutable source identity | Selector | Origin and explorer reference | Evidence scope | Proof |
|---|---|---|---|---|---|
| C1 | `projects/body-war/app@b7d60c96…` | scoped clean status; `npm run validate`; `npm test`; `npm run e2e:all`; `npm run test:ui` | **Parent current-head execution, 2026-07-27**; corroborates Agent 1 list/create rows and Agent 3 “What can be tested locally now” | Current fake-provider local paths; Node 3/3, disposable Docker Postgres e2e, Playwright 7/7 | **executed** |
| C2 | `projects/body-war/app/static/app.js@b7d60c96…`; `projects/body-war/app/e2e/troqar-product-architecture/ui.spec.ts@b7d60c96…` | app `:386-418`; UI test `:89-96` | Agent 1 “Affirmative browser consent”; Agent 2 “P0”; Agent 3 readiness order 2 | Software manufactures consent and passing UI test does not exercise affirmation | **observed** |
| C3 | `projects/body-war/docs/features/parque-taquaral-online-mvp/operations.md@b7d60c96…` | `:25-45` | Agent 1 consent row; Agent 2 “P0” | Contract requires explicit consent and retained/excluded-data boundary | **observed** |
| C4 | `projects/body-war/app/static/app.js@b7d60c96…`; `projects/body-war/app/static/index.html@b7d60c96…` | app `:289-295,381-399`; HTML `:100-147` | Agent 2 “P1 — Help does not preserve…” | Help loses clicked-track context; selectors default independently | **observed** |
| C5 | `projects/body-war/app/src/auth/strava-oauth.ts@b7d60c96…`; `memory-repository.ts@b7d60c96…`; `drizzle-repository.ts@b7d60c96…`; `package.json@b7d60c96…` | OAuth `:172-189`; memory `:135-147`; Drizzle `:202-214`; package `:13-17` | Agent 1 “Live real-Strava activity consult” | Current activity path is synthetic and tests explicitly select fake mode | **observed** |
| C6 | `projects/body-war/app/static/app.js@b7d60c96…`; `interfaces.md@b7d60c96…` | app `:394-420,413-458`; interfaces `:53-72` | Agent 2 “Duplicate and partial-success submission risk” | Retry ambiguity exists; backend idempotency is not established | **unverified** |
| C7 | `projects/body-war/docs/ONLINE-DEPLOY-MANUAL.md@b7d60c96…`; `TASK-SESSION-RESULT.md@b7d60c96…` | manual `:16-21,75-158,238-277`; result `:1-15` | Agent 3 readiness orders 3–6 | Hosted infrastructure and OAuth rehearsal remain operator-bound and unexecuted | **unverified** |
| C8 | `projects/body-war/docs/validation/FRIEND-ACTIVITY-CONSENT-TEMPLATE.md@b7d60c96…` | `:1-30` | Agent 3 readiness order 7 | Consent template is blank and must be narrowed to the named one-shot attachment | **unverified** |
| C9 | `projects/body-war/docs/validation/ACTIVITY-IMPORT-RECEIPT.md@b7d60c96…`; `infra/deployment-receipts/TEMPLATE.md@b7d60c96…` | import `:6-31,48-61`; deploy `:10-20` | Agent 3 readiness orders 8–9 | Import template exists; current receipt set lacks a structurally validated SuggestedTrack-submission witness | **unverified** |
| C10 | `projects/body-war/.craft/ledger.yml@b7d60c96…`; `memory-repository.ts@b7d60c96…`; `drizzle-repository.ts@b7d60c96…` | ledger `:636-653`; memory `:192-218`; Drizzle `:266-295` | Agent 1 candidate-attach row; Agent 3 readiness order 9 | Closure requires real import and submission; repository transition target is `evidence_submitted` | **observed** |
| C11 | `projects/body-war/docs/features/parque-taquaral-online-mvp/queries.md@b7d60c96…`; `server.ts@b7d60c96…` | queries `:19-36`; server `:640-669,374-389` | Agent 1 detail/readback row | Candidate count/readback and non-claims can anchor the one-witness threshold, but the exact live witness is absent | **unverified** |
| C12 | `SPEC.md@b7d60c96…`; `states.md@b7d60c96…`; `server.ts@b7d60c96…` | spec `:76-81`; states `:15-30`; server `:332-389` | Agent 1 “Operator review…” | Geometry, scoring, acceptance, and pilot readiness remain intentionally outside | **observed** |
| C13 | `projects/body-war/.craft/ledger.yml@b7d60c96…`; `WORK-PACK.md@b7d60c96…` | ledger `:879-906,985-1000`; work-pack `:53-63` | Agent 1 “Planning-state synchronization” | Work-pack projection is stale but does not block runtime testing | **observed** |

## 9. Unresolved Evidence And Typed Repair Owners

| ID | Boundary | Unresolved evidence | Typed repair owner | Closure |
|---|---|---|---|---|
| U1 | **Bound: moderated-local admission** | Displayed/affirmed/transmitted/persisted consent equality and non-first-track Help witness do not exist. | Application/UI and browser-test owner | LP-01 tests and 3/3 supervised threshold |
| U2 | **Bound: hosted admission** | Real token read/refresh, gateway, and `fake_mode: false` signal are absent. | Application auth/token-repository plus Strava adapter owners | RF-02 controlled tests and redacted hosted-mode attestation |
| U3 | **Bound: hosted admission** | Deployed artifact lacks a frozen commit+image identity in current evidence. | Build/deploy owner | Immutable identity recorded in admission receipt |
| U4 | **Bound: hosted admission** | DNS/TLS/env/Traefik/callback and OAuth rehearsal remain unknown by design. | Operator-private owner | Secret-free deploy/OAuth rehearsal receipt |
| U5 | **Bound: hosted admission** | External consent does not yet name the one SuggestedTrack attachment. | Participant plus operator-private consent owner | Exact bounded consent handle |
| U6 | **Bound: hosted admission** | Submission receipt schema and deterministic structural validator do not exist. | Evidence/receipt owner | HOST-01 schema-only validation |
| U7 | **Produced during execution/closure** | No real import, submission, state/count delta, or filled receipts exist yet. | Participant, operator-private owner, and evidence validator | WITNESS-01 exact threshold; absence before execution is expected |
| U8 | **Bound: repeat/retry use** | Backend idempotency and partial-success recovery remain unproven. | Repository/schema and UI owner | RF-01 duplicate/partial-success witnesses |
| U9 | **Deferred from first formative round** | Full keyboard/screen-reader validation and broader accessibility evidence remain unexecuted. | Accessibility test owner | Separate accessibility validation before any corresponding claim |
| U10 | **Deferred hardening** | Focused detail-payload and `evidence_summary` assertions remain absent. | API test owner | Direct response assertions |
| U11 | **Deferred closeout** | Work-pack status conflicts with the completed ledger projection. | Planning/ledger projection owner | Bounded synchronization after prototype research |
| U12 | **Permanently outside this frontier** | Geometry, scoring, operator promotion, pilot, production, and release proof remain absent. | Their respective future authority owners | No closure sought by this dispatch |
