# Project Decisions

## Purpose

Capture project-level decisions that must be resolved before feature-level planning and pipeline execution.

## Decision Register

| ID     | Decision                         | Options Considered                                                                       | Selected Option                                                                          | Status   | Scope   | Rationale                                                                                  | Source              | Date       |
| ------ | -------------------------------- | ---------------------------------------------------------------------------------------- | ---------------------------------------------------------------------------------------- | -------- | ------- | ------------------------------------------------------------------------------------------ | ------------------- | ---------- |
| PD-001 | Scope boundary for first rollout | A) onboarding only; B) onboarding + dashboard; C) onboarding + dashboard + payment links | C) onboarding + operations dashboard + payment-link management                           | selected | project | This is the smallest slice that demonstrates central/vendor/submerchant operational value. | discovery interview | 2026-05-01 |
| PD-002 | Initial delivery slice           | A) broad hierarchy with many rails; B) constrained hierarchy and one rail                | B) central -> vendor -> submerchant with PIX-only links in v1                            | selected | project | Constrains complexity while matching current operating model.                              | discovery interview | 2026-05-01 |
| PD-003 | Source-of-truth policy           | A) code-first; B) docs-first; C) mixed by team                                           | B) docs-first for behavior contracts, code must align before merge                       | selected | project | DomainSpec workflow requires explicit contracts before implementation scaling.             | start command seed  | 2026-05-01 |
| PD-004 | Migration strictness             | A) strict everywhere; B) strict for financial behavior, tolerant for naming/structure    | B) strict for monetary, commission, and settlement behavior; tolerant for naming cleanup | selected | project | Preserves correctness where drift has highest business risk.                               | start command seed  | 2026-05-01 |
| PD-005 | Verification baseline command    | A) unit tests only; B) tests + lint + typecheck; C) add e2e in baseline                  | B) `npm test && npm run lint && npm run typecheck`                                       | selected | project | Minimal reliable gate before progressing features in implementation phase.                 | start command seed  | 2026-05-01 |
| PD-006 | Settlement cadence strategy      | A) fixed global cadence; B) configurable by tenant; C) manual close only                 | B) configurable by tenant using approved presets                                         | selected | project | Different vendors have different operating rhythms and close needs.                        | discovery interview | 2026-05-01 |
| PD-007 | Commission model for v1          | A) dynamic rule engine; B) fixed percentage by level; C) hybrid                          | B) fixed percentage by hierarchy level                                                   | selected | project | Predictability and implementation speed are higher for the initial release.                | discovery interview | 2026-05-01 |
| PD-008 | Payment methods in v1            | A) cash + card + PIX; B) PIX only; C) card only                                          | B) PIX only                                                                              | selected | project | Single rail reduces integration and reconciliation complexity in the first cycle.          | discovery interview | 2026-05-01 |

## Required Startpoint Decisions

| Key                           | Decision Prompt                                                                | Example Resolution                                                                                     | Status   |
| ----------------------------- | ------------------------------------------------------------------------------ | ------------------------------------------------------------------------------------------------------ | -------- |
| scope-boundary                | What is in scope and explicitly out of scope for the first rollout?            | In: onboarding, operations dashboard, payment links. Out: full POS device lifecycle and non-PIX rails. | selected |
| initial-delivery-slice        | What is the smallest valuable delivery slice?                                  | central -> vendor -> submerchant with PIX links and tenant cadence presets.                            | selected |
| source-of-truth-policy        | In brownfield, which source is authoritative when docs and code diverge?       | Docs are behavior authority; code must align or docs update before merge.                              | selected |
| migration-strictness          | How strict should migration from current state to DomainSpec be in this cycle? | Strict for financial behavior, tolerant for naming and structure cleanup.                              | selected |
| verification-baseline-command | What command set defines minimum verification before feature progression?      | `npm test && npm run lint && npm run typecheck`                                                        | selected |

## Blockers

| ID  | Blocking Decision | Why Blocked | Owner | Next Action | Target Date |
| --- | ----------------- | ----------- | ----- | ----------- | ----------- |
| -   | None currently    | -           | -     | -           | -           |

## Notes

- Use `status: blocked` for decisions that prevent startpoint or pipeline progression.
- Convert blocked decisions to selected as soon as evidence is available.
- Keep rationale concise and evidence-linked when possible.

## Change Log

| Date       | Change                                                                 | Author                  |
| ---------- | ---------------------------------------------------------------------- | ----------------------- |
| 2026-05-01 | Initial project decisions created                                      | domainspec-orchestrator |
| 2026-05-01 | Discovery interview decisions applied for v1 scope and operating model | domainspec-orchestrator |
