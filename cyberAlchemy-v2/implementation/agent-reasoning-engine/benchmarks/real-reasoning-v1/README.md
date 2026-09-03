# ARE Real Reasoning Benchmark v1

This candidate harness measures observable reasoning-engine behavior across routing, request-aware context retrieval, context-view lifecycle, fail-closed boundaries, and optional real Codex conversations. It does not attempt to inspect hidden chain-of-thought and grants no authority.

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
- `all`: core plus integration; `--include-live` adds the live comparison.

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
