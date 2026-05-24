---
feature: freight-and-shipment-batching
version: current
status: draft
updatedAt: 2026-05-21
docType: operations
owners:
  - group operator
---

# Freight And Shipment Batching Operations

## CreateShipmentBatch

Creates a draft shipping wave.

Input:

- optional title
- optional operator note
- operator ID

Postconditions:

- [Shipment Batch](domain.md#shipment-batch) exists in `draft`
- [ShipmentBatchCreated](events.md#shipmentbatchcreated) is emitted

## AddWaitingDosesToPackage

Adds selected waiting doses to a buyer package in a shipment batch.

Input:

- `shipmentBatchId`
- buyer ID
- waiting dose IDs
- operator ID

Preconditions:

- shipment batch is `draft`
- selected waiting doses belong to the same buyer
- selected waiting doses satisfy [ShipmentEligibilityRule](rules.md#r1-shipment-eligibility-rule)

Postconditions:

- buyer package exists or is updated
- package line items preserve listing/allocation/slot traceability
- [BuyerPackageCreated](events.md#buyerpackagecreated) is emitted when a new package is created
- [WaitingDosePackaged](events.md#waitingdosepackaged) is emitted for added waiting doses

## RemoveWaitingDoseFromPackage

Removes a waiting dose from a draft package.

Input:

- `buyerPackageId`
- waiting dose ID
- operator ID

Preconditions:

- buyer package is not shipped
- shipment batch is not shipped

Postconditions:

- waiting dose becomes available for future package selection again

## ValidateShipmentReadiness

Checks buyer package eligibility before marking it ready or shipped.

Input:

- `buyerPackageId`

Preconditions:

- buyer package exists

Postconditions:

- package becomes `ready` when it has eligible waiting doses and Buyer Registry reports shipping readiness
- package becomes `blocked` when address or dose eligibility is missing

## MarkPackageShipped

Marks one buyer package as shipped.

Input:

- `buyerPackageId`
- optional tracking note
- operator ID

Preconditions:

- package is `ready`
- buyer shipping readiness is still true
- package contains at least one waiting dose

Postconditions:

- package becomes `shipped`
- packaged waiting doses are marked shipped in this boundary
- [PackageMarkedShipped](events.md#packagemarkedshipped) is emitted

## CloseShipmentBatch

Closes a shipment batch after all packages are shipped or cancelled.

Input:

- `shipmentBatchId`
- operator ID

Preconditions:

- every package is `shipped` or `cancelled`

Postconditions:

- batch becomes `shipped` when at least one package shipped and none remain open
- [ShipmentBatchClosed](events.md#shipmentbatchclosed) is emitted
