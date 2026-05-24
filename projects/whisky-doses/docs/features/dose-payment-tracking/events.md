---
feature: dose-payment-tracking
version: current
status: draft
updatedAt: 2026-05-21
docType: events
owners:
  - group operator
---

# Dose Payment Tracking Events

## PaymentRunOpened

Produced by: [OpenPaymentRun](operations.md#openpaymentrun)

Payload:

- `paymentRunId`
- selected listing IDs
- deadline
- openedAt

Consumers:

- Payment Link And Reminder Messaging generates buyer-facing payment link text.

## PaymentObligationCreated

Produced by: [OpenPaymentRun](operations.md#openpaymentrun)

Payload:

- `paymentRunId`
- `obligationId`
- `buyerId`
- expected amount
- line items

Consumers:

- Payment Link And Reminder Messaging generates one link/instruction per obligation.

## PaymentWebhookReceived

Produced by: [ApplyPixWebhook](operations.md#applypixwebhook)

Payload:

- provider correlation key
- provider transaction ID
- received amount
- callback timestamp

Consumers:

- Reconciliation saga.

## PaymentReconciled

Produced by: [ApplyPixWebhook](operations.md#applypixwebhook) or [ManualMarkPaid](operations.md#manualmarkpaid)

Payload:

- `obligationId`
- `buyerId`
- expected amount
- received amount
- resulting status
- source: `provider` or `manual`

Consumers:

- Public WhatsApp List Rendering refreshes buyer-level paid/unpaid snippets.
- Payment Link And Reminder Messaging stops or suppresses reminders.
- Freight And Shipment Batching can treat dose payment as satisfied when status permits.

## PaymentExceptionRaised

Produced by: [ApplyPixWebhook](operations.md#applypixwebhook) or [RetryReconciliation](operations.md#retryreconciliation)

Payload:

- exception type: `partial`, `overpaid`, `unmatched`, or `failed`
- obligation ID when matched
- provider correlation key when available
- reason

Consumers:

- Operator UI / notification surface.
