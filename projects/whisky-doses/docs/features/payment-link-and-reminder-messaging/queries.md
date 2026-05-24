---
feature: payment-link-and-reminder-messaging
version: current
status: draft
updatedAt: 2026-05-21
docType: queries
owners:
  - group operator
---

# Payment Link And Reminder Messaging Queries

## GetPaymentLinkMessages

Reads payment link artifacts and rendered payment link text for a payment run or obligation.

Input:

- optional `paymentRunId`
- optional `obligationId`
- optional status filter

Output:

- artifact ID
- payment run ID
- obligation ID
- buyer ID and WhatsApp mention
- amount and deadline copied from payment truth at render time
- payment link status
- rendered text

## GetReminderQueue

Reads pending, rendered, failed, or suppressed reminders.

Filters:

- reminder type
- payment run ID
- obligation ID
- listing ID
- delivery status
- planned render date

Output:

- reminder schedule ID
- trigger
- target reference
- recipient summary
- planned render time
- delivery status
- stop/suppression reason when present

## GetRenderedMessages

Reads generated copy/paste message audit records.

Filters:

- message type
- source object reference
- buyer ID
- rendered date range

Output:

- rendered message ID
- message type
- rendered text
- recipient set
- status
- operator ID
- rendered timestamp
