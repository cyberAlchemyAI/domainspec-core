# Body War Business Ontology Node Index

Status: `generated-projection`

This is a human review projection. The individual JSON records in `nodes/`
are the validated candidate node surface. This index has no authority effect.

Start with [Business Ontology Views](BUSINESS-VIEWS.md) for arrow-based
capability, journey, evidence, territory, progression, and lifecycle maps.
Return here when you need the exhaustive node catalog.

## Validation summary

- Nodes: 237
- Relations: 231
- Lifecycle policies: 11
- Residue items: 6
- Receipt status: `pass`
- Authority effect: `none`

### Nodes by business kind

| Business kind | Count |
| --- | ---: |
| `actor` | 12 |
| `bounded_context` | 12 |
| `capability` | 18 |
| `entity` | 16 |
| `event` | 18 |
| `external_system` | 1 |
| `interface` | 4 |
| `ledger` | 1 |
| `lifecycle_state` | 58 |
| `metric` | 3 |
| `operation` | 32 |
| `outcome` | 2 |
| `policy` | 11 |
| `premise` | 10 |
| `query` | 17 |
| `value_object` | 17 |
| `workflow` | 5 |

### Nodes by candidate status

| Candidate status | Count |
| --- | ---: |
| `blocked` | 29 |
| `candidate` | 31 |
| `deferred` | 12 |
| `reviewed-candidate` | 165 |

## Login to ScorePreview chain

| Step | Concept | Kind | Status | Resolution gate |
| ---: | --- | --- | --- | --- |
| 1 | [Anonymous Visitor](nodes/actor.anonymous-visitor.json) | `actor` | `reviewed-candidate` | `body-war.product-ontology-review` |
| 2 | [Authenticate Via Strava](nodes/operation.authenticate-via-strava.json) | `operation` | `reviewed-candidate` | `body-war.product-ontology-review` |
| 3 | [Connected Runner](nodes/actor.connected-runner.json) | `actor` | `reviewed-candidate` | `body-war.product-ontology-review` |
| 4 | [Select SuggestedTrack](nodes/operation.select-suggested-track.json) | `operation` | `candidate` | `body-war.product-ontology-review` |
| 5 | [SuggestedTrack](nodes/entity.suggested-track.json) | `entity` | `reviewed-candidate` | `body-war.product-ontology-review` |
| 6 | [Confirm Track With Activity](nodes/operation.confirm-track-with-activity.json) | `operation` | `candidate` | `body-war.product-ontology-review` |
| 7 | [RunnerConfirmation](nodes/entity.runner-confirmation.json) | `entity` | `candidate` | `body-war.product-ontology-review` |
| 8 | [ActivityEvidenceCandidate](nodes/entity.activity-evidence-candidate.json) | `entity` | `reviewed-candidate` | `body-war.product-ontology-review` |
| 9 | [Fetch Selected Activity Geometry](nodes/operation.fetch-selected-activity-geometry.json) | `operation` | `blocked` | `decision-gate` |
| 10 | [ActivityGeometrySample](nodes/value.activity-geometry-sample.json) | `value_object` | `blocked` | `decision-gate` |
| 11 | [Derive GeometryCandidate](nodes/operation.derive-geometry-candidate.json) | `operation` | `blocked` | `decision-gate` |
| 12 | [GeometryCandidate](nodes/entity.geometry-candidate.json) | `entity` | `blocked` | `decision-gate` |
| 13 | [Build ScoreInputSnapshot](nodes/operation.build-score-input-snapshot.json) | `operation` | `blocked` | `decision-gate` |
| 14 | [ScoreInputSnapshot](nodes/value.score-input-snapshot.json) | `value_object` | `blocked` | `decision-gate` |
| 15 | [Calculate ScorePreview](nodes/operation.calculate-score-preview.json) | `operation` | `blocked` | `decision-gate` |
| 16 | [ScorePreview](nodes/outcome.score-preview.json) | `outcome` | `blocked` | `decision-gate` |
| 17 | [Project ScorePreview](nodes/operation.project-score-preview.json) | `operation` | `blocked` | `decision-gate` |

The blocked steps are intentionally present. A deterministic fixture can later
exercise them only after its exact policy inputs are selected; real-provider
geometry remains separately gated by privacy, scope, retention, and supervised
evidence.

## All nodes

| Concept | Label | Kind | Role | Status | Evidence | Commitment |
| --- | --- | --- | --- | --- | --- | --- |
| [`body-war.business.actor.anonymous-visitor`](nodes/actor.anonymous-visitor.json) | Anonymous Visitor | `actor` | authority object | `reviewed-candidate` | `high` | `high` |
| [`body-war.business.actor.anti-cheat-reviewer`](nodes/actor.anti-cheat-reviewer.json) | Anti-Cheat Reviewer | `actor` | workflow object | `reviewed-candidate` | `high` | `high` |
| [`body-war.business.actor.city-community-operator`](nodes/actor.city-community-operator.json) | City or Community Operator | `actor` | authority object | `deferred` | `high` | `low` |
| [`body-war.business.actor.clan-member`](nodes/actor.clan-member.json) | Clan Member | `actor` | authority object | `reviewed-candidate` | `high` | `high` |
| [`body-war.business.actor.connected-runner`](nodes/actor.connected-runner.json) | Connected Runner | `actor` | authority object | `reviewed-candidate` | `high` | `high` |
| [`body-war.business.actor.invader`](nodes/actor.invader.json) | Invader | `actor` | authority object | `reviewed-candidate` | `high` | `high` |
| [`body-war.business.actor.product-team`](nodes/actor.product-team.json) | Body War Product Team | `actor` | authority object | `reviewed-candidate` | `high` | `high` |
| [`body-war.business.actor.prototype-operator`](nodes/actor.prototype-operator.json) | Prototype Operator | `actor` | workflow object | `reviewed-candidate` | `high` | `high` |
| [`body-war.business.actor.runner`](nodes/actor.runner.json) | Runner | `actor` | authority object | `reviewed-candidate` | `high` | `high` |
| [`body-war.business.actor.sponsor-partner`](nodes/actor.sponsor-partner.json) | Sponsor Partner | `actor` | authority object | `deferred` | `high` | `low` |
| [`body-war.business.actor.track-policy-owner`](nodes/actor.track-policy-owner.json) | Track and Policy Owner | `actor` | authority object | `reviewed-candidate` | `high` | `high` |
| [`body-war.business.actor.zone-owner`](nodes/actor.zone-owner.json) | Zone Owner | `actor` | authority object | `reviewed-candidate` | `high` | `high` |
| [`body-war.business.context.activity-evidence`](nodes/context.activity-evidence.json) | Activity Evidence | `bounded_context` | authority object | `reviewed-candidate` | `high` | `high` |
| [`body-war.business.context.community`](nodes/context.community.json) | Community | `bounded_context` | authority object | `reviewed-candidate` | `high` | `high` |
| [`body-war.business.context.control-competition`](nodes/context.control-competition.json) | Control and Competition | `bounded_context` | authority object | `reviewed-candidate` | `high` | `high` |
| [`body-war.business.context.geometry-evidence`](nodes/context.geometry-evidence.json) | Candidate Geometry Evidence | `bounded_context` | authority object | `candidate` | `medium` | `medium` |
| [`body-war.business.context.identity-consent`](nodes/context.identity-consent.json) | Identity and Consent | `bounded_context` | authority object | `reviewed-candidate` | `high` | `high` |
| [`body-war.business.context.monetization-sponsored-zones`](nodes/context.monetization-sponsored-zones.json) | Monetization and Sponsored Zones | `bounded_context` | authority object | `deferred` | `high` | `low` |
| [`body-war.business.context.pilot-operations`](nodes/context.pilot-operations.json) | Pilot Operations | `bounded_context` | authority object | `reviewed-candidate` | `high` | `high` |
| [`body-war.business.context.progression`](nodes/context.progression.json) | Progression | `bounded_context` | authority object | `reviewed-candidate` | `high` | `high` |
| [`body-war.business.context.route-expansion`](nodes/context.route-expansion.json) | Suggested Track Route Expansion | `bounded_context` | authority object | `reviewed-candidate` | `high` | `high` |
| [`body-war.business.context.run-validation-anti-cheat`](nodes/context.run-validation-anti-cheat.json) | Run Validation and Anti-Cheat | `bounded_context` | authority object | `reviewed-candidate` | `high` | `high` |
| [`body-war.business.context.score-preview`](nodes/context.score-preview.json) | Score Preview | `bounded_context` | authority object | `blocked` | `medium` | `low` |
| [`body-war.business.context.territory-catalog`](nodes/context.territory-catalog.json) | Territory Catalog | `bounded_context` | authority object | `reviewed-candidate` | `high` | `high` |
| [`body-war.business.capability.activity-geometry`](nodes/capability.activity-geometry.json) | Selected Activity Geometry | `capability` | workflow object | `blocked` | `medium` | `low` |
| [`body-war.business.capability.activity-import`](nodes/capability.activity-import.json) | Activity Import | `capability` | authority object | `reviewed-candidate` | `high` | `high` |
| [`body-war.business.capability.auth-consent`](nodes/capability.auth-consent.json) | Authentication and Consent | `capability` | authority object | `reviewed-candidate` | `high` | `high` |
| [`body-war.business.capability.challenges-missions`](nodes/capability.challenges-missions.json) | Challenges and Missions | `capability` | authority object | `reviewed-candidate` | `high` | `high` |
| [`body-war.business.capability.community-clans`](nodes/capability.community-clans.json) | Community and Clans | `capability` | authority object | `reviewed-candidate` | `high` | `high` |
| [`body-war.business.capability.control-ownership`](nodes/capability.control-ownership.json) | Control and Ownership | `capability` | authority object | `reviewed-candidate` | `high` | `high` |
| [`body-war.business.capability.economy`](nodes/capability.economy.json) | RunCoin and Premium Economy | `capability` | authority object | `deferred` | `high` | `low` |
| [`body-war.business.capability.evidence-candidate-attach`](nodes/capability.evidence-candidate-attach.json) | Evidence Candidate Attachment | `capability` | authority object | `reviewed-candidate` | `high` | `high` |
| [`body-war.business.capability.evidence-submission`](nodes/capability.evidence-submission.json) | Evidence Submission | `capability` | authority object | `reviewed-candidate` | `high` | `high` |
| [`body-war.business.capability.notifications`](nodes/capability.notifications.json) | Notifications | `capability` | authority object | `reviewed-candidate` | `high` | `high` |
| [`body-war.business.capability.pilot-operations`](nodes/capability.pilot-operations.json) | Pilot Operations Capability | `capability` | authority object | `reviewed-candidate` | `high` | `high` |
| [`body-war.business.capability.rankings-seasons`](nodes/capability.rankings-seasons.json) | Rankings and Seasons | `capability` | authority object | `reviewed-candidate` | `high` | `high` |
| [`body-war.business.capability.score-preview`](nodes/capability.score-preview.json) | Explained Score Preview | `capability` | projection object | `blocked` | `medium` | `low` |
| [`body-war.business.capability.score-xp`](nodes/capability.score-xp.json) | Score and XP | `capability` | authority object | `reviewed-candidate` | `high` | `high` |
| [`body-war.business.capability.sponsored-zones`](nodes/capability.sponsored-zones.json) | Sponsored Zones | `capability` | authority object | `deferred` | `high` | `low` |
| [`body-war.business.capability.suggested-track-creation`](nodes/capability.suggested-track-creation.json) | Suggested Track Creation | `capability` | authority object | `reviewed-candidate` | `high` | `high` |
| [`body-war.business.capability.suggested-track-discovery`](nodes/capability.suggested-track-discovery.json) | Suggested Track Discovery | `capability` | authority object | `reviewed-candidate` | `high` | `high` |
| [`body-war.business.capability.track-territory-catalog`](nodes/capability.track-territory-catalog.json) | Track and Territory Catalog | `capability` | authority object | `reviewed-candidate` | `high` | `high` |
| [`body-war.business.entity.activity-evidence-candidate`](nodes/entity.activity-evidence-candidate.json) | ActivityEvidenceCandidate | `entity` | evidence object | `reviewed-candidate` | `high` | `high` |
| [`body-war.business.entity.challenge`](nodes/entity.challenge.json) | Challenge | `entity` | authority object | `reviewed-candidate` | `high` | `high` |
| [`body-war.business.entity.clan`](nodes/entity.clan.json) | Clan | `entity` | authority object | `reviewed-candidate` | `high` | `high` |
| [`body-war.business.entity.evidence-submission`](nodes/entity.evidence-submission.json) | EvidenceSubmission | `entity` | evidence object | `reviewed-candidate` | `high` | `high` |
| [`body-war.business.entity.geometry-candidate`](nodes/entity.geometry-candidate.json) | GeometryCandidate | `entity` | evidence object | `blocked` | `medium` | `low` |
| [`body-war.business.entity.invasion`](nodes/entity.invasion.json) | Invasion | `entity` | workflow object | `reviewed-candidate` | `high` | `high` |
| [`body-war.business.entity.notification`](nodes/entity.notification.json) | Notification | `entity` | projection object | `reviewed-candidate` | `high` | `high` |
| [`body-war.business.entity.ownership-record`](nodes/entity.ownership-record.json) | Ownership Record | `entity` | evidence object | `reviewed-candidate` | `high` | `high` |
| [`body-war.business.entity.provider-account`](nodes/entity.provider-account.json) | ProviderAccount | `entity` | authority object | `reviewed-candidate` | `high` | `high` |
| [`body-war.business.entity.ranking-snapshot`](nodes/entity.ranking-snapshot.json) | Ranking Snapshot | `entity` | evidence object | `reviewed-candidate` | `high` | `high` |
| [`body-war.business.entity.run-activity`](nodes/entity.run-activity.json) | RunActivity | `entity` | evidence object | `reviewed-candidate` | `high` | `high` |
| [`body-war.business.entity.runner-confirmation`](nodes/entity.runner-confirmation.json) | RunnerConfirmation | `entity` | evidence object | `candidate` | `medium` | `medium` |
| [`body-war.business.entity.season`](nodes/entity.season.json) | Season | `entity` | authority object | `reviewed-candidate` | `high` | `high` |
| [`body-war.business.entity.sponsored-zone`](nodes/entity.sponsored-zone.json) | Sponsored Zone | `entity` | authority object | `deferred` | `high` | `low` |
| [`body-war.business.entity.suggested-track`](nodes/entity.suggested-track.json) | SuggestedTrack | `entity` | authority object | `reviewed-candidate` | `high` | `high` |
| [`body-war.business.entity.territory-unit`](nodes/entity.territory-unit.json) | TerritoryUnit | `entity` | authority object | `reviewed-candidate` | `high` | `high` |
| [`body-war.business.event.activities-imported`](nodes/event.activities-imported.json) | ActivitiesImported | `event` | evidence object | `reviewed-candidate` | `high` | `high` |
| [`body-war.business.event.challenge-completed`](nodes/event.challenge-completed.json) | ChallengeCompleted | `event` | evidence object | `reviewed-candidate` | `high` | `high` |
| [`body-war.business.event.controller-updated`](nodes/event.controller-updated.json) | ControllerUpdated | `event` | evidence object | `reviewed-candidate` | `high` | `high` |
| [`body-war.business.event.defense-succeeded`](nodes/event.defense-succeeded.json) | DefenseSucceeded | `event` | evidence object | `reviewed-candidate` | `high` | `high` |
| [`body-war.business.event.evidence-preview-accepted`](nodes/event.evidence-preview-accepted.json) | EvidencePreviewAccepted | `event` | evidence object | `reviewed-candidate` | `high` | `high` |
| [`body-war.business.event.evidence-rejected`](nodes/event.evidence-rejected.json) | EvidenceRejected | `event` | evidence object | `reviewed-candidate` | `high` | `high` |
| [`body-war.business.event.evidence-submitted`](nodes/event.evidence-submitted.json) | EvidenceSubmitted | `event` | evidence object | `reviewed-candidate` | `high` | `high` |
| [`body-war.business.event.evidence-verified`](nodes/event.evidence-verified.json) | EvidenceVerified | `event` | evidence object | `reviewed-candidate` | `high` | `high` |
| [`body-war.business.event.geometry-derived`](nodes/event.geometry-derived.json) | Geometry Derived | `event` | evidence object | `blocked` | `medium` | `low` |
| [`body-war.business.event.invasion-opened`](nodes/event.invasion-opened.json) | InvasionOpened | `event` | evidence object | `reviewed-candidate` | `high` | `high` |
| [`body-war.business.event.provider-access-revoked`](nodes/event.provider-access-revoked.json) | ProviderAccessRevoked | `event` | evidence object | `reviewed-candidate` | `high` | `high` |
| [`body-war.business.event.provider-connected`](nodes/event.provider-connected.json) | ProviderConnected | `event` | evidence object | `reviewed-candidate` | `high` | `high` |
| [`body-war.business.event.runner-confirmed-track-activity`](nodes/event.runner-confirmed-track-activity.json) | Runner Confirmed Track Activity | `event` | evidence object | `candidate` | `medium` | `medium` |
| [`body-war.business.event.score-input-snapshotted`](nodes/event.score-input-snapshotted.json) | Score Input Snapshotted | `event` | evidence object | `blocked` | `medium` | `low` |
| [`body-war.business.event.score-preview-calculated`](nodes/event.score-preview-calculated.json) | Score Preview Calculated | `event` | evidence object | `blocked` | `medium` | `low` |
| [`body-war.business.event.season-snapshot-closed`](nodes/event.season-snapshot-closed.json) | SeasonSnapshotClosed | `event` | evidence object | `reviewed-candidate` | `high` | `high` |
| [`body-war.business.event.territory-published`](nodes/event.territory-published.json) | TerritoryPublished | `event` | evidence object | `reviewed-candidate` | `high` | `high` |
| [`body-war.business.event.xp-awarded`](nodes/event.xp-awarded.json) | XPAwarded | `event` | evidence object | `reviewed-candidate` | `high` | `high` |
| [`body-war.business.external.strava`](nodes/external.strava.json) | Strava | `external_system` | evidence object | `reviewed-candidate` | `high` | `high` |
| [`body-war.business.interface.http-api`](nodes/interface.http-api.json) | Body War HTTP API | `interface` | workflow object | `reviewed-candidate` | `high` | `high` |
| [`body-war.business.interface.score-preview-journey-api`](nodes/interface.score-preview-journey-api.json) | Score Preview Journey API | `interface` | workflow object | `blocked` | `medium` | `low` |
| [`body-war.business.interface.strava-provider-boundary`](nodes/interface.strava-provider-boundary.json) | Strava Provider Boundary | `interface` | workflow object | `reviewed-candidate` | `high` | `high` |
| [`body-war.business.interface.suggested-track-api`](nodes/interface.suggested-track-api.json) | SuggestedTrack API | `interface` | workflow object | `reviewed-candidate` | `high` | `high` |
| [`body-war.business.ledger.xp-ledger`](nodes/ledger.xp-ledger.json) | XP Ledger | `ledger` | evidence object | `reviewed-candidate` | `high` | `high` |
| [`body-war.business.state.activity.empty`](nodes/state.activity.empty.json) | Activities Empty | `lifecycle_state` | authority object | `reviewed-candidate` | `high` | `high` |
| [`body-war.business.state.activity.loading`](nodes/state.activity.loading.json) | Activities Loading | `lifecycle_state` | authority object | `reviewed-candidate` | `high` | `high` |
| [`body-war.business.state.activity.not-loaded`](nodes/state.activity.not-loaded.json) | Activities Not Loaded | `lifecycle_state` | authority object | `reviewed-candidate` | `high` | `high` |
| [`body-war.business.state.activity.provider-error`](nodes/state.activity.provider-error.json) | Activity Provider Error | `lifecycle_state` | authority object | `reviewed-candidate` | `high` | `high` |
| [`body-war.business.state.activity.ready`](nodes/state.activity.ready.json) | Activities Ready | `lifecycle_state` | authority object | `reviewed-candidate` | `high` | `high` |
| [`body-war.business.state.auth.anonymous`](nodes/state.auth.anonymous.json) | Auth Anonymous | `lifecycle_state` | authority object | `reviewed-candidate` | `high` | `high` |
| [`body-war.business.state.auth.connected`](nodes/state.auth.connected.json) | Auth Connected | `lifecycle_state` | authority object | `reviewed-candidate` | `high` | `high` |
| [`body-war.business.state.auth.error`](nodes/state.auth.error.json) | Auth Error | `lifecycle_state` | authority object | `reviewed-candidate` | `high` | `high` |
| [`body-war.business.state.auth.revoked`](nodes/state.auth.revoked.json) | Auth Revoked | `lifecycle_state` | authority object | `reviewed-candidate` | `high` | `high` |
| [`body-war.business.state.auth.unconfigured`](nodes/state.auth.unconfigured.json) | Auth Unconfigured | `lifecycle_state` | authority object | `reviewed-candidate` | `high` | `high` |
| [`body-war.business.state.challenge.active`](nodes/state.challenge.active.json) | Challenge Active | `lifecycle_state` | authority object | `reviewed-candidate` | `high` | `high` |
| [`body-war.business.state.challenge.available`](nodes/state.challenge.available.json) | Challenge Available | `lifecycle_state` | authority object | `reviewed-candidate` | `high` | `high` |
| [`body-war.business.state.challenge.complete`](nodes/state.challenge.complete.json) | Challenge Complete | `lifecycle_state` | authority object | `reviewed-candidate` | `high` | `high` |
| [`body-war.business.state.challenge.expired`](nodes/state.challenge.expired.json) | Challenge Expired | `lifecycle_state` | authority object | `reviewed-candidate` | `high` | `high` |
| [`body-war.business.state.challenge.rewarded`](nodes/state.challenge.rewarded.json) | Challenge Rewarded | `lifecycle_state` | authority object | `reviewed-candidate` | `high` | `high` |
| [`body-war.business.state.controller.contested`](nodes/state.controller.contested.json) | Controller Contested | `lifecycle_state` | authority object | `reviewed-candidate` | `high` | `high` |
| [`body-war.business.state.controller.expired`](nodes/state.controller.expired.json) | Controller Expired | `lifecycle_state` | authority object | `reviewed-candidate` | `high` | `high` |
| [`body-war.business.state.controller.neutral`](nodes/state.controller.neutral.json) | Controller Neutral | `lifecycle_state` | authority object | `reviewed-candidate` | `high` | `high` |
| [`body-war.business.state.controller.preview-controlled`](nodes/state.controller.preview-controlled.json) | Controller Preview-Controlled | `lifecycle_state` | authority object | `reviewed-candidate` | `high` | `high` |
| [`body-war.business.state.controller.verified-controlled`](nodes/state.controller.verified-controlled.json) | Controller Verified-Controlled | `lifecycle_state` | authority object | `reviewed-candidate` | `high` | `high` |
| [`body-war.business.state.evidence-candidate.accepted`](nodes/state.evidence-candidate.accepted.json) | Evidence Candidate Accepted | `lifecycle_state` | authority object | `reviewed-candidate` | `high` | `high` |
| [`body-war.business.state.evidence-candidate.operator-review`](nodes/state.evidence-candidate.operator-review.json) | Evidence Candidate Operator Review | `lifecycle_state` | authority object | `reviewed-candidate` | `high` | `high` |
| [`body-war.business.state.evidence-candidate.rejected`](nodes/state.evidence-candidate.rejected.json) | Evidence Candidate Rejected | `lifecycle_state` | authority object | `reviewed-candidate` | `high` | `high` |
| [`body-war.business.state.evidence-candidate.submitted`](nodes/state.evidence-candidate.submitted.json) | Evidence Candidate Submitted | `lifecycle_state` | authority object | `reviewed-candidate` | `high` | `high` |
| [`body-war.business.state.geometry-candidate.absent`](nodes/state.geometry-candidate.absent.json) | Geometry Candidate Absent | `lifecycle_state` | authority object | `candidate` | `medium` | `high` |
| [`body-war.business.state.geometry-candidate.derived-candidate`](nodes/state.geometry-candidate.derived-candidate.json) | Geometry Derived Candidate | `lifecycle_state` | authority object | `candidate` | `medium` | `high` |
| [`body-war.business.state.geometry-candidate.fetch-pending`](nodes/state.geometry-candidate.fetch-pending.json) | Geometry Fetch Pending | `lifecycle_state` | authority object | `candidate` | `medium` | `high` |
| [`body-war.business.state.geometry-candidate.rejected`](nodes/state.geometry-candidate.rejected.json) | Geometry Candidate Rejected | `lifecycle_state` | authority object | `candidate` | `medium` | `high` |
| [`body-war.business.state.geometry-candidate.superseded`](nodes/state.geometry-candidate.superseded.json) | Geometry Candidate Superseded | `lifecycle_state` | authority object | `candidate` | `medium` | `high` |
| [`body-war.business.state.geometry-candidate.unavailable`](nodes/state.geometry-candidate.unavailable.json) | Geometry Unavailable | `lifecycle_state` | authority object | `candidate` | `medium` | `high` |
| [`body-war.business.state.geometry.draft`](nodes/state.geometry.draft.json) | Geometry Draft | `lifecycle_state` | authority object | `reviewed-candidate` | `high` | `high` |
| [`body-war.business.state.geometry.missing`](nodes/state.geometry.missing.json) | Geometry Missing | `lifecycle_state` | authority object | `reviewed-candidate` | `high` | `high` |
| [`body-war.business.state.geometry.placeholder`](nodes/state.geometry.placeholder.json) | Geometry Placeholder | `lifecycle_state` | authority object | `reviewed-candidate` | `high` | `high` |
| [`body-war.business.state.geometry.source-backed`](nodes/state.geometry.source-backed.json) | Geometry Source-Backed | `lifecycle_state` | authority object | `reviewed-candidate` | `high` | `high` |
| [`body-war.business.state.geometry.validated`](nodes/state.geometry.validated.json) | Geometry Validated | `lifecycle_state` | authority object | `reviewed-candidate` | `high` | `high` |
| [`body-war.business.state.score-preview.available`](nodes/state.score-preview.available.json) | Score Preview Available | `lifecycle_state` | authority object | `candidate` | `medium` | `low` |
| [`body-war.business.state.score-preview.blocked-geometry`](nodes/state.score-preview.blocked-geometry.json) | Score Blocked By Geometry | `lifecycle_state` | authority object | `candidate` | `medium` | `low` |
| [`body-war.business.state.score-preview.blocked-policy`](nodes/state.score-preview.blocked-policy.json) | Score Blocked By Policy | `lifecycle_state` | authority object | `candidate` | `medium` | `low` |
| [`body-war.business.state.score-preview.calculation-pending`](nodes/state.score-preview.calculation-pending.json) | Score Calculation Pending | `lifecycle_state` | authority object | `candidate` | `medium` | `low` |
| [`body-war.business.state.score-preview.failed`](nodes/state.score-preview.failed.json) | Score Calculation Failed | `lifecycle_state` | authority object | `candidate` | `medium` | `low` |
| [`body-war.business.state.score-preview.incomplete-projection`](nodes/state.score-preview.incomplete-projection.json) | Score Incomplete Projection | `lifecycle_state` | authority object | `candidate` | `medium` | `low` |
| [`body-war.business.state.score-preview.snapshot-pending`](nodes/state.score-preview.snapshot-pending.json) | Score Snapshot Pending | `lifecycle_state` | authority object | `candidate` | `medium` | `low` |
| [`body-war.business.state.score-preview.superseded`](nodes/state.score-preview.superseded.json) | Score Preview Superseded | `lifecycle_state` | authority object | `candidate` | `medium` | `low` |
| [`body-war.business.state.score-preview.unavailable`](nodes/state.score-preview.unavailable.json) | Score Preview Unavailable | `lifecycle_state` | authority object | `candidate` | `medium` | `low` |
| [`body-war.business.state.season.active`](nodes/state.season.active.json) | Season Active | `lifecycle_state` | authority object | `reviewed-candidate` | `high` | `high` |
| [`body-war.business.state.season.closed`](nodes/state.season.closed.json) | Season Closed | `lifecycle_state` | authority object | `reviewed-candidate` | `high` | `high` |
| [`body-war.business.state.season.closing`](nodes/state.season.closing.json) | Season Closing | `lifecycle_state` | authority object | `reviewed-candidate` | `high` | `high` |
| [`body-war.business.state.season.preseason`](nodes/state.season.preseason.json) | Season Preseason | `lifecycle_state` | authority object | `reviewed-candidate` | `high` | `high` |
| [`body-war.business.state.submission.draft`](nodes/state.submission.draft.json) | Submission Draft | `lifecycle_state` | authority object | `reviewed-candidate` | `high` | `high` |
| [`body-war.business.state.submission.preview-accepted`](nodes/state.submission.preview-accepted.json) | Submission Preview-Accepted | `lifecycle_state` | authority object | `reviewed-candidate` | `high` | `high` |
| [`body-war.business.state.submission.rejected`](nodes/state.submission.rejected.json) | Submission Rejected | `lifecycle_state` | authority object | `reviewed-candidate` | `high` | `high` |
| [`body-war.business.state.submission.submitted`](nodes/state.submission.submitted.json) | Submission Submitted | `lifecycle_state` | authority object | `reviewed-candidate` | `high` | `high` |
| [`body-war.business.state.submission.verified`](nodes/state.submission.verified.json) | Submission Verified | `lifecycle_state` | authority object | `reviewed-candidate` | `high` | `high` |
| [`body-war.business.state.suggested-track.evidence-submitted`](nodes/state.suggested-track.evidence-submitted.json) | SuggestedTrack Evidence Submitted | `lifecycle_state` | authority object | `reviewed-candidate` | `high` | `high` |
| [`body-war.business.state.suggested-track.needs-evidence`](nodes/state.suggested-track.needs-evidence.json) | SuggestedTrack Needs Evidence | `lifecycle_state` | authority object | `reviewed-candidate` | `high` | `high` |
| [`body-war.business.state.suggested-track.operator-review`](nodes/state.suggested-track.operator-review.json) | SuggestedTrack Operator Review | `lifecycle_state` | authority object | `reviewed-candidate` | `high` | `high` |
| [`body-war.business.state.suggested-track.retired`](nodes/state.suggested-track.retired.json) | SuggestedTrack Retired | `lifecycle_state` | authority object | `reviewed-candidate` | `high` | `high` |
| [`body-war.business.state.suggested-track.source-backed`](nodes/state.suggested-track.source-backed.json) | SuggestedTrack Source-Backed | `lifecycle_state` | authority object | `reviewed-candidate` | `high` | `high` |
| [`body-war.business.metric.profile-xp`](nodes/metric.profile-xp.json) | Profile XP | `metric` | projection object | `reviewed-candidate` | `high` | `high` |
| [`body-war.business.metric.seasonal-ranking`](nodes/metric.seasonal-ranking.json) | Seasonal Ranking | `metric` | projection object | `reviewed-candidate` | `high` | `high` |
| [`body-war.business.metric.zone-score`](nodes/metric.zone-score.json) | Zone Score | `metric` | authority object | `blocked` | `high` | `low` |
| [`body-war.business.operation.activate-sponsored-zone`](nodes/operation.activate-sponsored-zone.json) | Activate Sponsored Zone | `operation` | workflow object | `deferred` | `high` | `low` |
| [`body-war.business.operation.attach-activity-evidence-candidate`](nodes/operation.attach-activity-evidence-candidate.json) | Attach ActivityEvidenceCandidate | `operation` | workflow object | `reviewed-candidate` | `high` | `high` |
| [`body-war.business.operation.authenticate-via-strava`](nodes/operation.authenticate-via-strava.json) | Authenticate Via Strava | `operation` | workflow object | `reviewed-candidate` | `high` | `high` |
| [`body-war.business.operation.auto-accept-preview-evidence`](nodes/operation.auto-accept-preview-evidence.json) | Auto-Accept Preview Evidence | `operation` | workflow object | `reviewed-candidate` | `high` | `high` |
| [`body-war.business.operation.award-xp`](nodes/operation.award-xp.json) | Award XP | `operation` | workflow object | `reviewed-candidate` | `high` | `high` |
| [`body-war.business.operation.build-score-input-snapshot`](nodes/operation.build-score-input-snapshot.json) | Build ScoreInputSnapshot | `operation` | workflow object | `blocked` | `medium` | `low` |
| [`body-war.business.operation.calculate-score-preview`](nodes/operation.calculate-score-preview.json) | Calculate ScorePreview | `operation` | workflow object | `blocked` | `medium` | `low` |
| [`body-war.business.operation.calculate-zone-score`](nodes/operation.calculate-zone-score.json) | Calculate Zone Score | `operation` | workflow object | `blocked` | `high` | `low` |
| [`body-war.business.operation.complete-challenge`](nodes/operation.complete-challenge.json) | Complete Challenge | `operation` | workflow object | `reviewed-candidate` | `high` | `high` |
| [`body-war.business.operation.complete-strava-oauth`](nodes/operation.complete-strava-oauth.json) | Complete Strava OAuth | `operation` | workflow object | `reviewed-candidate` | `high` | `high` |
| [`body-war.business.operation.compute-controller`](nodes/operation.compute-controller.json) | Compute Controller | `operation` | workflow object | `reviewed-candidate` | `high` | `high` |
| [`body-war.business.operation.confirm-track-with-activity`](nodes/operation.confirm-track-with-activity.json) | Confirm Track With Activity | `operation` | workflow object | `candidate` | `medium` | `medium` |
| [`body-war.business.operation.create-clan`](nodes/operation.create-clan.json) | Create Clan | `operation` | workflow object | `reviewed-candidate` | `high` | `high` |
| [`body-war.business.operation.create-suggested-track`](nodes/operation.create-suggested-track.json) | Create SuggestedTrack | `operation` | workflow object | `reviewed-candidate` | `high` | `high` |
| [`body-war.business.operation.defend-territory`](nodes/operation.defend-territory.json) | Defend Territory | `operation` | workflow object | `reviewed-candidate` | `high` | `high` |
| [`body-war.business.operation.derive-geometry-candidate`](nodes/operation.derive-geometry-candidate.json) | Derive GeometryCandidate | `operation` | workflow object | `blocked` | `medium` | `low` |
| [`body-war.business.operation.dispatch-notification`](nodes/operation.dispatch-notification.json) | Dispatch Notification | `operation` | workflow object | `reviewed-candidate` | `high` | `high` |
| [`body-war.business.operation.ensure-default-suggested-tracks`](nodes/operation.ensure-default-suggested-tracks.json) | Ensure Default SuggestedTracks | `operation` | workflow object | `reviewed-candidate` | `high` | `high` |
| [`body-war.business.operation.fetch-selected-activity-geometry`](nodes/operation.fetch-selected-activity-geometry.json) | Fetch Selected Activity Geometry | `operation` | workflow object | `blocked` | `medium` | `low` |
| [`body-war.business.operation.import-activities`](nodes/operation.import-activities.json) | Import Activities | `operation` | workflow object | `reviewed-candidate` | `high` | `high` |
| [`body-war.business.operation.join-challenge`](nodes/operation.join-challenge.json) | Join Challenge | `operation` | workflow object | `reviewed-candidate` | `high` | `high` |
| [`body-war.business.operation.join-clan`](nodes/operation.join-clan.json) | Join Clan | `operation` | workflow object | `reviewed-candidate` | `high` | `high` |
| [`body-war.business.operation.logout`](nodes/operation.logout.json) | Logout | `operation` | workflow object | `reviewed-candidate` | `high` | `high` |
| [`body-war.business.operation.open-invasion`](nodes/operation.open-invasion.json) | Open Invasion | `operation` | workflow object | `reviewed-candidate` | `high` | `high` |
| [`body-war.business.operation.project-score-preview`](nodes/operation.project-score-preview.json) | Project ScorePreview | `operation` | projection object | `blocked` | `medium` | `low` |
| [`body-war.business.operation.purchase-economy-item`](nodes/operation.purchase-economy-item.json) | Purchase Economy Item | `operation` | workflow object | `deferred` | `high` | `low` |
| [`body-war.business.operation.review-evidence`](nodes/operation.review-evidence.json) | Review Evidence | `operation` | workflow object | `reviewed-candidate` | `high` | `high` |
| [`body-war.business.operation.select-suggested-track`](nodes/operation.select-suggested-track.json) | Select SuggestedTrack | `operation` | workflow object | `candidate` | `medium` | `medium` |
| [`body-war.business.operation.snapshot-season`](nodes/operation.snapshot-season.json) | Snapshot Season | `operation` | workflow object | `reviewed-candidate` | `high` | `high` |
| [`body-war.business.operation.start-strava-oauth`](nodes/operation.start-strava-oauth.json) | Start Strava OAuth | `operation` | workflow object | `reviewed-candidate` | `high` | `high` |
| [`body-war.business.operation.submit-evidence`](nodes/operation.submit-evidence.json) | Submit Evidence | `operation` | workflow object | `reviewed-candidate` | `high` | `high` |
| [`body-war.business.operation.upsert-territory`](nodes/operation.upsert-territory.json) | Upsert Territory | `operation` | workflow object | `reviewed-candidate` | `high` | `high` |
| [`body-war.business.outcome.score-preview`](nodes/outcome.score-preview.json) | ScorePreview | `outcome` | projection object | `blocked` | `medium` | `low` |
| [`body-war.business.outcome.source-backed-track`](nodes/outcome.source-backed-track.json) | Source-Backed Track | `outcome` | authority object | `deferred` | `high` | `low` |
| [`body-war.business.policy.activity-eligibility`](nodes/policy.activity-eligibility.json) | Activity Eligibility Policy | `policy` | authority object | `blocked` | `high` | `low` |
| [`body-war.business.policy.anti-cheat`](nodes/policy.anti-cheat.json) | Anti-Cheat Policy | `policy` | authority object | `deferred` | `high` | `low` |
| [`body-war.business.policy.caducity`](nodes/policy.caducity.json) | Ownership Caducity Policy | `policy` | authority object | `blocked` | `high` | `low` |
| [`body-war.business.policy.consent-contract`](nodes/policy.consent-contract.json) | Consent Contract | `policy` | authority object | `candidate` | `medium` | `medium` |
| [`body-war.business.policy.controller-selection`](nodes/policy.controller-selection.json) | Controller Selection Policy | `policy` | authority object | `blocked` | `high` | `low` |
| [`body-war.business.policy.geometry-privacy`](nodes/policy.geometry-privacy.json) | Geometry Privacy Policy | `policy` | authority object | `blocked` | `medium` | `low` |
| [`body-war.business.policy.notification-privacy`](nodes/policy.notification-privacy.json) | Notification Privacy Policy | `policy` | authority object | `reviewed-candidate` | `high` | `high` |
| [`body-war.business.policy.ownership-eligibility`](nodes/policy.ownership-eligibility.json) | Ownership Eligibility Policy | `policy` | authority object | `blocked` | `high` | `low` |
| [`body-war.business.policy.preview-evidence`](nodes/policy.preview-evidence.json) | Preview Evidence Policy | `policy` | authority object | `reviewed-candidate` | `high` | `high` |
| [`body-war.business.policy.score-history`](nodes/policy.score-history.json) | Score History Policy | `policy` | authority object | `blocked` | `high` | `low` |
| [`body-war.business.policy.score-policy`](nodes/policy.score-policy.json) | ScorePolicy | `policy` | authority object | `blocked` | `medium` | `low` |
| [`body-war.business.premise.h-001`](nodes/premise.h-001.json) | H-001 Physical Activity Motivation | `premise` | authority object | `candidate` | `low` | `low` |
| [`body-war.business.premise.h-002`](nodes/premise.h-002.json) | H-002 Territory Competition | `premise` | authority object | `candidate` | `low` | `low` |
| [`body-war.business.premise.h-003`](nodes/premise.h-003.json) | H-003 Strava Trust | `premise` | authority object | `candidate` | `low` | `low` |
| [`body-war.business.premise.h-004`](nodes/premise.h-004.json) | H-004 Park Pilot | `premise` | authority object | `candidate` | `low` | `low` |
| [`body-war.business.premise.h-005`](nodes/premise.h-005.json) | H-005 Composite Score | `premise` | authority object | `candidate` | `low` | `low` |
| [`body-war.business.premise.h-006`](nodes/premise.h-006.json) | H-006 Defense Window | `premise` | authority object | `candidate` | `low` | `low` |
| [`body-war.business.premise.h-007`](nodes/premise.h-007.json) | H-007 Progression | `premise` | authority object | `candidate` | `low` | `low` |
| [`body-war.business.premise.h-008`](nodes/premise.h-008.json) | H-008 Clan Sociality | `premise` | authority object | `candidate` | `low` | `low` |
| [`body-war.business.premise.h-009`](nodes/premise.h-009.json) | H-009 Sponsor Value | `premise` | authority object | `deferred` | `low` | `low` |
| [`body-war.business.premise.h-010`](nodes/premise.h-010.json) | H-010 Local Operator | `premise` | authority object | `candidate` | `low` | `low` |
| [`body-war.business.query.active-challenges`](nodes/query.active-challenges.json) | Active Challenges Query | `query` | projection object | `reviewed-candidate` | `high` | `high` |
| [`body-war.business.query.activity-list`](nodes/query.activity-list.json) | Activity List Query | `query` | projection object | `reviewed-candidate` | `high` | `high` |
| [`body-war.business.query.auth-status`](nodes/query.auth-status.json) | Auth Status Query | `query` | projection object | `reviewed-candidate` | `high` | `high` |
| [`body-war.business.query.clan-summary`](nodes/query.clan-summary.json) | Clan Summary Query | `query` | projection object | `reviewed-candidate` | `high` | `high` |
| [`body-war.business.query.current-controller`](nodes/query.current-controller.json) | Current Controller Query | `query` | projection object | `reviewed-candidate` | `high` | `high` |
| [`body-war.business.query.evidence-list`](nodes/query.evidence-list.json) | Evidence List Query | `query` | projection object | `reviewed-candidate` | `high` | `high` |
| [`body-war.business.query.get-suggested-track-detail`](nodes/query.get-suggested-track-detail.json) | Get SuggestedTrack Detail | `query` | projection object | `reviewed-candidate` | `high` | `high` |
| [`body-war.business.query.home-summary`](nodes/query.home-summary.json) | Home Summary Query | `query` | projection object | `reviewed-candidate` | `high` | `high` |
| [`body-war.business.query.latest-score-preview`](nodes/query.latest-score-preview.json) | Latest ScorePreview Query | `query` | projection object | `blocked` | `medium` | `low` |
| [`body-war.business.query.list-suggested-tracks`](nodes/query.list-suggested-tracks.json) | List SuggestedTracks | `query` | projection object | `reviewed-candidate` | `high` | `high` |
| [`body-war.business.query.notifications`](nodes/query.notifications.json) | Notifications Query | `query` | projection object | `reviewed-candidate` | `high` | `high` |
| [`body-war.business.query.operator-queue`](nodes/query.operator-queue.json) | Operator Queue Query | `query` | projection object | `reviewed-candidate` | `high` | `high` |
| [`body-war.business.query.profile-summary`](nodes/query.profile-summary.json) | Profile Summary Query | `query` | projection object | `reviewed-candidate` | `high` | `high` |
| [`body-war.business.query.rankings`](nodes/query.rankings.json) | Rankings Query | `query` | projection object | `reviewed-candidate` | `high` | `high` |
| [`body-war.business.query.score-preview-journey`](nodes/query.score-preview-journey.json) | Score Preview Journey Query | `query` | projection object | `blocked` | `medium` | `low` |
| [`body-war.business.query.track-detail`](nodes/query.track-detail.json) | Track Detail Query | `query` | projection object | `reviewed-candidate` | `high` | `high` |
| [`body-war.business.query.track-list`](nodes/query.track-list.json) | Track List Query | `query` | projection object | `reviewed-candidate` | `high` | `high` |
| [`body-war.business.value.activity-geometry-sample`](nodes/value.activity-geometry-sample.json) | ActivityGeometrySample | `value_object` | evidence object | `blocked` | `medium` | `low` |
| [`body-war.business.value.activity-sport-type`](nodes/value.activity-sport-type.json) | Activity Sport Type | `value_object` | authority object | `reviewed-candidate` | `high` | `high` |
| [`body-war.business.value.badge`](nodes/value.badge.json) | Badge | `value_object` | projection object | `reviewed-candidate` | `high` | `high` |
| [`body-war.business.value.control-basis`](nodes/value.control-basis.json) | Control Basis | `value_object` | evidence object | `reviewed-candidate` | `high` | `high` |
| [`body-war.business.value.controller-metric`](nodes/value.controller-metric.json) | Controller Metric | `value_object` | authority object | `blocked` | `high` | `low` |
| [`body-war.business.value.controller-state`](nodes/value.controller-state.json) | ControllerState | `value_object` | projection object | `reviewed-candidate` | `high` | `high` |
| [`body-war.business.value.defense-window`](nodes/value.defense-window.json) | Defense Window | `value_object` | authority object | `reviewed-candidate` | `high` | `high` |
| [`body-war.business.value.geometry-status`](nodes/value.geometry-status.json) | Geometry Status | `value_object` | authority object | `reviewed-candidate` | `high` | `high` |
| [`body-war.business.value.league`](nodes/value.league.json) | League | `value_object` | projection object | `reviewed-candidate` | `high` | `high` |
| [`body-war.business.value.privacy-consent`](nodes/value.privacy-consent.json) | Privacy Consent | `value_object` | authority object | `candidate` | `medium` | `medium` |
| [`body-war.business.value.redacted-activity-summary`](nodes/value.redacted-activity-summary.json) | Redacted Activity Summary | `value_object` | evidence object | `reviewed-candidate` | `high` | `high` |
| [`body-war.business.value.reference-time`](nodes/value.reference-time.json) | Reference Time | `value_object` | authority object | `reviewed-candidate` | `high` | `high` |
| [`body-war.business.value.runcoin`](nodes/value.runcoin.json) | RunCoin | `value_object` | authority object | `deferred` | `high` | `low` |
| [`body-war.business.value.score-input-snapshot`](nodes/value.score-input-snapshot.json) | ScoreInputSnapshot | `value_object` | evidence object | `blocked` | `medium` | `low` |
| [`body-war.business.value.submission-status`](nodes/value.submission-status.json) | Submission Status | `value_object` | authority object | `reviewed-candidate` | `high` | `high` |
| [`body-war.business.value.track-geometry`](nodes/value.track-geometry.json) | TrackGeometry | `value_object` | evidence object | `reviewed-candidate` | `high` | `high` |
| [`body-war.business.value.zone-type`](nodes/value.zone-type.json) | Zone Type | `value_object` | authority object | `reviewed-candidate` | `high` | `high` |
| [`body-war.business.workflow.invasion-defense`](nodes/workflow.invasion-defense.json) | Invasion and Defense Workflow | `workflow` | workflow object | `reviewed-candidate` | `high` | `high` |
| [`body-war.business.workflow.login-to-score-preview`](nodes/workflow.login-to-score-preview.json) | Login To ScorePreview Workflow | `workflow` | workflow object | `blocked` | `medium` | `low` |
| [`body-war.business.workflow.run-to-control`](nodes/workflow.run-to-control.json) | Run To Control Workflow | `workflow` | workflow object | `reviewed-candidate` | `high` | `high` |
| [`body-war.business.workflow.seasonal-progression`](nodes/workflow.seasonal-progression.json) | Seasonal Progression Workflow | `workflow` | workflow object | `reviewed-candidate` | `high` | `high` |
| [`body-war.business.workflow.suggested-track-expansion`](nodes/workflow.suggested-track-expansion.json) | SuggestedTrack Expansion Workflow | `workflow` | workflow object | `reviewed-candidate` | `high` | `high` |
