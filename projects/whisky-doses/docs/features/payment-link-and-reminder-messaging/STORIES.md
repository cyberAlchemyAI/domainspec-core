---
feature: payment-link-and-reminder-messaging
version: current
status: draft
updatedAt: 2026-05-21
docType: stories
owners:
  - group operator
---

# Payment Link And Reminder Messaging Stories

## Story Set

These stories mirror the Payment Link And Reminder Messaging capabilities in [SPEC.md](SPEC.md#capabilities) and preserve coverage across public, admin/operations, cross-feature integration, and edge-case journeys.

## PM-S1 Generate Payment Link Messages

Capability: [Payment Link Message Generation](SPEC.md#capabilities)
Journey type: admin/operations
Concept links: [Payment Link Artifact](domain.md#payment-link-artifact), [GeneratePaymentLinkMessages](operations.md#generatepaymentlinkmessages), [PaymentLinkCustomizationPolicy](rules.md#p1-payment-link-customization-policy)

Classic story:
As a group operator, I want to generate copyable payment link messages for unpaid obligations in a payment run, so that buyers receive the right payment instruction text.

BDD scenario:
Given a payment run exists with unpaid buyer obligations
When the operator generates payment link messages
Then one payment link artifact is created for each selected obligation
And rendered copy/paste text is recorded
And provider correlation-key attachment is requested through Dose Payment Tracking.

Acceptance checks:

- Defaults select all unpaid obligations in the payment run.
- Operator can customize recipients, message/description, deadline/expiry, and replacement behavior.
- Payment amount and deadline come from Dose Payment Tracking.
- Buyer name and WhatsApp mention come from Buyer Registry.

## PM-S2 Review And Copy Rendered Messages

Capability: [Rendered Message Audit](SPEC.md#capabilities)
Journey type: public
Concept links: [Rendered Message](domain.md#rendered-message), [GetRenderedMessages](queries.md#getrenderedmessages), [DirectPostingDeferredRule](rules.md#r3-direct-posting-deferred-rule)

Classic story:
As a group operator, I want to review and copy rendered payment or reminder text, so that I can paste it into WhatsApp without the system claiming it was delivered.

BDD scenario:
Given rendered messages exist
When the operator opens rendered message history
Then the UI shows message type, recipient context, rendered text, and render status
And the system labels the message as rendered for copy/paste, not sent.

Acceptance checks:

- Rendered text can be copied.
- Rendered status never implies WhatsApp delivery.
- Audit records remain available after link replacement or reminder suppression.

## PM-S3 Render Payment Reminder

Capability: [Payment Reminder Rendering](SPEC.md#capabilities)
Journey type: admin/operations
Concept links: [Reminder Schedule](domain.md#reminder-schedule), [RenderPaymentReminder](operations.md#renderpaymentreminder), [ReminderCadencePolicy](rules.md#p2-reminder-cadence-policy)

Classic story:
As a group operator, I want to render payment reminders for unpaid obligations at the selected cadence, so that unpaid buyers are prompted without stale or duplicate messaging.

BDD scenario:
Given a payment reminder cadence trigger fires
When the operator renders reminders for a payment run or obligation
Then the system confirms current payment status
And renders reminders only for unsatisfied obligations
And records the reminder as rendered.

Acceptance checks:

- Supported cadence includes payment opened, 24h before deadline, deadline day, and overdue.
- Paid obligations are skipped or suppressed.
- Exception statuses require exception-aware copy or operator choice.
- Freight payment reminders are outside v1.

## PM-S4 Render Listing Reminder

Capability: [Listing Reminder Rendering](SPEC.md#capabilities)
Journey type: cross-feature integration
Concept links: [Listing Reminder Trigger](domain.md#listing-reminder-trigger), [RenderListingReminder](operations.md#renderlistingreminder), [Bottle Listing And Dose Allocation](../bottle-listing-and-dose-allocation/SPEC.md)

Classic story:
As a group operator, I want to render listing availability or fill reminders from listing state, so that the group can be nudged without messaging owning listing lifecycle.

BDD scenario:
Given a listing opened, nearly filled, filled, or closed trigger exists
When the operator renders a listing reminder
Then the system reads listing context from Bottle Listing And Dose Allocation
And stores copyable reminder text without mutating listing state.

Acceptance checks:

- Listing reminder triggers include opened, nearly filled, filled, and closed.
- Listing state comes from Bottle Listing And Dose Allocation.
- Rendering does not allocate slots or close listings.

## PM-S5 Suppress Paid Or Noisy Reminders

Capability: [Reminder Suppression](SPEC.md#capabilities)
Journey type: edge-case
Concept links: [SuppressReminder](operations.md#suppressreminder), [StopReminderWhenPaidRule](rules.md#r2-stop-reminder-when-paid-rule), [ReminderDeliveryStatusLifecycle](states.md#reminderdeliverystatuslifecycle)

Classic story:
As a group operator, I want paid or noisy reminders to stop, so that buyers are not prompted after payment or manual suppression.

BDD scenario:
Given pending reminders exist for an obligation or listing
When payment is reconciled as satisfied or the operator suppresses the reminder
Then pending reminders become suppressed or skipped
And the suppression reason is recorded.

Acceptance checks:

- Paid/satisfied payment events suppress related payment reminders.
- Operator suppression requires a reason.
- Suppressed reminders remain auditable.
- Suppression does not change payment truth.

## PM-S6 Replace Payment Link Message

Capability: [Payment Link Message Generation](SPEC.md#capabilities)
Journey type: edge-case
Concept links: [ReplacePaymentLinkMessage](operations.md#replacepaymentlinkmessage), [LinkRegenerationPolicy](rules.md#p3-link-regeneration-policy), [PaymentLinkStatusLifecycle](states.md#paymentlinkstatuslifecycle)

Classic story:
As a group operator, I want to replace an active payment link message, so that stale or incorrect payment instructions can be cancelled and regenerated.

BDD scenario:
Given an active payment link artifact exists for an unpaid obligation
When the operator replaces the link with a reason
Then the prior artifact becomes replaced or cancelled
And a new active artifact is generated when requested
And audit history remains intact.

Acceptance checks:

- Paid obligations cannot receive normal replacement links.
- Prior artifacts remain auditable.
- Replacement can request a new provider correlation key attachment.
- Replacement emits [PaymentLinkMessageReplaced](events.md#paymentlinkmessagereplaced).

## Story Coverage Matrix

| Capability                      | Stories                                                                                      | Coverage                    |
| ------------------------------- | -------------------------------------------------------------------------------------------- | --------------------------- |
| Payment Link Message Generation | [PM-S1](#pm-s1-generate-payment-link-messages), [PM-S6](#pm-s6-replace-payment-link-message) | admin/operations, edge-case |
| Payment Reminder Rendering      | [PM-S3](#pm-s3-render-payment-reminder)                                                      | admin/operations            |
| Listing Reminder Rendering      | [PM-S4](#pm-s4-render-listing-reminder)                                                      | cross-feature integration   |
| Reminder Suppression            | [PM-S5](#pm-s5-suppress-paid-or-noisy-reminders)                                             | edge-case                   |
| Rendered Message Audit          | [PM-S2](#pm-s2-review-and-copy-rendered-messages)                                            | public                      |

## Concept Coverage Matrix

| Concept                                                               | Covered By                        | Notes                                      |
| --------------------------------------------------------------------- | --------------------------------- | ------------------------------------------ |
| `payment-link-and-reminder-messaging.PaymentLinkArtifact`             | PM-S1, PM-S6                      | Link lifecycle                             |
| `payment-link-and-reminder-messaging.ReminderSchedule`                | PM-S3, PM-S5                      | Reminder cadence and suppression           |
| `payment-link-and-reminder-messaging.ReminderMessage`                 | PM-S2, PM-S3, PM-S4               | Copyable text                              |
| `payment-link-and-reminder-messaging.RenderedMessage`                 | PM-S2, PM-S3, PM-S4               | Audit state                                |
| `payment-link-and-reminder-messaging.ListingReminderTrigger`          | PM-S4                             | Listing activity reminders                 |
| `payment-link-and-reminder-messaging.PaymentLinkStatusLifecycle`      | PM-S1, PM-S6                      | Active/replaced/cancelled/expired          |
| `payment-link-and-reminder-messaging.ReminderDeliveryStatusLifecycle` | PM-S3, PM-S5                      | Pending/rendered/skipped/failed/suppressed |
| `payment-link-and-reminder-messaging.GeneratePaymentLinkMessages`     | PM-S1                             | Link message generation                    |
| `payment-link-and-reminder-messaging.RenderPaymentReminder`           | PM-S3                             | Payment reminder rendering                 |
| `payment-link-and-reminder-messaging.RenderListingReminder`           | PM-S4                             | Listing reminder rendering                 |
| `payment-link-and-reminder-messaging.ReplacePaymentLinkMessage`       | PM-S6                             | Replacement flow                           |
| `payment-link-and-reminder-messaging.SuppressReminder`                | PM-S5                             | Stop/suppression                           |
| `payment-link-and-reminder-messaging.MessagingAPI`                    | PM-S1, PM-S3, PM-S4, PM-S5, PM-S6 | Operator API                               |
| `payment-link-and-reminder-messaging.MessagingModule`                 | PM-S2                             | Cross-feature/rendered output reads        |

## Drift Warnings

No story drift warnings identified.

## Unresolved Questions

No unresolved story questions.
