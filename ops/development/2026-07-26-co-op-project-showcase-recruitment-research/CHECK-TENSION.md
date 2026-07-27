# Check-Tension Receipt

- Candidate:
  `ops/development/2026-07-26-co-op-project-showcase-recruitment-research/dispatch-sheet.json`
- Admitted schema: `0.7.0`
- Sheet SHA-256:
  `af87013f928a664640923ad3e23087251341df900a4fd4c36722d8e0802555a6`
- Readiness: `PASS`
- Ledger mutation: `none`

## Independent Checker

- Handle:
  `tension-checker-2026-07-26-co-op-showcase-1`
- Verdict: `PASS`
- Digest:
  `af87013f928a664640923ad3e23087251341df900a4fd4c36722d8e0802555a6`
- Result:
  - `lane_z_explorers`: tests 1-4 pass.
  - `lane_a_explorers`: tests 1-4 pass.
  - `reviewers`: tests 1-4 pass.
  - sheet-wide test 5 passes.

## Independent Reviewer

- Handle:
  `tension-reviewer-2026-07-26-co-op-showcase-2`
- Verdict: `PASS`
- Digest:
  `af87013f928a664640923ad3e23087251341df900a4fd4c36722d8e0802555a6`
- Result:
  - all subject groups use canonical axes or declared composites;
  - each group's angles have distinct core methods and objects;
  - explorer lanes vary methodology and source corpus;
  - reviewer attack vectors are unique;
  - every unordered pair has an explicit predicted-disagreement sentence;
  - every group specializes the global portfolio-first versus decision-first
    recruitment tension.

The reviewer ran independently and received no checker apontamentos. Its own
verdict is unconditional `PASS`.

## Gate Result

`PASS + PASS`. The exact sheet may proceed to the human confirmation gate.
Any byte change to the sheet invalidates this receipt and requires live schema
validation plus two new independent tension verdicts.
