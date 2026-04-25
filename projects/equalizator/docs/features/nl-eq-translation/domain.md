# Domain: NL to EQ Translation

## Entities

### TranslationRequest

Represents one natural-language request to generate a tonal correction or enhancement plan.

| Field | Type | Required | Description |
| --- | --- | --- | --- |
| id | TranslationRequestId | yes | Unique request identifier |
| promptText | string | yes | Raw natural-language tonal request |
| listeningContext | [ListeningContext](#listeningcontext) | no | Playback target and environment |
| sourceAudioRef | string | no | Reference to analyzed audio source |
| constraints | [SafetyEnvelope](#safetyenvelope) | no | User or profile safety constraints |
| intentVector | [IntentVector](#intentvector) | no | Parsed representation of prompt intent |
| status | [TranslationStatus](#translationstatus) | yes | Current lifecycle state |
| createdAt | datetime | yes | Creation timestamp |

**Lifecycle:** See [TranslationRequestState](states.md#translationrequeststate)
**Operations:** [TranslatePromptToEqPlan](operations.md#translateprompttoeqplan), [ValidateEqPlanSafety](operations.md#validateeqplansafety)

---

### EqPlan

Represents one recommended EQ strategy linked to a translation request.

| Field | Type | Required | Description |
| --- | --- | --- | --- |
| id | EqPlanId | yes | Unique plan identifier |
| requestId | TranslationRequestId | yes | Parent request |
| bands | [EqBand](#eqband)[] | yes | Ordered filter set |
| explanation | string | yes | Plain-language rationale |
| confidence | number | yes | Translation confidence in [0,1] |
| objectiveScore | number | yes | Weighted quality and safety score |
| safetyPassed | boolean | yes | Whether hard guards passed |
| createdAt | datetime | yes | Publish timestamp |

**Lifecycle:** See [TranslationRequestState](states.md#translationrequeststate)
**Operations:** [TranslatePromptToEqPlan](operations.md#translateprompttoeqplan), [CapturePlanFeedback](operations.md#captureplanfeedback)

---

### PlanFeedback

Stores user outcomes for one published recommendation.

| Field | Type | Required | Description |
| --- | --- | --- | --- |
| id | PlanFeedbackId | yes | Feedback identifier |
| planId | EqPlanId | yes | Target plan |
| action | [FeedbackAction](#feedbackaction) | yes | accept, reject, or edit |
| editedBands | [EqBand](#eqband)[] | no | User-adjusted bands, when action is edit |
| rating | number | no | Optional subjective score (1-5) |
| comment | string | no | Optional qualitative note |
| createdAt | datetime | yes | Capture timestamp |

**Operations:** [CapturePlanFeedback](operations.md#captureplanfeedback)

---

## Value Objects

### EqBand

| Field | Type | Constraint |
| --- | --- | --- |
| filterType | [FilterType](#filtertype) | Required |
| frequencyHz | number | 20 <= frequencyHz <= 20000 |
| gainDb | number | -9 <= gainDb <= 9 |
| q | number | 0.3 <= q <= 8 |

**Equality:** same filterType, frequencyHz, gainDb, and q.

---

### ListeningContext

| Field | Type | Constraint |
| --- | --- | --- |
| deviceProfile | string | one of configured playback classes |
| environment | string | optional |
| contentType | string | optional |

**Equality:** same deviceProfile, environment, and contentType.

---

### IntentVector

| Field | Type | Constraint |
| --- | --- | --- |
| warmth | number | 0 <= x <= 1 |
| brightness | number | 0 <= x <= 1 |
| punch | number | 0 <= x <= 1 |
| clarity | number | 0 <= x <= 1 |
| smoothness | number | 0 <= x <= 1 |
| weight | number | Sum of active dimensions normalized |

**Equality:** all dimensions equal within tolerance epsilon = 0.01.

---

### SafetyEnvelope

| Field | Type | Constraint |
| --- | --- | --- |
| maxAbsGainDb | number | 1 <= x <= 12 |
| maxBandCount | number | 1 <= x <= 12 |
| minQ | number | 0.1 <= x <= 2 |
| maxQ | number | 2 <= x <= 12 |
| maxPredictedTruePeakDbtp | number | <= -1.0 |

**Equality:** all fields exactly equal.

---

## Enums

### DescriptorToken

| Value | Description |
| --- | --- |
| muddy | Excess low-mid energy, reduced clarity |
| boomy | Excess low-end resonance or buildup |
| harsh | Excess upper-mid energy causing fatigue |
| dull | Missing high-frequency openness |
| sibilant | Excess energy around speech sibilance range |
| thin | Insufficient low-mid body |
| boxy | Resonance around lower-mid enclosure tone |
| bright | Elevated high-frequency presence |

### FilterType

| Value | Description |
| --- | --- |
| bell | Peak or dip around center frequency |
| low_shelf | Broad low-frequency tilt |
| high_shelf | Broad high-frequency tilt |
| high_pass | Remove sub-low frequencies |
| low_pass | Remove high frequencies |
| notch | Narrow attenuation for resonant tone |

### TranslationStatus

| Value | Description |
| --- | --- |
| RECEIVED | Request created and awaiting parse |
| PARSED | Intent vector generated |
| ANALYZED | Audio features extracted |
| GENERATED | Candidate plans synthesized |
| VALIDATED | Candidate passed safety checks |
| PUBLISHED | Plan returned to user |
| FAILED | Flow terminated due to unrecoverable issue |

### FeedbackAction

| Value | Description |
| --- | --- |
| ACCEPTED | User accepted recommendation |
| REJECTED | User rejected recommendation |
| EDITED | User modified recommendation before acceptance |