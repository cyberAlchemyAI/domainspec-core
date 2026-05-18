# Arcanum Observability

This repository-local package stores Arcanum runtime command, sigil, and spell telemetry plus reflection state.

- signals/sigil-invocations.jsonl is the central append-only invocation ledger.
- by-sigil/ can hold optional per-artifact ledgers.
- hooks/ tracks background hook operations, failures, dedupe, and hook-health reflections.
- runs/ stores observed run bundles and checkpoints for long-running work.
- reflections/ can hold future reflection reports.
