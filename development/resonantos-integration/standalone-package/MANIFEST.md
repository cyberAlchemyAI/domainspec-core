# Package Manifest

## Root Files

| Path | Purpose |
| --- | --- |
| `README.md` | Package entrypoint. |
| `INTEGRATION-GUIDE.md` | Generic host-facing integration guide. |
| `OWNED-BASE.md` | Public-safe owned base and runnable/design boundary. |
| `FINDINGS.md` | Concise evidence-backed findings. |
| `boundaries.md` | Scrub, claim, and publication boundary. |
| `VERIFY.md` | Verification commands and status. |
| `SCRUB-REPORT.md` | Redaction and boundary scan report. |
| `HANDOFF.md` | Commit/handoff checklist for a later package commit. |
| `DECISIONS.md` | Decision-gate record for this package creation. |

## Contracts And Tools

| Path | Purpose |
| --- | --- |
| `contracts/evidence-card.schema.yml` | Copied public inventory evidence-card schema. |
| `contracts/evidence-set.schema.yml` | Copied public EvidenceSet schema. |
| `contracts/index.schema.yml` | Copied public inventory index schema. |
| `tools/validate-evidence-card-slice.sh` | Copied evidence-card slice validator. |
| `tools/validate-evidence-card-fixtures.sh` | Copied fixture validator. |
| `tools/validate-index-json.sh` | Copied index validator. |

## Fixtures

| Path | Purpose |
| --- | --- |
| `fixtures/evidence-card/cards.json` | Synthetic candidate cards for this package. |
| `fixtures/evidence-card/index.json` | Synthetic card index. |
| `fixtures/evidence-card/retrieval.json` | Retrieval fixture for package cards. |
| `fixtures/evidence-card/evidence-sets.json` | EvidenceSet fixture for package cards. |
| `fixtures/review-queue/candidate-request.json` | Candidate intake and Review Queue fixture. |
| `fixtures/no-promotion/no-promotion-case.json` | Default-deny promotion guardrail fixture. |

## Docs And Examples

| Path | Purpose |
| --- | --- |
| `docs/validator-policy.md` | Validator copy and provenance policy. |
| `docs/review-queue-mapping.md` | Candidate-to-Review-Queue lifecycle mapping. |
| `docs/scope-tags.md` | Scope-tag contract for candidate fixtures. |
| `docs/read-only-observer.md` | Read-only observer and meter receipt contract. |
| `docs/no-promotion-policy.md` | Default-deny promotion guardrail policy. |
| `docs/host-promotion-provider-body.md` | Host-side provider body contract. |
| `examples/observer/README.md` | Observer example notes. |
| `examples/provider-body/pseudocode.md` | Provider body pseudocode boundary example. |

## Source Material

`source-material/` contains redacted copies of the local source docs used to create the package.
They are retained for traceability and should be reviewed before any external publication.
