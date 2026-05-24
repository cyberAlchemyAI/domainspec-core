---
feature: dose-payment-tracking
version: current
status: draft
updatedAt: 2026-05-21
docType: interfaces
owners:
  - group operator
---

# Dose Payment Tracking Interfaces

## External PaymentTrackingAPI REST

Operator-facing REST surface.

| Endpoint                                              | Method | Exposes                                                                    | Notes                                     |
| ----------------------------------------------------- | ------ | -------------------------------------------------------------------------- | ----------------------------------------- |
| `/payment-runs`                                       | POST   | [OpenPaymentRun](operations.md#openpaymentrun)                             | Opens payment for selected listings       |
| `/payment-obligations/{obligationId}/correlation-key` | POST   | [AttachProviderCorrelationKey](operations.md#attachprovidercorrelationkey) | Stores provider key after link generation |
| `/payment-obligations/{obligationId}/manual-paid`     | POST   | [ManualMarkPaid](operations.md#manualmarkpaid)                             | Operator fallback                         |
| `/payment-runs/{paymentRunId}`                        | GET    | [GetPaymentRun](queries.md#getpaymentrun)                                  | Reads run                                 |
| `/payment-exceptions`                                 | GET    | [GetPaymentExceptions](queries.md#getpaymentexceptions)                    | Reads operator attention queue            |

## External PixWebhook Interface

Provider callback surface.

| Endpoint        | Method | Exposes                                          | Notes                                          |
| --------------- | ------ | ------------------------------------------------ | ---------------------------------------------- |
| `/webhooks/pix` | POST   | [ApplyPixWebhook](operations.md#applypixwebhook) | Must be idempotent by provider correlation key |

Payload requirements:

- provider correlation key (`txid` or equivalent)
- provider transaction ID
- received amount
- event timestamp
- raw payload for audit

## Internal PaymentTrackingModule Interface

Cross-feature read contract.

| Method                                    | Exposes                                                         | Consumer                            |
| ----------------------------------------- | --------------------------------------------------------------- | ----------------------------------- |
| `getListingPaymentSummary(listingId)`     | [GetListingPaymentSummary](queries.md#getlistingpaymentsummary) | Public WhatsApp List Rendering      |
| `getBuyerPaymentStatus(buyerId, filters)` | [GetBuyerPaymentStatus](queries.md#getbuyerpaymentstatus)       | Freight And Shipment Batching       |
| `getPaymentRun(paymentRunId)`             | [GetPaymentRun](queries.md#getpaymentrun)                       | Payment Link And Reminder Messaging |
| `getPaymentExceptions(filters)`           | [GetPaymentExceptions](queries.md#getpaymentexceptions)         | Operator UI / notifications         |

## Dependency BottleListingModule Interface

Required upstream interface from [Bottle Listing And Dose Allocation](../bottle-listing-and-dose-allocation/interfaces.md#internal-bottlelistingmodule-interface).

| Method                                      | Used By                                                    | Why                                     |
| ------------------------------------------- | ---------------------------------------------------------- | --------------------------------------- |
| `getPaymentEligibleAllocations(listingIds)` | [OpenPaymentRun](operations.md#openpaymentrun)             | Builds buyer obligations and line items |
| `getListingAllocationSummary(listingId)`    | [PaymentOpeningPolicy](rules.md#p1-payment-opening-policy) | Confirms on-fill opening conditions     |
