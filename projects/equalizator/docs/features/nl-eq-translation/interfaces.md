# Interfaces: NL to EQ Translation

## External: Equalizator Translation API (HTTP/JSON)

### POST /api/v1/eq/translate

**Exposes:** [TranslatePromptToEqPlan](operations.md#translateprompttoeqplan)
**Auth:** Bearer token

**Request:**

| Field | Type | Maps To |
| --- | --- | --- |
| requestId | string | [TranslatePromptToEqPlan](operations.md#translateprompttoeqplan).requestId |
| promptText | string | [TranslatePromptToEqPlan](operations.md#translateprompttoeqplan).promptText |
| listeningContext | object | [TranslatePromptToEqPlan](operations.md#translateprompttoeqplan).listeningContext |
| sourceAudioRef | string | [TranslatePromptToEqPlan](operations.md#translateprompttoeqplan).sourceAudioRef |
| constraints | object | [TranslatePromptToEqPlan](operations.md#translateprompttoeqplan).constraints |

**Responses:**

| Status | Condition | Body |
| --- | --- | --- |
| 200 | Success | planId, bands, explanation, confidence, objectiveScore |
| 400 | Rule violation | errorCode, message, violations |
| 422 | Low confidence or no safe candidate | errorCode, message |
| 500 | Internal failure | errorCode, traceId |

### POST /api/v1/eq/validate

**Exposes:** [ValidateEqPlanSafety](operations.md#validateeqplansafety)
**Auth:** Bearer token

**Request:**

| Field | Type | Maps To |
| --- | --- | --- |
| plan | object | [ValidateEqPlanSafety](operations.md#validateeqplansafety).plan |
| envelope | object | [ValidateEqPlanSafety](operations.md#validateeqplansafety).envelope |
| predictedTruePeakDbtp | number | [ValidateEqPlanSafety](operations.md#validateeqplansafety).predictedTruePeakDbtp |

**Responses:**

| Status | Condition | Body |
| --- | --- | --- |
| 200 | Validation complete | safetyPassed, margin, violations |
| 400 | Invalid payload | errorCode, message |
| 422 | Safety rule failure | errorCode, violations |

### POST /api/v1/eq/feedback

**Exposes:** [CapturePlanFeedback](operations.md#captureplanfeedback)
**Auth:** Bearer token

**Request:**

| Field | Type | Maps To |
| --- | --- | --- |
| planId | string | [CapturePlanFeedback](operations.md#captureplanfeedback).planId |
| action | string | [CapturePlanFeedback](operations.md#captureplanfeedback).action |
| editedBands | array | [CapturePlanFeedback](operations.md#captureplanfeedback).editedBands |
| rating | number | [CapturePlanFeedback](operations.md#captureplanfeedback).rating |
| comment | string | [CapturePlanFeedback](operations.md#captureplanfeedback).comment |

**Responses:**

| Status | Condition | Body |
| --- | --- | --- |
| 202 | Feedback accepted | feedbackId, status |
| 400 | Invalid payload | errorCode, message |
| 404 | Plan not found | errorCode, message |

---

## Internal: EqRecommendationEngine Interface

**Consumers:** API layer, batch evaluation tools, experimentation framework

| Method | Maps To | Description |
| --- | --- | --- |
| translate(request) | TranslatePromptToEqPlan operation | Generate and publish one recommendation |
| validate(plan, envelope, predictedPeak) | ValidateEqPlanSafety operation | Safety check for generated or edited plan |
| captureFeedback(payload) | CapturePlanFeedback operation | Persist learning signal |
| getPlanByRequest(requestId) | GetEqPlanByRequest query | Fetch latest recommendation |
| simulateImpact(plan, sourceAudioRef) | SimulateEqPlanImpact query | Estimate effect of candidate plan |