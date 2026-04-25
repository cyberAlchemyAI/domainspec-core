# Events: NL to EQ Translation

## TranslationRequested

**Produced by:** [TranslatePromptToEqPlan](operations.md#translateprompttoeqplan)
**Triggers transition:** [RECEIVED to PARSED](states.md#translationrequeststate)

### Payload

| Field | Type | Description |
| --- | --- | --- |
| requestId | TranslationRequestId | Correlation id |
| promptText | string | Original prompt |
| listeningContext | object | Optional playback context |
| createdAt | datetime | Event timestamp |

### Consumed by

| Consumer | Action |
| --- | --- |
| Recommendation engine | Start parse and candidate generation path |
| Observability pipeline | Increment request metrics |

## EqPlanPublished

**Produced by:** [TranslatePromptToEqPlan](operations.md#translateprompttoeqplan)
**Triggers transition:** [VALIDATED to PUBLISHED](states.md#translationrequeststate)

### Payload

| Field | Type | Description |
| --- | --- | --- |
| requestId | TranslationRequestId | Parent request id |
| planId | EqPlanId | Published plan id |
| confidence | number | Translation confidence |
| objectiveScore | number | Quality and safety composite |
| safetyPassed | boolean | Validation status |
| publishedAt | datetime | Event timestamp |

### Consumed by

| Consumer | Action |
| --- | --- |
| UI notification service | Return recommendation summary |
| Analytics pipeline | Record plan quality metrics |

## FeedbackCaptured

**Produced by:** [CapturePlanFeedback](operations.md#captureplanfeedback)
**Triggers transition:** [PUBLISHED to PUBLISHED](states.md#translationrequeststate)

### Payload

| Field | Type | Description |
| --- | --- | --- |
| feedbackId | PlanFeedbackId | Feedback identifier |
| planId | EqPlanId | Related plan |
| action | FeedbackAction | accept, reject, edit |
| rating | number | Optional rating |
| revisionDistance | number | Difference from original plan |
| capturedAt | datetime | Event timestamp |

### Consumed by

| Consumer | Action |
| --- | --- |
| Learning pipeline | Create training example |
| Product analytics | Track acceptance and revision loops |