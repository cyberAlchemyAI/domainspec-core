# Application domain

## Entities

### EmptyRequest

| Field | Type | Constraint |
| --- | --- | --- |


### OpaqueResponse

| Field | Type | Constraint |
| --- | --- | --- |
| value | unknown? | optional |

### ProfileResponse

| Field | Type | Constraint |
| --- | --- | --- |
| profile | PublicRunnerProfile | required |

### StatusResponse

| Field | Type | Constraint |
| --- | --- | --- |
| configured | boolean | required |
| authenticated | boolean | required |
| connected | boolean | required |
| athlete | PublicAthlete / null | required |
| redirect_uri | string | required |
| scope | string | required |
| identity_mode | string? | optional |
| login_uri | string? | optional |
| session_state | string? | optional |
| security_available | boolean? | optional |

### RunnerProfile

| Field | Type | Constraint |
| --- | --- | --- |
| principalId | string | required |
| displayName | string | required |
| privacyStatus | string | required |
| createdAt | string | required |
| updatedAt | string | required |

### ProviderAccount

| Field | Type | Constraint |
| --- | --- | --- |
| id | string | required |
| provider | StravaProvider | required |
| principalId | string | required |
| providerUserId | string | required |
| displayName | string / null | required |
| scope | string[] | required |
| status | ProviderStatus | required |
| linkedAt | string | required |
| updatedAt | string | required |
| metadata | record | required |

### OAuthState

| Field | Type | Constraint |
| --- | --- | --- |
| state | string | required |
| nonce | string | required |
| redirectTarget | string | required |
| createdAt | string | required |
| expiresAt | string | required |
| consumedAt | string / null | required |

### ProviderTokenRecord

| Field | Type | Constraint |
| --- | --- | --- |
| id | string | required |
| accountId | string | required |
| accessTokenCiphertext | string | required |
| refreshTokenCiphertext | string | required |
| expiresAt | string | required |
| createdAt | string | required |
| updatedAt | string | required |

### OAuthCallbackRequest

| Field | Type | Constraint |
| --- | --- | --- |
| code | string? | optional |
| state | string? | optional |
| error | string? | optional |

### LogoutResponse

| Field | Type | Constraint |
| --- | --- | --- |
| ok | boolean | required |

### PublicAthlete

| Field | Type | Constraint |
| --- | --- | --- |
| id | string / number | required |
| firstname | string / null? | optional |
| lastname | string / null? | optional |
| profile | string / null? | optional |
| strava_profile_url | string / null | required |
| scope | string[] | required |
| provider | StravaProvider | required |
| status | ProviderStatus | required |

### PublicSession

| Field | Type | Constraint |
| --- | --- | --- |
| expires_at | string | required |

### PublicConnection

| Field | Type | Constraint |
| --- | --- | --- |
| connected | boolean | required |
| account | PublicAthlete / null | required |
| profile_url | string / null | required |

### ProfilePrivacy

| Field | Type | Constraint |
| --- | --- | --- |
| provider_tokens | string | required |
| activity_import | string | required |
| csrf | string | required |

### ProfileValidation

| Field | Type | Constraint |
| --- | --- | --- |
| taquaral_activity | string | required |
| route_geometry | string | required |
| scoring | string | required |

### PublicRunnerProfile

| Field | Type | Constraint |
| --- | --- | --- |
| principal_id | string | required |
| display_name | string | required |
| principal_status | string | required |
| session | PublicSession | required |
| strava | PublicConnection | required |
| privacy | ProfilePrivacy | required |
| validation | ProfileValidation | required |

### ProviderLinkResponse

| Field | Type | Constraint |
| --- | --- | --- |
| url | string | required |

### ActivitySummary

| Field | Type | Constraint |
| --- | --- | --- |
| id | string | required |
| name | string | required |
| sport_type | string? | optional |
| type | string? | optional |
| distance | number | required |
| moving_time | number | required |
| average_speed | number | required |
| start_date | string | required |

### ActivityPageRequest

| Field | Type | Constraint |
| --- | --- | --- |
| page | string? | optional |
| per_page | string? | optional |

### ActivitiesResponse

| Field | Type | Constraint |
| --- | --- | --- |
| activities | ActivitySummary[] | required |
| receipt | ActivityImportReceipt | required |

### RedactionReceipt

| Field | Type | Constraint |
| --- | --- | --- |
| provider_tokens | string | required |
| raw_private_payload | string | required |
| maps | string | required |
| notes | string | required |

### ImportConsentReceipt

| Field | Type | Constraint |
| --- | --- | --- |
| friend_fixture | string | required |

### ActivityImportReceipt

| Field | Type | Constraint |
| --- | --- | --- |
| source | StravaProvider | required |
| principal_id | string | required |
| imported_at | string | required |
| summary_count | number | required |
| redaction | RedactionReceipt | required |
| consent | ImportConsentReceipt | required |
| authority | EvidenceAuthority | required |

### SuggestedTrack

| Field | Type | Constraint |
| --- | --- | --- |
| id | string | required |
| slug | string | required |
| name | string | required |
| placeLabel | string | required |
| city | string | required |
| country | string | required |
| distanceHintMeters | number / null | required |
| status | SuggestedTrackStatus | required |
| geometryAuthority | string | required |
| suggestedByPrincipalId | string / null | required |
| publicNote | string | required |
| createdAt | string | required |
| updatedAt | string | required |

### CreateTrackRequest

| Field | Type | Constraint |
| --- | --- | --- |
| name | string | required |
| place_label | string | required |
| city | string | required |
| distance_hint_meters | number / null? | optional |
| public_note | string? | optional |

### TrackKeyRequest

| Field | Type | Constraint |
| --- | --- | --- |
| idOrSlug | string | required |

### TrackListResponse

| Field | Type | Constraint |
| --- | --- | --- |
| suggested_tracks | PublicTrack[] | required |

### TrackResponse

| Field | Type | Constraint |
| --- | --- | --- |
| suggested_track | PublicTrack | required |
| my_evidence_candidates | PublicEvidence[]? | optional |
| evidence_summary | EvidenceSummary? | optional |

### PublicTrackAuthority

| Field | Type | Constraint |
| --- | --- | --- |
| route_geometry | string | required |
| scoring | NoClaim | required |
| pilot_ready | NoClaim | required |

### PublicTrack

| Field | Type | Constraint |
| --- | --- | --- |
| id | string | required |
| slug | string | required |
| name | string | required |
| place_label | string | required |
| city | string | required |
| country | string | required |
| distance_hint_meters | number / null | required |
| status | SuggestedTrackStatus | required |
| geometry_authority | string | required |
| suggested_by | string | required |
| public_note | string | required |
| created_at | string | required |
| updated_at | string | required |
| authority | PublicTrackAuthority | required |

### ActivityEvidenceCandidate

| Field | Type | Constraint |
| --- | --- | --- |
| id | string | required |
| suggestedTrackId | string | required |
| principalId | string | required |
| provider | StravaProvider | required |
| providerActivityId | string | required |
| redactedSummary | record | required |
| consentText | string | required |
| consentedAt | string | required |
| status | ActivityEvidenceCandidateStatus | required |
| createdAt | string | required |
| updatedAt | string | required |

### AttachEvidenceRequest

| Field | Type | Constraint |
| --- | --- | --- |
| activity_id | string | required |
| consent_acknowledged | boolean? | optional |
| consent_text | string? | optional |

### EvidenceResponse

| Field | Type | Constraint |
| --- | --- | --- |
| evidence_candidate | PublicEvidence | required |
| suggested_track | PublicTrack? | optional |

### EvidenceAuthority

| Field | Type | Constraint |
| --- | --- | --- |
| activity_summary | string | required |
| route_geometry | NoClaim | required |
| scoring | NoClaim | required |

### PublicEvidence

| Field | Type | Constraint |
| --- | --- | --- |
| id | string | required |
| suggested_track_id | string | required |
| provider | StravaProvider | required |
| provider_activity_id | string | required |
| redacted_summary | ActivitySummary | required |
| consented_at | string | required |
| status | ActivityEvidenceCandidateStatus | required |
| created_at | string | required |
| updated_at | string | required |
| authority | EvidenceAuthority | required |

### EvidenceSummaryAuthority

| Field | Type | Constraint |
| --- | --- | --- |
| activity_summary | string | required |
| route_geometry | NoClaim | required |
| scoring | NoClaim | required |
| pilot_ready | NoClaim | required |

### EvidenceSummary

| Field | Type | Constraint |
| --- | --- | --- |
| candidate_count | number | required |
| redaction | RedactionReceipt | required |
| authority | EvidenceSummaryAuthority | required |

### WithdrawEvidenceResponse

| Field | Type | Constraint |
| --- | --- | --- |
| withdrawn | boolean | required |
## Open Questions

See ../../README.md#open-questions.
