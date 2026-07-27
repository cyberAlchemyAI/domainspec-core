# Requirement Traceability

| Requirement | Design owner | SWUs | Required closure evidence |
| --- | --- | --- | --- |
| ILP-R01 authored/readiness split | Plan integration | 005 | authored-pass plus gated/blocked readiness matrix |
| ILP-R02 immutable one-SWU epoch | epoch contract | 002 | completeness and changed-control rejection fixtures |
| ILP-R03 mode-compatible roles | readiness | 004 | local and packaged positives; missing/incompatible/self-validation negatives |
| ILP-R04 ready-only Task Session route | Plan + Task Session | 005, 007 | real route entry and live pre-write matrices |
| ILP-R05 byte drift vs impact | drift classifier | 006A | exact join block plus four impact verdicts |
| ILP-R06 successor/supersession | transition validator | 003, 006B | every epoch-control mutation rejects same-epoch repair |
| ILP-R07 admitted append-only progress | authority + transition validator | 001, 003, 008B | owner receipt, edge fixtures, transition-derived denominator |
| ILP-R08 exclusive Refresh kinds | Refresh integration | 006B | kind/postcondition matrix and no-target-implementation negative |
| ILP-R09 legacy/path/local schema proof | epoch/readiness/migration | 002, 004, 008A | legacy no-inference and fresh revalidation receipts |
| ILP-R10 generic live proof/privacy | live proof and audit | 009, VERIFY | live receipt chain, exact-drift negative, public/private scan |

No requirement closes from prose status alone.

