# SuggestedTrack Testable-Prototype Gap — Findings

## Outcome

At commit `b7d60c96d5ace267f5aed8eb9921756aad1f66d3`, the
fake-provider local developer path is current-executed and can be tested now.
It is not yet admissible for moderated participant testing because the current
browser flow manufactures consent and does not bind a clicked Help action to
the later track selection. A first hosted real-Strava route is smaller than a
repeat-safe product route: after LP-01, RF-02, and HOST-01 close their exact
admission gates, WITNESS-01 may run as one supervised, single-attempt witness
with stop-on-ambiguity and no retry. RF-01 blocks repeat- or retry-capable
hosted use, not that first witness.

The current-execution statement is proven only by the clean scoped app worktree
and the four passing commands recorded in
`projects/body-war/development/research/20260727-suggested-track-testable-prototype-gap/CURRENT-VALIDATION.md#execution-identity`
and `#commands-and-results`: `npm run validate`, `npm test` (`3/3`),
`npm run e2e:all` against disposable local Docker Postgres, and
`npm run test:ui` (`7/7`, Chromium). All admitted paths selected fake Strava
(`CURRENT-VALIDATION.md#commands-and-results`). This is current local execution,
not hosted or real-provider evidence.

The smallest recommended next bounded route is **LP-01 only**. It removes the
two observed blockers to a moderated fake-provider participant test and is
also a prerequisite for the later hosted route. This recommendation does not
select, authorize, implement, deploy, or execute LP-01 or any later route.

## Terminology And Frontier Legend

These labels belong only to this research result. They are not Craft states,
promotion states, deployment authority, or release decisions.

| Label | Meaning |
|---|---|
| `current-executed` | The named command or path ran successfully at the named commit in `CURRENT-VALIDATION.md`. |
| `observed-current-gap` | Current source inspection identifies the gap; no closure is claimed. |
| `unverified` | A contract, template, manual, or proposed acceptance surface exists, but the required execution evidence does not. |
| `produced-during-execution` | Evidence is expected to be created by the bounded witness; its absence before that witness is not an admission defect. |
| `deferred` | The item is intentionally outside the claimed prototype frontier. |
| `current-executed-local-developer-path` | Developer/researcher use of the current fake-provider path only. |
| `admit-moderated-local-participant-test` | Three supervised fake-provider formative sessions become admissible only after LP-01 passes. |
| `admit-hosted-supervised-single-witness` | One real-provider, one-participant, one-track, one-activity, one-attempt witness becomes admissible only after LP-01, RF-02, and HOST-01 pass. |
| `single-witness-execution-and-closure` | WITNESS-01 produces the live import, submission, state/count, and filled-receipt evidence. |
| `hosted-repeat-safe` | Repeat- or retry-capable hosted use becomes admissible only after RF-01 passes. It does not imply unmoderated use. |

`ActivityEvidenceCandidate` remains the feature-contract term. An
`evidence_submitted` track has candidate evidence; it does not thereby have
source-backed geometry, a score, or operator acceptance
(`projects/body-war/docs/features/parque-taquaral-online-mvp/states.md:7-30`;
`projects/body-war/docs/features/parque-taquaral-online-mvp/domain.md:51-68`).

## Exact Current Boundary And Evidence Status

| Boundary | Current evidence | Disposition |
|---|---|---|
| Fake login, list/create/detail, synthetic activity selection, and candidate submission | Current-executed at the named commit; all current tests select fake Strava (`CURRENT-VALIDATION.md#commands-and-results`). Agent 1 ties list/create to `projects/body-war/app/server.ts:560-637`, candidate attach to `server.ts:672-725`, and repository state change to `projects/body-war/app/src/auth/memory-repository.ts:192-218` and `src/auth/drizzle-repository.ts:266-295` (`projects/body-war/development/research/20260727-suggested-track-testable-prototype-gap/research.md`, Agent 1, “SuggestedTrack implemented-versus-specified gap matrix”). | **Test now**, but developers/researchers only and fake-provider only. |
| Affirmative consent | The UI has no participant consent control and sends `consent_acknowledged: true` with a hard-coded phrase (`projects/body-war/app/static/app.js:386-418`); the passing UI journey clicks submit without affirming consent (`projects/body-war/app/e2e/troqar-product-architecture/ui.spec.ts:89-96`). The owned contract requires explicit consent and concrete retained/excluded fields (`projects/body-war/docs/features/parque-taquaral-online-mvp/operations.md:25-45`; `research.md`, Agent 1 “Affirmative browser consent” and Agent 2 “P0”). `CURRENT-VALIDATION.md#proof-ceiling` explicitly says the current pass does not prove visible informed consent. | **Observed current gap; LP-01 gate.** |
| Help-to-track binding | Help only scrolls to activities, while each activity selector independently defaults to the first track (`projects/body-war/app/static/app.js:289-295,381-399`; `projects/body-war/app/static/index.html:100-147`; `research.md`, Agent 2 “P1 — Help does not preserve the route the participant intended”). The current browser suite manually selects a track, so its pass does not prove Help binding (`CURRENT-VALIDATION.md#proof-ceiling`). | **Observed current gap; LP-01 gate.** |
| Real Strava activities | `listActivitySummaries` delegates to synthetic repository summaries (`projects/body-war/app/src/auth/strava-oauth.ts:172-189`; `projects/body-war/app/src/auth/memory-repository.ts:135-147`; `projects/body-war/app/src/auth/drizzle-repository.ts:202-214`), and the repository contract lacks the read/refresh path needed for live token use (`projects/body-war/app/src/auth/body-war-repository.ts:53-70`; `research.md`, Agent 1 “Live real-Strava activity consult”). | **Observed current gap; RF-02 gate.** |
| Hosted deployment and OAuth | Host, DNS/TLS, protected environment, Traefik, callback, deploy, and OAuth rehearsal remain operator-bound and unverified (`projects/body-war/docs/ONLINE-DEPLOY-MANUAL.md:16-21,75-158,238-277`; `projects/body-war/development/task-sessions/20260622T140208Z-traefik-secret-blind-deploy/TASK-SESSION-RESULT.md:1-15`; `research.md`, Agent 3 readiness orders 3–6). | **Unverified; HOST-01 gate.** |
| External participant consent | The current template is blank and covers connection/import, not attachment of one activity candidate to one named SuggestedTrack (`projects/body-war/docs/validation/FRIEND-ACTIVITY-CONSENT-TEMPLATE.md:1-30`; `research.md`, Agent 3 order 7). | **Unverified; HOST-01 gate.** |
| Submission receipts | The import template omits private data and bounds geometry/scoring claims, but proves import only; the deployment template stops at deployment/login checks (`projects/body-war/docs/validation/ACTIVITY-IMPORT-RECEIPT.md:6-31,48-61`; `projects/body-war/infra/deployment-receipts/TEMPLATE.md:10-20`; `research.md`, Agent 3 orders 8–9). | **Submission schema/validator unverified; HOST-01 gate. Filled live receipts are produced by WITNESS-01.** |
| Duplicate and partial-success behavior | The UI re-enables submission after the request and can make a successful mutation look failed if refresh fails; no adopted idempotency contract is present (`projects/body-war/app/static/app.js:394-420,413-458`; `projects/body-war/docs/features/parque-taquaral-online-mvp/interfaces.md:53-72`; `research.md`, Agent 2 “P1 — Duplicate and partial-success submission risk”). | **Observed risk; RF-01 gate for repeat/retry-capable hosted use, not the first one-shot witness.** |
| Geometry, scoring, acceptance, and pilot state | The feature explicitly keeps these outside the current build, and runtime preserves the non-claims (`projects/body-war/docs/features/parque-taquaral-online-mvp/SPEC.md:76-81`; `states.md:15-30`; `projects/body-war/app/server.ts:332-389`; `research.md`, Agent 1 “Operator review, source-backed geometry, acceptance/rejection, scoring”). | **Deferred; no closure sought.** |

## Test-Now / Must-Fix / Defer Matrix

| Surface | Developer local | Moderated local participant | Hosted supervised single witness | Hosted repeat/retry | Disposition |
|---|---:|---:|---:|---:|---|
| Current fake-provider application path | **Test now** | Insufficient by itself | Not real-provider evidence | Insufficient | Current-executed only (`CURRENT-VALIDATION.md#commands-and-results`). |
| Visible affirmative consent and displayed/affirmed/transmitted/persisted text identity | Current implementation fails | **Must fix: LP-01** | Required | Required | Current UI manufactures consent (`app/static/app.js:386-418`; `research.md`, Agent 2 P0). |
| Exact non-first Help-to-track binding at 320px and 390px | Current implementation fails | **Must fix: LP-01** | Required | Required | Current Help loses route context (`app/static/app.js:289-295,381-399`; `research.md`, Agent 2 P1). |
| Real token retrieval/refresh, activity gateway, and allow-list normalization | Synthetic only | Not needed | **Must fix: RF-02** | Required | Current activity summaries are synthetic (`app/src/auth/strava-oauth.ts:172-189`; `research.md`, Agent 1 live-activity row). |
| Immutable deployed artifact, real-mode signal, deploy/OAuth rehearsal, exact external consent, prevalidated receipt schemas | No hosted proof | Not needed | **Must fix: HOST-01** | Required | Hosted and receipt evidence is unverified (`ONLINE-DEPLOY-MANUAL.md:16-21,75-158,238-277`; `research.md`, Agent 3 orders 3–9). |
| Real import, exactly one submission, state/count delta, filled redacted receipts | Not applicable | Not applicable | **Produced by WITNESS-01** | Required evidence | The ledger requires real import and submission; current receipt shapes do not yet prove both (`projects/body-war/.craft/ledger.yml:636-653`; `research.md`, Agent 3 orders 8–9). |
| Idempotency and partial-success recovery | Unproven | Not required under supervised no-retry containment | Not required for one attempt | **Must fix: RF-01** | Current duplicate/refresh ambiguity is observed (`app/static/app.js:394-420`; `research.md`, Agent 2 duplicate-risk row). |
| Accessibility, broader API hardening, work-pack synchronization | No claim | No claim | No claim | No claim | **Defer.** |
| Geometry, scoring, promotion, pilot, production, release, shipment | No claim | No claim | No claim | No claim | **Outside frontier.** |

## Bounded Routes And Exact Witness Surfaces

None of the routes below is selected or authorized by this result.

### LP-01 — Moderated-Local Consent-And-Binding Gate

Proposed scope:

- Display the exact consent statement before an unchecked affirmation control,
  including the concrete retained allow-list and excluded raw/private fields.
- Derive `consent_acknowledged` only from the participant action.
- Make displayed, affirmed, transmitted, and persisted consent identities
  byte-identical, or canonically equal under one explicit deterministic rule.
- Carry Help from a non-first SuggestedTrack into a labelled, focused activity
  prompt; preserve that exact track through consent and submission at 320px and
  390px.
- Issue zero POSTs while unchecked and exactly one checked POST; persist exactly
  one candidate attached to that track in the normal happy path.

The current gaps grounding this proposed scope are at
`projects/body-war/app/static/app.js:289-295,381-418` and the owned consent
contract is at
`projects/body-war/docs/features/parque-taquaral-online-mvp/operations.md:25-45`
(`research.md`, Agent 1 affirmative-consent row; Agent 2 P0/P1).

Proposed acceptance commands:

```sh
cd projects/body-war/app
npm run validate
npm test
npm run e2e:all
npm run test:ui
```

Required browser witness: non-first-track Help → correct focused selection at
320px and 390px → zero POST while unchecked → exact consent text affirmed →
exactly one checked POST → persisted candidate references that same track.

### RF-02 — Real Strava Activity Boundary

Proposed scope:

- Retrieve and decrypt tokens server-side and refresh when necessary.
- Call the real Strava athlete-activities endpoint.
- Normalize only the current `ActivitySummary` allow-list and persist no raw
  provider payload.
- Keep synthetic activity only behind explicit fake mode.
- Emit a redacted hosted signal or operator attestation for
  `fake_mode: false` and real-adapter selection.

This proposed route repairs the current synthetic boundary at
`projects/body-war/app/src/auth/strava-oauth.ts:172-189`,
`memory-repository.ts:135-147`, `drizzle-repository.ts:202-214`, and
`body-war-repository.ts:53-70` (`research.md`, Agent 1 live-activity row).

Proposed acceptance commands are the same four LP-01 commands. Controlled tests
must witness gateway success, token refresh, provider failure, allow-listing,
and fake/real separation. Those tests do not prove a live account; the hosted
non-fake attestation belongs to HOST-01/WITNESS-01.

### HOST-01 — Hosted Supervised Single-Witness Admission Package

Proposed scope:

- Freeze the source commit and immutable image/artifact digest.
- Complete operator-private deployment and OAuth rehearsal without exposing
  secrets.
- Bind external consent to one participant, one activity import, and one
  candidate attachment to one named SuggestedTrack.
- Define machine-checkable import and submission receipt schemas and
  prevalidate blank/redacted forms.
- Freeze a one-attempt/no-retry protocol.
- Define operator-private value/log inspection that emits only a redacted
  pass/fail result.

The current deployment, consent, and receipt gaps are source-bound at
`projects/body-war/docs/ONLINE-DEPLOY-MANUAL.md:16-21,75-158,238-277`,
`projects/body-war/docs/validation/FRIEND-ACTIVITY-CONSENT-TEMPLATE.md:1-30`,
`ACTIVITY-IMPORT-RECEIPT.md:6-31,48-61`, and
`projects/body-war/infra/deployment-receipts/TEMPLATE.md:10-20`
(`research.md`, Agent 3 orders 3–9).

Proposed acceptance interface, which does not exist as a proven current
surface:

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

Admission requires one receipt binding the commit, artifact ID, host, callback
rehearsal, `fake_mode: false`, real-adapter signal, exact consent handle,
receipt-schema versions, and frozen no-retry protocol. Public smoke is shallow:
the current script checks status, a page marker, and obvious token terms only
(`projects/body-war/infra/scripts/smoke-online.sh:12-24`; `research.md`, Agent 3
order 5).

### WITNESS-01 — One Supervised Real-Strava Execution And Closure

This is not a pre-test implementation gap. It is the execution that produces
the live import, submission, and filled receipts currently absent.

Participant actions:

1. Complete OAuth.
2. Select the one consented activity.
3. Verify the one named SuggestedTrack.
4. Read and affirm the displayed consent.
5. Submit exactly once.

Passing requires every item below:

- pre-state `needs_evidence`;
- immutable commit/artifact identity matching HOST-01;
- `fake_mode: false` and a real-adapter signal;
- participant/session, activity, and SuggestedTrack selectors matching the
  consent and receipt bindings;
- exactly one submission POST and a successful response;
- post-state `evidence_submitted` and candidate-count delta exactly `+1`;
- matching displayed, affirmed, transmitted, and persisted consent identity;
- structurally valid import and submission receipts; and
- operator-private inspection reporting zero forbidden secret/private values
  while exposing only the redacted result.

The state/count witness can be anchored to
`projects/body-war/docs/features/parque-taquaral-online-mvp/queries.md:19-36`
and `projects/body-war/app/server.ts:374-389,640-669`; the required real import
and submission boundary is at `projects/body-war/.craft/ledger.yml:636-653`
(`research.md`, Agent 1 detail/readback row and Agent 3 orders 8–9).

If any identity, response, state, count, consent, or receipt result is
ambiguous, the operator stops the witness without retry. The result is
inconclusive and no blocker closes. Filled import and submission receipts are
created here, during execution and closure; they are not admission
prerequisites.

Proposed structural validation:

```sh
node projects/body-war/infra/scripts/validate-hosted-witness-receipts.cjs \
  --import REDACTED_IMPORT_RECEIPT \
  --submission REDACTED_SUBMISSION_RECEIPT
```

### RF-01 — Hosted Repeat/Retry Safety Gate

Proposed scope:

- enforce principal + track + activity uniqueness/idempotency;
- return a stable duplicate result and disable already-submitted pairs;
- distinguish “mutation accepted; refresh failed” from mutation failure; and
- prove that delayed double-click and accepted-POST/failed-refresh scenarios
  each leave exactly one candidate.

The current UI ambiguity and absent adopted idempotency contract are observed
at `projects/body-war/app/static/app.js:394-420,413-458` and
`projects/body-war/docs/features/parque-taquaral-online-mvp/interfaces.md:53-72`
(`research.md`, Agent 2 duplicate-risk row).

Proposed acceptance commands are the same four LP-01 commands, with explicit
duplicate, delayed-double-click, and partial-success witnesses. RF-01 is
mandatory before hosted repeat or retry-capable use. It is not a gate for
WITNESS-01 because that witness permits exactly one attempt and stops on
ambiguity. This research does not admit unmoderated use after either route.

## Moderated Local Participant Protocol

Only after LP-01 passes, the proposed formative protocol is exactly three
supervised 15-minute fake-provider sessions split across assigned 320px and
390px widths. Agent 2 proposed this as formative rather than statistical
evidence (`research.md`, Agent 2 “Smallest meaningful local usability test”);
the current suite's narrower responsive checks do not cover the Help/consent
journey (`projects/body-war/app/e2e/troqar-product-architecture/ui.spec.ts:108-130`;
`research.md`, Agent 2 P2).

Each participant is asked to:

1. Find a non-first SuggestedTrack and use its Help action.
2. Identify the selected route and named activity.
3. State every displayed retained-field category and exclusion in their own
   words.
4. Affirm consent deliberately.
5. Submit once.
6. Explain whether the candidate proves route geometry.
7. Create another suggestion without reusing the first evidence pair.

Every criterion must pass **3/3**:

- the intended non-first track remains selected;
- retained fields and exclusions are identified correctly;
- consent is visibly deliberate;
- exactly one POST occurs;
- the candidate attaches to the intended track;
- the participant says the submission is candidate evidence, not geometry
  proof; and
- required controls remain reachable at the assigned width.

The moderator stops immediately on consent ambiguity, route ambiguity, or
apparent partial success. The participant does not retry. A stopped session is
inconclusive, not something the participant is asked to repair. Passing this
protocol would remain bounded formative evidence, not accessibility or
statistical usability validation.

## Hosted Dependency And Ownership

### Admission

| Owner | Bounded responsibility | Required handoff surface |
|---|---|---|
| Application owner | Close LP-01 and RF-02. | Four local commands plus the route-specific witnesses above. |
| Test executor | Rerun all four commands against the frozen commit. | Commit-bound local validation receipt. |
| Build/deploy owner | Freeze commit and immutable image/artifact identity. | Secret-free artifact identity in HOST-01 admission receipt. |
| Operator-private owner | Configure DNS/TLS, protected environment, Traefik, callback, deployment, operator-account OAuth rehearsal, and private real-mode verification. | Secret-free deploy/OAuth rehearsal receipt and redacted `fake_mode: false`/real-adapter verdict. Agent 3 establishes these as private or unverified actions (`research.md`, orders 3, 4, and 6; `ONLINE-DEPLOY-MANUAL.md:75-158,238-277`). |
| Safe observer | Run only public smoke after operator completion. | Public status/page-marker/shallow-term result; no private provider state or logs (`infra/scripts/smoke-online.sh:12-24`; `research.md`, Agent 3 order 5). |
| Participant plus operator-private consent owner | Agree to the exact one-activity import and one candidate attachment to one named track. Keep identity mapping private. | Bounded consent handle; no raw identity in tracked artifacts (`FRIEND-ACTIVITY-CONSENT-TEMPLATE.md:1-30`; `research.md`, Agent 3 order 7). |
| Evidence validator | Prevalidate blank/redacted import and submission receipt structures. | Schema-only validation result; no private payload access. |
| Parent | Compare all admission evidence to HOST-01. | Explicit admit/reject decision for WITNESS-01. |

### Execution And Closure

| Owner | Bounded responsibility | Prohibited collapse |
|---|---|---|
| Participant | Complete OAuth, select the consented activity and named track, affirm, and submit once. | Does not inspect infrastructure, secrets, or logs. |
| Operator-private owner | Observe private state/count readback and perform private secret-value/log inspection. | Returns only redacted results; does not delegate private actions to observer or validator. |
| Safe observer | Repeat public smoke only if required. | Public reachability is not real-provider or submission proof. |
| Evidence validator | Structurally validate the redacted filled receipts. | Does not receive tokens, OAuth codes, raw payloads, maps, notes, private URLs, or identity mapping; the forbidden tracked fields are enumerated in `ACTIVITY-IMPORT-RECEIPT.md:48-56` (`research.md`, Agent 3 order 8). |
| Parent | Compare the complete WITNESS-01 threshold and decide whether `BLK-STRAVA-ACTIVITY-001` closes. | No automated or delegated blocker closure; no geometry, scoring, promotion, pilot, production, or release decision follows. |

## Reviewer Verdict Matrix

| Reviewer | Initial verdict | Load-bearing objection | Accepted disposition | Final verdict |
|---|---|---|---|---|
| Rittel | `REVISE`, never precedent `KILL` | Ownership needed separation; fresh current-head execution was missing; retry hardening was overstated as a first-witness gate. | Current execution is commit-bound; private actions stay participant/operator-private; safe observer and validator are narrowed; RF-01 gates repeat/retry, not WITNESS-01. | `REVISE`, no `KILL` (`projects/body-war/development/research/20260727-suggested-track-testable-prototype-gap/REVIEWER-RECEIPTS.md#rittel--precedent-and-ownership`). |
| Popper | `REVISE` | Consent needed displayed-to-persisted identity; Help needed an executable non-first-track witness; hosted evidence needed immutable identity, structural receipts, exact thresholds, and no-retry containment. | LP-01, HOST-01, and WITNESS-01 now name observable browser, artifact, request, state/count, consent, and receipt witnesses. | `REVISE` (`REVIEWER-RECEIPTS.md#popper--non-vacuity-and-observable-witness`). |
| Lakatos | `REVISE` | Research labels risked becoming lifecycle claims; hosted admission was conflated with live execution/closure; RF-01 and unmoderated use needed separation. | Labels are research-local; HOST-01 admits, WITNESS-01 executes/closes, and RF-01 gates repeat/retry only; unmoderated use remains unadmitted. | `REVISE` with no definitional collapse (`REVIEWER-RECEIPTS.md#lakatos--definitional-and-claim-boundary-soundness`). |

The accepted revision resolves all bounded reviewer objections. No reviewer
emitted `KILL`; this does not turn the proposed routes into approved work
(`REVIEWER-RECEIPTS.md#converged-reviewer-disposition`).

## Claim Ceilings And Deferred Items

- Current execution proves only the named commit's local fake-provider paths
  (`CURRENT-VALIDATION.md#proof-ceiling`).
- Disposable local Docker Postgres is not managed infrastructure or hosted
  deployment (`CURRENT-VALIDATION.md#commands-and-results`).
- Passing tests that manufacture consent do not prove affirmative participant
  consent or Help-to-track binding (`CURRENT-VALIDATION.md#proof-ceiling`;
  `app/static/app.js:289-295,386-418`; `research.md`, Agent 2 P0/P1).
- Three passing moderated formative sessions would not prove accessibility or
  statistical usability.
- A real import is not a SuggestedTrack submission; separate redacted witnesses
  are required (`ACTIVITY-IMPORT-RECEIPT.md:58-61`;
  `infra/deployment-receipts/TEMPLATE.md:10-20`; `research.md`, Agent 3 orders
  8–9).
- One supervised witness would not prove retry safety, repeatability, or
  unmoderated suitability.
- `evidence_submitted` means candidate evidence only; it does not prove route
  geometry or scoring (`states.md:15-30`; `server.ts:332-389`; `research.md`,
  Agent 1 operator-review row).
- No accessibility, geometry, scoring, operator acceptance, promotion, pilot,
  production, release, or shipment claim is admitted.
- Focused detail-payload/`evidence_summary` assertions are deferred API
  hardening; Agent 1 observed the implementation but no direct current API
  assertion (`projects/body-war/docs/features/parque-taquaral-online-mvp/queries.md:19-36`;
  `server.ts:374-389,640-669`; `research.md`, Agent 1 detail/readback row).
- Work-pack synchronization is deferred closeout, not runtime proof: the ledger
  records the one-go work complete while the Work Pack projection remains stale
  (`projects/body-war/.craft/ledger.yml:879-906,985-1000`;
  `projects/body-war/docs/features/parque-taquaral-online-mvp/WORK-PACK.md:53-63`;
  `research.md`, Agent 1 planning-state row).
- Inventory remains discovery-only and grants no application, production, or
  release authority (`.arcanum/inventory/entries/domainspec-v2-fpr02-integrated-consumer-proof-refresh.md:49-58`;
  `research.md`, Agents 1 and 3).

## Recommended Next Bounded Route

If implementation work is separately selected, choose **LP-01 alone** first.
Its acceptance surface is local, current-source-bound, and independent of
operator secrets or hosted infrastructure. A passing LP-01 would admit only the
three-session moderated fake-provider protocol. It would not select RF-02,
HOST-01, WITNESS-01, or RF-01; admit a real participant; close the real-Strava
blocker; or establish any accessibility, geometry, scoring, promotion, pilot,
production, release, or shipment claim.
