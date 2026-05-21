# Queries: Buyer Registry

This file defines read-only contracts owned by Buyer Registry.

## GetBuyer

**Type:** Query (read-only)
**Actor:** [Group operator](../../PROJECT-OVERVIEW.md#actors-and-stakeholders)

### Input

| Field   | Type                         | Required | Description                             |
| ------- | ---------------------------- | -------- | --------------------------------------- |
| buyerId | [BuyerId](domain.md#buyerid) | yes      | Identifies the [Buyer](domain.md#buyer) |

### Output

| Field               | Type                                           | Source                                                            | Description                                         |
| ------------------- | ---------------------------------------------- | ----------------------------------------------------------------- | --------------------------------------------------- |
| id                  | [BuyerId](domain.md#buyerid)                   | [Buyer](domain.md#buyer).id                                       | Buyer identity                                      |
| name                | string                                         | [Buyer](domain.md#buyer).name                                     | Buyer name                                          |
| whatsAppMention     | [WhatsApp Mention](domain.md#whatsapp-mention) | [Buyer](domain.md#buyer).whatsAppMention                          | Group mention                                       |
| cpf                 | [CPF](domain.md#cpf)                           | [Buyer](domain.md#buyer).cpf                                      | CPF when readable under retention state             |
| shippingAddress     | [Shipping Address](domain.md#shipping-address) | [Buyer](domain.md#buyer).shippingAddress                          | Address when present and readable                   |
| status              | [Buyer Status](domain.md#buyer-status)         | [Buyer](domain.md#buyer).status                                   | Lifecycle state                                     |
| reservationEligible | boolean                                        | [R1](rules.md#r1-reservation-identity-required)                   | Whether downstream allocation may accept this buyer |
| shippingReady       | boolean                                        | [R2](rules.md#r2-shipping-address-required-before-first-shipment) | Whether downstream shipment may include this buyer  |

### Reads From

| Entity                   | Relationship | Fields Used                                             |
| ------------------------ | ------------ | ------------------------------------------------------- |
| [Buyer](domain.md#buyer) | queries      | id, name, whatsAppMention, cpf, shippingAddress, status |

## SearchBuyers

**Type:** Query (read-only)
**Actor:** [Group operator](../../PROJECT-OVERVIEW.md#actors-and-stakeholders)

### Input

| Field      | Type   | Required | Description                                                                       |
| ---------- | ------ | -------- | --------------------------------------------------------------------------------- |
| searchText | string | no       | Matches [Buyer](domain.md#buyer).name or [Buyer](domain.md#buyer).whatsAppMention |

### Filters

| Field                   | Type                                   | Default | Description                                         |
| ----------------------- | -------------------------------------- | ------- | --------------------------------------------------- |
| status                  | [Buyer Status](domain.md#buyer-status) | active  | Restricts results by lifecycle state                |
| includeRetainedInactive | boolean                                | false   | Allows operator lookup of inactive retained records |

### Output

| Field  | Type  | Source                   | Description              |
| ------ | ----- | ------------------------ | ------------------------ |
| buyers | array | [Buyer](domain.md#buyer) | Matching buyer summaries |

### Reads From

| Entity                   | Relationship | Fields Used                       |
| ------------------------ | ------------ | --------------------------------- |
| [Buyer](domain.md#buyer) | queries      | id, name, whatsAppMention, status |

## CheckBuyerReservationEligibility

**Type:** Query (read-only)
**Actor:** Internal feature consumer or [group operator](../../PROJECT-OVERVIEW.md#actors-and-stakeholders)

### Input

| Field   | Type                         | Required | Description                             |
| ------- | ---------------------------- | -------- | --------------------------------------- |
| buyerId | [BuyerId](domain.md#buyerid) | yes      | Identifies the [Buyer](domain.md#buyer) |

### Output

| Field               | Type                         | Source                                          | Description                                        |
| ------------------- | ---------------------------- | ----------------------------------------------- | -------------------------------------------------- |
| buyerId             | [BuyerId](domain.md#buyerid) | [Buyer](domain.md#buyer).id                     | Buyer identity                                     |
| reservationEligible | boolean                      | [R1](rules.md#r1-reservation-identity-required) | True only when identity requirements are satisfied |
| missingFields       | string[]                     | [Buyer](domain.md#buyer) fields                 | Identity fields blocking reservation               |

### Reads From

| Entity                   | Relationship | Fields Used                            |
| ------------------------ | ------------ | -------------------------------------- |
| [Buyer](domain.md#buyer) | queries      | id, name, whatsAppMention, cpf, status |

## CheckBuyerShippingReadiness

**Type:** Query (read-only)
**Actor:** Internal feature consumer or [group operator](../../PROJECT-OVERVIEW.md#actors-and-stakeholders)

### Input

| Field   | Type                         | Required | Description                             |
| ------- | ---------------------------- | -------- | --------------------------------------- |
| buyerId | [BuyerId](domain.md#buyerid) | yes      | Identifies the [Buyer](domain.md#buyer) |

### Output

| Field         | Type                         | Source                                                            | Description                                       |
| ------------- | ---------------------------- | ----------------------------------------------------------------- | ------------------------------------------------- |
| buyerId       | [BuyerId](domain.md#buyerid) | [Buyer](domain.md#buyer).id                                       | Buyer identity                                    |
| shippingReady | boolean                      | [R2](rules.md#r2-shipping-address-required-before-first-shipment) | True only when address requirements are satisfied |
| missingFields | string[]                     | [Shipping Address](domain.md#shipping-address) fields             | Address fields blocking shipment                  |

### Reads From

| Entity                   | Relationship | Fields Used                                             |
| ------------------------ | ------------ | ------------------------------------------------------- |
| [Buyer](domain.md#buyer) | queries      | id, name, whatsAppMention, cpf, shippingAddress, status |
