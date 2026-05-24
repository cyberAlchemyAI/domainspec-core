---
feature: dose-payment-tracking
version: current
status: draft
updatedAt: 2026-05-21
docType: queries
owners:
  - group operator
---

# Dose Payment Tracking Queries

## GetPaymentRun

Reads one payment run with buyer obligations.

Input: `paymentRunId`

Output:

- payment run details
- selected listing IDs
- deadline
- buyer obligations and statuses
- exception counts

## GetBuyerPaymentStatus

Reads payment status for one buyer across one or more payment runs or listings.

Input:

- `buyerId`
- optional listing IDs
- optional payment run ID

Output:

- obligation IDs
- expected amount
- received amount
- status
- line items

## GetListingPaymentSummary

Reads buyer-level payment truth for public listing rendering.

Input:

- `listingId`

Output:

- buyer ID
- slot numbers
- payment status
- expected amount
- deadline when available

## GetPaymentExceptions

Reads obligations requiring operator attention.

Filters:

- status: `partial`, `overpaid`, `unmatched`, `failed`
- listing ID
- payment run ID

Output:

- obligation ID
- buyer ID
- expected amount
- received amount
- exception reason
- next action hint
