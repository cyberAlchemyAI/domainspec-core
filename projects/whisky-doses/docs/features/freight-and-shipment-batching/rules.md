---
feature: freight-and-shipment-batching
version: current
status: draft
updatedAt: 2026-05-21
docType: rules
owners:
  - group operator
---

# Freight And Shipment Batching Rules

## P1 Batch Composition Policy

Shipment batching uses both selected levels:

- a shipment batch is an operator-managed shipping wave
- each shipping wave contains one or more per-buyer packages
- each buyer package can include that buyer's paid waiting doses across multiple listings

The operator selects which paid waiting doses are included in each wave.

## P2 Freight Deferred Policy

Freight calculation and freight payment are outside v1.

This feature may record shipment planning and shipped status, but it must not:

- calculate freight amounts
- require freight payment before package shipment
- reconcile freight payment evidence
- generate freight payment reminders

## R1 Shipment Eligibility Rule

A dose is eligible for packaging only when:

- it belongs to an active dose allocation
- its dose payment is satisfied according to Dose Payment Tracking
- it has not already been shipped
- it is not already included in another active package

## R2 Package Ownership Rule

A buyer package may contain waiting doses for exactly one buyer.

If a shipping wave includes multiple buyers, it must contain multiple buyer packages.

## R3 Shipping Address Required Rule

A buyer package cannot be marked `ready` or `shipped` unless Buyer Registry reports that the buyer has shipping readiness.

Shipping readiness requires a full shipping address before the buyer's first shipment.

## R4 No Listing Mutation Rule

Shipment batching may read listing allocation state but cannot mutate listing lifecycle, dose slots, or allocation ownership.

## R5 No Payment Truth Mutation Rule

Shipment batching may read dose payment status but cannot mark dose payment as paid, failed, partial, or otherwise reconciled.
