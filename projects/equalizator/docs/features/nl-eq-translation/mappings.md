# Mappings: NL to EQ Translation

## PromptToIntentVector

**From:** API Request
**To:** [IntentVector](domain.md#intentvector)
**Direction:** Inbound

### Field Mapping

| Source Field | Target Field | Transform | Notes |
| --- | --- | --- | --- |
| promptText | intent dimensions | descriptor extraction + weighting | Uses controlled vocabulary and alias map |
| promptText modifiers | weight | normalized weighting | Handles terms like slightly, strongly, very |
| listeningContext.deviceProfile | device prior | prior lookup | Optional ranking prior |

### Defaults

| Target Field | Default Value | Condition |
| --- | --- | --- |
| intent dimensions | neutral profile | no descriptors detected |
| weight | 1.0 | no explicit intensity modifiers |

### Validation

| Field | Validation | On Failure |
| --- | --- | --- |
| promptText | length 1..500 | reject request |
| intent dimensions | normalized with tolerance | parser fallback and low confidence |

## IntentAndFeaturesToEqBands

**From:** [IntentVector](domain.md#intentvector) + audio feature snapshot
**To:** [EqBand](domain.md#eqband)[]
**Direction:** Inbound

### Field Mapping

| Source Field | Target Field | Transform | Notes |
| --- | --- | --- | --- |
| intent dimensions | gainDb | optimization under constraints | Weighted objective with safety penalties |
| spectral profile | frequencyHz | feature-guided placement | Avoids redundant overlapping bands |
| masking risk | q | adaptive broad/narrow choice | Higher risk prefers broader correction |
| device prior | band ranking | context-aware reweighting | Applied before final candidate ranking |

### Defaults

| Target Field | Default Value | Condition |
| --- | --- | --- |
| filterType | bell | no specific shelf/high-pass trigger |
| q | 1.0 | no resonance evidence |

### Validation

| Field | Validation | On Failure |
| --- | --- | --- |
| gainDb | within envelope bound | candidate rejected |
| q | within envelope range | candidate rejected |
| band count | <= maxBandCount | candidate rejected |

## FeedbackToTrainingSignal

**From:** [PlanFeedback](domain.md#planfeedback)
**To:** Learning dataset row
**Direction:** Outbound

### Field Mapping

| Source Field | Target Field | Transform | Notes |
| --- | --- | --- | --- |
| action | outcome_label | categorical mapping | accepted/rejected/edited |
| editedBands | revision_distance | distance from original plan | used for quality calibration |
| rating | preference_score | normalized score 0..1 | optional when provided |
| comment | weak supervision text | embedding extraction | optional qualitative signal |

### Defaults

| Target Field | Default Value | Condition |
| --- | --- | --- |
| preference_score | null | no rating provided |
| revision_distance | 0 | action is ACCEPTED and no edits |

### Validation

| Field | Validation | On Failure |
| --- | --- | --- |
| action | in enum set | discard record |
| rating | null or 1..5 | nullify rating and keep event |