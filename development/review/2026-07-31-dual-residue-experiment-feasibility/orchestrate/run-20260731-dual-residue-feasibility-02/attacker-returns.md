# Collected attacker returns

Dispatch: `2026-07-31-dual-residue-experiment-feasibility-review`  
Run: `run-20260731-dual-residue-feasibility-02`  
Target: `/home/vrondelli/projects/dual-residue-experiment` (read-only)

This packet preserves the substantive return from each attack action and its
Robot Talks cross-examination. It is an execution input, not the final review.

## spawn-0001 — formal and claim-contract attack

Initial return:

- **CRITICAL — comparator mismatch.** The E1 machine contract tests condition D
  against the per-axis best of A/B/C, while the title and surrounding narrative
  frame the claim as two separate signals versus one aggregated score, i.e. D
  versus A. The primary D-vs-A question and the separate specialist-dominance
  question must be split.
- **CRITICAL — gradient-independence contradiction.** E1 says `grad_indep` is not
  verdict-bearing, but its PASS route raises veracidade on P-1 `grad_indep`.
  Remove that promotion effect.
- **MAJOR — axiom overreach.** A conditional critical-locus result is presented as
  unconditional categorical nonrecoverability. Condition D is itself a scalar
  weighted sum, so the experiment cannot establish general scalar blindness.
- **MAJOR — unsupported equivalence.** The premise treats gradient linear
  independence as equivalent to independent error movement and as implying strict
  specialist dominance; the available argument does not establish either step.
- **MAJOR — inconsistent verdict algebra.** The constitution says falsified iff D
  fails to strictly beat on both axes and ambiguous otherwise, while E1 defines
  PASS/FLAG/BLOCK differently. The branches are not a single exhaustive contract.
- **MAJOR — top-level proposal drift.** The short proposal repeats the same claim,
  comparator, and promotion ambiguities.
- **MAJOR — direction is not machine-bound.** Gates name p-values, but strict
  negative effect direction is prose rather than an explicit required field and
  predicate.
- **MINOR — truth table hides cases.** It collapses significance and mixed-direction
  outcomes that the evaluator needs to distinguish.

KEEP observations:

- E1 explicitly preserves the shallow-schema ceiling.
- The research notes distinguish gradient cosine, error covariance, and benchmark
  deltas.
- The rich-schema addendum is labeled proposed rather than proven.
- The configuration surface distinguishes the intended objective arms.

Robot Talks reconciliation:

- The mechanics finding that condition A lacks DPO and D lacks weights makes the
  formal comparator mismatch worse: even the nominal arms are not faithful.
- Missing paired bootstrap plus a reporter capable of emitting `VALIDATED` escalates
  the absent statistical gate binding to critical.
- Unconsumed splits and the `eta_ins` denominator issue add construct-validity
  failures.
- Selecting `min(eta_sch, eta_ins)` rewards a single strong axis rather than joint
  superiority.
- Observed gradient-scale imbalance is a treatment-design risk, not evidence for
  `grad_indep`.
- The ownership review is consistent: unresolved authority, missing upstream
  objects, and 8B/0.5B drift prevent promotion.
- Stable boundary: a repaired E1 could test only four faithful, local,
  corpus-specific arms. D-vs-A and D-vs-B/C are different claims. Neither result
  would prove gradient independence, categorical irreducibility, general scalar
  blindness, the rich-schema successor, or upstream promotion. The current bytes
  reliably test none of those propositions.

## spawn-0002 — executable mechanics and measurement attack

Initial return:

- **CRITICAL — condition A is not SFT+DPO.** Configuration names DPO, but the
  training path implements SFT only and contains no DPO trainer.
- **CRITICAL — condition D has no operational weights.** Null weights become zero;
  there is no declared or executed grid search, leaving D operationally equivalent
  to SFT.
- **CRITICAL — verdict can bypass the promised statistics.** Required paired
  bootstrap fields and per-example metric vectors are absent. The evaluator emits
  aggregates only, while the reporter can print `VALIDATED` from point-estimate
  booleans alone.
- **MAJOR — split provenance is not enforced.** The manifest hashes split files, but
  the committed JSONL split files are absent and training regenerates data without
  checking the manifest. Development data is unused.
- **MAJOR — invalid examples distort `eta_ins`.** The README says invalid examples
  are excluded, but evaluation counts them as instruction failures in the total
  denominator.
- **MAJOR — joint selection is implemented as best-axis selection.** D chooses
  `min(eta_sch, eta_ins)`, rewarding one excellent axis rather than joint movement.
- **MAJOR — token/loss alignment is unproved.** JSON prefix character offsets are
  advanced per token and prompt masks are all true; causal alignment is not
  asserted by tests.
- **MAJOR — observed objectives are severely imbalanced.** In the committed probe,
  `L_ins` gradients are zero for two of four samples; the two non-zero norms are
  approximately 725.9 and 431.4 versus `L_sch` norms 1.04 and 0.945. Fixed weights
  cannot be presumed to balance this.
- **MINOR — README evidence inventory is stale.** It says there are no results or
  splits and names 58 tests, although result JSON, a manifest, and 64 test
  definitions exist.

Command receipts:

- Proposal validation passed one frontmatter-oriented check only.
- `pytest` could not run because it is not installed.
- The smoke path could not run because NumPy is absent.
- Torch, Transformers, Datasets, TRL, PEFT, NumPy, Pydantic, and Pytest are absent;
  JSON Schema and YAML libraries are present.
- An ephemeral report invocation exited zero and printed `VALIDATED` with only
  conditions/verdict/scheme-wins/instruction-wins point fields.
- Declared split JSONL files are absent.
- No network, model download, training run, or target write was performed.

Robot Talks reconciliation:

- No mechanics finding was refuted or demoted.
- The formal comparator mismatch strengthens the missing-A-DPO finding.
- E1's own `grad_indep` disclaimer means gradient evidence can be preflight evidence
  only.
- The formal requirement for explicit effect direction strengthens the paired
  bootstrap requirement.
- Ownership drift strengthens the need to freeze one contract and prove code/config
  parity against it.
- `NOT-YET-MECHANICALLY-FEASIBLE` and `CONCEPTUALLY-MIS-SPECIFIED` are distinct,
  cumulative conclusions.
- A retry needs: one canonical frozen contract; faithful A DPO and D grid-search
  arms; verified split hashes; aligned per-example vectors, direction, and paired
  bootstrap gates; fail-closed reporting; tokenizer-aligned scheme loss and a
  stabilized instruction loss; runnable tests; a corrected comparator/headline;
  no automatic `grad_indep` inference; and strictly local promotion semantics.

## spawn-0003 — ownership, lifecycle, and repository-fit attack

Initial return:

- **MAJOR — README evidence-state drift.** Its broad “nothing has run / no results /
  no data splits” statements conflict with committed splits metadata, probe results,
  and a session claiming a first end-to-end probe. A narrower statement that no
  frozen four-arm experiment has run remains supportable.
- **MAJOR — no actually frozen source of truth.** The README calls the top proposal
  frozen, but it has blank source commits and only a summary. The more detailed E1
  contract remains lifecycle `proposed` with a null `frozen_at`.
- **MAJOR — unresolved upstream authority.** Canonical/theorem references point to
  absent `domainspec` and `domainspec-theorem` paths and have no immutable URL or
  commit binding.
- **MAJOR — model/evidence contract drift.** The constitution specifies an 8B target
  and uncommitted results while the active experiment is scoped to 0.5B and has
  committed probes/split metadata.
- **MAJOR — claim identity drift.** README says A/B/C/D tests `grad_indep`; E1 says
  the experiment does not adjudicate it.
- **MINOR — status wording overstates confidence.** The verdict is pending while
  veracidade is high.
- **MINOR — research-ledger completion is procedural only.** Substantive questions
  remain open and its pointer is stale.
- Target repository was clean on `main` at
  `a07d8bcf10f6292d708e063b2ea992ee744cf807` during the attack.
- Contextual-fit conclusion: this is a sensible standalone, candidate evidence
  harness for DomainSpec, but not an authority source.

Robot Talks reconciliation:

- The formal and mechanics findings survive cross-examination.
- The `grad_indep` inconsistency is promotion-blocking claim-identity drift.
- There is no stable executable contract to which code, data, and verdict can be
  compared.
- Overall status is upgraded from “feasible with repairs” to **NOT-YET-FEASIBLE**;
  the architectural placement remains sensible, but the repair gap is too large to
  describe as ordinary cleanup.
- Reconsider after the claim, comparator, and verdict are selected; code and report
  fields faithfully implement them; splits and all arms are demonstrated; and a
  fresh proposal is frozen.
- Current reports, probes, and integrations cannot promote the axiom, `grad_indep`,
  DomainSpec authority, or a theorem claim. A repaired frozen run could establish
  only a local verdict on its pinned model, corpus, implementation, metrics, and
  comparator. A canonical DomainSpec owner must separately accept any candidate
  result; an empirical result cannot alter a theorem's proved object. Rich-schema or
  broad claims require a successor experiment.
