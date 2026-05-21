---
feature: bottle-listing-and-dose-allocation
version: current
status: draft
updatedAt: 2026-05-21
docType: events
owners:
  - group operator
---

# Bottle Listing And Dose Allocation Events

## BottleListingCreated

Produced by: [CreateBottleListing](operations.md#createbottlelisting)

Payload:
- `listingId`
- `totalDoseSlots`
- `createdAt`

Consumers:
- Public WhatsApp List Rendering may render draft previews later.

## BottleListingOpened

Produced by: [OpenBottleListing](operations.md#openbottlelisting)

Payload:
- `listingId`
- `openedAt`

Consumers:
- Public WhatsApp List Rendering can produce copy/paste listing text.
- Payment Link And Reminder Messaging can use listing availability reminders.

## DoseSlotsAllocated

Produced by: [AllocateDoseSlots](operations.md#allocatedoseslots)

Payload:
- `listingId`
- `buyerId`
- `allocationId`
- `slotNumbers`
- `allocatedAt`
- derived `filled`

Consumers:
- Public WhatsApp List Rendering refreshes slot display.
- Dose Payment Tracking reads allocations when a payment run is opened.

## DoseSlotsReleased

Produced by: [ReleaseDoseSlots](operations.md#releasedoseslots)

Payload:
- `listingId`
- `buyerId`
- `allocationId`
- `slotNumbers`
- `releasedAt`
- derived `filled`

Consumers:
- Public WhatsApp List Rendering refreshes slot display.
- Dose Payment Tracking must not include released slots in future payment runs.

## BottleListingClosed

Produced by: [CloseBottleListing](operations.md#closebottlelisting)

Payload:
- `listingId`
- `closedAt`
- optional `reason`
- derived `filled`

Consumers:
- Public WhatsApp List Rendering displays closed state.
- Dose Payment Tracking may evaluate whether payment can open according to listing payment mode.
