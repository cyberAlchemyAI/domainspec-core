---
feature: freight-and-shipment-batching
version: current
status: draft
updatedAt: 2026-05-21
docType: glossary
owners:
  - group operator
---

# Freight And Shipment Batching Glossary

| Term                     | Definition                                                                                          |
| ------------------------ | --------------------------------------------------------------------------------------------------- |
| Waiting Dose             | Paid allocated dose that has not yet been shipped and can be considered for a package.              |
| Shipment Batch           | Operator-managed shipping wave containing one or more buyer packages.                               |
| Buyer Package            | Shipment unit for one buyer within a shipment batch.                                                |
| Package Line Item        | Traceable package content entry pointing back to listing, allocation, and slot.                     |
| Shipping Readiness Check | Validation result confirming whether the buyer package can ship, especially whether address exists. |
| Shipment Batch Status    | Batch lifecycle status: draft, ready, shipped, or cancelled.                                        |
| Package Shipment Status  | Package lifecycle status: planned, blocked, ready, shipped, or cancelled.                           |
| Freight Deferred         | V1 policy that excludes freight amount calculation and freight payment tracking from this feature.  |
