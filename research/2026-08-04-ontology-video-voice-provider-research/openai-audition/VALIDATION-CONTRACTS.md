# Planned Validation Contracts

Status: Design-stage contracts only. No fixture has been implemented or executed.

## Fixture specification

| ID | Claim | Polarity | Input or violation | Expected result | Phase |
|---|---|---|---|---|---|
| FX-001 | Frozen excerpt binds request | positive | Exact `audition-excerpt.txt` and digest | Preview contains exact 237-word text | L0 |
| FX-002 | Stale excerpt blocks | negative | One punctuation/code-point change | `not_ready`; no request preview admitted | L0 |
| FX-003 | Missing owner decision blocks | negative | Accent/locale unset | Block before credential/network/output | L0 |
| FX-004 | Secret cannot persist | negative | Secret-shaped field/value in manifest or output | Validator rejects and redacts diagnostics | L0 |
| FX-005 | Unsupported control blocks | negative | Add `seed`, `pitch`, or pronunciation field | Schema/request projection rejects | L0 |
| FX-006 | Exact request projection | positive | Complete admitted fixture manifest | Byte-stable redacted JSON for model/voice/input/instructions/format | L0 |
| FX-007 | No overwrite | negative | Existing attempt target | Stop before transport invocation | L1 |
| FX-008 | Ambiguous external failure | negative | Timeout after request write | No success event; bounded failure receipt; no automatic retry | L1 |
| FX-009 | Two repetitions match | positive | Two successful mocked binary responses | Two unique attempts; identical request digest | L1 |
| FX-010 | Invalid audio rejects | negative | Truncated or malformed WAV | Candidate rejected; raw evidence retained | L2 |
| FX-011 | Word mismatch rejects | negative | One omitted or substituted word | Unresolved fidelity mismatch; rejected | L2 |
| FX-012 | Body War error rejects | negative | Manual key-phrase review fails | Configuration rejected without text/control repair | L2 |
| FX-013 | Blind key separation | positive | Two verified repetitions and three listener orders | Opaque assets, separated repetitions, protected key | L2 |
| FX-014 | Scores cannot decide | negative | Passing weighted aggregate without operator record | State remains `blinded` | L2 |
| FX-015 | Disclosure required | negative | Audience-facing derivative lacks AI notice | Production handoff blocked | L3 |

## Validator contracts

| ID | Target | Binding | Verdicts | Stale/self-issue rule | Owner |
|---|---|---|---|---|---|
| VC-001 | Candidate manifest schema | Canonical manifest bytes + source digests | pass/fail | Stale input fails; validator cannot author owner decisions | audition-package-validator |
| VC-002 | Redacted request preview | Manifest digest + provider contract version | pass/fail | Any extra key or secret-shaped material fails | provider-interface-validator |
| VC-003 | Attempt receipt | Manifest + request + raw-byte hashes | pass/fail | Existing path, partial file, or mismatch fails | audition-runner-validator |
| VC-004 | Verification receipt | Raw/derivative hashes + pinned tool manifest | pass/fail | Tool/version/digest drift fails | verification-owner |
| VC-005 | Blind-listening package | Verified asset hashes + order/key manifests | pass/fail | Exposed key or unbalanced order fails | listening-experience-owner |
| VC-006 | Operator decision | Locked scores + unblinded evidence hashes | pass/fail | Missing named operator or illegal outcome fails | production-operator |

## Required validation surfaces

- JSON Schema or equivalent exact structural validation for every machine record.
- Deterministic canonical JSON digests for manifests and receipts.
- Node `node:test` unit and integration fixtures with an injected fake transport; no network in tests.
- A transport spy proving preflight failures invoke the network zero times.
- WAV inspection through a pinned local tool selected before L1.
- Independent forced alignment and word-fidelity passes with manual escalation.
- Static scans for `OPENAI_API_KEY`, bearer patterns, and unexpected request keys in generated evidence.
- Scoped whitespace, JSON parse, link, dependency, and no-overwrite checks.

## Claim ceiling

Passing local fixtures can establish implementation behavior under those fixtures. Only an explicitly authorized live audition can establish provider response evidence. Only human listening can establish voice-fit evidence. Neither can establish public-release authorization or production readiness.
