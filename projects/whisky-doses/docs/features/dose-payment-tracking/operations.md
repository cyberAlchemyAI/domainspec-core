---
feature: dose-payment-tracking
version: current
status: draft
updatedAt: 2026-05-21
docType: operations
owners:
  - group operator
---

# Dose Payment Tracking Operations

## OpenPaymentRun

Creates a payment run from selected listings and buyer allocations.

| Field   | Value                                                                                                           |
| ------- | --------------------------------------------------------------------------------------------------------------- |
| Actor   | group operator or on-fill trigger                                                                               |
| Trigger | listing fills or operator manually opens payment                                                                |
| Input   | selected listing IDs, deadline, opening mode                                                                    |
| Output  | [Payment Run](domain.md#payment-run) and [Buyer Payment Obligation](domain.md#buyer-payment-obligation) records |

Rules:

- [P1 Payment Opening Policy](rules.md#p1-payment-opening-policy)
- [P2 Payment Run Grouping Policy](rules.md#p2-payment-run-grouping-policy)
- [R1 Payment Eligible Allocation Rule](rules.md#r1-payment-eligible-allocation-rule)

Produces: [PaymentRunOpened](events.md#paymentrunopened), [PaymentObligationCreated](events.md#paymentobligationcreated)

## CalculateBuyerPaymentTotal

Derives a buyer obligation total from line items.

Inputs:

- payment line items

Formula: [C1 Buyer Payment Total](rules.md#c1-buyer-payment-total)

Output:

- expected amount

## AttachProviderCorrelationKey

Stores the provider correlation key generated for a buyer obligation.

| Field   | Value                                                   |
| ------- | ------------------------------------------------------- |
| Actor   | Payment Link And Reminder Messaging or provider adapter |
| Trigger | payment link/QR is generated                            |
| Input   | obligation ID, provider correlation key                 |
| Output  | obligation can be reconciled automatically              |

Boundary rule: this operation attaches correlation data only; Payment Link And Reminder Messaging owns buyer-facing link text and delivery.

## ApplyPixWebhook

Processes a Pix/provider callback.

| Field   | Value                                                                                |
| ------- | ------------------------------------------------------------------------------------ |
| Actor   | Pix provider webhook                                                                 |
| Trigger | provider notifies payment event                                                      |
| Input   | provider correlation key, received amount, provider transaction ID, callback payload |
| Output  | updated obligation status or unmatched/failed exception                              |

Rules:

- [R2 Correlation Idempotency Rule](rules.md#r2-correlation-idempotency-rule)
- [R3 Amount Match Rule](rules.md#r3-amount-match-rule)
- [R4 Provider Correlation Required Rule](rules.md#r4-provider-correlation-required-rule)

Produces: [PaymentWebhookReceived](events.md#paymentwebhookreceived), [PaymentReconciled](events.md#paymentreconciled) or [PaymentExceptionRaised](events.md#paymentexceptionraised)

## RetryReconciliation

Retries technical reconciliation failures from scheduled jobs.

| Field   | Value                                      |
| ------- | ------------------------------------------ |
| Actor   | scheduled job / cron                       |
| Trigger | retryable webhook processing failure       |
| Input   | failed reconciliation attempt ID           |
| Output  | reconciled payment or UI-visible exception |

Postconditions:

- Retryable failures remain scheduled until retry policy ends.
- Non-retryable failures become `failed` or `unmatched`.

## ManualMarkPaid

Operator fallback that marks an obligation paid.

| Field   | Value                                                                                             |
| ------- | ------------------------------------------------------------------------------------------------- |
| Actor   | group operator                                                                                    |
| Trigger | webhook missing, failed, or intentionally overridden                                              |
| Input   | obligation ID, received amount, audit reason                                                      |
| Output  | obligation status becomes `paid`, `partial`, or `overpaid` according to operator-selected outcome |

Rules:

- [P3 Manual Fallback Policy](rules.md#p3-manual-fallback-policy)

Produces: [PaymentReconciled](events.md#paymentreconciled)
