# Initial Definitions

## Glossary Seed

| Term                      | Working Definition                                                | Category      | Status | Evidence Type |
| ------------------------- | ----------------------------------------------------------------- | ------------- | ------ | ------------- |
| Central controller        | Top-level operator supervising vendor network performance         | role          | draft  | stated        |
| Vendor                    | Mid-level operator managing a portfolio of submerchants or stores | role          | draft  | stated        |
| Submerchant               | Retail client under a vendor that receives payments               | role          | draft  | stated        |
| Hierarchy node            | Organizational unit in the central -> vendor -> submerchant chain | business term | draft  | stated        |
| Payment link              | Shareable request-to-pay artifact with amount, status, and expiry | workflow      | draft  | stated        |
| PIX payment               | Instant transfer payment method used in v1 flows                  | system        | draft  | stated        |
| Commission split          | Fixed percentage distribution by hierarchy level                  | policy        | draft  | stated        |
| Settlement window         | Tenant-defined cadence window used for close operations           | workflow      | draft  | stated        |
| Idempotency key           | Deterministic key used to prevent duplicate payment/split effects | system        | draft  | hypothesized  |
| Governance decision trace | Record of policy inputs and selected outcome                      | workflow      | draft  | hypothesized  |

## Bounded Context Definitions

| Context                     | Responsibility                                                | In Scope                                                    | Out Of Scope                                | Status    |
| --------------------------- | ------------------------------------------------------------- | ----------------------------------------------------------- | ------------------------------------------- | --------- |
| Network Onboarding          | Onboard and activate vendor/submerchant accounts in hierarchy | profile submission, hierarchy assignment, activation status | payroll and HR setup                        | candidate |
| Vendor Operations Dashboard | Expose central and vendor visibility over client operations   | KPI cards, client status, activity timeline                 | advanced BI/data warehouse modeling         | candidate |
| Payment Link Management     | Create, publish, and monitor PIX payment links                | link creation, expiry, status updates, payment events       | non-PIX payment rails in v1                 | candidate |
| Commission And Settlement   | Compute fixed level splits and perform cadence-based close    | split accrual, settlement window close, close report        | variable contract engine beyond fixed split | candidate |
| Access And Governance       | Protect high-impact operations and capture audit evidence     | roles, permission checks, decision traces                   | identity provider internals                 | candidate |

## Core Concepts

| Concept                     | Suggested Meta-Type | Context                   | Description                                              | Status |
| --------------------------- | ------------------- | ------------------------- | -------------------------------------------------------- | ------ |
| CentralTenant               | Entity              | Network Onboarding        | Top-level tenant that supervises vendors and policies    | draft  |
| VendorAccount               | Entity              | Network Onboarding        | Vendor identity and operating profile in the hierarchy   | draft  |
| SubmerchantAccount          | Entity              | Network Onboarding        | Retail client account under a vendor                     | draft  |
| PaymentLink                 | Entity              | Payment Link Management   | Link object with amount, PIX payload, status, and expiry | draft  |
| PaymentLinkStatus           | State Machine       | Payment Link Management   | Lifecycle from created to paid, expired, or canceled     | draft  |
| PaymentMethod               | Enum / Type         | Payment Link Management   | Allowed methods for v1 (PIX only)                        | draft  |
| FixedLevelSplitPolicy       | Policy              | Commission And Settlement | Fixed percentage allocation by hierarchy level           | draft  |
| CreatePaymentLink           | Operation           | Payment Link Management   | Validates request and creates trackable payment link     | draft  |
| PixPaymentConfirmed         | Event               | Payment Link Management   | Event emitted when PIX transfer is confirmed             | draft  |
| CloseTenantSettlement       | Workflow            | Commission And Settlement | Closes tenant window and publishes split report          | draft  |
| SettlementAuthorizationRule | Rule                | Access And Governance     | Blocks close when permission or preconditions fail       | draft  |

## Rules And Policies

| Name                          | Type      | Description                                                              | Source    | Status |
| ----------------------------- | --------- | ------------------------------------------------------------------------ | --------- | ------ |
| HierarchyDepthRule            | rule      | Hierarchy depth is constrained to central -> vendor -> submerchant in v1 | interview | draft  |
| PixOnlyPaymentPolicy          | policy    | Only PIX payment links are valid in v1                                   | interview | draft  |
| FixedPercentageSplitPolicy    | policy    | Split percentages are fixed by hierarchy level in v1                     | interview | draft  |
| TenantSettlementCadencePolicy | policy    | Each tenant can define approved settlement cadence preset                | interview | draft  |
| MonetaryRoundingInvariant     | invariant | Monetary outputs are normalized to two decimals at boundaries            | stated    | draft  |
| IdempotentPaymentEventRule    | rule      | Duplicate PIX callbacks must not duplicate financial effects             | inferred  | draft  |
| PermissionDenyByDefaultPolicy | policy    | Missing permission mapping resolves to deny for writes                   | stated    | draft  |

## External Interfaces

| Interface                            | Purpose                                                  | Owner                  | Dependency Type | Status    |
| ------------------------------------ | -------------------------------------------------------- | ---------------------- | --------------- | --------- |
| POST /api/v1/vendors/onboarding      | Create and start vendor onboarding flow                  | pos-multilevel backend | user-facing     | candidate |
| POST /api/v1/submerchants/onboarding | Create and start submerchant onboarding flow             | pos-multilevel backend | user-facing     | candidate |
| GET /api/v1/dashboard/operations     | Return central/vendor operational dashboard metrics      | pos-multilevel backend | user-facing     | candidate |
| POST /api/v1/payment-links           | Create PIX payment link for a submerchant                | pos-multilevel backend | user-facing     | candidate |
| GET /api/v1/payment-links/{id}       | Inspect payment-link lifecycle and payment status        | pos-multilevel backend | user-facing     | candidate |
| POST /api/v1/settlements/close       | Trigger tenant settlement close using configured cadence | pos-multilevel backend | user-facing     | candidate |

## Metrics And Definitions

| Metric                            | Definition                                                 | Decision It Supports                             | Status |
| --------------------------------- | ---------------------------------------------------------- | ------------------------------------------------ | ------ |
| submerchant_activation_time_hours | median(activation_completed_at - onboarding_started_at)    | Is onboarding flow efficient enough for rollout? | draft  |
| active_submerchants_per_vendor    | active_submerchant_count / active_vendor_count             | Is vendor network adoption healthy?              | draft  |
| payment_link_conversion_rate      | paid_links / created_links                                 | Are payment links effective for collections?     | draft  |
| payout_dispute_rate               | disputed_payout_entries / total_payout_entries             | Is split model trusted by operators?             | draft  |
| on_time_settlement_close_rate     | settlement_closes_within_sla / total_settlement_closes     | Is tenant cadence operating reliably?            | draft  |
| duplicate_event_block_rate        | duplicate_callbacks_blocked / duplicate_callbacks_received | Is idempotency control working as expected?      | draft  |

## Ambiguities To Resolve

| Topic                                       | Why Ambiguous                                                      | Resolution Needed                                          |
| ------------------------------------------- | ------------------------------------------------------------------ | ---------------------------------------------------------- |
| Onboarding compliance checklist             | Activation requires clear mandatory documents and validation rules | Define v1 KYC/compliance schema for vendor and submerchant |
| Payment-link expiration policy              | Expiry affects conversion and fraud/abuse risk                     | Define default and max expiry by tenant tier               |
| Refund and reversal behavior for paid links | Reversal logic affects split and settlement integrity              | Define reversal operation contract and timing              |
| Cadence preset boundaries                   | Too much flexibility can reduce close reliability                  | Define allowed cadence presets and tenant eligibility      |
