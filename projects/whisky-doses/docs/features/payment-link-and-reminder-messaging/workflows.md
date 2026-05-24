---
feature: payment-link-and-reminder-messaging
version: current
status: draft
updatedAt: 2026-05-21
docType: workflows
owners:
  - group operator
---

# Payment Link And Reminder Messaging Workflows

## Payment Link Message Rendering

```mermaid
sequenceDiagram
    participant Operator
    participant Messaging
    participant Payment as Payment Tracking
    participant Buyer as Buyer Registry
    participant Provider as Provider Adapter

    Operator->>Messaging: generate link messages(paymentRunId)
    Messaging->>Payment: getPaymentRun(paymentRunId)
    Messaging->>Buyer: get buyer names and WhatsApp mentions
    Messaging->>Provider: create Pix/link payload per selected obligation
    Messaging->>Payment: attach provider correlation key
    Messaging->>Messaging: store active artifacts and rendered messages
    Messaging-->>Operator: copyable payment link text
```

Result:

- payment link artifacts are active
- rendered payment link text is available for copy/paste
- payment truth owns the attached provider correlation key

## Payment Reminder Rendering

```mermaid
sequenceDiagram
    participant Scheduler
    participant Messaging
    participant Payment as Payment Tracking
    participant Operator

    Scheduler->>Messaging: cadence trigger
    Messaging->>Payment: confirm current obligation status
    alt unpaid
        Messaging->>Messaging: render reminder text
        Messaging-->>Operator: copyable reminder
    else paid or suppressed
        Messaging->>Messaging: skip or suppress reminder
    end
```

Result:

- unpaid buyers receive rendered reminder text for operator use
- paid buyers are skipped or suppressed
- no direct WhatsApp delivery is inferred

## Listing Reminder Rendering

```mermaid
sequenceDiagram
    participant Listing as Bottle Listing
    participant Messaging
    participant Operator

    Listing-->>Messaging: listing opened or allocation changed
    Messaging->>Listing: get allocation summary
    Messaging->>Messaging: render listing reminder
    Messaging-->>Operator: copyable listing reminder text
```

Result:

- listing reminders reflect availability or fill state
- listing lifecycle remains owned by Bottle Listing And Dose Allocation

## Link Replacement

```mermaid
sequenceDiagram
    participant Operator
    participant Messaging
    participant Payment as Payment Tracking
    participant Provider as Provider Adapter

    Operator->>Messaging: replace link artifact
    Messaging->>Payment: confirm obligation is not paid
    Messaging->>Messaging: mark prior artifact replaced
    Messaging->>Provider: create replacement link payload
    Messaging->>Payment: attach replacement correlation key
    Messaging-->>Operator: replacement copyable text
```

Result:

- prior link remains auditable
- replacement link becomes active
- payment truth can reconcile against the active provider correlation key
