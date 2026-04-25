# Operations: NL to EQ Translation

## TranslatePromptToEqPlan

**Type:** Operation (mutation)
**Actor:** Authenticated user or system client
**Triggers:** User submits natural-language tonal request

### Input

| Field | Type | Required | Description |
| --- | --- | --- | --- |
| requestId | TranslationRequestId | yes | Correlation identifier |
| promptText | string | yes | User tonal request |
| listeningContext | [ListeningContext](domain.md#listeningcontext) | no | Target playback context |
| sourceAudioRef | string | no | Reference to source audio |
| constraints | [SafetyEnvelope](domain.md#safetyenvelope) | no | Optional custom limits |

### Rules

| ID | Rule | Formal |
| --- | --- | --- |
| R1 | Prompt must be non-empty and bounded | 1 <= len(promptText) <= 500 |
| R2 | At least one descriptor token or mappable phrase must be extracted | token_count >= 1 |
| R3 | Candidate plan band count must stay under configured maximum | band_count <= maxBandCount |
| R4 | Every generated band must respect parameter bounds | forall band: -maxAbsGainDb <= gainDb <= maxAbsGainDb and minQ <= q <= maxQ |
| R5 | Prediction confidence must exceed publication threshold | confidence >= publishThreshold |

### Calculations

| ID | Calculation | Formula |
| --- | --- | --- |
| C1 | Intent vector normalization | intent_i = weight_i / sum(weights) |
| C2 | Objective score | score = w1*tonal_match - w2*masking_risk - w3*peak_risk - w4*complexity |
| C3 | Translation confidence | confidence = calibrated(parser_confidence, model_agreement, safety_margin) |

### State Transition

[TranslationRequest](domain.md#translationrequest): RECEIVED -> PUBLISHED

### Postconditions

- A validated [EqPlan](domain.md#eqplan) is persisted and returned.
- A publication event is emitted with explanation and confidence.
- Full trace data is stored for offline evaluation.

### Error States

| Condition | Result |
| --- | --- |
| Parser cannot resolve intent | Request marked FAILED with parse_error |
| No candidate passes safety rules | Request marked FAILED with safety_error |
| Confidence below publish threshold | Request marked FAILED with low_confidence |

## ValidateEqPlanSafety

**Type:** Operation (mutation)
**Actor:** System policy engine
**Triggers:** Candidate EQ plan generated or externally edited

### Input

| Field | Type | Required | Description |
| --- | --- | --- | --- |
| plan | [EqPlan](domain.md#eqplan) | yes | Candidate plan to validate |
| envelope | [SafetyEnvelope](domain.md#safetyenvelope) | yes | Active safety limits |
| predictedTruePeakDbtp | number | yes | Estimated true peak after applying plan |

### Rules

| ID | Rule | Formal |
| --- | --- | --- |
| R1 | Per-band gain stays within bound | forall band: abs(gainDb) <= envelope.maxAbsGainDb |
| R2 | Q stays within configured range | forall band: envelope.minQ <= q <= envelope.maxQ |
| R3 | Band count stays within limit | len(bands) <= envelope.maxBandCount |
| R4 | Predicted true peak stays below guardrail | predictedTruePeakDbtp <= envelope.maxPredictedTruePeakDbtp |

### Calculations

| ID | Calculation | Formula |
| --- | --- | --- |
| C1 | Safety margin | margin = envelope.maxPredictedTruePeakDbtp - predictedTruePeakDbtp |
| C2 | Violation count | violations = sum(rule_failed_i) |

### State Transition

[TranslationRequest](domain.md#translationrequest): GENERATED -> VALIDATED

### Postconditions

- Plan is marked safetyPassed=true when all rules pass.
- Validation report with failures and margins is attached to plan.

### Error States

| Condition | Result |
| --- | --- |
| Any safety rule fails | Plan rejected with violation details |
| Predicted peak unavailable | Validation deferred or failed by policy |

## CapturePlanFeedback

**Type:** Operation (mutation)
**Actor:** Authenticated user or system client
**Triggers:** User accepts, rejects, or edits an EQ plan

### Input

| Field | Type | Required | Description |
| --- | --- | --- | --- |
| planId | EqPlanId | yes | Target plan |
| action | [FeedbackAction](domain.md#feedbackaction) | yes | Outcome action |
| editedBands | [EqBand](domain.md#eqband)[] | no | User changes when action is EDITED |
| rating | number | no | Optional quality score 1-5 |
| comment | string | no | Optional textual feedback |

### Rules

| ID | Rule | Formal |
| --- | --- | --- |
| R1 | Edited bands required when action is EDITED | action = EDITED => len(editedBands) >= 1 |
| R2 | Rating range must be valid | rating is null or (1 <= rating <= 5) |

### Calculations

| ID | Calculation | Formula |
| --- | --- | --- |
| C1 | Revision distance | delta = distance(originalBands, editedBands) |
| C2 | Training label | label = f(action, rating, delta) |

### State Transition

[TranslationRequest](domain.md#translationrequest): PUBLISHED -> PUBLISHED

### Postconditions

- [PlanFeedback](domain.md#planfeedback) is persisted and linked to plan.
- Feedback event is emitted for learning pipeline ingestion.

### Error States

| Condition | Result |
| --- | --- |
| Plan not found | feedback_rejected_not_found |
| Invalid action payload | feedback_rejected_invalid_payload |