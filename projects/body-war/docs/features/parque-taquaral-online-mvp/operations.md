# Operations: SuggestedTrack Route Expansion

## CreateSuggestedTrack

Create a connected-runner route suggestion.

| Input | Type | Rule |
| --- | --- | --- |
| principalId | uuid | Authenticated runner session. |
| name | string | Required, trimmed, max 255. |
| placeLabel | string | Required, trimmed, max 255. |
| city | string | Required, trimmed, max 120. |
| distanceHintMeters | integer | Optional positive value. |
| publicNote | string | Optional, trimmed. |

### Rules

| Rule | Description |
| --- | --- |
| CT-1 | Creation requires login and `body-war.suggested-track.create`. |
| CT-2 | New suggestions start as `needs_evidence`. |
| CT-3 | `geometryAuthority` remains `needs_evidence`. |
| CT-4 | Creation must not claim source-backed or pilot-ready status. |

## AttachActivityEvidenceCandidate

Attach one live Strava activity summary to a suggestion with explicit consent.

| Input | Type | Rule |
| --- | --- | --- |
| principalId | uuid | Authenticated runner session. |
| suggestedTrackId | uuid | Existing suggestion. |
| providerActivityId | string | Must match a live redacted activity summary visible to the runner. |
| consentAcknowledged | boolean | Must be true. |
| consentText | string | Stored with the candidate. |

### Rules

| Rule | Description |
| --- | --- |
| EC-1 | Activity browsing is live and ephemeral. |
| EC-2 | Persistence stores redacted summary fields only: id, name, sport type, distance, moving time, average speed, start date. |
| EC-3 | Raw provider payloads, maps, notes, tokens, and secrets are never stored in the candidate. |
| EC-4 | A `needs_evidence` suggestion may move to `evidence_submitted`. |
| EC-5 | `source_backed` and `pilot_ready` are not set by this operation. |

## EnsureDefaultSuggestedTracks

Create or refresh the `volta-do-taquaral` seed suggestion.

| Field | Value |
| --- | --- |
| slug | `volta-do-taquaral` |
| name | `Volta do Taquaral` |
| status | `needs_evidence` |
| geometryAuthority | `needs_evidence` |

### Rules

| Rule | Description |
| --- | --- |
| SD-1 | Seed is idempotent data, not a hardcoded UI branch. |
| SD-2 | Seed must be available in memory and Postgres-backed runs. |
