---
feature: bottle-listing-and-dose-allocation
version: current
status: draft
updatedAt: 2026-05-21
docType: operations
owners:
  - group operator
---

# Bottle Listing And Dose Allocation Operations

## CreateBottleListing

Creates a draft listing and numbered dose slots.

| Field   | Value                                                                                                                              |
| ------- | ---------------------------------------------------------------------------------------------------------------------------------- |
| Actor   | group operator                                                                                                                     |
| Trigger | operator prepares a bottle offering                                                                                                |
| Input   | bottle details, dose size, price per dose, total slots, optional per-person limit, payment opening mode, optional payment deadline |
| Output  | draft [Bottle Listing](domain.md#bottle-listing) and generated [Dose Slot](domain.md#dose-slot) records                            |

Rules:

- `totalDoseSlots > 0`
- `doseSizeMl > 0`
- `paymentOpeningMode in ["on_fill", "manual"]`

Produces: [BottleListingCreated](events.md#bottlelistingcreated)

## OpenBottleListing

Moves a draft listing to open.

| Field   | Value                                         |
| ------- | --------------------------------------------- |
| Actor   | group operator                                |
| Trigger | operator is ready to accept dose reservations |
| Input   | `listingId`                                   |
| Output  | listing status becomes `open`                 |

Preconditions:

- Listing exists.
- Listing status is `draft`.
- Required listing details are complete.

Produces: [BottleListingOpened](events.md#bottlelistingopened)

## AllocateDoseSlots

Assigns selected open dose slots to one eligible buyer.

| Field   | Value                                                                |
| ------- | -------------------------------------------------------------------- |
| Actor   | group operator                                                       |
| Trigger | buyer requests one or more doses                                     |
| Input   | `listingId`, `buyerId`, selected `slotIds` or requested quantity     |
| Output  | active [Dose Allocation](domain.md#dose-allocation), allocated slots |

Rules:

- [R1 Slot Availability Rule](rules.md#r1-slot-availability-rule)
- [R2 Listing Open Rule](rules.md#r2-listing-open-rule)
- [R3 Per Person Dose Limit Rule](rules.md#r3-per-person-dose-limit-rule)
- [R4 Active Allocation Uniqueness Rule](rules.md#r4-active-allocation-uniqueness-rule)
- [R5 Buyer Reservation Eligibility Rule](rules.md#r5-buyer-reservation-eligibility-rule)

Postconditions:

- Allocated slots have status `allocated`.
- Allocation status is `active`.
- Listing fill is recalculated by [C1 Filled Listing Derivation](rules.md#c1-filled-listing-derivation).

Produces: [DoseSlotsAllocated](events.md#doseslotsallocated)

## ReleaseDoseSlots

Releases active allocated slots while the listing is open.

| Field   | Value                                                   |
| ------- | ------------------------------------------------------- |
| Actor   | group operator                                          |
| Trigger | operator corrects allocation or buyer gives up slots    |
| Input   | `allocationId`, slot IDs to release                     |
| Output  | released allocation quantity and open replacement slots |

Preconditions:

- Listing is `open`.
- Allocation is active.
- Requested slots belong to the allocation.

Postconditions:

- Released slots can be allocated again.
- Allocation status becomes `released` when all slots are released.

Produces: [DoseSlotsReleased](events.md#doseslotsreleased)

## CloseBottleListing

Closes a listing so normal allocation changes stop.

| Field   | Value                                                                    |
| ------- | ------------------------------------------------------------------------ |
| Actor   | group operator                                                           |
| Trigger | listing is intentionally stopped, filled, or no longer accepting changes |
| Input   | `listingId`, optional close reason                                       |
| Output  | listing status becomes `closed`                                          |

Preconditions:

- Listing status is `draft` or `open`.

Postconditions:

- No further normal allocations or releases are allowed.
- Payment opening may be triggered by Dose Payment Tracking if payment mode is `on_fill` and the listing is filled.

Produces: [BottleListingClosed](events.md#bottlelistingclosed)
