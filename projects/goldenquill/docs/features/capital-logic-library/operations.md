# Operations: Capital Logic Library

## ValidateCard

Validates a CLC or CIC card against its closed set, structural completeness, and the
anti-coupling invariant before the card may advance toward `validated_v1`. Fail-closed.

> **Intentional rule convergence.** This operation is guarded by both
> [ClosedSetRule](#closedsetrule) and [AntiCouplingRule](#anticouplingrule). These rules
> are deliberately distinct and independent guards on the same validation gate — not a
> missing relationship. An LLM compiler should realize them as separate predicates, both
> required, no shared parent.

**Actor:** [CapitalLogicCard](domain.md#capitallogiccard)

### Inputs

| Field    | Type             | Required |
| -------- | ---------------- | -------- |
| card     | CapitalLogicCard or CustomerIdentityCard | yes |
| family   | CardFamily       | yes      |

### Rules

| ID  | Rule                                                                     | Enforcement                                          |
| --- | ------------------------------------------------------------------------ | ---------------------------------------------------- |
| R1  | [ClosedSetRule](#closedsetrule): identifier must be a member of the correct closed set (8 CLC / 6 CIC) | See [ClosedSetRule](#closedsetrule) |
| R2  | [AntiCouplingRule](#anticouplingrule): no CLC card enumerates CICs; no CIC `capital_logic_activation` lists a CLC subset; no `primary_capital_logic_activations` binding | See [AntiCouplingRule](#anticouplingrule) |
| R3  | CIC cards must define all five operational primitives and all four quadrant keys | Structural completeness check                        |
| R4  | Transition to `validated_v1` requires `governance.expert_reviewed == true` for the card's segment | Farmer exempt — already v1                            |

### Postconditions

- Card structure conforms to its family schema
- Anti-coupling invariant holds (no design-time CIC↔CLC binding)
- Card is eligible to advance in [CardLifecycle](states.md#cardlifecycle)

### Error States

| Condition                                  | Result                                  |
| ------------------------------------------ | --------------------------------------- |
| Identifier not in closed set               | Reject — closed-set violation           |
| CIC↔CLC binding field present              | Reject — `F-CIC-CLC-COUPLING-VIOLATION` |
| Missing primitive or quadrant on a CIC card | Reject — incomplete structure          |

---

## ValidateRulePack

Validates a funder rule pack: mandatory provenance, typed requirements, closed-set
`observed_clc_tags`, and the absence of any CIC-coupling field. Fail-closed.

> **Intentional rule convergence.** Guarded by [ProvenanceRequiredRule](#provenancerequiredrule),
> [AntiCouplingRule](#anticouplingrule), and [ClosedSetRule](#closedsetrule). The three are
> independent, separately-testable guards on one gate — intentional, not an inferred shared
> parent. AntiCouplingRule and ClosedSetRule are reused across ValidateCard and
> ValidateRulePack by design (both gates enforce the same orthogonality + closed-set canon).

**Actor:** [RulePack](domain.md#rulepack)

### Inputs

| Field | Type     | Required |
| ----- | -------- | -------- |
| pack  | RulePack | yes      |

### Rules

| ID  | Rule                                                                            | Enforcement                                  |
| --- | ------------------------------------------------------------------------------- | -------------------------------------------- |
| R5  | [ProvenanceRequiredRule](#provenancerequiredrule): pack carries `source_provenance` and every requirement carries `evidence_ref` | See [ProvenanceRequiredRule](#provenancerequiredrule) |
| R6  | [AntiCouplingRule](#anticouplingrule): no requirement or pack field constrains CIC eligibility from a CLC | See [AntiCouplingRule](#anticouplingrule) |
| R7  | [ClosedSetRule](#closedsetrule): any `observed_clc_tags` entry draws only from the canonical eight | See [ClosedSetRule](#closedsetrule) |
| R8  | `maintenance.next_review_due` is present (staleness must be computable)          | Presence check                               |

### Postconditions

- Pack and all requirements carry citable provenance
- No CIC-coupling field present
- `observed_clc_tags` (if any) are labeled non-binding and within the closed eight

### Error States

| Condition                                | Result                                  |
| ---------------------------------------- | --------------------------------------- |
| Missing pack provenance or evidence_ref  | Reject — provenance violation           |
| CIC-coupling field present               | Reject — `F-CIC-CLC-COUPLING-VIOLATION` |
| Unknown CLC tag                          | Reject — closed-set violation           |
| Missing `next_review_due`                | Reject — staleness not computable       |

---

## RegisterRulePack

Admits a validated rule pack into the library, computes its initial staleness via
[StalenessComputation](#stalenesscomputation), and emits a staleness event when the
computed status is `stale`.

**Actor:** [RulePack](domain.md#rulepack)
**Emits:** [RulePackMarkedStale](events.md#rulepackmarkedstale)

### Inputs

| Field | Type     | Required |
| ----- | -------- | -------- |
| pack  | RulePack | yes      |
| now   | date     | yes      |

### Rules

| ID  | Rule                                                                  | Enforcement                          |
| --- | --------------------------------------------------------------------- | ------------------------------------ |
| R9  | Pack must have passed [ValidateRulePack](#validaterulepack) first      | Precondition gate                    |
| R10 | [ClosedSetRule](#closedsetrule): admitted pack tags remain within closed eight | See [ClosedSetRule](#closedsetrule) |

### Calculations Applied

1. [StalenessComputation](#stalenesscomputation) — derives status from `maintenance.next_review_due` vs `now`

### Postconditions

- Pack is admitted at status `active` or `stale` per computed result
- If computed `stale`, emits [RulePackMarkedStale](events.md#rulepackmarkedstale)

### Error States

| Condition                          | Result                       |
| ---------------------------------- | ---------------------------- |
| Pack not previously validated      | Reject — validation gate     |
| Duplicate `rule_pack_id`           | Reject — already registered  |

---

## StalenessComputation

Pure function deriving a rule pack's status from its maintenance block. Deterministic:
same `next_review_due` and `now` always produce the same status.

**Type:** Calculation
Derives a status for [RegisterRulePack](#registerrulepack).

### Formula

```
status = retired   if program retired
       = stale     if next_review_due < now
       = active     otherwise
```

### Properties

- Deterministic (no clock read inside; `now` is an input)
- Total (defined for all date inputs)
- Monotone: once `next_review_due < now`, status stays `stale` until re-reviewed

---

## AntiCouplingRule

The load-bearing invariant: no schema construct may bind a Customer Identity Category
to a subset of Capital Logic Cards, or vice versa. CIC and CLC are orthogonal; matching
is opportunity-driven at runtime, never archetype-driven at design time.

**Type:** Rule
Enforces [ValidateCard](#validatecard) and [ValidateRulePack](#validaterulepack).

| ID         | Expression                                                                                  |
| ---------- | ------------------------------------------------------------------------------------------- |
| ACR-INV-1  | No CapitalLogicCard carries a `cic_binding` field                                           |
| ACR-INV-2  | No CustomerIdentityCard `capital_logic_activation` primitive lists a CLC subset             |
| ACR-INV-3  | No `primary_capital_logic_activations` binding is present on any CIC card                   |
| ACR-INV-4  | No FunderRequirement or RulePack field constrains CIC eligibility                           |

Violation of any → fail closed under `F-CIC-CLC-COUPLING-VIOLATION` (architecture v7.0.8).

---

## ClosedSetRule

Identifiers and tags must resolve to the canonical closed sets: exactly eight CLCs
(TILTH-CLC-00) and exactly six CICs (TILTH-CIC-REVIEW-01). No ninth card, no aliases
promoted to first-class members.

**Type:** Rule
Enforces [ValidateCard](#validatecard), [ValidateRulePack](#validaterulepack), and [RegisterRulePack](#registerrulepack).

| ID        | Expression                                                              |
| --------- | ----------------------------------------------------------------------- |
| CSR-INV-1 | `clc_id ∈ CLCIdentifier` (cardinality 8)                                |
| CSR-INV-2 | `cic_id ∈ CICIdentifier` (cardinality 6)                                |
| CSR-INV-3 | `∀ tag ∈ observed_clc_tags : tag ∈ CLCIdentifier`                       |

---

## ProvenanceRequiredRule

No rule pack and no requirement may exist without a citable source (Law 1, source of
truth; Law 5, applicant brings substance — never fabricate).

**Type:** Rule
Enforces [ValidateRulePack](#validaterulepack).

| ID        | Expression                                                       |
| --------- | ---------------------------------------------------------------- |
| PRR-INV-1 | `pack.source_provenance` is present and well-formed             |
| PRR-INV-2 | `∀ req ∈ pack.requirements : req.evidence_ref` is non-empty      |
