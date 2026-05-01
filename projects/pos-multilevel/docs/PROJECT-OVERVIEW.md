# POS Multilevel

## Summary

POS Multilevel is a multi-tenant payment operations platform where a central controller manages vendors, and vendors manage submerchants or stores. The platform focuses on onboarding, operational visibility, and payment-link flows that support multi-level commercial operations. The immediate goal is to launch a constrained v1 slice with clear hierarchy rules and measurable operational outcomes.

## Discovery Mode

- Mode: greenfield
- Project state: partial implementation
- Interview date: 2026-05-01
- Operator / owner: pos-multilevel project owner

## Problem Framing

- Primary user or customer: central controller operating a vendor network that serves submerchants and stores
- Core problem: hierarchy operations, client visibility, and payment-link flows are hard to coordinate consistently across central, vendor, and store layers
- Value proposition: one dashboard-driven model for onboarding, network tracking, and payment-link operations with explicit hierarchy rules
- Business goal: improve activation speed, payment-link throughput, and operational visibility across the network
- Non-goals: full in-person POS hardware lifecycle, non-PIX payment rails in v1, and full ERP/payroll replacement

## Current State

| Item                    | Status  | Evidence Type | Notes                                                                                                   |
| ----------------------- | ------- | ------------- | ------------------------------------------------------------------------------------------------------- |
| Product scope           | partial | stated        | v1 scope is onboarding, operations dashboard, and payment-link creation.                                |
| Domain boundaries       | partial | stated        | Operating model is central controller -> vendor -> submerchant/store (3 levels).                        |
| Existing implementation | partial | stated        | There is an existing retailer operation context, but no repository implementation yet for this project. |
| Metrics baseline        | partial | stated        | Operational activity exists, but baseline KPIs are not yet formalized in a single metric contract.      |

Evidence type:

- observed = seen in repository or artifacts
- stated = given by operator
- hypothesized = inferred but not yet validated

## Actors And Stakeholders

| Actor                        | Goal                                               | Pain Point                                                 | Frequency | Evidence Type |
| ---------------------------- | -------------------------------------------------- | ---------------------------------------------------------- | --------- | ------------- |
| Central Controller Operator  | Oversee vendor and submerchant network performance | Limited unified visibility across vendor operations        | daily     | stated        |
| Vendor Operator              | Track clients and execute payment operations       | Hard to monitor all submerchant activity from one place    | daily     | stated        |
| Submerchant / Store Operator | Activate and receive payments quickly              | Onboarding and payment setup can be fragmented             | daily     | stated        |
| Finance Operations           | Ensure predictable split and settlement behavior   | Multi-level payout calculations are hard to audit manually | weekly    | hypothesized  |
| Platform Admin               | Configure hierarchy and policy safely              | Incorrect hierarchy or split setup can affect many tenants | weekly    | hypothesized  |

## Candidate Bounded Contexts

| Context                     | Responsibility                                                  | Key Concepts                                       | Status    | Evidence Type |
| --------------------------- | --------------------------------------------------------------- | -------------------------------------------------- | --------- | ------------- |
| Network Onboarding          | Onboard vendors and submerchants into hierarchy                 | hierarchy node, onboarding status, tenant profile  | candidate | stated        |
| Vendor Operations Dashboard | Provide central and vendor visibility over client operations    | vendor KPI, client status, activity timeline       | candidate | stated        |
| Payment Link Management     | Create and monitor PIX payment links                            | payment link, PIX payload, link status, expiry     | candidate | stated        |
| Commission And Settlement   | Apply fixed split policy and close funds by tenant cadence      | commission split, accrual entry, settlement window | candidate | stated        |
| Access And Governance       | Enforce permissions and auditability for high-impact operations | role, permission, decision trace                   | candidate | hypothesized  |

## Core Workflows

| Workflow                        | Trigger                                        | Main Steps                                                                 | Failure Mode                                        | Evidence Type |
| ------------------------------- | ---------------------------------------------- | -------------------------------------------------------------------------- | --------------------------------------------------- | ------------- |
| Onboard Vendor And Submerchant  | central or vendor starts onboarding            | submit profile -> validate hierarchy placement -> activate account         | incomplete compliance data blocks activation        | stated        |
| Track Network Operations        | operator opens dashboard                       | aggregate client metrics -> filter by hierarchy -> inspect status/outliers | stale data or missing drill-down context            | stated        |
| Create Payment Link             | vendor or submerchant requests collection link | validate permissions -> create PIX link -> publish and track status        | invalid payload or expired link before payment      | stated        |
| Process PIX Payment And Split   | PIX confirmation received                      | validate payment event -> mark link paid -> apply fixed split by level     | duplicate callback or split mismatch                | hypothesized  |
| Close Settlement By Tenant Rule | configured settlement window reached           | collect paid transactions -> compute tenant close -> publish close report  | cadence misconfiguration or reconciliation mismatch | stated        |

## Constraints

| Constraint                                           | Type        | Why It Matters                                          | Evidence Type |
| ---------------------------------------------------- | ----------- | ------------------------------------------------------- | ------------- |
| Hierarchy depth fixed to 3 levels in v1              | business    | Keeps policy and visibility manageable in first release | stated        |
| Payment method limited to PIX in v1                  | technical   | Reduces integration surface and speeds launch           | stated        |
| Commission model is fixed percentage by level        | business    | Creates predictable split behavior for first rollout    | stated        |
| Settlement cadence configurable by tenant            | operational | Different vendor profiles need different close windows  | stated        |
| Deterministic rounding and idempotent event handling | technical   | Prevents duplicate or inconsistent financial effects    | hypothesized  |
| Permission-first write controls with audit traces    | business    | Protects high-impact hierarchy and financial operations | hypothesized  |

## Success Signals

| Signal                            | Why It Matters                                       | Current Baseline | Target Direction |
| --------------------------------- | ---------------------------------------------------- | ---------------- | ---------------- |
| submerchant_activation_time_hours | Measures onboarding efficiency                       | unknown          | reduce           |
| active_submerchants_per_vendor    | Measures network adoption and vendor productivity    | unknown          | improve          |
| payment_link_conversion_rate      | Measures payment-link effectiveness                  | unknown          | improve          |
| payout_dispute_rate               | Measures trust in fixed split model                  | unknown          | reduce           |
| on_time_settlement_close_rate     | Measures settlement reliability under tenant cadence | unknown          | improve          |

## Risks And Unknowns

| Risk                                                           | Why Risky                                                | Severity | What Would Reduce It                                          |
| -------------------------------------------------------------- | -------------------------------------------------------- | -------- | ------------------------------------------------------------- |
| Onboarding compliance requirements are not yet explicit        | Activation could stall if required documents are unclear | high     | Define KYC/compliance checklist and decision ownership        |
| PIX-only dependency creates concentration risk                 | Outage or provider changes can pause collections         | medium   | Define fallback and alert policy for PIX disruptions          |
| Fixed split may not fit all vendor contracts                   | Some vendor agreements may require exceptions            | medium   | Define allowed exception model and approval workflow          |
| Tenant cadence flexibility can increase operational complexity | Too many cadence options can hurt close reliability      | medium   | Limit cadence presets and monitor close SLA by tenant profile |
| Dashboard data freshness expectations are not set              | Operators may lose trust if figures lag                  | medium   | Define freshness SLO and drill-down traceability              |

## Recommended Next Artifacts

1. docs/features/network-onboarding/SPEC.md
2. docs/features/vendor-operations-dashboard/SPEC.md
3. docs/features/payment-link-management/SPEC.md
4. docs/features/commission-settlement/SPEC.md

## Open Questions

1. Which KYC/compliance fields are mandatory at vendor and submerchant onboarding time?
2. What are default and maximum payment-link expiration windows per tenant?
3. Should split accrual happen on payment confirmation or on settlement close for v1?
