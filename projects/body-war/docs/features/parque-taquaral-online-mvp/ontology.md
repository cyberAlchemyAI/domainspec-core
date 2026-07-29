---
module: body-war-suggested-track-score-ontology
version: 0.1.0
status: feature-ontology-baseline
updatedAt: 2026-07-28
docType: body-war-feature-ontology
scope: CTX-BODY-WAR-SUGGESTED-TRACKS
authorityEffect: body-war-feature-node-identities-only
domainSpecAdoption: not-run
implementationConformance: not-claimed
cyberAlchemyPromotion: none
---

# Ontology: Login to SuggestedTrack Score Preview

## Authority Boundary

This document is the Body War feature-owned ontology baseline for the journey:

```text
login -> connected runner -> SuggestedTrack -> activity selection
  -> explicit consent -> ownership validation -> evidence candidate
  -> private geometry candidate -> canonical score input
  -> explained preview-only score
```

It owns the node identities, meanings, typed relationships, state vocabulary,
and intent-to-system bridge needed for the next DomainSpec adoption. It does
not claim that specified system nodes are implemented, does not ratify open
score or privacy parameters, does not promote any node into CyberAlchemy, and
does not grant source-backed geometry or game authority.

## Ontology Conventions

### Branches

| Branch | Owns |
| --- | --- |
| `business` | Actors, roles, meaning, rules, policies, evidence, operations, outcomes, and lifecycle states. |
| `system` | UI surfaces, endpoints, services, gateways, stores, schemas, controls, tests, and receipts. |
| `bridge` | Traceability between business intent and system realization, including drift and evidence gaps. |

### Maturity

| Value | Meaning |
| --- | --- |
| `existing_contract` | Present in the current Body War feature contracts or candidate map. This alone is not runtime proof. |
| `specified_new` | Defined by this ontology for later DomainSpec and implementation work. |
| `decision_required` | Node identity and purpose are defined, but owner-selected parameters remain open. |
| `deferred` | Defined but outside the local-fixture prototype. |
| `excluded` | Visible boundary node that the prototype must not enter automatically. |

Evidence confidence and commitment maturity are separate. `high` confidence
means the cited source supports the meaning; it does not mean the system
realization exists.

### Edge Types

| Branch | Allowed edge types |
| --- | --- |
| `business` | `is_a`, `initiates`, `becomes`, `enters`, `creates`, `selects`, `affirms`, `binds`, `governs`, `validates`, `produces`, `supports`, `contributes_to`, `explains`, `displays`, `does_not_promote` |
| `system` | `exposes`, `invokes`, `authorizes`, `reads`, `writes`, `validates`, `implements`, `feeds`, `projects`, `observes`, `scans`, `tests` |
| `bridge` | `realized_by`, `depends_on`, `constrained_by`, `observed_by`, `tested_by`, `drifts_from`, `traced_to` |

## Source Registry

| Source ID | Path | Role |
| --- | --- | --- |
| `SRC-DOMAIN` | [`domain.md`](domain.md) | Current feature entity and enum contract. |
| `SRC-STATES` | [`states.md`](states.md) | Current SuggestedTrack and evidence lifecycles. |
| `SRC-OPERATIONS` | [`operations.md`](operations.md) | Current creation, evidence, and seed rules. |
| `SRC-INTERFACES` | [`interfaces.md`](interfaces.md) | Current HTTP and repository surfaces. |
| `SRC-UI` | [`ui-spec.md`](ui-spec.md) | Current login/connected UI and copy boundaries. |
| `SRC-INVOKE-ONTOLOGY` | [`ONTOLOGY-MAP.md`](../../../development/invoke-runs/20260728T055629Z-login-suggest-track-score-preview/ONTOLOGY-MAP.md) | Governed candidate business/system/bridge map; candidate evidence, not prior authority. |
| `SRC-INVOKE-SPEC` | [`SPEC.md`](../../../development/invoke-runs/20260728T055629Z-login-suggest-track-score-preview/SPEC.md) | Approved design input for the expanded journey; not implementation proof. |

## Business Node Registry

### Actors, Roles, Surfaces, and Journey

| ID | Kind | Meaning | Maturity | Evidence confidence | Sources |
| --- | --- | --- | --- | --- | --- |
| `bw.actor.anonymous-visitor` | actor | Person who has not established a Body War session. | `existing_contract` | high | `SRC-UI`, `SRC-INVOKE-SPEC` |
| `bw.actor.runner` | actor | Person using Body War to turn a run into track evidence and a visible preliminary result. | `existing_contract` | high | `SRC-INVOKE-ONTOLOGY` |
| `bw.role.connected-runner` | role | Runner with an active Body War session and linked provider account. | `existing_contract` | high | `SRC-INVOKE-ONTOLOGY`, `SRC-UI` |
| `bw.role.prototype-operator` | role | Person configuring prototype execution and supervised receipts without promotion authority. | `specified_new` | high | `SRC-INVOKE-SPEC` |
| `bw.role.track-policy-owner` | role | Owner authorized to ratify score policy and later track-promotion rules. | `specified_new` | high | `SRC-INVOKE-SPEC` |
| `bw.actor.strava-provider` | external actor | Provider of identity, activity summaries, selected activity details, and streams under granted scope. | `existing_contract` | high | `SRC-OPERATIONS`, `SRC-INVOKE-SPEC` |
| `bw.surface.login-entry` | business surface | Anonymous entry that explains and starts Strava connection. | `existing_contract` | high | `SRC-UI`, `SRC-INVOKE-SPEC` |
| `bw.surface.connected-track-workspace` | business surface | Connected-runner area for creating/selecting a track and choosing evidence. | `existing_contract` | high | `SRC-UI` |
| `bw.surface.score-preview-card` | business surface | Explained preliminary score display with evidence mode, limitations, and authority ceiling. | `specified_new` | high | `SRC-INVOKE-SPEC` |
| `bw.journey.login-to-score-preview` | workflow | Resumable end-to-end participant journey covered by this ontology. | `specified_new` | high | `SRC-INVOKE-SPEC` |

### Domain Objects, Evidence, Policies, and Outcomes

| ID | Kind | Meaning | Maturity | Evidence confidence | Sources |
| --- | --- | --- | --- | --- | --- |
| `bw.entity.suggested-track` | entity | Runner-proposed route awaiting evidence and, separately, source backing. | `existing_contract` | high | `SRC-DOMAIN`, `SRC-INVOKE-ONTOLOGY` |
| `bw.entity.provider-activity` | external entity | One activity summary owned by the connected runner and eligible for selection. | `existing_contract` | high | `SRC-OPERATIONS`, `SRC-INVOKE-SPEC` |
| `bw.contract.geometry-use-consent` | consent contract | Versioned exact text covering retained redacted facts, ephemeral geometry use, derived private geometry, and excluded data. | `specified_new` | high | `SRC-INVOKE-SPEC` |
| `bw.event.runner-confirmation` | domain event | Explicit affirmation binding one principal, one SuggestedTrack, one provider activity, and one consent version/text. | `specified_new` | high | `SRC-INVOKE-ONTOLOGY`, `SRC-INVOKE-SPEC` |
| `bw.rule.activity-ownership` | business rule | Confirmation has no evidence authority until the provider activity is validated as owned by the authenticated principal. | `specified_new` | high | `SRC-INVOKE-SPEC` |
| `bw.evidence.activity-evidence-candidate` | evidence | Retained redacted activity facts attached to a SuggestedTrack for later review. | `existing_contract` | high | `SRC-DOMAIN`, `SRC-INVOKE-ONTOLOGY` |
| `bw.evidence.activity-geometry-sample` | ephemeral evidence | In-operation aligned `latlng`, distance, and time streams for one consented activity; never a persisted raw payload. | `specified_new` | high | `SRC-INVOKE-SPEC` |
| `bw.policy.geometry-privacy` | policy | Versioned filtering, simplification, retention, deletion, and visibility rules applied before geometry persistence. | `decision_required` | high | `SRC-INVOKE-ONTOLOGY`, `SRC-INVOKE-SPEC` |
| `bw.evidence.geometry-candidate` | evidence | Privacy-filtered private route shape derived from a consented owned activity. | `specified_new` | high | `SRC-INVOKE-ONTOLOGY`, `SRC-INVOKE-SPEC` |
| `bw.policy.score-policy` | policy | Versioned score window, eligibility, normalization, aggregation, rounding, caps, and missing-data rules. | `decision_required` | high | `SRC-INVOKE-ONTOLOGY`, `SRC-INVOKE-SPEC` |
| `bw.value.activity-metric` | value object | Privacy-safe derived qualifying activity facts used inside one score-policy window. | `specified_new` | high | `SRC-INVOKE-SPEC` |
| `bw.evidence.score-input-snapshot` | evidence | Immutable canonical ordered policy-window inputs and provenance bound to exact geometry and policy digests. | `specified_new` | high | `SRC-INVOKE-ONTOLOGY`, `SRC-INVOKE-SPEC` |
| `bw.read-model.score-component-explanation` | read model | Named pace, distance, and frequency inputs, points, missing-data state, and limitation copy. | `specified_new` | high | `SRC-INVOKE-SPEC` |
| `bw.read-model.score-preview` | read model | Explained non-authoritative result calculated from one canonical snapshot under one policy. | `specified_new` | high | `SRC-INVOKE-ONTOLOGY`, `SRC-INVOKE-SPEC` |
| `bw.outcome.preliminary-score-visible` | outcome | Runner can see a labelled preliminary result in the web page without a control or promotion claim. | `specified_new` | high | `SRC-INVOKE-SPEC` |
| `bw.promoted-state.source-backed-track` | promoted state | SuggestedTrack whose source or geometry evidence was separately accepted by an operator. | `excluded` | high | `SRC-DOMAIN`, `SRC-STATES`, `SRC-INVOKE-ONTOLOGY` |
| `bw.rule.preview-authority-ceiling` | constraint | Geometry remains `candidate_from_activity`, score remains `preview_only`, and neither changes track or territory authority. | `specified_new` | high | `SRC-INVOKE-ONTOLOGY`, `SRC-INVOKE-SPEC` |
| `bw.rule.evidence-mode` | rule | Every result names `fixture` or `real_strava`; evidence from one lane cannot prove the other. | `specified_new` | high | `SRC-INVOKE-SPEC` |

### Decision Nodes

| ID | Kind | Meaning | Maturity | Required owner output | Sources |
| --- | --- | --- | --- | --- | --- |
| `bw.decision.score-policy-v0` | decision | Ratify every numeric and historical input needed by `bw.policy.score-policy`. | `decision_required` | Pace target/floor, distance cap, geometry tolerance, window anchor/timezone, eligible activities, aggregation, self-sample rule, history consent, rounding, and incomplete-history behavior. | `SRC-INVOKE-SPEC` |
| `bw.decision.geometry-privacy-v0` | decision | Ratify every privacy and lifecycle parameter needed by `bw.policy.geometry-privacy`. | `decision_required` | Start/end filtering, simplification, private rendering metadata, retention, deletion, and active sink rules. | `SRC-INVOKE-SPEC` |
| `bw.decision.oauth-scope-v0` | decision | Ratify the provider scope contract for a real Strava lane. | `deferred` | Required/accepted scopes and treatment of private activities. | `SRC-INVOKE-SPEC` |

### Operation Nodes

| ID | Kind | Meaning | Maturity | Sources |
| --- | --- | --- | --- | --- |
| `bw.operation.authenticate-via-strava` | operation | Start OAuth, validate callback state/scope, bind provider account, and establish session. | `existing_contract` | `SRC-INVOKE-SPEC` |
| `bw.operation.select-suggested-track` | operation | Create or explicitly select the exact track carried through the journey. | `existing_contract` | `SRC-DOMAIN`, `SRC-OPERATIONS`, `SRC-INVOKE-SPEC` |
| `bw.operation.select-provider-activity` | operation | Select one redacted current activity owned by the connected runner. | `existing_contract` | `SRC-OPERATIONS`, `SRC-UI` |
| `bw.operation.confirm-track-with-activity` | operation | Submit exact unchecked-by-default consent and create a pending confirmation intent. | `specified_new` | `SRC-INVOKE-SPEC` |
| `bw.operation.attach-activity-evidence` | operation | Persist evidence and transition the track only after ownership validation. | `existing_contract` | `SRC-OPERATIONS`, `SRC-INVOKE-SPEC` |
| `bw.operation.fetch-selected-activity-geometry` | operation | Fetch selected detail/streams ephemerally after ownership and consent checks. | `specified_new` | `SRC-INVOKE-SPEC` |
| `bw.operation.derive-geometry-candidate` | operation | Validate, filter, simplify, digest, and persist private candidate geometry. | `specified_new` | `SRC-INVOKE-SPEC` |
| `bw.operation.build-score-input-snapshot` | operation | Assemble canonical ordered window inputs and provenance without raw streams. | `specified_new` | `SRC-INVOKE-SPEC` |
| `bw.operation.calculate-score-preview` | operation | Deterministically calculate explained components and a permitted total from one snapshot. | `specified_new` | `SRC-INVOKE-SPEC` |
| `bw.operation.project-score-preview` | operation | Expose the authenticated preliminary result, evidence lane, and limitations. | `specified_new` | `SRC-INVOKE-SPEC` |

## System Node Registry

### Entry, Authentication, and Provider Boundary

| ID | Kind | Realization | Maturity | Evidence confidence | Sources |
| --- | --- | --- | --- | --- | --- |
| `sys.ui.login-page` | UI surface | Anonymous Strava connection entry. | `existing_contract` | high | `SRC-UI`, `SRC-INVOKE-SPEC` |
| `sys.endpoint.strava-oauth-start` | endpoint | `GET /api/auth/strava/start`. | `existing_contract` | high | `SRC-INVOKE-SPEC` |
| `sys.endpoint.strava-oauth-callback` | endpoint | `GET /api/auth/strava/callback`. | `existing_contract` | high | `SRC-INVOKE-SPEC` |
| `sys.component.browser-session` | component | Signed authenticated session and principal binding. | `existing_contract` | high | `SRC-INVOKE-ONTOLOGY` |
| `sys.component.csrf-guard` | component | CSRF/origin protection for browser mutations. | `existing_contract` | high | `SRC-INTERFACES`, `SRC-INVOKE-SPEC` |
| `sys.component.strava-oauth-adapter` | component | OAuth exchange and provider-account binding. | `existing_contract` | high | `SRC-INVOKE-ONTOLOGY` |
| `sys.store.provider-account` | store | Protected provider identity and token binding. | `existing_contract` | medium | `SRC-INVOKE-SPEC` |
| `sys.service.protected-token` | service | Server-side token decrypt, scope validation, refresh, and race-safe update. | `deferred` | high | `SRC-INVOKE-SPEC` |
| `sys.endpoint.activities-list` | endpoint | `GET /api/activities` redacted summaries. | `existing_contract` | high | `SRC-INVOKE-SPEC` |
| `sys.gateway.activity-list` | gateway | Authenticated activity-summary provider boundary. | `existing_contract` | high | `SRC-INVOKE-ONTOLOGY` |
| `sys.adapter.fixture-provider` | adapter | Deterministic Strava-shaped activity, history, detail, stream, and failure fixtures for L0. | `specified_new` | high | `SRC-INVOKE-SPEC` |
| `sys.adapter.real-strava` | adapter | Non-fake list/detail/streams gateway under accepted scope. | `deferred` | high | `SRC-INVOKE-SPEC` |

### Track, Consent, and Journey Boundary

| ID | Kind | Realization | Maturity | Evidence confidence | Sources |
| --- | --- | --- | --- | --- | --- |
| `sys.endpoint.suggested-track-list-create` | endpoint | `GET/POST /api/suggested-tracks`. | `existing_contract` | high | `SRC-INTERFACES` |
| `sys.store.suggested-track` | store | Memory/Postgres SuggestedTrack persistence. | `existing_contract` | high | `SRC-INTERFACES` |
| `sys.ui.track-workspace` | UI surface | Connected home SuggestedTrack region. | `existing_contract` | high | `SRC-UI` |
| `sys.ui.track-selector` | UI control | Explicit track selection with no implicit first-item fallback. | `specified_new` | high | `SRC-INVOKE-SPEC` |
| `sys.ui.activity-selector` | UI control | Redacted activity chooser bound to the selected track. | `existing_contract` | high | `SRC-UI`, `SRC-INVOKE-SPEC` |
| `sys.ui.geometry-consent-control` | UI control | Visible unchecked exact consent statement and affirmative control. | `specified_new` | high | `SRC-INVOKE-SPEC` |
| `sys.schema.runner-confirmation` | schema | Typed principal/track/activity/consent pending intent and accepted confirmation. | `specified_new` | high | `SRC-INVOKE-SPEC` |
| `sys.service.consent-command-validator` | service | Checks affirmation, exact displayed text/version, track binding, activity binding, session, and CSRF. | `specified_new` | high | `SRC-INVOKE-SPEC` |
| `sys.service.activity-ownership-validator` | service | Validates current provider-account ownership before evidence mutation. | `specified_new` | high | `SRC-INVOKE-SPEC` |
| `sys.service.score-preview-journey-orchestrator` | service | Idempotent staged confirmation-to-preview coordinator with resumable recovery. | `specified_new` | high | `SRC-INVOKE-SPEC` |
| `sys.endpoint.score-preview-journey-command` | endpoint | `POST /api/suggested-tracks/{id}/score-preview-journeys`. | `specified_new` | high | `SRC-INVOKE-SPEC` |
| `sys.endpoint.score-preview-journey-read` | endpoint | `GET /api/score-preview-journeys/{journeyId}`. | `specified_new` | high | `SRC-INVOKE-SPEC` |
| `sys.endpoint.score-preview-read` | endpoint | `GET /api/suggested-tracks/{id}/score-preview`. | `specified_new` | high | `SRC-INVOKE-SPEC` |
| `sys.store.activity-evidence` | store | Redacted ActivityEvidenceCandidate persistence after ownership acceptance. | `existing_contract` | high | `SRC-INTERFACES`, `SRC-INVOKE-SPEC` |

### Geometry, Score, Projection, and Evidence

| ID | Kind | Realization | Maturity | Evidence confidence | Sources |
| --- | --- | --- | --- | --- | --- |
| `sys.gateway.activity-geometry` | gateway | Selected activity detail and aligned stream acquisition. | `specified_new` | high | `SRC-INVOKE-ONTOLOGY`, `SRC-INVOKE-SPEC` |
| `sys.service.geometry-normalizer` | service | Validation, privacy filtering, simplification, metrics, encoding, and digest. | `specified_new` | high | `SRC-INVOKE-ONTOLOGY`, `SRC-INVOKE-SPEC` |
| `sys.schema.geometry-candidate` | schema | Persistable private GeometryCandidate contract. | `specified_new` | high | `SRC-INVOKE-SPEC` |
| `sys.store.geometry-candidate` | store | Principal-private derived geometry persistence. | `specified_new` | high | `SRC-INVOKE-SPEC` |
| `sys.registry.score-policy` | registry | Exact policy bytes, stable ID/version, and digest verification. | `decision_required` | high | `SRC-INVOKE-SPEC` |
| `sys.service.score-input-assembler` | service | Eligibility, window, derivation, ordering, aggregation inputs, and provenance assembly. | `decision_required` | high | `SRC-INVOKE-ONTOLOGY`, `SRC-INVOKE-SPEC` |
| `sys.schema.score-input-snapshot` | schema | Canonical immutable ScoreInputSnapshot contract. | `specified_new` | high | `SRC-INVOKE-SPEC` |
| `sys.store.score-input-snapshot` | store | Exact canonical snapshot persistence. | `specified_new` | high | `SRC-INVOKE-SPEC` |
| `sys.service.score-preview-calculator` | service | Pure deterministic policy-bound component and total calculation. | `decision_required` | high | `SRC-INVOKE-ONTOLOGY`, `SRC-INVOKE-SPEC` |
| `sys.schema.score-preview` | schema | Preview result, comparison class, limitations, evidence mode, and authority. | `specified_new` | high | `SRC-INVOKE-SPEC` |
| `sys.store.score-preview` | store | Idempotent partial or complete preview persistence. | `specified_new` | high | `SRC-INVOKE-SPEC` |
| `sys.projection.score-preview` | projection | Authenticated latest journey and score read model. | `specified_new` | high | `SRC-INVOKE-ONTOLOGY`, `SRC-INVOKE-SPEC` |
| `sys.ui.score-preview-card` | UI surface | Responsive preliminary total/components/limitations display. | `specified_new` | high | `SRC-INVOKE-SPEC` |
| `sys.evidence.prototype-receipt` | evidence | Provider mode, policy/snapshot/geometry digests, selectors, result, scans, and claim ceiling. | `specified_new` | high | `SRC-INVOKE-ONTOLOGY`, `SRC-INVOKE-SPEC` |
| `sys.control.raw-stream-sink-scan` | control | Separate canary checks for persistence, application/error logs, test snapshots, and receipts. | `specified_new` | high | `SRC-INVOKE-SPEC` |

### Verification Nodes

| ID | Kind | Realization | Maturity | Sources |
| --- | --- | --- | --- | --- |
| `sys.test.repository-contract` | test | Memory/Postgres round-trip, unique constraints, ownership rejection, and raw-field absence. | `specified_new` | `SRC-INVOKE-SPEC` |
| `sys.test.fixture-gateway` | test | Deterministic owned/unowned, complete-window, geometry, scope, and provider-failure fixtures. | `specified_new` | `SRC-INVOKE-SPEC` |
| `sys.test.geometry-normalizer` | test | Valid, malformed, misaligned, implausible, filtered, and deterministic geometry cases. | `specified_new` | `SRC-INVOKE-SPEC` |
| `sys.test.score-golden` | test | Policy/snapshot digest, component, cap, window, rounding, and incomplete-history cases. | `specified_new` | `SRC-INVOKE-SPEC` |
| `sys.test.journey-api` | test | Consent, ownership ordering, idempotency, resume, partial success, and stable error controls. | `specified_new` | `SRC-INVOKE-SPEC` |
| `sys.test.browser-witness` | test | Login-to-score browser journey under responsive, text, keyboard, and recovery stress. | `specified_new` | `SRC-UI`, `SRC-INVOKE-SPEC` |
| `sys.test.authority-negative-control` | test | Blocks automatic source-backed, verified-control, pilot, release, or production mutation/copy. | `specified_new` | `SRC-INVOKE-SPEC` |

## Lifecycle State Node Registry

### Runner Connection

| ID | Meaning |
| --- | --- |
| `bw.state.runner.anonymous` | No Body War session. |
| `bw.state.runner.oauth-pending` | OAuth was initiated and callback state is pending. |
| `bw.state.runner.connected` | Provider account and Body War session are bound. |

```text
bw.state.runner.anonymous
  -> bw.state.runner.oauth-pending
  -> bw.state.runner.connected
```

### SuggestedTrack

| ID | Meaning | Prototype admission |
| --- | --- | --- |
| `bw.state.suggested-track.needs-evidence` | Suggestion has no accepted source-backed evidence. | yes |
| `bw.state.suggested-track.evidence-submitted` | At least one validated redacted candidate exists. | yes |
| `bw.state.suggested-track.operator-review` | Operator is reviewing candidate evidence. | no |
| `bw.state.suggested-track.source-backed` | Operator accepted source/geometry evidence. | no |
| `bw.state.suggested-track.retired` | Suggestion is inactive. | no |

```text
bw.state.suggested-track.needs-evidence
  -> bw.state.suggested-track.evidence-submitted
  -> bw.state.suggested-track.operator-review
  -> bw.state.suggested-track.source-backed

any active SuggestedTrack state -> bw.state.suggested-track.retired
```

Only the first transition is admitted by this prototype journey.

### RunnerConfirmation

| ID | Meaning |
| --- | --- |
| `bw.state.confirmation.pending` | Exact consent intent exists but ownership has not been accepted. |
| `bw.state.confirmation.accepted` | Ownership, consent, principal, track, and activity bindings passed. |
| `bw.state.confirmation.rejected` | A binding, ownership, consent, or security rule failed; no evidence transition occurred. |

```text
bw.state.confirmation.pending
  -> bw.state.confirmation.accepted | bw.state.confirmation.rejected
```

### GeometryCandidate

| ID | Meaning |
| --- | --- |
| `bw.state.geometry.absent` | No candidate exists for the accepted confirmation. |
| `bw.state.geometry.fetch-pending` | Ephemeral provider geometry acquisition is in progress. |
| `bw.state.geometry.derived-candidate` | Privacy-filtered principal-private candidate exists. |
| `bw.state.geometry.unavailable` | Provider geometry was absent or temporarily unavailable. |
| `bw.state.geometry.rejected` | Validation or privacy rules rejected the sample. |
| `bw.state.geometry.superseded` | A later valid derivation replaced the candidate for projection. |

```text
bw.state.geometry.absent
  -> bw.state.geometry.fetch-pending
  -> bw.state.geometry.derived-candidate
  -> bw.state.geometry.superseded

bw.state.geometry.fetch-pending
  -> bw.state.geometry.unavailable | bw.state.geometry.rejected
```

### ScoreInputSnapshot

| ID | Meaning |
| --- | --- |
| `bw.state.snapshot.unavailable` | Required policy, geometry, or eligible inputs are not present. |
| `bw.state.snapshot.build-pending` | Canonical input assembly is in progress. |
| `bw.state.snapshot.complete-window` | Snapshot contains the ratified complete policy window. |
| `bw.state.snapshot.single-activity-projection` | Snapshot contains only the geometry-seeding activity and cannot yield a comparable total. |
| `bw.state.snapshot.blocked` | Policy, digest, eligibility, consent, or input validation failed. |

```text
bw.state.snapshot.unavailable
  -> bw.state.snapshot.build-pending
  -> bw.state.snapshot.complete-window
     | bw.state.snapshot.single-activity-projection
     | bw.state.snapshot.blocked
```

### ScorePreview

| ID | Meaning |
| --- | --- |
| `bw.state.preview.unavailable` | No score projection exists. |
| `bw.state.preview.snapshot-pending` | Score waits for canonical snapshot assembly. |
| `bw.state.preview.calculation-pending` | Calculator accepted a complete or explicitly partial snapshot. |
| `bw.state.preview.available` | Explained comparable preview is available for a complete window. |
| `bw.state.preview.incomplete-projection` | Explained non-comparable partial projection is available; frequency and total are null. |
| `bw.state.preview.blocked-policy` | Policy is missing, stale, unratified, or tampered. |
| `bw.state.preview.blocked-geometry` | Required geometry is absent or rejected. |
| `bw.state.preview.failed` | Calculation failed after accepted inputs. |
| `bw.state.preview.superseded` | A later calculation under new inputs or policy replaced the projection. |

```text
bw.state.preview.unavailable
  -> bw.state.preview.snapshot-pending
  -> bw.state.preview.calculation-pending
  -> bw.state.preview.available
     | bw.state.preview.incomplete-projection
     | bw.state.preview.failed

bw.state.preview.snapshot-pending
  -> bw.state.preview.blocked-policy | bw.state.preview.blocked-geometry

bw.state.preview.available
  -> bw.state.preview.superseded
```

### Resumable Journey

| ID | Meaning |
| --- | --- |
| `bw.state.journey.accepted` | Command passed session, CSRF, and exact consent-shape checks. |
| `bw.state.journey.ownership-validated` | Selected activity ownership passed. |
| `bw.state.journey.evidence-attached` | Redacted evidence and allowed SuggestedTrack transition persisted. |
| `bw.state.journey.geometry-derived` | Private GeometryCandidate persisted or idempotently reused. |
| `bw.state.journey.snapshot-built` | Canonical ScoreInputSnapshot persisted or reused. |
| `bw.state.journey.preview-available` | Complete or explicitly partial ScorePreview is readable. |
| `bw.state.journey.recoverable-failure` | A completed earlier stage is preserved and a later stage may safely resume. |
| `bw.state.journey.blocked` | Security, authority, policy, or non-recoverable validation rule stopped progression. |

```text
bw.state.journey.accepted
  -> bw.state.journey.ownership-validated
  -> bw.state.journey.evidence-attached
  -> bw.state.journey.geometry-derived
  -> bw.state.journey.snapshot-built
  -> bw.state.journey.preview-available

any accepted stage
  -> bw.state.journey.recoverable-failure
  -> resume from the last accepted stage

any stage -> bw.state.journey.blocked
```

## Business Relationships

| From | Edge | To | Rule |
| --- | --- | --- | --- |
| `bw.actor.anonymous-visitor` | `enters` | `bw.surface.login-entry` | Anonymous visitor sees no connected workspace. |
| `bw.actor.runner` | `initiates` | `bw.operation.authenticate-via-strava` | Runner explicitly starts provider connection. |
| `bw.actor.runner` | `becomes` | `bw.role.connected-runner` | Valid callback plus Body War session. |
| `bw.role.connected-runner` | `enters` | `bw.surface.connected-track-workspace` | Session-gated surface. |
| `bw.role.connected-runner` | `creates` | `bw.entity.suggested-track` | Creation starts `needs-evidence`. |
| `bw.role.connected-runner` | `selects` | `bw.entity.suggested-track` | Exact ID persists through the journey. |
| `bw.role.connected-runner` | `selects` | `bw.entity.provider-activity` | Activity comes from the current runner list. |
| `bw.role.connected-runner` | `affirms` | `bw.contract.geometry-use-consent` | Affirmative control is unchecked by default. |
| `bw.operation.confirm-track-with-activity` | `produces` | `bw.event.runner-confirmation` | Confirmation begins as pending intent. |
| `bw.event.runner-confirmation` | `binds` | `bw.entity.suggested-track` | Exact track, never implicit first item. |
| `bw.event.runner-confirmation` | `binds` | `bw.entity.provider-activity` | Exact selected activity. |
| `bw.event.runner-confirmation` | `binds` | `bw.contract.geometry-use-consent` | Displayed, affirmed, transmitted, and persisted text/version match. |
| `bw.rule.activity-ownership` | `validates` | `bw.event.runner-confirmation` | Rejection produces no evidence or track transition. |
| `bw.operation.attach-activity-evidence` | `produces` | `bw.evidence.activity-evidence-candidate` | Only after accepted ownership. |
| `bw.evidence.activity-evidence-candidate` | `supports` | `bw.evidence.geometry-candidate` | Exact consented activity binding. |
| `bw.operation.fetch-selected-activity-geometry` | `produces` | `bw.evidence.activity-geometry-sample` | Raw stream lifetime is operation-scoped. |
| `bw.policy.geometry-privacy` | `governs` | `bw.operation.derive-geometry-candidate` | Filter before encoding or persistence. |
| `bw.operation.derive-geometry-candidate` | `produces` | `bw.evidence.geometry-candidate` | Authority fixed to candidate, visibility fixed private. |
| `bw.evidence.geometry-candidate` | `contributes_to` | `bw.evidence.score-input-snapshot` | Exact geometry ID and digest. |
| `bw.value.activity-metric` | `contributes_to` | `bw.evidence.score-input-snapshot` | Canonically ordered derived metrics only. |
| `bw.policy.score-policy` | `governs` | `bw.operation.build-score-input-snapshot` | Window and eligibility are policy-bound. |
| `bw.operation.build-score-input-snapshot` | `produces` | `bw.evidence.score-input-snapshot` | Complete-window and partial-history states remain distinct. |
| `bw.policy.score-policy` | `governs` | `bw.operation.calculate-score-preview` | Numeric output blocks until policy ratification. |
| `bw.evidence.score-input-snapshot` | `contributes_to` | `bw.read-model.score-preview` | Calculator consumes exactly one canonical snapshot. |
| `bw.operation.calculate-score-preview` | `produces` | `bw.read-model.score-preview` | Authority fixed to `preview_only`. |
| `bw.read-model.score-component-explanation` | `explains` | `bw.read-model.score-preview` | Components disclose inputs, points, and missing evidence. |
| `bw.operation.project-score-preview` | `displays` | `bw.surface.score-preview-card` | Authenticated runner only. |
| `bw.surface.score-preview-card` | `produces` | `bw.outcome.preliminary-score-visible` | Preliminary, explained, and limitation-labelled. |
| `bw.rule.preview-authority-ceiling` | `governs` | `bw.read-model.score-preview` | Preview never decides track or territory control. |
| `bw.read-model.score-preview` | `does_not_promote` | `bw.promoted-state.source-backed-track` | Separate operator-owned promotion remains required. |
| `bw.rule.evidence-mode` | `governs` | `bw.read-model.score-preview` | Fixture and real-provider claims remain separate. |

## System Relationships

| From | Edge | To | Contract |
| --- | --- | --- | --- |
| `sys.ui.login-page` | `invokes` | `sys.endpoint.strava-oauth-start` | Explicit runner action. |
| `sys.endpoint.strava-oauth-start` | `invokes` | `sys.component.strava-oauth-adapter` | State and requested scope are server-bound. |
| `sys.component.strava-oauth-adapter` | `invokes` | `sys.endpoint.strava-oauth-callback` | Callback verifies provider response and state. |
| `sys.endpoint.strava-oauth-callback` | `writes` | `sys.store.provider-account` | Protected provider binding. |
| `sys.endpoint.strava-oauth-callback` | `writes` | `sys.component.browser-session` | Authenticated principal session. |
| `sys.component.browser-session` | `authorizes` | `sys.endpoint.activities-list` | `body-war.activity.read`. |
| `sys.component.browser-session` | `authorizes` | `sys.endpoint.suggested-track-list-create` | SuggestedTrack read/create permissions. |
| `sys.component.csrf-guard` | `authorizes` | `sys.endpoint.score-preview-journey-command` | Browser mutation protection. |
| `sys.endpoint.activities-list` | `invokes` | `sys.gateway.activity-list` | Redacted summaries only. |
| `sys.adapter.fixture-provider` | `implements` | `sys.gateway.activity-list` | Explicit L0 provider mode. |
| `sys.adapter.fixture-provider` | `implements` | `sys.gateway.activity-geometry` | Deterministic detail/stream and history fixtures. |
| `sys.adapter.real-strava` | `implements` | `sys.gateway.activity-list` | Deferred non-fake provider lane. |
| `sys.adapter.real-strava` | `implements` | `sys.gateway.activity-geometry` | Deferred non-fake detail/streams lane. |
| `sys.service.protected-token` | `authorizes` | `sys.adapter.real-strava` | Server-only accepted-scope token lifecycle. |
| `sys.ui.track-workspace` | `invokes` | `sys.endpoint.suggested-track-list-create` | List/create suggestions. |
| `sys.endpoint.suggested-track-list-create` | `reads` | `sys.store.suggested-track` | Connected-runner list. |
| `sys.endpoint.suggested-track-list-create` | `writes` | `sys.store.suggested-track` | New `needs_evidence` suggestion. |
| `sys.ui.track-selector` | `feeds` | `sys.ui.activity-selector` | Exact non-first track ID is retained. |
| `sys.ui.activity-selector` | `reads` | `sys.endpoint.activities-list` | Current redacted summaries. |
| `sys.ui.geometry-consent-control` | `invokes` | `sys.endpoint.score-preview-journey-command` | Exact track/activity/text/version command. |
| `sys.endpoint.score-preview-journey-command` | `invokes` | `sys.service.score-preview-journey-orchestrator` | One durable public mutation boundary. |
| `sys.service.score-preview-journey-orchestrator` | `invokes` | `sys.service.consent-command-validator` | Validate before pending intent admission. |
| `sys.service.consent-command-validator` | `validates` | `sys.schema.runner-confirmation` | Principal, track, activity, consent, CSRF. |
| `sys.service.score-preview-journey-orchestrator` | `invokes` | `sys.service.activity-ownership-validator` | Ownership before evidence mutation. |
| `sys.service.activity-ownership-validator` | `reads` | `sys.gateway.activity-list` | Current provider-account ownership. |
| `sys.service.score-preview-journey-orchestrator` | `writes` | `sys.store.activity-evidence` | Only after ownership acceptance. |
| `sys.service.score-preview-journey-orchestrator` | `invokes` | `sys.gateway.activity-geometry` | Fetch selected consented activity. |
| `sys.gateway.activity-geometry` | `feeds` | `sys.service.geometry-normalizer` | Ephemeral aligned streams. |
| `sys.service.geometry-normalizer` | `validates` | `sys.schema.geometry-candidate` | Privacy-filtered persistable output only. |
| `sys.service.score-preview-journey-orchestrator` | `writes` | `sys.store.geometry-candidate` | Idempotent private candidate. |
| `sys.registry.score-policy` | `feeds` | `sys.service.score-input-assembler` | Verified policy bytes and digest. |
| `sys.store.geometry-candidate` | `feeds` | `sys.service.score-input-assembler` | Exact geometry and digest. |
| `sys.gateway.activity-geometry` | `feeds` | `sys.service.score-input-assembler` | Policy-eligible privacy-safe derived history metrics. |
| `sys.service.score-input-assembler` | `validates` | `sys.schema.score-input-snapshot` | Canonical ordering and provenance. |
| `sys.service.score-preview-journey-orchestrator` | `writes` | `sys.store.score-input-snapshot` | One immutable snapshot per accepted input identity. |
| `sys.store.score-input-snapshot` | `feeds` | `sys.service.score-preview-calculator` | Exact snapshot only. |
| `sys.registry.score-policy` | `feeds` | `sys.service.score-preview-calculator` | Exact matching policy/digest. |
| `sys.service.score-preview-calculator` | `validates` | `sys.schema.score-preview` | Component, total, comparison, limitation, and authority invariants. |
| `sys.service.score-preview-journey-orchestrator` | `writes` | `sys.store.score-preview` | Idempotent complete or partial result. |
| `sys.endpoint.score-preview-journey-read` | `reads` | `sys.projection.score-preview` | Accepted stage and recovery state. |
| `sys.endpoint.score-preview-read` | `reads` | `sys.projection.score-preview` | Latest current-runner projection. |
| `sys.store.score-preview` | `projects` | `sys.projection.score-preview` | Score and explanation read model. |
| `sys.projection.score-preview` | `projects` | `sys.ui.score-preview-card` | Preliminary score, evidence mode, and limitations. |
| `sys.service.score-preview-calculator` | `observes` | `sys.evidence.prototype-receipt` | Input/output and policy digests. |
| `sys.control.raw-stream-sink-scan` | `scans` | `sys.store.geometry-candidate` | No raw provider streams. |
| `sys.control.raw-stream-sink-scan` | `scans` | `sys.evidence.prototype-receipt` | No raw provider streams or secrets. |
| `sys.test.repository-contract` | `tests` | `sys.store.score-input-snapshot` | Memory/Postgres parity and raw-field absence. |
| `sys.test.fixture-gateway` | `tests` | `sys.adapter.fixture-provider` | Deterministic positive and negative provider cases. |
| `sys.test.geometry-normalizer` | `tests` | `sys.service.geometry-normalizer` | Geometry and privacy invariants. |
| `sys.test.score-golden` | `tests` | `sys.service.score-preview-calculator` | Deterministic policy/snapshot calculation. |
| `sys.test.journey-api` | `tests` | `sys.service.score-preview-journey-orchestrator` | Ordering, idempotency, recovery, and authority. |
| `sys.test.browser-witness` | `tests` | `sys.ui.score-preview-card` | Browser-visible local fixture journey. |
| `sys.test.authority-negative-control` | `tests` | `sys.schema.score-preview` | No promotion/control authority. |

## Business-to-System Bridges

| Business node | Edge | System node | Alignment evidence | Current disposition |
| --- | --- | --- | --- | --- |
| `bw.surface.login-entry` | `realized_by` | `sys.ui.login-page` | `SRC-UI`, `SRC-INVOKE-SPEC` | Existing contract. |
| `bw.operation.authenticate-via-strava` | `realized_by` | `sys.component.strava-oauth-adapter` | `SRC-INVOKE-ONTOLOGY`, `SRC-INVOKE-SPEC` | Existing structure; live witness deferred. |
| `bw.role.connected-runner` | `realized_by` | `sys.component.browser-session` | `SRC-INVOKE-ONTOLOGY` | Existing structure. |
| `bw.entity.suggested-track` | `realized_by` | `sys.store.suggested-track` | `SRC-DOMAIN`, `SRC-INTERFACES` | Existing contract. |
| `bw.surface.connected-track-workspace` | `realized_by` | `sys.ui.track-workspace` | `SRC-UI` | Existing contract. |
| `bw.entity.provider-activity` | `realized_by` | `sys.gateway.activity-list` | `SRC-OPERATIONS`, `SRC-INVOKE-ONTOLOGY` | Fixture-backed current boundary. |
| `bw.contract.geometry-use-consent` | `realized_by` | `sys.ui.geometry-consent-control` | `SRC-INVOKE-SPEC` | Specified; current UI contract excludes maps. |
| `bw.event.runner-confirmation` | `realized_by` | `sys.schema.runner-confirmation` | `SRC-INVOKE-SPEC` | Specified, not implementation-evidenced. |
| `bw.rule.activity-ownership` | `realized_by` | `sys.service.activity-ownership-validator` | `SRC-INVOKE-SPEC` | Specified, not implementation-evidenced. |
| `bw.evidence.activity-evidence-candidate` | `realized_by` | `sys.store.activity-evidence` | `SRC-DOMAIN`, `SRC-INTERFACES` | Existing contract; ordering must be hardened. |
| `bw.evidence.activity-geometry-sample` | `realized_by` | `sys.gateway.activity-geometry` | `SRC-INVOKE-SPEC` | Specified ephemeral boundary. |
| `bw.policy.geometry-privacy` | `realized_by` | `sys.service.geometry-normalizer` | `SRC-INVOKE-SPEC` | Blocked on `bw.decision.geometry-privacy-v0`. |
| `bw.evidence.geometry-candidate` | `realized_by` | `sys.schema.geometry-candidate` | `SRC-INVOKE-SPEC` | Specified, not implementation-evidenced. |
| `bw.policy.score-policy` | `realized_by` | `sys.registry.score-policy` | `SRC-INVOKE-SPEC` | Blocked on `bw.decision.score-policy-v0`. |
| `bw.evidence.score-input-snapshot` | `realized_by` | `sys.schema.score-input-snapshot` | `SRC-INVOKE-SPEC` | Specified, not implementation-evidenced. |
| `bw.read-model.score-preview` | `realized_by` | `sys.schema.score-preview` | `SRC-INVOKE-SPEC` | Specified, not implementation-evidenced. |
| `bw.read-model.score-component-explanation` | `realized_by` | `sys.projection.score-preview` | `SRC-INVOKE-SPEC` | Specified, not implementation-evidenced. |
| `bw.surface.score-preview-card` | `realized_by` | `sys.ui.score-preview-card` | `SRC-INVOKE-SPEC` | Specified, not implementation-evidenced. |
| `bw.journey.login-to-score-preview` | `realized_by` | `sys.service.score-preview-journey-orchestrator` | `SRC-INVOKE-SPEC` | Specified resumable boundary. |
| `bw.journey.login-to-score-preview` | `tested_by` | `sys.test.browser-witness` | `SRC-INVOKE-SPEC` | Planned local witness. |
| `bw.rule.preview-authority-ceiling` | `tested_by` | `sys.test.authority-negative-control` | `SRC-INVOKE-SPEC` | Required negative control. |
| `bw.rule.evidence-mode` | `observed_by` | `sys.evidence.prototype-receipt` | `SRC-INVOKE-ONTOLOGY`, `SRC-INVOKE-SPEC` | Receipt must name exact lane. |
| `bw.actor.strava-provider` | `realized_by` | `sys.adapter.real-strava` | `SRC-INVOKE-SPEC` | Deferred L2; fixture evidence cannot satisfy it. |
| `bw.evidence.geometry-candidate` | `constrained_by` | `sys.control.raw-stream-sink-scan` | `SRC-INVOKE-SPEC` | All active sinks must close. |
| `bw.read-model.score-preview` | `depends_on` | `sys.service.score-input-assembler` | `SRC-INVOKE-ONTOLOGY`, `SRC-INVOKE-SPEC` | Complete-window comparison requires canonical snapshot. |

## Drift and Evidence Gaps

| ID | Business expectation | Observed/current contract | Required closure |
| --- | --- | --- | --- |
| `ONT-JSP-001` | Geometry use requires exact affirmative consent. | Current UI/operation contract says maps are excluded and stores only redacted summary consent. | Adopt `bw.contract.geometry-use-consent` into DomainSpec and implement unchecked exact binding. |
| `ONT-JSP-002` | Selected activity geometry is available only after consent and ownership. | Current activity-summary boundary omits geometry. | Add `sys.gateway.activity-geometry`; keep list redacted. |
| `ONT-JSP-003` | Private candidate geometry has a typed schema, state, repository, and privacy policy. | No current feature contract defines geometry persistence. | Ratify `bw.decision.geometry-privacy-v0`, then adopt and implement geometry nodes. |
| `ONT-JSP-004` | Numeric output is governed by a complete versioned ScorePolicy. | Only weights, a 14-day window, and cap are known; normalizers and aggregation are open. | Ratify `bw.decision.score-policy-v0`. |
| `ONT-JSP-005` | A comparable preview consumes a canonical complete-window snapshot. | No current feature contract or implementation node owns canonical score inputs. | Adopt and implement ScoreInputSnapshot nodes; partial history must have null frequency/total. |
| `ONT-JSP-006` | Browser shows an explained `preview_only` score. | Current UI forbids `verified scoring` and has no score projection. | Adopt preview semantics and implement the labelled score card without verified/control copy. |
| `ONT-JSP-007` | Real-provider claims require non-fake list/detail/history plus secure token lifecycle. | Candidate map reports a synthetic activity adapter despite OAuth structure. | Defer until `bw.decision.oauth-scope-v0`, protected token service, real adapter, admission, and supervised witness. |
| `ONT-JSP-008` | Candidate geometry and score never promote track/game authority. | Existing lifecycle contains later `source_backed`; accidental coupling would cross owner authority. | Preserve separate state machines and authority-negative controls. |
| `ONT-JSP-009` | DomainSpec contracts use this ontology's exact node meanings. | `domain.md`, `states.md`, `operations.md`, `interfaces.md`, and `ui-spec.md` predate this complete ontology. | Run a separate ontology-to-DomainSpec adoption after decisions are recorded. |
| `ONT-JSP-010` | System nodes marked `specified_new` have implementation and test evidence before conformance is claimed. | This ontology run does not inspect or mutate application code. | Implement through selected SWUs and attach exact receipts; do not infer conformance from this file. |

## Journey Coverage

| Stage | Business node | System node | Maturity | Next closure |
| --- | --- | --- | --- | --- |
| Login entry | `bw.surface.login-entry` | `sys.ui.login-page` | existing contract | Preserve during DomainSpec adoption. |
| OAuth start/callback | `bw.operation.authenticate-via-strava` | `sys.component.strava-oauth-adapter` | existing structure | Keep real-provider proof deferred. |
| Connected session | `bw.role.connected-runner` | `sys.component.browser-session` | existing structure | Preserve principal binding. |
| Track create/select | `bw.entity.suggested-track` | `sys.ui.track-selector` | mixed | Add exact non-first selection contract. |
| Activity selection | `bw.entity.provider-activity` | `sys.ui.activity-selector` | existing contract | Bind exact selected track/activity. |
| Consent | `bw.contract.geometry-use-consent` | `sys.ui.geometry-consent-control` | specified new | Adopt exact versioned consent. |
| Ownership | `bw.rule.activity-ownership` | `sys.service.activity-ownership-validator` | specified new | Enforce before mutation. |
| Evidence | `bw.evidence.activity-evidence-candidate` | `sys.store.activity-evidence` | existing contract | Harden pending/accepted ordering. |
| Geometry fetch | `bw.evidence.activity-geometry-sample` | `sys.gateway.activity-geometry` | specified new | Keep raw streams ephemeral. |
| Geometry derivation | `bw.evidence.geometry-candidate` | `sys.service.geometry-normalizer` | decision plus implementation | Resolve privacy policy first. |
| Score inputs | `bw.evidence.score-input-snapshot` | `sys.service.score-input-assembler` | decision plus implementation | Resolve score policy first. |
| Score calculation | `bw.read-model.score-preview` | `sys.service.score-preview-calculator` | decision plus implementation | Deterministic fixture/golden controls. |
| Web projection | `bw.surface.score-preview-card` | `sys.ui.score-preview-card` | specified new | Responsive explained preliminary display. |
| Prototype proof | `bw.rule.evidence-mode` | `sys.evidence.prototype-receipt` | specified new | Local fixture receipt before human testing. |

All participant-visible stages have a business node, a system node, and at
least one bridge. This is ontology coverage, not implementation coverage.

## Future DomainSpec Adoption Map

| Ontology group | Future owner file | Required adoption |
| --- | --- | --- |
| Actors, roles, entities, evidence, value objects, policies, read models | [`domain.md`](domain.md) | Add exact fields, invariants, authority, visibility, and decision references. |
| Lifecycle state nodes and transition exclusions | [`states.md`](states.md) | Add confirmation, geometry, snapshot, preview, and resumable journey machines. |
| Operation nodes and business rules | [`operations.md`](operations.md) | Add preconditions, ordering, idempotency, privacy, calculation, and failure semantics. |
| Endpoints, gateways, services, stores, schemas, and read boundaries | [`interfaces.md`](interfaces.md) | Add command/read API and internal provider/calculation contracts. |
| Login, selection, consent, recovery, private geometry cue, score card, copy | [`ui-spec.md`](ui-spec.md) | Add exact interaction, accessibility, responsive, evidence-mode, and authority language. |

DomainSpec adoption must preserve ontology IDs in headings or traceability
tables so implementation artifacts can link back without redefining meaning.

## Ontology Completion Gate

The ontology baseline is structurally complete when:

1. every node ID is unique;
2. every relationship endpoint names a registered node;
3. every participant-visible journey stage has business, system, and bridge coverage;
4. every specified system node is labelled without claiming implementation;
5. `bw.decision.score-policy-v0` and `bw.decision.geometry-privacy-v0` remain open rather than receiving invented defaults;
6. all geometry and score nodes preserve private-candidate and `preview_only` authority;
7. fixture and real-provider evidence lanes remain distinct;
8. DomainSpec adoption and application implementation remain `not-run`.
