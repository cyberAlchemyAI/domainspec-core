# Application operations

## ReadStatus

### Rules

| ID | Rule | Formal |
| --- | --- | --- |
| AUTH | Public configuration and optional connection status; never returns tokens. | {"authentication":"public","permission":null} |
| EFFECT0 | Bound adapter effect | read:session |
| EFFECT1 | Bound adapter effect | read:ProviderAccount |

## ReadProfile

### Rules

| ID | Rule | Formal |
| --- | --- | --- |
| AUTH | Authenticated safe principal/profile view. | {"authentication":"session","permission":null} |
| EFFECT0 | Bound adapter effect | read:RunnerProfile |
| EFFECT1 | Bound adapter effect | read:ProviderAccount |

## StartStrava

### Rules

| ID | Rule | Formal |
| --- | --- | --- |
| AUTH | Legacy fake-provider login, or authenticated CSRF-protected provider linking when OIDC identity mode is selected. | {"authentication":"public","permission":null} |
| EFFECT0 | Bound adapter effect | create:OAuthState |
| EFFECT1 | Bound adapter effect | set:state-cookie |

## CompleteStrava

### Rules

| ID | Rule | Formal |
| --- | --- | --- |
| AUTH | Validate single-use state and browser cookie. OIDC mode links to the current session without issuing identity; the legacy Strava pilot creates its own session. | {"authentication":"public","permission":null} |
| EFFECT0 | Bound adapter effect | consume:OAuthState |
| EFFECT1 | Bound adapter effect | exchange:provider-code |
| EFFECT2 | Bound adapter effect | upsert:ProviderAccount |
| EFFECT3 | Bound adapter effect | upsert:RunnerProfile |
| EFFECT4 | Bound adapter effect | encrypt:ProviderTokenRecord |
| EFFECT5 | Bound adapter effect | create:session |

## Logout

### Rules

| ID | Rule | Formal |
| --- | --- | --- |
| AUTH | Logout accepts an already absent session; valid sessions require CSRF/origin guards. | {"authentication":"optional-session","permission":null} |
| EFFECT0 | Bound adapter effect | revoke:session |
| EFFECT1 | Bound adapter effect | clear:cookies |

## StartOidc

### Rules

| ID | Rule | Formal |
| --- | --- | --- |
| AUTH | Fixed self-hosted issuer login or bounded active-session renewal; never arbitrary redirects. | {"authentication":"public","permission":null} |
| EFFECT0 | Bound adapter effect | create:OidcTransaction |
| EFFECT1 | Bound adapter effect | set:login-cookie |

## CompleteOidc

### Rules

| ID | Rule | Formal |
| --- | --- | --- |
| AUTH | Validate OIDC identity and transaction, map issuer/subject, rotate local session; reject revoked parents. | {"authentication":"public","permission":null} |
| EFFECT0 | Bound adapter effect | consume:OidcTransaction |
| EFFECT1 | Bound adapter effect | verify:issuer-identity |
| EFFECT2 | Bound adapter effect | create:session |

## LinkStrava

### Rules

| ID | Rule | Formal |
| --- | --- | --- |
| AUTH | Explicit authenticated provider link with CSRF and session-bound single-use state. | {"authentication":"session","permission":null} |
| EFFECT0 | Bound adapter effect | create:OAuthState |
| EFFECT1 | Bound adapter effect | set:state-cookie |

## ReadSecurity

### Rules

| ID | Rule | Formal |
| --- | --- | --- |
| AUTH | Authenticated durable security settings page; adapter verifies the current issuer and app session. | {"authentication":"public","permission":null} |
| EFFECT0 | Bound adapter effect | verify:issuer-identity |

## ChangeSecurity

### Rules

| ID | Rule | Formal |
| --- | --- | --- |
| AUTH | Verify current session, exact origin, session-bound CSRF and allowlisted action before fresh Keycloak authentication. | {"authentication":"public","permission":null} |
| EFFECT0 | Bound adapter effect | create:OidcTransaction |
| EFFECT1 | Bound adapter effect | set:login-cookie |

## ListActivities

### Rules

| ID | Rule | Formal |
| --- | --- | --- |
| AUTH | Consult activities for the authenticated runner and redact the provider response. | {"authentication":"session","permission":"body-war.activity.read"} |
| EFFECT0 | Bound adapter effect | consult:Strava |
| EFFECT1 | Bound adapter effect | no-persist:raw-provider-response |

## ListTracks

### Rules

| ID | Rule | Formal |
| --- | --- | --- |
| AUTH | List suggestions for a connected runner. | {"authentication":"connected","permission":"body-war.suggested-track.read"} |
| EFFECT0 | Bound adapter effect | read:SuggestedTrack |

## CreateTrack

### Rules

| ID | Rule | Formal |
| --- | --- | --- |
| AUTH | Create a needs-evidence suggestion with no geometry or scoring claim. | {"authentication":"connected","permission":"body-war.suggested-track.create"} |
| EFFECT0 | Bound adapter effect | create:SuggestedTrack |

## ReadTrack

### Rules

| ID | Rule | Formal |
| --- | --- | --- |
| AUTH | Retrieve one track and only the current runner evidence candidates. | {"authentication":"connected","permission":"body-war.suggested-track.read"} |
| EFFECT0 | Bound adapter effect | read:SuggestedTrack |
| EFFECT1 | Bound adapter effect | read:own-ActivityEvidenceCandidate |

## AttachEvidence

### Rules

| ID | Rule | Formal |
| --- | --- | --- |
| AUTH | Attach only a visible provider activity with explicit consent, redaction and duplicate rejection. | {"authentication":"connected","permission":"body-war.suggested-track-evidence.create"} |
| EFFECT0 | Bound adapter effect | check:generated-consent |
| EFFECT1 | Bound adapter effect | consult:own-Strava-activity |
| EFFECT2 | Bound adapter effect | reject:duplicate |
| EFFECT3 | Bound adapter effect | persist:redacted-candidate |
| EFFECT4 | Bound adapter effect | transition:TrackEvidenceLifecycle |

## WithdrawEvidence

### Rules

| ID | Rule | Formal |
| --- | --- | --- |
| AUTH | Delete own evidence and consent; no connected provider required. Fresh consent is required for resubmission. | {"authentication":"session","permission":null} |
| EFFECT0 | Bound adapter effect | check:owner |
| EFFECT1 | Bound adapter effect | erase:summary-and-consent |
| EFFECT2 | Bound adapter effect | transition:TrackEvidenceLifecycle |
## Open Questions

See ../../README.md#open-questions.

## PilotCriticalRequirements

### Rules

| ID | Rule | Formal |
| --- | --- | --- |
| SEC_ISOLATION | Runner-scoped detail returns no other runner evidence and profile resolves to the authenticated principal. | Runner-scoped detail returns no other runner evidence and profile resolves to the authenticated principal. |
| SEC_PERMISSION | Anonymous access returns 401 and an authenticated principal without the read grant receives 403. | Anonymous access returns 401 and an authenticated principal without the read grant receives 403. |
| SEC_OAUTH_REPLAY | A consumed OAuth callback cannot mint a second browser session. | A consumed OAuth callback cannot mint a second browser session. |
| SEC_CSRF | Missing CSRF and an untrusted origin reject a valid-session write. | Missing CSRF and an untrusted origin reject a valid-session write. |
| SEC_REQUEST | Malformed, unknown-field, wrong-type and oversized JSON requests are rejected before persistence. | Malformed, unknown-field, wrong-type and oversized JSON requests are rejected before persistence. |
| SEC_REVOCATION | Internal consent disposition erases the exact candidate, resets the empty track and is idempotent. | Internal consent disposition erases the exact candidate, resets the empty track and is idempotent. |
| DB_OAUTH | Twelve concurrent PostgreSQL consumers return exactly one OAuth state; expiry at the boundary is rejected. | Twelve concurrent PostgreSQL consumers return exactly one OAuth state; expiry at the boundary is rejected. |
| DB_DUPLICATE | Twelve concurrent identical attachments create exactly one row; uniqueness includes runner identity. | Twelve concurrent identical attachments create exactly one row; uniqueness includes runner identity. |
| DB_ATOMIC | Failure between evidence insertion and track update rolls both back and permits one successful retry. | Failure between evidence insertion and track update rolls both back and permits one successful retry. |
| DB_DISPOSITION | Concurrent disposition and replacement preserve the new candidate and consistent track state. | Concurrent disposition and replacement preserve the new candidate and consistent track state. |
| DB_PERSISTENCE | A fresh reader process sees committed evidence and track state after all writer connections close. | A fresh reader process sees committed evidence and track state after all writer connections close. |

## CreateTrackRules

### Rules

| ID | Rule | Formal |
| --- | --- | --- |
| name | Trim and truncate text using UTF-16 code units; required text remains nonempty; optional distance is a positive integer or null. | {"operation":"CreateTrack","field":"name","rule":{"kind":"text","min":1,"max":255},"error":"invalid_suggested_track"} |
| place_label | Trim and truncate text using UTF-16 code units; required text remains nonempty; optional distance is a positive integer or null. | {"operation":"CreateTrack","field":"place_label","rule":{"kind":"text","min":1,"max":255},"error":"invalid_suggested_track"} |
| city | Trim and truncate text using UTF-16 code units; required text remains nonempty; optional distance is a positive integer or null. | {"operation":"CreateTrack","field":"city","rule":{"kind":"text","min":1,"max":120},"error":"invalid_suggested_track"} |
| public_note | Trim and truncate text using UTF-16 code units; required text remains nonempty; optional distance is a positive integer or null. | {"operation":"CreateTrack","field":"public_note","rule":{"kind":"text","min":0,"max":500},"error":"invalid_suggested_track"} |
| distance_hint_meters | Trim and truncate text using UTF-16 code units; required text remains nonempty; optional distance is a positive integer or null. | {"operation":"CreateTrack","field":"distance_hint_meters","rule":{"kind":"positive-integer"},"error":"invalid_suggested_track"} |

## EvidenceInputRules

### Rules

| ID | Rule | Formal |
| --- | --- | --- |
| activity_id | Trim and truncate id and consent text before the existing generated consent predicate. | {"operation":"AttachEvidence","field":"activity_id","rule":{"kind":"text","min":0,"max":255},"error":"invalid_evidence_request"} |
| consent_text | Trim and truncate id and consent text before the existing generated consent predicate. | {"operation":"AttachEvidence","field":"consent_text","rule":{"kind":"text","min":0,"max":500},"error":"invalid_evidence_request"} |

## ActivityPagination

### Rules

| ID | Rule | Formal |
| --- | --- | --- |
| page | Closed query with Number conversion, integer bounds, absent-value defaults and duplicate rejection. | {"operation":"ListActivities","field":"page","rule":{"kind":"integer","min":1,"max":10,"default":1},"error":"strava_provider_bounds_invalid"} |
| per_page | Closed query with Number conversion, integer bounds, absent-value defaults and duplicate rejection. | {"operation":"ListActivities","field":"per_page","rule":{"kind":"integer","min":1,"max":100,"default":20},"error":"strava_provider_bounds_invalid"} |
