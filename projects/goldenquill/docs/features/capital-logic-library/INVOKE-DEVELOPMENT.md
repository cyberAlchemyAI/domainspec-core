---
node: capital-logic-library
docType: invoke-development
status: flag
updatedAt: 2026-06-13
sourceLedger: docs/features/capital-logic-library/.craft/ledger.yml
sourceBuildSpec: docs/features/capital-logic-library/BUILD-SPEC.md
dispatch: docs/strategy/development/non-strict-coding-node-invoke/NON-STRICT-CODING-INVOKE.dispatch.json
---

# Invoke Development - Capital Logic Library

## Invoke Result

- Mode: define -> design -> plan
- Phase status: flag
- Target artifact: capital logic content and governance package
- Template family: content and rule-pack packet
- Coding boundary: this artifact defines card/rule-pack governance and launch
  content workflow; runtime card tooling is a later implementation concern
- Next route: Josh/domain-expert authoring and later backend support

## Non-Strict-Coding Classification

This node is selected because the immediate work is content architecture:
card schema, governance, five launch cards, paid expert review, source
universes, and recurring funder rule packs.

## Define Artifact

Objective: define the Capital Logic Library as a governed content system that
can be expert-reviewed and later connected to promotion-governance without
recreating the root feature.

Source contracts:

- `docs/features/capital-logic-library/BUILD-SPEC.md`
- `docs/features/capital-logic-library/.craft/ledger.yml`
- root promotion-governance Craft ledger
- `docs/golden-quill-task-role-breakdown-handoff.md`

Terms:

- launch card;
- rule pack;
- source universe;
- expert structured input;
- promotion-governance link.

Open gaps:

- `GAP-CLL-LAUNCH-CARDS`
- `GAP-CLL-DOMAIN-EXPERTS`
- `GAP-CLL-RULE-PACKS`

## Design Artifact

Context view: this node supplies the grant-strategy content spine without
pretending content edits are runtime promotion.

High-level structure: card schema and governance, launch card pipeline, expert
input contracts, segment source universes, recurring funder rule packs, and
promotion-governance linkage.

Low-level components:

- card metadata and testability rules;
- five-card launch register;
- expert review packet;
- rule-pack ownership fields;
- source-universe list per segment.

Workflow process: define schema, author or update five launch cards, send
structured review packets to domain experts, record corrections, and link
reusable improvements through promotion-governance.

Decision flow: domain expert onboarding and compensation are operator/staffing
decisions. Card content can progress as draft, but validation needs paid input.

Dependency interface: feeds sales material, Scout source-universe setup, and
root promotion-governance evidence.

## Plan Artifact

Implementation layering for this authoring pass:

| Layer | Decision Question | Minimum Working Unit | Exit Evidence |
| --- | --- | --- | --- |
| L0 | Do we have a useful card schema? | One card schema and Farmer v1 reference. | Schema review. |
| L1 | Can the five launch cards move through expert review? | Launch register and review packet. | Expert-input checklist. |
| L2 | Can rule packs stay governed over time? | Rule-pack ownership model. | Maintenance owner named. |
| L3 | Can content feed reusable learning safely? | Promotion-governance link. | No direct self-promotion. |

Work-pack:

| Task ID | Goal | Write Scope | Validation |
| --- | --- | --- | --- |
| CLL-AUTH-001 | Author card schema and governance rules. | Content spec. | Testability fields present. |
| CLL-AUTH-002 | Create five-card launch register. | Content register. | Status for each card. |
| CLL-AUTH-003 | Define expert review packet. | Review template. | Domain expert role and evidence requested. |
| CLL-AUTH-004 | Define rule-pack maintenance model. | Rule-pack spec. | Owner and update cadence. |

SWU handoff:

| SWU ID | Parent Task | Done Criteria | Execution Owner |
| --- | --- | --- | --- |
| SWU-CLL-001 | CLL-AUTH-001 | Schema distinguishes defaults, evidence, tests, and revision history. | local-fallback |
| SWU-CLL-002 | CLL-AUTH-002 | Five launch cards have status and next evidence request. | manual |
| SWU-CLL-003 | CLL-AUTH-003 | Expert packet can be sent without extra context. | manual |
| SWU-CLL-004 | CLL-AUTH-004 | Rule-pack maintenance owner and cadence are defined. | local-fallback |

Residue: four domain experts remain unfilled and launch-card validation is not
complete until expert input lands.

