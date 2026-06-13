# Queries: Capital Logic Library

## GetCardDefaults

Returns the archetype-level operational-primitive defaults for a CIC card. These are
the **Card-level archetype defaults** — layer 1 of the classification three-layer
default chain (Card → operator override → per-grant SP0). Configuration only; never an
eligibility constraint across the CIC/CLC axes.

**Type:** Query

### Inputs

| Field  | Type            | Required |
| ------ | --------------- | -------- |
| cic_id | CICIdentifier   | yes      |

### Reads From

- [CustomerIdentityCard](domain.md#customeridentitycard) — the five operational primitives and four-quadrant profile

### Output

| Field                  | Type                | Source                                         |
| ---------------------- | ------------------- | ---------------------------------------------- |
| search_vocabulary      | object              | CustomerIdentityCard.operational_primitives    |
| evidence_schema        | object              | CustomerIdentityCard.operational_primitives    |
| language_register      | object              | CustomerIdentityCard.operational_primitives    |
| reporting_rhythm       | object              | CustomerIdentityCard.operational_primitives    |
| capital_logic_activation | object            | CustomerIdentityCard.operational_primitives (config; no CLC subset) |
| profile                | FourQuadrantProfile | CustomerIdentityCard.profile                   |

### Authorization

- Public library read; no `orgs/` data accessed (Law 3).
