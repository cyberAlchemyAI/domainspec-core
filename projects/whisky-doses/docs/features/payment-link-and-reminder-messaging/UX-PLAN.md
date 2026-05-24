---
feature: payment-link-and-reminder-messaging
version: current
status: draft
updatedAt: 2026-05-21
docType: ux-plan
owners:
  - group operator
sources:
  - SPEC.md
  - STORIES.md
  - UI-SPEC.md
  - ../../UI-ARCHITECTURE.md
invoke_adapter: unavailable
---

# Payment Link And Reminder Messaging UX Plan

## Invocation Note

Local Arcanum invoke adapter was unavailable in this workspace; this UX plan was authored directly from SPEC.md, STORIES.md, UI-SPEC.md, and UI-ARCHITECTURE.md.

## UX Intent

Make buyer-facing payment and reminder text easy to generate, review, copy, replace, and suppress while making it unmistakable that v1 renders copy/paste text only.

Primary user: group operator.

Primary outcomes:

- generate payment link messages from payment obligations
- review and copy rendered messages
- render payment reminders by cadence
- render listing reminders from listing triggers
- replace stale links and suppress stale/noisy reminders

## Experience Principles

- Never imply delivery: use "Rendered" and "Copy" language, not "Sent".
- Source truth stays upstream: amounts/status come from Dose Payment Tracking, buyer mention from Buyer Registry, listing context from Bottle Listing.
- Message preview is critical: operator should see exactly what will be pasted.
- Suppression and replacement need reasons to keep audit useful.

## Primary Flow

1. Operator opens `/messages`.
2. Operator chooses payment run and generates link messages for default unpaid obligations or custom subset.
3. UI shows rendered text preview and copy action.
4. Generated artifacts appear in rendered message audit.
5. Operator copies text and posts manually to WhatsApp outside the system.

UX success criteria:

- default unpaid-recipient selection is obvious and editable
- preview clearly shows amount, deadline, buyer mention, and link/instruction text
- copy action does not mark message delivered

## Secondary Flows

### Payment Reminder

1. Operator opens reminder queue or payment run context.
2. Operator renders reminder for cadence trigger.
3. UI rechecks payment status and skips/suppresses paid obligations.

### Listing Reminder

1. Operator selects listing trigger.
2. UI reads listing context and renders availability/fill reminder.

### Replacement And Suppression

1. Operator replaces active link or suppresses reminder.
2. UI requires reason.
3. Prior artifact/reminder remains auditable.

## Screen Plan

| Screen               | UX Role                    | Key Decisions                                                |
| -------------------- | -------------------------- | ------------------------------------------------------------ |
| `/messages`          | Active messaging workbench | Tabs for link messages, payment reminders, listing reminders |
| `/messages/rendered` | Copy/paste audit           | Filter rendered history by type, buyer, source, date         |

## Interaction Details

- Primary actions: "Generate Link Messages", "Render Payment Reminder", "Render Listing Reminder".
- Message preview should be selectable and have one copy button.
- Reminder rows show trigger, target, status, and suppression reason when present.
- Link artifact rows show active/replaced/cancelled/expired status.

## Edge And Empty States

| State                           | UX Response                                               |
| ------------------------------- | --------------------------------------------------------- |
| No unpaid obligations           | Explain there are no eligible payment links to generate   |
| Buyer missing mention           | Block rendering for that buyer and link to Buyer Registry |
| Obligation paid before render   | Skip/suppress and explain payment is already satisfied    |
| Direct posting requested        | Explain v1 is copy/paste only                             |
| Replacement for paid obligation | Block normal replacement and explain paid-state boundary  |

## Cross-Feature Handoffs

| Handoff                                 | UX Contract                                                                                                    |
| --------------------------------------- | -------------------------------------------------------------------------------------------------------------- |
| From Buyer Registry                     | Rendered text uses the canonical buyer mention and blocks when the mention is missing                          |
| From Dose Payment Tracking              | Payment links and payment reminders consume unpaid obligations, amounts, deadlines, and paid/suppressed status |
| From Bottle Listing And Dose Allocation | Listing reminders consume listing availability, fill, and close context without mutating allocation            |

## UX Validation Checklist

- [ ] Copy/paste semantics are clear; no screen implies WhatsApp delivery.
- [ ] Default recipient selection targets unpaid obligations while allowing an operator-customized subset.
- [ ] Message preview shows exactly what the operator will copy.
- [ ] Reminder suppression and payment-link replacement require reasons.
- [ ] Paid obligations are skipped or blocked before rendering stale payment reminders.

## Iteration Notes

- Freight payment reminders remain outside v1.
- Public listing formatting belongs to Public WhatsApp List Rendering.
- Future WhatsApp API posting must introduce delivery semantics separately from rendered audit.
