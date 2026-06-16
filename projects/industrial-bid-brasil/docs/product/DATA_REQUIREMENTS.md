# Data Requirements

## Data Principle

The engine improves in two stages:

1. Public and web data provide market context, buyer-process context, financial
   calibration, and comparable public awards.
2. Organization-side data provides the real advantage: productivity, atestados,
   buyer behavior, pricing history, payment delays, and actual margin.

## Minimum Viable Organization Data

| Data Class | Template | Required Fields | Primary Use |
| --- | --- | --- | --- |
| Company profile | `company_profile.csv` | legal name, CNPJ, services, buyer registrations | habilitation and portal readiness |
| Certificates | `certificates_register.csv` | document type, issuer, expiry, file path, status | disqualification prevention |
| Atestados | `atestados_register.csv` | buyer, service, quantity, dates, signer, wording | technical eligibility and fit |
| Equipment | `equipment_register.csv` | equipment, capacity, location, availability, cost | feasibility and cost |
| Labor | `labor_register.csv` | role, rate, location, availability, assumptions | direct labor and mobilization |
| Supplier quotes | `supplier_quotes.csv` | item, supplier, unit, price, validity, region | cost confidence |
| Historical bids | `historical_bids.csv` | buyer, object, quantity, price, result, winner | win and competitiveness learning |
| Job actuals | `job_actuals.csv` | planned vs actual cost, productivity, delay, margin | pricing and execution learning |
| Buyer feedback | `buyer_feedback.csv` | bid, buyer, reason won/lost, notes | win/loss model |

## Public And Web Data Lanes

| Lane | Sources | Data To Collect | Use |
| --- | --- | --- | --- |
| Public procurement | PNCP, Compras.gov.br, Portal da Transparencia, Painel de Compras | object, buyer, modality, item, quantity, winner, value, dates, contract | comparable prices and buyer context |
| Buyer workflow | Petrobras, Petronect, Vale suppliers, Eletrobras, Ariba, Nimbi, SRM | registration workflow, portal steps, attachment rules, revision rounds | submission readiness |
| Cost and finance | SINAPI, IBGE, BCB SGS, PDET/Novo CAGED/RAIS | indices, rates, labor context, financial series | benchmark and escalation |
| Safety and standards | NRs, buyer specs, internal method statements | standard identifiers, required checks, proposal sections | compliance and technical proposal |

## Collection Rules

- Login-gated or invitation-only buyer portal data must be collected through the
  contractor's lawful account and explicit operator action.
- Store source URLs, collection dates, and confidence.
- Keep public comparable prices separate from private bid history.
- Do not copy copyrighted technical standards into the project. Store
  identifiers, applicability notes, and permitted excerpts only.

## Confidence Rules

- Missing private job actuals means productivity confidence starts low.
- Missing supplier quote validity means material price confidence starts low.
- Missing payment history means cash-flow risk uses public financial proxies.
- Missing atestado text means eligibility confidence cannot be automated.
