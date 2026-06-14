---
docType: non-strict-coding-node-selection
status: active
updatedAt: 2026-06-13
dispatch: NON-STRICT-CODING-INVOKE.dispatch.json
source: Craft ledger sweep across 12 workspace ledgers
---

# Non-Strict-Coding Node Selection

## Purpose

This package records the Craft -> Dispatch Spec -> Invoke strategy for Golden Quill
nodes whose next useful movement is canonical authoring, not immediate code mutation.

The output is one `INVOKE-DEVELOPMENT.md` artifact per selected node. Each artifact
contains the current define/design/plan surface for that node and preserves a hard
boundary between planning/spec work and later implementation.

## Selection Rule

A node is selected when its immediate work is one or more of:

- governance or canon ratification;
- operating procedure, playbook, checklist, or service wrapper;
- staffing, budget, trigger, sales, legal, or finance planning;
- test/proof specification before executable tests exist;
- hardware or image procedure definition before scripts or field execution;
- parent recomposition of child work.

A node is excluded from this batch when its next movement is primarily runtime code,
feature implementation, or mutation-capable engineering.

## Selected Nodes

| Node | Ledger | Why selected | Canonical artifact |
| --- | --- | --- | --- |
| boundary-and-canon | `docs/strategy/development/boundary-and-canon/.craft/ledger.yml` | Governance/canon decisions, posture vocabulary, and UI phase treatment. | `docs/strategy/development/boundary-and-canon/INVOKE-DEVELOPMENT.md` |
| hardware-golden-image | `docs/features/hardware-golden-image/.craft/ledger.yml` | Hardware/image procedure specs and receipt contracts precede any scripts or field execution. | `docs/features/hardware-golden-image/INVOKE-DEVELOPMENT.md` |
| quality-security-proof | `docs/features/quality-security-proof/.craft/ledger.yml` | Proof/test matrix, claims register, security-review assignment, and instrumentation definitions. | `docs/features/quality-security-proof/INVOKE-DEVELOPMENT.md` |
| capital-logic-library | `docs/features/capital-logic-library/.craft/ledger.yml` | Card schema, rule-pack governance, launch-card authoring, and expert-review coordination. | `docs/features/capital-logic-library/INVOKE-DEVELOPMENT.md` |
| sales-contracting-legal | `docs/strategy/development/sales-contracting-legal/.craft/ledger.yml` | Sales materials, LOI/agreement/data-policy planning, and bookkeeper trigger. | `docs/strategy/development/sales-contracting-legal/INVOKE-DEVELOPMENT.md` |
| white-glove-delivery-node-care | `docs/strategy/development/white-glove-delivery-node-care/.craft/ledger.yml` | Service-wrapper playbook, Day-60 template, and CS/field-tech transition checklist. | `docs/strategy/development/white-glove-delivery-node-care/INVOKE-DEVELOPMENT.md` |
| company-operations-finance | `docs/strategy/development/company-operations-finance/.craft/ledger.yml` | Operating checklists, support triage, Node Care cadence, and validation packet ownership. | `docs/strategy/development/company-operations-finance/INVOKE-DEVELOPMENT.md` |
| staffing-budget-and-triggers | `docs/strategy/development/staffing-budget-and-triggers/.craft/ledger.yml` | Hours/rates scaffold, onboarding triggers, and role-cost decisions. | `docs/strategy/development/staffing-budget-and-triggers/INVOKE-DEVELOPMENT.md` |
| after-acceleration-roadmap | `docs/strategy/development/after-acceleration-roadmap/.craft/ledger.yml` | Post-capital sequencing, stage gates, repeatability proof, and service-pilot decisions. | `docs/strategy/development/after-acceleration-roadmap/INVOKE-DEVELOPMENT.md` |
| node-on-desk-readiness | `docs/strategy/development/node-on-desk-readiness/.craft/ledger.yml` | Parent recomposition surface that binds child receipts into node-on-desk readiness. | `docs/strategy/development/node-on-desk-readiness/INVOKE-DEVELOPMENT.md` |

## Excluded From This Batch

| Node | Reason |
| --- | --- |
| tilth-runtime-build | Strict runtime implementation node. It should consume canon/procedure outputs from this batch, then route through an implementation work-pack. |
| root promotion-governance Craft ledger | Already has a build spec and handoff for the L0 learning-loop spine; next work is decision-gated and build-oriented. |

## Template Families Created By This Pass

| Family | Used by | Notes |
| --- | --- | --- |
| Governance decision packet | boundary-and-canon, after-acceleration-roadmap, staffing-budget-and-triggers | Holds decisions, ratification surfaces, and downstream unlocks. |
| Procedure/proof specification packet | hardware-golden-image, quality-security-proof | Defines receipts, acceptance tests, and proof surfaces before coding or test implementation. |
| Content and rule-pack packet | capital-logic-library | Separates content governance from future runtime implementation. |
| Operating playbook packet | white-glove-delivery-node-care, company-operations-finance, sales-contracting-legal | Converts workbook rows into repeatable service, sales, legal, and support procedures. |
| Parent recomposition packet | node-on-desk-readiness | Defines cross-node gates and receipt recomposition without duplicating child build detail. |

## Subagent Strategy

Dispatch Spec recommends a fanout strategy for future delegated review, but this
authoring pass did not spawn runtime subagents. Authorization remains
`requires_user_permission`.

Recommended future roles:

- `governance-author`: decision packets and canon guardrails.
- `procedure-author`: hardware/proof procedure specs and receipt contracts.
- `ops-author`: service, sales, legal, finance, and support operating artifacts.
- `parent-synthesizer`: parent recomposition and cross-node gate consistency.

Join policy: `parent_synthesis`. Each future receipt must cite `dispatch_id`,
`step_id`, `capability_ref`, artifacts, validation, blockers, residue, and handoff
note.

## Validation Surface

- Dispatch route: `docs/strategy/development/non-strict-coding-node-invoke/NON-STRICT-CODING-INVOKE.dispatch.json`
- Dispatch validator: `.agents/skills/dispatch-spec/scripts/validate-dispatch.py`
- Source ledgers: all selected node `.craft/ledger.yml` files
- Source specs: each selected node `BUILD-SPEC.md`
- Output artifacts: each selected node `INVOKE-DEVELOPMENT.md`

