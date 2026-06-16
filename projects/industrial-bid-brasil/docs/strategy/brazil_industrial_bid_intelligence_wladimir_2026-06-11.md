---
title: Brazil Industrial Bid Intelligence - Wladimir Cardoso de Lima
date: 2026-06-11
source: Questionnaire response from Wladimir Cardoso de Lima
status: exploration
related_artifact: docs/strategy/brazil_industrial_bid_questionnaire.html
---

# Brazil Industrial Bid Intelligence - Wladimir Cardoso de Lima

This note distills Wladimir Cardoso de Lima's questionnaire response into an
operating model for a possible Brazil industrial bid-response variant of
Golden Quill / Tilth. It is exploratory source intelligence, not a locked
product spec.

## 1. Domain Boundary

The relevant work is not generic proposal writing. It is industrial bid
participation for large Brazilian buyers and institutional procurement.

Primary service domains:

- Industrial painting
- Abrasive blasting / jateamento
- Hydrojetting / hidrojato
- Scaffolding and access
- Insulation
- Industrial maintenance
- Offshore services

Primary buyer sectors:

- Petrobras / oil and gas
- Vale / mining
- CSN / steel
- ArcelorMittal / steel
- Energy / hydroelectric
- Ports / naval
- Private companies
- Government / institutions

## 2. Native Workflow

The Brazil industrial workflow maps closely to the existing Tilth logic, but
with different source documents, review criteria, and costing surfaces.

Equivalent chain:

```text
Edital / carta convite / portal invitation
-> bid/no-bid decision
-> scope and contract review
-> technical questions to buyer
-> site visit / technical visit
-> habilitation documents
-> cost composition and price scenario
-> technical proposal
-> commercial proposal
-> portal / envelope submission
-> 2-3 price revision rounds
```

The "RFA is source of truth" equivalent is:

- Contract object
- Technical specification
- service quantities
- draft contract
- execution deadline
- payment terms
- site-visit observations

## 3. Bid / No-Bid Logic

Wladimir's minimum positive signals:

- Clear scope
- Executable deadline

Primary reasons to stop before pricing:

- Impossible deadline
- Confusing scope
- High penalty / multa alta

Implication for system design:

The first machine pass should not draft. It should classify the opportunity as:

- proceed
- proceed with technical questions
- proceed only after site visit
- likely no-bid
- blocked by contract / penalty / scope ambiguity

## 4. First Reading Priority

The first part read is the object / scope of the contract.

Critical first alerts:

- Object of contract
- service quantities
- short deadline
- high penalties
- difficult mobilization

System rule:

The first extraction screen should show "Objeto do contrato" and
"Quantitativos dos serviços" before anything else. If the object and quantities
are unclear, the system should halt and ask for clarification instead of
continuing into price composition.

## 5. Buyer Questions

The system should learn to generate buyer-clarification questions before final
pricing. Wladimir's example questions:

1. Is final disposal of waste generated during service execution the client's
   responsibility or the contractor's responsibility?
2. Is hydrojetting with abrasive conventional?
3. What standards apply to hot-dip galvanized hardware materials?
4. What is the condition of the surfaces of the metallic structures to be
   treated?

Reusable question classes:

- Waste disposal responsibility
- Method definition
- material standard
- actual surface condition
- scope/quantity ambiguity
- access/mobilization uncertainty
- responsibility split between buyer and contractor

## 6. Habilitation Risk

Common documents:

- Social contract / corporate registration
- CNPJ and registrations
- negative certificates
- technical attestations

Highest-friction document:

- Technical attestations / atestados técnicos

System implication:

The Brazil variant needs a "habilitation readiness" preflight. Technical
attestations should be treated as a high-risk eligibility artifact, not a
simple attachment. The system should compare:

- service scope required by buyer
- service scope proven in attestations
- buyer's minimum experience requirement
- whether the attestation language matches the bid object

## 7. Site Visit Logic

Wladimir says the technical visit almost always changes price.

Site visit observations that matter:

- Real area
- height / access
- interference with plant operation
- permitted working hours
- mobilization and transport

Highest-cost scope error:

- Difference between buyer-provided scope and real scope to be executed

System rule:

If the bid includes field execution and the technical visit is possible, the
machine should flag "price confidence is low until site-visit facts are
captured." If there is no site visit, the proposal should include explicit
assumptions and exclusions.

## 8. Cost Composition Model

Core cost blocks:

- Direct labor
- social charges
- benefits / food / transport
- consumable materials
- paints / solvents
- equipment
- indirect costs
- taxes
- margin / risk

Productivity is driven by:

- height
- access

Frequently forgotten costs:

- mobilization
- maintenance

Margin is driven by:

- technical risk
- payment terms
- possibility of addendum / aditivo

System implication:

The budget engine should not just total a spreadsheet. It should maintain a
risk-aware price narrative:

- What drives productivity?
- What is assumed about access?
- What mobilization costs are included?
- What maintenance costs are included?
- What payment term affects financial cost?
- Is there realistic aditivo room or is scope locked?

## 9. Technical Proposal Logic

A strong technical proposal must show:

- Understanding of scope
- execution method
- schedule
- equipment
- safety plan
- quality control
- previous experience

Important technical terms and norms mentioned:

- Sa 2 1/2
- ST2
- ST3
- NR-35
- NR-33
- QSMS / OSMS as written in response

Wladimir's distinction between strong and weak proposal:

- execution deadline
- payment conditions

System implication:

The technical proposal should not be treated as decorative text. It is a
risk-control artifact that proves the contractor understands execution,
schedule, safety, quality, equipment, and prior experience.

## 10. Negotiation Logic

Expected private-buyer price revision rounds:

- 2 to 3 rounds

Wladimir does not lower price without clarifying risk.

Hard negotiation boundary:

- bad payment conditions

System rule:

When buyer requests a discount, the system should first surface a risk ledger,
not merely suggest margin cuts. Discount analysis should ask:

- Which risk remains unclear?
- Which assumptions can be changed?
- Which exclusions must be written?
- Does payment timing create financial cost?
- Is the price reduction below acceptable risk?

## 11. Submission Channels

Observed channels:

- Nimbi
- SRM
- Ariba
- email
- sealed physical envelope

Eliminating submission error:

- incomplete spreadsheet / planilha incompleta

System implication:

Portal adapters matter, but the first durable adapter is a submission
checklist. Before sending, the system should validate:

- complete price sheet
- required attachments present
- correct technical/commercial split
- signatures
- file naming
- deadlines
- physical envelope requirements when applicable

## 12. Market Intelligence

Companies observed in the market:

- Conami
- Reframax
- Ecoblast
- Manserv
- Kaefer-Rip
- Promar
- Grupo Refratech
- Priner

Signal of a strong competitor:

- competitor has the current contract

System implication:

Competitive assessment should track incumbency. A competitor with the current
contract likely has site familiarity, buyer relationship, operational history,
and better real-cost knowledge.

## 13. Five Rules For A Young Estimator

Wladimir's five rules:

1. Read the technical specification carefully.
2. Always check the draft contract.
3. Check whether a technical visit is possible.
4. Check whether labor can be hired locally at the job site.
5. Pay attention when assembling the technical proposal.

These five rules are the seed of the Brazil industrial estimator doctrine.

System doctrine:

Before building price, the system should prove these five checks have been
answered.

## 14. Critical Story

Failure pattern:

The contractor accepted the buyer-provided scope. During execution, the real
scope was much larger, and there was no possibility of contract addendum.

Core lesson:

Never price solely from buyer-provided scope when real-field conditions may
expand execution. If addendum is impossible, scope uncertainty must be priced,
excluded, clarified, or treated as no-bid risk.

## 15. Product Implications For Brazil Variant

Recommended exploratory modules:

1. Edital / carta convite source-of-truth extractor
2. Bid/no-bid and risk preflight
3. Buyer clarification question generator
4. Site-visit checklist and assumption register
5. Habilitation document readiness checker
6. Technical attestation scope matcher
7. Industrial cost-composition model
8. Technical proposal builder
9. Commercial proposal and price-sheet checker
10. Price revision / negotiation risk ledger
11. Portal and envelope submission checklist
12. Competitor/incumbent intelligence register

## 16. Fit With Existing Golden Quill Logic

The operating logic is close to Tilth:

- source document is authoritative
- operator brings the substance
- extracted facts must be traced
- drafting follows after eligibility and evidence checks
- budgets need assumptions and supporting detail
- final package must match submission channel requirements

The main difference is the review lens:

- Tilth grants ask: can this applicant prove eligibility, fit, outcomes, budget,
  and compliance against a funder?
- Brazil industrial bids ask: can this contractor qualify, price the service,
  control execution risk, submit a complete package, and survive negotiation
  without losing money?

## 17. Next Exploration Questions

Follow-up questions should go deeper into:

- How technical attestations are judged
- exact price-sheet formats by buyer/portal
- how taxes and social charges vary by contract type
- how payment terms affect price
- how to write exclusions without weakening the proposal
- how site-visit findings change productivity
- how to classify addendum possibility
- how to detect when incumbent advantage makes a bid unlikely
- differences between Petrobras, Vale, CSN, ArcelorMittal, and private portals
- minimum viable industrial service library: painting, blasting, hydrojet,
  scaffolding, insulation

