---
title: Brazil Industrial Bid Engine Research Strategy
date: 2026-06-11
status: exploration
dispatch: docs/strategy/brazil_industrial_bid_research_dispatch_2026-06-11.json
seed_artifacts:
  - docs/strategy/brazil_industrial_bid_questionnaire.html
  - docs/strategy/brazil_industrial_bid_intelligence_wladimir_2026-06-11.md
scope: research strategy for optimization parameters, web/public data collection, and organization-side data requirements
---

# Brazil Industrial Bid Engine Research Strategy

This strategy defines what a Brazil industrial bid-response engine should
optimize, what data can likely be collected from scattered public web sources,
and what private organization data is needed to make the engine excellent.

It is exploratory. It does not promote a product spec, runtime module, card, or
canonical memory.

## 1. Core Thesis

The Brazil industrial bidding engine should optimize a contractor's chance of
submitting a complete, qualified, technically credible, correctly priced bid
that can survive execution and negotiation without destroying margin.

The engine is not just a proposal writer. It is a decision and pricing system
with five linked jobs:

1. Decide whether to bid.
2. Extract contract object, quantities, deadlines, payment terms, penalties,
   site-visit conditions, and technical specifications.
3. Build a risk-aware cost composition.
4. Assemble technical and commercial proposal material.
5. Validate submission completeness for portals, email, or sealed envelopes.

## 2. Optimization Targets

The engine should optimize multiple objectives at once. A bid that maximizes
win probability but loses money is bad; a high-margin bid that is technically
disqualified is also bad.

### 2.1 Primary Objective Functions

| Objective | What It Means | Why It Matters |
|---|---|---|
| Qualified bid probability | Probability the contractor survives habilitation, documentation, and technical-compliance review | Avoids wasted bid effort and disqualification |
| Win probability | Probability the buyer selects the bid | Core commercial target |
| Risk-adjusted expected profit | Expected margin after technical, scope, payment, and execution risk | Prevents "winning a loss" |
| Cash-flow safety | Whether payment terms and working-capital burden are tolerable | Bad payment terms were named as a hard negotiation boundary |
| Execution feasibility | Whether team, equipment, access, site conditions, and schedule make the work executable | Prevents impossible delivery commitments |
| Submission completeness | Whether all planilhas, documents, signatures, and portal/envelope requirements are complete | Wladimir named incomplete planilha as eliminatory |

### 2.2 Secondary Optimization Targets

- Price competitiveness against historical awards and known buyer behavior
- Scope uncertainty reduction before final price
- Site-visit information completeness
- Atestado tecnico fit against required scope
- Technical proposal credibility
- Negotiation resilience through explicit assumptions and exclusions
- Learning rate from prior bids and actual job results

## 3. Metric Ledger

Each metric should have a direct data source, a fallback proxy, and an owner.

| Metric | Direct Inputs | Public/Web Sources | Org-Side Sources | Fallback Proxy |
|---|---|---|---|---|
| Scope clarity score | Object, service quantities, units, technical spec, draft contract | Edital/carta convite, PNCP/Compras.gov.br notices, buyer portals | Buyer invitation docs, internal clarifications | Count missing required fields |
| Deadline feasibility score | Proposal due date, site visit date, mobilization date, execution deadline | Public notices, portal deadlines | Historical mobilization duration, crew availability | Deadline vs historical median preparation/execution time |
| Habilitation readiness | Required certificates, registrations, negative certificates, atestados | Edital requirements, buyer supplier pages | Company certificates, atestado library, expiry dates | Required-doc checklist coverage |
| Atestado fit score | Required service type, buyer minimum experience, atestado scope text | Edital/carta convite | Atestado corpus and prior service descriptions | Text similarity plus manual review |
| Site-visit risk score | real area, access, height, surface condition, operation interference | Usually not public | Site visit forms, photos, measurements, notes | No visit = high uncertainty |
| Cost confidence | labor, materials, equipment, indirects, taxes, mobilization, maintenance | SINAPI/IBGE, public price indices, BCB series, labor datasets | Internal cost sheets, supplier quotes, job actuals | Confidence by missing cost blocks |
| Productivity confidence | method, area, height, access, surface condition, work hours | Standards/guides rarely give real productivity | Historical production rates by service and site condition | Wladimir/estimator default ranges |
| Price competitiveness | historical award values, unit prices, incumbent data | PNCP, Compras.gov.br, Portal da Transparencia, public contracts | Submitted prices, buyer feedback, known competitor prices | Comparable public award bands |
| Payment-term risk | payment schedule, retention, financial cost, delay history | Contract draft, public contracts where available | Internal receivables history, buyer payment history | BCB interest series applied to payment lag |
| Aditivo exposure | scope uncertainty, contract amendment language, buyer history | Draft contract, public contract amendments where available | prior aditivos, disputed scopes, actual-vs-bid variance | contract language risk flag |
| Submission completeness | required planilhas, docs, format, portal fields, signatures | Portal instructions, edital checklist | Submission package, certificate store | deterministic checklist |

## 4. Public And Web Data Lanes

### 4.1 Public Procurement Data

Public procurement data is useful for historical awards, item descriptions,
deadlines, contract values, winners, and sometimes contract amendments.

Likely sources:

- PNCP open data and API surfaces for contratação, atas, and contracts under
  Brazilian public procurement law.
- Compras.gov.br open data API for federal procurement and legacy modules
  covering licitações, pregões, and item-level records.
- Portal da Transparência API for federal licitações and contracts.
- Painel de Compras dashboards for public-procurement lifecycle exploration.

Research tasks:

1. Identify fields available per endpoint: buyer, modality, object, item,
   quantity, unit, winner, value, dates, contract, amendments.
2. Test whether industrial-service keywords retrieve useful examples:
   pintura industrial, jateamento, hidrojateamento, andaime, isolamento,
   manutenção industrial, tratamento de superfície.
3. Compare public award data against Wladimir's private-market categories.
4. Build a public comparable-price corpus, but label it as public-sector only.

Limit:

Public award prices may not reflect Petrobras/Vale/private portal negotiation
behavior. They are market context, not automatic pricing truth.

### 4.2 Private And State-Company Buyer Surfaces

Private portals and state-company supplier systems are less open. The engine
should map them as workflows first, data feeds second.

Likely sources:

- Petrobras Canal Fornecedor and Petronect for supplier registration,
  contracting rules, opportunity surfaces, and families/categories.
- Vale supplier pages and pre-registration flow.
- Eletrobras supplier page and SAP Ariba supplier workflows.
- SAP Ariba sourcing screens, Nimbi, SRM, buyer-specific portals, email, and
  sealed envelope workflows.

Research tasks:

1. Map each buyer's registration and qualification workflow.
2. Record which data is public, login-gated, invitation-only, or manual.
3. Identify the buyer's classification families and service categories.
4. Capture submission mechanics: portal fields, attachments, pricing sheets,
   revision rounds, clarification windows, and technical/commercial split.

Limit:

Private portal data should not be scraped or assumed accessible without lawful
credentials and operator approval. The first engine should support manual
upload/export from the supplier's own portal account.

### 4.3 Cost, Labor, Inflation, And Finance Sources

These sources calibrate cost assumptions and escalation, but they do not
replace company actuals.

Likely sources:

- SINAPI from Caixa/IBGE for construction cost references and indices.
- IBGE SINAPI publication pages and historical tables.
- Banco Central do Brasil SGS API for Selic, IPCA, and other financial series.
- PDET / Novo CAGED / RAIS labor datasets for formal labor market signals,
  occupation/geography trends, and wage context.
- CBIC/CUB dashboards for construction cost context where relevant.

Research tasks:

1. Determine which sources expose APIs vs downloadable files vs dashboards.
2. Map series to engine inputs: financial cost, inflation escalation, regional
   cost context, wage pressure, labor availability, and benchmark sanity checks.
3. Track refresh cadence and regional granularity.
4. Mark which data is benchmark-only and which can safely drive formulas.

Limit:

Industrial painting, blasting, hydrojet, and offshore productivity are highly
site-specific. Public indices should calibrate and sanity-check; internal job
actuals should dominate productivity learning.

### 4.4 Technical Standards And Compliance Sources

The engine needs a standards index, but many standards are copyrighted or
paywalled.

Likely source classes:

- Public NR guidance and labor-safety regulations.
- Buyer technical specifications.
- Contractor method statements.
- Internal estimator doctrine.
- Standards references named inside edital/carta convite.

Research tasks:

1. Build a standards-reference registry that stores identifiers and short
   usage notes, not copyrighted standard text.
2. Classify terms like Sa 2 1/2, ST2, ST3, NR-35, NR-33, QSMS, surface
   condition, galvanized material standard, waste disposal, and inspection.
3. Link standards to proposal sections, cost drivers, and risk flags.

Limit:

Do not copy proprietary standards into the engine. Store references, required
checks, and operator-owned source excerpts only when allowed.

## 5. Organization-Side Data Requirements

The best engine will come from the contractor's private history. Public data
can make the engine useful; org-side data makes it sharp.

### 5.1 Minimum Viable Org Data

| Data Class | Required Fields | Why It Matters |
|---|---|---|
| Company profile | legal name, CNPJ, registrations, service categories, buyer registrations | habilitation and portal readiness |
| Certificate register | document type, expiry date, issuing body, file, status | avoids disqualification |
| Atestado library | buyer, project, service scope, area/quantity, dates, signer, technical wording | atestado fit scoring |
| Equipment register | equipment, capacity, location, availability, rental/owned, maintenance cost | execution feasibility and cost |
| Labor register | roles, rates, availability, local hiring possibility, union/benefit assumptions | direct labor and mobilization |
| Supplier quote library | materials, paints, solvents, equipment rental, validity date, region | cost confidence |
| Historical bids | buyer, object, quantities, submitted price, result, winner if known, revision rounds | win probability and price calibration |
| Job actuals | planned vs actual labor, materials, equipment, productivity, margin, delays | learning loop |
| Buyer feedback | reasons lost/won, clarification questions, negotiation notes | win/loss model |

### 5.2 High-Value Org Data

- Actual productivity by service type, height/access condition, surface
  condition, and permitted work hours
- Actual mobilization and demobilization costs by region/site type
- Maintenance costs by equipment and job duration
- Payment delay history by buyer
- Contract disputes and aditivo outcomes
- Scope variance: buyer quantity vs real executed quantity
- Incumbent/competitor notes by buyer and plant
- Which technical proposal language worked for each buyer type

## 6. Data Model Needed For The Engine

Recommended core entities:

- `BidOpportunity`
- `Buyer`
- `BuyerPortal`
- `BidDocument`
- `ScopeItem`
- `TechnicalRequirement`
- `ContractRisk`
- `HabilitationRequirement`
- `CompanyCredential`
- `AtestadoTecnico`
- `SiteVisitObservation`
- `CostComposition`
- `ProductivityAssumption`
- `PriceScenario`
- `ClarificationQuestion`
- `TechnicalProposalSection`
- `SubmissionChecklist`
- `NegotiationRound`
- `BidOutcome`
- `JobActual`

The model should keep source provenance on every extracted fact:

- source document or URL
- page/paragraph/cell/field
- extraction date
- confidence
- operator confirmation status
- freshness/expiry where relevant

## 7. Engine Modules To Research And Rank

Rank modules by impact on profitable, qualified bids.

### Tier 1 - Must Exist

1. Source-of-truth extractor for edital, carta convite, portal invitation, and
   buyer emails
2. Bid/no-bid risk preflight
3. Habilitation and atestado readiness checker
4. Technical clarification question generator
5. Site-visit checklist and assumption register
6. Cost-composition and price-scenario model
7. Submission completeness checker

### Tier 2 - Differentiators

1. Public comparable-award search
2. Buyer/portal workflow adapter
3. Incumbent and competitor intelligence
4. Payment-term and cash-flow risk calculator
5. Negotiation-round risk ledger
6. Technical-proposal quality scorer

### Tier 3 - Learning Loop

1. Win/loss model
2. Actual-vs-budget variance model
3. Productivity calibration by service and site condition
4. Buyer-specific pricing and risk memory
5. Aditivo and scope-variance predictor

## 8. Research Questions

The research route should answer these questions before implementation:

1. Which public procurement sources expose item-level service quantities and
   award prices reliably enough for comparable pricing?
2. How far can PNCP/Compras.gov.br/Transparência data get us for industrial
   services before private-buyer data becomes necessary?
3. Which buyer portals allow lawful export/manual collection of opportunity
   data by the supplier?
4. Which fields are common across Petrobras, Vale, ArcelorMittal, CSN,
   Eletrobras, Nimbi, SRM, Ariba, and email/envelope workflows?
5. What is the minimum org-data intake form that creates useful predictions
   after 10, 25, and 100 historical bids?
6. Which metrics can be validated immediately and which need long-term labels?
7. What does the engine do when no site visit is possible?
8. How should the system price or block impossible aditivo conditions?
9. How should payment terms alter price and bid/no-bid?
10. What is the evidence threshold for recommending "no-bid"?

## 9. Validation Plan

### Phase A - Source Feasibility

Build a source matrix with:

- source name
- URL/API
- authority class
- accessible fields
- refresh cadence
- access constraints
- sample industrial-service queries
- reliability notes

Pass condition:

- at least one public procurement source yields relevant industrial-service
  examples with object, dates, buyer, and award/value fields
- at least one buyer portal workflow is mapped as manual/upload compatible
- every source is labeled public API, public dashboard, login-gated,
  invitation-only, paid/private, or manual-only

### Phase B - Metric Obtainability

For each optimization metric, prove:

- required input fields
- direct source or org-side collection method
- fallback proxy
- refresh cadence
- validation label

Pass condition:

- no primary objective lacks an obtainable data path

### Phase C - Org Intake Prototype

Design the minimum org intake package:

- company documents
- atestados
- certificate register
- equipment/labor register
- historical bid sheet
- job actuals sheet
- buyer/competitor notes

Pass condition:

- a contractor can seed the engine without needing a complex ERP integration

### Phase D - First Scoring Prototype

Prototype scorecards:

- bid/no-bid score
- scope clarity score
- habilitation readiness
- cost confidence
- cash-flow risk
- technical proposal completeness
- submission completeness

Pass condition:

- every score explains which facts drove it and which missing facts would
  change the recommendation

## 10. Stop Conditions

Stop or defer if:

- the research cannot identify lawful data-access paths for private portals
- optimization metrics lack input fields or labels
- org data required is too burdensome for an old-school contractor to provide
- public data is too sparse to support pricing claims
- the engine would recommend prices without site-visit assumptions or explicit
  exclusions
- the strategy drifts into generic grant/proposal writing instead of industrial
  bid-response mechanics

## 11. Near-Term Research Deliverables

1. `public_data_source_matrix.md`
2. `org_data_intake_schema.md`
3. `optimization_metric_ledger.md`
4. `industrial_bid_entity_model.md`
5. `buyer_portal_workflow_matrix.md`
6. `first_scorecard_wireframe.md`
7. `evidence_boundary_report.md`

## 12. Source Seeds

These are initial public source candidates identified during strategy creation.
They require a deeper field-level source-feasibility pass before use in any
engine.

- PNCP Dados Abertos:
  `https://www.gov.br/pncp/pt-br/acesso-a-informacao/dados-abertos`
- Compras.gov.br Dados Abertos:
  `https://dadosabertos.compras.gov.br/`
- Portal da Transparência API de Dados:
  `https://portaldatransparencia.gov.br/api-de-dados`
- Painel de Compras:
  `https://paineldecompras.economia.gov.br/`
- Petrobras Canal Fornecedor:
  `https://canalfornecedor.petrobras.com.br/`
- Petronect:
  `https://www.petronect.com.br/`
- Vale Fornecedores:
  `https://vale.com/pt/fornecedores`
- Eletrobras Fornecedores / SAP Ariba:
  `https://www.eletrobras.com/pt/Paginas/Fornecedores.aspx`
- SINAPI Caixa:
  `https://www.caixa.gov.br/poder-publico/modernizacao-gestao/sinapi/Paginas/default.aspx`
- SINAPI IBGE:
  `https://www.ibge.gov.br/estatisticas/economicas/precos-e-custos/9270-sistema-nacional-de-pesquisa-de-custos-e-indices-da-construcao-civil.html`
- Banco Central Dados Abertos / SGS:
  `https://dadosabertos.bcb.gov.br/`
- PDET / Novo CAGED / RAIS:
  `https://www.gov.br/trabalho-e-emprego/pt-br/assuntos/estatisticas-trabalho`

