---
feature: payment-link-and-reminder-messaging
version: current
status: draft
updatedAt: 2026-05-21
docType: states
owners:
  - group operator
---

# Payment Link And Reminder Messaging States

## PaymentLinkStatusLifecycle

```mermaid
stateDiagram-v2
    [*] --> draft
    draft --> active: generated
    active --> replaced: replace requested
    active --> cancelled: cancel requested
    active --> expired: deadline/expiry passes
    replaced --> [*]
    cancelled --> [*]
    expired --> [*]
```

Allowed statuses:

- `draft`
- `active`
- `replaced`
- `cancelled`
- `expired`

Invariants:

- only one active artifact should exist for an obligation unless provider semantics require an explicit overlap window
- replaced, cancelled, and expired artifacts remain auditable
- paid obligations must not receive replacement links unless the operator explicitly records an exception workflow outside normal reminders

## ReminderDeliveryStatusLifecycle

```mermaid
stateDiagram-v2
    [*] --> pending
    pending --> rendered: render copy/paste text
    pending --> skipped: no longer eligible
    pending --> suppressed: operator or paid event suppresses
    pending --> failed: render failure
    failed --> pending: retry render
    rendered --> suppressed: later invalidated
    rendered --> [*]
    skipped --> [*]
    suppressed --> [*]
```

Allowed statuses:

- `pending`
- `rendered`
- `skipped`
- `failed`
- `suppressed`

Invariants:

- `rendered` means generated for copy/paste, not delivered through WhatsApp
- payment reminders cannot remain pending after the obligation becomes paid
- suppressed reminders require a reason
