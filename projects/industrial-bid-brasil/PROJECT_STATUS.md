# Project Status

## Snapshot

- Project: Industrial Bid Brasil
- Path: `/home/vrondelli/projects/domainspec-core/projects/industrial-bid-brasil`
- Status: seed package created
- Date: 2026-06-11
- Owner context: separate project under `domainspec-core/projects`
- Runtime status: no application runtime yet

## What Exists

- Wladimir questionnaire artifact copied from GoldenQuill exploration.
- Wladimir intelligence extraction copied from GoldenQuill exploration.
- Research strategy and dispatch copied from GoldenQuill exploration.
- Invoke define/design/plan seed package created for this standalone project.
- Data templates created for minimum viable organization data.

## What Does Not Exist Yet

- No production scoring engine.
- No parser for edital, carta convite, portals, planilhas, or contracts.
- No database.
- No private portal connector.
- No automated public-data ingestion.
- No validated pricing formulas.

## Current Product Question

Can Wladimir's industrial bidding doctrine be encoded into a local-first engine
that helps a contractor decide whether to bid, what to ask, what data is missing,
how confident the price is, and whether the submission package is complete?

## Immediate Next Step

Execute L0 from [docs/product/WORK-PACK.md](docs/product/WORK-PACK.md):

1. Normalize seed data templates.
2. Build a local JSON opportunity schema.
3. Implement deterministic bid/no-bid and confidence scorecards.
4. Validate with the Wladimir seed example.

## Decision Log

| Date | Decision |
| --- | --- |
| 2026-06-11 | Create this as a separate project instead of mixing it into GoldenQuill. |
| 2026-06-11 | Keep GoldenQuill artifacts as seed evidence, but let this project own Brazil industrial bidding logic. |
| 2026-06-11 | Start with deterministic scorecards and private organization data before public-data automation. |
