---
node: staffing-budget-and-triggers
docType: invoke-development
status: flag
updatedAt: 2026-06-13
sourceLedger: docs/strategy/development/staffing-budget-and-triggers/.craft/ledger.yml
sourceBuildSpec: docs/strategy/development/staffing-budget-and-triggers/BUILD-SPEC.md
dispatch: docs/strategy/development/non-strict-coding-node-invoke/NON-STRICT-CODING-INVOKE.dispatch.json
---

# Invoke Development - Staffing, Budget, and Triggers

## Invoke Result

- Mode: define -> design -> plan
- Phase status: flag
- Target artifact: staffing and budget trigger package
- Template family: governance decision packet
- Coding boundary: no code or automation is involved; this is business and
  staffing decision scaffolding
- Next route: Josh fills hours/rates and selects trigger model

## Non-Strict-Coding Classification

This node is selected because all current blockers are operator/business input:
blank hours/rates, onboarding-now roles, onboarding-later triggers, and the
trigger model decision.

## Define Artifact

Objective: make the workbook computable as a budget and staffing plan without
inventing rates, hours, or thresholds.

Source contracts:

- `docs/strategy/development/staffing-budget-and-triggers/BUILD-SPEC.md`
- `docs/strategy/development/staffing-budget-and-triggers/.craft/ledger.yml`
- `docs/golden-quill-task-role-breakdown-handoff.md`

Terms:

- hours/rates scaffold;
- onboard-now roles;
- onboard-later roles;
- deployment-count trigger;
- revenue trigger;
- absorbed role.

Open decisions and gaps:

- `DEC-SBT-TRIGGER-MODEL`
- `GAP-SBT-HOURS-RATES`
- `GAP-SBT-ONBOARD-NOW`
- `GAP-SBT-ONBOARD-LATER`

## Design Artifact

Context view: this node turns task rows and role rows into an explicit cost and
staffing decision surface.

High-level structure: row-level hours/rates worksheet, role trigger model,
onboard-now procurement plan, onboard-later handoff plan, and cross-node cost
dependencies.

Low-level components:

- per-row task budget fields;
- role trigger options;
- near-now role list: domain experts, legal, security reviewer;
- later role list: customer success, field/install tech, bookkeeper;
- dependency map to WGD, QSP, CLL, SCL, and NOD.

Workflow process: fill hours/rates, select trigger model, cost near-now roles,
set later-role trigger thresholds, then feed node-on-desk RG-X.

Decision flow: no budget can be computed until hours/rates are filled.
Trigger-model selection is a Josh decision.

Dependency interface: feeds node-on-desk readiness, white-glove handoff,
capital expert review, security review, and legal-first LOI.

## Plan Artifact

Implementation layering for this authoring pass:

| Layer | Decision Question | Minimum Working Unit | Exit Evidence |
| --- | --- | --- | --- |
| L0 | Can every row accept hours/rates? | Budget worksheet scaffold. | No row missing fields. |
| L1 | Can near-now roles be costed? | Procurement/cost lane. | Legal/security/domain expert rows. |
| L2 | Can later roles trigger predictably? | Trigger model selection. | `DEC-SBT-TRIGGER-MODEL` closed. |
| L3 | Can readiness be budgeted? | RG-X feed to NOD. | Computable total. |

Work-pack:

| Task ID | Goal | Write Scope | Validation |
| --- | --- | --- | --- |
| SBT-AUTH-001 | Prepare row-level hours/rates worksheet. | Budget planning docs. | Every workbook row represented. |
| SBT-AUTH-002 | Frame trigger-model decision. | Decision packet. | Options and impacts clear. |
| SBT-AUTH-003 | Cost onboard-now roles. | Budget planning docs. | Domain expert/legal/security rows present. |
| SBT-AUTH-004 | Define later-role trigger placeholders. | Budget planning docs. | CS/field/bookkeeper triggers present. |

SWU handoff:

| SWU ID | Parent Task | Done Criteria | Execution Owner |
| --- | --- | --- | --- |
| SWU-SBT-001 | SBT-AUTH-001 | Worksheet can receive Josh-supplied values. | manual |
| SWU-SBT-002 | SBT-AUTH-002 | Trigger options are ready for Josh selection. | manual |
| SWU-SBT-003 | SBT-AUTH-003 | Near-now roles have cost slots and timing. | manual |
| SWU-SBT-004 | SBT-AUTH-004 | Later roles map to deployment/revenue triggers. | manual |

Residue: values are intentionally blank until Josh supplies them or approves
bounded external benchmarks.

