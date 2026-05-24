---
feature: dose-payment-tracking
version: current
status: draft
updatedAt: 2026-05-21
docType: rules
owners:
  - group operator
---

# Dose Payment Tracking Rules

## Policies

### P1 Payment Opening Policy

V1 supports opening payment on listing fill or by manual operator action.

Selection:

- `on_fill`: payment may open when all selected listing slots are filled by derivation.
- `manual`: payment opens only when the operator explicitly opens a run.

Immediate-on-allocation payment is outside v1.

### P2 Payment Run Grouping Policy

The operator selects one or more listings for a payment run. For each buyer with active allocations in selected listings, the system creates one combined buyer obligation with line items for each source listing/allocation.

### P3 Manual Fallback Policy

The operator may manually mark an obligation paid when provider reconciliation is missing, failed, or operationally overridden.

Requirements:

- Manual mark must include operator identity and audit reason.
- Manual mark changes payment truth but does not create provider evidence.

## Rules

### R1 Payment Eligible Allocation Rule

Only active allocations from selected listings can be included in a payment run.

Formal expression:

```text
lineItems.all(item.listingId in selectedListingIds && item.allocationStatus == "active")
```

Enforces: [OpenPaymentRun](operations.md#openpaymentrun)

### R2 Correlation Idempotency Rule

A provider callback with the same provider correlation key must not apply more than once.

Formal expression:

```text
processedCallbacks.where(correlationKey == callback.correlationKey).count <= 1
```

Enforces: [ApplyPixWebhook](operations.md#applypixwebhook)

### R3 Amount Match Rule

Received amount determines the reconciled status.

Decision table:

| Condition                          | Status     |
| ---------------------------------- | ---------- |
| `receivedAmount == expectedAmount` | `paid`     |
| `receivedAmount < expectedAmount`  | `partial`  |
| `receivedAmount > expectedAmount`  | `overpaid` |

Enforces: [ApplyPixWebhook](operations.md#applypixwebhook)

### R4 Provider Correlation Required Rule

Automatic reconciliation requires a provider correlation key tied to one obligation.

Formal expression:

```text
callback.correlationKey != null
&& obligations.where(providerCorrelationKey == callback.correlationKey).count == 1
```

Enforces: [ApplyPixWebhook](operations.md#applypixwebhook)

## Calculations

### C1 Buyer Payment Total

Formula:

```text
expectedAmount = sum(lineItems.map(item => item.doseCount * item.pricePerDose))
```

Properties:

- Deterministic for the selected listing allocation snapshot.
- Preserves line-item traceability for later review.
