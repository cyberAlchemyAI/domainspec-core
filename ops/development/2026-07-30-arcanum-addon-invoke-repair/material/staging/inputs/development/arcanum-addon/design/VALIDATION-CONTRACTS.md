# Validation Contracts

All rows are planned. They are not Plan or execution evidence.

## Fixtures

| Fixture | Claim | Polarity | Target | Expected result | Execution phase |
| --- | --- | --- | --- | --- | --- |
| F-MANIFEST-VALID | catalog separation | positive | sideload manifest | valid; available/uninstalled/disabled/ungranted | implementation |
| F-MANIFEST-SECRET | public/secret boundary | negative | manifest validator | secret/private marker rejected | implementation |
| F-PREVIEW-ZERO | preview zero effects | positive + negative counters | pure proposal resolver | deterministic bytes and all effect counters zero | implementation |
| F-STALE-DIGEST | exact approval | negative | approval route | stale digest rejected; zero starts | implementation |
| F-REPLAY | at-most-once | negative | run route | second action starts nothing | implementation |
| F-MISSING-STRATEGY | no substitution | negative | adapter | Strategy blocked; OpenCode/Hermes/model-CLI counters zero | validation |
| F-CHILD-ISOLATION | scoped clarification | negative | child route | A receives one; parent/B zero | validation |
| F-RELOAD | owner truth | positive | run projection | identical owner state or `Unknown` | validation |
| F-DISABLE | lifecycle | negative | cached launch | zero new starts | validation |
| F-DEGRADED-COMPAT | compatibility drift | negative | enabled/running candidate + changed provenance | zero new starts; `Incompatible`; history preserved; explicit re-enable required | validation |
| F-DEGRADED-OWNER | owner loss | negative | enabled/running candidate + unavailable required owner | zero substitution/starts; `Blocked` or `Unknown`; history preserved | validation |
| F-UNINSTALL-PRESERVE | uninstall separation | positive + forbidden-mutation counters | isolated accepted disabled snapshot | product-owned state removed; Bootstrap inventory and retained owner history unchanged | validation |
| F-ROLLBACK-FAIL | rollback separation | positive + forced failure | separate isolated copy of the same disabled snapshot | pinned product artifacts restore on success; failure remains disabled; Bootstrap/history unchanged | validation |
| F-TWO-CHILD-BROWSER | end-to-end product value | positive/negative | extension + bridge local fixture | all significant scenario observations | validation |

## Validator Contracts

| Contract | Target | Accepted binding | Verdicts | Stale/self-issue rule | Owner |
| --- | --- | --- | --- | --- | --- |
| V-MANIFEST | `addon.arcanum` JSON | current SDK source and manifest digest | pass/fail | reject stale SDK binding | Add-on SDK |
| V-BOOTSTRAP | compatibility receipt | source/bootstrap/selection/content digests | compatible/incompatible | detector cannot self-admit | compatibility validator |
| V-PROPOSAL | proposal canonicalization | proposal schema/profile/grant/provenance digest | pass/fail | reject stale digest | proposal validator |
| V-APPROVAL | persisted approval | current proposal + approver + expiry + replay | pass/fail | approval owner distinct from UI | host approval owner |
| V-OWNER-RESULT | run/child reconciliation | owner handle and record schema | exact/Unknown | UI cannot self-issue terminal state | reconciliation owner |
| V-LIFECYCLE-BRANCHES | degradation/uninstall/rollback receipts | same accepted disabled snapshot digest, isolated branch ids, forbidden-mutation counters, recovery result | pass/fail | branch owner cannot admit missing sibling or changed baseline | lifecycle validation owner |
| V-REDACTION | every sink | forbidden canary set | pass/fail | any match fails | security owner |

## Repository Gates

- focused Add-on SDK manifest/registry tests;
- focused bridge capability consistency and Arcanum route tests;
- focused proposal/approval/replay/state/clarification/artifact/lifecycle tests;
- `npm run test:browser-first`;
- `node scripts/security-pipeline/run-check.mjs`;
- `npm run pre-release:scan`;
- `npm run verify:alpha`;
- live Chrome fixture only after deterministic gates pass.

Successful execution of any subset does not decide readiness, promotion, or
release.
