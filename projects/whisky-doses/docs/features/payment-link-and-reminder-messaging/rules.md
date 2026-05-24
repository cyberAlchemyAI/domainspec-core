---
feature: payment-link-and-reminder-messaging
version: current
status: draft
updatedAt: 2026-05-21
docType: rules
owners:
  - group operator
---

# Payment Link And Reminder Messaging Rules

## P1 Payment Link Customization Policy

When generating payment link messages for a payment run, the default recipient set is every unpaid buyer obligation in the selected payment run.

Defaults:

- recipients: all unpaid obligations
- amount: expected amount from Dose Payment Tracking
- description: listing-based line item summary
- deadline/expiry: payment run deadline
- regeneration: disabled unless operator requests replacement

Operator-customizable fields:

- buyer selection
- message text or description
- deadline/expiry
- cancel/replace regeneration

## P2 Reminder Cadence Policy

V1 supports dose payment reminders and listing availability/fill reminders.

Payment reminder cadence:

- when payment opens
- 24 hours before deadline
- on deadline day
- when overdue

Freight payment reminders are outside v1.

## P3 Link Regeneration Policy

Replacing a payment link message must:

- mark the prior active artifact `replaced` or `cancelled`
- create a new artifact with a new provider correlation key candidate when provider semantics require it
- preserve audit history for the prior rendered text
- request correlation-key attachment through Dose Payment Tracking when the new link is active

## R1 Unpaid Recipient Rule

Payment reminders may be rendered only for obligations whose payment status is not satisfied.

Satisfied statuses:

- `paid`
- any future status explicitly classified by Dose Payment Tracking as payment-satisfied

Exception statuses such as `partial`, `overpaid`, `unmatched`, or `failed` require operator attention and must use exception-aware reminder text or be skipped.

## R2 Stop Reminder When Paid Rule

When [Dose Payment Tracking](../dose-payment-tracking/SPEC.md) emits `PaymentReconciled` with a paid/satisfied status, all pending reminder schedules for that obligation must become `suppressed` or `skipped`.

## R3 Direct Posting Deferred Rule

The system must render copy/paste WhatsApp text only in v1.

It must not:

- call WhatsApp APIs
- represent rendered messages as externally delivered
- treat copy/paste rendering as proof that a buyer received the message

## R4 Source Authority Rule

Messaging must read payment amount, payment status, and deadline from Dose Payment Tracking. It must read buyer mention/name from Buyer Registry. It must read listing availability/fill context from Bottle Listing And Dose Allocation.

Messaging may cache rendered text for audit, but cached text is not authoritative for payment, buyer, or listing truth.
