# User Stories: NL to EQ Translation

## Story 1 - Prompt To Plan

As a creator, I want to describe the tonal problem in plain language so that I get an EQ recommendation without manually tuning frequencies.

### Acceptance Criteria

- Given a valid tonal prompt, when I call translate, then I receive a plan with bands, explanation, and confidence.
- Given an ambiguous prompt, when confidence is low, then I receive a clear low-confidence response and next-step guidance.

## Story 2 - Safety First

As a product owner, I want every recommendation to pass safety rules so that users never receive unstable or risky EQ settings.

### Acceptance Criteria

- Given candidate plans, when validation runs, then any plan violating gain, Q, or peak rules is rejected.
- Given no safe candidate, when publication is attempted, then response indicates safety failure and does not publish.

## Story 3 - Learning Loop

As a model lead, I want user outcomes captured as structured feedback so that future recommendations improve.

### Acceptance Criteria

- Given an accepted or edited plan, when feedback is submitted, then feedback event is persisted and emitted.
- Given edited bands, when feedback is processed, then revision distance is computed for training usage.