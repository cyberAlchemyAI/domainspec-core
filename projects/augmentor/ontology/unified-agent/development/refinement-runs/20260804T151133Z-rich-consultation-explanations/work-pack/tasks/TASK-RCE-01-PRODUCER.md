# TASK-RCE-01: Neutral Bundle Producer

## SWU-RCE-002

Convert all 22 beginner explanations to the structured example/analogy shape and add glossary refs plus reviewed keywords.

- Preserve friendly name, plain meaning, state, process, and boundary intent.
- Add non-empty analogy limitations for every emitted analogy.
- Mark every example `illustrative` or `source-derived`; source-derived requires sources.
- Ensure every glossary ref resolves and every projected term is used.
- Add validation for total coverage, length, plain-language lint, and forbidden current-state inflation.

## SWU-RCE-003

Compile `projection.json`, `glossary.json`, and their shared manifest as one atomic bundle.

- Add field-level provenance and scoped state.
- Use reviewed keywords for retrieval support; exclude example/analogy prose from ranking.
- Bind both artifact and schema digests into one `bundleDigest`.
- Extend leakage validation and adversarial fixtures.
- Prove deterministic generation and `--check` behavior.
- Stop if any projected field lacks an allowlist entry and source handle.
