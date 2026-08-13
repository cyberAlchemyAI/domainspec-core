# Craft–WaveDB Read-Only Experiment Goal

Lifecycle note: this directory began as a proposal-only snapshot. The bounded
experiment was later admitted and completed through `WP-CWE-20260806`. See
`GOAL-CLOSEOUT.md` for the authoritative execution result; the original profile,
context pack, and context index remain preserved as pre-admission evidence.

This directory is a proposal-only native Codex Goal package for one finite,
repository-local experiment. It does not authorize or execute the experiment.

The proposed one-shot stream proves independent, read-only access to the
accepted WaveDB `0.15.9` snapshot, adds a minimal experiment-local CLI, runs
failure controls only against disposable copies, and closes with one terminal
receipt. It does not construct the Craft API.

## Package files

- `CODEX-GOAL-PROFILE.md` — compact native `/goal` command and readiness result.
- `CONTEXT-PACK.md` — full evidence, graph, boundaries, acceptance contract,
  and claim ceiling.
- `context-index.json` — machine-readable source coverage and admission state.

## Proposal snapshot state

At proposal time, coverage was complete but runtime readiness was blocked. The
then-current source Work Pack had `allowedRoutes: []`, the proposed one-shot
stream was not admitted, and its experiment-local write root and validation
commands were not yet owned by an applied Invoke Refresh.

That historical Goal was not runnable until a reviewed Work Pack refresh:

1. selects `CRAFT-WAVEDB-READONLY-EXPERIMENT-001` as one ordered stream;
2. admits the exact capability route and experiment-local write root;
3. materializes exact validation commands and Task Session bindings; and
4. receives separate operator authorization to execute the Goal.

Those conditions were later satisfied by the separate executed Work Pack named
in `GOAL-CLOSEOUT.md`. The completed result remains only a repeatable local
experiment receipt. It is not an API, portable package, npm publication, Docker
image, deployment, or production-readiness claim.
