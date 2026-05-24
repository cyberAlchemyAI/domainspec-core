---
feature: freight-and-shipment-batching
version: current
status: draft
updatedAt: 2026-05-21
docType: workflows
owners:
  - group operator
---

# Freight And Shipment Batching Workflows

## Waiting Dose Selection

```mermaid
sequenceDiagram
    participant Operator
    participant Shipment as Shipment Batching
    participant Listing as Bottle Listing
    participant Payment as Dose Payment Tracking
    participant Buyer as Buyer Registry

    Operator->>Shipment: list waiting dose candidates
    Shipment->>Listing: get allocated doses
    Shipment->>Payment: confirm paid/satisfied status
    Shipment->>Buyer: check shipping readiness
    Shipment-->>Operator: paid waiting doses with readiness blockers
```

Result:

- operator sees shippable and blocked waiting doses
- unpaid or already-shipped doses are excluded

## Shipment Batch Composition

```mermaid
sequenceDiagram
    participant Operator
    participant Shipment as Shipment Batching

    Operator->>Shipment: create shipment batch
    Operator->>Shipment: add selected waiting doses
    Shipment->>Shipment: group by buyer package
    Shipment->>Shipment: preserve listing/slot line items
    Shipment-->>Operator: draft shipping wave
```

Result:

- a shipping wave contains per-buyer packages
- packages can include doses from multiple listings

## Shipment Readiness Validation

```mermaid
sequenceDiagram
    participant Operator
    participant Shipment as Shipment Batching
    participant Buyer as Buyer Registry

    Operator->>Shipment: validate package readiness
    Shipment->>Buyer: check shipping readiness
    alt ready
        Shipment->>Shipment: package ready
    else blocked
        Shipment->>Shipment: package blocked with reasons
    end
```

Result:

- packages without buyer address are blocked
- freight calculation/payment is not evaluated in v1

## Package Shipment

```mermaid
sequenceDiagram
    participant Operator
    participant Shipment as Shipment Batching

    Operator->>Shipment: mark package shipped
    Shipment->>Shipment: mark package line items shipped
    Shipment-->>Operator: package shipped status
    Operator->>Shipment: close batch when all packages finished
```

Result:

- shipped packages leave the waiting dose pool
- batch closes when all packages are shipped or cancelled
