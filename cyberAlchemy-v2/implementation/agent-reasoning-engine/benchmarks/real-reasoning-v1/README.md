# ARE Real Reasoning Benchmark v1

This candidate harness measures observable reasoning-engine behavior across routing, request-aware context retrieval, context-view lifecycle, fail-closed boundaries, exact-prefix cache reuse, and optional real Codex conversations. Cache comparisons accept only provider-reported usage bound to the same projection and prefix; absent fields remain unobserved. It does not attempt to inspect hidden chain-of-thought and grants no authority.

## Run

Use the repository's Node 26.8.1 runtime:

```sh
cd /home/vrondelli/projects/domainspec-core/cyberAlchemy-v2/implementation/agent-reasoning-engine/benchmarks/real-reasoning-v1
/home/vrondelli/.nvm/versions/node/v26.8.1/bin/node bin/benchmark.mjs --mode core
/home/vrondelli/.nvm/versions/node/v26.8.1/bin/node bin/benchmark.mjs --mode integration
```

`all` runs core and integration. Real Codex comparison is deliberately opt-in:

```sh
PATH=/home/vrondelli/.nvm/versions/node/v26.8.1/bin:$PATH \
  /home/vrondelli/.nvm/versions/node/v26.8.1/bin/node bin/benchmark.mjs \
  --mode live --repetitions 3
```

The multi-turn extension keeps one ephemeral Codex thread alive for each
Define, Research, Ontology, or Plan conversation and scores all three turns:

```sh
PATH=/home/vrondelli/.nvm/versions/node/v26.8.1/bin:$PATH \
  /home/vrondelli/.nvm/versions/node/v26.8.1/bin/node bin/benchmark.mjs \
  --mode live-multiturn --repetitions 1
```

One repetition performs 24 real turns: 12 ARE and 12 paired controls. Increase
repetitions explicitly for stability evidence; model calls remain opt-in.

To reuse an already-running persistent gateway, add `--gateway-socket /path/to/are-gateway.sock`. The gateway must authorize `codex:benchmark` on the interaction-bound lane and must have been restarted after the profile change.

Results are written under `runs/` unless `--stdout-only` is supplied. Timing is local evidence, not a universal performance guarantee. A live `NOT_EVALUATED` result means the installed Codex version did not match the exact protocol binding; the gate is not relaxed.

## Modes

- `core`: 20 route cases, 10 context-retrieval cases, deterministic replay, and warm latency.
- `integration`: five multi-turn lifecycle traces plus six fail-closed cases.
- `live`: paired ARE/control ephemeral app-server turns, alternating execution order.
- `live-multiturn`: four paired three-turn conversations with thread continuity, per-turn grounding, Context Item citation, question-policy, and authority-safety checks.
- `external-retrieval`: exact-bound Agent Retrieval Bench JSONL plus ARE prediction JSONL, scored for MRR, Recall/Precision/F0.5@20, BCY@8k, and selective abstention.
- `external-retrieval-run`: produce deterministic ARE hybrid-lexical predictions from exact corpus snapshots, then score them through the same adapter.
- `all`: core plus integration; `--include-live` adds the live comparison.

## External retrieval lane

The first external adapter targets [Agent Retrieval Bench](https://github.com/eyuansu62/agent-retrieval-bench) without vendoring its corpus. Download and validate an upstream release separately, produce one prediction per sample, and run:

```sh
node bin/benchmark.mjs \
  --mode external-retrieval \
  --dataset /path/to/arb/samples.jsonl \
  --predictions /path/to/are-predictions.jsonl \
  --dataset-id v2-positive-or-selective-release \
  --dataset-revision <exact-upstream-revision> \
  --stdout-only
```

Prediction records conform to `schemas/external-retrieval-input.schema.json`. Each ranked file must carry observed `header_tokens` and `content_tokens`; the adapter never estimates missing token counts. Dataset and prediction bytes are SHA-256 bound in the result, repository/base-commit mismatches block, duplicate or unexpected predictions block, and missing predictions remain visible failures.

Run the included structural canary with:

```sh
npm run benchmark:external-retrieval:fixture
npm run benchmark:external-retrieval:produce-fixture
```

Run the producer against a downloaded release whose corpus directory contains
`corpus_manifest.jsonl`:

```sh
node bin/benchmark.mjs \
  --mode external-retrieval-run \
  --dataset /path/to/arb/samples.jsonl \
  --corpus-dir /path/to/arb/corpus-release \
  --dataset-id v2-selective-release \
  --dataset-revision <exact-upstream-revision> \
  --predictions-output /path/to/are-predictions.jsonl
```

The producer uses request fields and the exact base-commit corpus only; gold
labels are forbidden inputs to ranking and abstention. It combines BM25 content
matching, path/anchor proximity, task-aware source/test priors, deterministic
tie-breaking, and a configurable evidence threshold. Corpus paths may not
escape the supplied corpus directory. The production receipt binds the dataset,
manifest, selected snapshots, predictions, and ARB canonical
`regex_code_tokenizer_v1`.

The positive quality targets reproduce the best published upstream reference value for each ARB metric, even though those values come from different retrievers. The selective-success target is explicitly an ARE candidate target rather than an upstream leaderboard claim. A PASS is local benchmark evidence only and does not demonstrate end-to-end repair success or grant authority.

### Benchmark attack order

The external program advances in impact order:

1. **Agent Retrieval Bench:** file ranking, hard token-budget coverage, and the retrieve-versus-abstain decision. The scorer is implemented.
2. **ARE prediction producer:** connect request selection to exact repository snapshots and emit the prediction schema above. The deterministic hybrid-lexical baseline is implemented; its real quality is not known until the downloaded 427-row release is run.
3. **ContextBench:** test whether retrieved context improves downstream task completion, after retrieval quality is measurable.
4. **MemoryAgentBench:** test longer-lived state selection only after per-request retrieval and abstention are stable.

This order attacks the current precision failure directly. It avoids using an end-task score to hide whether the wrong context was retrieved, and avoids adding durable-memory complexity before selective retrieval is reliable.

## Improvement loop

Start with a fast diagnosis and create one bounded iteration:

```sh
node bin/improve.mjs --mode diagnose --fast
node bin/improve.mjs --mode iterate --baseline runs/improvements/<diagnose-report>.json
```

The iteration report selects one target, records the exact baseline, snapshots every allowlisted implementation file, and prints the verification command. It never edits or reverts source files. After making the bounded change, verify it against that report:

```sh
node bin/improve.mjs --mode verify-candidate \
  --target context-overflow \
  --baseline runs/improvements/<iterate-report>.json
```

Fast baselines compare correctness and safety while recording, but not enforcing, noisy short-sample latency. Use a full diagnosis before final candidate verification. After one candidate returns `KEEP`, require a reproducible streak:

```sh
node bin/improve.mjs --mode loop \
  --target context-overflow \
  --baseline runs/improvements/<iterate-report>.json \
  --max-attempts 5
```

The loop returns `STABLE` only after two consecutive `KEEP` assessments. Any safety, lifecycle, non-target quality, or full-run latency regression rejects the candidate. A stable deterministic candidate advances to the explicitly invoked live holdout; it does not invoke model turns automatically.

## Evolution cycle

The evolution runtime converts benchmark failures into immutable improvement
signals, selects one target, exact-binds research results, records reproduction,
builds a content-addressed variant record, compares it against protected quality,
latency, safety, determinism, and holdout constraints, and emits a recommend-only
upgrade decision by default.

Run the deterministic, no-model fixture canary with:

```sh
/home/vrondelli/.nvm/versions/node/v26.8.1/bin/node bin/evolution-canary.mjs
```

The canary exercises the complete lifecycle but does not mutate the source tree,
activate a candidate, publish, or deploy. Real reproduction, worktree mutation,
and activation require separately configured runners.
