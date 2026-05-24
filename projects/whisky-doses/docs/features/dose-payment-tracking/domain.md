---
feature: dose-payment-tracking
version: current
status: draft
updatedAt: 2026-05-21
docType: domain
owners:
  - group operator
---

# Dose Payment Tracking Domain

## Entities

### Payment Run

Operator-opened collection event for one or more selected listings.

| Field                | Type           | Required | Description                         |
| -------------------- | -------------- | -------- | ----------------------------------- |
| `id`                 | Payment Run ID | yes      | Stable identifier                   |
| `selectedListingIds` | Listing ID[]   | yes      | Listings included in this run       |
| `openedBy`           | Operator ID    | yes      | Operator who opened payment         |
| `openingMode`        | enum           | yes      | `on_fill` or `manual`               |
| `deadline`           | date           | no       | Payment due date                    |
| `status`             | enum           | yes      | `open`, `completed`, or `cancelled` |
| `openedAt`           | timestamp      | yes      | Opening time                        |

### Buyer Payment Obligation

One buyer's combined payment obligation across all selected listings in a payment run.

| Field                    | Type                                                  | Required | Description                                 |
| ------------------------ | ----------------------------------------------------- | -------- | ------------------------------------------- |
| `id`                     | Obligation ID                                         | yes      | Stable identifier                           |
| `paymentRunId`           | Payment Run ID                                        | yes      | Owning payment run                          |
| `buyerId`                | Buyer ID                                              | yes      | Buyer who owes payment                      |
| `lineItems`              | [Payment Line Item](#payment-line-item)[]             | yes      | Listing/dose traceability                   |
| `expectedAmount`         | [Money Amount](#money-amount)                         | yes      | Sum of line items                           |
| `receivedAmount`         | [Money Amount](#money-amount)                         | no       | Provider/operator-confirmed received amount |
| `providerCorrelationKey` | [Provider Correlation Key](#provider-correlation-key) | no       | Key used by provider/webhook                |
| `status`                 | [Payment Status](#payment-status)                     | yes      | Reconciliation state                        |
| `deadline`               | date                                                  | no       | Obligation deadline copied from payment run |

## Value Objects

### Payment Line Item

Traceable contribution from one listing allocation to a buyer obligation.

| Field          | Type                          | Required | Description                |
| -------------- | ----------------------------- | -------- | -------------------------- |
| `listingId`    | Listing ID                    | yes      | Source listing             |
| `allocationId` | Allocation ID                 | yes      | Source allocation          |
| `slotNumbers`  | positive integer[]            | yes      | Assigned slots             |
| `doseCount`    | positive integer              | yes      | Number of doses            |
| `pricePerDose` | [Money Amount](#money-amount) | yes      | Source listing price       |
| `lineTotal`    | [Money Amount](#money-amount) | yes      | `doseCount * pricePerDose` |

### Provider Correlation Key

Provider-facing identifier used to match callbacks to one buyer payment obligation. Pix implementation uses generated `txid` or provider equivalent.

Rules:

- Unique for active obligations.
- Required before automatic webhook reconciliation can mark payment.
- Duplicate callbacks for the same key are idempotent.

### Money Amount

BRL-denominated amount.

Rules:

- Must be greater than or equal to zero.
- Expected amount is derived from line items.
- Received amount comes from provider callback or manual operator confirmation.

## Enums

### Payment Status

| Value        | Description                                                                       |
| ------------ | --------------------------------------------------------------------------------- |
| `pending`    | Payment is open and waiting for buyer action                                      |
| `processing` | Provider event is being reconciled                                                |
| `paid`       | Received amount exactly satisfies expected amount or operator manually marks paid |
| `partial`    | Received amount is below expected amount                                          |
| `overpaid`   | Received amount is above expected amount                                          |
| `unmatched`  | Provider event cannot be matched to an obligation                                 |
| `failed`     | Reconciliation failed after retry handling                                        |
