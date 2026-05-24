---
feature: freight-and-shipment-batching
version: current
status: draft
updatedAt: 2026-05-21
docType: states
owners:
  - group operator
---

# Freight And Shipment Batching States

## ShipmentBatchStatusLifecycle

```mermaid
stateDiagram-v2
    [*] --> draft
    draft --> ready: at least one ready package
    draft --> cancelled: cancel batch
    ready --> shipped: close after packages shipped/cancelled
    ready --> cancelled: cancel remaining work
    shipped --> [*]
    cancelled --> [*]
```

Allowed statuses:

- `draft`
- `ready`
- `shipped`
- `cancelled`

Invariants:

- a batch cannot become `shipped` while any package is `planned`, `blocked`, or `ready`
- a batch can span multiple listings
- cancelled batches do not mark waiting doses as shipped

## PackageShipmentStatusLifecycle

```mermaid
stateDiagram-v2
    [*] --> planned
    planned --> blocked: readiness validation fails
    planned --> ready: readiness validation passes
    blocked --> ready: blocker resolved
    ready --> shipped: operator marks shipped
    planned --> cancelled: cancel package
    blocked --> cancelled: cancel package
    ready --> cancelled: cancel package
    shipped --> [*]
    cancelled --> [*]
```

Allowed statuses:

- `planned`
- `blocked`
- `ready`
- `shipped`
- `cancelled`

Invariants:

- only `ready` packages can become `shipped`
- `blocked` packages must expose blocking reasons
- `shipped` package line items are no longer waiting dose candidates
