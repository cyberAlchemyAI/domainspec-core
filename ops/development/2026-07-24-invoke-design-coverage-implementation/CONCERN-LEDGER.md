# Concern Ledger: Invoke Design Coverage

This is an authored candidate. Until the independent extractor and validator
exist, its evidence state is `authored-complete`, not
`design-validator-pass`.

| Concern | Primary owner | Artifact owner | Validator owner | Disposition | Output |
| --- | --- | --- | --- | --- | --- |
| Architecture | Spellcraft | Invoke Design contract | `invoke-design-selection-validator` | required | architecture companion and triggered extensions |
| Authority | Spellcraft | schemas and mode gates | `invoke-design-selection-validator` | required | distinct author, extractor, validator, and consumer identities |
| Security/abuse | Spellcraft | receipt validation | `invoke-design-selection-validator` | required | forged, stale, replay, and self-issuance negatives |
| State/event | Spellcraft | selection result | `invoke-design-selection-validator` | required | four dispositions and two-pass transition |
| Persistence/concurrency | Spellcraft | repository writer contract | lifecycle validation | required | serialized canonical writer and generated-after-canonical rule |
| Failure/compensation | Spellcraft | diagnostics and repair route | fixture runner | required | deterministic failure codes and no partial pass |
| Integration/versioning | Spellcraft | canonical/generated interface | parity validator | required | versioned schemas and mirror parity |
| Migration | Spellcraft | old Design output adapter policy | fixture runner | required | legacy authored output cannot inherit validator pass |
| Privacy/data | package-local public-boundary owner | public/private scan | lifecycle validation | required | sanitized public fixtures and path/name scan |
| Validation | Spellcraft | fixture and validator contracts | fixture runner | required | red-before/green-after and mutation tests |
| UX/content/accessibility | Invoke UX companion owner | `UX-PLAN.md` | Spellcraft review | required | human-readable dispositions, diagnostics, recovery, and text semantics |
| Reliability | unresolved until detector exists | none | extractor | block | detector must prove whether service claims exist |
| Rollout/operations | unresolved until detector exists | none | extractor | block | detector must prove whether deployment/operator commitments exist |
| Performance | unresolved until detector exists | none | extractor | block | detector must prove whether measurable resource claims exist |

The last three rows block validator-backed N/A, not the remediation Plan whose
purpose is to implement the detector. They may become
`not-applicable-with-rationale` only through a detector-negative receipt.

