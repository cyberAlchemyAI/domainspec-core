# Mappings

Status: `draft-pass`

## Strava Activity To RunActivity

| Strava Field | Domain Field | Rule |
| --- | --- | --- |
| `id` | `activityId` | Stringify if needed. |
| `name` | `name` | Preserve display name; trim. |
| `sport_type` or `type` | `sportType` | Only run-like types can be submitted. |
| `distance` | `distanceMeters` | Numeric meters. |
| `moving_time` | `movingTimeSeconds` | Numeric seconds. |
| `average_speed` | `averageSpeed` | Numeric meters/second. |
| `start_date` | `startedAt` | ISO date if provided. |
| maps/private payloads | none | Do not expose in read model. |
| access/refresh token | none | Never map to browser/domain read model. |

## RunActivity To EvidenceSubmission

| Activity Field | Submission Field | Rule |
| --- | --- | --- |
| `activityId` | `activityId` | Required. |
| runner session | `runnerId` | Derived from server auth context. |
| selected track | `territoryId` | Required. |
| distance/time/speed | `redactedMetrics` | Persist summary only. |
| submit time | `submittedAt` | Server clock. |
| preview mode | `status` | Start as `submitted`, then `preview-accepted` if policy passes. |

## EvidenceSubmission To ControllerState

| Submission Field | Controller Field | Rule |
| --- | --- | --- |
| `territoryId` | `territoryId` | Same territory. |
| `runnerId` | `controllerRunnerId` | Accepted winner. |
| redacted time/speed | `metricValue` | Metric-specific. |
| `preview-accepted` | `basis=preview` | Never `verified`. |
| `verified` | `basis=verified` | Requires operator or validation path. |

## Visual Source To UI Tokens

| Source Note Claim | UI Token / Rule |
| --- | --- |
| Orange/fire | Primary action and challenge urgency. |
| Green/territory | Controlled state, map ownership, success. |
| Dark/light variants | App shell, contrast bands, map overlays. |
| Bebas Neue titles | Display/headline style. |
| DM Sans body | Body, forms, data labels. |
| Bottom nav concepts | Home, Routes, Challenges, Community, Profile. |
