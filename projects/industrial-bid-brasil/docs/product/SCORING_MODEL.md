# Scoring Model

## Purpose

The first scoring model is deterministic and explainable. It should help an
estimator see why an opportunity is promising, risky, blocked, or not worth
pricing yet.

All component scores are 0 to 100. Missing critical evidence lowers confidence
or blocks final recommendation; it must not be hidden inside an average.

## Top-Level Recommendation

| Recommendation | Rule |
| --- | --- |
| Proceed | Composite >= 75 and no hard blockers. |
| Clarify | Composite 55-74, or missing non-critical evidence. |
| Site visit required | Field execution opportunity with insufficient site facts. |
| No-bid | Composite < 55, impossible deadline, high penalty, or unacceptable payment terms. |
| Blocked | Object, quantities, technical specification, deadline, or draft contract are missing or contradictory. |

## Composite Score

| Component | Weight |
| --- | ---: |
| Scope clarity | 20 |
| Deadline feasibility | 15 |
| Habilitation readiness | 15 |
| Site visit / assumption confidence | 15 |
| Cost confidence | 15 |
| Payment and contract risk | 10 |
| Submission completeness | 10 |

```text
composite =
  scope_clarity * 0.20 +
  deadline_feasibility * 0.15 +
  habilitation_readiness * 0.15 +
  site_confidence * 0.15 +
  cost_confidence * 0.15 +
  payment_contract_score * 0.10 +
  submission_completeness * 0.10
```

## Hard Blockers

- contract object unavailable
- service quantities unavailable
- technical specification unavailable
- execution deadline unavailable
- draft contract unavailable when penalties or payment terms govern risk
- impossible execution deadline
- required habilitation document unavailable and not recoverable before deadline
- incomplete mandatory pricing sheet at submission

## Component Metrics

### Scope Clarity

Inputs:

- object
- service quantities
- unit of measure
- technical specification
- draft contract
- assumptions and exclusions

Rule:

- Start at 100.
- Subtract 25 for missing quantities.
- Subtract 20 for missing technical specification.
- Subtract 15 for ambiguous method.
- Subtract 15 for unclear waste responsibility.
- Subtract 15 for unclear surface condition.
- Floor at 0.

### Deadline Feasibility

Inputs:

- proposal due date
- site visit date
- mobilization date
- execution deadline
- crew availability
- equipment availability

Rule:

- Start at 100.
- Subtract 30 if proposal deadline leaves insufficient review time.
- Subtract 25 if execution time is below historical minimum.
- Subtract 20 if mobilization window is unknown.
- Subtract 15 if crew or equipment availability is unconfirmed.
- Any impossible deadline sets recommendation to no-bid.

### Habilitation Readiness

Inputs:

- certificate register
- buyer registrations
- atestado library
- edital/carta convite required documents

Rule:

- Required certificate present and valid: full credit.
- Certificate expired before submission: zero for that item.
- Atestado text missing or weakly matched: high-risk flag.
- Missing required atestado can block submission.

### Site Visit / Assumption Confidence

Inputs:

- real area
- height and access
- operation interference
- permitted work hours
- mobilization and transport facts
- surface condition

Rule:

- Start at 100 when site visit facts are complete.
- Start at 50 when no visit happened but assumptions are documented.
- Start at 35 when field facts are mostly unknown.
- Add explicit assumptions and exclusions before allowing proposal export.

### Cost Confidence

Inputs:

- direct labor
- encargos sociais
- benefits, food, transport
- consumables
- paints and solvents
- equipment
- indirect costs
- taxes
- mobilization
- maintenance
- margin and risk reserve

Rule:

- Missing mobilization or maintenance subtracts 20 each.
- Missing supplier quote validity subtracts 10.
- Missing productivity basis subtracts 25.
- Missing tax assumptions subtracts 15.

### Payment And Contract Risk

Inputs:

- payment schedule
- retention
- penalty clauses
- aditivo language
- buyer payment history
- working capital cost

Rule:

- Bad payment terms may force no-bid even with high technical fit.
- High penalty subtracts 30.
- No aditivo path with uncertain scope subtracts 25.
- Payment delay history subtracts 10-25 by severity.

### Submission Completeness

Inputs:

- portal checklist
- required planilhas
- documents
- signatures
- file formats
- envelope rules where applicable

Rule:

- Every mandatory item must be present before submission.
- Missing mandatory planilha is eliminatory.
- Score can be high only after final package review.

## Risk-Adjusted Expected Profit

```text
risk_adjusted_expected_profit =
  (expected_revenue
   - expected_cost
   - risk_reserve
   - financial_cost_of_payment_terms)
  * win_probability
```

## Pricing Authority Rule

The engine may recommend a pricing confidence level, but final price authority
stays with the estimator. No final price recommendation is allowed unless:

- object is clear
- quantities are known
- technical specification is available
- execution deadline is known
- payment terms are known
- cost blocks are complete or explicitly assumed
- risk reserve is visible
