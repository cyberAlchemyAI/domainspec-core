---
feature: payment-link-and-reminder-messaging
version: current
status: draft
updatedAt: 2026-05-21
docType: domain
owners:
  - group operator
---

# Payment Link And Reminder Messaging Domain

## Payment Link Artifact

Entity representing the generated payment-link/instruction artifact for one buyer payment obligation.

Fields:

- `paymentLinkArtifactId`
- `paymentRunId`
- `obligationId`
- `buyerId`
- provider correlation key candidate (`txid` or equivalent)
- payment URL or Pix instruction payload
- expected amount
- description
- deadline or expiry
- [Payment Link Status](#payment-link-status)
- created/replaced/cancelled timestamps

Constraints:

- expected amount comes from Dose Payment Tracking, not this feature
- active artifacts must reference an active buyer obligation
- replacement creates a new active artifact and marks the prior one `replaced`

## Reminder Schedule

Entity representing the selected reminder plan for a payment run, obligation, or listing trigger.

Fields:

- `reminderScheduleId`
- trigger type: `payment_opened`, `payment_due_soon`, `payment_due_today`, `payment_overdue`, or listing trigger
- target payment run, obligation, or listing reference
- planned render time
- suppression status
- rendered message references

Constraints:

- payment schedules must stop when payment truth becomes paid
- listing schedules must not mutate listing lifecycle
- freight payment schedules are outside v1

## Reminder Message

Value object containing recipient, trigger context, and human-readable message text for copy/paste use.

Fields:

- recipient buyer ID when buyer-specific
- optional WhatsApp mention
- trigger context
- rendered text
- included payment link artifact when applicable
- generated timestamp

## Rendered Message

Entity preserving the generated copy/paste output and its lifecycle.

Fields:

- `renderedMessageId`
- message type: `payment_link`, `payment_reminder`, or `listing_reminder`
- source object reference
- target recipient set
- rendered text
- [Reminder Delivery Status](#reminder-delivery-status)
- rendered timestamp
- operator who rendered it

Constraints:

- rendered status means the system generated copyable text
- external WhatsApp delivery confirmation is not represented in v1

## Listing Reminder Trigger

Enum / type describing listing-origin reminder causes:

- `listing_opened`
- `listing_nearly_filled`
- `listing_filled`
- `listing_closed`

## Payment Link Status

Enum / type for payment link artifact lifecycle:

- `draft`
- `active`
- `replaced`
- `cancelled`
- `expired`

## Reminder Delivery Status

Enum / type for rendered reminder lifecycle:

- `pending`
- `rendered`
- `skipped`
- `failed`
- `suppressed`
