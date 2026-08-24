# Inventory Bootstrap Diagnostic

## Scope and authority

This is governance-only diagnostic evidence for dispatch
`2026-08-09-augmentor-resonantos-ontology-docs-mvp`. It does not change the
Inventory entry, result record, indexes, log, runtime, accepted research,
product code, authority, or external state.

## Reproduced failure

Command:

```text
.arcanum/inventory/bin/inventory append --record research/2026-08-09-augmentor-resonantos-ontology-docs-mvp/inventory-result-record.json --timestamp 2026-08-09T21:00:26Z --dry-run --json
```

Observed exit code: `1`.

Observed operation receipt:

- status: `baseline-blocked`
- reason code: `baseline-not-ready`
- operation fingerprint:
  `e6b48f85f8d9c334839f08be3912cec722965cd78bb25d227b054f61c373ff0b`
- receipt SHA-256:
  `d044c22f8e8558ac05afc776653c6f444699341bdc92d72f74b8393b55869e04`
- baseline index SHA-256:
  `ebda7d9d8d5ff0b40c1d4308c46e29ced5aad1b53e9511e62d308ffbc8d82d29`
- baseline human-index SHA-256:
  `a1a8c30b98db89bafa6e22725aa83877671d0d37883c215ab057350fc1f81a13`
- baseline failure count: `1`
- baseline warning count: `150`
- candidate: `not-reached`
- write attempted: `false`
- observed changed paths: none

The direct projection-conformance report identifies the only failure as:

```text
source_coverage: source has no machine row: entries/augmentor-resonantos-ontology-docs-mvp-research-result-synthesis.md
```

## Root cause

The append dry-run validates the baseline before it reads and normalizes the
record. The staged entry must already exist under the governed `entries/**/*.md`
root so the candidate can pass existence and source-coverage validation. Its
presence, however, makes the old baseline non-ready because the old machine
index does not yet contain its row. The operation exits before it can construct
the candidate that would repair that exact gap.

This is a candidate-admission ordering deadlock, not disputed Inventory content
and not general permission to append over a broken baseline.

## Affected invariant

Inventory append needs both halves of this invariant:

1. unrelated baseline failures must block mutation; and
2. a staged governed source plus its exact new record must be able to produce a
   fully conformant candidate that adds the missing row.

The current implementation enforces the first half so early that the second
half is unreachable. The safe state was preserved: neither `index.json` nor
`index.md` was written.

## Identity evidence

The staged entry and append record agree on:

- ID:
  `augmentor-resonantos-ontology-docs-mvp-research-result-synthesis`
- path:
  `entries/augmentor-resonantos-ontology-docs-mvp-research-result-synthesis.md`
- kind: `entry`
- type: `synthesis`

The machine index contains no row for that result ID or path. It contains the
distinct earlier strategy-result entry only.

## Minimal repair boundary

Make baseline admission candidate-aware for exactly one repairable source gap.
Read and normalize the record before returning `baseline-not-ready`, then allow
candidate construction only when the complete baseline failure set is exactly
the missing machine row for the normalized new entry. Require the resulting
staged candidate to pass full projection conformance before dry-run or apply can
succeed.

All other baseline failures remain blocking.

