---
feature: bottle-listing-and-dose-allocation
version: current
status: draft
updatedAt: 2026-05-21
docType: queries
owners:
  - group operator
---

# Bottle Listing And Dose Allocation Queries

## GetBottleListing

Reads one listing with slots and active allocations.

Input: `listingId`

Output:

- listing details
- listing status
- dose slots with status and buyer assignment
- derived filled flag

## ListOpenListings

Lists listings with status `open`.

Filters:

- bottle name
- fill state
- created date

Output:

- listing summary
- available slot count
- allocated slot count
- derived filled flag

## GetListingAllocationSummary

Reads allocation totals for one listing.

Input: `listingId`

Output:

- `totalDoseSlots`
- `allocatedSlotCount`
- `availableSlotCount`
- `buyerAllocationRows`
- `filled`

## GetPaymentEligibleAllocations

Reads selected listing allocations for Dose Payment Tracking.

Input:

- listing IDs

Output:

- listing line items
- buyer IDs
- allocated dose counts
- price per dose
- total per buyer per listing

Boundary rule: this query does not open payment and does not own paid/unpaid truth.

## GetBuyerAllocatedDoses

Reads allocated dose records for one buyer across listings.

Input:

- `buyerId`
- optional listing status filter

Output:

- listing IDs
- slot numbers
- dose size
- price per dose
- allocation status
