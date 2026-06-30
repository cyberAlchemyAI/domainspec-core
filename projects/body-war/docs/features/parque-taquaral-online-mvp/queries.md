# Queries: SuggestedTrack Route Expansion

## ListSuggestedTracks

Return active suggestions visible to a connected runner.

| Output Field | Type | Description |
| --- | --- | --- |
| suggested_tracks | SuggestedTrack[] | Suggestions sorted by seed priority and creation time. |

### Rules

| Rule | Description |
| --- | --- |
| QT-1 | Query requires `body-war.suggested-track.read`. |
| QT-2 | Results must expose status and geometry authority honestly. |
| QT-3 | Results must not expose provider tokens or raw activity payloads. |

## GetSuggestedTrackDetail

Return one suggestion with the current runner's attached candidate list and a
redacted evidence count.

| Output Field | Type | Description |
| --- | --- | --- |
| suggested_track | SuggestedTrack | The selected route suggestion. |
| my_evidence_candidates | ActivityEvidenceCandidate[] | Candidates submitted by the current principal. |
| evidence_summary | object | Candidate count and authority labels. |

### Rules

| Rule | Description |
| --- | --- |
| QD-1 | Detail is connected-runner only in L0. |
| QD-2 | Candidate summaries remain redacted. |
| QD-3 | Authority labels stay `route_geometry: not_claimed` and `scoring: not_claimed`. |
