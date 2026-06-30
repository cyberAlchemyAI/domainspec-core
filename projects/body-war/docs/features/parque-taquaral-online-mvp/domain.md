# Domain: SuggestedTrack Route Expansion

## Entities

### SuggestedTrack

A route suggestion visible to connected runners in L0.

| Field | Type | Required | Description |
| --- | --- | --- | --- |
| id | uuid | yes | Stable database identifier. |
| slug | string | yes | Human-readable unique key. |
| name | string | yes | Runner-facing route name. |
| placeLabel | string | yes | Place cue such as park or neighborhood. |
| city | string | yes | City label. |
| country | string | yes | ISO-like country label, default `BR`. |
| distanceHintMeters | integer | no | Optional runner-supplied distance hint. |
| status | [SuggestedTrackStatus](#suggestedtrackstatus) | yes | Current evidence/promotion state. |
| geometryAuthority | string | yes | `needs_evidence` until source-backed evidence exists. |
| suggestedByPrincipalId | uuid | no | Connected runner who proposed the route. |
| publicNote | string | no | Short runner-facing note. |
| createdAt | timestamp | yes | Creation time. |
| updatedAt | timestamp | yes | Last mutation time. |

**Lifecycle:** See [SuggestedTrackLifecycle](states.md#suggestedtracklifecycle)
**Operations:** [CreateSuggestedTrack](operations.md#createsuggestedtrack), [AttachActivityEvidenceCandidate](operations.md#attachactivityevidencecandidate)

### ActivityEvidenceCandidate

A consenting runner's redacted Strava activity summary attached to a suggestion
for later operator review.

| Field | Type | Required | Description |
| --- | --- | --- | --- |
| id | uuid | yes | Stable database identifier. |
| suggestedTrackId | uuid | yes | Suggested track being helped. |
| principalId | uuid | yes | Connected runner who consented. |
| provider | string | yes | `strava` for this build. |
| providerActivityId | string | yes | Provider activity identifier. |
| redactedSummary | object | yes | Name, sport type, distance, moving time, speed, and start date only. |
| consentText | string | yes | Consent phrase shown at submit time. |
| consentedAt | timestamp | yes | Consent capture time. |
| status | [ActivityEvidenceCandidateStatus](#activityevidencecandidatestatus) | yes | Candidate review state. |
| createdAt | timestamp | yes | Creation time. |
| updatedAt | timestamp | yes | Last mutation time. |

**Lifecycle:** See [EvidenceCandidateLifecycle](states.md#evidencecandidatelifecycle)

## Enums

### SuggestedTrackStatus

| Value | Description |
| --- | --- |
| needs_evidence | Default state; route is only a suggestion. |
| evidence_submitted | At least one redacted candidate has been attached. |
| operator_review | Operator is reviewing candidate evidence. |
| source_backed | Operator promoted after source/geometry evidence; out of this build. |
| retired | Hidden from active expansion. |

### ActivityEvidenceCandidateStatus

| Value | Description |
| --- | --- |
| submitted | Runner submitted a consented redacted summary. |
| operator_review | Operator is reviewing the candidate. |
| accepted | Operator accepted the candidate as useful evidence. |
| rejected | Operator rejected the candidate. |
