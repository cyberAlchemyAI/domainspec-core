# Initial Definitions

## Glossary Seed

| Term | Working Definition | Category | Status | Evidence Type |
|---|---|---|---|---|
| Intent prompt | Free text description of desired tonal outcome | workflow | draft | observed |
| Descriptor token | Normalized tonal term extracted from prompt (for example muddy, harsh, warm) | system | draft | observed |
| Intent vector | Weighted representation of target tonal attributes | metric | draft | hypothesized |
| EQ plan | Structured set of parametric filters with rationale and confidence | system | draft | observed |
| Safety envelope | Hard limits on gain, Q, and predicted peak behavior | policy | draft | observed |
| Listening context | Device and environment where audio is expected to be consumed | role | draft | stated |
| Translation confidence | Confidence score for mapping prompt to plan | metric | draft | hypothesized |
| Tonal match score | Human or model rating of how well output matches intended sound | metric | draft | hypothesized |

## Bounded Context Definitions

| Context | Responsibility | In Scope | Out Of Scope | Status |
|---|---|---|---|---|
| Intent Interpretation | Convert language to normalized intent | lexical parsing, confidence, ambiguity detection | direct DSP filter synthesis | candidate |
| Program Material Analysis | Compute source audio descriptors | spectral bands, dynamics proxies, masking risks | mastering chain decisions | candidate |
| EQ Synthesis | Produce candidate filter sets | constrained optimization, ranking, rationale | final limiter/compressor changes | candidate |
| Safety And Compliance | Enforce hard operational limits | gain/Q bounds, true peak guard, policy checks | artistic preference ranking | candidate |
| Feedback Learning | Update mappings from usage outcomes | acceptance data, revision deltas, retraining signals | real-time low-latency inference path | candidate |

## Core Concepts

| Concept | Suggested Meta-Type | Context | Description | Status |
|---|---|---|---|---|
| TranslationRequest | Entity | Intent Interpretation | A request containing prompt, constraints, and context metadata | draft |
| IntentVector | Value Object | Intent Interpretation | Weighted tonal goals inferred from prompt and modifiers | draft |
| AudioFeatureSnapshot | Value Object | Program Material Analysis | Compact measurable features extracted from source audio | draft |
| EqBand | Value Object | EQ Synthesis | One filter instruction with frequency, gain, Q, and filter type | draft |
| EqPlan | Entity | EQ Synthesis | Candidate or published set of EqBand entries with score and rationale | draft |
| SafetyPolicy | Policy | Safety And Compliance | Set of guards that must pass before publishing a plan | draft |
| TranslationWorkflow | Workflow | Cross-context | Orchestration from prompt to published plan | draft |
| FeedbackCaptured | Event | Feedback Learning | Signal emitted when user accepts, rejects, or edits a plan | draft |

## Rules And Policies

| Name | Type | Description | Source | Status |
|---|---|---|---|---|
| MaxBandGainRule | rule | Per-band gain must remain within safe range (default +/-9 dB) | inferred | draft |
| QRangeRule | rule | Q must stay inside stable recommendation range (default 0.3 to 8.0) | inferred | draft |
| MaxBandCountPolicy | policy | Total band count is limited by profile to preserve usability | inferred | draft |
| TruePeakRiskGuard | invariant | Predicted processing should not increase true peak risk above threshold | inferred | draft |
| DeviceAwarePolicy | policy | Candidate ranking should weight expected playback device behavior | stated | draft |
| ExplanationRequiredPolicy | policy | Every published plan must include plain-language rationale | stated | draft |

## External Interfaces

| Interface | Purpose | Owner | Dependency Type | Status |
|---|---|---|---|---|
| POST /api/v1/eq/translate | Create recommendation from prompt and optional audio context | equalizator backend | user-facing | candidate |
| POST /api/v1/eq/validate | Validate externally edited EQ plans against safety envelope | equalizator backend | user-facing | candidate |
| POST /api/v1/eq/feedback | Capture accept/reject/edit outcomes | equalizator backend | user-facing | candidate |
| Audio feature extractor module | Produce source descriptors for synthesis | internal DSP component | internal | candidate |

## Metrics And Definitions

| Metric | Definition | Decision It Supports | Status |
|---|---|---|---|
| first_pass_acceptance_rate | accepted_without_edit / total_recommendations | Is mapping useful on first attempt? | draft |
| median_revision_steps | median number of user edits before acceptance | Is output close to intent? | draft |
| safety_fail_rate | failed_policy_checks / generated_candidates | Are generation constraints correct? | draft |
| tonal_match_score | average subjective rating per recommendation | Is user-perceived quality improving? | draft |

## Ambiguities To Resolve

| Topic | Why Ambiguous | Resolution Needed |
|---|---|---|
| Descriptor ontology granularity | Too few tokens underfit intent; too many reduce reliability | Define v1 controlled vocabulary with max token count |
| Objective weighting strategy | Competing goals between tonal target, safety, and simplicity | Select optimization objective per use case profile |
| Required source analysis depth | Deep analysis improves precision but increases latency | Decide v1 feature set and latency budget |
| Feedback trust model | Not all user edits represent better output | Define confidence-weighted feedback ingestion policy |