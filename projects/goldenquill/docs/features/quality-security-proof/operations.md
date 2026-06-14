# Operations: Quality, Security & Proof

Operations, rules, calculations, queries, and events for the proof layer. Rules reference but never redefine the `CLAUDE.md` gate codes.

## AuthorGuardrailTest

Adds one typed test row to the [GuardrailTestMatrix](domain.md#guardrailtestmatrix) for a single fail-closed gate. Each row pairs a gate with a synthetic prohibited-input fixture and a fail-closed assertion.

**Source:** `quality-security-proof.AuthorGuardrailTest`
**Emits:** none (matrix mutation; coverage emits separately)

### Inputs

| Field             | Type            | Required |
| ----------------- | --------------- | -------- |
| gate              | FailClosedGate  | yes      |
| axis              | EnforcementAxis | yes      |
| fixture_ref       | string          | yes      |
| expected_behavior | string          | yes      |

### Business Rules

| ID    | Rule                                                                      | Enforcement                                                |
| ----- | ------------------------------------------------------------------------- | ---------------------------------------------------------- |
| R1    | [FailClosedAssertionRule](#failclosedassertionrule): assertion is fail-closed | See [FailClosedAssertionRule](#failclosedassertionrule)    |
| R2    | [Law3FixtureRule](#law3fixturerule): fixture is synthetic, never live `orgs/` | See [Law3FixtureRule](#law3fixturerule)                    |

<!-- Intentional convergence: FailClosedAssertionRule (test quality) and Law3FixtureRule (org isolation) are independent guards that both gate this operation. Not residue — every authored test must satisfy both. -->

### Postconditions

- A [GuardrailTest](domain.md#guardrailtest) row exists with `status = pending`
- The matrix `coverage_status` is `incomplete` until re-verified
- The gate code appears in the matrix `gates` set

### Error States

| Condition                              | Result                                  |
| -------------------------------------- | --------------------------------------- |
| Gate code not in any canonical roster  | Rejected — cannot test an unknown gate  |
| Fixture references live `orgs/` data   | Rejected by [Law3FixtureRule](#law3fixturerule) |

---

## VerifyMatrixCoverage

Asserts that every gate code enumerated in the matrix has at least one [GuardrailTest](domain.md#guardrailtest) row and that all rows pass. This is the deployment-eligibility META gate (mirrors `F-CLASS-COVERAGE-INCOMPLETE`).

**Source:** `quality-security-proof.VerifyMatrixCoverage`
**Emits:** [`quality-security-proof.MatrixCoverageVerified`](#matrixcoverageverified)

### Inputs

| Field     | Type   | Required |
| --------- | ------ | -------- |
| matrix_id | string | yes      |

### Business Rules

| ID    | Rule                                                                  | Enforcement                                      |
| ----- | --------------------------------------------------------------------- | ------------------------------------------------ |
| R3    | [CoverageRule](#coveragerule): every gate code has ≥1 test            | See [CoverageRule](#coveragerule)                |

### Calculations Applied

1. [CoverageRatioCalculation](#coverageratiocalculation) — covered gates ÷ total gates

### Postconditions

- `coverage_status = verified` only when ratio == 1.0 and all rows pass
- `quality-security-proof.MatrixCoverageVerified` is emitted on success
- Build consumers may read the verified state as deployment-eligible

### Error States

| Condition                          | Result                                          |
| ---------------------------------- | ----------------------------------------------- |
| Any gate code uncovered            | `coverage_status` stays `incomplete`; blocked   |
| Any test row `status = fail`       | Verification fails; deployment blocked          |

---

## RegisterClaim

Records a verbatim external claim and its target surface in the [ClaimsRegister](domain.md#claimsregister). Newly registered claims start at `draft` and are unshippable.

**Source:** `quality-security-proof.RegisterClaim`
**Emits:** none

### Inputs

| Field       | Type    | Required |
| ----------- | ------- | -------- |
| claim_text  | string  | yes      |
| surface     | string  | yes      |
| sales_touch | boolean | yes      |

### Postconditions

- A [Claim](domain.md#claim) exists with `status = draft`
- The claim is unshippable until evidence is resolved

### Error States

| Condition                  | Result                          |
| -------------------------- | ------------------------------- |
| Empty `claim_text`         | Rejected                        |
| Unknown `surface` value    | Rejected                        |

---

## ResolveEvidence

Binds a [Claim](domain.md#claim) to an [EvidenceCategory](domain.md#evidencecategory) and a resolvable [EvidenceHandle](domain.md#evidencehandle). A claim with no resolvable handle stays `draft`.

**Source:** `quality-security-proof.ResolveEvidence`
**Emits:** none

### Inputs

| Field             | Type             | Required |
| ----------------- | ---------------- | -------- |
| claim_id          | string           | yes      |
| evidence_category | EvidenceCategory | yes      |
| evidence_handle   | EvidenceHandle   | yes      |

### Business Rules

| ID    | Rule                                                                                | Enforcement                                          |
| ----- | ----------------------------------------------------------------------------------- | ---------------------------------------------------- |
| R4    | [EvidenceResolvableRule](#evidenceresolvablerule): handle must resolve              | See [EvidenceResolvableRule](#evidenceresolvablerule) |
| R5    | [ClassificationCheckRule](#classificationcheckrule): no `confidential` field rendered | See [ClassificationCheckRule](#classificationcheckrule) |

<!-- Intentional convergence: EvidenceResolvableRule (handle resolves) and ClassificationCheckRule (no confidential leak) are independent guards that both gate this operation. Not residue — both must pass to reach `evidenced`. -->

### Postconditions

- Claim `status = evidenced` when both rules pass
- The claim now carries a resolved [EvidenceHandle](domain.md#evidencehandle)
- The classification check result is recorded

### Error States

| Condition                                | Result                                              |
| ---------------------------------------- | --------------------------------------------------- |
| Evidence handle does not resolve         | Stays `draft`; flagged unshippable                  |
| `classification_check = fail`            | Blocked by [ClassificationCheckRule](#classificationcheckrule) |
| `evidence_category` outside closed set   | Rejected                                            |

---

## ApproveClaim

Records Josh approval for a claim. Required before any `sales_touch: true` claim may ship.

**Source:** `quality-security-proof.ApproveClaim`
**Emits:** [`quality-security-proof.ClaimApproved`](#claimapproved)

### Inputs

| Field        | Type   | Required |
| ------------ | ------ | -------- |
| claim_id     | string | yes      |
| approver_ref | string | yes      |

### Business Rules

| ID    | Rule                                                                       | Enforcement                                      |
| ----- | -------------------------------------------------------------------------- | ------------------------------------------------ |
| R6    | [SalesTouchApprovalRule](#salestouchapprovalrule): sales-touch needs Josh  | See [SalesTouchApprovalRule](#salestouchapprovalrule) |

### Postconditions

- Claim `status = approved`
- `quality-security-proof.ClaimApproved` is emitted
- A sales-touch claim may now proceed to `shipped`

### Error States

| Condition                            | Result                                      |
| ------------------------------------ | ------------------------------------------- |
| Claim not yet `evidenced`            | Rejected — cannot approve unevidenced claim |
| Approver is not Josh on a sales-touch claim | Blocked by [SalesTouchApprovalRule](#salestouchapprovalrule) |

---

## DefineInstrument

Registers one [InstrumentDefinition](domain.md#instrumentdefinition) in the [InstrumentCatalog](domain.md#instrumentcatalog) with its source, cadence, and consumer.

**Source:** `quality-security-proof.DefineInstrument`
**Emits:** none

### Inputs

| Field           | Type           | Required |
| --------------- | -------------- | -------- |
| metric_name     | string         | yes      |
| unit            | string         | yes      |
| source          | string         | yes      |
| capture_cadence | CaptureCadence | yes      |
| consumer        | string         | yes      |

### Business Rules

| ID    | Rule                                                                          | Enforcement                                      |
| ----- | ----------------------------------------------------------------------------- | ------------------------------------------------ |
| R7    | [DecimalDisciplineRule](#decimaldisciplinerule): unit is Decimal/int, no float | See [DecimalDisciplineRule](#decimaldisciplinerule) |
| R8    | [ReceiptFieldExistsRule](#receiptfieldexistsrule): CycleReceipt source must exist | See [ReceiptFieldExistsRule](#receiptfieldexistsrule) |

<!-- Intentional convergence: DecimalDisciplineRule (A12 no-float) and ReceiptFieldExistsRule (no invented §17 fields) are independent guards that both gate this operation. Not residue — both must pass to define an instrument. -->

### Postconditions

- An [InstrumentDefinition](domain.md#instrumentdefinition) exists in the catalog
- The instrument is routed to its named consumer
- The unit passed the A12 no-float check

### Error States

| Condition                                   | Result                                          |
| ------------------------------------------- | ----------------------------------------------- |
| Float unit supplied                         | Blocked by [DecimalDisciplineRule](#decimaldisciplinerule) |
| CycleReceipt source field does not exist    | Blocked by [ReceiptFieldExistsRule](#receiptfieldexistsrule) |

---

## CaptureRenewalIntent

Records a Day-60 [RenewalIntentCapture](domain.md#renewalintentcapture) reading via the QSP-defined form. Feeds `INS-QSP-RENEWAL-INTENT`.

**Source:** `quality-security-proof.CaptureRenewalIntent`
**Emits:** none

### Inputs

| Field    | Type                | Required |
| -------- | ------------------- | -------- |
| node_ref | string              | yes      |
| signal   | RenewalIntentSignal | yes      |
| note     | string              | no       |

### Postconditions

- A [RenewalIntentCapture](domain.md#renewalintentcapture) reading exists
- The reading feeds `INS-QSP-RENEWAL-INTENT`

### Error States

| Condition                       | Result                          |
| ------------------------------- | ------------------------------- |
| `signal` outside the enum       | Rejected                        |
| `node_ref` references live org  | Rejected (Law 3)                |

---


## CoverageRule

Every gate code enumerated by the matrix must have at least one [GuardrailTest](domain.md#guardrailtest) row. Mirrors `F-CLASS-COVERAGE-INCOMPLETE` (referenced, not redefined).

**Formal:**
```
∀ g ∈ matrix.gates: ∃ t ∈ matrix.tests: t.gate.code == g.code
```

### Invariants

| ID        | Invariant                                                              |
| --------- | --------------------------------------------------------------------- |
| COV-INV-1 | A matrix with `coverage_status == verified` has zero uncovered gates  |
| COV-INV-2 | The 16 F-CLASS-* and 12 F-WPFA-* codes are each present in `gates`    |

## FailClosedAssertionRule

A guardrail test must assert *fail-closed behavior* (blocked deployment / no cloud emission / route-to-LOCAL), not merely that an exception was raised.

**Formal:**
```
∀ t ∈ matrix.tests: t.expected_behavior ∈ {blocked, local_route, no_cloud_egress}
```

### Invariants

| ID        | Invariant                                                             |
| --------- | --------------------------------------------------------------------- |
| FCA-INV-1 | No test passes on a mere raised exception without a fail-closed claim |

## Law3FixtureRule

Every test fixture must be synthetic; no fixture may reference live `orgs/<slug>/` client data (Law 3, Org Isolation).

**Formal:**
```
∀ t ∈ matrix.tests: ¬ references_live_org(t.fixture_ref)
```

### Invariants

| ID        | Invariant                                                       |
| --------- | --------------------------------------------------------------- |
| L3F-INV-1 | No fixture path resolves under a live `orgs/<slug>/` directory  |
| L3F-INV-2 | Synthetic fixtures use `orgs/_TEMPLATE` shape only              |
| L3F-INV-3 | A fixture referencing live client data fails the Law 3 self-check |

## EvidenceResolvableRule

A claim cannot leave `draft` unless its [EvidenceHandle](domain.md#evidencehandle) resolves to a real artifact.

**Formal:**
```
claim.status ≠ draft ⇒ resolves(claim.evidence_handle.handle)
```

### Invariants

| ID        | Invariant                                                          |
| --------- | ------------------------------------------------------------------ |
| EVR-INV-1 | A `shipped` claim has a non-empty, resolvable evidence handle      |
| EVR-INV-2 | `security-review`-backed claims stay `draft` until reviewer signs  |
| EVR-INV-3 | A claim with an unresolvable handle is flagged unshippable         |
| EVR-INV-4 | Resolution is idempotent for the same handle                      |

## ClassificationCheckRule

A claim's evidence may not render any field whose classification register entry is `confidential` (mirrors `F-WPFA-PDF-CONFIDENTIAL-LEAK`).

**Formal:**
```
claim.status ∈ {evidenced, approved, shipped} ⇒ claim.classification_check == pass
```

### Invariants

| ID        | Invariant                                                            |
| --------- | -------------------------------------------------------------------- |
| CLC-INV-1 | No evidenced claim renders a `confidential`-classified field         |
| CLC-INV-2 | A failing classification check blocks promotion past `draft`         |
| CLC-INV-3 | The check mirrors but does not redefine `F-WPFA-PDF-CONFIDENTIAL-LEAK` |
| CLC-INV-4 | Public/shareable fields pass; confidential/operator_flagged fail     |
| CLC-INV-5 | The check runs before any sales-touch approval                       |

## SalesTouchApprovalRule

A sales-touch claim cannot reach `shipped` without a recorded Josh approval.

**Formal:**
```
claim.sales_touch ∧ claim.status == shipped ⇒ approved_by_josh(claim)
```

### Invariants

| ID        | Invariant                                                       |
| --------- | --------------------------------------------------------------- |
| STA-INV-1 | A `sales_touch` claim cannot ship without a recorded approver   |
| STA-INV-2 | Non-sales-touch claims may ship on evidence alone               |
| STA-INV-3 | Approval is recorded with an approver_ref before `shipped`      |
| STA-INV-4 | Approval cannot be inferred; it must be explicit                |
| STA-INV-5 | A revoked approval returns the claim below `shipped`            |
| STA-INV-6 | Only Josh is a valid approver for sales-touch claims            |

## DecimalDisciplineRule

No instrument unit may be a float; monetary uses Decimal, energy uses int micro-watt-hours (A12 mandate).

**Formal:**
```
∀ i ∈ catalog.instruments: i.unit ∉ {float, double}
```

### Invariants

| ID        | Invariant                                                         |
| --------- | ----------------------------------------------------------------- |
| DEC-INV-1 | No instrument unit is `float` or `double`                         |
| DEC-INV-2 | Monetary instruments use Decimal                                  |
| DEC-INV-3 | Energy instruments use int micro-watt-hours                       |
| DEC-INV-4 | Count instruments use int                                         |
| DEC-INV-5 | A float-unit definition fails the A12 self-check                  |
| DEC-INV-6 | The rule extends A12 to energy quantities per WPFA §17            |
| DEC-INV-7 | Unit strings are validated at definition time, not at capture     |

## ReceiptFieldExistsRule

Any instrument whose `source` derives from the WPFA CycleReceipt must name a field that already exists on the §17 sub-kind — no invented receipt fields.

**Formal:**
```
∀ i ∈ catalog.instruments:
    is_cycle_receipt_source(i.source) ⇒ i.source ∈ CycleReceipt.fields
```

### Invariants

| ID        | Invariant                                                          |
| --------- | ------------------------------------------------------------------ |
| RFE-INV-1 | A CycleReceipt-sourced instrument names an existing §17 field      |
| RFE-INV-2 | An invented receipt field name fails definition                    |
| RFE-INV-3 | Non-CycleReceipt sources (support log, Day-60) are exempt          |
| RFE-INV-4 | Field existence is checked against the §17 sub-kind, not assumed    |
| RFE-INV-5 | Source-field drift after a §17 change re-triggers the check        |
| RFE-INV-6 | The rule does not mutate the §17 sub-kind                          |
| RFE-INV-7 | Energy/dollar fields map to the A12 Decimal/int micro-watt-hour types |
| RFE-INV-8 | A renamed §17 field invalidates the prior instrument definition    |

---


## CoverageRatioCalculation

Derives the matrix coverage ratio used by [VerifyMatrixCoverage](#verifymatrixcoverage).

**Formula:**
```
coverage_ratio = |{ g ∈ gates : ∃ t : t.gate.code == g.code }| / |gates|
```

**Properties:** bounded in [0, 1]; deterministic; equals 1.0 iff every gate is covered.

---


## GetUncoveredGates

Lists every gate code in the [GuardrailTestMatrix](domain.md#guardrailtestmatrix) that has no test row. Used by the META gate and by build consumers to see what blocks eligibility.

**Reads From:** [GuardrailTestMatrix](domain.md#guardrailtestmatrix)

### Inputs

| Field     | Type   | Required |
| --------- | ------ | -------- |
| matrix_id | string | yes      |

### Output

List of gate codes with zero associated tests (empty list ⇒ deployment-eligible).

## GetApprovedClaims

Returns claims at `status = approved` (or `shipped`) for a surface. This is the read model `sales-contracting-legal` consumes to know which claims it may cite.

**Reads From:** [ClaimsRegister](domain.md#claimsregister)

### Inputs

| Field        | Type   | Required |
| ------------ | ------ | -------- |
| surface      | string | no       |
| include_shipped | boolean | no    |
| evidence_category | string | no  |

### Output

List of approved [Claim](domain.md#claim) entries with resolved evidence handles.

## GetInstrumentsForConsumer

Returns the [InstrumentDefinition](domain.md#instrumentdefinition) entries routed to a named consumer (`data-room` / `day-60` / `validation-packet` / `node-care`).

**Reads From:** [InstrumentCatalog](domain.md#instrumentcatalog)

### Inputs

| Field    | Type   | Required |
| -------- | ------ | -------- |
| consumer | string | yes      |

### Output

List of instrument definitions whose `consumer` matches.

---


## MatrixCoverageVerified

Announces that the [GuardrailTestMatrix](domain.md#guardrailtestmatrix) reached full coverage with all rows passing — the signal that gates build deployment-eligibility.

**Produced by:** [VerifyMatrixCoverage](#verifymatrixcoverage)

### Schema

| Field          | Type   | Description                          |
| -------------- | ------ | ------------------------------------ |
| matrix_id      | string | The verified matrix                  |
| coverage_ratio | string | Decimal ratio (must equal 1.0)       |
| verified_at    | string | ISO timestamp of verification        |

### Consumed By

| Consumer                  | Action                                          |
| ------------------------- | ----------------------------------------------- |
| `tilth-runtime-build`     | Marks build deployment-eligible                 |
| `hardware-golden-image`   | Marks golden image deployment-eligible          |

## ClaimApproved

Announces that a [Claim](domain.md#claim) received the approval required for sales use.

**Produced by:** [ApproveClaim](#approveclaim)

### Payload

| Field        | Type   | Description                |
| ------------ | ------ | -------------------------- |
| claim_id     | string | The approved claim         |
| approver_ref | string | Recorded approver identity |

### Consumed By

| Consumer                   | Action                                        |
| -------------------------- | --------------------------------------------- |
| `sales-contracting-legal`  | Permits citing the claim in customer copy     |
