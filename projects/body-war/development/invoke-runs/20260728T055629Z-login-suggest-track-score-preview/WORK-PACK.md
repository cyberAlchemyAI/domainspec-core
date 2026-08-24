---
module: body-war-login-suggest-track-score-preview
version: current
status: blocked-pending-decisions
updatedAt: 2026-07-28
docType: work-pack
complexity: high
selected_swu: none
---

# Work Pack

## Work-Pack Gate

| Field | Value |
| --- | --- |
| Scope | Body War login-to-score-preview journey |
| Complexity | high |
| Plan status | complete for selection |
| Mutation status | not authorized |
| Selected SWU | none |
| First executable gate | DEC-JSP-001 and DEC-JSP-002 |
| Current proof | existing fake-provider suggestion/evidence loop only |

## TASK-JSP-W0 — Resolve Prototype Policies

### Objective

Create owner-ratified artifacts for score normalization/window/eligibility and
history consent, geometry privacy/retention, and OAuth scope.

The decisions may close in stages: DEC-JSP-001 and DEC-JSP-002 admit L0;
DEC-JSP-003 is required only before SWU-JSP-008 and does not block the local
fixture prototype.

### Inputs

- `ARCHITECTURE.md#blocking-decisions`
- `SPEC.md#proposed-scorepolicy-v0-decision-shape`
- existing game-rules and Strava contracts

### Outputs

- `DEC-JSP-001` complete ScorePolicy V0 bytes and digest, including window
  anchor/timezone, eligibility/aggregation, bootstrap self-sample, missing
  history, and history/consent rules;
- `DEC-JSP-002` geometry privacy, retention, deletion contract;
- `DEC-JSP-003` OAuth scope decision.

### Acceptance

No placeholder, implicit default, or unresolved numeric parameter remains in a
selected implementation unit.

## TASK-JSP-L0 — Local Prototype

### SWU-JSP-001 — Persistence and Repository Contracts

**Owns:** typed pending intent, validated confirmation, GeometryCandidate,
ScoreInputSnapshot, ScorePreview, repository methods, Postgres
schema/migration, memory adapter parity.

**Prerequisites:** DEC-JSP-001 and DEC-JSP-002.

**Outputs:** additive schema and types; separate confirmation, geometry, and
score unique constraints;
round-trip tests.

**Acceptance:**

- migration and schema validation pass;
- memory/Postgres parity passes;
- raw stream fields have no persistence column;
- pending intent has no evidence authority and ownership rejection leaves no
  confirmation/evidence row;
- existing SuggestedTrack tests remain green.

**Excluded:** provider calls, algorithms, UI.

### SWU-JSP-002 — Deterministic Fixture Geometry Gateway

**Owns:** `StravaActivityGateway` interface and fake fixtures for owned/unowned
activity, complete-window derived history, detail/streams, missing geometry,
misalignment, and provider fault.

**Prerequisites:** SWU-JSP-001 contracts.

**Acceptance:**

- fake mode is explicit in status and receipts;
- every fixture is deterministic;
- complete-window fixtures bind canonical activity metrics and provenance;
- real mode cannot fall back to fixture data;
- no token/payload leakage.

**Excluded:** real HTTP calls.

### SWU-JSP-003 — Geometry Normalizer

**Owns:** pure validation/normalization/privacy-filter algorithm and receipts.

**Prerequisites:** DEC-JSP-002, SWU-JSP-002.

**Acceptance:**

- deterministic valid candidate output;
- malformed/misaligned/implausible cases reject;
- raw streams are absent from output, persistence, logs, and snapshots;
- candidate authority and visibility are fixed to
  `candidate_from_activity` and `principal_private`.

**Excluded:** score and source-backed promotion.

### SWU-JSP-004 — ScorePolicy Registry, Snapshot, and Calculator

**Owns:** exact DEC-JSP-001 policy artifact, loader/digest verification, pure
ScoreInputSnapshot assembler, pure calculator, component explanation.

**Prerequisites:** DEC-JSP-001, SWU-JSP-001 through SWU-JSP-003.

**Acceptance:**

- golden fixtures bind exact policy, geometry, evidence-set, and snapshot
  digests;
- repeated input is byte-stable;
- missing/stale/tampered policy blocks;
- component sum, cap, window, unique-day, and rounding invariants pass;
- incomplete history emits a non-comparable component projection with null
  frequency/total;
- output authority is `preview_only`.

**Excluded:** conquest/controller decision.

### SWU-JSP-005 — Idempotent Confirmation and Journey API

**Owns:** exact consent binding, pending-intent/ownership ordering,
staged/resumable orchestration, one public command/read API boundary, stable
errors, and read model.

**Prerequisites:** SWU-JSP-001 through SWU-JSP-004.

**Acceptance:**

- unchecked/mismatched consent creates no mutation;
- fake ownership validates before exact non-first track/activity evidence
  binding persists;
- ownership mismatch leaves no confirmation/evidence transition;
- double request creates one logical result;
- accepted write plus read failure resumes without duplication;
- missing geometry preserves confirmation/evidence;
- missing policy preserves geometry and produces no numeric zero;
- incomplete history produces no comparable total;
- no automatic source-backed/control mutation.

### SWU-JSP-006 — Responsive Consent and Score UI

**Owns:** Help binding, visible consent control/copy, progress/recovery states,
private geometry cue, explained score card.

**Prerequisites:** SWU-JSP-005.

**Acceptance:**

- all `UX-PLAN.md#browser-witnesses` pass;
- 320px and 390px critical controls remain reachable;
- short-height landscape, 200% text, long content, and orientation witnesses
  pass;
- keyboard and screen-reader semantics pass scoped checks;
- fixture mode and preview ceiling are visible;
- no `verified`, `source-backed`, control, pilot, or production copy.

### SWU-JSP-007 — Local Integrated Evidence Gate

**Owns:** fixture end-to-end receipt and scoped validation closeout.

**Prerequisites:** SWU-JSP-001 through SWU-JSP-006.

**Commands:**

```sh
npm --prefix projects/body-war/app run validate
npm --prefix projects/body-war/app test
npm --prefix projects/body-war/app run e2e:all
npm --prefix projects/body-war/app run test:ui
```

**Acceptance:**

- memory and disposable Postgres lanes pass;
- `T-JSP-LOCAL-001`, `T-JSP-SCORE-004`, and
  `T-JSP-AUTHORITY-005` receipts pass;
- no-leak canaries pass independently for application/error logs, test
  snapshots, persistence, and receipts active in L0;
- clean scoped app worktree identity is recorded;
- claim ceiling says local fixture prototype only.

## TASK-JSP-L1 — Moderated Local Test

### SWU-JSP-UX-001 — Formative Protocol and Three Sessions

**Owner:** UX evidence route plus human operator.

**Prerequisites:** SWU-JSP-007 passing receipt.

**Acceptance:** execute the exact bounded protocol in
`UX-PLAN.md#moderated-test-boundary`, preserve individual observations and
formative-only claim ceiling, and route residue back to a new bounded plan.

This is human evidence, not an application coding SWU.

## TASK-JSP-L2 — Real Provider

### SWU-JSP-008 — Token Access and Refresh

**Owns:** encrypted token read/decrypt/refresh/update, typed errors, canary
tests.

**Prerequisites:** DEC-JSP-003 and SWU-JSP-007.

**Acceptance:**

- valid token read works server-side;
- callback rejects accepted scopes that do not satisfy DEC-JSP-003;
- concurrent expired-token requests use account-row CAS or singleflight,
  preserve the newest token pair, and perform at most one bounded retry;
- refresh failure is typed and non-leaking;
- token plaintext appears nowhere outside the immediate provider call.

### SWU-JSP-009 — Real Activity and Geometry Gateway

**Owns:** official Strava list/detail/streams calls, policy-eligible history
derivation, and allow-list normalization.

**Prerequisites:** SWU-JSP-008.

**Acceptance:**

- controlled HTTP fixtures cover success, ownership mismatch, insufficient
  scope, rate limit, malformed streams, and upstream failures;
- explicit real mode never reads synthetic repository activities;
- real history processing obeys DEC-JSP-001 consent/window/eligibility and can
  produce a canonical snapshot without persisting raw streams;
- raw payload/stream canaries are absent from every enumerated real-provider
  sink;
- code evidence remains distinct from a live account witness.

## TASK-JSP-L3 — Hosted Witness

### SWU-JSP-HOST-001 — Admission Package

**Owns:** immutable artifact identity, hosted non-fake signal, exact external
consent, receipt schemas/validator, one-attempt protocol.

**Prerequisites:** SWU-JSP-007, SWU-JSP-009, existing HOST-01 infrastructure
requirements.

**Acceptance:** claim-specific admission receipt binds immutable artifact,
provider mode, external consent version, validators, and one-attempt protocol.
The parent records an explicit `admit` or `reject` event; admission does not
execute the witness.

### SWU-JSP-WITNESS-001 — One Supervised Execution

**Owner:** experiment/operator route.

**Prerequisites:** passing admission package plus explicit parent `admit`.

**Acceptance:** one participant, one named track, one activity, one attempt;
exact consent binding; candidate geometry and ScorePreview; state/count delta;
redacted receipts; no forbidden values; stop on ambiguity.

### Hosted Claim-Specific Receipt Contracts

The generic Dispatch Spec receipt envelope is only transport. Its `artifacts`
must point to a claim-specific JSON receipt, and `validation_result` must name
the passing validator result for those exact bytes.

HOST admission receipt requires:

- immutable artifact digest and hosted non-fake `provider_mode`;
- external consent version/digest;
- gateway/local validation selectors;
- one-attempt protocol digest;
- witness-receipt schema/validator digest;
- parent gate selector;
- residue.

Witness receipt requires:

- HOST admission receipt and parent-admit event digests;
- provider mode and immutable artifact digest;
- principal/track/activity/consent identity digests;
- pre/post state and count delta;
- refresh and all-sink scan results;
- geometry, ScoreInputSnapshot, and ScorePreview receipt digests;
- explicit claim ceiling and audit reference;
- residue.

A generic `status: pass` without this artifact plus validator result blocks.

## Dependency Graph

```text
DEC-JSP-001..003
  -> SWU-JSP-001
    -> SWU-JSP-002
      -> SWU-JSP-003
        -> SWU-JSP-004
  -> SWU-JSP-005
    -> SWU-JSP-006
      -> SWU-JSP-007
        -> SWU-JSP-UX-001
        -> SWU-JSP-008
          -> SWU-JSP-009
            -> SWU-JSP-HOST-001
              -> parent admit/reject gate
                -> SWU-JSP-WITNESS-001
```

## SWU Atomicity Review

| Unit | One owner boundary | One reviewable result | Independent acceptance | Verdict |
| --- | --- | --- | --- | --- |
| JSP-001 | schema/repository | additive persistence contract | repository tests | pass |
| JSP-002 | fake gateway | deterministic provider boundary | gateway fixtures | pass |
| JSP-003 | pure geometry | candidate algorithm | algorithm fixtures | pass |
| JSP-004 | score-input/calculator | policy-bound canonical snapshot and calculation | golden/negative fixtures | pass |
| JSP-005 | orchestration/API | resumable journey boundary | API/integration tests | pass |
| JSP-006 | web UX | participant-facing journey | browser/accessibility tests | pass |
| JSP-007 | validation | evidence closeout only | named command/receipt gate | pass |
| JSP-008 | token service | protected-token lifecycle | security fixtures | pass |
| JSP-009 | real gateway | provider HTTP boundary | controlled HTTP fixtures | pass |
| HOST/WITNESS | operator evidence | hosted admission/live receipt | supervised protocol | pass |

## Selection Boundary

No SWU is selected. The next authorization is a decision-gate, followed by
explicit SWU selection. Plan approval, decision ratification, SWU selection,
Task Session preflight, deployment, and human/live execution remain separate
acts.
