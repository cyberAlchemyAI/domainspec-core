# Stage 07 — Interrogation: Design Review

## Attack questions

| Attack | Design response | Outcome |
| --- | --- | --- |
| Can the tie path still emit an undeclared code? | The closed vocabulary excludes `ABSTAIN_AMBIGUOUS_CHOICE`; tie maps to `ABSTAIN_AMBIGUOUS_INTENT`. | Closed at design level. |
| Can simultaneous failures produce nondeterministic codes? | A total six-code precedence selects one primary code and preserves subordinate gaps. | Closed at design level. |
| Can a successful receipt carry an abstention code? | Success requires non-empty selection and null code; abstention requires declared non-null code. | Closed at design level. |
| Can a relation survive merely because its consumer field is non-empty? | No. `RETAIN` requires a baseline, mutant, observable delta, and failing assertion. | Closed at design level. |
| Can duplicate edge and endpoint fields both be treated as canonical? | No. Five candidates are `MERGE` until canonicalization/equality validation is chosen. | Correctly non-retained. |
| Can underdefined consumers enter the retained vocabulary? | No. Three candidates are `DEFER` until traversal/output behavior is exact. | Correctly non-retained. |
| Does this design prove runtime behavior? | No. All rows and fixtures are explicitly planned. | Evidence ceiling preserved. |

## Surviving residue

- Canonical representation for five merge candidates is not selected here.
- Concrete consumer contracts for three deferred candidates do not yet exist.
- Dynamic fixture results do not yet exist.

## Verdict

`pass` for design completeness and falsifiability; `not_executed` for runtime validation.
