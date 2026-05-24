---
feature: dose-payment-tracking
version: current
status: draft
updatedAt: 2026-05-21
docType: states
owners:
  - group operator
---

# Dose Payment Tracking States

## PaymentStatusLifecycle

State machine for [Buyer Payment Obligation](domain.md#buyer-payment-obligation).

| From         | Event or Operation                                             | To           | Guard                                                         |
| ------------ | -------------------------------------------------------------- | ------------ | ------------------------------------------------------------- |
| none         | [PaymentObligationCreated](events.md#paymentobligationcreated) | `pending`    | payment run opened                                            |
| `pending`    | [PaymentWebhookReceived](events.md#paymentwebhookreceived)     | `processing` | correlation key received                                      |
| `processing` | [PaymentReconciled](events.md#paymentreconciled)               | `paid`       | received amount equals expected amount or operator marks paid |
| `processing` | [PaymentReconciled](events.md#paymentreconciled)               | `partial`    | received amount below expected amount                         |
| `processing` | [PaymentReconciled](events.md#paymentreconciled)               | `overpaid`   | received amount above expected amount                         |
| `pending`    | [PaymentExceptionRaised](events.md#paymentexceptionraised)     | `unmatched`  | provider event cannot be matched                              |
| `processing` | [PaymentExceptionRaised](events.md#paymentexceptionraised)     | `failed`     | retry policy exhausted or payload invalid                     |
| `pending`    | [ManualMarkPaid](operations.md#manualmarkpaid)                 | `paid`       | operator confirms paid                                        |
| `partial`    | [ManualMarkPaid](operations.md#manualmarkpaid)                 | `paid`       | operator accepts or corrects remaining amount                 |

Invariants:

- Duplicate provider callbacks for an already terminal obligation do not change state.
- `paid`, `partial`, and `overpaid` all represent matched payment truth but different amount outcomes.
- `unmatched` belongs to a provider event without a clean obligation match.
