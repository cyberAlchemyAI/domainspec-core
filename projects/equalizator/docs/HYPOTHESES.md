# Hypotheses

## Hypothesis Register

| ID | Proposition | Expected Effect | Confidence | Status |
|---|---|---|---|---|
| H1 | Hybrid intent parsing plus constrained optimization outperforms direct text-to-filter generation | Higher first-pass acceptance and lower safety failures | medium | proposed |
| H2 | Device-aware ranking improves perceived tonal match over device-agnostic ranking | Higher tonal match score across playback contexts | medium | proposed |
| H3 | Explainable recommendations reduce revision loops | Lower median revision steps and faster acceptance | medium | proposed |
| H4 | A controlled descriptor vocabulary improves consistency without harming expressiveness | Higher parser confidence and lower ambiguity rate | low | proposed |

## Hypothesis Details

### H1 - Hybrid Translator Superiority

- Proposition: If intent interpretation and EQ synthesis are separated and connected by constrained optimization, recommendation quality and safety both improve versus direct generation.
- Decision owner: product owner and model lead
- Primary signal: first_pass_acceptance_rate
- Expected direction: improve
- Current evidence: observed domain research and engineering priors
- Evidence type: hypothesized
- Why this might be true: decomposition reduces failure coupling and enforces guardrails early.
- Strongest counterargument: modern end-to-end models may implicitly learn constraints if enough data exists.
- Confounders: evaluation prompt set bias, user skill variance, and source audio diversity.
- Disconfirming outcome: no improvement in acceptance or safety compared to baseline direct generation.
- Scope notes: likely strongest for mixed-skill users and constrained operational profiles.

### H2 - Device-Aware Ranking Value

- Proposition: Using listening context (headphones, phone speaker, car, studio monitors) when ranking EQ candidates improves perceived match quality.
- Decision owner: product owner
- Primary signal: tonal_match_score per device segment
- Expected direction: improve
- Current evidence: stated need from cross-source playback variability
- Evidence type: hypothesized
- Why this might be true: psychoacoustic and playback response differences affect perceived tonal balance.
- Strongest counterargument: a robust generic plan may already perform sufficiently in most contexts.
- Confounders: poor device metadata quality, subjective rating variability.
- Disconfirming outcome: no meaningful score difference between context-aware and generic ranking.
- Scope notes: more relevant for consumer playback optimization than studio-only scenarios.

### H3 - Explainability Effect

- Proposition: Recommendations that include concise rationale (what changed and why) lead to higher user trust and fewer correction steps.
- Decision owner: product and UX leads
- Primary signal: median_revision_steps
- Expected direction: reduce
- Current evidence: no direct baseline yet
- Evidence type: hypothesized
- Why this might be true: explanation helps users diagnose mismatch quickly and calibrate expectations.
- Strongest counterargument: experts may ignore explanations and adjust by ear immediately.
- Confounders: explanation quality and user expertise level.
- Disconfirming outcome: revisions unchanged or increased when explanations are present.
- Scope notes: expected highest impact for novice and intermediate users.

### H4 - Controlled Vocabulary Benefit

- Proposition: Restricting descriptor mapping to a curated vocabulary with aliases increases parser consistency and model robustness.
- Decision owner: model lead
- Primary signal: parser_confidence_mean and ambiguity_rate
- Expected direction: improve confidence, reduce ambiguity
- Current evidence: language ambiguity risk identified in discovery
- Evidence type: hypothesized
- Why this might be true: fewer semantic collisions in prompt interpretation.
- Strongest counterargument: constrained language may frustrate users and reduce expressiveness.
- Confounders: alias coverage quality and prompt coaching UX.
- Disconfirming outcome: increased fallback rate or degraded user satisfaction.
- Scope notes: should include free-form fallback path to avoid hard failures.

## Prioritization

| Hypothesis ID | Value If True | Cost To Test | Risk If Wrong | Priority |
|---|---|---|---|---|
| H1 | high | medium | high | now |
| H2 | medium | medium | medium | now |
| H3 | medium | low | low | now |
| H4 | medium | low | medium | later |