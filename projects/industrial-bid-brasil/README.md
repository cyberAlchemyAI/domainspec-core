# Industrial Bid Brasil

Industrial Bid Brasil is a seed project for a Brazil-focused industrial
bidding engine. It starts from Wladimir Cardoso de Lima's 30+ years of
industrial bidding experience and turns that expertise into a governed product
baseline: bid/no-bid logic, edital and carta convite extraction, technical
questions, habilitation readiness, cost confidence, risk-aware pricing, and
submission completeness.

This project is separate from GoldenQuill. GoldenQuill remains the grant and
proposal system context; this project owns the Brazil industrial bidding domain.

## Current Status

- Status: invoked seed package
- Date: 2026-06-11
- Phase: define/design/plan baseline
- Runtime: none yet
- Next route: task-session against [docs/product/WORK-PACK.md](docs/product/WORK-PACK.md)

## Seed Artifacts

- [Questionnaire](docs/strategy/brazil_industrial_bid_questionnaire.html)
- [Wladimir intelligence extraction](docs/strategy/brazil_industrial_bid_intelligence_wladimir_2026-06-11.md)
- [Research strategy](docs/strategy/brazil_industrial_bid_research_strategy_2026-06-11.md)
- [Research dispatch](docs/strategy/brazil_industrial_bid_research_dispatch_2026-06-11.json)
- [Invoke result](docs/invoke/INVOKE_RESULT.md)
- [MVP spec](docs/product/MVP_SPEC.md)
- [Data requirements](docs/product/DATA_REQUIREMENTS.md)
- [Scoring model](docs/product/SCORING_MODEL.md)
- [Implementation layering](docs/product/IMPLEMENTATION-LAYERING.md)
- [Work-pack](docs/product/WORK-PACK.md)

## Domain Boundary

The engine targets industrial service bidding in Brazil, especially:

- pintura industrial
- jateamento
- hidrojato
- andaime and access
- isolamento
- manutencao industrial
- offshore service work

Primary buyer contexts include Petrobras, Vale, CSN, ArcelorMittal, energy,
ports, private companies, and government/institutional procurement.

## Product Thesis

The engine should optimize a contractor's chance of submitting a complete,
qualified, technically credible, correctly priced bid that can survive execution
and negotiation without destroying margin.

The first machine job is not drafting. The first job is deciding whether the
opportunity is bid-worthy, what is missing, and which risks must be clarified
before price is trusted.

## Seed Rules

1. Always read object, quantities, technical specification, draft contract,
   execution deadline, and payment terms before pricing.
2. Treat atestados tecnicos as a high-risk habilitation artifact.
3. Treat site visits as price-changing evidence for field execution.
4. Flag mobilization and maintenance as frequently forgotten costs.
5. Never cut price in negotiation without naming the risk being accepted.

## Data Templates

The first data templates live under [data_templates](data_templates). They are
header-first templates for collecting organization data before an app exists.

## Next Build

Use [docs/product/WORK-PACK.md](docs/product/WORK-PACK.md) as the execution
entrypoint. The first implementation slice should create a local, file-backed
prototype that can load one opportunity, one company profile, one certificate
register, one atestado library, and one cost assumption set, then produce a
bid/no-bid and risk-confidence report.
