// Generated closed record validation for JSON success responses.
const records = {
    "EmptyRequest": {},
    "OpaqueResponse": {
        "value": "unknown?"
    },
    "ProfileResponse": {
        "profile": "PublicRunnerProfile"
    },
    "StatusResponse": {
        "configured": "boolean",
        "authenticated": "boolean",
        "connected": "boolean",
        "athlete": "PublicAthlete|null",
        "redirect_uri": "string",
        "scope": "string",
        "identity_mode": "string?",
        "login_uri": "string?",
        "session_state": "string?"
    },
    "RunnerProfile": {
        "principalId": "string",
        "displayName": "string",
        "privacyStatus": "string",
        "createdAt": "string",
        "updatedAt": "string"
    },
    "ProviderAccount": {
        "id": "string",
        "provider": "StravaProvider",
        "principalId": "string",
        "providerUserId": "string",
        "displayName": "string|null",
        "scope": "string[]",
        "status": "ProviderStatus",
        "linkedAt": "string",
        "updatedAt": "string",
        "metadata": "record"
    },
    "OAuthState": {
        "state": "string",
        "nonce": "string",
        "redirectTarget": "string",
        "createdAt": "string",
        "expiresAt": "string",
        "consumedAt": "string|null"
    },
    "ProviderTokenRecord": {
        "id": "string",
        "accountId": "string",
        "accessTokenCiphertext": "string",
        "refreshTokenCiphertext": "string",
        "expiresAt": "string",
        "createdAt": "string",
        "updatedAt": "string"
    },
    "OAuthCallbackRequest": {
        "code": "string?",
        "state": "string?",
        "error": "string?"
    },
    "LogoutResponse": {
        "ok": "boolean"
    },
    "PublicAthlete": {
        "id": "string|number",
        "firstname": "string|null?",
        "lastname": "string|null?",
        "profile": "string|null?",
        "strava_profile_url": "string|null",
        "scope": "string[]",
        "provider": "StravaProvider",
        "status": "ProviderStatus"
    },
    "PublicSession": {
        "expires_at": "string"
    },
    "PublicConnection": {
        "connected": "boolean",
        "account": "PublicAthlete|null",
        "profile_url": "string|null"
    },
    "ProfilePrivacy": {
        "provider_tokens": "string",
        "activity_import": "string",
        "csrf": "string"
    },
    "ProfileValidation": {
        "taquaral_activity": "string",
        "route_geometry": "string",
        "scoring": "string"
    },
    "PublicRunnerProfile": {
        "principal_id": "string",
        "display_name": "string",
        "principal_status": "string",
        "session": "PublicSession",
        "strava": "PublicConnection",
        "privacy": "ProfilePrivacy",
        "validation": "ProfileValidation"
    },
    "ProviderLinkResponse": {
        "url": "string"
    },
    "ActivitySummary": {
        "id": "string",
        "name": "string",
        "sport_type": "string?",
        "type": "string?",
        "distance": "number",
        "moving_time": "number",
        "average_speed": "number",
        "start_date": "string"
    },
    "ActivityPageRequest": {
        "page": "string?",
        "per_page": "string?"
    },
    "ActivitiesResponse": {
        "activities": "ActivitySummary[]",
        "receipt": "ActivityImportReceipt"
    },
    "RedactionReceipt": {
        "provider_tokens": "string",
        "raw_private_payload": "string",
        "maps": "string",
        "notes": "string"
    },
    "ImportConsentReceipt": {
        "friend_fixture": "string"
    },
    "ActivityImportReceipt": {
        "source": "StravaProvider",
        "principal_id": "string",
        "imported_at": "string",
        "summary_count": "number",
        "redaction": "RedactionReceipt",
        "consent": "ImportConsentReceipt",
        "authority": "EvidenceAuthority"
    },
    "SuggestedTrack": {
        "id": "string",
        "slug": "string",
        "name": "string",
        "placeLabel": "string",
        "city": "string",
        "country": "string",
        "distanceHintMeters": "number|null",
        "status": "SuggestedTrackStatus",
        "geometryAuthority": "string",
        "suggestedByPrincipalId": "string|null",
        "publicNote": "string",
        "createdAt": "string",
        "updatedAt": "string"
    },
    "CreateTrackRequest": {
        "name": "string",
        "place_label": "string",
        "city": "string",
        "distance_hint_meters": "number|null?",
        "public_note": "string?"
    },
    "TrackKeyRequest": {
        "idOrSlug": "string"
    },
    "TrackListResponse": {
        "suggested_tracks": "PublicTrack[]"
    },
    "TrackResponse": {
        "suggested_track": "PublicTrack",
        "my_evidence_candidates": "PublicEvidence[]?",
        "evidence_summary": "EvidenceSummary?"
    },
    "PublicTrackAuthority": {
        "route_geometry": "string",
        "scoring": "NoClaim",
        "pilot_ready": "NoClaim"
    },
    "PublicTrack": {
        "id": "string",
        "slug": "string",
        "name": "string",
        "place_label": "string",
        "city": "string",
        "country": "string",
        "distance_hint_meters": "number|null",
        "status": "SuggestedTrackStatus",
        "geometry_authority": "string",
        "suggested_by": "string",
        "public_note": "string",
        "created_at": "string",
        "updated_at": "string",
        "authority": "PublicTrackAuthority"
    },
    "ActivityEvidenceCandidate": {
        "id": "string",
        "suggestedTrackId": "string",
        "principalId": "string",
        "provider": "StravaProvider",
        "providerActivityId": "string",
        "legacySubmissionId": "string|null?",
        "redactedSummary": "record",
        "consentText": "string",
        "consentedAt": "string",
        "status": "ActivityEvidenceCandidateStatus",
        "createdAt": "string",
        "updatedAt": "string"
    },
    "AttachEvidenceRequest": {
        "activity_id": "string",
        "consent_acknowledged": "boolean?",
        "consent_text": "string?",
        "legacy_submission_id": "string?"
    },
    "EvidenceResponse": {
        "evidence_candidate": "PublicEvidence",
        "suggested_track": "PublicTrack?"
    },
    "EvidenceAuthority": {
        "activity_summary": "string",
        "route_geometry": "NoClaim",
        "scoring": "NoClaim"
    },
    "PublicEvidence": {
        "id": "string",
        "suggested_track_id": "string",
        "provider": "StravaProvider",
        "provider_activity_id": "string",
        "redacted_summary": "ActivitySummary",
        "consented_at": "string",
        "status": "ActivityEvidenceCandidateStatus",
        "created_at": "string",
        "updated_at": "string",
        "authority": "EvidenceAuthority"
    },
    "EvidenceSummaryAuthority": {
        "activity_summary": "string",
        "route_geometry": "NoClaim",
        "scoring": "NoClaim",
        "pilot_ready": "NoClaim"
    },
    "EvidenceSummary": {
        "candidate_count": "number",
        "redaction": "RedactionReceipt",
        "authority": "EvidenceSummaryAuthority"
    },
    "LegacySubmissionRequest": {
        "track_id": "string",
        "activity_id": "string|number|null?",
        "activity_name": "string|null?",
        "moving_time": "number|null?",
        "distance": "number|null?",
        "average_speed": "number|null?"
    },
    "LegacyTracksResponse": {
        "tracks": "LegacyTrack[]"
    },
    "LegacySubmissionsResponse": {
        "submissions": "LegacySubmission[]"
    },
    "LegacySubmissionResponse": {
        "submission": "unknown"
    },
    "LegacyTrack": {
        "id": "string",
        "name": "string",
        "pilot": "string",
        "description": "string",
        "controller_metric": "string"
    },
    "LegacySubmission": {
        "id": "string",
        "created_at": "number",
        "athlete_id": "string|number",
        "athlete_name": "string",
        "track_id": "string",
        "activity_id": "string|number|null?",
        "activity_name": "string|null?",
        "moving_time": "number|null?",
        "distance": "number|null?",
        "average_speed": "number|null?",
        "status": "string",
        "authority": "string",
        "public_controller_metric": "string",
        "parallel_evidence": "string"
    },
    "RetiredLegacyResponse": {
        "error": "string",
        "message": "string",
        "next": "string"
    },
    "MigrationItem": {
        "id": "string",
        "activity_id": "string",
        "activity_name": "string",
        "legacy_track_name": "string",
        "status": "MigrationStatus",
        "suggested_track_id": "string|null",
        "evidence_candidate_id": "string|null"
    },
    "MigrationQueueResponse": {
        "items": "MigrationItem[]",
        "has_more": "boolean"
    },
    "MigrationPageRequest": {
        "page": "string?",
        "per_page": "string?"
    }
};
const enums = {
    "StravaProvider": [
        "strava"
    ],
    "ProviderStatus": [
        "linked",
        "disconnected"
    ],
    "SuggestedTrackStatus": [
        "needs_evidence",
        "evidence_submitted",
        "operator_review",
        "source_backed",
        "retired"
    ],
    "NoClaim": [
        "not_claimed"
    ],
    "ActivityEvidenceCandidateStatus": [
        "submitted",
        "operator_review",
        "accepted",
        "rejected"
    ],
    "MigrationStatus": [
        "requires_consent",
        "migrated"
    ]
};
function valid(t, v) { if (t.endsWith('?'))
    return v === undefined || valid(t.slice(0, -1), v); if (t.endsWith('|null'))
    return v === null || valid(t.slice(0, -5), v); if (t.includes('|'))
    return t.split('|').some(part => valid(part, v)); if (t.endsWith('[]'))
    return Array.isArray(v) && v.every(x => valid(t.slice(0, -2), x)); if (t === 'unknown')
    return true; if (t === 'number')
    return typeof v === 'number' && Number.isFinite(v); if (t === 'string' || t === 'boolean')
    return typeof v === t; if (t === 'record')
    return !!v && typeof v === 'object' && !Array.isArray(v); const en = enums[t]; if (en)
    return typeof v === 'string' && en.includes(v); const fields = records[t]; if (!fields || !v || typeof v !== 'object' || Array.isArray(v))
    return false; const obj = v; return Object.keys(obj).every(k => Object.hasOwn(fields, k)) && Object.entries(fields).every(([k, type]) => valid(type, obj[k])); }
export function assertRecord(name, value) { if (!valid(name, value))
    throw Error('APPLICATION_RESPONSE_CONTRACT:' + name); }
//# sourceMappingURL=validation.js.map