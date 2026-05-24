---
feature: payment-link-and-reminder-messaging
version: current
status: draft
updatedAt: 2026-05-21
docType: glossary
owners:
  - group operator
---

# Payment Link And Reminder Messaging Glossary

| Term                               | Definition                                                                                                        |
| ---------------------------------- | ----------------------------------------------------------------------------------------------------------------- |
| Payment Link Artifact              | Generated payment URL, Pix instruction, or provider payload tied to one buyer payment obligation.                 |
| Reminder Schedule                  | Stored plan deciding whether and when a payment or listing reminder should be rendered.                           |
| Reminder Message                   | Human-readable copy/paste text generated for a buyer or group context.                                            |
| Rendered Message                   | Audit record of copyable text produced by the system for operator use.                                            |
| Listing Reminder Trigger           | Listing-origin cause for reminder text, such as listing opened, nearly filled, filled, or closed.                 |
| Payment Link Status                | Lifecycle status for a payment link artifact: draft, active, replaced, cancelled, or expired.                     |
| Reminder Delivery Status           | Lifecycle status for reminder rendering: pending, rendered, skipped, failed, or suppressed.                       |
| Provider Correlation Key Candidate | `txid` or equivalent key generated with the link and attached to payment truth for reconciliation.                |
| Suppression                        | Operator or system decision to stop pending reminders because they are stale, paid, noisy, or manually cancelled. |
| Copy/Paste Rendering               | V1 delivery mode where the system generates WhatsApp-ready text without posting it directly.                      |
