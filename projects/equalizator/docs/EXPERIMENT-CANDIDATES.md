# Experiment Candidates

## Candidate Register

| ID | Hypothesis | Intervention | Primary Signal | Cost | Priority |
|---|---|---|---|---|---|
| EX-1 | H1 | Compare hybrid pipeline versus direct generation baseline | first_pass_acceptance_rate | medium | now |
| EX-2 | H2 | Enable device-aware ranking branch in candidate scorer | tonal_match_score by device | medium | now |
| EX-3 | H3 | A/B explainable output versus no rationale | median_revision_steps | low | now |
| EX-4 | H4 | Introduce controlled vocabulary with alias expansion | ambiguity_rate | low | later |

## Candidate Details

### EX-1 - Hybrid vs Direct Mapping

- Linked hypothesis: H1
- Decision owner: product owner and model lead
- Business question: Should v1 architecture enforce modular translation and constraints?
- Intervention: route 50 percent of traffic to hybrid parser plus constrained optimizer, 50 percent to direct baseline.
- Target segment or scope: internal pilot users across mixed skill levels.
- Duration or observation window: 2 weeks or 300 qualified sessions.
- Primary signal: first_pass_acceptance_rate.
- Secondary signals: safety_fail_rate, median_revision_steps.
- Expected effect: hybrid improves acceptance while maintaining lower safety failures.
- Disconfirming outcome: no gain in acceptance or worsening safety profile.
- Risks: training data leakage between branches, inconsistent prompt distribution.
- Preconditions: stable baseline implementation and branch routing.
- Minimum instrumentation needed: request branch tag, acceptance outcome, safety result, revision count.
- Recommended next step: run now.

### EX-2 - Device-Aware Ranking

- Linked hypothesis: H2
- Decision owner: product owner
- Business question: Is playback context necessary in v1 recommendations?
- Intervention: rank candidates with device-specific priors for test group only.
- Target segment or scope: users with explicit device metadata.
- Duration or observation window: 2 weeks.
- Primary signal: tonal_match_score by device segment.
- Secondary signals: first_pass_acceptance_rate.
- Expected effect: significant uplift in tonal match score for mobile and headphones segments.
- Disconfirming outcome: no segment uplift or higher safety violations.
- Risks: unreliable device tagging and sample imbalance.
- Preconditions: device metadata capture in request path.
- Minimum instrumentation needed: device type, chosen candidate, rating, acceptance.
- Recommended next step: run now after EX-1 starts.

### EX-3 - Explainability A/B

- Linked hypothesis: H3
- Decision owner: UX and product leads
- Business question: Should explanations be mandatory in output contracts?
- Intervention: show concise rationale in test branch, hide rationale in control.
- Target segment or scope: novice and intermediate users.
- Duration or observation window: 10 days.
- Primary signal: median_revision_steps.
- Secondary signals: completion_time_to_acceptance, trust_rating.
- Expected effect: fewer revisions and faster acceptance.
- Disconfirming outcome: no reduction in revisions or slower completion time.
- Risks: poor explanation text quality can distort results.
- Preconditions: reliable explanation generator.
- Minimum instrumentation needed: revision count, completion time, user trust rating.
- Recommended next step: run now.

### EX-4 - Controlled Vocabulary Pilot

- Linked hypothesis: H4
- Decision owner: model lead
- Business question: Is a constrained descriptor ontology worth adopting in v1?
- Intervention: prompt parser first maps to curated token set with alias table.
- Target segment or scope: all text prompts except explicit expert mode.
- Duration or observation window: 2 weeks.
- Primary signal: ambiguity_rate.
- Secondary signals: parser_confidence_mean, fallback_to_manual_rate.
- Expected effect: lower ambiguity and higher confidence with stable satisfaction.
- Disconfirming outcome: increased fallback or user frustration.
- Risks: ontology misses important descriptors.
- Preconditions: descriptor dictionary and fallback strategy.
- Minimum instrumentation needed: raw prompt, resolved tokens, confidence, fallback events.
- Recommended next step: refine vocabulary, then run.

## Sequencing Notes

1. Start EX-1 and EX-3 first because they are highest differentiators and low coupling.
2. Run EX-2 in parallel only after device metadata quality check passes.
3. Stage EX-4 after establishing baseline parser instrumentation.