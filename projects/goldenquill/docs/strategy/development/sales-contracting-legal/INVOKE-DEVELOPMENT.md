---
node: sales-contracting-legal
docType: invoke-development
status: flag
updatedAt: 2026-06-13
sourceLedger: docs/strategy/development/sales-contracting-legal/.craft/ledger.yml
sourceBuildSpec: docs/strategy/development/sales-contracting-legal/BUILD-SPEC.md
dispatch: docs/strategy/development/non-strict-coding-node-invoke/NON-STRICT-CODING-INVOKE.dispatch.json
---

# Invoke Development - Sales, Contracting, and Legal

## Invoke Result

- Mode: define -> design -> plan
- Phase status: flag
- Target artifact: sales and legal operating package
- Template family: operating playbook packet
- Coding boundary: no product code or legal drafting authority is claimed here;
  counsel-owned clauses remain outside this artifact
- Next route: Josh sales-material authoring plus fractional legal counsel

## Non-Strict-Coding Classification

This node is selected because the immediate work is a sales/legal planning
surface: claims-backed materials, readiness checklist, agreement/LOI/data-policy
requirements, procurement notes, insurance, deposits, invoicing, and cost
tracking.

## Define Artifact

Objective: define the sales and contracting package needed before a first LOI
or customer agreement can safely ship.

Source contracts:

- `docs/strategy/development/sales-contracting-legal/BUILD-SPEC.md`
- `docs/strategy/development/sales-contracting-legal/.craft/ledger.yml`
- `docs/golden-quill-task-role-breakdown-handoff.md`
- quality-security-proof claims register dependency

Terms:

- claims-backed sales material;
- readiness checklist;
- legal-first LOI;
- data-policy terms;
- deposit and invoicing trigger.

Open gaps:

- `GAP-SCL-SALES-MATERIALS`
- `GAP-SCL-LEGAL-FIRST-LOI`
- `GAP-SCL-DEPOSIT-INVOICING`

## Design Artifact

Context view: this node controls the public/commercial wrapper around the
technical product.

High-level structure: one-pager/demo/segment framing, qualification checklist,
LOI/agreement/data-policy/procurement/insurance, and deposit/invoicing flow.

Low-level components:

- claim-to-evidence map from QSP;
- fit/no-fit and referral readiness checklist;
- counsel intake brief;
- LOI/agreement clause inventory;
- deposit and invoicing control fields.

Workflow process: claims register lands, sales material drafts cite it, legal
counsel prepares or approves LOI/agreement/data-policy, then deposit and
invoicing rules activate at first revenue.

Decision flow: legal counsel retention is blocking before first LOI signs.
Bookkeeper activation is later and revenue-triggered.

Dependency interface: consumes QSP claims register and staffing/budget trigger
decisions; feeds white-glove customer onboarding.

## Plan Artifact

Implementation layering for this authoring pass:

| Layer | Decision Question | Minimum Working Unit | Exit Evidence |
| --- | --- | --- | --- |
| L0 | Can sales claims be traced? | Claims-backed one-pager outline. | Every claim has QSP evidence slot. |
| L1 | Can prospects be qualified consistently? | Readiness checklist. | Fit/no-fit criteria. |
| L2 | Can LOI/legal work proceed safely? | Counsel intake brief and clause inventory. | Legal owner named. |
| L3 | Can first revenue be tracked? | Deposit/invoicing trigger fields. | Bookkeeper trigger named. |

Work-pack:

| Task ID | Goal | Write Scope | Validation |
| --- | --- | --- | --- |
| SCL-AUTH-001 | Draft claims-backed sales-material outline. | Sales planning docs. | Claims reference QSP register. |
| SCL-AUTH-002 | Author qualification/readiness checklist. | Sales planning docs. | Fit/no-fit criteria clear. |
| SCL-AUTH-003 | Prepare legal counsel intake packet. | Legal planning docs. | Does not replace counsel. |
| SCL-AUTH-004 | Define deposit/invoicing trigger. | Finance handoff. | Bookkeeper activation named. |

SWU handoff:

| SWU ID | Parent Task | Done Criteria | Execution Owner |
| --- | --- | --- | --- |
| SWU-SCL-001 | SCL-AUTH-001 | One-pager/demo outline contains no unsupported claims. | local-fallback |
| SWU-SCL-002 | SCL-AUTH-002 | Readiness checklist distinguishes fit, no-fit, and referral. | local-fallback |
| SWU-SCL-003 | SCL-AUTH-003 | Counsel receives issue list and source context. | manual |
| SWU-SCL-004 | SCL-AUTH-004 | Deposit/invoicing trigger is ready for COF/bookkeeper. | local-fallback |

Residue: fractional legal counsel remains blocking before first LOI signs.

