# Experiment Candidates

## Candidate Register

| ID   | Hypothesis | Intervention                                                               | Primary Signal                    | Cost   | Priority |
| ---- | ---------- | -------------------------------------------------------------------------- | --------------------------------- | ------ | -------- |
| EX-1 | H1         | Roll out structured vendor/submerchant onboarding with fixed step contract | submerchant_activation_time_hours | low    | now      |
| EX-2 | H2         | Launch hierarchy-aware central/vendor operations dashboard                 | active_submerchants_per_vendor    | medium | now      |
| EX-3 | H3         | Limit v1 collections to PIX payment links with tracked expiry presets      | payment_link_conversion_rate      | low    | now      |
| EX-4 | H4         | Apply fixed percentage split by level in payout calculations               | payout_dispute_rate               | low    | now      |
| EX-5 | H5         | Enable tenant cadence presets for settlement close                         | on_time_settlement_close_rate     | medium | later    |

## Candidate Details

### EX-1 - Structured Onboarding Pilot

- Linked hypothesis: H1
- Decision owner: product owner and vendor success lead
- Business question: Can we reduce activation friction for retailer-focused rollout?
- Intervention: enforce a standardized onboarding flow for vendor and submerchant activation.
- Target segment or scope: one retailer-heavy vendor cluster.
- Duration or observation window: 4 weeks.
- Primary signal: submerchant_activation_time_hours.
- Secondary signals: onboarding_dropoff_rate, activation_rework_count.
- Expected effect: lower activation time and fewer rework loops.
- Disconfirming outcome: no meaningful activation-time improvement.
- Risks: missing compliance rules or manual bottlenecks.
- Preconditions: explicit onboarding field contract and approval ownership.
- Minimum instrumentation needed: onboarding step timestamps, rejection reasons, final activation event.
- Recommended next step: run now.

### EX-2 - Operations Dashboard Pilot

- Linked hypothesis: H2
- Decision owner: central operations lead
- Business question: Does shared visibility between central and vendors improve operational execution?
- Intervention: enable dashboard views with hierarchy filters and client operational drill-down.
- Target segment or scope: central team plus selected vendor operators.
- Duration or observation window: 4 weeks.
- Primary signal: active_submerchants_per_vendor.
- Secondary signals: issue_triage_time_minutes, dashboard_weekly_active_users.
- Expected effect: improved operator response and healthier active network indicators.
- Disconfirming outcome: activity and issue-response metrics remain flat.
- Risks: data staleness and weak dashboard adoption.
- Preconditions: agreed KPI definitions and refresh cadence.
- Minimum instrumentation needed: dashboard usage logs, metric snapshots, issue lifecycle timestamps.
- Recommended next step: run now.

### EX-3 - PIX Link Flow Focus

- Linked hypothesis: H3
- Decision owner: product and engineering leads
- Business question: Is PIX-only payment-link collection the right v1 focus?
- Intervention: launch payment-link creation and collection flow with PIX as sole method.
- Target segment or scope: pilot vendor and its active submerchants.
- Duration or observation window: 30 days.
- Primary signal: payment_link_conversion_rate.
- Secondary signals: link_expiry_without_payment_rate, duplicate_callback_block_rate.
- Expected effect: strong conversion with stable event-handling behavior.
- Disconfirming outcome: low conversion or unstable payment event processing.
- Risks: PIX downtime and poor expiry defaults.
- Preconditions: payment-link lifecycle contract and callback idempotency strategy.
- Minimum instrumentation needed: link lifecycle events, conversion timestamps, callback dedupe logs.
- Recommended next step: run now.

### EX-4 - Fixed Split Validation

- Linked hypothesis: H4
- Decision owner: finance operations lead
- Business question: Does fixed split by level reduce payout disputes enough for early scale?
- Intervention: compute and expose payout entries using fixed percentages per hierarchy level.
- Target segment or scope: same pilot cohort used in EX-1 and EX-3.
- Duration or observation window: 2 settlement cycles.
- Primary signal: payout_dispute_rate.
- Secondary signals: payout_adjustment_count, payout_explanation_time_minutes.
- Expected effect: lower dispute volume and faster payout explanation.
- Disconfirming outcome: dispute rate remains unchanged.
- Risks: legacy contracts requiring exceptions.
- Preconditions: split table governance and versioning policy.
- Minimum instrumentation needed: payout records, dispute tags, split version metadata.
- Recommended next step: run now.

### EX-5 - Tenant Cadence Presets

- Linked hypothesis: H5
- Decision owner: central finance operations lead
- Business question: Should cadence be configurable by tenant in v1 or deferred?
- Intervention: allow approved cadence presets per tenant and monitor close outcomes.
- Target segment or scope: selected tenants with different transaction volumes.
- Duration or observation window: 3 close cycles.
- Primary signal: on_time_settlement_close_rate.
- Secondary signals: close_failure_rate, manual_override_rate.
- Expected effect: better close reliability across mixed tenant profiles.
- Disconfirming outcome: reliability worsens due to scheduling complexity.
- Risks: misconfigured presets and support burden.
- Preconditions: preset governance rules and default fallback cadence.
- Minimum instrumentation needed: close scheduler events, preset assignment logs, close SLA outcomes.
- Recommended next step: run after EX-1 to EX-4 baseline stabilizes.

## Sequencing Notes

1. Start EX-1 and EX-3 first to stabilize onboarding and collections.
2. Run EX-2 and EX-4 after KPI definitions and split versioning are in place.
3. Stage EX-5 after at least one baseline close cycle with default cadence.
