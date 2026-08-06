# State and event contract

## Invocation algebra

| State | Allowed successor | Failure behavior |
|---|---|---|
| transport received | transport rejection or request admitted | one typed rejection; no trusted disposition |
| request admitted | catalog admitted or `invalid` | invalid subject/reasons, zero candidate |
| catalog admitted | evaluated | pure finite evaluation |
| evaluated | `candidate`, `ambiguous`, or `no-match` | exhaustive terminal branch |

`invalid` is also terminal for admitted requests with invalid catalogs. Every
trusted terminal disposition is immutable and canonical.

## Human boundary

`candidate` does not transition to a resolver-owned selected state. Human
confirmation creates or confirms the existing canonical Dispatch/group/seat
under its existing owner. That separate artifact may then be evaluated by the
host binding and authorization owners.

## Admission lifecycle

Candidate, canonical, generated, installed, consumer-admitted, released, and
deployed are distinct evidence states. No automatic transition crosses them.

