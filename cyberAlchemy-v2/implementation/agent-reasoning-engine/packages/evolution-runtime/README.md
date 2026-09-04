# ARE Evolution Runtime

This package implements the Agent Reasoning Engine improvement loop as
immutable records stored through the existing append-only Reasoning State
ledger.

It turns measured results into improvement signals and targets, preserves
research and reproduction evidence, identifies content-addressed engine
variants, compares them with an exact baseline, and emits recommend-only
upgrade decisions by default.

Completed optimizations can be retained as `are.improvement-retention/v1`
records. A retention binds one candidate identity to exact implementation and
evidence file digests plus its observed comparison. Currentness is recomputed
from every bound file: only a current `implemented-and-verified` record can
suppress rediscovery of that exact candidate. Missing or changed bytes make the
record stale and return the candidate to the experiment frontier.

Its research-learning ontology adds a feedback loop before technique creation:

```text
benchmark anomaly
  -> ResearchHypothesis
  -> HypothesisObservation
  -> ResearchExperiment
  -> LearningDecision
  -> existing TechniqueCandidate and variant comparison path
```

The ontology is machine-readable at `ontology/research-learning-v1.json`. Each
hypothesis is falsifiable and includes its experiment template. Observations
are append-only and preserve supporting, inconclusive, and counterevidence
postures. A deterministic learning decision asks for replication, a controlled
experiment, hypothesis revision, or technique materialization.

The first registered fixture, `ARE-RH-LEXICAL-001`, captures the Luna finding
that an exact-term scorer can reject a structurally adequate answer when the
literal requested token is absent. The detector recognizes only concept
markers declared in the fixture. Marker presence is a research signal, not an
automatic semantic correctness judgment.

The fixture also records each implementation attempt without rewriting the
hypothesis. The v2 and v3 declared-equivalence scorers are preserved as
separate candidate identities: both retained the v1 quality and safety results
but failed the registered latency ceiling. Their exact report references,
digests, measurements, and next actions remain in
`fixtures/luna-lexical-scoring-hypothesis.json` for the next reversible attempt.
The scorer loop now creates a sealed successor hypothesis after each failed
attempt, binds the next attempt to that successor, and stops creating successors
when a PASS is reached or the attempt bound is exhausted.
The strategy-loop variant rotates through a declared catalog of implementation
patterns and stores the exact function reference on each hypothesis, making
code-pattern learning inspectable rather than only metric-based.
The gain-gated strategy loop adds a measurable-progress trigger: the first
attempt establishes the best value, later attempts must improve the selected
metric while all protected quality and safety checks remain true, and the loop
stops at the configured no-gain bound. Missing metrics and lost protected
checks fail closed. This prevents the improvement loop from spending attempts
without evidence of progress; it remains recommend-only benchmark evidence.
The portfolio runner complements that exploit loop by declaring several
strategy-bound hypotheses up front, screening every branch, allocating full
repetitions only to the best survivors, and preserving every branch outcome.
Full and confirmation stages use independent replications and retain aggregate
median/minimum/maximum evidence. It can optionally evaluate the selected branch
on a disjoint confirmation holdout; otherwise its winner remains explicitly
provisional. A branch that does not improve over its screening aggregate is
rejected before confirmation.

The runtime does not expose model chain-of-thought. It stores inspectable
system records and provenance. Research providers are disabled by default, and
benchmark success does not activate or deploy an engine version.

## Runtime surfaces

- `createEvolutionRuntime` appends and seals signals, targets, research results,
  retained improvements, technique candidates, reproduction trials, variants,
  comparisons, and upgrade decisions in the Reasoning State ledger.
- `createImprovementRetention` and
  `assessImprovementRetentionCurrentness` preserve a verified optimization and
  compare every selected implementation and evidence dependency before reuse.
- `runResearchScout` calls declared providers only when research is enabled.
- `diagnoseLexicalScoringAnomaly` converts an exact scored case plus declared
  concept markers into a bounded hypothesis observation.
- `runHypothesisLearningCycle` registers the hypothesis and observations,
  creates its reproducible experiment, makes the next learning decision, and
  seals the append-only reasoning epoch.
- `createVariantWorkspaceFactory` creates one content-addressed detached Git
  worktree outside the serving repository, enforces one writer, and blocks any
  changed path outside the target mutation allowlist.
- `createEvolutionScheduler` runs one cycle at a time and replays duplicate
  trigger identities without a second cycle call.
- `createServingVersionStore` writes a hash-bound serving pointer atomically.
- `applyUpgradeDecision` leaves recommend-only decisions untouched; controlled
  local activation requires an exact predecessor and an injected canary, and a
  failed canary restores the predecessor.

The package supplies mechanisms, not a background daemon. A caller chooses the
research providers, reproduction runner, variant change, benchmark manifest,
canary, cadence, and whether controlled local activation is enabled.

Run tests with Linux Node v26.8.1:

```sh
/home/vrondelli/.nvm/versions/node/v26.8.1/bin/node --test test/*.test.mjs
```

Run the first deterministic learning canary:

```sh
npm run hypothesis-canary
```
