---
org: FIT Farms
canonical_entity_name: FIT Farms LLC
role_label: client
sectors: food_ag, community_dev, arts
active_version: v1-demo
for_profit: true
flagship_project: Golden Quill
paired_operator_folder: orgs/fit_farms_commons/
demo_fixture: true
demo_origin: orgs/fit_farms/PROJECT_CONTEXT.md (snapshot 2026-05-01 — trimmed for demo deterministic bytes)
---

# FIT Farms — PROJECT_CONTEXT (Demo Driver Snapshot)

This is a deterministic-bytes snapshot consumed by `tests/demo/test_demo_driver.py`. It is shaped after the live `orgs/fit_farms/PROJECT_CONTEXT.md` but trimmed and pinned to keep the demo run reproducible. The live file is canonical for grant work; this fixture is canonical for the demo pipeline regression.

## Entity Information
- **Legal Name:** FIT Farms LLC
- **Entity Type:** For-profit LLC
- **Nonprofit status:** No (501(c)(3) NOT applicable; for-profit producer entity).
- **State of Incorporation:** PA
- **EIN:** 12-3456789
- **UEI (SAM.gov):** [NEEDED]
- **SAM.gov Registration Status:** [NEEDED]
- **Flagship Project:** Golden Quill — regenerative grant intelligence

## Location
- **Address:** [REDACTED — operator on file]
- **County:** Allegheny
- **State:** PA
- **Urban/Rural Designation:** Urban
- **Congressional District:** [NEEDED]

## Mission

FIT Farms is the umbrella organization stewarding farms, mycology, and food-justice initiatives in the Pittsburgh region. It builds hydroponic and mushroom production systems, delivers horticultural-therapy and maker-space programming to underserved populations, and stewards Pittsburgh's oldest herb farm in transition to protected green space.

## Sectors

- **food_ag** — mushroom and herb production, hydroponics
- **community_dev** — food justice, horticultural therapy, youth education, green-space stewardship
- **arts** — maker-space programming

## Leadership

- **Josh Inklovich — Founder / Chief Servant Leader (2015–present)**
  - 25+ years project management in skilled trades and workforce development
  - Co-founder, MycoSymbiotics Cooperative
  - Board member, Mycofest (12 years running)
  - Helped design Pennsylvania's wild mushroom foraging certification program

## VAPG-Relevant Production & Capacity

- Hydroponic and mushroom production systems on multiple Pittsburgh-area sites
- Stewardship of Healcrest — Pittsburgh's oldest herb farm
- Outdoor mushroom + vertical-garden build at Mystic Mamas (Allentown)
- Indoor hydroponic + mushroom grow build with Abiding Missions
- Production-systems consultant to Inoculated Farms (NJ) — 1,500 lbs/week scale

## Partnerships

- MycoSymbiotics Cooperative (co-founder)
- Mycofest (board member, 12+ years)
- Inoculated Farms (production-systems consultant)
- Mystic Mamas, Abiding Missions, Bloomfield Garfield Corporation
- Allegheny Land Trust, Goodwill of SWPA, Passport Academy Charter School
- Voices Against Violence, IdeaFoundry (portfolio company relationship)

## Prior Grant Experience

- Goodwill Industries Power of Work award (FIT Inc., 2013–2017 era)
- Three competitive 2026 wins (operator portfolio; specific routing per `orgs/fit_farms/grants/`)

## Boilerplate — Short (50 words)

FIT Farms is a Pittsburgh-based umbrella organization stewarding farms, mycology, and food-justice initiatives. Founded in 2015, it has built hydroponic classrooms in charter schools, delivered horticultural therapy to elderly and disabled participants, and transitioned Pittsburgh's oldest herb farm into protected green space.

## Demo Notes

This snapshot deliberately omits the [NEEDED] fields that would block a real submission. Demo Driver tests do NOT submit; they prove the pipeline composes end-to-end with realistic input bytes. Fields marked [NEEDED] in the live file are also marked here — the demo path exercises Logician PRE-gate behaviour when those fields are absent (Law 5 substance check).
