# Woovi And WhatsApp Integration Research

Date: 2026-05-20

## Purpose

Inventory the external reference material needed to design future payment and WhatsApp messaging features for Whisky Dose Group Operations.

This document is research, not a feature spec. It should be used later when specifying:

- dose payment charge creation
- payment confirmation reconciliation
- individual buyer payment messages
- group-facing listing/status messages
- WhatsApp provider selection
- webhook reliability and idempotency

## Source Inventory

| Source                                                                                                                    | What It Provides                                                                                                         | Relevance                                                            |
| ------------------------------------------------------------------------------------------------------------------------- | ------------------------------------------------------------------------------------------------------------------------ | -------------------------------------------------------------------- |
| [Woovi Pix + WhatsApp via BotConversa](https://developers.woovi.com/docs/integrations/integrating-pix-with-whatsapp)      | Woovi webhook to BotConversa flow, webhook validation call, charge-created payload usage, BotConversa contact/flow setup | Useful for low-code individual message automation after Woovi events |
| [Woovi WhatsApp category](https://developers.woovi.com/docs/category/whatsapp)                                            | Native WhatsApp activation, charge notification, receipt notification                                                    | Establishes Woovi's built-in WhatsApp path                           |
| [Woovi activate WhatsApp](https://developers.woovi.com/docs/whatsapp/whatsapp-how-to-activate)                            | Panel path: `Api/Plugins`, add WhatsApp integration, enable notifications                                                | Operational setup reference                                          |
| [Woovi send charges by WhatsApp](https://developers.woovi.com/docs/whatsapp/whatsapp-how-to-send-charges)                 | Native charge notification setup and charge creation option                                                              | Candidate for individual Pix charge delivery                         |
| [Woovi send receipts by WhatsApp](https://developers.woovi.com/docs/whatsapp/whatsapp-how-to-send-receipts)               | Native receipt notification setup                                                                                        | Candidate for automatic paid confirmation messages                   |
| [Woovi create charge flow](https://developers.woovi.com/docs/flows/flow-create-charge-api)                                | Charge API endpoint, headers, payload, customer fields, centavos rule                                                    | Primary charge creation reference                                    |
| [Woovi webhook category](https://developers.woovi.com/docs/category/webhook-2)                                            | Webhook docs index                                                                                                       | Entry point for event, retry, timeout, security docs                 |
| [Woovi webhook events](https://developers.woovi.com/docs/webhook/webhook-events-type)                                     | Charge, transaction, movement, dispute, account registration, Pix automatic events                                       | Defines which events can update payment/shipment states              |
| [Woovi webhook retry](https://developers.woovi.com/docs/webhook/webhook-retry)                                            | Retry conditions and exponential schedule                                                                                | Required for idempotent receiver design                              |
| [Woovi webhook test](https://developers.woovi.com/docs/webhook/webhook-test)                                              | Initial test payload and required empty `200` response                                                                   | Required for setup verification                                      |
| [Woovi webhook timeout](https://developers.woovi.com/docs/webhook/webhook-timeout)                                        | 100-second webhook timeout                                                                                               | Receiver must acknowledge quickly                                    |
| [Woovi webhook headers](https://developers.woovi.com/docs/webhook/webhook-headers)                                        | Custom HTTP headers on webhook requests                                                                                  | Useful for endpoint auth layering                                    |
| [Woovi webhook signature validation](https://developers.woovi.com/en/docs/webhook/seguranca/webhook-signature-validation) | Recommended `x-webhook-signature` RSA validation; HMAC comparison                                                        | Security reference for validating sender                             |
| [Woovi concepts: Charge](https://developers.woovi.com/docs/concepts/charge)                                               | Charge definition: payment request, one payment, due date, reconciliation                                                | Domain mapping to `DosePaymentCharge`                                |
| [Woovi concepts: Correlation ID](https://developers.woovi.com/docs/concepts/correlation-id)                               | UUID/GUID correlation tracking                                                                                           | Use whisky-domain IDs as stable correlation anchors                  |
| [Woovi concepts: Idempotence](https://developers.woovi.com/docs/concepts/idempotence)                                     | `correlationID`, webhook idempotency, duplicate event handling patterns                                                  | Required for payment safety                                          |
| [Woovi concepts: Transaction](https://developers.woovi.com/docs/concepts/transaction)                                     | Transaction means received payment                                                                                       | Domain mapping to confirmed Pix receipt                              |
| [woovibr/woovi-prompts](https://github.com/woovibr/woovi-prompts)                                                         | Prompt library for Woovi integration code generation                                                                     | Useful implementation aide, not authoritative API spec               |
| [woovi-prompts: whatsapp.md](https://github.com/woovibr/woovi-prompts/blob/main/prompts/whatsapp.md)                      | Two WhatsApp paths: native Woovi or API + provider; provider examples                                                    | Useful design comparison                                             |
| [woovi-prompts: charge-pix.md](https://github.com/woovibr/woovi-prompts/blob/main/prompts/charge-pix.md)                  | Charge endpoint summary, status values, expected response fields                                                         | Useful checklist for implementation                                  |
| [woovi-prompts: webhooks.md](https://github.com/woovibr/woovi-prompts/blob/main/prompts/webhooks.md)                      | Webhook receiver patterns, queueing, idempotency, event mapping                                                          | Useful implementation checklist; verify against official docs        |
| [360dialog messaging overview](https://docs.360dialog.com/docs/messaging/overview)                                        | WhatsApp Business Platform message model, 24-hour service window, opt-in, templates, webhooks                            | Individual messaging rules and compliance                            |
| [360dialog group messaging API](https://docs.360dialog.com/docs/messaging/groups/messaging-api)                           | Group send/receive via `recipient_type: "group"` and group IDs                                                           | Current official/BSP-style group API candidate                       |
| [Z-API group introduction](https://developer.z-api.io/en/group/introduction)                                              | WhatsApp group as chat ID, group management methods                                                                      | Unofficial/session-style group posting candidate                     |
| [Z-API send text](https://developer.z-api.io/en/message/send-text)                                                        | Text send endpoint to contact or group ID                                                                                | Practical group and individual send API                              |
| [Z-API search groups](https://developer.z-api.io/en/group/get-groups)                                                     | Get group list and group IDs from instance                                                                               | Required to target existing WhatsApp group with Z-API                |
| [Z-API mention everyone](https://developer.z-api.io/en/group/mention-all)                                                 | `mentionAll` with `@all` group mention behavior                                                                          | High-risk but relevant for announcement semantics                    |
| [Whapi group send reference](https://support.whapi.cloud/help-desk/groups/send-group-message)                             | Alternative group message provider model                                                                                 | Backup provider research                                             |

## Woovi Payment Model

### Charge Creation

The Woovi create-charge flow creates Pix charges via:

- `POST https://api.woovi.com/api/openpix/v1/charge` in the official flow page.
- Authorization header containing the Woovi App ID.
- JSON payload with `correlationID`, `value`, `comment`, and optional `customer`.
- `value` is in centavos.
- `customer` can include `name`, `email`, `phone`, and `taxID`.

The prompt repository also documents `POST https://api.woovi.com/api/v1/charge`. Treat this as an implementation prompt reference, but verify the final endpoint from the active Woovi API explorer before coding because Woovi docs show both `/api/openpix/v1` and `/api/v1` forms across materials.

### Domain Mapping For Whisky Doses

| Woovi Field      | Whisky Dose Meaning                                                                | Notes                                                                                                  |
| ---------------- | ---------------------------------------------------------------------------------- | ------------------------------------------------------------------------------------------------------ |
| `correlationID`  | Internal payment charge ID, likely derived from buyer + listing/payment obligation | Must be stable and unique. Do not generate a new one on retry for the same obligation.                 |
| `value`          | Amount owed in centavos                                                            | For dose payment: sum of buyer's reserved slots for one listing. For freight: separate freight charge. |
| `comment`        | Human-readable payment description                                                 | Example: `Dose LD Pulteney 25Y - slots 1, 2`. Keep under provider limits.                              |
| `customer.name`  | Buyer name                                                                         | Should come from buyer registry.                                                                       |
| `customer.phone` | Buyer WhatsApp phone                                                               | Required for native Woovi WhatsApp notifications.                                                      |
| `customer.taxID` | CPF/CNPJ                                                                           | Sensitive PII; store minimally and protect.                                                            |
| `brCode`         | Pix copia-e-cola                                                                   | Suitable for direct individual message, not group publication.                                         |
| `qrCodeImage`    | QR code image                                                                      | Individual message or checkout UI.                                                                     |
| `paymentLinkUrl` | Woovi hosted payment link                                                          | Best fallback for WhatsApp delivery.                                                                   |

### Payment Status

Woovi charge concept:

- A charge is a payment request.
- A charge accepts only one payment.
- A charge has an expiration/due date.
- A received payment can reconcile automatically against the charge.

Relevant statuses from Woovi prompt inventory:

- `ACTIVE`
- `COMPLETED`
- `EXPIRED`

Relevant events from official webhook docs:

- `OPENPIX:CHARGE_CREATED`
- `OPENPIX:CHARGE_COMPLETED`
- `OPENPIX:CHARGE_EXPIRED`
- `OPENPIX:CHARGE_COMPLETED_NOT_SAME_CUSTOMER_PAYER`
- `OPENPIX:TRANSACTION_RECEIVED`

For this project, `OPENPIX:CHARGE_COMPLETED` should be the primary event that marks a dose or freight payment as paid. `OPENPIX:CHARGE_COMPLETED_NOT_SAME_CUSTOMER_PAYER` should create a review state because the payer differs from the registered customer.

## Webhook Receiver Requirements

The receiver should be designed as an idempotent event ingress, not as a synchronous business workflow.

### Setup And Validation

- Woovi sends a test request when a webhook is created.
- The test endpoint should return HTTP `200` with an empty body.
- Woovi can configure custom HTTP headers for webhook requests.
- Woovi webhooks always call the configured endpoint with `POST`.
- Charge events can be linked to an API/application in Woovi.

### Timeout And Retry

- Woovi webhook timeout is documented as 100 seconds.
- Retry happens when the endpoint returns HTTP status above 400, is unavailable, or Woovi has an internal error.
- Woovi performs 8 attempts with exponential intervals: 10, 20, 40, 80, 160, 320, 640, 1280 seconds.
- After retry exhaustion, manual resend is available from the platform.

Design consequence:

- Validate signature.
- Persist raw event and dedupe key.
- Acknowledge quickly with `200`.
- Process domain transitions asynchronously.

### Signature And Authentication

Recommended validation:

- Use `x-webhook-signature`.
- Validate with Woovi public key.
- This validates that the request came from Woovi.

Deprecated/secondary validation:

- `X-OpenPix-Signature` HMAC-SHA1 validates using webhook-specific secret.
- Woovi docs label the older HMAC method as deprecated in the signature guidance.

Implementation note:

- Preserve the raw request body for signature verification. Do not verify against reserialized JSON.

### Idempotency Strategy

Woovi documentation explicitly recommends idempotency for webhook handlers because duplicate events can happen.

Candidate unique key:

- `event + charge.correlationID`
- fallback for Pix-only events: `event + pix.endToEndId`
- fallback for transfer/movement events: `event + transfer.correlationID`

Domain event mapping:

| Webhook Event                                      | Domain Effect                                                     |
| -------------------------------------------------- | ----------------------------------------------------------------- |
| `OPENPIX:CHARGE_CREATED`                           | External charge is available; store Woovi charge metadata         |
| `OPENPIX:CHARGE_COMPLETED`                         | Mark dose/freight payment as paid if amount and correlation match |
| `OPENPIX:CHARGE_EXPIRED`                           | Mark payment obligation as expired or needs regeneration          |
| `OPENPIX:CHARGE_COMPLETED_NOT_SAME_CUSTOMER_PAYER` | Mark paid but require payer review before shipment eligibility    |
| `OPENPIX:TRANSACTION_RECEIVED`                     | Reconciliation fallback or static QR/manual Pix tracking          |

## WhatsApp Messaging Findings

### Separate Two Message Channels

For this project, group messaging and individual messaging should be separate feature boundaries.

| Channel          | Purpose                                                                     | Recommended Direction                                       |
| ---------------- | --------------------------------------------------------------------------- | ----------------------------------------------------------- |
| Group            | Public listing, slot allocation, open/closed status, transparency snapshots | Start with copy/paste rendering; evaluate provider later    |
| Individual buyer | Pix charge, receipt, freight payment, shipment updates                      | Use native Woovi WhatsApp if enough; otherwise API provider |

### Individual Messages

Woovi built-in path:

- Activate WhatsApp in the Woovi panel under `Api/Plugins`.
- Enable charge and receipt notifications.
- When creating a charge, select/provide a customer and enable WhatsApp send behavior.
- Customer phone is essential.

API/provider path:

- Backend creates Woovi charge.
- Backend sends buyer a WhatsApp message through provider.
- Message can include `paymentLinkUrl`, `brCode`, and QR image.
- Payment confirmation must still come from Woovi webhook, not from buyer text/audio confirmation.

Official WhatsApp Business Platform constraints from 360dialog docs:

- Free-form messages are allowed only inside the 24-hour customer service window.
- Outside the window, use approved template messages.
- Users must opt in before business messages.
- Incoming messages and delivery statuses arrive via webhooks.

Design consequence:

- Store buyer opt-in state if using WhatsApp Business Platform.
- Store provider message ID for audit.
- Use templates for charge/payment reminders if the buyer has not recently messaged the business.

### Group Messages

There are three practical paths:

1. Copy/paste group renderer.
   - Lowest risk.
   - No API dependency.
   - Best first step for preserving current WhatsApp group workflow.

2. Official/BSP group API path.
   - 360dialog documents group send support using existing `POST https://waba-v2.360dialog.io/messages` with `recipient_type: "group"` and `to: "<GROUP_ID>"`.
   - Supports text, media, text templates, and media templates according to the 360dialog group messaging page.
   - Receive group messages through the same WABA webhook, with `group_id`.
   - Status webhooks are aggregated for group sends.
   - This appears to be a current BSP-supported path and should be evaluated directly with the selected BSP and Meta account eligibility.

3. Session-style WhatsApp Web providers.
   - Z-API treats groups as chats and can send text to a group ID through `send-text`.
   - Z-API can list groups, create/manage groups, mention members/groups, and mention everyone with `@all`.
   - Whapi offers similar group ID based sending.
   - These providers may be operationally convenient, but should be treated as higher platform-risk unless confirmed as compliant for the chosen account type and volume.

### Z-API Group Mechanics

Useful details from Z-API docs:

- Group ID is used in the same `phone` field used for contact sends.
- Modern group IDs can look like `120363019502650977-group`.
- `GET /instances/{instanceId}/token/{token}/groups` returns group list and group IDs.
- `POST /instances/{instanceId}/token/{token}/send-text` can send text to a contact or group.
- Required fields for text: `phone`, `message`.
- Optional fields include `delayMessage` and `delayTyping`.
- Mention everyone requires `mentionAll: true` and the message body must include `@all`.

Design consequence:

- If using Z-API, persist provider group ID separately from WhatsApp display name.
- Avoid `mentionAll` by default; require explicit operator action because it is intrusive.

## Candidate Architecture Decisions

### ADR Candidate: Payment Provider

Decision:

- Use Woovi as the Pix charge and webhook reconciliation provider.

Rationale:

- Native Pix charge creation, WhatsApp notifications, receipts, and webhook event model map cleanly to dose/freight obligations.

Open:

- Confirm final API endpoint variant before implementation.
- Decide whether dose payment and freight payment are separate Woovi charges.

### ADR Candidate: Payment Confirmation Authority

Decision:

- Woovi webhook is the authority for paid status.

Rationale:

- Avoid manual WhatsApp claims or screenshot/audio confirmations as source of truth.

Open:

- Define exception workflow for mismatched payer events.

### ADR Candidate: Group Transparency First Slice

Decision:

- Start with copy/paste WhatsApp list rendering, not automated group posting.

Rationale:

- The current operation already works through manual group posting.
- Group APIs have more provider/compliance uncertainty than individual buyer notifications.
- Renderer can be reused later by any group provider.

Open:

- Decide whether group posting automation is required for MVP or can wait until after allocation/payment accuracy.

### ADR Candidate: Individual Buyer Payment Messages

Decision:

- Prefer native Woovi WhatsApp notifications for initial buyer charge/receipt messages if it satisfies message format and phone-number requirements.

Fallback:

- Use provider middleware such as Meta Cloud API through BSP, Z-API, BotConversa, or another provider.

Open:

- Whether custom message content is needed beyond Woovi's native templates.
- Whether buyer opt-in is already established in the current group operation.

## Feature Implications

### Buyer Registry

Add fields needed by payment/messaging:

- legal name
- CPF/CNPJ
- WhatsApp phone
- WhatsApp display/mention label
- delivery address
- WhatsApp messaging opt-in state
- preferred notification mode

### Bottle Listing And Dose Allocation

No direct Woovi dependency unless payment opening creates charges per buyer/listing.

Keep provider-neutral data:

- listing ID
- buyer allocation
- amount owed per buyer
- payment opening rule
- payment deadline

### Dose Payment Tracking

Likely entities:

- `PaymentObligation`
- `WooviCharge`
- `PaymentEvent`
- `PaymentReview`

Rules:

- A payment obligation can create at most one active Woovi charge per buyer/listing unless regeneration is explicitly modeled.
- Completed webhook with matching correlation marks obligation paid.
- Mismatched payer event requires operator review before shipment eligibility.

### Public WhatsApp List Rendering

Renderer should output:

- listing title line
- payment date/deadline line
- open/closed status
- numbered slot list
- buyer display names/mentions
- optional payment-open text

Renderer should not include:

- individual BR codes
- buyer CPF/address
- private payment links unless intentionally posted to group

### Freight And Shipment Batching

Freight payment can reuse Woovi charge model:

- one freight charge per buyer shipment package, or
- one freight charge per shipment batch/buyer package.

Open decision:

- Whether freight payment is separate from dose payment in Woovi.

## Implementation Checklist For Later

Before coding Woovi integration:

- Confirm Woovi endpoint namespace from API explorer.
- Create env vars: `WOOVI_APP_ID`, webhook public key or validation config, optional webhook auth token.
- Define `correlationID` format and uniqueness constraint.
- Define webhook raw-body capture.
- Define `webhook_events` table with unique key.
- Define event-to-domain transition rules.
- Define mismatched payer handling.
- Define charge expiration/regeneration behavior.

Before coding WhatsApp integration:

- Choose first messaging path: copy/paste renderer, native Woovi, BSP API, or session provider.
- For individual messages, document opt-in and template requirements.
- For group messages, store provider group ID separately.
- Log outbound messages with provider, target, payload type, correlation ID, and provider message ID.
- Add throttling/manual confirmation for any group send.
- Keep group renderer provider-neutral.

## Recommended Next DomainSpec Work

1. Resolve payment feature decisions in `docs/PROJECT-DECISIONS.md`.
2. Create a feature spec for `dose-payment-tracking`.
3. Keep `public-whatsapp-list-rendering` separate and start with copy/paste output.
4. Add a later spike or experiment candidate for automated group posting provider choice.
