# Queries: NL to EQ Translation

## GetEqPlanByRequest

**Type:** Query (read-only)
**Actor:** Authenticated user or system client

### Input

| Field | Type | Required | Description |
| --- | --- | --- | --- |
| requestId | TranslationRequestId | yes | Translation request identifier |

### Filters

| Field | Type | Default | Description |
| --- | --- | --- | --- |
| includeHistory | boolean | false | Include previous candidate plans |

### Output

| Field | Type | Source | Description |
| --- | --- | --- | --- |
| planId | EqPlanId | [EqPlan](domain.md#eqplan).id | Latest published plan |
| bands | EqBand[] | [EqPlan](domain.md#eqplan).bands | Filter set |
| explanation | string | [EqPlan](domain.md#eqplan).explanation | Human-readable rationale |
| confidence | number | [EqPlan](domain.md#eqplan).confidence | Translation confidence |
| safetyPassed | boolean | [EqPlan](domain.md#eqplan).safetyPassed | Safety status |

### Reads From

| Entity | Relationship | Fields Used |
| --- | --- | --- |
| TranslationRequest | queries | id, status |
| EqPlan | queries | id, requestId, bands, explanation, confidence, safetyPassed |

## SimulateEqPlanImpact

**Type:** Query (read-only)
**Actor:** Authenticated user or system client

### Input

| Field | Type | Required | Description |
| --- | --- | --- | --- |
| sourceAudioRef | string | yes | Target audio reference |
| bands | EqBand[] | yes | Candidate or edited EQ bands |
| listeningContext | [ListeningContext](domain.md#listeningcontext) | no | Optional playback context |

### Filters

| Field | Type | Default | Description |
| --- | --- | --- | --- |
| includeDiagnostics | boolean | true | Include risk diagnostics |

### Output

| Field | Type | Source | Description |
| --- | --- | --- | --- |
| predictedTonalShift | object | computed projection | Low/mid/high expected deltas |
| predictedTruePeakDbtp | number | computed projection | Estimated post-EQ true peak |
| maskingRiskScore | number | computed projection | Relative masking risk estimate |
| warnings | string[] | rule evaluation | Human-readable warnings |

### Reads From

| Entity | Relationship | Fields Used |
| --- | --- | --- |
| EqPlan | queries | bands |
| TranslationRequest | queries | listeningContext |
| AudioFeatureSnapshot (derived) | queries | spectral and dynamic proxy values |