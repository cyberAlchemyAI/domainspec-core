---
feature: freight-and-shipment-batching
version: current
status: draft
updatedAt: 2026-05-21
docType: queries
owners:
  - group operator
---

# Freight And Shipment Batching Queries

## GetWaitingDoseCandidates

Reads paid allocated doses that are not shipped and not already packaged.

Filters:

- buyer ID
- listing ID
- oldest waiting age
- payment satisfied only

Output:

- waiting dose ID
- buyer ID
- listing ID
- allocation ID
- slot number
- payment status
- waiting since timestamp
- shipping readiness summary

## GetShipmentBatch

Reads one shipment batch with buyer packages.

Input:

- `shipmentBatchId`

Output:

- batch details
- batch status
- buyer packages
- package line items
- readiness blockers
- shipped/cancelled timestamps

## ListShipmentBatches

Reads shipment batches for operator review.

Filters:

- status
- created date range
- buyer ID
- listing ID

Output:

- batch ID
- title
- status
- package count
- blocked package count
- shipped package count

## GetBuyerPackage

Reads one buyer package with line items and readiness.

Input:

- `buyerPackageId`

Output:

- buyer package ID
- shipment batch ID
- buyer ID
- package status
- package line items
- shipping readiness check
- tracking note
