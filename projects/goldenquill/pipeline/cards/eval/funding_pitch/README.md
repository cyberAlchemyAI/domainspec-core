# Funding pitch — the study itself is fundable work

## The meta-loop

Per operator directive 2026-05-15 PM: paying expert reviewers requires funding. The expert-reviewer study is itself a grantable research project. **Tilth applies for funding to evaluate Tilth.**

This closes a satisfying loop: Tilth's own grant-finder + grant-writer skills dogfood themselves to fund the study that empirically evaluates whether Tilth's Card System measurably helps grant-writing outcomes.

## Probable CLC matches

The study's funding pitch maps cleanly to multiple CLCs:

- **`research_evidence` (TILTH-CLC-04)** — formal evaluation study with defined methods, IRB-equivalent considerations, sample-size analysis, blinded peer review, pre-registration discipline, public results.
- **`catalytic_change` (TILTH-CLC-02)** — demonstration / proof-of-concept of a new approach (card-driven grant-writing intelligence) with theory of change, leverage plan, replication pathway, field-learning agenda.
- **`market_access` (TILTH-CLC-05)** — could frame as commercialization-readiness evidence for the Golden Quill product line if pitched to SBIR Phase I or EDA Build to Scale.

## Probable funder types

- Federal research grants — NSF (CISE, EHR program evaluation, science of science strands), USDA SARE evaluation strands, USDA AFRI Education + Workforce Development program.
- Foundation innovation funds — MacArthur Foundation 100&Change, Ford Foundation BUILD, Schmidt Futures, climate-tech foundations (ClimateWorks, Bezos Earth Fund's tech wing), philanthropy-research intermediaries (Center for Effective Philanthropy, Bridgespan).
- Field-building intermediaries — community-development sector evaluation funders, agriculture-research intermediaries, food-systems-philanthropy intermediaries.
- SBIR / STTR — Phase I research demonstration if framed as small-business-research evaluation of a novel grant-writing-intelligence system.

## Dogfooding application

Tilth's grant-finder skill produces a funder shortlist for this study as its own dogfooded use case. Tilth's grant-writer skill drafts the application(s). The resulting applications are themselves test cases for the card layer:

- Arm A version of the application (Tilth-without-cards) ships to one funder.
- Arm B version (Tilth-with-cards) ships to another funder.
- Arm C version (frontier LLM rudimentary prompt) is generated but typically not submitted.

Win-rate delta between the Arm A funder application and the Arm B funder application becomes one data point in the larger study. (Caveat: n=1 per arm, and funders + opportunities differ; informational only, not decisive.)

## Status at v7.0.11 LOCK candidate

Funding pitch authoring deferred to v0.2 first wave. This README scaffold lands at v0.2 LOCK so the funding-pitch workspace exists when scenario design + reviewer-panel recruitment land.

## What goes here at v0.2 first wave landing

- `funder_shortlist_<date>.yaml` — grant-finder skill output.
- `application_<funder_slug>_<opportunity_id>/` — full application package per funder.
- `decision_log.md` — operator decisions on which funders to apply to, which to skip, which to defer.
- `submission_receipts/` — funder portal submission confirmations + grant.gov receipts.
- `award_decisions/` — funder award/decline/withdrawal notifications.
