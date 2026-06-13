---
node: white-glove-delivery-node-care
docType: invoke-development
status: flag
updatedAt: 2026-06-13
sourceLedger: docs/strategy/development/white-glove-delivery-node-care/.craft/ledger.yml
sourceBuildSpec: docs/strategy/development/white-glove-delivery-node-care/BUILD-SPEC.md
dispatch: docs/strategy/development/non-strict-coding-node-invoke/NON-STRICT-CODING-INVOKE.dispatch.json
---

# Invoke Development - White-Glove Delivery and Node Care

## Invoke Result

- Mode: define -> design -> plan
- Phase status: flag
- Target artifact: delivery service wrapper and Node Care package
- Template family: operating playbook packet
- Coding boundary: no UI, runtime, or install automation is authored here; this
  is the human-facing wrapper over the locked technical spine
- Next route: service-template authoring and later dogfood install proof

## Non-Strict-Coding Classification

This node is selected because its current work is a repeatable service wrapper:
document request, onboarding, posture conversation, deployment record, training,
Day-60 review, and Node Care cadence.

## Define Artifact

Objective: make the founder-led install teachable, repeatable, and auditable
without changing the headless v0.1 product boundary.

Source contracts:

- `docs/strategy/development/white-glove-delivery-node-care/BUILD-SPEC.md`
- `docs/white_glove_v0_1_beta.md`
- `docs/golden-quill-task-role-breakdown-handoff.md`
- QSP instrumentation and staffing-trigger dependencies

Terms:

- delivery service wrapper;
- Deployment Record;
- Posture Conversation Script;
- Day-60 review;
- Node Care recurring schedule;
- CS/Field-Tech handoff.

Open gaps:

- `GAP-WGD-PLAYBOOK`
- `GAP-WGD-CS-HANDOFF`
- `GAP-WGD-DAY60`

## Design Artifact

Context view: this node is the customer-facing delivery process around the
local appliance and first grant cycle.

High-level structure: pre-deployment kit, Day-0 install, vault build,
source-universe setup, first opportunity packet, training sessions, branded
closeout, Day-60 review, and recurring Node Care.

Low-level components:

- Document-Request Kit;
- Onboarding Questionnaire;
- Posture-Conversation Script;
- Deployment Record;
- Vault-Build Worksheet and Missing-Doc List;
- Source-Universe Manifest;
- First-Opportunity Packet;
- Training Curriculum;
- Branded Closeout;
- Node Care schedule.

Workflow process: prepare customer, install node, build vault, run first
opportunity, train operator, close out, then review use at Day 60.

Decision flow: Day-60 metrics depend on QSP instrumentation; CS/Field-Tech
activation depends on staffing-budget triggers.

Dependency interface: consumes hardware image, runtime, QSP metrics, staffing
triggers, and sales/legal readiness; feeds node-on-desk readiness.

## Plan Artifact

Implementation layering for this authoring pass:

| Layer | Decision Question | Minimum Working Unit | Exit Evidence |
| --- | --- | --- | --- |
| L0 | Can the pre-deployment wrapper be run? | Four pre-deployment templates. | Template checklist. |
| L1 | Can first-cycle delivery be repeated? | Vault/source/opportunity/training templates. | Non-author run criterion. |
| L2 | Can Day-60 and Node Care be governed? | Review and recurring schedule. | QSP metric dependency marked. |
| L3 | Can CS/Field-Tech take over? | Transition checklist. | Staffing trigger placeholder. |

Work-pack:

| Task ID | Goal | Write Scope | Validation |
| --- | --- | --- | --- |
| WGD-AUTH-001 | Author pre-deployment wrapper templates. | Service templates. | Classification review and posture sign-off present. |
| WGD-AUTH-002 | Author first-cycle/training templates. | Service templates. | No UI deliverables. |
| WGD-AUTH-003 | Author Day-60 and Node Care templates. | Service templates. | QSP metrics dependency explicit. |
| WGD-AUTH-004 | Author CS/Field-Tech transition checklist. | Service templates. | Staffing trigger placeholder explicit. |

SWU handoff:

| SWU ID | Parent Task | Done Criteria | Execution Owner |
| --- | --- | --- | --- |
| SWU-WGD-001 | WGD-AUTH-001 | Document request, questionnaire, posture script, deployment record exist. | local-fallback |
| SWU-WGD-002 | WGD-AUTH-002 | First-cycle and training surfaces map to locked technical spine. | local-fallback |
| SWU-WGD-003 | WGD-AUTH-003 | Day-60 template marks QSP metrics as dependency. | local-fallback |
| SWU-WGD-004 | WGD-AUTH-004 | Transition checklist waits on staffing trigger. | manual |

Residue: repeatability is not proven until a non-author runs the kit end to end.

