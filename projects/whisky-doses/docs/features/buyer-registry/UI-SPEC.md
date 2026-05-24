---
id: buyer-registry-ui
feature: buyer-registry
title: "Buyer Registry UI Specification"
summary: Operator UI for buyer identity, reservation eligibility, shipping readiness, and retention handling.
status: draft
pillar: operations
domain: buyer-registry-ui
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

# UI Specification: Buyer Registry

Governs the frontend presentation of buyer identity, reservation eligibility, shipping readiness, and retention handling.

Constrained by [UI-ARCHITECTURE.md](../../UI-ARCHITECTURE.md).

## Route Table

| Route               | Page Title   | Layout   | Auth Required | Permission     |
| ------------------- | ------------ | -------- | ------------- | -------------- |
| `/buyers`           | Buyers       | AppShell | Yes           | group operator |
| `/buyers/{buyerId}` | Buyer Detail | AppShell | Yes           | group operator |

## Page Layouts

### `/buyers` Buyers

```text
┌──────────────────────────────────────────────────────────────┐
│ Header: Buyers                          [Register Buyer]    │
├──────────────────────────────────────────────────────────────┤
│ Search / Status Filter                                      │
├──────────────────────────────────────────────────────────────┤
│ BuyerTable                                                   │
│ Name | WhatsApp | Status | Reservation | Shipping | Actions  │
└──────────────────────────────────────────────────────────────┘
```

Primary purpose:

- Search active buyers by name or WhatsApp mention.
- Register new buyers.
- Surface reservation eligibility and shipping readiness at scan speed.

### `/buyers/{buyerId}` Buyer Detail

```text
┌──────────────────────────────────────────────────────────────┐
│ Header: Buyer Detail                    [Edit Identity]      │
├──────────────────────────────────────────────────────────────┤
│ BuyerSummaryPanel                                            │
│ Identity fields, status, eligibility badges                  │
├──────────────────────────────────────────────────────────────┤
│ ShippingAddressPanel                    [Set Address]        │
├──────────────────────────────────────────────────────────────┤
│ RetentionPanel                         [Mark Inactive]       │
└──────────────────────────────────────────────────────────────┘
```

Primary purpose:

- Inspect one buyer.
- Correct identity.
- Add or replace shipping address.
- Mark inactive and apply retention action.

## Component Inventory

| Component                 | Type              | Location                                                | Purpose                                                       |
| ------------------------- | ----------------- | ------------------------------------------------------- | ------------------------------------------------------------- |
| `BuyerTable`              | Table             | `components/buyer-registry/BuyerTable.tsx`              | Lists buyer summaries with eligibility and readiness badges   |
| `BuyerSearchFilters`      | Form              | `components/buyer-registry/BuyerSearchFilters.tsx`      | Controls search text, status, and retained inactive inclusion |
| `RegisterBuyerDialog`     | Dialog/Form       | `components/buyer-registry/RegisterBuyerDialog.tsx`     | Creates an active buyer                                       |
| `BuyerSummaryPanel`       | Detail panel      | `components/buyer-registry/BuyerSummaryPanel.tsx`       | Shows identity, status, and eligibility                       |
| `EditBuyerIdentityDialog` | Dialog/Form       | `components/buyer-registry/EditBuyerIdentityDialog.tsx` | Updates name, WhatsApp mention, or CPF                        |
| `ShippingAddressPanel`    | Detail/Form panel | `components/buyer-registry/ShippingAddressPanel.tsx`    | Shows and sets shipping address                               |
| `RetentionPanel`          | Action panel      | `components/buyer-registry/RetentionPanel.tsx`          | Marks inactive and applies delete/anonymize                   |
| `BuyerStatusBadge`        | State indicator   | `components/buyer-registry/BuyerStatusBadge.tsx`        | Displays lifecycle status                                     |
| `EligibilityBadge`        | State indicator   | `components/buyer-registry/EligibilityBadge.tsx`        | Displays reservation/shipping readiness                       |

## Data Flow

### `/buyers`

| API Call       | Hook                 | Cache Key                          | Triggers                          |
| -------------- | -------------------- | ---------------------------------- | --------------------------------- |
| `GET /buyers`  | `useBuyers()`        | `queryKeys.buyers.list(filters)`   | Page mount, search/filter changes |
| `POST /buyers` | `useRegisterBuyer()` | invalidates `queryKeys.buyers.all` | Register buyer submit             |

### `/buyers/{buyerId}`

| API Call                                  | Hook                             | Cache Key                          | Triggers                     |
| ----------------------------------------- | -------------------------------- | ---------------------------------- | ---------------------------- |
| `GET /buyers/{buyerId}`                   | `useBuyer(buyerId)`              | `queryKeys.buyers.detail(buyerId)` | Page mount, mutation success |
| `PATCH /buyers/{buyerId}/identity`        | `useUpdateBuyerIdentity()`       | invalidates buyer detail and list  | Edit identity submit         |
| `PUT /buyers/{buyerId}/shipping-address`  | `useSetBuyerShippingAddress()`   | invalidates buyer detail and list  | Set address submit           |
| `POST /buyers/{buyerId}/inactive`         | `useMarkBuyerInactive()`         | invalidates buyer detail and list  | Mark inactive action         |
| `POST /buyers/{buyerId}/retention-action` | `useApplyBuyerRetentionAction()` | invalidates buyer detail and list  | Delete/anonymize submit      |

## Form Contracts

### RegisterBuyerForm

| Field             | Type   | HTML Input              | Validation                      | Error Message                             |
| ----------------- | ------ | ----------------------- | ------------------------------- | ----------------------------------------- |
| `name`            | string | `text`                  | Required                        | "Buyer name is required."                 |
| `whatsAppMention` | string | `text`                  | Required, mention-like text     | "WhatsApp mention is required."           |
| `cpf`             | string | `text`                  | Required, CPF format validation | "CPF is required."                        |
| `shippingAddress` | object | grouped optional fields | Optional until first shipment   | "Complete the address or leave it blank." |

Zod schema intent:

```typescript
z.object({
  name: z.string().min(1, "Buyer name is required."),
  whatsAppMention: z.string().min(1, "WhatsApp mention is required."),
  cpf: z.string().min(1, "CPF is required."),
  shippingAddress: shippingAddressSchema.optional(),
});
```

### EditBuyerIdentityForm

| Field             | Type   | HTML Input | Validation            | Error Message                   |
| ----------------- | ------ | ---------- | --------------------- | ------------------------------- |
| `name`            | string | `text`     | Required after update | "Buyer name is required."       |
| `whatsAppMention` | string | `text`     | Required after update | "WhatsApp mention is required." |
| `cpf`             | string | `text`     | Required after update | "CPF is required."              |

### ShippingAddressForm

| Field           | Type   | HTML Input | Validation | Error Message                 |
| --------------- | ------ | ---------- | ---------- | ----------------------------- |
| `recipientName` | string | `text`     | Required   | "Recipient name is required." |
| `streetLine1`   | string | `text`     | Required   | "Street address is required." |
| `city`          | string | `text`     | Required   | "City is required."           |
| `state`         | string | `text`     | Required   | "State is required."          |
| `postalCode`    | string | `text`     | Required   | "Postal code is required."    |
| `country`       | string | `text`     | Required   | "Country is required."        |

### RetentionActionForm

| Field             | Type   | HTML Input        | Validation                             | Error Message                 |
| ----------------- | ------ | ----------------- | -------------------------------------- | ----------------------------- |
| `reason`          | string | `textarea`        | Optional                               | n/a                           |
| `retentionAction` | enum   | segmented control | `delete` or `anonymize` after inactive | "Choose delete or anonymize." |

## Error Code To UI Message Mapping

| API Condition                     | HTTP Status | UI Message                                                                |
| --------------------------------- | ----------- | ------------------------------------------------------------------------- |
| Missing required identity         | 400         | "Name, WhatsApp mention, and CPF are required before reservation."        |
| Duplicate active CPF              | 400         | "Another active buyer already uses this CPF."                             |
| Duplicate active WhatsApp mention | 400         | "Another active buyer already uses this WhatsApp mention."                |
| Incomplete shipping address       | 400         | "Complete the shipping address before marking this buyer shipment ready." |
| Buyer not found                   | 404         | "Buyer not found."                                                        |
| Non-operator mutation             | 403         | "Only the group operator can change buyer records."                       |
| Retention action before inactive  | 400         | "Mark the buyer inactive before choosing delete or anonymize."            |

## State To UI Mapping

| Domain Value                  | UI Representation         | Color / Variant   |
| ----------------------------- | ------------------------- | ----------------- |
| `active`                      | Badge "Active"            | green / default   |
| `inactive`                    | Badge "Inactive"          | amber / warning   |
| `anonymized`                  | Badge "Anonymized"        | muted / secondary |
| `deleted`                     | Badge "Deleted"           | muted / outline   |
| `reservationEligible = true`  | Badge "Reservation ready" | green / default   |
| `reservationEligible = false` | Badge "Missing identity"  | amber / warning   |
| `shippingReady = true`        | Badge "Shipping ready"    | green / default   |
| `shippingReady = false`       | Badge "Needs address"     | amber / warning   |

## Story To UI Mapping

| Story                                                                  | UI Surface                            | Notes                                         |
| ---------------------------------------------------------------------- | ------------------------------------- | --------------------------------------------- |
| [BR-S1](STORIES.md#br-s1-register-buyer-for-reservation)               | RegisterBuyerDialog, BuyerTable       | Creates active buyer and shows eligibility    |
| [BR-S2](STORIES.md#br-s2-search-and-select-buyer)                      | BuyerSearchFilters, BuyerTable        | Search and status filters                     |
| [BR-S3](STORIES.md#br-s3-update-buyer-identity)                        | Buyer Detail, EditBuyerIdentityDialog | Correct identity while preserving eligibility |
| [BR-S4](STORIES.md#br-s4-add-shipping-address-before-first-shipment)   | ShippingAddressPanel                  | Address readiness for shipment                |
| [BR-S5](STORIES.md#br-s5-expose-reservation-eligibility-to-allocation) | BuyerTable, BuyerSummaryPanel         | Eligibility badge visible to operator         |
| [BR-S6](STORIES.md#br-s6-mark-buyer-inactive-and-resolve-retention)    | RetentionPanel                        | Inactive and terminal retention flow          |

## Accessibility Requirements

| Component                 | Requirement                                                    |
| ------------------------- | -------------------------------------------------------------- |
| `BuyerTable`              | Semantic `<table>` with column headers and visible row actions |
| `BuyerSearchFilters`      | Search input has associated label and clear button             |
| `RegisterBuyerDialog`     | `aria-modal="true"`, focus trap, Esc to close                  |
| `EditBuyerIdentityDialog` | Required fields announce validation errors                     |
| `ShippingAddressPanel`    | Missing address fields are listed as text, not color only      |
| `RetentionPanel`          | Destructive actions require confirmation and clear labels      |
| Status badges             | Include accessible labels describing state meaning             |

## UI Concept Registry

| Concept                   | ID                                          | Type            |
| ------------------------- | ------------------------------------------- | --------------- |
| `/buyers`                 | `ui.buyer-registry.buyers-page`             | Page            |
| `/buyers/{buyerId}`       | `ui.buyer-registry.buyer-detail-page`       | Page            |
| `BuyerTable`              | `ui.buyer-registry.BuyerTable`              | Component       |
| `BuyerSearchFilters`      | `ui.buyer-registry.BuyerSearchFilters`      | Form            |
| `RegisterBuyerDialog`     | `ui.buyer-registry.RegisterBuyerDialog`     | Form            |
| `EditBuyerIdentityDialog` | `ui.buyer-registry.EditBuyerIdentityDialog` | Form            |
| `ShippingAddressPanel`    | `ui.buyer-registry.ShippingAddressPanel`    | Component       |
| `RetentionPanel`          | `ui.buyer-registry.RetentionPanel`          | Component       |
| `BuyerStatusBadge`        | `ui.buyer-registry.BuyerStatusBadge`        | State Indicator |
| `EligibilityBadge`        | `ui.buyer-registry.EligibilityBadge`        | State Indicator |
| `useBuyers`               | `ui.buyer-registry.useBuyers`               | Hook / Binding  |
| `useBuyer`                | `ui.buyer-registry.useBuyer`                | Hook / Binding  |

## Checker Result

Status: PASS

Reason: UI-SPEC is constrained by `docs/UI-ARCHITECTURE.md`, maps every Buyer Registry operation/query/state needed by the stories, and preserves the operator-only v1 boundary.
