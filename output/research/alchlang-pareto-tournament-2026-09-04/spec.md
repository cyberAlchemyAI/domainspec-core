# AlchLang Pareto Tournament benchmark candidate

Status: research prototype

## Question

Can competing AlchLang documentation layouts be compared without reducing
accessibility, task performance, meaning coverage, density, and preference to
one weighted score?

## Tournament contract

1. Build every variant from the same content and production-build procedure.
2. Run the existing frontend hard gates first. A variant with a failed
   interaction, accessibility violation, overflow, runtime error, or exceeded
   bundle budget is ineligible; a fast broken page cannot win.
3. Exercise the same task cards on every eligible variant:
   - identify what AlchLang models;
   - find the canonical syntax for one backend type;
   - construct and validate a small `.alch` file;
   - explain the boundary between SFOL, contracts, bindings, and evidence.
4. Retain separate objective values. Do not sum them:
   - task completion time, minimize;
   - comprehension accuracy, maximize;
   - required meaning coverage, maximize;
   - mobile viewport pages, minimize;
   - pairwise preference probability, maximize.
5. Apply epsilon dominance. Candidate A dominates B only when A is no worse
   than B outside each objective's practical-equivalence margin and is
   meaningfully better on at least one objective.
6. Rank by Pareto layers. Layer 1 is the non-dominated frontier; removing it
   reveals layer 2, and so on.
7. Run pairwise human matches only among frontier candidates. Randomize left
   and right order, allow a tie, show one task context at a time, and record
   rationale. Fit preference independently for each declared question; never
   merge distinct questions into a universal UX score.
8. Stop when every frontier pair has enough observations for the chosen
   uncertainty bound, the comparison budget is exhausted, or the owner decides
   that the remaining trade-off needs a product choice.

## Practical-equivalence margins for the first calibration

These are hypotheses for fixture calibration, not accepted product thresholds:

| Objective | Direction | Epsilon |
| --- | --- | ---: |
| Median task time | minimize | 2 seconds |
| Comprehension accuracy | maximize | 0.03 |
| Required meaning coverage | maximize | 0.02 |
| Mobile viewport pages | minimize | 1 viewport |
| Pairwise preference probability | maximize | 0.05 |

## Candidate family for the first real experiment

- `baseline`: current candidate, unchanged.
- `compact-spacing`: typography and vertical rhythm only; content order stays
  unchanged.
- `progressive-reference`: tutorial remains linear while detailed reference
  tables and long examples move behind explicit disclosure or subroutes.
- `task-first`: starts with the mini workspace, revealing explanation beside
  the construction task.

Only one treatment family should change per variant. Otherwise a tournament
result cannot identify which intervention caused an outcome.

## Evidence and authority

Automated browser observations can gate deterministic failures and provide
density proxies. Comprehension and preference require people performing the
declared tasks. A Pareto frontier is a decision surface, not product approval.
The current candidate, owner judgment, and future variants remain separate
immutable digests.

## Failure modes to test

- Many objectives can make nearly every candidate non-dominated. Keep the
  vector small and task-linked.
- Pairwise preference can be cyclic or inconsistent. Preserve ties, order,
  participant, and uncertainty instead of manufacturing a total order.
- Shorter is not automatically better. Required meaning coverage protects
  dense expert documentation from a false-positive simplicity rule.
- Missing human evidence is `not_evaluable`, never zero.
- A dominated candidate may still be retained as a known-bad fixture, but it
  must not advance to product approval.

