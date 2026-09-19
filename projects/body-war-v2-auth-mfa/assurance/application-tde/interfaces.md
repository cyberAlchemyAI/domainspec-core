# Application interfaces

### GET /api/status

**Responses:**

| Status | Condition | Body |
| --- | --- | --- |
| 200 | success | StatusResponse |
| 500 | adapter error | error response |

### GET /api/profile

**Responses:**

| Status | Condition | Body |
| --- | --- | --- |
| 200 | success | ProfileResponse |
| 400 | adapter error | error response |
| 401 | adapter error | error response |
| 403 | adapter error | error response |
| 500 | adapter error | error response |

### GET /api/auth/strava/start

**Responses:**

| Status | Condition | Body |
| --- | --- | --- |
| 302 | success | OpaqueResponse |
| 400 | adapter error | error response |
| 405 | adapter error | error response |
| 500 | adapter error | error response |

### GET /api/auth/strava/callback

**Responses:**

| Status | Condition | Body |
| --- | --- | --- |
| 302 | success | OpaqueResponse |
| 500 | adapter error | error response |

### POST /api/auth/logout

**Responses:**

| Status | Condition | Body |
| --- | --- | --- |
| 200 | success | LogoutResponse |
| 400 | adapter error | error response |
| 401 | adapter error | error response |
| 403 | adapter error | error response |
| 500 | adapter error | error response |

### GET /api/auth/oidc/start

**Responses:**

| Status | Condition | Body |
| --- | --- | --- |
| 303 | success | OpaqueResponse |
| 404 | adapter error | error response |
| 500 | adapter error | error response |

### GET /api/auth/oidc/callback

**Responses:**

| Status | Condition | Body |
| --- | --- | --- |
| 303 | success | OpaqueResponse |
| 404 | adapter error | error response |
| 500 | adapter error | error response |

### POST /api/auth/strava/link

**Responses:**

| Status | Condition | Body |
| --- | --- | --- |
| 200 | success | ProviderLinkResponse |
| 400 | adapter error | error response |
| 401 | adapter error | error response |
| 403 | adapter error | error response |
| 500 | adapter error | error response |

### GET /api/auth/security

**Responses:**

| Status | Condition | Body |
| --- | --- | --- |
| 200 | success | OpaqueResponse |
| 400 | adapter error | error response |
| 401 | adapter error | error response |
| 404 | adapter error | error response |
| 503 | adapter error | error response |

### POST /api/auth/security

**Responses:**

| Status | Condition | Body |
| --- | --- | --- |
| 303 | success | OpaqueResponse |
| 400 | adapter error | error response |
| 401 | adapter error | error response |
| 403 | adapter error | error response |
| 404 | adapter error | error response |
| 413 | adapter error | error response |
| 415 | adapter error | error response |
| 503 | adapter error | error response |

### GET /api/activities

**Responses:**

| Status | Condition | Body |
| --- | --- | --- |
| 200 | success | ActivitiesResponse |
| 400 | adapter error | error response |
| 401 | adapter error | error response |
| 403 | adapter error | error response |
| 500 | adapter error | error response |

### GET /api/suggested-tracks

**Responses:**

| Status | Condition | Body |
| --- | --- | --- |
| 200 | success | TrackListResponse |
| 400 | adapter error | error response |
| 401 | adapter error | error response |
| 403 | adapter error | error response |
| 500 | adapter error | error response |

### POST /api/suggested-tracks

**Responses:**

| Status | Condition | Body |
| --- | --- | --- |
| 201 | success | TrackResponse |
| 400 | adapter error | error response |
| 401 | adapter error | error response |
| 403 | adapter error | error response |
| 413 | adapter error | error response |
| 500 | adapter error | error response |

### GET /api/suggested-tracks/:idOrSlug

**Responses:**

| Status | Condition | Body |
| --- | --- | --- |
| 200 | success | TrackResponse |
| 401 | adapter error | error response |
| 403 | adapter error | error response |
| 404 | adapter error | error response |
| 409 | adapter error | error response |
| 500 | adapter error | error response |

### POST /api/suggested-tracks/:idOrSlug/evidence-candidates

**Responses:**

| Status | Condition | Body |
| --- | --- | --- |
| 201 | success | EvidenceResponse |
| 400 | adapter error | error response |
| 401 | adapter error | error response |
| 403 | adapter error | error response |
| 404 | adapter error | error response |
| 409 | adapter error | error response |
| 413 | adapter error | error response |
| 429 | adapter error | error response |
| 500 | adapter error | error response |
| 502 | adapter error | error response |

### POST /api/evidence-candidates/:id/withdraw

**Responses:**

| Status | Condition | Body |
| --- | --- | --- |
| 200 | success | WithdrawEvidenceResponse |
| 400 | adapter error | error response |
| 401 | adapter error | error response |
| 403 | adapter error | error response |
| 413 | adapter error | error response |
| 429 | adapter error | error response |
| 500 | adapter error | error response |
## Open Questions

See ../../README.md#open-questions.
