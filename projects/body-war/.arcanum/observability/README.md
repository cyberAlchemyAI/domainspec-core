# Arcanum Observability

This repository-local package stores Arcanum command, sigil, and spell telemetry plus reflection state.

- signals/sigil-invocations.jsonl is the central append-only invocation ledger.
- by-sigil/ and by-capability/ hold rebuildable ledger-reference indexes.
- hooks/ stores hook operation evidence.
- runs/ stores pending and completed observer envelopes.
- reflections/ can hold reflection reports.
