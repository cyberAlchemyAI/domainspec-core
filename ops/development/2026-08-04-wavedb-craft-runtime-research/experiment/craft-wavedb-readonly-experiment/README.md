# Craft–WaveDB Read-Only Experiment

This private, checkout-local package tests read-only access to the accepted
Craft WaveDB snapshot. It reads only isolated filesystem copies beneath
`.work/`; the accepted original store and the 28 canonical Craft ledgers are
identity-checked before and after each execution node.

## Fixed runtime

- Node: `/home/vrondelli/.nvm/versions/node/v26.6.0/bin/node` (`v26.6.0`)
- WaveDB: accepted local `@vijayee/wavedb@0.15.9` package bytes
- Snapshot: accepted `wcli-20260805-node26-0.15.9-03` receipt and store digest
- Public adapter exports: `status`, `verify`, `listLedgers`, and `getRaw`

No package download, source build, network access, server, writer, iterator,
`Subtree`, publication, deployment, or canonical-store replacement belongs to
this experiment.

## Validation

From the repository root, use the pinned Node executable:

```sh
/home/vrondelli/.nvm/versions/node/v26.6.0/bin/node --test \
  ops/development/2026-08-04-wavedb-craft-runtime-research/experiment/craft-wavedb-readonly-experiment/test/reader.test.cjs \
  ops/development/2026-08-04-wavedb-craft-runtime-research/experiment/craft-wavedb-readonly-experiment/test/adapter.test.cjs \
  ops/development/2026-08-04-wavedb-craft-runtime-research/experiment/craft-wavedb-readonly-experiment/test/failure.test.cjs
/home/vrondelli/.nvm/versions/node/v26.6.0/bin/node \
  ops/development/2026-08-04-wavedb-craft-runtime-research/experiment/craft-wavedb-readonly-experiment/scripts/validate-receipts.cjs
```

The one-shot `run-cwe-003.cjs` command is governed by its Task Session because
it exclusively creates `.work/CWE-003`, the CWE-003 node receipt, and the
experiment terminal receipt.

## Evidence and claim ceiling

Node receipts are under `execution/CWE-*/receipt.json`; Task Session terminals
are under `execution/CWE-*/task-session-terminal.json`; the experiment terminal
is `execution/terminal-receipt.json`.

Maximum claim: A repeatable checkout-local, read-only experiment independently
accessed the accepted derived Craft snapshot without changing canonical source
or accepted store bytes.

This evidence does not select or prove an API successor, product integration,
promotion, publication, deployment, production readiness, concurrency on a
shared store, recovery, scale, or durability.
