---
node: company-operations-finance
docType: invoke-development
status: flag
updatedAt: 2026-06-13
sourceLedger: docs/strategy/development/company-operations-finance/.craft/ledger.yml
sourceBuildSpec: docs/strategy/development/company-operations-finance/BUILD-SPEC.md
dispatch: docs/strategy/development/non-strict-coding-node-invoke/NON-STRICT-CODING-INVOKE.dispatch.json
---

# Invoke Development - Company Operations and Finance

## Invoke Result

- Mode: define -> design -> plan
- Phase status: flag
- Target artifact: operations and finance operating package
- Template family: operating playbook packet
- Coding boundary: no support tooling or finance automation is implemented here;
  this artifact defines procedures, ownership, and evidence
- Next route: Josh/Victor operating checklist authoring

## Non-Strict-Coding Classification

This node is selected because the current work is company operating structure:
entity hygiene, support triage, Node Care cadence, and validation packet
maintenance.

## Define Artifact

Objective: define the operating floor that keeps Golden Quill customers
supported, evidence maintained, and finances trackable.

Source contracts:

- `docs/strategy/development/company-operations-finance/BUILD-SPEC.md`
- `docs/strategy/development/company-operations-finance/.craft/ledger.yml`
- QSP claims/instrumentation dependency
- `docs/golden-quill-task-role-breakdown-handoff.md`

Terms:

- entity hygiene checklist;
- support triage boundary;
- Node Care cadence;
- validation packet;
- support absorbs vs engineering sees.

Open gaps:

- `GAP-COF-ENTITY-HYGIENE`
- `GAP-COF-SUPPORT-TRIAGE`
- `GAP-COF-NODE-CARE-OPS`
- `GAP-COF-VALIDATION-PACKET`

## Design Artifact

Context view: this node is the operating floor after deployment and first
revenue.

High-level structure: entity/banking/bookkeeping/insurance checklist, support
channel and issue log, triage rules, Node Care cadence, and validation packet
ownership.

Low-level components:

- entity hygiene checklist;
- support issue taxonomy;
- escalation rule for engineering;
- Node Care schedule;
- validation packet evidence map.

Workflow process: keep company hygiene current, log support issues, triage them
against support/engineering boundaries, run Node Care, and maintain validation
evidence for investors/funders.

Decision flow: support-triage rules are blocking because they define when
engineering capacity is consumed. Validation packet depends on QSP claims and
instrumentation.

Dependency interface: consumes QSP metrics and claims register; coordinates with
white-glove Node Care and sales/contracting finance triggers.

## Plan Artifact

Implementation layering for this authoring pass:

| Layer | Decision Question | Minimum Working Unit | Exit Evidence |
| --- | --- | --- | --- |
| L0 | Can company hygiene be checked? | Entity/finance checklist. | Reviewable checklist. |
| L1 | Can support be triaged? | Issue log and escalation rules. | Boundary rules. |
| L2 | Can Node Care recur? | Cadence and responsibility map. | Schedule and owner. |
| L3 | Can validation packets stay current? | Evidence ownership map. | QSP feed linked. |

Work-pack:

| Task ID | Goal | Write Scope | Validation |
| --- | --- | --- | --- |
| COF-AUTH-001 | Author entity hygiene checklist. | Ops docs. | Banking/bookkeeping/contracts/insurance covered. |
| COF-AUTH-002 | Author support triage rules. | Ops docs. | Support vs engineering boundary clear. |
| COF-AUTH-003 | Author Node Care cadence. | Ops docs. | Quarterly/source-index/vault care covered. |
| COF-AUTH-004 | Author validation packet owner map. | Ops docs. | QSP inputs linked. |

SWU handoff:

| SWU ID | Parent Task | Done Criteria | Execution Owner |
| --- | --- | --- | --- |
| SWU-COF-001 | COF-AUTH-001 | Checklist covers entity, bank, books, filings, insurance. | manual |
| SWU-COF-002 | COF-AUTH-002 | Issue taxonomy and escalation threshold are reviewable. | local-fallback |
| SWU-COF-003 | COF-AUTH-003 | Node Care cadence names customer and technical responsibilities. | local-fallback |
| SWU-COF-004 | COF-AUTH-004 | Validation packet has evidence owner per section. | local-fallback |

Residue: validation packet cannot fully close until QSP claims register and
instrumentation land.

