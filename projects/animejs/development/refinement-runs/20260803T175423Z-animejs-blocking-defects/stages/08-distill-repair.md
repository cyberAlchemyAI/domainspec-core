# Stage 08 — Distill Repair and Toy-Game Specification

## Repair delta

The repaired design closes the original two defects without claiming implementation:

- QRY-003 now has a closed vocabulary, exact terminal mappings, deterministic precedence, receipt nullability, migration semantics, and eight finite planned fixtures.
- The relation set is no longer admitted wholesale: 17 candidates have discriminating planned witnesses, five are marked `MERGE`, and three are marked `DEFER`.

Structured evidence:

- `08-query-contract-matrix.json`
- `08-relation-behavior-witness-matrix.json`

## Toy game

For each retained relation:

1. Construct the exact source and target fixture.
2. Run the named consumer against the baseline relation.
3. Remove the edge or alter the specified property and run the same consumer.
4. Compare the observable output to the planned mutant delta.
5. Fail when the asserted delta is absent or differs.

For query behavior, run each named fixture against the repaired algorithm version and fail on an undeclared code, wrong precedence, invalid receipt nullability, or rewritten historical receipt.

## Pareto gate

- Vocabulary size is minimized: no new ambiguous-choice synonym.
- Determinism increases: terminal mapping and precedence are explicit.
- Behavioral evidence is strengthened: retention requires an observable delta.
- Migration cost remains bounded: version the new algorithm and preserve old receipts.
- Scope remains bounded: no ontology or runtime mutation in Refine.

## Validation result

`pass` for repair-design non-vacuity: all 25 candidates have a finite disposition and all 17 retained rows have a planned delta. `planned_not_executed` for the toy game and query fixtures.
