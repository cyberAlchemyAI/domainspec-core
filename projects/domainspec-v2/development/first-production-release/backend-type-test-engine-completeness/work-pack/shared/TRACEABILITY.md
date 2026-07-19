# Traceability — Backend Type Test Engine Completeness

| Requirement | Layer | Task/SWU | Evidence target | Upstream owner |
| --- | --- | --- | --- | --- |
| Exact 13 backend kinds | L1 | CONTRACT / BTE-002 | profile contract and kind-set negative | FPR-02B + definitions |
| Exact 16 backend relationship signatures | L1/L2 | EDGE / BTE-009 | edge profile, traversal, causal composition/removal, and signature negatives | FPR-02B + relationship owner |
| One YAML schema per kind | L0/L1 | CONTRACT / BTE-001,002 | schema discovery/digest receipt | meta-type criteria owner |
| Shared evaluator across three surfaces | L0 | CONTRACT / BTE-001 | parity tests | tooling owner |
| Minted-node body mapping | L0 | NODE / BTE-003 | rule-family positive/negative matrix | minted-project contract owner |
| Positive exercise of every kind | L1 | NODE / BTE-004 | 13-node corpus receipt | FPR-02B/FPR-04 |
| Mutation per criterion | L1/L2 | NODE / BTE-004; DERIVATION / BTE-007 | 16 killed mutations | validation owner |
| Independent obligation denominator | L2 | OBLIGATIONS / BTE-005 | owner-bound `O_spec` and receipt | FPR-07 |
| Deterministic derivation | L2 | DERIVATION / BTE-006 | exact `O_gen`, key, provenance replay | semantic engine owner |
| Executable tests, no skips | L2 | DERIVATION / BTE-007 | execution report | FPR-07 |
| Fail-closed missing/empty witness | L3 | INTEGRATION / BTE-008 | seeded red receipts | release validation owner |
| Aggregate required checks | L3 | INTEGRATION / BTE-008 | required-check manifest | release validation owner |
| Integrated BTE/IOLM/Body War evidence | L3 | MANIFEST / BTE-010 | exact identity, digest, posture, and redaction comparison | consumer + Craft owners |
| Independent closure | L3 | VERIFY exemption | verifier verdict | independent reviewer |

## Recomposition

`BTE-001 + BTE-003` proves the common criterion boundary. `BTE-002 + BTE-004 + BTE-009` proves exact backend node/edge breadth. `BTE-005 + BTE-006 + BTE-007` proves independently denominated derivation and execution. `BTE-008 + BTE-010 + VERIFY` turns those proofs and the IOLM/Body War consumer receipts into a fail-closed, replayable, non-admitting FPR handoff.
