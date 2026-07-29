# SuggestedTrack Prototype-Gap Reviewer Receipts

These are the joined independent and confrontation returns from the confirmed
reviewer group. The reviewers were read-only. No reviewer edited Body War
application or authority artifacts.

## Rittel — Precedent And Ownership

### Independent report

#### Key findings

- The developer-local flow is already implemented and had prior passing
  receipts, but the synthesis initially lacked a fresh current-head witness.
  Runtime selectors are `app/server.ts:589-725` and
  `app/static/app.js:301-459`; the prior receipt is
  `development/task-sessions/20260629T061500Z-suggested-track-one-go-build/TASK-SESSION-RESULT.md:21-29`.
- Visible consent and exact track binding are justified
  `build-from-owned` blockers for a narrowly moderated fake-provider test.
  Current defects are at `app/static/app.js:289-295,381-418`; the owned consent
  boundary is `docs/features/parque-taquaral-online-mvp/operations.md:27-45`.
- Retry safety is legitimate `build-from-owned` hardening, but the operation
  and interface do not currently define idempotency as an admission
  requirement. Both repositories insert candidates and the schema has no pair
  uniqueness (`app/src/auth/memory-repository.ts:192-218`,
  `app/src/auth/drizzle-repository.ts:266-295`,
  `app/src/infrastructure/postgres/schema.ts:120-140`;
  `docs/features/parque-taquaral-online-mvp/interfaces.md:53-72`).
- The real-Strava and hosted gaps are not already deployed. Token storage lacks
  the read/update path needed for refresh
  (`app/src/auth/body-war-repository.ts:53-70`), activity listing remains
  synthetic (`app/src/auth/strava-oauth.ts:172-189`), and online deployment
  remains operator-blocked (`docs/ONLINE-DEPLOY-MANUAL.md:270-277`).
- Existing external consent covers connection and import, not attaching a
  candidate to a SuggestedTrack
  (`docs/validation/FRIEND-ACTIVITY-CONSENT-TEMPLATE.md:15-19,23-30`).
  Participant/operator-private action cannot be assigned to a generic evidence
  owner.

#### Classification and inconsistencies

| Item | Classification | Independent conclusion |
|---|---|---|
| Developer-local flow | `already-deployed` | Fresh execution was required before a current-pass claim. |
| Consent and binding | `build-from-owned` | Application/UI owner closes the concrete retention boundary. |
| Retry safety | `build-from-owned` | Valid hardening, not an existing first-witness KILL gate. |
| Real activity adapter | `build-from-owned` | Application auth/repository and adapter owners share it. |
| Hosted bring-up | `build-from-owned` | Operator precedent exists; deployment does not. |
| Real witness receipts | `precedent-clean` | New bounded receipt is valid; absence of precedent is not KILL. |
| Geometry/scoring/promotion deferral | `precedent-clean` | Explicitly consistent with non-goals. |
| Planning synchronization | `build-from-owned` | Owned closeout repair, not a testing blocker. |

The initial synthesis also needed to:

- restrict the safe observer to public smoke;
- restrict the evidence owner to redaction/validation;
- assign private activity to participant/operator-private owners;
- expand the external consent scope;
- replace the self-matching vocabulary grep; and
- require a fresh current-head receipt.

#### Initial verdict

`REVISE`, never `KILL` on precedent.

### Final confrontation position

Popper's evidence strengthened the need for exact displayed-to-persisted
consent, immutable hosted artifact identity, a non-fake runtime signal,
structural receipt validation, and explicit moderated-local thresholds.
Lakatos correctly separated hosted admission, execution, and closure.

The stable conclusion is:

- `SWU-RF-01` is not mandatory for the first supervised, one-attempt hosted
  witness.
- It is mandatory before unsupervised, repeatable, or retry-capable hosted use.
- The first witness must issue exactly one submission and stop without retry
  after any ambiguous response or refresh. Ambiguity is an inconclusive
  witness.
- Participant/operator-private owners perform private actions; safe observers
  run public smoke; evidence owners validate redacted receipts; the parent
  alone decides blocker closure.

Final verdict: `REVISE`, no `KILL`.

## Popper — Non-Vacuity And Observable Witness

### Independent report

#### Key findings

- The local frontier required an immutable source identity and fresh commands.
  `validate`, `e2e:all`, and `test:ui` prove only their bounded local paths.
  The Postgres harness is disposable local Docker Postgres, not managed
  Postgres (`app/scripts/e2e.sh:6-10,23-57`).
- Consent closure must bind displayed, affirmed, and persisted text. The server
  currently accepts client-supplied nonempty consent text
  (`app/server.ts:687-713`), while the current UI constant is less concrete
  than the retention contract (`app/static/app.js:9`;
  `docs/features/parque-taquaral-online-mvp/operations.md:41-45`).
- The LP browser witness must click Help on a non-first track, assert focus and
  selection, assert zero unchecked POSTs, and assert exactly one checked POST
  to the clicked track.
- The known partial-success path can re-enable submission after a successful
  mutation and failed refresh (`app/static/app.js:394-420`). The first
  moderated session can exclude it only with explicit no-retry containment and
  non-vacuous thresholds.
- Public smoke proves status, page marker, and a shallow term check only
  (`infra/scripts/smoke-online.sh:12-24`). Hosted acceptance additionally needs
  immutable artifact identity, a non-fake signal, OAuth/import/submission
  witnesses, and private log inspection represented only by a redacted result.
- The current consent template does not cover candidate submission, and the
  proposed grep necessarily matches forbidden-field policy prose. A structural
  allow-list receipt validator plus operator-side value/log checks is required.

#### Independent tensions and verdict

- “Ready now” had to distinguish source-observed executability from a fresh
  pass.
- Consent is privacy-critical for real data and a fidelity/comprehension gate
  for fake participant testing.
- Deterministic adapter tests cannot prove live account behavior.
- The participant protocol needs explicit 3/3 thresholds, zero duplicate POSTs,
  and assigned-width reachability.

Initial verdict: `REVISE`, not `KILL`; every disputed frontier has an observable
witness.

### Final confrontation position

Rittel and Lakatos changed the retry-safety disposition. The current authority
does not adopt idempotency, and duplication requires a second submission
attempt. Therefore:

- `SWU-RF-01` is not mandatory for one tightly supervised, single-attempt
  hosted witness.
- It is mandatory before unmoderated use, repeat attempts after ambiguity, an
  at-most-once claim, or broader repeat/pilot admission.
- Pre-test admission must close LP-01 and RF-02, bind current source and hosted
  artifact identity, record fake mode off, rehearse operator-owned OAuth, adopt
  exact external consent, prepare receipt validation, and impose one
  attempt/no retry.
- Participant performs the consented UI action; operator owns private state;
  safe observer/evidence owner only observes and validates.
- Post-test closure must prove exactly one request and candidate result through
  redacted evidence. An ambiguous outcome is inconclusive.

Final verdict: `REVISE`.

## Lakatos — Definitional And Claim-Boundary Soundness

### Independent report

#### Key findings

- `test-now` initially meant permission to begin fresh validation, not proof of
  a current working path.
- Consent and exact track binding form a sound minimum for a narrowly moderated
  fake-provider session, but “participant-safe” overclaims two bounded fixes.
- Hosted prerequisites were conflated with evidence created by the test itself.
  Real import, submission, and completed receipts belong to execution and
  closure, not “before test.”
- External consent currently stops at import and must explicitly cover a
  non-authoritative candidate attachment to one SuggestedTrack.
- `evidence_submitted`, `source_backed`, operator review, geometry, scoring, and
  pilot promotion remain distinct in
  `docs/features/parque-taquaral-online-mvp/states.md:7-30`,
  `domain.md:51-68`, and `SPEC.md:76-81`.

#### Independent corrections and verdict

- Declare frontier labels research-local, not lifecycle/release states.
- Rename LP-01 to a bounded consent-and-binding gate.
- Split hosted admission, execution, and closure.
- Treat idempotency as hardening unless an owner adopts it as a new first-run
  safety policy.
- Keep `ActivityEvidenceCandidate` as the feature-contract term.
- Keep the stale Work Pack projection as closeout drift, not a runtime-testing
  blocker.

Initial verdict: `REVISE`; no genuine unbounded definitional collapse.

### Final confrontation position

Use the research-local label `hosted-supervised-single-witness`:

- one consented participant;
- one immutable deployed artifact;
- one fresh `needs_evidence` track;
- one real activity; and
- exactly one supervised submission attempt.

Admission requires current local validation, LP-01, RF-02, operator-private
deployment/OAuth smoke, external consent for named candidate attachment,
prevalidated receipt schemas, immutable artifact/run identity, a structural
non-fake signal, and separated owners.

Execution passes only with one consent handle, bound track/activity selectors,
pre-state `needs_evidence`, exactly one POST, successful response, post-state
`evidence_submitted`, candidate-count delta `+1`, valid import/submission
receipts, fake mode false, zero forbidden private values, and matching artifact
identity. Ambiguity stops without retry and remains inconclusive.

Use `hosted-repeat-safe` only after RF-01 proves at-most-one candidate across
duplicate, double-click, and partial-success scenarios. Do not admit
unmoderated hosted testing from this research.

Final verdict: `REVISE`.

## Converged Reviewer Disposition

No reviewer emitted `KILL`. All three require one bounded synthesis revision.
They converge on:

1. current fake-provider execution may be claimed only through fresh
   commit-bound evidence;
2. LP-01 is an exact consent-and-binding gate, not general participant safety;
3. the first hosted frontier is a supervised, one-attempt witness;
4. RF-01 is deferred from that single witness but blocks repeat/retry-capable or
   unmoderated use;
5. hosted admission, execution, and closure must be separate;
6. participant, operator-private, safe-observer, evidence-validator, and parent
   responsibilities must not collapse;
7. receipts must bind artifact identity, non-fake execution, exact state/count
   thresholds, and structural secrecy rules; and
8. no geometry, scoring, promotion, pilot, production, or release claim
   follows.
