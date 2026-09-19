// Generated operation contracts.
export const operationContracts = {
  "ReadStatus": {
    "authentication": "public",
    "permission": null,
    "effects": [
      "read:session",
      "read:ProviderAccount"
    ],
    "input": "EmptyRequest",
    "output": "StatusResponse"
  },
  "ReadProfile": {
    "authentication": "session",
    "permission": null,
    "effects": [
      "read:RunnerProfile",
      "read:ProviderAccount"
    ],
    "input": "EmptyRequest",
    "output": "ProfileResponse"
  },
  "StartStrava": {
    "authentication": "public",
    "permission": null,
    "effects": [
      "create:OAuthState",
      "set:state-cookie"
    ],
    "input": "EmptyRequest",
    "output": "OpaqueResponse"
  },
  "CompleteStrava": {
    "authentication": "public",
    "permission": null,
    "effects": [
      "consume:OAuthState",
      "exchange:provider-code",
      "upsert:ProviderAccount",
      "upsert:RunnerProfile",
      "encrypt:ProviderTokenRecord",
      "create:session"
    ],
    "input": "OAuthCallbackRequest",
    "output": "OpaqueResponse"
  },
  "Logout": {
    "authentication": "optional-session",
    "permission": null,
    "effects": [
      "revoke:session",
      "clear:cookies"
    ],
    "input": "EmptyRequest",
    "output": "LogoutResponse"
  },
  "StartOidc": {
    "authentication": "public",
    "permission": null,
    "effects": [
      "create:OidcTransaction",
      "set:login-cookie"
    ],
    "input": "EmptyRequest",
    "output": "OpaqueResponse"
  },
  "CompleteOidc": {
    "authentication": "public",
    "permission": null,
    "effects": [
      "consume:OidcTransaction",
      "verify:issuer-identity",
      "create:session"
    ],
    "input": "OAuthCallbackRequest",
    "output": "OpaqueResponse"
  },
  "LinkStrava": {
    "authentication": "session",
    "permission": null,
    "effects": [
      "create:OAuthState",
      "set:state-cookie"
    ],
    "input": "EmptyRequest",
    "output": "ProviderLinkResponse"
  },
  "ReadSecurity": {
    "authentication": "public",
    "permission": null,
    "effects": [
      "verify:issuer-identity"
    ],
    "input": "EmptyRequest",
    "output": "OpaqueResponse"
  },
  "ChangeSecurity": {
    "authentication": "public",
    "permission": null,
    "effects": [
      "create:OidcTransaction",
      "set:login-cookie"
    ],
    "input": "EmptyRequest",
    "output": "OpaqueResponse"
  },
  "ListActivities": {
    "authentication": "session",
    "permission": "body-war.activity.read",
    "effects": [
      "consult:Strava",
      "no-persist:raw-provider-response"
    ],
    "input": "ActivityPageRequest",
    "output": "ActivitiesResponse"
  },
  "ListTracks": {
    "authentication": "connected",
    "permission": "body-war.suggested-track.read",
    "effects": [
      "read:SuggestedTrack"
    ],
    "input": "EmptyRequest",
    "output": "TrackListResponse"
  },
  "CreateTrack": {
    "authentication": "connected",
    "permission": "body-war.suggested-track.create",
    "effects": [
      "create:SuggestedTrack"
    ],
    "input": "CreateTrackRequest",
    "output": "TrackResponse"
  },
  "ReadTrack": {
    "authentication": "connected",
    "permission": "body-war.suggested-track.read",
    "effects": [
      "read:SuggestedTrack",
      "read:own-ActivityEvidenceCandidate"
    ],
    "input": "TrackKeyRequest",
    "output": "TrackResponse"
  },
  "AttachEvidence": {
    "authentication": "connected",
    "permission": "body-war.suggested-track-evidence.create",
    "effects": [
      "check:generated-consent",
      "consult:own-Strava-activity",
      "reject:duplicate",
      "persist:redacted-candidate",
      "transition:TrackEvidenceLifecycle"
    ],
    "input": "AttachEvidenceRequest",
    "output": "EvidenceResponse"
  },
  "WithdrawEvidence": {
    "authentication": "session",
    "permission": null,
    "effects": [
      "check:owner",
      "erase:summary-and-consent",
      "transition:TrackEvidenceLifecycle"
    ],
    "input": "EmptyRequest",
    "output": "WithdrawEvidenceResponse"
  }
} as const;
export type OperationId = keyof typeof operationContracts;
