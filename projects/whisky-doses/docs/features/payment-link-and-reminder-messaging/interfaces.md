---
feature: payment-link-and-reminder-messaging
version: current
status: draft
updatedAt: 2026-05-21
docType: interfaces
owners:
  - group operator
---

# Payment Link And Reminder Messaging Interfaces

## External MessagingAPI REST

Operator-facing REST surface.

| Endpoint                                                  | Method | Exposes                                                                  | Notes                                                   |
| --------------------------------------------------------- | ------ | ------------------------------------------------------------------------ | ------------------------------------------------------- |
| `/payment-runs/{paymentRunId}/payment-link-messages`      | POST   | [GeneratePaymentLinkMessages](operations.md#generatepaymentlinkmessages) | Generates copyable link messages for unpaid obligations |
| `/payment-link-artifacts/{paymentLinkArtifactId}/replace` | POST   | [ReplacePaymentLinkMessage](operations.md#replacepaymentlinkmessage)     | Cancels or replaces an active link artifact             |
| `/payment-reminders/render`                               | POST   | [RenderPaymentReminder](operations.md#renderpaymentreminder)             | Renders payment reminder text                           |
| `/listing-reminders/render`                               | POST   | [RenderListingReminder](operations.md#renderlistingreminder)             | Renders listing availability/fill reminder text         |
| `/reminders/suppress`                                     | POST   | [SuppressReminder](operations.md#suppressreminder)                       | Operator or system suppression                          |
| `/payment-link-messages`                                  | GET    | [GetPaymentLinkMessages](queries.md#getpaymentlinkmessages)              | Reads generated link messages                           |
| `/reminders`                                              | GET    | [GetReminderQueue](queries.md#getreminderqueue)                          | Reads reminder queue                                    |
| `/rendered-messages`                                      | GET    | [GetRenderedMessages](queries.md#getrenderedmessages)                    | Reads copy/paste audit                                  |

## Internal MessagingModule Interface

Cross-feature read/render contract.

| Method                            | Exposes                                                      | Consumer                                    |
| --------------------------------- | ------------------------------------------------------------ | ------------------------------------------- |
| `getPaymentLinkMessages(filters)` | [GetPaymentLinkMessages](queries.md#getpaymentlinkmessages)  | Operator UI, Public WhatsApp List Rendering |
| `getReminderQueue(filters)`       | [GetReminderQueue](queries.md#getreminderqueue)              | Operator UI                                 |
| `getRenderedMessages(filters)`    | [GetRenderedMessages](queries.md#getrenderedmessages)        | Operator UI, audit/export views             |
| `renderPaymentReminder(command)`  | [RenderPaymentReminder](operations.md#renderpaymentreminder) | Operator UI                                 |
| `renderListingReminder(command)`  | [RenderListingReminder](operations.md#renderlistingreminder) | Operator UI                                 |

## Dependency PaymentTrackingModule Interface

Required upstream interface from [Dose Payment Tracking](../dose-payment-tracking/interfaces.md#internal-paymenttrackingmodule-interface).

| Method                                      | Used By                                                                  | Why                                                         |
| ------------------------------------------- | ------------------------------------------------------------------------ | ----------------------------------------------------------- |
| `getPaymentRun(paymentRunId)`               | [GeneratePaymentLinkMessages](operations.md#generatepaymentlinkmessages) | Reads obligations, amount, deadline, status, and line items |
| `getBuyerPaymentStatus(buyerId, filters)`   | [RenderPaymentReminder](operations.md#renderpaymentreminder)             | Confirms unpaid/satisfied status before reminding           |
| payment correlation-key attachment endpoint | [GeneratePaymentLinkMessages](operations.md#generatepaymentlinkmessages) | Stores generated provider key under payment truth owner     |
| payment events subscription                 | [SuppressReminder](operations.md#suppressreminder)                       | Stops reminders after reconciliation                        |

## Dependency BuyerRegistryModule Interface

Required upstream interface from [Buyer Registry](../buyer-registry/interfaces.md#internal-buyerregistrymodule-interface).

| Method                                   | Used By                      | Why                                           |
| ---------------------------------------- | ---------------------------- | --------------------------------------------- |
| `getBuyer(buyerId)` or lookup equivalent | link and reminder rendering  | Reads buyer name and WhatsApp mention         |
| `searchBuyers(filters)`                  | operator recipient selection | Supports operator customization of recipients |

## Dependency BottleListingModule Interface

Required upstream interface from [Bottle Listing And Dose Allocation](../bottle-listing-and-dose-allocation/interfaces.md#internal-bottlelistingmodule-interface).

| Method                                   | Used By                                                      | Why                                                    |
| ---------------------------------------- | ------------------------------------------------------------ | ------------------------------------------------------ |
| `getListingAllocationSummary(listingId)` | [RenderListingReminder](operations.md#renderlistingreminder) | Reads availability, fill state, and buyer slot context |
| listing events subscription              | [RenderListingReminder](operations.md#renderlistingreminder) | Produces listing activity reminder opportunities       |

## External Provider Adapter Boundary

The payment provider or Pix adapter may generate URLs, QR payloads, or provider identifiers. This module may call that adapter to generate messageable link material, but reconciliation and payment status remain owned by Dose Payment Tracking.
