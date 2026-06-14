# Domain: Quality, Security & Proof

Structural concepts for the proof layer. Gate primitives (F-CLASS-* / F-WPFA-* / the Five Laws) are owned by `CLAUDE.md` and are *referenced* here as [FailClosedGate](#failclosedgate) value objects — never redefined.


## GuardrailTestMatrix

The canonical, single-source matrix that maps every locked fail-closed gate code to at least one executable acceptance test. Persisted as `guardrail-test-matrix.yaml`. It is the file the META coverage gate checks against, and the artifact `hardware-golden-image` / `tilth-runtime-build` must see green before a build is deployment-eligible.

| Field            | Type                                          | Required | Description                                                       |
| ---------------- | --------------------------------------------- | -------- | ----------------------------------------------------------------- |
| matrix_id        | string                                        | yes      | Unique identifier per deployment                                  |
| gates            | [FailClosedGate](#failclosedgate)[]           | yes      | Every gate code that must be covered                              |
| tests            | [GuardrailTest](#guardrailtest)[]             | yes      | Authored test rows                                                |
| coverage_status  | [MatrixCoverageStatus](#matrixcoveragestatus) | yes      | Whether every gate code has ≥1 test                               |

**Operations:** [AuthorGuardrailTest](operations.md#authorguardrailtest), [VerifyMatrixCoverage](operations.md#verifymatrixcoverage)

---

## GuardrailTest

One row of the matrix: a `(gate → prohibited-input fixture → assert fail-closed)` acceptance test. The defining discipline is that it asserts *fail-closed behavior* (no cloud emission / no deployment / route-to-LOCAL), not merely that an exception was raised.

| Field             | Type                                  | Required | Description                                                       |
| ----------------- | ------------------------------------- | -------- | ----------------------------------------------------------------- |
| test_id           | string                                | yes      | Stable `T-QSP-*` id; never renumbered on insert                   |
| gate              | FailClosedGate                        | yes      | The gate code this test exercises (see matrix container)          |
| axis              | [EnforcementAxis](#enforcementaxis)   | yes      | Which of the four enforcement axes                                |
| fixture_ref       | string                                | yes      | Path to the synthetic prohibited-input fixture                    |
| expected_behavior | string                                | yes      | The fail-closed assertion (blocked / LOCAL / no-egress)           |
| status            | [TestStatus](#teststatus)             | yes      | pass / fail / pending                                             |

**Contained by:** [GuardrailTestMatrix](#guardrailtestmatrix) (child row; the matrix is the actor that performs `AuthorGuardrailTest`)

---

## ClaimsRegister

The append-only audit of every external/customer-facing claim Golden Quill makes, persisted as `claims-register.yaml`. One per node. It is the upstream gate for `sales-contracting-legal`: sales copy may cite a claim only when its register entry is `approved`.

| Field      | Type                       | Required | Description                            |
| ---------- | -------------------------- | -------- | -------------------------------------- |
| register_id | string                    | yes      | Unique identifier per node             |
| claims     | [Claim](#claim)[]          | yes      | All registered claims                  |

**Operations:** [RegisterClaim](operations.md#registerclaim), [ResolveEvidence](operations.md#resolveevidence), [ApproveClaim](operations.md#approveclaim)

---

## Claim

A single verbatim external claim and its evidence binding, modeled on the WPFA buyer-facing chain (`CLAUDE.md` §17: claim → coefficient + cycle_id + trace_id). A claim cannot reach `shipped` without a resolved [EvidenceHandle](#evidencehandle) and a passing classification check.

| Field               | Type                                  | Required | Description                                                       |
| ------------------- | ------------------------------------- | -------- | ----------------------------------------------------------------- |
| claim_id            | string                                | yes      | `CLM-QSP-*` id                                                    |
| claim_text          | string                                | yes      | Verbatim external claim                                           |
| surface             | string                                | yes      | sales_one_pager / demo / website / LOI / validation_packet / node_care |
| evidence_category   | [EvidenceCategory](#evidencecategory) | yes      | One of the 8-category closed set                                  |
| evidence_handle     | [EvidenceHandle](#evidencehandle)     | yes      | Concrete resolvable artifact reference                            |
| classification_check | string                               | yes      | pass / fail — may not render a `confidential` field               |
| sales_touch         | boolean                               | yes      | If true, Josh approval required before ship                       |
| status              | [ClaimStatus](#claimstatus)           | yes      | draft / evidenced / approved / shipped                            |

**Lifecycle:** draft → evidenced → approved → shipped (governed by [ClaimStatus](#claimstatus))
**Contained by:** [ClaimsRegister](#claimsregister) (child entry; the register is the actor that performs `RegisterClaim`, `ResolveEvidence`, `ApproveClaim`)

---

## InstrumentCatalog

The catalog of all defined measurement instruments for a node, persisted as `instrument-definitions.yaml`. One per node. Enforces that no instrument carries a float unit (A12).

| Field       | Type                                          | Required | Description                  |
| ----------- | --------------------------------------------- | -------- | ---------------------------- |
| catalog_id  | string                                        | yes      | Unique identifier per node   |
| instruments | [InstrumentDefinition](#instrumentdefinition)[] | yes    | All defined instruments      |

**Operations:** [DefineInstrument](operations.md#defineinstrument)

---

## InstrumentDefinition

One typed measurement instrument. Source fields that derive from the WPFA CycleReceipt must already exist on the §17 sub-kind — no invented receipt fields.

| Field           | Type                              | Required | Description                                                |
| --------------- | --------------------------------- | -------- | ---------------------------------------------------------- |
| instrument_id   | string                            | yes      | `INS-QSP-*` id                                             |
| metric_name     | string                            | yes      | Human-readable metric name                                 |
| unit            | string                            | yes      | Decimal or int unit; never float (A12)                     |
| source          | string                            | yes      | CycleReceipt field / support issue log / Day-60 review     |
| capture_cadence | [CaptureCadence](#capturecadence) | yes      | per-cycle / per-node / per-quarter / ongoing               |
| baseline_target | string                            | yes      | Value or `TBD-first-node`                                  |
| consumer        | string                            | yes      | data-room / day-60 / validation-packet / node-care         |

**Contained by:** [InstrumentCatalog](#instrumentcatalog) (child entity; the catalog is the actor that performs `DefineInstrument`)

---

## RenewalIntentCapture

A single Day-60 renewal-intent reading for a node, captured via the QSP-defined form so Customer Success records it consistently (row 76). Feeds `INS-QSP-RENEWAL-INTENT`.

| Field        | Type                                        | Required | Description                          |
| ------------ | ------------------------------------------- | -------- | ------------------------------------ |
| capture_id   | string                                      | yes      | Unique identifier per reading        |
| node_ref     | string                                      | yes      | Synthetic node reference (Law 3)     |
| signal       | [RenewalIntentSignal](#renewalintentsignal) | yes      | strong / neutral / at-risk           |
| note         | string                                      | no       | Free-text qualifier                  |
| captured_at  | string                                      | yes      | ISO timestamp of the Day-60 reading  |

**Operations:** [CaptureRenewalIntent](operations.md#capturerenewalintent)

---


## FailClosedGate

A reference to a named gate code defined and owned by `CLAUDE.md`. This value object carries the code string and its origin clause; it **never redefines** the gate semantics. It exists so the matrix can enumerate coverage without mutating the canonical roster.

| Field      | Type   | Constraint                                                                 |
| ---------- | ------ | -------------------------------------------------------------------------- |
| code       | string | Must match an existing `F-CLASS-*` / `F-WPFA-*` code, or a Five-Laws ref   |
| roster     | string | `f-class` (16) / `f-wpfa` (12) / `five-laws`                               |
| source_ref | string | `CLAUDE.md` clause where the code is canonically defined                   |

**Equality:** Two FailClosedGate values are equal iff their `code` strings are equal.

---

## EvidenceHandle

A concrete, resolvable pointer to the artifact that backs a claim. Resolvability is the load-bearing property: a claim with an unresolvable handle may not ship.

| Field          | Type   | Constraint                                                                       |
| -------------- | ------ | -------------------------------------------------------------------------------- |
| handle         | string | Artifact path / test id / `coefficient_id`+`cycle_id`+`trace_id` / signature id  |
| provenance_ref | string | Logfire trace_id / signed-receipt id / reviewer sign-off id / `n/a-structural`   |

**Equality:** Equal iff `handle` and `provenance_ref` both match.

### Invariants

| ID        | Invariant                                                          |
| --------- | ------------------------------------------------------------------ |
| EVH-INV-1 | A handle backing a `shipped` claim must resolve to a real artifact |
| EVH-INV-2 | `n/a-structural` provenance is admissible only for boundary attestations |

---

## Enums

### EnforcementAxis

The four guardrail-test axes from BUILD-SPEC §1.2.

| Value              | Description                                                       |
| ------------------ | ----------------------------------------------------------------- |
| posture            | Posture enforcement (Frontier-Eligible / Split-Context / Local-Only) |
| classification     | Per-field classification routing                                  |
| audit              | Audit completeness (spans, boundary events, hashes)               |
| fail-closed-meta   | META coverage + WPFA receipt integrity + Five Laws gates          |

---

### EvidenceCategory

The closed set of evidence categories (BUILD-SPEC §2.2). No claim may cite a category outside this set.

| Value                   | Description                                          |
| ----------------------- | ---------------------------------------------------- |
| guardrail-test          | Backed by a §1 matrix test id                        |
| security-review         | Independent reviewer sign-off                        |
| wpfa-receipt            | WPFA CycleReceipt (coefficient + cycle_id + trace)   |
| instrumentation-metric  | A §3 `INS-QSP-*` instrument metric                   |
| demo-integrity          | Canonical live-demo standard (never staged-as-live)  |
| deployment-test         | Internal install-from-checklist run                  |
| architecture-lock       | Locked architecture / Five Laws clause               |
| structural-attestation  | Operator Ed25519 boundary signature                  |

---

### ClaimStatus

Claim lifecycle.

| Value     | Description                                              |
| --------- | -------------------------------------------------------- |
| draft     | Registered, evidence not yet resolved — unshippable      |
| evidenced | Evidence handle resolved and classification check passed |
| approved  | Josh-approved (required for any sales-touch claim)       |
| shipped   | Live in customer-facing copy                             |

---

### RenewalIntentSignal

Day-60 renewal-intent enum (BUILD-SPEC §3.2 `INS-QSP-RENEWAL-INTENT`).

| Value   | Description                       |
| ------- | --------------------------------- |
| strong  | Strong renewal intent             |
| neutral | Undecided                         |
| at-risk | Renewal at risk                   |

---

### CaptureCadence

Instrument capture rhythm.

| Value       | Description                  |
| ----------- | ---------------------------- |
| per-cycle   | Captured each grant cycle    |
| per-node    | Captured once per node       |
| per-quarter | Captured each quarter        |
| ongoing     | Continuously accumulated     |

---

### MatrixCoverageStatus

| Value      | Description                                          |
| ---------- | ---------------------------------------------------- |
| incomplete | At least one gate code has no test row               |
| verified   | Every gate code has ≥1 test and the META gate is green |

---

### TestStatus

| Value   | Description                          |
| ------- | ------------------------------------ |
| pending | Authored, not yet run                |
| pass    | Fail-closed behavior demonstrated    |
| fail    | Gate did not fail closed             |
