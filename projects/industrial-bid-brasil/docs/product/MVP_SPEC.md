# MVP Spec

## Purpose

Create a local-first industrial bidding assistant for Brazil that helps an
estimator decide whether to bid, what to clarify, which habilitation documents
are missing, how confident the cost model is, and whether the submission package
is complete.

## Primary User

An experienced industrial bidding estimator or owner-operator who participates
in bids for Petrobras, Vale, CSN, ArcelorMittal, energy, port, private, and
government opportunities.

## MVP Workflow

```text
Opportunity intake
-> document and field extraction
-> bid/no-bid scorecard
-> buyer question draft
-> habilitation readiness check
-> site visit risk check
-> cost confidence checklist
-> proposal/submission checklist
-> estimator review
```

## MVP Inputs

- edital, carta convite, email invitation, or portal export
- object and service quantities
- technical specification
- draft contract
- execution deadline
- payment terms
- site visit notes
- certificate register
- atestado library
- equipment and labor assumptions
- supplier quote library
- historical bid/job actuals when available

## MVP Outputs

- bid/no-bid recommendation: proceed, clarify, site-visit required, no-bid, or blocked
- missing data checklist
- technical clarification questions
- habilitation readiness report
- atestado fit warning
- cost confidence score
- payment and contract risk flags
- submission completeness checklist

## Non-Goals For MVP

- no autonomous final price
- no scraping private portals
- no legal advice
- no replacement for estimator approval
- no production CRM or ERP integration
- no copyrighted standards corpus

## Product Rules

1. If object or quantities are unclear, do not proceed to price confidence.
2. If technical specification or execution deadline is missing, block final
   recommendation.
3. If atestados are required and no matching atestado is available, flag
   habilitation risk as high.
4. If a field execution opportunity has no site visit or site facts, lower cost
   confidence.
5. If payment terms are poor, raise negotiation and cash-flow risk even when
   technical fit is high.

## Acceptance For MVP

The MVP is acceptable when it can load one opportunity and one organization data
pack, then produce a deterministic report with:

- all required missing fields listed
- scorecard component values
- human-readable rationale for each block or flag
- proposed buyer questions
- submission checklist status
- no silent pricing recommendation when required evidence is missing
