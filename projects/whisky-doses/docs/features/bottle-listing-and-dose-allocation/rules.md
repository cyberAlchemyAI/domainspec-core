---
feature: bottle-listing-and-dose-allocation
version: current
status: draft
updatedAt: 2026-05-21
docType: rules
owners:
  - group operator
---

# Bottle Listing And Dose Allocation Rules

## Rules

### R1 Slot Availability Rule

A dose allocation can only assign open slots that belong to the target listing.

Formal expression:

```text
requestedSlotIds.all(slot.listingId == listing.id && slot.status == "open")
&& requestedSlotIds.count == requestedQuantity
```

Enforces: [AllocateDoseSlots](operations.md#allocatedoseslots)

### R2 Listing Open Rule

Buyers can receive dose slots only while the listing is open.

Formal expression:

```text
listing.status == "open"
```

Enforces: [AllocateDoseSlots](operations.md#allocatedoseslots), [ReleaseDoseSlots](operations.md#releasedoseslots)

### R3 Per Person Dose Limit Rule

If a listing defines `perPersonDoseLimit`, the buyer's active allocation count after the operation must not exceed it.

Formal expression:

```text
listing.perPersonDoseLimit == null
|| buyerActiveSlotCountAfter <= listing.perPersonDoseLimit
```

Enforces: [AllocateDoseSlots](operations.md#allocatedoseslots)

### R4 Active Allocation Uniqueness Rule

A dose slot can belong to at most one active allocation.

Formal expression:

```text
activeAllocations.where(slotIds contains slot.id).count <= 1
```

Enforces: [AllocateDoseSlots](operations.md#allocatedoseslots)

### R5 Buyer Reservation Eligibility Rule

The buyer must be reservation eligible according to Buyer Registry before allocation.

Formal expression:

```text
BuyerRegistryModule.checkReservationEligibility(buyerId).eligible == true
```

Enforces: [AllocateDoseSlots](operations.md#allocatedoseslots)

## Calculations

### C1 Filled Listing Derivation

Filled state is derived from slot occupancy.

Formula:

```text
filled = allocatedSlotCount(listing.id) == listing.totalDoseSlots
```

Properties:

- Does not change `listing.status`.
- May become true while the listing remains `open`.
- May become false again if slots are released before closure.
