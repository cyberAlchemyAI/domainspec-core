# Stage 05 — Distill

## Round 1: candidate units

| Candidate | Benefit | Failure mode |
| --- | --- | --- |
| Query-code patch only | Smallest textual change. | Leaves terminal mappings, precedence, nullability, and decorative relations open. |
| Retain all relations with named consumers | Preserves the 25-term vocabulary. | Consumer labels remain vacuous; eight mutants survive. |
| Full ontology rebuild | Could absorb all changes at once. | Exceeds the confirmed Refine scope and hides unexecuted evidence behind new bytes. |
| AKV non-vacuity repair contract | Couples query terminal closure with falsifiable relation retention. | Requires a later implementation owner to materialize and execute fixtures. |

## Round 2: selected core

Select the `AKV non-vacuity repair contract` as the smallest coherent unit. It contains exactly two mandatory components:

1. a closed QRY-003/QueryReceipt terminal contract; and
2. a 25-row relation-retention registry with `RETAIN`, `MERGE`, or `DEFER` evidence.

Neither component is independently sufficient. Query closure without relation evidence leaves inert graph edges; relation closure without query closure leaves an undeclared terminal result.

## Recomposition proof

The selected core can later compose with the candidate ontology by:

- generating or validating QueryReceipt behavior from the query matrix;
- admitting only the 17 retained relations into the executable candidate surface;
- representing five merge decisions as canonicalization work, not duplicate edges;
- excluding three deferred relations from retention until behavior is specified; and
- binding every retained relation to a named fixture and failure assertion.

This recomposition is a design proof only. It does not claim the candidate ontology exists or that any fixture passes.

## Verdict

`pass` for distilled repair scope.
