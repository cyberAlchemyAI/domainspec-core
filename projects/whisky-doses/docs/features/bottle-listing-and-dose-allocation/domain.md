---
feature: bottle-listing-and-dose-allocation
version: current
status: draft
updatedAt: 2026-05-21
docType: domain
owners:
  - group operator
---

# Bottle Listing And Dose Allocation Domain

## Entities

### Bottle Listing

An operator-created offer for dose slots from one whisky bottle.

| Field                | Type                              | Required | Description                                       |
| -------------------- | --------------------------------- | -------- | ------------------------------------------------- |
| `id`                 | Listing ID                        | yes      | Stable identifier                                 |
| `bottleName`         | string                            | yes      | Human-readable bottle name                        |
| `alcoholPercentage`  | decimal                           | no       | ABV shown when available                          |
| `doseSizeMl`         | positive integer                  | yes      | Milliliters per dose                              |
| `pricePerDose`       | [Money Amount](#money-amount)     | yes      | Price for one dose slot                           |
| `totalDoseSlots`     | positive integer                  | yes      | Count of numbered slots generated for the listing |
| `perPersonDoseLimit` | [Dose Quantity](#dose-quantity)   | no       | Optional buyer-level cap                          |
| `paymentOpeningMode` | enum                              | yes      | `on_fill` or `manual`                             |
| `paymentDeadline`    | date                              | no       | Deadline shown when payment opens                 |
| `status`             | [Listing Status](#listing-status) | yes      | `draft`, `open`, or `closed`                      |
| `createdAt`          | timestamp                         | yes      | Creation time                                     |

### Dose Slot

A numbered allocation unit inside one bottle listing.

| Field          | Type                                  | Required | Description                        |
| -------------- | ------------------------------------- | -------- | ---------------------------------- |
| `id`           | Dose Slot ID                          | yes      | Stable slot identifier             |
| `listingId`    | Listing ID                            | yes      | Parent listing                     |
| `slotNumber`   | positive integer                      | yes      | Number shown in public list        |
| `status`       | [Dose Slot Status](#dose-slot-status) | yes      | `open`, `allocated`, or `released` |
| `allocationId` | Allocation ID                         | no       | Active allocation when allocated   |

Constraint: `(listingId, slotNumber)` is unique.

### Dose Allocation

An assignment of one or more dose slots to one buyer.

| Field         | Type                            | Required | Description                      |
| ------------- | ------------------------------- | -------- | -------------------------------- |
| `id`          | Allocation ID                   | yes      | Stable allocation identifier     |
| `listingId`   | Listing ID                      | yes      | Listing where slots are assigned |
| `buyerId`     | Buyer ID                        | yes      | Buyer from Buyer Registry        |
| `slotIds`     | Dose Slot ID[]                  | yes      | Assigned dose slots              |
| `quantity`    | [Dose Quantity](#dose-quantity) | yes      | Count of assigned slots          |
| `status`      | enum                            | yes      | `active` or `released`           |
| `allocatedAt` | timestamp                       | yes      | Assignment time                  |

## Value Objects

### Dose Quantity

Positive integer dose count requested or assigned for one buyer in one listing.

Rules:

- Must be greater than zero.
- Must not exceed available open slots.
- Must not exceed `perPersonDoseLimit` when the listing defines one.

### Money Amount

BRL-denominated amount used for price per dose.

Rules:

- Must be greater than or equal to zero.
- Payment totals are derived by Dose Payment Tracking, not owned here.

## Enums

### Listing Status

| Value    | Description                                                     |
| -------- | --------------------------------------------------------------- |
| `draft`  | Listing is being prepared and cannot accept reservations        |
| `open`   | Listing can accept dose allocation while slots remain available |
| `closed` | Listing no longer accepts normal allocation changes             |

### Dose Slot Status

| Value       | Description                                                        |
| ----------- | ------------------------------------------------------------------ |
| `open`      | Slot can be allocated                                              |
| `allocated` | Slot is assigned to an active buyer allocation                     |
| `released`  | Slot was previously allocated and returned to availability history |

## Derived Values

### Filled Listing

A listing is filled when `allocatedSlotCount == totalDoseSlots`. Filled is not a lifecycle state and does not automatically close the listing.
