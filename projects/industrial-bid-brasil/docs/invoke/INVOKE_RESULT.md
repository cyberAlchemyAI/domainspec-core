# Invoke Result

- Mode: plan
- Spell: invoke
- Canonical ID: invoke
- Scope: library
- Phase status: pass
- Mode contract: `/home/vrondelli/projects/domainspec-core/arcanum/spells/invoke/plan.md`
- Define contract: `/home/vrondelli/projects/domainspec-core/arcanum/spells/invoke/define.md`
- Design contract: `/home/vrondelli/projects/domainspec-core/arcanum/spells/invoke/design.md`
- Target artifact: Industrial Bid Brasil seed package
- Target artifact type: neutral project seed
- Target owner: `/home/vrondelli/projects/domainspec-core/projects/industrial-bid-brasil`

## Outputs

- [README.md](../../README.md)
- [PROJECT_STATUS.md](../../PROJECT_STATUS.md)
- [MVP_SPEC.md](../product/MVP_SPEC.md)
- [DATA_REQUIREMENTS.md](../product/DATA_REQUIREMENTS.md)
- [SCORING_MODEL.md](../product/SCORING_MODEL.md)
- [IMPLEMENTATION-LAYERING.md](../product/IMPLEMENTATION-LAYERING.md)
- [WORK-PACK.md](../product/WORK-PACK.md)
- [data_templates](../../data_templates)

## Context Summary

The seed package was invoked from the GoldenQuill exploration of Brazil
industrial bid participation. The source evidence includes:

- Wladimir Cardoso de Lima's questionnaire response.
- The generated questionnaire HTML.
- A distilled intelligence memo from Wladimir's answers.
- A research strategy for public/web data and organization-side data.
- Prior inspection of an industrial orçamento workbook and bidding model
  document from Wladimir's files.

## Template / Profile Selection

- Profile: neutral project seed, not sigil or spell lifecycle.
- Companion templates: implementation-layering and work-pack.
- Complexity: medium, because the project crosses product design, data
  templates, scoring logic, and future runtime work.
- Output mode: single-file plan artifacts with no split task files yet.

## Design Views

| View | Coverage |
| --- | --- |
| Context | Brazil industrial bidding, private and public procurement, Wladimir source intelligence. |
| High-level structure | Opportunity intake, data registers, scorecards, cost confidence, submission checklist. |
| Low-level components | CSV templates, scorecard inputs, required fields, validation checks. |
| Workflow process | Intake -> extraction -> bid/no-bid -> questions -> habilitation -> cost confidence -> proposal/submission. |
| Decision flow | Proceed, clarify, site-visit required, no-bid, blocked. |
| Dependency interface | Public data lanes, private org data, local estimator review, future parser/connectors. |

## Decisions

- Create a separate project under `domainspec-core/projects`.
- Use `industrial-bid-brasil` as the seed slug.
- Transfer GoldenQuill exploration artifacts as source evidence, not as runtime
  code.
- Start with deterministic, explainable scorecards.
- Make private organization data the primary learning source; public web data is
  context and calibration.

## Unresolved Gaps

- Final product name is not locked.
- No customer organization has supplied real bid history yet.
- No runtime data store has been selected.
- No public-source connector has been validated.
- Pricing formulas remain seed rules until tested against actual jobs.

## Next Route

`task-session` against [../product/WORK-PACK.md](../product/WORK-PACK.md), starting
with `SWU-IBB-001`.
