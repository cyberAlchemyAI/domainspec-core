---
feature: bottle-listing-and-dose-allocation
version: current
status: draft
updatedAt: 2026-05-21
docType: states
owners:
  - group operator
---

# Bottle Listing And Dose Allocation States

## ListingLifecycle

State machine for [Bottle Listing](domain.md#bottle-listing).

| From | Event | To | Guard |
| --- | --- | --- | --- |
| none | [BottleListingCreated](events.md#bottlelistingcreated) | `draft` | listing details valid |
| `draft` | [BottleListingOpened](events.md#bottlelistingopened) | `open` | required fields complete |
| `draft` | [BottleListingClosed](events.md#bottlelistingclosed) | `closed` | operator closes draft |
| `open` | [BottleListingClosed](events.md#bottlelistingclosed) | `closed` | operator closes open listing |

Invariants:
- `filled` is not a lifecycle state.
- `closed` blocks normal allocation and release operations.
- Reopen is outside v1.

## DoseSlotStatus

State model for [Dose Slot](domain.md#dose-slot).

| From | Event | To | Guard |
| --- | --- | --- | --- |
| none | [BottleListingCreated](events.md#bottlelistingcreated) | `open` | slot generated for listing |
| `open` | [DoseSlotsAllocated](events.md#doseslotsallocated) | `allocated` | slot is selected and available |
| `allocated` | [DoseSlotsReleased](events.md#doseslotsreleased) | `released` | operator releases active allocation |
| `released` | [DoseSlotsReleased](events.md#doseslotsreleased) | `open` | release is represented as history and slot becomes available for reallocation |

Implementation note: the persisted model may represent release history separately and set the current slot status directly to `open`; the domain contract requires that release history remains auditable.
