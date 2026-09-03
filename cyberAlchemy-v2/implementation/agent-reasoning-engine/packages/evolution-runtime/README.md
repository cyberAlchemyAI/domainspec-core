# ARE Evolution Runtime

This package implements the Agent Reasoning Engine improvement loop as
immutable records stored through the existing append-only Reasoning State
ledger.

It turns measured results into improvement signals and targets, preserves
research and reproduction evidence, identifies content-addressed engine
variants, compares them with an exact baseline, and emits recommend-only
upgrade decisions by default.

The runtime does not expose model chain-of-thought. It stores inspectable
system records and provenance. Research providers are disabled by default, and
benchmark success does not activate or deploy an engine version.

## Runtime surfaces

- `createEvolutionRuntime` appends and seals signals, targets, research results,
  technique candidates, reproduction trials, variants, comparisons, and upgrade
  decisions in the Reasoning State ledger.
- `runResearchScout` calls declared providers only when research is enabled.
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
