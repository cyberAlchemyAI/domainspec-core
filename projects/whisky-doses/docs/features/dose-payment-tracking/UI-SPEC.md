---
id: dose-payment-tracking-ui
feature: dose-payment-tracking
title: "Dose Payment Tracking UI Specification"
summary: Operator UI for payment runs, buyer obligations, provider reconciliation status, exceptions, and manual fallback.
status: draft
pillar: operations
domain: dose-payment-tracking-ui
audience:
  - developers
priority: p0
lang: en
owners:
  - web-core
updatedAt: 2026-05-21
dependencies:
  - SPEC.md
  - interfaces.md
  - operations.md
  - queries.md
  - states.md
  - STORIES.md
includes: []
constitution: docs/UI-ARCHITECTURE.md
---

# UI Specification: Dose Payment Tracking

Governs the frontend presentation of payment run opening, buyer obligations, payment status, reconciliation exceptions, and manual fallback.

Constrained by [UI-ARCHITECTURE.md](../../UI-ARCHITECTURE.md).

## Route Table

| Route                          | Page Title         | Layout   | Auth Required | Permission     |
| ------------------------------ | ------------------ | -------- | ------------- | -------------- |
| `/payment-runs`                | Payment Runs       | AppShell | Yes           | group operator |
| `/payment-runs/{paymentRunId}` | Payment Run Detail | AppShell | Yes           | group operator |
| `/payment-exceptions`          | Payment Exceptions | AppShell | Yes           | group operator |

## Page Layouts

### `/payment-runs` Payment Runs

```text
┌──────────────────────────────────────────────────────────────┐
│ Header: Payment Runs                  [Open Payment Run]     │
├──────────────────────────────────────────────────────────────┤
│ Filters: listing, status, deadline                           │
├──────────────────────────────────────────────────────────────┤
│ PaymentRunTable                                              │
│ Run | Listings | Deadline | Obligations | Exceptions | Action │
└──────────────────────────────────────────────────────────────┘
```

Primary purpose:

- Open payment for selected listings.
- Review payment runs and exception counts.

### `/payment-runs/{paymentRunId}` Payment Run Detail

```text
┌──────────────────────────────────────────────────────────────┐
│ Header: Payment Run Detail             [Generate Links later]│
├──────────────────────────────────────────────────────────────┤
│ PaymentRunSummary                                            │
├──────────────────────────────────────────────────────────────┤
│ ObligationTable                                              │
│ Buyer | Expected | Received | Status | Line Items | Actions   │
└──────────────────────────────────────────────────────────────┘
```

Primary purpose:

- Inspect buyer obligations and totals.
- Attach provider correlation key through integration.
- Manually mark paid when fallback is needed.

### `/payment-exceptions` Payment Exceptions

```text
┌──────────────────────────────────────────────────────────────┐
│ Header: Payment Exceptions                                   │
├──────────────────────────────────────────────────────────────┤
│ Exception filters: status, listing, payment run              │
├──────────────────────────────────────────────────────────────┤
│ ExceptionQueue                                               │
│ Buyer | Expected | Received | Exception | Next Action        │
└──────────────────────────────────────────────────────────────┘
```

Primary purpose:

- Surface `partial`, `overpaid`, `unmatched`, and `failed` reconciliation work.
- Guide operator fallback without hiding exception status.

## Component Inventory

| Component              | Type            | Location                                                    | Purpose                                                      |
| ---------------------- | --------------- | ----------------------------------------------------------- | ------------------------------------------------------------ |
| `OpenPaymentRunDialog` | Dialog/Form     | `components/dose-payment-tracking/OpenPaymentRunDialog.tsx` | Selects listings, deadline, and opening mode                 |
| `PaymentRunTable`      | Table           | `components/dose-payment-tracking/PaymentRunTable.tsx`      | Lists payment runs and exception counts                      |
| `PaymentRunSummary`    | Detail panel    | `components/dose-payment-tracking/PaymentRunSummary.tsx`    | Shows selected listings, deadline, totals, and status counts |
| `ObligationTable`      | Table           | `components/dose-payment-tracking/ObligationTable.tsx`      | Shows buyer obligations, amounts, statuses, and line items   |
| `PaymentStatusBadge`   | State indicator | `components/dose-payment-tracking/PaymentStatusBadge.tsx`   | Displays payment status                                      |
| `ManualMarkPaidDialog` | Dialog/Form     | `components/dose-payment-tracking/ManualMarkPaidDialog.tsx` | Applies operator fallback with audit reason                  |
| `CorrelationKeyPanel`  | Detail panel    | `components/dose-payment-tracking/CorrelationKeyPanel.tsx`  | Displays attached provider correlation key state             |
| `ExceptionQueue`       | Table           | `components/dose-payment-tracking/ExceptionQueue.tsx`       | Lists payment exceptions requiring operator attention        |
| `ExceptionNextAction`  | Action cell     | `components/dose-payment-tracking/ExceptionNextAction.tsx`  | Shows retry/fallback guidance from exception read model      |

## Data Flow

### `/payment-runs`

| API Call                           | Hook                          | Cache Key                                             | Triggers                |
| ---------------------------------- | ----------------------------- | ----------------------------------------------------- | ----------------------- |
| `GET /payment-runs/{paymentRunId}` | `usePaymentRun(paymentRunId)` | `queryKeys.paymentRuns.detail(paymentRunId)`          | Linked detail reads     |
| `POST /payment-runs`               | `useOpenPaymentRun()`         | invalidates payment run and listing payment summaries | Open payment run submit |

Implementation note: if no list endpoint exists yet, the first UI implementation may source recent run navigation from created-run responses and direct detail routes. A future list endpoint can extend this route without changing obligation behavior.

### `/payment-runs/{paymentRunId}`

| API Call                                                   | Hook                                | Cache Key                                     | Triggers                     |
| ---------------------------------------------------------- | ----------------------------------- | --------------------------------------------- | ---------------------------- |
| `GET /payment-runs/{paymentRunId}`                         | `usePaymentRun(paymentRunId)`       | `queryKeys.paymentRuns.detail(paymentRunId)`  | Page mount, mutation success |
| `POST /payment-obligations/{obligationId}/correlation-key` | `useAttachProviderCorrelationKey()` | invalidates payment run detail                | Provider/link integration    |
| `POST /payment-obligations/{obligationId}/manual-paid`     | `useManualMarkPaid()`               | invalidates payment run detail and exceptions | Manual fallback submit       |

### `/payment-exceptions`

| API Call                                               | Hook                     | Cache Key                                     | Triggers                                          |
| ------------------------------------------------------ | ------------------------ | --------------------------------------------- | ------------------------------------------------- |
| `GET /payment-exceptions`                              | `usePaymentExceptions()` | `queryKeys.paymentExceptions.list(filters)`   | Page mount, filter changes, reconciliation events |
| `POST /payment-obligations/{obligationId}/manual-paid` | `useManualMarkPaid()`    | invalidates exceptions and payment run detail | Manual fallback submit                            |

## Form Contracts

### OpenPaymentRunForm

| Field         | Type     | HTML Input        | Validation                       | Error Message                    |
| ------------- | -------- | ----------------- | -------------------------------- | -------------------------------- |
| `listingIds`  | string[] | multi-select      | At least one listing             | "Choose at least one listing."   |
| `deadline`    | date     | date input        | Required for collection deadline | "Payment deadline is required."  |
| `openingMode` | enum     | segmented control | `on_fill` or `manual`            | "Choose a payment opening mode." |

Zod schema intent:

```typescript
z.object({
  listingIds: z.array(z.string()).min(1, "Choose at least one listing."),
  deadline: z.string().min(1, "Payment deadline is required."),
  openingMode: z.enum(["on_fill", "manual"]),
});
```

### AttachProviderCorrelationKeyForm

| Field                    | Type   | HTML Input     | Validation | Error Message                           |
| ------------------------ | ------ | -------------- | ---------- | --------------------------------------- |
| `obligationId`           | string | hidden/context | Required   | "Obligation is required."               |
| `providerCorrelationKey` | string | text           | Required   | "Provider correlation key is required." |

### ManualMarkPaidForm

| Field            | Type   | HTML Input        | Validation                       | Error Message                        |
| ---------------- | ------ | ----------------- | -------------------------------- | ------------------------------------ |
| `obligationId`   | string | hidden/context    | Required                         | "Obligation is required."            |
| `receivedAmount` | number | number            | Non-negative BRL amount          | "Received amount must be valid."     |
| `auditReason`    | string | textarea          | Required                         | "Audit reason is required."          |
| `outcome`        | enum   | segmented control | `paid`, `partial`, or `overpaid` | "Choose the reconciliation outcome." |

## Error Code To UI Message Mapping

| API Condition                      | HTTP Status | UI Message                                                           |
| ---------------------------------- | ----------- | -------------------------------------------------------------------- |
| Empty or invalid listing selection | 400         | "Choose listings with active allocations before opening payment."    |
| Unsupported opening mode           | 400         | "Payment can open on fill or by manual action only."                 |
| Missing provider correlation key   | 400         | "Attach a provider correlation key before automatic reconciliation." |
| Duplicate webhook callback         | 200         | "Callback was already processed; no payment state changed."          |
| Unmatched provider callback        | 400         | "Provider callback could not be matched to one obligation."          |
| Retry exhausted                    | 400         | "Reconciliation failed after retries and needs operator attention."  |
| Missing manual audit reason        | 400         | "Add an audit reason before manually marking paid."                  |

## State To UI Mapping

| Domain Value | UI Representation  | Color / Variant   |
| ------------ | ------------------ | ----------------- |
| `pending`    | Badge "Pending"    | amber / warning   |
| `processing` | Badge "Processing" | blue / info       |
| `paid`       | Badge "Paid"       | green / default   |
| `partial`    | Badge "Partial"    | amber / warning   |
| `overpaid`   | Badge "Overpaid"   | blue / info       |
| `unmatched`  | Badge "Unmatched"  | red / destructive |
| `failed`     | Badge "Failed"     | red / destructive |

## Story To UI Mapping

| Story                                                                    | UI Surface                            | Notes                                            |
| ------------------------------------------------------------------------ | ------------------------------------- | ------------------------------------------------ |
| [DP-S1](STORIES.md#dp-s1-open-payment-run-from-selected-listings)        | OpenPaymentRunDialog, PaymentRunTable | Opens payment from selected listing allocations  |
| [DP-S2](STORIES.md#dp-s2-review-buyer-obligations-and-totals)            | PaymentRunSummary, ObligationTable    | Shows obligations, line items, expected totals   |
| [DP-S3](STORIES.md#dp-s3-attach-provider-correlation-key)                | CorrelationKeyPanel                   | Displays/attaches provider correlation key state |
| [DP-S4](STORIES.md#dp-s4-reconcile-pix-webhook-idempotently)             | ObligationTable, PaymentStatusBadge   | Shows reconciled status outcomes                 |
| [DP-S5](STORIES.md#dp-s5-surface-reconciliation-exceptions)              | ExceptionQueue, ExceptionNextAction   | Lists partial/overpaid/unmatched/failed          |
| [DP-S6](STORIES.md#dp-s6-manually-mark-paid-as-fallback)                 | ManualMarkPaidDialog                  | Operator fallback with audit reason              |
| [DP-S7](STORIES.md#dp-s7-expose-payment-truth-to-rendering-and-shipment) | PaymentRunSummary, ObligationTable    | Shows authoritative payment truth                |

## Accessibility Requirements

| Component              | Requirement                                                          |
| ---------------------- | -------------------------------------------------------------------- |
| `PaymentRunTable`      | Semantic `<table>` with column headers and visible row actions       |
| `OpenPaymentRunDialog` | `aria-modal="true"`, focus trap, Esc to close                        |
| `ObligationTable`      | Amounts and statuses are text-visible, not color-only                |
| `PaymentStatusBadge`   | Includes accessible label explaining status                          |
| `ManualMarkPaidDialog` | Destructive/manual fallback action requires confirmation context     |
| `ExceptionQueue`       | Exception severity is represented with text and icon, not color only |

## UI Concept Registry

| Concept                        | ID                                                 | Type            |
| ------------------------------ | -------------------------------------------------- | --------------- |
| `/payment-runs`                | `ui.dose-payment-tracking.payment-runs-page`       | Page            |
| `/payment-runs/{paymentRunId}` | `ui.dose-payment-tracking.payment-run-detail-page` | Page            |
| `/payment-exceptions`          | `ui.dose-payment-tracking.payment-exceptions-page` | Page            |
| `OpenPaymentRunDialog`         | `ui.dose-payment-tracking.OpenPaymentRunDialog`    | Form            |
| `PaymentRunTable`              | `ui.dose-payment-tracking.PaymentRunTable`         | Component       |
| `PaymentRunSummary`            | `ui.dose-payment-tracking.PaymentRunSummary`       | Component       |
| `ObligationTable`              | `ui.dose-payment-tracking.ObligationTable`         | Component       |
| `PaymentStatusBadge`           | `ui.dose-payment-tracking.PaymentStatusBadge`      | State Indicator |
| `ManualMarkPaidDialog`         | `ui.dose-payment-tracking.ManualMarkPaidDialog`    | Form            |
| `CorrelationKeyPanel`          | `ui.dose-payment-tracking.CorrelationKeyPanel`     | Component       |
| `ExceptionQueue`               | `ui.dose-payment-tracking.ExceptionQueue`          | Component       |
| `usePaymentRun`                | `ui.dose-payment-tracking.usePaymentRun`           | Hook / Binding  |
| `usePaymentExceptions`         | `ui.dose-payment-tracking.usePaymentExceptions`    | Hook / Binding  |

## Checker Result

Status: PASS

Reason: UI-SPEC is constrained by `docs/UI-ARCHITECTURE.md`, maps payment run opening, buyer obligations, webhook reconciliation states, exceptions, manual fallback, and downstream payment-truth read models without assigning payment-link messaging or WhatsApp posting ownership to this feature.
