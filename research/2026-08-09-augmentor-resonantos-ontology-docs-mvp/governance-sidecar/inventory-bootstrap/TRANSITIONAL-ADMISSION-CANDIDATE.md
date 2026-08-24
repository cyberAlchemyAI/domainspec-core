# Candidate: Fail-Closed Transitional Inventory Admission

## Status

Separately staged governance-runtime repair proposal. This document is not an
applied patch and grants no authority to modify canonical Inventory runtime
files.

## Proposed behavior

In `runAppendDryRun`, preserve the current runtime and baseline-byte checks, but
move record parsing and normalization before the unconditional
`baseline-not-ready` return.

Define a deterministic predicate equivalent to:

```text
repairable_single_source_gap(report, normalized_entry, transition) =
  transition.disposition == "added"
  AND report.failure_count == 1
  AND source_coverage is the only failed check
  AND source_coverage.missing_source_rows == [normalized_entry.path]
  AND source_coverage.orphan_machine_rows == []
  AND source_coverage.errors == [
    "source has no machine row: " + normalized_entry.path
  ]
  AND every non-source-coverage check is pass
```

Admission rules:

1. If the baseline is ready, retain current behavior.
2. If the baseline is blocked and the predicate is false, retain
   `baseline-blocked / baseline-not-ready`.
3. If the predicate is true, construct the index and human-index candidate in
   the isolated staged Inventory copy.
4. Require the candidate report to be fully `ready`. A candidate failure stays
   `candidate-blocked`; it never reaches apply.
5. Preserve the observed blocked baseline report in the receipt and add a
   machine-readable disposition or residue such as
   `baseline-single-source-gap-repaired-by-candidate`.
6. Apply must reproduce the validated candidate digests and repeat the existing
   immediate baseline-drift check before either index write.

The predicate must inspect structured report fields, not match a substring in
console output.

## Why this remains fail-closed

The exception is bound to one normalized record path and one prospective
`added` transition. It cannot admit:

- an unrelated unindexed source;
- two or more missing rows;
- an orphan machine row;
- an identity, facet, existence, derived-map, human-view, or freshness failure;
- a conflicting existing ID;
- a record whose path differs from the missing source; or
- a candidate that is not fully projection-conformant.

The exact baseline and candidate bytes remain digest-bound. This changes the
order of candidate admission, not the authority or validation ceiling.

## Regression proof required before apply

Add a finite fixture matrix to the owned Inventory runtime tests:

| Fixture | Expected result |
| --- | --- |
| Ready baseline plus valid new record/source | `dry-run-ready`; no writes |
| Baseline with only the matching staged source gap | `dry-run-ready`; candidate ready; no writes |
| Matching source gap plus one unrelated missing source | `baseline-blocked` |
| Matching source gap plus any non-source check failure | `baseline-blocked` |
| Missing source path differs from normalized record path | `baseline-blocked` |
| Existing ID differs from the submitted record | conflict/block |
| Matching gap but candidate validation fails | `candidate-blocked` |
| Apply after validated dry-run with unchanged baseline | both index projections match validated candidate digests and final conformance is ready |
| Baseline changes between dry-run and write | `baseline-drift-before-write`; no candidate commit |

Each dry-run fixture must assert byte identity for the real `index.json` and
`index.md`. Each negative fixture must assert zero writes.

## Required revalidation

After an owner accepts exact repair bytes:

1. Run the owned Inventory runtime unit and integration tests, including the
   matrix above.
2. Re-run the original dry-run command with the original record and timestamp.
3. Require `dry-run-ready`, candidate `lookup_readiness: ready`, and no observed
   writes.
4. Apply only through the Inventory appender, not by hand-editing either index.
5. Run the full projection-conformance validator over the applied `index.json`.
6. Require one machine row and one human row for the result entry, exact derived
   maps, ready lookup state, and an Inventory log closeout through the owned
   workflow.
7. Run scoped whitespace/diff checks over the accepted runtime repair and the
   Inventory closeout artifacts.

## Acceptance boundary

Renewed owner acceptance is required for the exact canonical runtime repair
bytes because they change Inventory admission semantics. The unchanged research
entry and result record do not need semantic reconfirmation merely because the
runtime repair is mechanical; they still must pass the repaired dry-run and
normal apply gates.

