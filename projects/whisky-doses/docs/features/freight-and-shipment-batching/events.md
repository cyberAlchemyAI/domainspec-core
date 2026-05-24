---
feature: freight-and-shipment-batching
version: current
status: draft
updatedAt: 2026-05-21
docType: events
owners:
  - group operator
---

# Freight And Shipment Batching Events

## ShipmentBatchCreated

Produced by: [CreateShipmentBatch](operations.md#createshipmentbatch)

Payload:

- `shipmentBatchId`
- operator ID
- created timestamp

Consumers:

- Operator UI shows a draft shipping wave.

## BuyerPackageCreated

Produced by: [AddWaitingDosesToPackage](operations.md#addwaitingdosestopackage)

Payload:

- `buyerPackageId`
- `shipmentBatchId`
- buyer ID

Consumers:

- Operator UI shows per-buyer package grouping.
- Future freight calculation can quote by buyer package.

## WaitingDosePackaged

Produced by: [AddWaitingDosesToPackage](operations.md#addwaitingdosestopackage)

Payload:

- waiting dose ID
- buyer package ID
- buyer ID
- listing ID
- allocation ID
- slot number

Consumers:

- Waiting dose candidate views remove the packaged dose from available selections.

## PackageMarkedShipped

Produced by: [MarkPackageShipped](operations.md#markpackageshipped)

Payload:

- buyer package ID
- shipment batch ID
- buyer ID
- waiting dose IDs
- shipped timestamp
- optional tracking note

Consumers:

- Operator UI shows package shipped.
- Public WhatsApp List Rendering may show shipment transparency when needed.

## ShipmentBatchClosed

Produced by: [CloseShipmentBatch](operations.md#closeshipmentbatch)

Payload:

- shipment batch ID
- final status
- package counts
- closed timestamp

Consumers:

- Operator UI removes the batch from active shipment planning.
