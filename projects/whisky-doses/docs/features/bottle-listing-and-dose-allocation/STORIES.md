---
feature: bottle-listing-and-dose-allocation
version: current
status: draft
updatedAt: 2026-05-21
docType: stories
owners:
  - group operator
---

# Bottle Listing And Dose Allocation Stories

## Story Set

These stories mirror the Bottle Listing And Dose Allocation capabilities in [SPEC.md](SPEC.md#capabilities) and preserve coverage across public, admin/operations, cross-feature integration, and edge-case journeys.

## BL-S1 Create Draft Bottle Listing

Capability: [Listing Management](SPEC.md#capabilities)
Journey type: admin/operations
Concept links: [Bottle Listing](domain.md#bottle-listing), [CreateBottleListing](operations.md#createbottlelisting), [ListingLifecycle](states.md#listinglifecycle)

Classic story:
As a group operator, I want to create a draft bottle listing with numbered dose slots, so that I can prepare an offer before accepting reservations.

BDD scenario:
Given the operator has bottle details, dose size, price per dose, total slots, and payment mode
When the operator creates a listing
Then a draft listing exists
And numbered open dose slots are generated
And invalid dose count, dose size, price, or payment mode is rejected.

Acceptance checks:

- A valid listing starts in `draft`.
- `totalDoseSlots` and `doseSizeMl` must be positive.
- Payment opening mode must be `on_fill` or `manual`.
- [BottleListingCreated](events.md#bottlelistingcreated) is emitted.

## BL-S2 Open Listing For Reservations

Capability: [Listing Management](SPEC.md#capabilities)
Journey type: public
Concept links: [OpenBottleListing](operations.md#openbottlelisting), [Listing Status](domain.md#listing-status), [BottleListingOpened](events.md#bottlelistingopened)

Classic story:
As a group operator, I want to open a draft listing, so that buyers can request dose slots from the WhatsApp group offer.

BDD scenario:
Given a draft listing has complete required details
When the operator opens the listing
Then the listing status becomes `open`
And downstream rendering can produce group-facing listing text.

Acceptance checks:

- Only `draft` listings can be opened.
- Required listing details must be complete.
- Open listings appear in [ListOpenListings](queries.md#listopenlistings).
- [BottleListingOpened](events.md#bottlelistingopened) is emitted.

## BL-S3 Allocate Dose Slots To Eligible Buyer

Capability: [Dose Slot Allocation](SPEC.md#capabilities)
Journey type: admin/operations
Concept links: [AllocateDoseSlots](operations.md#allocatedoseslots), [Dose Allocation](domain.md#dose-allocation), [SlotAvailabilityRule](rules.md#r1-slot-availability-rule)

Classic story:
As a group operator, I want to allocate selected dose slots to an eligible buyer, so that reservations are accurate and traceable.

BDD scenario:
Given a listing is open
And selected slots are open
And Buyer Registry reports the buyer is reservation eligible
When the operator allocates the slots
Then an active allocation is created
And the selected slots become allocated
And the listing filled flag is recalculated.

Acceptance checks:

- Allocation is allowed only while listing status is `open`.
- Selected slots must belong to the listing and be open.
- Buyer must be reservation eligible through Buyer Registry.
- Per-person dose limit must not be exceeded when present.
- [DoseSlotsAllocated](events.md#doseslotsallocated) is emitted.

## BL-S4 Release Allocated Slots

Capability: [Dose Slot Allocation](SPEC.md#capabilities)
Journey type: edge-case
Concept links: [ReleaseDoseSlots](operations.md#releasedoseslots), [Dose Slot Status](domain.md#dose-slot-status), [DoseSlotsReleased](events.md#doseslotsreleased)

Classic story:
As a group operator, I want to release allocated slots while a listing is open, so that corrections or buyer withdrawals make slots available again.

BDD scenario:
Given a listing is open
And an active allocation owns selected slots
When the operator releases those slots
Then the slots become available for reallocation
And release history remains auditable.

Acceptance checks:

- Release is allowed only while the listing is open.
- Requested slots must belong to the allocation.
- Fully released allocations become released.
- Filled flag is recalculated after release.

## BL-S5 Close Listing And Stop Allocation Changes

Capability: [Listing Management](SPEC.md#capabilities)
Journey type: admin/operations
Concept links: [CloseBottleListing](operations.md#closebottlelisting), [BottleListingClosed](events.md#bottlelistingclosed), [ListingLifecycle](states.md#listinglifecycle)

Classic story:
As a group operator, I want to close a listing, so that normal allocation changes stop and downstream payment or rendering flows can react.

BDD scenario:
Given a listing is draft or open
When the operator closes the listing
Then listing status becomes `closed`
And normal allocations and releases are blocked
And downstream consumers can refresh their read models.

Acceptance checks:

- Draft or open listings can close.
- Already closed listings reject close attempts.
- Closed listings block normal allocation and release operations.
- [BottleListingClosed](events.md#bottlelistingclosed) is emitted.

## BL-S6 Expose Allocation Summary To Payment And Rendering

Capability: [Listing Read Models](SPEC.md#capabilities)
Journey type: cross-feature integration
Concept links: [GetListingAllocationSummary](queries.md#getlistingallocationsummary), [GetPaymentEligibleAllocations](queries.md#getpaymenteligibleallocations), [BottleListingModule](interfaces.md#internal-bottlelistingmodule-interface)

Classic story:
As a downstream payment or rendering feature, I want listing allocation summaries, so that I can display current slots or open payment for selected listing allocations.

BDD scenario:
Given a listing has dose slots and allocations
When a downstream consumer reads allocation summary or payment-eligible allocations
Then the response includes slot counts, buyer allocation rows, filled state, and listing line items
And no payment truth is changed by the read.

Acceptance checks:

- Allocation summary reports total, allocated, available, buyer rows, and filled.
- Payment-eligible allocation query returns buyer IDs, dose counts, price per dose, and totals per buyer/listing.
- Read models do not mutate listing or payment state.
- Buyer allocated dose query supports shipment batching later.

## Story Coverage Matrix

| Capability           | Stories                                                                                                                                               | Coverage                    |
| -------------------- | ----------------------------------------------------------------------------------------------------------------------------------------------------- | --------------------------- |
| Listing Management   | [BL-S1](#bl-s1-create-draft-bottle-listing), [BL-S2](#bl-s2-open-listing-for-reservations), [BL-S5](#bl-s5-close-listing-and-stop-allocation-changes) | public, admin/operations    |
| Dose Slot Allocation | [BL-S3](#bl-s3-allocate-dose-slots-to-eligible-buyer), [BL-S4](#bl-s4-release-allocated-slots)                                                        | admin/operations, edge-case |
| Allocation Integrity | [BL-S3](#bl-s3-allocate-dose-slots-to-eligible-buyer), [BL-S4](#bl-s4-release-allocated-slots)                                                        | edge-case                   |
| Listing Read Models  | [BL-S6](#bl-s6-expose-allocation-summary-to-payment-and-rendering)                                                                                    | cross-feature integration   |

## Concept Coverage Matrix

| Concept                                                             | Covered By                        | Notes                            |
| ------------------------------------------------------------------- | --------------------------------- | -------------------------------- |
| `bottle-listing-and-dose-allocation.BottleListing`                  | BL-S1, BL-S2, BL-S5               | Listing entity and lifecycle     |
| `bottle-listing-and-dose-allocation.DoseSlot`                       | BL-S1, BL-S3, BL-S4, BL-S6        | Numbered slot state              |
| `bottle-listing-and-dose-allocation.DoseAllocation`                 | BL-S3, BL-S4, BL-S6               | Buyer-slot assignment            |
| `bottle-listing-and-dose-allocation.ListingStatus`                  | BL-S1, BL-S2, BL-S5               | Draft/open/closed                |
| `bottle-listing-and-dose-allocation.DoseSlotStatus`                 | BL-S3, BL-S4                      | Open/allocated/released          |
| `bottle-listing-and-dose-allocation.ListingLifecycle`               | BL-S1, BL-S2, BL-S5               | Listing state machine            |
| `bottle-listing-and-dose-allocation.CreateBottleListing`            | BL-S1                             | Draft creation                   |
| `bottle-listing-and-dose-allocation.OpenBottleListing`              | BL-S2                             | Publication                      |
| `bottle-listing-and-dose-allocation.CloseBottleListing`             | BL-S5                             | Closure                          |
| `bottle-listing-and-dose-allocation.AllocateDoseSlots`              | BL-S3                             | Allocation mutation              |
| `bottle-listing-and-dose-allocation.ReleaseDoseSlots`               | BL-S4                             | Release mutation                 |
| `bottle-listing-and-dose-allocation.SlotAvailabilityRule`           | BL-S3, BL-S4                      | Oversell prevention              |
| `bottle-listing-and-dose-allocation.ListingOpenRule`                | BL-S3, BL-S4, BL-S5               | Allocation boundary              |
| `bottle-listing-and-dose-allocation.PerPersonDoseLimitRule`         | BL-S3                             | Buyer cap                        |
| `bottle-listing-and-dose-allocation.ActiveAllocationUniquenessRule` | BL-S3                             | Duplicate active slot prevention |
| `bottle-listing-and-dose-allocation.FilledListingDerivation`        | BL-S3, BL-S4, BL-S6               | Filled is derived                |
| `bottle-listing-and-dose-allocation.BottleListingAPI`               | BL-S1, BL-S2, BL-S3, BL-S4, BL-S5 | Operator API                     |
| `bottle-listing-and-dose-allocation.BottleListingModule`            | BL-S6                             | Cross-feature contract           |

## Drift Warnings

No story drift warnings identified.

## Unresolved Questions

No unresolved story questions.
