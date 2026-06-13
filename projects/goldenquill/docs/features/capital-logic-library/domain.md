# Domain: Capital Logic Library

Structural concepts for the Capital Logic Library — the governed, machine-readable
representation of the Eight Capital Logic Cards (CLC), the Six Customer Identity
Cards (CIC), and the funder rule-pack schema. All concepts are funder-side /
archetype-side public artifacts; none reference `orgs/` data (Law 3). CIC and CLC
are orthogonal — no concept here may carry a design-time CIC→CLC binding.

## Entities

### CapitalLogicCard

A governed CLC card: the funder-side representation of *why/how funding flows*
(underwriting logic + example sources). One of the canonical eight, identified by
[CLCIdentifier](#clcidentifier). A CLC card MUST NOT enumerate which CICs it serves.

| Field           | Type                              | Required | Description                                              |
| --------------- | --------------------------------- | -------- | -------------------------------------------------------- |
| clc_id          | [CLCIdentifier](#clcidentifier)   | yes      | Closed-set identifier (exactly one of the eight)         |
| envelope        | [CardEnvelope](#cardenvelope)     | yes      | Shared card header                                       |
| funding_logic   | string                            | yes      | Underwriting logic — why/how funding flows               |
| example_sources | string[]                          | yes      | Illustrative funder/program classes (examples, not bindings) |
| cic_binding     | FORBIDDEN                         | no       | **Forbidden field — no CLC card may enumerate CICs (anti-coupling)** |

**Lifecycle:** See [CardLifecycle](states.md#cardlifecycle)
**Operations:** [ValidateCard](operations.md#validatecard)

---

### CustomerIdentityCard

A governed CIC card: the applicant-side representation of *what world the applicant
operates in*. One of the canonical six, identified by [CICIdentifier](#cicidentifier).
Carries five [OperationalPrimitive](#operationalprimitive) configurations and one
[FourQuadrantProfile](#fourquadrantprofile). Its `capital_logic_activation` primitive
configures HOW the CIC processes whatever CLC an opportunity activates at runtime; it
MUST NOT enumerate a CLC subset.

| Field                  | Type                                              | Required | Description                                                  |
| ---------------------- | ------------------------------------------------- | -------- | ------------------------------------------------------------ |
| cic_id                 | [CICIdentifier](#cicidentifier)                   | yes      | Closed-set identifier (exactly one of the six)               |
| envelope               | [CardEnvelope](#cardenvelope)                     | yes      | Shared card header                                           |
| coverage_axis          | string                                            | yes      | Production / Learning / Public Sector / Culture / Member Ownership / Intermediary Infrastructure |
| includes               | string[]                                          | yes      | Sub-world enumeration ("Includes" band)                      |
| operational_primitives | [OperationalPrimitive](#operationalprimitive)[]   | yes      | Exactly five (search_vocabulary, evidence_schema, language_register, reporting_rhythm, capital_logic_activation) |
| profile                | [FourQuadrantProfile](#fourquadrantprofile)       | yes      | Four-quadrant operational profile                            |
| primary_capital_logic_activations | FORBIDDEN                              | no       | **Legacy footer band forbidden as a binding; if present, relabeled "Common patterns observed historically — not a constraint"** |

**Lifecycle:** See [CardLifecycle](states.md#cardlifecycle)
**Operations:** [ValidateCard](operations.md#validatecard)

---

### RulePack

A versioned, funder-scoped set of codified hard requirements for a recurring
funder/program — the deterministic constraints an application must satisfy. Packs are
per-cycle (the decay unit). A pack MAY record `observed_clc_tags` (non-binding, from
the closed eight only) but MUST NOT carry any field constraining which CIC may apply.

| Field             | Type                                          | Required | Description                                            |
| ----------------- | --------------------------------------------- | -------- | ------------------------------------------------------ |
| rule_pack_id      | string (slug)                                 | yes      | `<funder>__<program>__<fy>`                            |
| funder_name       | string                                        | yes      | Display name                                           |
| program_name      | string                                        | yes      | Display name                                           |
| fiscal_year       | string                                        | yes      | Cycle this pack codifies (decay unit)                  |
| schema_version    | string (semver)                               | yes      | Of the rule-pack schema                                |
| source_provenance | [SourceProvenance](#sourceprovenance)         | yes      | Mandatory — no pack without a citable source           |
| requirements      | [FunderRequirement](#funderrequirement)[]     | yes      | Codified hard requirements                             |
| maintenance       | [MaintenanceBlock](#maintenanceblock)         | yes      | Decay metadata driving staleness                       |
| status            | [RulePackStatus](#rulepackstatus)             | yes      | draft \| active \| stale \| retired                    |
| observed_clc_tags | [CLCIdentifier](#clcidentifier)[]             | no       | Non-binding observed CLC(s); never references a CIC    |
| cic_coupling      | FORBIDDEN                                     | no       | **Forbidden field — no pack may constrain CIC eligibility (anti-coupling)** |

**Lifecycle:** See [RulePackLifecycle](states.md#rulepacklifecycle)
**Operations:** [ValidateRulePack](operations.md#validaterulepack), [RegisterRulePack](operations.md#registerrulepack)

---

## Value Objects

### CardEnvelope

The shared header carried by both card families. Diverges only in the body fields of
the owning entity.

| Field          | Type                              | Constraint                                          |
| -------------- | --------------------------------- | --------------------------------------------------- |
| card_id        | string (slug)                     | e.g. `clc-public-purpose-works`, `cic-food-systems` |
| card_family    | [CardFamily](#cardfamily)         | clc \| cic                                          |
| canonical_ref  | string                            | Drawing ID (`TILTH-CLC-00` / `TILTH-CIC-REVIEW-01`) |
| display_name   | string                            | From canonical naming in `CLAUDE.md`                |
| schema_version | string (semver)                   | Of the card schema                                  |
| status         | [CardStatus](#cardstatus)         | draft \| in_authoring \| validated_v1 \| superseded |
| asset_ref      | string                            | Optional PNG visual-layer counterpart path          |

**Equality:** Two envelopes are equal if `card_id` and `schema_version` match.

---

### OperationalPrimitive

One of the five configuration blocks a CIC card carries. Configuration, never an
eligibility constraint across the CIC/CLC axes.

| Field      | Type   | Constraint                                                                       |
| ---------- | ------ | -------------------------------------------------------------------------------- |
| name       | string | One of: search_vocabulary, evidence_schema, language_register, reporting_rhythm, capital_logic_activation |
| config     | object | Archetype-level default configuration block                                      |
| clc_subset | FORBIDDEN | **The `capital_logic_activation` primitive MUST NOT list a CLC subset (anti-coupling)** |

**Equality:** Equal if `name` and serialized `config` match.

---

### FourQuadrantProfile

The four-quadrant operational profile a CIC card carries; downstream Tilth components
read it.

| Field                    | Type   | Constraint               |
| ------------------------ | ------ | ------------------------ |
| operating_reality        | string | Required quadrant        |
| tilth_configuration      | string | Required quadrant        |
| evidence_signals         | string | Required quadrant        |
| funding_reporting_rhythm | string | Required quadrant        |

**Equality:** Equal if all four quadrant strings match.

---

### FunderRequirement

The testable unit inside a rule pack — one codified hard requirement with a typed
check shape and mandatory evidence pointer.

| Field        | Type                                            | Constraint                                              |
| ------------ | ----------------------------------------------- | ------------------------------------------------------- |
| req_id       | string                                          | Stable within pack                                      |
| kind         | [RequirementKind](#requirementkind)             | Closed set                                              |
| statement    | string                                          | Human-readable hard requirement                         |
| check_shape  | [CheckShape](#checkshape)                       | Deterministic check class (so Logician can realize it)  |
| params       | object                                          | Bound values (conditional on check_shape)               |
| severity     | [RequirementSeverity](#requirementseverity)     | hard_fail \| warn (default hard_fail)                   |
| evidence_ref | string                                          | Mandatory pointer into the pack's SourceProvenance      |
| clc_binding  | FORBIDDEN                                        | **Forbidden — no requirement may bind to / constrain a CIC (anti-coupling)** |

**Equality:** Equal if `req_id` and `statement` match.

---

### SourceProvenance

The citable source backing a rule pack (Law 1, Law 5). No rule may exist without one.

| Field          | Type   | Constraint                          |
| -------------- | ------ | ----------------------------------- |
| source_type    | string | `rfa` \| `program_page`             |
| url_or_handle  | string | Citable location                    |
| retrieved_date | date   | When the source was captured        |
| quote_or_section | string | Verbatim quote or section reference |

**Equality:** Equal if `url_or_handle` and `quote_or_section` match.

---

### MaintenanceBlock

Decay metadata that makes the ONGOING marker auditable. Staleness is computed from
`next_review_due`, never asserted.

| Field           | Type                                  | Constraint                                |
| --------------- | ------------------------------------- | ----------------------------------------- |
| review_cadence  | string                                | e.g. `annual` (cadence value is operator data) |
| last_reviewed   | date                                  | When the pack was last reviewed           |
| next_review_due | date                                  | Drives deterministic staleness            |
| maintainer_role | string                                | Symbolic role ("Capital Logic Library maintainer") |
| status          | [RulePackStatus](#rulepackstatus)     | current \| stale \| retired projection    |

**Equality:** Equal if `next_review_due` and `maintainer_role` match.

---

## Enums

### CardFamily

| Value | Description                       |
| ----- | --------------------------------- |
| clc   | Capital Logic Card (funder-side)  |
| cic   | Customer Identity Card (applicant-side) |

### CardStatus

| Value         | Description                                              |
| ------------- | -------------------------------------------------------- |
| draft         | Skeleton authored, not yet in active authoring           |
| in_authoring  | Being authored / under expert review                     |
| validated_v1  | Expert-reviewed and validated (Farmer exempt — already v1)|
| superseded    | Replaced by a newer card version                         |

### CLCIdentifier

The closed set of exactly eight Capital Logic Cards (TILTH-CLC-00).

| Value                          | Description                                  |
| ------------------------------ | -------------------------------------------- |
| public_purpose_works           | Mandate, eligibility, civic-benefit funding  |
| catalytic_change               | Transition, innovation, demonstration funding|
| operating_capacity             | Staffing, systems, equipment, readiness      |
| research_evidence              | Inquiry, evaluation, pilots, proof-building   |
| market_access                  | Buyers, channels, commercialization, demand   |
| credit_underwriting            | Loans, guarantees, repayment, finance-readiness |
| sponsorship_corporate_support  | Corporate sponsors, gifts, partnerships       |
| shared_assets                  | Cooperative infrastructure, commons           |

### CICIdentifier

The closed set of exactly six Customer Identity Categories (TILTH-CIC-REVIEW-01).

| Value                  | Description                                       |
| ---------------------- | ------------------------------------------------- |
| food_systems           | Seasonal multi-activity funding world             |
| educator               | Compliance-dense learning institution             |
| public_agency          | Public-accountability funding environment         |
| arts_culture           | Merit-plus-sustainability funding world           |
| cooperative            | Member-governed ownership system                  |
| ecosystem_intermediary | Portfolio-scale ecosystem connector               |

### RequirementKind

| Value           | Description                          |
| --------------- | ------------------------------------ |
| eligibility     | Who may apply                        |
| format          | Document format constraints          |
| deadline        | Deadline structure                   |
| attachment      | Required attachments                 |
| limit           | Page / word / count limits           |
| match_cost_share | Match or cost-share requirements    |
| registration    | Registration prerequisites (SAM/UEI) |
| other           | Catch-all for atypical hard requirements |

### CheckShape

| Value          | Description                              |
| -------------- | ---------------------------------------- |
| boolean        | True/false predicate                     |
| numeric_bound  | Numeric threshold (e.g. max_pages)       |
| date           | Date comparison (e.g. deadline)          |
| set_membership | Value must be in an allowed set          |
| presence       | A required element must be present       |

### RequirementSeverity

| Value     | Description                                 |
| --------- | ------------------------------------------- |
| hard_fail | Violation blocks the application (default)  |
| warn      | Violation surfaces a warning, not a block   |

### RulePackStatus

| Value   | Description                                          |
| ------- | ---------------------------------------------------- |
| draft   | Authored, not yet admitted to the library            |
| active  | Current and admitted; `next_review_due` in the future|
| stale   | `next_review_due` is past (computed, not asserted)   |
| retired | Program retired; pack no longer applies              |
