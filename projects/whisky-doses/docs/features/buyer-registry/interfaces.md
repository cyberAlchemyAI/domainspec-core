# Interfaces: Buyer Registry

This file defines the external operator API and internal module contract for Buyer Registry.

## External: BuyerRegistryAPI (REST)

### POST /buyers

**Exposes:** [RegisterBuyer](operations.md#registerbuyer)
**Auth:** Operator session.

**Request:**

| Field           | Type                                           | Maps To                                                      |
| --------------- | ---------------------------------------------- | ------------------------------------------------------------ |
| name            | string                                         | [RegisterBuyer](operations.md#registerbuyer).name            |
| whatsAppMention | [WhatsApp Mention](domain.md#whatsapp-mention) | [RegisterBuyer](operations.md#registerbuyer).whatsAppMention |
| cpf             | [CPF](domain.md#cpf)                           | [RegisterBuyer](operations.md#registerbuyer).cpf             |
| shippingAddress | [Shipping Address](domain.md#shipping-address) | [RegisterBuyer](operations.md#registerbuyer).shippingAddress |

**Responses:**

| Status | Condition                                                                                              | Body                                   |
| ------ | ------------------------------------------------------------------------------------------------------ | -------------------------------------- |
| 201    | [Buyer](domain.md#buyer) registered                                                                    | [GetBuyer](queries.md#getbuyer) output |
| 400    | [R1](rules.md#r1-reservation-identity-required) or [R3](rules.md#r3-active-buyer-uniqueness) violation | rule error                             |
| 403    | [R4](rules.md#r4-operator-management-only-in-v1) violation                                             | authorization error                    |

### PATCH /buyers/{buyerId}/identity

**Exposes:** [UpdateBuyerIdentity](operations.md#updatebuyeridentity)
**Auth:** Operator session.

**Request:**

| Field           | Type                                           | Maps To                                                                  |
| --------------- | ---------------------------------------------- | ------------------------------------------------------------------------ |
| buyerId         | [BuyerId](domain.md#buyerid)                   | [UpdateBuyerIdentity](operations.md#updatebuyeridentity).buyerId         |
| name            | string                                         | [UpdateBuyerIdentity](operations.md#updatebuyeridentity).name            |
| whatsAppMention | [WhatsApp Mention](domain.md#whatsapp-mention) | [UpdateBuyerIdentity](operations.md#updatebuyeridentity).whatsAppMention |
| cpf             | [CPF](domain.md#cpf)                           | [UpdateBuyerIdentity](operations.md#updatebuyeridentity).cpf             |

**Responses:**

| Status | Condition                                        | Body                                   |
| ------ | ------------------------------------------------ | -------------------------------------- |
| 200    | [Buyer](domain.md#buyer) updated                 | [GetBuyer](queries.md#getbuyer) output |
| 400    | Required identity removed or uniqueness violated | rule error                             |
| 404    | [Buyer](domain.md#buyer) not found               | not-found error                        |

### PUT /buyers/{buyerId}/shipping-address

**Exposes:** [SetBuyerShippingAddress](operations.md#setbuyershippingaddress)
**Auth:** Operator session.

**Request:**

| Field           | Type                                           | Maps To                                                                          |
| --------------- | ---------------------------------------------- | -------------------------------------------------------------------------------- |
| buyerId         | [BuyerId](domain.md#buyerid)                   | [SetBuyerShippingAddress](operations.md#setbuyershippingaddress).buyerId         |
| shippingAddress | [Shipping Address](domain.md#shipping-address) | [SetBuyerShippingAddress](operations.md#setbuyershippingaddress).shippingAddress |

**Responses:**

| Status | Condition                                                                   | Body                                                                         |
| ------ | --------------------------------------------------------------------------- | ---------------------------------------------------------------------------- |
| 200    | [Shipping Address](domain.md#shipping-address) set                          | [CheckBuyerShippingReadiness](queries.md#checkbuyershippingreadiness) output |
| 400    | [R2](rules.md#r2-shipping-address-required-before-first-shipment) violation | rule error                                                                   |
| 404    | [Buyer](domain.md#buyer) not found                                          | not-found error                                                              |

### POST /buyers/{buyerId}/inactive

**Exposes:** [MarkBuyerInactive](operations.md#markbuyerinactive)
**Auth:** Operator session.

**Request:**

| Field   | Type                         | Maps To                                                      |
| ------- | ---------------------------- | ------------------------------------------------------------ |
| buyerId | [BuyerId](domain.md#buyerid) | [MarkBuyerInactive](operations.md#markbuyerinactive).buyerId |
| reason  | string                       | [MarkBuyerInactive](operations.md#markbuyerinactive).reason  |

**Responses:**

| Status | Condition                                | Body                                   |
| ------ | ---------------------------------------- | -------------------------------------- |
| 200    | [Buyer](domain.md#buyer) marked inactive | [GetBuyer](queries.md#getbuyer) output |
| 400    | [Buyer](domain.md#buyer) is not active   | rule error                             |

### POST /buyers/{buyerId}/retention-action

**Exposes:** [DeleteOrAnonymizeBuyer](operations.md#deleteoranonymizebuyer)
**Auth:** Operator session.

**Request:**

| Field           | Type                                           | Maps To                                                                        |
| --------------- | ---------------------------------------------- | ------------------------------------------------------------------------------ |
| buyerId         | [BuyerId](domain.md#buyerid)                   | [DeleteOrAnonymizeBuyer](operations.md#deleteoranonymizebuyer).buyerId         |
| retentionAction | [Retention Action](domain.md#retention-action) | [DeleteOrAnonymizeBuyer](operations.md#deleteoranonymizebuyer).retentionAction |

**Responses:**

| Status | Condition                                          | Body                                      |
| ------ | -------------------------------------------------- | ----------------------------------------- |
| 200    | Retention action applied                           | [Buyer](domain.md#buyer) lifecycle result |
| 400    | [P1](rules.md#p1-buyer-retention-policy) violation | rule error                                |

### GET /buyers/{buyerId}

**Exposes:** [GetBuyer](queries.md#getbuyer)
**Auth:** Operator session.

### GET /buyers

**Exposes:** [SearchBuyers](queries.md#searchbuyers)
**Auth:** Operator session.

## Internal: BuyerRegistryModule Interface

**Consumers:** Bottle Listing And Dose Allocation, Freight And Shipment Batching, Payment Link And Reminder Messaging.

| Method                               | Maps To                                                                               | Description                                                             |
| ------------------------------------ | ------------------------------------------------------------------------------------- | ----------------------------------------------------------------------- |
| getBuyer(buyerId)                    | [GetBuyer](queries.md#getbuyer) query                                                 | Returns operator-readable buyer profile when allowed by lifecycle state |
| searchBuyers(searchText, status)     | [SearchBuyers](queries.md#searchbuyers) query                                         | Supports operator lookup for recipient or allocation selection          |
| checkReservationEligibility(buyerId) | [CheckBuyerReservationEligibility](queries.md#checkbuyerreservationeligibility) query | Tells allocation whether identity prerequisites are met                 |
| checkShippingReadiness(buyerId)      | [CheckBuyerShippingReadiness](queries.md#checkbuyershippingreadiness) query           | Tells shipment batching whether address prerequisites are met           |
