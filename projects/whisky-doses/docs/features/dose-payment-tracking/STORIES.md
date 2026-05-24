---
feature: dose-payment-tracking
version: current
status: draft
updatedAt: 2026-05-21
docType: stories
owners:
  - group operator
---

# Dose Payment Tracking Stories

## Story Set

These stories mirror the Dose Payment Tracking capabilities in [SPEC.md](SPEC.md#capabilities) and preserve coverage across public, admin/operations, cross-feature integration, and edge-case journeys.

## DP-S1 Open Payment Run From Selected Listings

Capability: [Payment Run Opening](SPEC.md#capabilities)
Journey type: admin/operations
Concept links: [Payment Run](domain.md#payment-run), [OpenPaymentRun](operations.md#openpaymentrun), [PaymentOpeningPolicy](rules.md#p1-payment-opening-policy)

Classic story:
As a group operator, I want to open payment for one or more selected listings, so that buyers receive one combined obligation across their allocated doses.

BDD scenario:
Given selected listings have active allocations
When payment opens by on-fill trigger or manual operator action
Then a payment run is created
And one buyer payment obligation is created per buyer
And obligation line items preserve listing and allocation traceability.

Acceptance checks:

- Payment can open on fill or by manual action.
- Only active allocations from selected listings are included.
- Buyer obligations group selected listing allocations by buyer.
- [PaymentRunOpened](events.md#paymentrunopened) and [PaymentObligationCreated](events.md#paymentobligationcreated) are emitted.

## DP-S2 Review Buyer Obligations And Totals

Capability: [Buyer Obligation Tracking](SPEC.md#capabilities)
Journey type: public
Concept links: [Buyer Payment Obligation](domain.md#buyer-payment-obligation), [Payment Line Item](domain.md#payment-line-item), [CalculateBuyerPaymentTotal](operations.md#calculatebuyerpaymenttotal)

Classic story:
As a group operator, I want to review each buyer's owed amount and line items, so that payment collection can be checked before links or reminders are generated.

BDD scenario:
Given a payment run exists
When the operator opens the payment run
Then the UI shows buyer obligations, expected amount, status, deadline, and line items
And totals are derived from dose count times price per dose.

Acceptance checks:

- Obligation totals match [Buyer Payment Total](rules.md#c1-buyer-payment-total).
- Line items preserve listing/dose traceability.
- Payment status is visible next to each buyer obligation.
- Exception counts are visible in the payment run summary.

## DP-S3 Attach Provider Correlation Key

Capability: [Pix Reconciliation](SPEC.md#capabilities)
Journey type: cross-feature integration
Concept links: [Provider Correlation Key](domain.md#provider-correlation-key), [AttachProviderCorrelationKey](operations.md#attachprovidercorrelationkey), [PaymentTrackingModule](interfaces.md#internal-paymenttrackingmodule-interface)

Classic story:
As Payment Link And Reminder Messaging, I want to attach a provider correlation key to an obligation, so that Pix webhook callbacks can reconcile automatically.

BDD scenario:
Given a payment link or Pix payload was generated for an obligation
When the messaging feature attaches the provider correlation key
Then the obligation can be matched by future provider callbacks
And no buyer-facing message text is owned by payment tracking.

Acceptance checks:

- Correlation key is stored under the payment truth owner.
- Attachment does not mark payment paid.
- Attachment does not generate or send buyer-facing messages.
- Future callbacks can match the obligation by key.

## DP-S4 Reconcile Pix Webhook Idempotently

Capability: [Pix Reconciliation](SPEC.md#capabilities)
Journey type: admin/operations
Concept links: [ApplyPixWebhook](operations.md#applypixwebhook), [CorrelationIdempotencyRule](rules.md#r2-correlation-idempotency-rule), [AmountMatchRule](rules.md#r3-amount-match-rule)

Classic story:
As the system, I want to process Pix webhook callbacks idempotently, so that payment status reflects provider evidence without double-applying duplicate callbacks.

BDD scenario:
Given a provider callback contains a correlation key and received amount
When the callback is applied
Then a matching obligation moves through processing
And the received amount classifies the obligation as paid, partial, or overpaid
And duplicate callbacks do not change state twice.

Acceptance checks:

- Matching callback records [PaymentWebhookReceived](events.md#paymentwebhookreceived).
- Equal amount becomes `paid`.
- Lower amount becomes `partial`.
- Higher amount becomes `overpaid`.
- Duplicate callback does not double-apply payment.

## DP-S5 Surface Reconciliation Exceptions

Capability: [Payment Truth Read Models](SPEC.md#capabilities)
Journey type: edge-case
Concept links: [GetPaymentExceptions](queries.md#getpaymentexceptions), [PaymentExceptionRaised](events.md#paymentexceptionraised), [PaymentStatusLifecycle](states.md#paymentstatuslifecycle)

Classic story:
As a group operator, I want to see unmatched, failed, partial, and overpaid payment exceptions, so that I can resolve payment issues before reminders, rendering, or shipment rely on stale truth.

BDD scenario:
Given reconciliation cannot match a callback or finds an exception amount
When the operator opens payment exceptions
Then each exception shows obligation, buyer, expected amount, received amount, reason, and next action hint.

Acceptance checks:

- `partial`, `overpaid`, `unmatched`, and `failed` statuses appear in exception views.
- Retry exhaustion produces a UI-visible exception.
- Exception query does not mutate payment truth.
- Operator can select an obligation for manual fallback when allowed.

## DP-S6 Manually Mark Paid As Fallback

Capability: [Manual Fallback](SPEC.md#capabilities)
Journey type: edge-case
Concept links: [ManualMarkPaid](operations.md#manualmarkpaid), [ManualFallbackPolicy](rules.md#p3-manual-fallback-policy), [PaymentReconciled](events.md#paymentreconciled)

Classic story:
As a group operator, I want to manually mark an obligation paid with an audit reason, so that payment truth can recover when webhook reconciliation is missing or failed.

BDD scenario:
Given an obligation needs manual resolution
When the operator marks it paid with received amount and audit reason
Then payment truth updates according to the selected outcome
And [PaymentReconciled](events.md#paymentreconciled) is emitted with source `manual`.

Acceptance checks:

- Manual paid marking requires operator identity and audit reason.
- Manual fallback can move pending or partial obligations to paid when allowed.
- Manual fallback does not create provider evidence.
- Downstream consumers can treat paid obligations as satisfied.

## DP-S7 Expose Payment Truth To Rendering And Shipment

Capability: [Payment Truth Read Models](SPEC.md#capabilities)
Journey type: cross-feature integration
Concept links: [GetBuyerPaymentStatus](queries.md#getbuyerpaymentstatus), [GetListingPaymentSummary](queries.md#getlistingpaymentsummary), [PaymentTrackingModule](interfaces.md#internal-paymenttrackingmodule-interface)

Classic story:
As a downstream rendering, reminder, or shipment feature, I want authoritative payment status read models, so that public status, reminder suppression, and shipment readiness use payment truth.

BDD scenario:
Given payment obligations exist
When a downstream feature queries buyer or listing payment status
Then it receives obligation IDs, expected amount, received amount, status, line items, and deadline when available
And no downstream feature changes payment truth through read models.

Acceptance checks:

- Listing summary exposes buyer-level payment status for public rendering.
- Buyer payment status supports shipment readiness decisions.
- Payment run read model supports payment-link generation and reminders.
- Read models are authoritative for payment status.

## Story Coverage Matrix

| Capability                | Stories                                                                                                           | Coverage                                    |
| ------------------------- | ----------------------------------------------------------------------------------------------------------------- | ------------------------------------------- |
| Payment Run Opening       | [DP-S1](#dp-s1-open-payment-run-from-selected-listings)                                                           | admin/operations                            |
| Buyer Obligation Tracking | [DP-S2](#dp-s2-review-buyer-obligations-and-totals)                                                               | public                                      |
| Pix Reconciliation        | [DP-S3](#dp-s3-attach-provider-correlation-key), [DP-S4](#dp-s4-reconcile-pix-webhook-idempotently)               | admin/operations, cross-feature integration |
| Manual Fallback           | [DP-S6](#dp-s6-manually-mark-paid-as-fallback)                                                                    | edge-case                                   |
| Payment Truth Read Models | [DP-S5](#dp-s5-surface-reconciliation-exceptions), [DP-S7](#dp-s7-expose-payment-truth-to-rendering-and-shipment) | edge-case, cross-feature integration        |

## Concept Coverage Matrix

| Concept                                              | Covered By                        | Notes                           |
| ---------------------------------------------------- | --------------------------------- | ------------------------------- |
| `dose-payment-tracking.PaymentRun`                   | DP-S1, DP-S2                      | Run lifecycle and read model    |
| `dose-payment-tracking.BuyerPaymentObligation`       | DP-S1, DP-S2, DP-S6               | Buyer-level payment truth       |
| `dose-payment-tracking.PaymentLineItem`              | DP-S1, DP-S2, DP-S7               | Listing/dose traceability       |
| `dose-payment-tracking.ProviderCorrelationKey`       | DP-S3, DP-S4                      | Webhook matching                |
| `dose-payment-tracking.PaymentStatus`                | DP-S2, DP-S4, DP-S5, DP-S6, DP-S7 | Status display and transitions  |
| `dose-payment-tracking.OpenPaymentRun`               | DP-S1                             | Run creation                    |
| `dose-payment-tracking.CalculateBuyerPaymentTotal`   | DP-S2                             | Amount derivation               |
| `dose-payment-tracking.AttachProviderCorrelationKey` | DP-S3                             | Link/reconciliation integration |
| `dose-payment-tracking.ApplyPixWebhook`              | DP-S4                             | Provider reconciliation         |
| `dose-payment-tracking.RetryReconciliation`          | DP-S5                             | Technical failure recovery      |
| `dose-payment-tracking.ManualMarkPaid`               | DP-S6                             | Operator fallback               |
| `dose-payment-tracking.GetPaymentRun`                | DP-S2, DP-S3                      | Run detail                      |
| `dose-payment-tracking.GetBuyerPaymentStatus`        | DP-S7                             | Shipment and buyer status       |
| `dose-payment-tracking.GetListingPaymentSummary`     | DP-S7                             | Public rendering                |
| `dose-payment-tracking.GetPaymentExceptions`         | DP-S5, DP-S6                      | Exception queue                 |
| `dose-payment-tracking.PaymentTrackingAPI`           | DP-S1, DP-S3, DP-S6               | Operator/API surface            |
| `dose-payment-tracking.PaymentTrackingModule`        | DP-S3, DP-S7                      | Cross-feature contract          |

## Drift Warnings

No story drift warnings identified.

## Unresolved Questions

No unresolved story questions.
