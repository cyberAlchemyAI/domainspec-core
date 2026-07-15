---
wave: W2
layer: L1
status: blocked
---

# W2: FPR-02 Supported Profile

## Decision

After this wave, we know whether one exact backend profile and pilot boundary can serve as a nonempty denominator.

## Order

1. `SWU-FPR02-001` — decide admitted/exercised/deferred scope, origin, redaction, claims, rollback, and owners.
2. `SWU-FPR02-002` — emit schemas/artifacts and stable profile digest.
3. `SWU-FPR02-003` — kill fail-closed negative matrix.

## Entry

Verified FPR-01 ratification receipt.

## Promotion Gate

One validator consumes every declared artifact; two runs yield the same digest; empty, unknown, absent, deferred, placeholder, missing-obligation, unresolved-origin, and empty-redaction fixtures all fail distinctly.

