---
feature: payment-link-and-reminder-messaging
version: current
status: draft
updatedAt: 2026-05-21
docType: operations
owners:
  - group operator
---

# Payment Link And Reminder Messaging Operations

## GeneratePaymentLinkMessages

Creates payment link artifacts and copyable payment link messages for selected obligations in a payment run.

Input:

- `paymentRunId`
- optional selected obligation IDs
- optional message customization
- optional deadline/expiry override
- operator ID

Preconditions:

- payment run exists in Dose Payment Tracking
- selected obligations are unpaid or exception-handled by operator choice
- buyers have WhatsApp mentions in Buyer Registry

Postconditions:

- one [Payment Link Artifact](domain.md#payment-link-artifact) exists for each selected obligation
- rendered payment link messages are recorded
- [PaymentLinkMessageRendered](events.md#paymentlinkmessagerendered) is emitted
- provider correlation key attachment is requested through Dose Payment Tracking

## RenderPaymentReminder

Creates copyable payment reminder text for eligible unpaid obligations.

Input:

- `paymentRunId` or `obligationId`
- cadence trigger
- optional recipient subset
- optional message customization
- operator ID

Preconditions:

- obligation payment status is unsatisfied
- reminder schedule is not suppressed
- direct posting is not requested

Postconditions:

- [Rendered Message](domain.md#rendered-message) is stored with `rendered` status
- [PaymentReminderRendered](events.md#paymentreminderrendered) is emitted

## RenderListingReminder

Creates copyable listing availability or fill reminder text from listing state.

Input:

- `listingId`
- listing reminder trigger
- optional message customization
- operator ID

Preconditions:

- listing exists in Bottle Listing And Dose Allocation
- trigger is one of the supported [Listing Reminder Trigger](domain.md#listing-reminder-trigger) values

Postconditions:

- rendered listing reminder is stored
- [ListingReminderRendered](events.md#listingreminderrendered) is emitted

## ReplacePaymentLinkMessage

Cancels or replaces an existing active payment link artifact.

Input:

- `paymentLinkArtifactId`
- replacement reason
- optional new customization
- operator ID

Preconditions:

- artifact is `active`
- linked obligation is not already paid

Postconditions:

- prior artifact becomes `replaced` or `cancelled`
- new artifact becomes `active` when replacement is requested
- [PaymentLinkMessageReplaced](events.md#paymentlinkmessagereplaced) is emitted

## SuppressReminder

Suppresses pending reminders for one obligation, payment run, listing, or schedule.

Input:

- target reference
- suppression reason
- operator ID or system trigger

Preconditions:

- target reminder schedule exists

Postconditions:

- pending reminders become `suppressed`
- [ReminderSuppressed](events.md#remindersuppressed) is emitted

## RecordReminderRendered

Records that copy/paste text was generated for operator use.

Input:

- rendered message ID
- message text
- render context
- operator ID

Postconditions:

- rendered message audit fields are complete
- no external delivery status is inferred
