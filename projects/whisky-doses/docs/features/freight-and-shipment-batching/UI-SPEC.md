---
id: freight-and-shipment-batching-ui
feature: freight-and-shipment-batching
title: "Freight And Shipment Batching UI Specification"
summary: Operator UI for paid waiting doses, shipment batches, per-buyer packages, readiness blockers, and shipped state.
status: draft
pillar: operations
domain: freight-and-shipment-batching-ui
audience:
  - developers
priority: p1
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

# UI Specification: Freight And Shipment Batching

Governs the frontend presentation of paid waiting dose candidates, shipment batches, per-buyer packages, readiness validation, and shipped state.

Constrained by [UI-ARCHITECTURE.md](../../UI-ARCHITECTURE.md).

## Route Table

| Route                          | Page Title            | Layout   | Auth Required | Permission     |
| ------------------------------ | --------------------- | -------- | ------------- | -------------- |
| `/shipments`                   | Shipments             | AppShell | Yes           | group operator |
| `/shipments/{shipmentBatchId}` | Shipment Batch Detail | AppShell | Yes           | group operator |

## Page Layouts

### `/shipments` Shipments

```text
┌──────────────────────────────────────────────────────────────┐
│ Header: Shipments                     [Create Shipment Batch]│
├──────────────────────────────────────────────────────────────┤
│ WaitingDoseCandidateTable                                    │
├──────────────────────────────────────────────────────────────┤
│ ShipmentBatchTable                                           │
│ Batch | Status | Packages | Blocked | Shipped | Actions      │
└──────────────────────────────────────────────────────────────┘
```

Primary purpose:

- Review paid waiting doses.
- Create shipment batches.
- Navigate to active batch planning.

### `/shipments/{shipmentBatchId}` Shipment Batch Detail

```text
┌──────────────────────────────────────────────────────────────┐
│ Header: Shipment Batch Detail       [Close Batch]            │
├──────────────────────────────────────────────────────────────┤
│ ShipmentBatchSummary                                         │
├──────────────────────────────────────────────────────────────┤
│ AddToPackagePanel: buyer + waiting doses                     │
├──────────────────────────────────────────────────────────────┤
│ BuyerPackageTable                                            │
│ Buyer | Items | Status | Blockers | Validate | Shipped       │
└──────────────────────────────────────────────────────────────┘
```

Primary purpose:

- Group selected paid waiting doses into per-buyer packages.
- Validate readiness and show blockers.
- Mark ready packages shipped and close finished batches.

## Component Inventory

| Component                   | Type            | Location                                                                 | Purpose                                                  |
| --------------------------- | --------------- | ------------------------------------------------------------------------ | -------------------------------------------------------- |
| `WaitingDoseCandidateTable` | Table           | `components/freight-and-shipment-batching/WaitingDoseCandidateTable.tsx` | Lists eligible paid waiting doses and readiness blockers |
| `CreateShipmentBatchDialog` | Dialog/Form     | `components/freight-and-shipment-batching/CreateShipmentBatchDialog.tsx` | Creates draft shipment batch                             |
| `ShipmentBatchTable`        | Table           | `components/freight-and-shipment-batching/ShipmentBatchTable.tsx`        | Lists shipment batches                                   |
| `ShipmentBatchSummary`      | Detail panel    | `components/freight-and-shipment-batching/ShipmentBatchSummary.tsx`      | Shows batch status and package counts                    |
| `AddToPackagePanel`         | Form            | `components/freight-and-shipment-batching/AddToPackagePanel.tsx`         | Adds selected waiting doses to buyer package             |
| `BuyerPackageTable`         | Table           | `components/freight-and-shipment-batching/BuyerPackageTable.tsx`         | Shows package contents, blockers, and actions            |
| `ReadinessBlockerList`      | Status panel    | `components/freight-and-shipment-batching/ReadinessBlockerList.tsx`      | Explains why a package is blocked                        |
| `ShipmentStatusBadge`       | State indicator | `components/freight-and-shipment-batching/ShipmentStatusBadge.tsx`       | Displays batch status                                    |
| `PackageStatusBadge`        | State indicator | `components/freight-and-shipment-batching/PackageStatusBadge.tsx`        | Displays package status                                  |

## Data Flow

### `/shipments`

| API Call                 | Hook                         | Cache Key                                   | Triggers                                    |
| ------------------------ | ---------------------------- | ------------------------------------------- | ------------------------------------------- |
| `GET /waiting-doses`     | `useWaitingDoseCandidates()` | `queryKeys.shipments.waitingDoses(filters)` | Page mount, filter changes, package changes |
| `GET /shipment-batches`  | `useShipmentBatches()`       | `queryKeys.shipments.batches(filters)`      | Page mount, batch changes                   |
| `POST /shipment-batches` | `useCreateShipmentBatch()`   | invalidates shipment batches                | Create batch submit                         |

### `/shipments/{shipmentBatchId}`

| API Call                                                        | Hook                                | Cache Key                                       | Triggers                             |
| --------------------------------------------------------------- | ----------------------------------- | ----------------------------------------------- | ------------------------------------ |
| `GET /shipment-batches/{shipmentBatchId}`                       | `useShipmentBatch(shipmentBatchId)` | `queryKeys.shipments.detail(shipmentBatchId)`   | Page mount, package mutation success |
| `POST /shipment-batches/{shipmentBatchId}/packages`             | `useAddWaitingDosesToPackage()`     | invalidates batch detail and waiting candidates | Add to package submit                |
| `DELETE /buyer-packages/{buyerPackageId}/items/{waitingDoseId}` | `useRemoveWaitingDoseFromPackage()` | invalidates batch detail and waiting candidates | Remove item action                   |
| `POST /buyer-packages/{buyerPackageId}/validate`                | `useValidateShipmentReadiness()`    | invalidates batch detail                        | Validate action                      |
| `POST /buyer-packages/{buyerPackageId}/shipped`                 | `useMarkPackageShipped()`           | invalidates batch detail and waiting candidates | Mark shipped action                  |
| `POST /shipment-batches/{shipmentBatchId}/close`                | `useCloseShipmentBatch()`           | invalidates batch detail and batch list         | Close batch action                   |

## Form Contracts

### CreateShipmentBatchForm

| Field          | Type   | HTML Input | Validation | Error Message |
| -------------- | ------ | ---------- | ---------- | ------------- |
| `title`        | string | text       | Optional   | n/a           |
| `operatorNote` | string | textarea   | Optional   | n/a           |

### AddWaitingDosesToPackageForm

| Field             | Type     | HTML Input                    | Validation               | Error Message                              |
| ----------------- | -------- | ----------------------------- | ------------------------ | ------------------------------------------ |
| `shipmentBatchId` | string   | hidden/context                | Required                 | "Shipment batch is required."              |
| `buyerId`         | string   | searchable select             | Required                 | "Choose a buyer."                          |
| `waitingDoseIds`  | string[] | checkbox list/table selection | At least one, same buyer | "Choose paid waiting doses for one buyer." |

### MarkPackageShippedForm

| Field            | Type   | HTML Input     | Validation | Error Message                |
| ---------------- | ------ | -------------- | ---------- | ---------------------------- |
| `buyerPackageId` | string | hidden/context | Required   | "Buyer package is required." |
| `trackingNote`   | string | textarea       | Optional   | n/a                          |

## Error Code To UI Message Mapping

| API Condition                    | HTTP Status | UI Message                                                            |
| -------------------------------- | ----------- | --------------------------------------------------------------------- |
| Unpaid dose selected             | 400         | "Only paid doses can be packaged for shipment."                       |
| Dose already shipped or packaged | 400         | "This dose is already shipped or assigned to another active package." |
| Mixed buyers in one package      | 400         | "A package can contain doses for one buyer only."                     |
| Missing shipping address         | 400         | "Add the buyer's shipping address before marking this package ready." |
| Package not ready                | 400         | "Resolve package blockers before marking shipped."                    |
| Open packages remain             | 400         | "Close the batch only after packages are shipped or cancelled."       |
| Freight requested                | 400         | "Freight calculation and payment are outside v1."                     |

## State To UI Mapping

| Domain Value        | UI Representation | Color / Variant   |
| ------------------- | ----------------- | ----------------- |
| `draft` batch       | Badge "Draft"     | muted / secondary |
| `ready` batch       | Badge "Ready"     | blue / info       |
| `shipped` batch     | Badge "Shipped"   | green / default   |
| `cancelled` batch   | Badge "Cancelled" | muted / outline   |
| `planned` package   | Badge "Planned"   | muted / secondary |
| `blocked` package   | Badge "Blocked"   | red / destructive |
| `ready` package     | Badge "Ready"     | blue / info       |
| `shipped` package   | Badge "Shipped"   | green / default   |
| `cancelled` package | Badge "Cancelled" | muted / outline   |

## Story To UI Mapping

| Story                                                              | UI Surface                                    | Notes                                        |
| ------------------------------------------------------------------ | --------------------------------------------- | -------------------------------------------- |
| [FS-S1](STORIES.md#fs-s1-identify-paid-waiting-doses)              | WaitingDoseCandidateTable                     | Shows paid waiting candidates and blockers   |
| [FS-S2](STORIES.md#fs-s2-create-shipment-batch)                    | CreateShipmentBatchDialog, ShipmentBatchTable | Creates draft shipping wave                  |
| [FS-S3](STORIES.md#fs-s3-package-waiting-doses-by-buyer)           | AddToPackagePanel, BuyerPackageTable          | Groups selected doses into per-buyer package |
| [FS-S4](STORIES.md#fs-s4-validate-shipment-readiness)              | ReadinessBlockerList, PackageStatusBadge      | Shows address/eligibility blockers           |
| [FS-S5](STORIES.md#fs-s5-mark-package-shipped-and-close-batch)     | BuyerPackageTable, ShipmentBatchSummary       | Shipped progress and batch closure           |
| [FS-S6](STORIES.md#fs-s6-remove-dose-from-package-before-shipment) | BuyerPackageTable                             | Removes unshipped package item               |

## Accessibility Requirements

| Component                   | Requirement                                                            |
| --------------------------- | ---------------------------------------------------------------------- |
| `WaitingDoseCandidateTable` | Semantic `<table>` with buyer, listing, payment, and readiness columns |
| `CreateShipmentBatchDialog` | `aria-modal="true"`, focus trap, Esc to close                          |
| `AddToPackagePanel`         | Buyer and dose selection have visible labels and validation messages   |
| `BuyerPackageTable`         | Package actions identify buyer and item count in accessible labels     |
| `ReadinessBlockerList`      | Blockers are listed as text, not color only                            |
| Status badges               | Include text labels; color is not the only state indicator             |

## UI Concept Registry

| Concept                        | ID                                                            | Type            |
| ------------------------------ | ------------------------------------------------------------- | --------------- |
| `/shipments`                   | `ui.freight-and-shipment-batching.shipments-page`             | Page            |
| `/shipments/{shipmentBatchId}` | `ui.freight-and-shipment-batching.shipment-batch-detail-page` | Page            |
| `WaitingDoseCandidateTable`    | `ui.freight-and-shipment-batching.WaitingDoseCandidateTable`  | Component       |
| `CreateShipmentBatchDialog`    | `ui.freight-and-shipment-batching.CreateShipmentBatchDialog`  | Form            |
| `ShipmentBatchTable`           | `ui.freight-and-shipment-batching.ShipmentBatchTable`         | Component       |
| `ShipmentBatchSummary`         | `ui.freight-and-shipment-batching.ShipmentBatchSummary`       | Component       |
| `AddToPackagePanel`            | `ui.freight-and-shipment-batching.AddToPackagePanel`          | Form            |
| `BuyerPackageTable`            | `ui.freight-and-shipment-batching.BuyerPackageTable`          | Component       |
| `ReadinessBlockerList`         | `ui.freight-and-shipment-batching.ReadinessBlockerList`       | Component       |
| `ShipmentStatusBadge`          | `ui.freight-and-shipment-batching.ShipmentStatusBadge`        | State Indicator |
| `PackageStatusBadge`           | `ui.freight-and-shipment-batching.PackageStatusBadge`         | State Indicator |
| `useWaitingDoseCandidates`     | `ui.freight-and-shipment-batching.useWaitingDoseCandidates`   | Hook / Binding  |
| `useShipmentBatch`             | `ui.freight-and-shipment-batching.useShipmentBatch`           | Hook / Binding  |
| `useShipmentBatches`           | `ui.freight-and-shipment-batching.useShipmentBatches`         | Hook / Binding  |

## Checker Result

Status: PASS

Reason: UI-SPEC is constrained by `docs/UI-ARCHITECTURE.md`, maps waiting dose selection, shipment batch composition, per-buyer package management, readiness blockers, shipped state, and batch closure while keeping freight calculation/payment outside v1.
