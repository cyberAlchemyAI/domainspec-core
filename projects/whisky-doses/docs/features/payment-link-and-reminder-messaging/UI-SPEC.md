---
id: payment-link-and-reminder-messaging-ui
feature: payment-link-and-reminder-messaging
title: "Payment Link And Reminder Messaging UI Specification"
summary: Operator UI for generating payment link messages, rendering reminders, replacing links, suppressing reminders, and reviewing copy/paste audit state.
status: draft
pillar: operations
domain: payment-link-and-reminder-messaging-ui
audience:
  - developers
priority: p0
lang: en
owners:
  - web-core
updatedAt: 2026-05-21
dependencies:
  - SPEC.md
  - interfaces.md
  - operations.md
  - queries.md
  - states.md
  - STORIES.md
includes: []
constitution: docs/UI-ARCHITECTURE.md
---

# UI Specification: Payment Link And Reminder Messaging

Governs the frontend presentation of payment link generation, reminder rendering, suppression, replacement, and rendered-message audit state.

Constrained by [UI-ARCHITECTURE.md](../../UI-ARCHITECTURE.md).

## Route Table

| Route                | Page Title                | Layout   | Auth Required | Permission     |
| -------------------- | ------------------------- | -------- | ------------- | -------------- |
| `/messages`          | Payment Links & Reminders | AppShell | Yes           | group operator |
| `/messages/rendered` | Rendered Messages         | AppShell | Yes           | group operator |

## Page Layouts

### `/messages` Payment Links & Reminders

```text
┌──────────────────────────────────────────────────────────────┐
│ Header: Payment Links & Reminders                            │
├──────────────────────────────────────────────────────────────┤
│ Tabs: Link Messages | Payment Reminders | Listing Reminders  │
├──────────────────────────────────────────────────────────────┤
│ Work queue: target, trigger, status, action                  │
├──────────────────────────────────────────────────────────────┤
│ MessagePreviewPanel with copy action                         │
└──────────────────────────────────────────────────────────────┘
```

Primary purpose:

- Generate payment link text for payment runs.
- Render payment and listing reminders.
- Replace links and suppress reminders.

### `/messages/rendered` Rendered Messages

```text
┌──────────────────────────────────────────────────────────────┐
│ Header: Rendered Messages                                    │
├──────────────────────────────────────────────────────────────┤
│ Filters: type, buyer, source, date range                     │
├──────────────────────────────────────────────────────────────┤
│ RenderedMessageTable                                         │
│ Type | Recipient | Source | Status | Rendered At | Copy       │
└──────────────────────────────────────────────────────────────┘
```

Primary purpose:

- Review copy/paste audit history.
- Copy previously rendered text without implying WhatsApp delivery.

## Component Inventory

| Component                     | Type              | Location                                                                         | Purpose                                             |
| ----------------------------- | ----------------- | -------------------------------------------------------------------------------- | --------------------------------------------------- |
| `PaymentLinkGenerationPanel`  | Form              | `components/payment-link-and-reminder-messaging/PaymentLinkGenerationPanel.tsx`  | Selects payment run, obligations, and customization |
| `ReminderQueueTable`          | Table             | `components/payment-link-and-reminder-messaging/ReminderQueueTable.tsx`          | Lists pending/rendered/suppressed/failed reminders  |
| `PaymentReminderRenderDialog` | Dialog/Form       | `components/payment-link-and-reminder-messaging/PaymentReminderRenderDialog.tsx` | Renders payment reminder text                       |
| `ListingReminderRenderDialog` | Dialog/Form       | `components/payment-link-and-reminder-messaging/ListingReminderRenderDialog.tsx` | Renders listing reminder text                       |
| `MessagePreviewPanel`         | Preview/copy tool | `components/payment-link-and-reminder-messaging/MessagePreviewPanel.tsx`         | Shows rendered text and copy action                 |
| `RenderedMessageTable`        | Table             | `components/payment-link-and-reminder-messaging/RenderedMessageTable.tsx`        | Shows copy/paste audit records                      |
| `ReplacePaymentLinkDialog`    | Dialog/Form       | `components/payment-link-and-reminder-messaging/ReplacePaymentLinkDialog.tsx`    | Replaces or cancels active link artifacts           |
| `SuppressReminderDialog`      | Dialog/Form       | `components/payment-link-and-reminder-messaging/SuppressReminderDialog.tsx`      | Records reminder suppression reason                 |
| `PaymentLinkStatusBadge`      | State indicator   | `components/payment-link-and-reminder-messaging/PaymentLinkStatusBadge.tsx`      | Displays link artifact status                       |
| `ReminderStatusBadge`         | State indicator   | `components/payment-link-and-reminder-messaging/ReminderStatusBadge.tsx`         | Displays reminder delivery/render status            |

## Data Flow

### `/messages`

| API Call                                                       | Hook                               | Cache Key                                       | Triggers                                            |
| -------------------------------------------------------------- | ---------------------------------- | ----------------------------------------------- | --------------------------------------------------- |
| `GET /payment-link-messages`                                   | `usePaymentLinkMessages()`         | `queryKeys.messages.paymentLinks(filters)`      | Page mount, filter changes, generation success      |
| `GET /reminders`                                               | `useReminderQueue()`               | `queryKeys.messages.reminders(filters)`         | Page mount, filter changes, render/suppress success |
| `POST /payment-runs/{paymentRunId}/payment-link-messages`      | `useGeneratePaymentLinkMessages()` | invalidates link messages and rendered messages | Generate link messages submit                       |
| `POST /payment-link-artifacts/{paymentLinkArtifactId}/replace` | `useReplacePaymentLinkMessage()`   | invalidates link messages and rendered messages | Replace link submit                                 |
| `POST /payment-reminders/render`                               | `useRenderPaymentReminder()`       | invalidates reminders and rendered messages     | Render payment reminder submit                      |
| `POST /listing-reminders/render`                               | `useRenderListingReminder()`       | invalidates reminders and rendered messages     | Render listing reminder submit                      |
| `POST /reminders/suppress`                                     | `useSuppressReminder()`            | invalidates reminders                           | Suppress submit                                     |

### `/messages/rendered`

| API Call                 | Hook                    | Cache Key                              | Triggers                   |
| ------------------------ | ----------------------- | -------------------------------------- | -------------------------- |
| `GET /rendered-messages` | `useRenderedMessages()` | `queryKeys.messages.rendered(filters)` | Page mount, filter changes |

## Form Contracts

### GeneratePaymentLinkMessagesForm

| Field              | Type     | HTML Input    | Validation                               | Error Message               |
| ------------------ | -------- | ------------- | ---------------------------------------- | --------------------------- |
| `paymentRunId`     | string   | select/search | Required                                 | "Choose a payment run."     |
| `obligationIds`    | string[] | checkbox list | Optional, defaults to unpaid obligations | "Choose valid obligations." |
| `messageText`      | string   | textarea      | Optional customization                   | "Message text is invalid."  |
| `deadlineOverride` | date     | date input    | Optional                                 | "Deadline must be valid."   |

### RenderPaymentReminderForm

| Field            | Type   | HTML Input    | Validation                          | Error Message                         |
| ---------------- | ------ | ------------- | ----------------------------------- | ------------------------------------- |
| `paymentRunId`   | string | select/search | Required unless obligation selected | "Choose a payment run or obligation." |
| `obligationId`   | string | select/search | Optional                            | "Choose a valid obligation."          |
| `cadenceTrigger` | enum   | select        | Required                            | "Choose a reminder trigger."          |
| `messageText`    | string | textarea      | Optional customization              | "Reminder text is invalid."           |

### RenderListingReminderForm

| Field                    | Type   | HTML Input    | Validation             | Error Message                        |
| ------------------------ | ------ | ------------- | ---------------------- | ------------------------------------ |
| `listingId`              | string | select/search | Required               | "Choose a listing."                  |
| `listingReminderTrigger` | enum   | select        | Required               | "Choose a listing reminder trigger." |
| `messageText`            | string | textarea      | Optional customization | "Reminder text is invalid."          |

### ReplacePaymentLinkForm

| Field                   | Type    | HTML Input     | Validation | Error Message                               |
| ----------------------- | ------- | -------------- | ---------- | ------------------------------------------- |
| `paymentLinkArtifactId` | string  | hidden/context | Required   | "Payment link artifact is required."        |
| `reason`                | string  | textarea       | Required   | "Replacement reason is required."           |
| `generateReplacement`   | boolean | switch         | Required   | "Choose whether to generate a replacement." |

### SuppressReminderForm

| Field               | Type   | HTML Input     | Validation | Error Message                     |
| ------------------- | ------ | -------------- | ---------- | --------------------------------- |
| `targetReference`   | string | hidden/context | Required   | "Reminder target is required."    |
| `suppressionReason` | string | textarea       | Required   | "Suppression reason is required." |

## Error Code To UI Message Mapping

| API Condition                     | HTTP Status | UI Message                                                           |
| --------------------------------- | ----------- | -------------------------------------------------------------------- |
| Payment run not found             | 404         | "Payment run not found."                                             |
| No unpaid obligations selected    | 400         | "Choose at least one unpaid obligation."                             |
| Buyer missing WhatsApp mention    | 400         | "Buyer needs a WhatsApp mention before rendering this message."      |
| Obligation already paid           | 400         | "Paid obligations cannot receive normal payment link replacement."   |
| Reminder no longer eligible       | 400         | "This reminder is no longer eligible and was skipped or suppressed." |
| Direct WhatsApp posting requested | 400         | "V1 renders copy/paste text only; WhatsApp posting is deferred."     |
| Missing suppression reason        | 400         | "Add a reason before suppressing this reminder."                     |

## State To UI Mapping

| Domain Value          | UI Representation  | Color / Variant   |
| --------------------- | ------------------ | ----------------- |
| `draft` link          | Badge "Draft"      | muted / secondary |
| `active` link         | Badge "Active"     | green / default   |
| `replaced` link       | Badge "Replaced"   | amber / warning   |
| `cancelled` link      | Badge "Cancelled"  | muted / outline   |
| `expired` link        | Badge "Expired"    | red / destructive |
| `pending` reminder    | Badge "Pending"    | amber / warning   |
| `rendered` reminder   | Badge "Rendered"   | green / default   |
| `skipped` reminder    | Badge "Skipped"    | muted / secondary |
| `failed` reminder     | Badge "Failed"     | red / destructive |
| `suppressed` reminder | Badge "Suppressed" | muted / outline   |

## Story To UI Mapping

| Story                                                       | UI Surface                                       | Notes                                |
| ----------------------------------------------------------- | ------------------------------------------------ | ------------------------------------ |
| [PM-S1](STORIES.md#pm-s1-generate-payment-link-messages)    | PaymentLinkGenerationPanel, MessagePreviewPanel  | Generates copyable payment link text |
| [PM-S2](STORIES.md#pm-s2-review-and-copy-rendered-messages) | RenderedMessageTable, MessagePreviewPanel        | Copy/paste audit                     |
| [PM-S3](STORIES.md#pm-s3-render-payment-reminder)           | PaymentReminderRenderDialog, ReminderQueueTable  | Payment cadence reminders            |
| [PM-S4](STORIES.md#pm-s4-render-listing-reminder)           | ListingReminderRenderDialog                      | Listing activity reminders           |
| [PM-S5](STORIES.md#pm-s5-suppress-paid-or-noisy-reminders)  | SuppressReminderDialog, ReminderStatusBadge      | Suppression workflow                 |
| [PM-S6](STORIES.md#pm-s6-replace-payment-link-message)      | ReplacePaymentLinkDialog, PaymentLinkStatusBadge | Link replacement/cancel              |

## Accessibility Requirements

| Component                     | Requirement                                                         |
| ----------------------------- | ------------------------------------------------------------------- |
| `MessagePreviewPanel`         | Copy action has explicit label and rendered text remains selectable |
| `ReminderQueueTable`          | Semantic `<table>` with trigger/status columns                      |
| `PaymentReminderRenderDialog` | `aria-modal="true"`, focus trap, Esc to close                       |
| `ListingReminderRenderDialog` | Trigger selector has visible label and validation text              |
| `ReplacePaymentLinkDialog`    | Replacement/cancel action requires reason and confirmation context  |
| `SuppressReminderDialog`      | Suppression reason is required and announced on error               |
| Status badges                 | Include text labels; color is not the only state indicator          |

## UI Concept Registry

| Concept                       | ID                                                                   | Type            |
| ----------------------------- | -------------------------------------------------------------------- | --------------- |
| `/messages`                   | `ui.payment-link-and-reminder-messaging.messages-page`               | Page            |
| `/messages/rendered`          | `ui.payment-link-and-reminder-messaging.rendered-messages-page`      | Page            |
| `PaymentLinkGenerationPanel`  | `ui.payment-link-and-reminder-messaging.PaymentLinkGenerationPanel`  | Form            |
| `ReminderQueueTable`          | `ui.payment-link-and-reminder-messaging.ReminderQueueTable`          | Component       |
| `PaymentReminderRenderDialog` | `ui.payment-link-and-reminder-messaging.PaymentReminderRenderDialog` | Form            |
| `ListingReminderRenderDialog` | `ui.payment-link-and-reminder-messaging.ListingReminderRenderDialog` | Form            |
| `MessagePreviewPanel`         | `ui.payment-link-and-reminder-messaging.MessagePreviewPanel`         | Component       |
| `RenderedMessageTable`        | `ui.payment-link-and-reminder-messaging.RenderedMessageTable`        | Component       |
| `ReplacePaymentLinkDialog`    | `ui.payment-link-and-reminder-messaging.ReplacePaymentLinkDialog`    | Form            |
| `SuppressReminderDialog`      | `ui.payment-link-and-reminder-messaging.SuppressReminderDialog`      | Form            |
| `PaymentLinkStatusBadge`      | `ui.payment-link-and-reminder-messaging.PaymentLinkStatusBadge`      | State Indicator |
| `ReminderStatusBadge`         | `ui.payment-link-and-reminder-messaging.ReminderStatusBadge`         | State Indicator |
| `usePaymentLinkMessages`      | `ui.payment-link-and-reminder-messaging.usePaymentLinkMessages`      | Hook / Binding  |
| `useReminderQueue`            | `ui.payment-link-and-reminder-messaging.useReminderQueue`            | Hook / Binding  |
| `useRenderedMessages`         | `ui.payment-link-and-reminder-messaging.useRenderedMessages`         | Hook / Binding  |

## Checker Result

Status: PASS

Reason: UI-SPEC is constrained by `docs/UI-ARCHITECTURE.md`, maps payment link generation, reminder rendering, listing reminder rendering, suppression, replacement, and rendered-message audit while preserving copy/paste-only and no-payment-truth ownership boundaries.
