---
feature: dose-payment-tracking
version: current
status: draft
updatedAt: 2026-05-21
docType: glossary
owners:
  - group operator
---

# Dose Payment Tracking Glossary

| Term                        | Definition                                                                                                                | Source                                                                           |
| --------------------------- | ------------------------------------------------------------------------------------------------------------------------- | -------------------------------------------------------------------------------- |
| Payment Run                 | Operator-opened collection event for selected listings.                                                                   | [domain.md#payment-run](domain.md#payment-run)                                   |
| Buyer Payment Obligation    | One buyer's combined amount due across the selected listings in a payment run.                                            | [domain.md#buyer-payment-obligation](domain.md#buyer-payment-obligation)         |
| Payment Line Item           | Traceable listing/allocation contribution to an obligation.                                                               | [domain.md#payment-line-item](domain.md#payment-line-item)                       |
| Provider Correlation Key    | Generated identifier, such as Pix `txid`, used to match provider callbacks to an obligation.                              | [domain.md#provider-correlation-key](domain.md#provider-correlation-key)         |
| Payment Status              | Reconciliation state for an obligation: `pending`, `processing`, `paid`, `partial`, `overpaid`, `unmatched`, or `failed`. | [domain.md#payment-status](domain.md#payment-status)                             |
| Payment Reconciliation Saga | Retryable process that turns provider callbacks into payment truth or UI-visible exceptions.                              | [workflows.md#paymentreconciliationsaga](workflows.md#paymentreconciliationsaga) |
| Manual Fallback             | Operator action that marks an obligation paid when automatic reconciliation is absent or exceptional.                     | [rules.md#p3-manual-fallback-policy](rules.md#p3-manual-fallback-policy)         |
