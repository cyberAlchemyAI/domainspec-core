---
feature: bottle-listing-and-dose-allocation
version: current
status: draft
updatedAt: 2026-05-21
docType: glossary
owners:
  - group operator
---

# Bottle Listing And Dose Allocation Glossary

| Term | Definition | Source |
| --- | --- | --- |
| Bottle Listing | Operator-created offer for numbered dose slots from one whisky bottle. | [domain.md#bottle-listing](domain.md#bottle-listing) |
| Dose Slot | Numbered unit inside a listing that can be open, allocated, or released. | [domain.md#dose-slot](domain.md#dose-slot) |
| Dose Allocation | Assignment of one or more dose slots to one buyer in one listing. | [domain.md#dose-allocation](domain.md#dose-allocation) |
| Listing Status | Lifecycle value for a listing: `draft`, `open`, or `closed`. | [domain.md#listing-status](domain.md#listing-status) |
| Filled Listing | Derived condition where allocated slot count equals total dose slots. | [rules.md#c1-filled-listing-derivation](rules.md#c1-filled-listing-derivation) |
| Per-Person Dose Limit | Optional listing rule that caps active slots held by one buyer. | [rules.md#r3-per-person-dose-limit-rule](rules.md#r3-per-person-dose-limit-rule) |
| Reservation Eligibility | Buyer Registry result required before a buyer can receive slots. | [rules.md#r5-buyer-reservation-eligibility-rule](rules.md#r5-buyer-reservation-eligibility-rule) |
| Listing Read Model | Query output consumed by rendering, payment, and shipment features. | [queries.md](queries.md) |
