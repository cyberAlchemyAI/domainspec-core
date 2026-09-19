# Interfaces: SuggestedTrack Route Expansion

## External: SuggestedTrack API (HTTP)

All routes require an authenticated connected runner session in L0.

### GET /api/suggested-tracks

**Exposes:** [ListSuggestedTracks](queries.md#listsuggestedtracks)
**Auth:** `body-war.suggested-track.read`

**Responses:**

| Status | Condition | Body |
| --- | --- | --- |
| 200 | Success | `{ suggested_tracks: SuggestedTrack[] }` |
| 401/403 | Missing session or permission | Standard error payload |

### POST /api/suggested-tracks

**Exposes:** [CreateSuggestedTrack](operations.md#createsuggestedtrack)
**Auth:** `body-war.suggested-track.create` plus CSRF/origin protection

**Request:**

| Field | Type | Maps To |
| --- | --- | --- |
| name | string | `CreateSuggestedTrack.name` |
| place_label | string | `CreateSuggestedTrack.placeLabel` |
| city | string | `CreateSuggestedTrack.city` |
| distance_hint_meters | integer | `CreateSuggestedTrack.distanceHintMeters` |
| public_note | string | `CreateSuggestedTrack.publicNote` |

**Responses:**

| Status | Condition | Body |
| --- | --- | --- |
| 201 | Created | `{ suggested_track }` |
| 400 | Invalid input | Standard error payload |

### GET /api/suggested-tracks/{idOrSlug}

**Exposes:** [GetSuggestedTrackDetail](queries.md#getsuggestedtrackdetail)
**Auth:** `body-war.suggested-track.read`

**Responses:**

| Status | Condition | Body |
| --- | --- | --- |
| 200 | Success | `{ suggested_track, my_evidence_candidates, evidence_summary }` |
| 404 | Unknown suggestion | Standard error payload |

### POST /api/suggested-tracks/{idOrSlug}/evidence-candidates

**Exposes:** [AttachActivityEvidenceCandidate](operations.md#attachactivityevidencecandidate)
**Auth:** `body-war.suggested-track-evidence.create` plus CSRF/origin protection

**Request:**

| Field | Type | Maps To |
| --- | --- | --- |
| activity_id | string | `AttachActivityEvidenceCandidate.providerActivityId` |
| consent_acknowledged | boolean | `AttachActivityEvidenceCandidate.consentAcknowledged` |
| consent_text | string | `AttachActivityEvidenceCandidate.consentText` |

**Responses:**

| Status | Condition | Body |
| --- | --- | --- |
| 201 | Candidate attached | `{ evidence_candidate, suggested_track }` |
| 400 | Missing consent or invalid activity | Standard error payload |
| 404 | Unknown suggestion | Standard error payload |

## Internal: Body War Repository Interface

| Method | Maps To | Description |
| --- | --- | --- |
| `ensureDefaultSuggestedTracks` | Seed operation | Creates or updates `volta-do-taquaral` as `needs_evidence`. |
| `listSuggestedTracks` | `ListSuggestedTracks` query | Reads connected-runner suggestions. |
| `createSuggestedTrack` | `CreateSuggestedTrack` operation | Persists runner-created suggestion. |
| `addActivityEvidenceCandidate` | `AttachActivityEvidenceCandidate` operation | Persists redacted summary and consent. |
