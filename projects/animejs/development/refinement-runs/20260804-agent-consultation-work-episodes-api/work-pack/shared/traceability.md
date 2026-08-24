# Design-to-SWU Traceability

| Design invariant | Implemented by | Accepted by |
| --- | --- | --- |
| closed neutral projection allowlist and leakage report | 001, 006 | forbidden-field mutants and deterministic manifest digest |
| disjoint read/append/recovery/project capabilities | 002, 009 | capability matrix with zero journal delta on denial |
| immutable Task/Version/owner/graph context | 002, 008 | handle mutation and cross-principal fixtures |
| exact transition and terminal rules | 003, 008 | transition matrix and lifecycle service tests |
| atomic append, idempotency, unambiguous recovery | 004 | stale-writer and before/after-commit crash fixtures |
| immutable digest-chained history | 004, 005 | gap/fork/order/digest rejection |
| version-keyed deterministic snapshots | 005 | repeated byte replay and upgrade retention |
| overlay-only supersession and zero canonical writes | 003, 006 | cycle and canonical-delta assertions |
| evidence provenance and revocation eligibility | 008 | forged/rebound/revoked evidence fixtures |
| semantic effect none and zero Lessons | 002, 006, 008, 010 | receipt and graph-closure assertions |
| bounded consultation/abstention/stale/denied algebra | 001, 007 | query and failure-union tests |

All rows recompose into [API-CONTRACT.md](../../API-CONTRACT.md); none reaches
the explicitly excluded L3 transport or Lesson-review route.

