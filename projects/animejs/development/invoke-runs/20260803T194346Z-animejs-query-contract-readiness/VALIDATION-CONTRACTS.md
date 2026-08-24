# Validation Contracts

## Design witness contracts

| Fixture | Claim | Polarity | Input or violation | Expected result | Phase |
| --- | --- | --- | --- | --- | --- |
| QRY003-POS-JS-001 | success XOR | positive | JS candidate wins | selected JS ID; null abstention | implementation |
| QRY003-POS-WAAPI-001 | success XOR | positive | WAAPI candidate wins | selected WAAPI ID; null abstention | implementation |
| QRY003-NEG-TIE-001 | tie normalization | negative | equal top candidates | `ABSTAIN_AMBIGUOUS_INTENT`; one next question | implementation |
| QRY003-NEG-VERSION-001 | version gate | negative | missing exact VersionContext | `ABSTAIN_UNKNOWN_VERSION` | implementation |
| QRY003-NEG-UNKNOWN-001 | source gap | negative | understood feature without binding | `ABSTAIN_MISSING_SOURCE` | implementation |
| QRY003-NEG-CONFLICT-001 | contradiction gate | negative | incompatible intersecting propositions | `ABSTAIN_CONFLICT`; both preserved | implementation |
| QRY003-NEG-PERF-001 | performance evidence gate | negative | unsupported performance claim | `ABSTAIN_PERFORMANCE_EVIDENCE` | implementation |
| QRY003-NEG-PRECEDENCE-001 | total precedence | negative | all failure predicates true | unknown version primary; subordinate gaps preserved | implementation |

## Validator contract

| Contract | Target | Required binding | Verdicts | Stale input | Self-issued evidence | Owner |
| --- | --- | --- | --- | --- | --- | --- |
| VAL-QRY003-001 | schema, policy, eight fixtures | exact algorithm version, six codes, eight IDs | pass/fail | reject | reject | query-contract-candidate-owner |

## Acceptance-critical checks

1. Policy JSON parses and declares exactly the six expected codes in the exact precedence order.
2. Schema JSON parses and rejects `ABSTAIN_AMBIGUOUS_CHOICE`.
3. Migration note states new-receipt-only adoption and historical immutability.
4. Runner discovers exactly eight unique fixture IDs.
5. Every fixture result matches its expected terminal contract.
6. Validation writes only its predeclared execution receipt path.

All rows are `plan-evidence-pending` after Plan. No check is marked executed by Design.
