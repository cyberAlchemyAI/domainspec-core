---
feature: payment-link-and-reminder-messaging
version: current
status: draft
updatedAt: 2026-05-21
docType: events
owners:
  - group operator
---

# Payment Link And Reminder Messaging Events

## PaymentLinkMessageRendered

Produced by: [GeneratePaymentLinkMessages](operations.md#generatepaymentlinkmessages)

Payload:

- `paymentLinkArtifactId`
- `paymentRunId`
- `obligationId`
- `buyerId`
- provider correlation key candidate
- rendered message ID

Consumers:

- Operator UI shows copyable payment link text.
- Dose Payment Tracking stores the provider correlation key through its attachment interface.

## PaymentReminderRendered

Produced by: [RenderPaymentReminder](operations.md#renderpaymentreminder)

Payload:

- reminder schedule ID
- payment run ID
- obligation ID
- buyer ID
- cadence trigger
- rendered message ID

Consumers:

- Operator UI shows copyable reminder text.
- Reminder reporting can measure reminder conversion and noise rate.

## ListingReminderRendered

Produced by: [RenderListingReminder](operations.md#renderlistingreminder)

Payload:

- reminder schedule ID
- listing ID
- listing reminder trigger
- rendered message ID

Consumers:

- Operator UI shows copyable listing reminder text.
- Public WhatsApp List Rendering may consume reminder snippets when composing group text.

## ReminderSuppressed

Produced by: [SuppressReminder](operations.md#suppressreminder)

Payload:

- reminder schedule ID
- target reference
- suppression reason
- source: `operator` or `system`

Consumers:

- Operator UI removes or explains pending reminders.
- Reminder reporting can distinguish paid stops from manual suppression.

## PaymentLinkMessageReplaced

Produced by: [ReplacePaymentLinkMessage](operations.md#replacepaymentlinkmessage)

Payload:

- prior payment link artifact ID
- replacement payment link artifact ID when generated
- obligation ID
- reason

Consumers:

- Operator UI shows active replacement link.
- Audit views preserve prior link history.
