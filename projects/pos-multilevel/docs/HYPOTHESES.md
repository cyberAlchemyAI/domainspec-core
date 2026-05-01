# Hypotheses

## Hypothesis Register

| ID  | Proposition                                                                                               | Expected Effect                                                      | Confidence | Status   |
| --- | --------------------------------------------------------------------------------------------------------- | -------------------------------------------------------------------- | ---------- | -------- |
| H1  | Structured onboarding for vendors and submerchants reduces time-to-activation                             | Lower submerchant activation time                                    | high       | proposed |
| H2  | A hierarchy-aware operations dashboard improves vendor client management                                  | Higher active submerchants per vendor and faster issue triage        | medium     | proposed |
| H3  | PIX-only payment-link flow in v1 improves conversion and reduces operational complexity                   | Higher payment link conversion rate with stable settlement close SLA | medium     | proposed |
| H4  | Fixed percentage split by hierarchy level reduces payout disputes in early rollout                        | Lower payout dispute rate                                            | medium     | proposed |
| H5  | Tenant-configurable settlement cadence presets improve close reliability across different vendor profiles | Higher on-time settlement close rate                                 | medium     | proposed |

## Hypothesis Details

### H1 - Structured Onboarding Acceleration

- Proposition: If vendor and submerchant onboarding are standardized with explicit hierarchy placement, activation becomes faster and more predictable.
- Decision owner: product owner and vendor success lead
- Primary signal: submerchant_activation_time_hours
- Expected direction: reduce
- Current evidence: current operation exists but activation process is not yet formalized in platform contracts
- Evidence type: stated
- Why this might be true: standardized data requirements and step sequencing reduce rework loops.
- Strongest counterargument: compliance/KYC review may dominate cycle time regardless of workflow quality.
- Confounders: manual approval staffing, document quality, and seasonal onboarding volume.
- Disconfirming outcome: activation time does not improve after workflow standardization.
- Scope notes: first measured in retailer-focused pilot segment.

### H2 - Dashboard Visibility Gain

- Proposition: If central and vendor operators share a hierarchy-aware dashboard, client monitoring and intervention improve.
- Decision owner: central operations lead
- Primary signal: active_submerchants_per_vendor
- Expected direction: improve
- Current evidence: stated need for vendors to track clients and central to track vendor operations
- Evidence type: stated
- Why this might be true: shared operational visibility reduces blind spots and delayed actions.
- Strongest counterargument: visibility alone may not improve outcomes without clear operating playbooks.
- Confounders: metric freshness, user adoption quality, and dashboard training gaps.
- Disconfirming outcome: activity and intervention outcomes stay flat despite dashboard rollout.
- Scope notes: evaluate by central and vendor cohorts separately.

### H3 - PIX Link Focus Benefit

- Proposition: If v1 limits collections to PIX payment links, teams can improve payment conversion while keeping implementation and operations focused.
- Decision owner: product and engineering leads
- Primary signal: payment_link_conversion_rate
- Expected direction: improve
- Current evidence: payment method scope selected as PIX only for v1
- Evidence type: stated
- Why this might be true: one payment rail reduces UX and integration variance in first release.
- Strongest counterargument: excluding other methods can reduce reachable payer segments.
- Confounders: payer familiarity with PIX, expiry defaults, and communication channel quality.
- Disconfirming outcome: conversion underperforms compared to baseline/manual process.
- Scope notes: v1-only strategy, reassess when adding additional methods.

### H4 - Fixed Split Trust

- Proposition: If split logic is fixed percentage by hierarchy level in v1, payout interpretation disputes will decrease.
- Decision owner: finance operations lead
- Primary signal: payout_dispute_rate
- Expected direction: reduce
- Current evidence: commission model selected as fixed by level
- Evidence type: stated
- Why this might be true: deterministic formulas are easier to explain and audit.
- Strongest counterargument: fixed percentages may not match all contractual realities.
- Confounders: data quality in hierarchy mapping and contract exceptions.
- Disconfirming outcome: dispute volume remains high despite deterministic split logic.
- Scope notes: track dispute root cause taxonomy, not only aggregate rate.

### H5 - Cadence Preset Reliability

- Proposition: Tenant-configurable settlement cadence presets improve operational fit and close reliability versus one global cadence.
- Decision owner: finance operations and central platform leads
- Primary signal: on_time_settlement_close_rate
- Expected direction: improve
- Current evidence: cadence strategy selected as configurable by tenant
- Evidence type: stated
- Why this might be true: cadence can align with each tenant's business rhythm and volume profile.
- Strongest counterargument: too many cadence choices can increase misconfiguration and missed closes.
- Confounders: tenant setup quality and preset governance.
- Disconfirming outcome: close reliability decreases after enabling tenant-specific cadence.
- Scope notes: start with a small preset menu before expanding flexibility.

## Prioritization

| Hypothesis ID | Value If True | Cost To Test | Risk If Wrong | Priority |
| ------------- | ------------- | ------------ | ------------- | -------- |
| H1            | high          | low          | medium        | now      |
| H2            | high          | medium       | medium        | now      |
| H3            | high          | low          | medium        | now      |
| H4            | medium        | low          | medium        | now      |
| H5            | medium        | medium       | medium        | later    |
