# Test Spec: Capital Logic Library

Test obligations derived from the spec. IDs follow `T-{ASPECT}-{Concept}-{nn}`.
All fixtures are synthetic (no real client data, no `orgs/` reads — Law 3) and no
fixture asserts fabricated authoritative card/rule content (Law 5).

## Entity Structural Invariants

| ID                              | Scenario                                                        | Expect |
| ------------------------------- | --------------------------------------------------------------- | ------ |
| T-OP-CapitalLogicCard-01        | CapitalLogicCard rejects any `cic_binding` field at construction | reject |
| T-OP-CustomerIdentityCard-01    | CustomerIdentityCard rejects `primary_capital_logic_activations` binding | reject |
| T-OP-RulePack-01                | RulePack rejects any `cic_coupling` field at construction       | reject |

## ValidateCard (Operation)

| ID                       | Scenario                                                              | Expect    |
| ------------------------ | -------------------------------------------------------------------- | --------- |
| T-OP-ValidateCard-01     | CLC card with valid `clc_id` in the closed 8 (ClosedSetRule pass)    | accept    |
| T-OP-ValidateCard-02     | Card with identifier outside the closed set (ClosedSetRule fail)     | reject    |
| T-OP-ValidateCard-03     | CLC card carrying a `cic_binding` field (AntiCouplingRule fail)      | reject    |
| T-OP-ValidateCard-04     | CIC card with no CLC subset anywhere (AntiCouplingRule pass)         | accept    |
| T-OP-ValidateCard-05     | CIC card whose `capital_logic_activation` lists a CLC subset         | reject    |
| T-OP-ValidateCard-06     | CIC card missing a primitive or quadrant (R3 fail)                   | reject    |
| T-OP-ValidateCard-07     | Postcondition: structure conforms to family schema                  | holds     |
| T-OP-ValidateCard-08     | Postcondition: anti-coupling invariant holds                        | holds     |
| T-OP-ValidateCard-09     | Postcondition: card eligible to advance in CardLifecycle            | holds     |
| T-OP-ValidateCard-10     | Error: identifier not in closed set → closed-set violation          | reject    |
| T-OP-ValidateCard-11     | Error: CIC↔CLC binding present → F-CIC-CLC-COUPLING-VIOLATION        | reject    |
| T-OP-ValidateCard-12     | Error: missing primitive/quadrant on CIC card                       | reject    |

## ValidateRulePack (Operation)

| ID                          | Scenario                                                            | Expect |
| --------------------------- | ------------------------------------------------------------------ | ------ |
| T-OP-ValidateRulePack-01    | Pack with provenance + every req evidence_ref (ProvenanceRule pass) | accept |
| T-OP-ValidateRulePack-02    | Pack missing source_provenance (ProvenanceRequiredRule fail)        | reject |
| T-OP-ValidateRulePack-03    | Pack with a CIC-coupling field (AntiCouplingRule fail)              | reject |
| T-OP-ValidateRulePack-04    | Pack with no CIC coupling (AntiCouplingRule pass)                   | accept |
| T-OP-ValidateRulePack-05    | `observed_clc_tags` all within closed 8 (ClosedSetRule pass)        | accept |
| T-OP-ValidateRulePack-06    | `observed_clc_tags` with unknown tag (ClosedSetRule fail)           | reject |
| T-OP-ValidateRulePack-07    | Missing `next_review_due` (R8 fail)                                 | reject |
| T-OP-ValidateRulePack-08    | Postcondition: pack + requirements carry provenance                 | holds  |
| T-OP-ValidateRulePack-09    | Postcondition: no CIC-coupling field present                        | holds  |
| T-OP-ValidateRulePack-10    | Postcondition: observed tags labeled non-binding, within 8         | holds  |
| T-OP-ValidateRulePack-11    | Error: missing evidence_ref → provenance violation                  | reject |
| T-OP-ValidateRulePack-12    | Error: CIC-coupling field → F-CIC-CLC-COUPLING-VIOLATION            | reject |
| T-OP-ValidateRulePack-13    | Error: unknown CLC tag → closed-set violation                       | reject |
| T-OP-ValidateRulePack-14    | Error: missing next_review_due → staleness not computable           | reject |

## RegisterRulePack (Operation)

| ID                          | Scenario                                                            | Expect |
| --------------------------- | ------------------------------------------------------------------ | ------ |
| T-OP-RegisterRulePack-01    | Register a validated pack with future next_review_due → active     | accept |
| T-OP-RegisterRulePack-02    | Register a pack not previously validated (R9 fail)                 | reject |
| T-OP-RegisterRulePack-03    | Register duplicate rule_pack_id                                    | reject |
| T-OP-RegisterRulePack-04    | Admitted pack tags remain within closed 8 (R10 pass)               | accept |
| T-OP-RegisterRulePack-05    | Postcondition: pack admitted at active or stale per computed status | holds  |
| T-OP-RegisterRulePack-06    | Postcondition: stale pack emits RulePackMarkedStale                | holds  |
| T-OP-RegisterRulePack-07    | Error: pack not validated → validation gate                        | reject |
| T-OP-RegisterRulePack-08    | Error: duplicate id → already registered                           | reject |

## StalenessComputation (Calculation)

| ID                              | Scenario                                                | Expect  |
| ------------------------------- | ------------------------------------------------------- | ------- |
| T-OP-StalenessComputation-01    | next_review_due < now → stale                           | stale   |
| T-OP-StalenessComputation-02    | next_review_due >= now → active                         | active  |
| T-OP-StalenessComputation-03    | program retired → retired regardless of dates           | retired |
| T-OP-StalenessComputation-04    | Determinism: same inputs → same status                  | holds   |
| T-OP-StalenessComputation-05    | Monotone: once stale, stays stale until re-review       | holds   |

## GetCardDefaults (Query)

| ID                          | Scenario                                                            | Expect |
| --------------------------- | ------------------------------------------------------------------ | ------ |
| T-QR-GetCardDefaults-01     | Returns all five operational-primitive defaults for a CIC          | shape  |
| T-QR-GetCardDefaults-02     | Returns four-quadrant profile                                      | shape  |
| T-QR-GetCardDefaults-03     | `capital_logic_activation` default carries no CLC subset           | holds  |
| T-QR-GetCardDefaults-04     | Unknown cic_id → not found                                         | reject |
| T-QR-GetCardDefaults-05     | No `orgs/` data accessed (Law 3)                                   | holds  |

## RulePackMarkedStale (Event)

| ID                              | Scenario                                              | Expect |
| ------------------------------- | ----------------------------------------------------- | ------ |
| T-EV-RulePackMarkedStale-01     | Emitted by RegisterRulePack when computed status stale | emit   |
| T-EV-RulePackMarkedStale-02     | Transitions RulePackLifecycle active → stale          | holds  |
| T-EV-RulePackMarkedStale-03     | Consumer: maintainer schedules re-review              | holds  |

## CapitalLogicLibraryModule (Interface)

| ID                              | Scenario                                                        | Expect |
| ------------------------------- | --------------------------------------------------------------- | ------ |
| T-IF-validateCard-01            | `validateCard` exposes ValidateCard; rejects coupling-bearing card | reject |
| T-IF-getCardDefaults-01         | `getCardDefaults` exposes GetCardDefaults; returns CIC defaults | shape  |
| T-IF-validateRulePack-01        | `validateRulePack` exposes ValidateRulePack; fail-closed on no provenance | reject |
| T-IF-registerRulePack-01        | `registerRulePack` exposes RegisterRulePack; admits validated pack | accept |

## CardLifecycle (State Machine)

| ID                          | Scenario                                                            | Expect |
| --------------------------- | ------------------------------------------------------------------ | ------ |
| T-ST-CardLifecycle-01       | draft → in_authoring                                               | accept |
| T-ST-CardLifecycle-02       | in_authoring → validated_v1 with expert_reviewed == true           | accept |
| T-ST-CardLifecycle-03       | in_authoring → validated_v1 without expert review (non-Farmer)     | reject |
| T-ST-CardLifecycle-04       | validated_v1 → superseded                                          | accept |
| T-ST-CardLifecycle-05       | Invalid: draft → validated_v1                                      | reject |
| T-ST-CardLifecycle-06       | Invalid: superseded → validated_v1 (terminal)                      | reject |
| T-ST-CardLifecycle-07       | Invariant CL-INV-1: validated_v1 requires expert review            | holds  |
| T-ST-CardLifecycle-08       | Invariant CL-INV-2: identifier never changes                       | holds  |

## RulePackLifecycle (State Machine)

| ID                              | Scenario                                                        | Expect |
| ------------------------------- | --------------------------------------------------------------- | ------ |
| T-ST-RulePackLifecycle-01       | draft → active on register                                      | accept |
| T-ST-RulePackLifecycle-02       | active → stale when next_review_due elapsed                     | accept |
| T-ST-RulePackLifecycle-03       | stale → active on re-review                                     | accept |
| T-ST-RulePackLifecycle-04       | active → retired                                                | accept |
| T-ST-RulePackLifecycle-05       | stale → retired                                                 | accept |
| T-ST-RulePackLifecycle-06       | Invalid: draft → stale                                          | reject |
| T-ST-RulePackLifecycle-07       | Invalid: retired → active (terminal)                            | reject |
| T-ST-RulePackLifecycle-08       | Invariant RPL-INV-1: staleness computed, never asserted         | holds  |
| T-ST-RulePackLifecycle-09       | Invariant RPL-INV-2: provenance present in non-terminal states  | holds  |
