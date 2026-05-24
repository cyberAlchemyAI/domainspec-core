---
id: bottle-listing-and-dose-allocation-ui
feature: bottle-listing-and-dose-allocation
title: "Bottle Listing And Dose Allocation UI Specification"
summary: Operator UI for creating bottle listings, opening reservations, allocating numbered dose slots, releasing slots, and closing listings.
status: draft
pillar: operations
domain: bottle-listing-and-dose-allocation-ui
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

# UI Specification: Bottle Listing And Dose Allocation

Governs the frontend presentation of bottle listings, numbered dose slots, buyer allocations, derived fill state, and listing lifecycle actions.

Constrained by [UI-ARCHITECTURE.md](../../UI-ARCHITECTURE.md).

## Route Table

| Route                   | Page Title      | Layout   | Auth Required | Permission     |
| ----------------------- | --------------- | -------- | ------------- | -------------- |
| `/listings`             | Bottle Listings | AppShell | Yes           | group operator |
| `/listings/{listingId}` | Listing Detail  | AppShell | Yes           | group operator |

## Page Layouts

### `/listings` Bottle Listings

```text
┌──────────────────────────────────────────────────────────────┐
│ Header: Bottle Listings              [Create Listing]        │
├──────────────────────────────────────────────────────────────┤
│ Filters: bottle name, fill state, created date               │
├──────────────────────────────────────────────────────────────┤
│ ListingTable                                                  │
│ Bottle | Status | Slots | Filled | Payment Mode | Actions     │
└──────────────────────────────────────────────────────────────┘
```

Primary purpose:

- Review open and draft listing work.
- Create draft listings.
- Navigate to slot allocation detail.

### `/listings/{listingId}` Listing Detail

```text
┌──────────────────────────────────────────────────────────────┐
│ Header: Listing Detail            [Open] [Close]             │
├──────────────────────────────────────────────────────────────┤
│ ListingSummaryPanel: bottle, price, dose size, fill state    │
├──────────────────────────────────────────────────────────────┤
│ SlotGrid: numbered slots with buyer assignment               │
├──────────────────────────────────────────────────────────────┤
│ AllocationPanel: select buyer, slots/quantity, allocate      │
├──────────────────────────────────────────────────────────────┤
│ AllocationRows: active allocations and release actions       │
└──────────────────────────────────────────────────────────────┘
```

Primary purpose:

- Open draft listings.
- Allocate and release slots while open.
- Close listings and expose downstream-ready allocation summaries.

## Component Inventory

| Component             | Type            | Location                                                                | Purpose                                                        |
| --------------------- | --------------- | ----------------------------------------------------------------------- | -------------------------------------------------------------- |
| `ListingTable`        | Table           | `components/bottle-listing-and-dose-allocation/ListingTable.tsx`        | Lists listing summaries and current slot counts                |
| `ListingFilters`      | Form            | `components/bottle-listing-and-dose-allocation/ListingFilters.tsx`      | Filters by bottle name, fill state, and created date           |
| `CreateListingDialog` | Dialog/Form     | `components/bottle-listing-and-dose-allocation/CreateListingDialog.tsx` | Creates a draft listing and generated slots                    |
| `ListingSummaryPanel` | Detail panel    | `components/bottle-listing-and-dose-allocation/ListingSummaryPanel.tsx` | Shows lifecycle, bottle details, payment hints, and fill state |
| `SlotGrid`            | Grid            | `components/bottle-listing-and-dose-allocation/SlotGrid.tsx`            | Displays stable numbered dose slots and allocation status      |
| `AllocationPanel`     | Form            | `components/bottle-listing-and-dose-allocation/AllocationPanel.tsx`     | Selects buyer and slots or requested quantity for allocation   |
| `AllocationRows`      | Table           | `components/bottle-listing-and-dose-allocation/AllocationRows.tsx`      | Shows active allocations and release actions                   |
| `ListingStatusBadge`  | State indicator | `components/bottle-listing-and-dose-allocation/ListingStatusBadge.tsx`  | Displays draft/open/closed                                     |
| `SlotStatusBadge`     | State indicator | `components/bottle-listing-and-dose-allocation/SlotStatusBadge.tsx`     | Displays open/allocated/released history                       |
| `FilledIndicator`     | State indicator | `components/bottle-listing-and-dose-allocation/FilledIndicator.tsx`     | Displays derived filled state                                  |

## Data Flow

### `/listings`

| API Call             | Hook                       | Cache Key                            | Triggers                   |
| -------------------- | -------------------------- | ------------------------------------ | -------------------------- |
| `GET /listings/open` | `useOpenListings()`        | `queryKeys.listings.open(filters)`   | Page mount, filter changes |
| `POST /listings`     | `useCreateBottleListing()` | invalidates `queryKeys.listings.all` | Create listing submit      |

### `/listings/{listingId}`

| API Call                                   | Hook                          | Cache Key                                         | Triggers                     |
| ------------------------------------------ | ----------------------------- | ------------------------------------------------- | ---------------------------- |
| `GET /listings/{listingId}`                | `useBottleListing(listingId)` | `queryKeys.listings.detail(listingId)`            | Page mount, mutation success |
| `POST /listings/{listingId}/open`          | `useOpenBottleListing()`      | invalidates listing detail and open list          | Open action                  |
| `POST /listings/{listingId}/allocations`   | `useAllocateDoseSlots()`      | invalidates listing detail and allocation summary | Allocate submit              |
| `POST /allocations/{allocationId}/release` | `useReleaseDoseSlots()`       | invalidates listing detail and allocation summary | Release action               |
| `POST /listings/{listingId}/close`         | `useCloseBottleListing()`     | invalidates listing detail and open list          | Close action                 |

## Form Contracts

### CreateListingForm

| Field                | Type   | HTML Input        | Validation                      | Error Message                            |
| -------------------- | ------ | ----------------- | ------------------------------- | ---------------------------------------- |
| `bottleName`         | string | `text`            | Required                        | "Bottle name is required."               |
| `doseSizeMl`         | number | `number`          | Greater than 0                  | "Dose size must be greater than zero."   |
| `pricePerDose`       | number | `number`          | Non-negative BRL amount         | "Price per dose must be valid."          |
| `totalDoseSlots`     | number | `number`          | Greater than 0                  | "Total slots must be greater than zero." |
| `perPersonDoseLimit` | number | `number`          | Optional, positive when present | "Dose limit must be positive."           |
| `paymentOpeningMode` | enum   | segmented control | `on_fill` or `manual`           | "Choose a payment opening mode."         |
| `paymentDeadline`    | date   | date input        | Optional                        | "Payment deadline must be a valid date." |

Zod schema intent:

```typescript
z.object({
  bottleName: z.string().min(1, "Bottle name is required."),
  doseSizeMl: z.number().positive("Dose size must be greater than zero."),
  pricePerDose: z.number().nonnegative("Price per dose must be valid."),
  totalDoseSlots: z
    .number()
    .int()
    .positive("Total slots must be greater than zero."),
  perPersonDoseLimit: z.number().int().positive().optional(),
  paymentOpeningMode: z.enum(["on_fill", "manual"]),
  paymentDeadline: z.string().optional(),
});
```

### AllocateDoseSlotsForm

| Field               | Type     | HTML Input          | Validation                               | Error Message                       |
| ------------------- | -------- | ------------------- | ---------------------------------------- | ----------------------------------- |
| `buyerId`           | string   | searchable select   | Required, reservation eligible           | "Choose a reservation-ready buyer." |
| `slotIds`           | string[] | slot grid selection | Required when explicit slots selected    | "Choose at least one open slot."    |
| `requestedQuantity` | number   | number stepper      | Required when using next available slots | "Choose a valid dose quantity."     |

### ReleaseDoseSlotsForm

| Field          | Type     | HTML Input     | Validation                    | Error Message                        |
| -------------- | -------- | -------------- | ----------------------------- | ------------------------------------ |
| `allocationId` | string   | hidden/context | Required                      | "Allocation is required."            |
| `slotIds`      | string[] | checkbox list  | Required subset of allocation | "Choose slots from this allocation." |

## Error Code To UI Message Mapping

| API Condition                   | HTTP Status | UI Message                                                             |
| ------------------------------- | ----------- | ---------------------------------------------------------------------- |
| Invalid listing details         | 400         | "Complete the listing details before saving."                          |
| Non-draft listing opened        | 400         | "Only draft listings can be opened."                                   |
| Listing not open for allocation | 400         | "Open the listing before allocating slots."                            |
| Slot unavailable or duplicate   | 400         | "One or more selected slots are no longer available."                  |
| Buyer not reservation eligible  | 400         | "This buyer needs name, WhatsApp mention, and CPF before reservation." |
| Per-person dose limit exceeded  | 400         | "This allocation exceeds the per-person dose limit."                   |
| Listing already closed          | 400         | "This listing is already closed."                                      |
| Listing not found               | 404         | "Listing not found."                                                   |

## State To UI Mapping

| Domain Value       | UI Representation                    | Color / Variant   |
| ------------------ | ------------------------------------ | ----------------- |
| `draft`            | Badge "Draft"                        | muted / secondary |
| `open`             | Badge "Open"                         | green / default   |
| `closed`           | Badge "Closed"                       | muted / outline   |
| `open` slot        | Slot cell with empty state           | neutral / outline |
| `allocated` slot   | Slot cell with buyer mention         | green / default   |
| `released` history | Release marker in allocation history | amber / warning   |
| `filled = true`    | Badge "Filled"                       | green / default   |
| `filled = false`   | Badge "Available"                    | blue / info       |

## Story To UI Mapping

| Story                                                                        | UI Surface                                | Notes                                           |
| ---------------------------------------------------------------------------- | ----------------------------------------- | ----------------------------------------------- |
| [BL-S1](STORIES.md#bl-s1-create-draft-bottle-listing)                        | CreateListingDialog, ListingTable         | Creates draft listing and generated slots       |
| [BL-S2](STORIES.md#bl-s2-open-listing-for-reservations)                      | Listing Detail header, ListingStatusBadge | Opens draft listing                             |
| [BL-S3](STORIES.md#bl-s3-allocate-dose-slots-to-eligible-buyer)              | SlotGrid, AllocationPanel                 | Allocates explicit or next available slots      |
| [BL-S4](STORIES.md#bl-s4-release-allocated-slots)                            | AllocationRows, SlotGrid                  | Releases selected active allocation slots       |
| [BL-S5](STORIES.md#bl-s5-close-listing-and-stop-allocation-changes)          | Listing Detail header                     | Closes listing and disables normal allocation   |
| [BL-S6](STORIES.md#bl-s6-expose-allocation-summary-to-payment-and-rendering) | ListingSummaryPanel, AllocationRows       | Shows summary data used by downstream consumers |

## Accessibility Requirements

| Component             | Requirement                                                               |
| --------------------- | ------------------------------------------------------------------------- |
| `ListingTable`        | Semantic `<table>` with column headers and row actions                    |
| `CreateListingDialog` | `aria-modal="true"`, focus trap, Esc to close                             |
| `SlotGrid`            | Keyboard navigable grid with accessible slot labels and stable dimensions |
| `AllocationPanel`     | Buyer selector has visible label and validation message region            |
| `AllocationRows`      | Release actions clearly identify affected buyer and slot numbers          |
| Status badges         | Include text labels; color is not the only state indicator                |

## UI Concept Registry

| Concept                 | ID                                                          | Type            |
| ----------------------- | ----------------------------------------------------------- | --------------- |
| `/listings`             | `ui.bottle-listing-and-dose-allocation.listings-page`       | Page            |
| `/listings/{listingId}` | `ui.bottle-listing-and-dose-allocation.listing-detail-page` | Page            |
| `ListingTable`          | `ui.bottle-listing-and-dose-allocation.ListingTable`        | Component       |
| `ListingFilters`        | `ui.bottle-listing-and-dose-allocation.ListingFilters`      | Form            |
| `CreateListingDialog`   | `ui.bottle-listing-and-dose-allocation.CreateListingDialog` | Form            |
| `ListingSummaryPanel`   | `ui.bottle-listing-and-dose-allocation.ListingSummaryPanel` | Component       |
| `SlotGrid`              | `ui.bottle-listing-and-dose-allocation.SlotGrid`            | Component       |
| `AllocationPanel`       | `ui.bottle-listing-and-dose-allocation.AllocationPanel`     | Form            |
| `AllocationRows`        | `ui.bottle-listing-and-dose-allocation.AllocationRows`      | Component       |
| `ListingStatusBadge`    | `ui.bottle-listing-and-dose-allocation.ListingStatusBadge`  | State Indicator |
| `SlotStatusBadge`       | `ui.bottle-listing-and-dose-allocation.SlotStatusBadge`     | State Indicator |
| `FilledIndicator`       | `ui.bottle-listing-and-dose-allocation.FilledIndicator`     | State Indicator |
| `useOpenListings`       | `ui.bottle-listing-and-dose-allocation.useOpenListings`     | Hook / Binding  |
| `useBottleListing`      | `ui.bottle-listing-and-dose-allocation.useBottleListing`    | Hook / Binding  |

## Checker Result

Status: PASS

Reason: UI-SPEC is constrained by `docs/UI-ARCHITECTURE.md`, maps listing lifecycle, slot allocation, release, close, read model, and cross-feature buyer eligibility behavior, and preserves the no-payment-truth/no-WhatsApp-posting boundaries.
