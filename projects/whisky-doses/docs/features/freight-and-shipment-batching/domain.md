---
feature: freight-and-shipment-batching
version: current
status: draft
updatedAt: 2026-05-21
docType: domain
owners:
  - group operator
---

# Freight And Shipment Batching Domain

## Waiting Dose

Entity / projection representing one buyer-owned allocated dose that is paid and not yet shipped.

Fields:

- `waitingDoseId`
- buyer ID
- listing ID
- allocation ID
- slot number
- dose quantity or dose unit reference
- dose payment status snapshot
- shipped marker

Constraints:

- must reference an active allocation
- must have satisfied dose payment before it can be packaged
- must not appear in more than one active buyer package

## Shipment Batch

Entity representing an operator-managed shipping wave.

Fields:

- `shipmentBatchId`
- title or operator note
- selected buyer package IDs
- [Shipment Batch Status](#shipment-batch-status)
- created/ready/shipped/cancelled timestamps

Constraints:

- contains one or more buyer packages before it can become ready
- can span multiple bottle listings
- does not imply a fixed shipping cycle

## Buyer Package

Entity representing the shipment unit for one buyer inside a shipment batch.

Fields:

- `buyerPackageId`
- `shipmentBatchId`
- buyer ID
- package line items
- shipping readiness result
- [Package Shipment Status](#package-shipment-status)
- optional tracking note

Constraints:

- belongs to exactly one buyer
- may include waiting doses across multiple listings
- cannot be marked shipped while blocked by shipping readiness

## Package Line Item

Value object preserving traceability from package content back to listing allocation.

Fields:

- listing ID
- allocation ID
- slot number
- dose quantity
- payment obligation references when available

## Shipping Readiness Check

Value object representing whether a buyer package can be shipped.

Fields:

- buyer ID
- has shipping address
- has eligible waiting doses
- blocking reasons
- checked timestamp

## Shipment Batch Status

Enum / type for shipping wave lifecycle:

- `draft`
- `ready`
- `shipped`
- `cancelled`

## Package Shipment Status

Enum / type for per-buyer package lifecycle:

- `planned`
- `blocked`
- `ready`
- `shipped`
- `cancelled`
