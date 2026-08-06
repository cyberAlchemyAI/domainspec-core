# Stage 06 — Invoke Design

## Design status

`authored-complete`, not implemented and not validator-passed.

## View 1 — Requirements

- `Q1`: every QRY-003 terminal path resolves to success or one code from the closed vocabulary.
- `Q2`: simultaneous failures select one deterministic primary code while retaining subordinate gaps.
- `Q3`: QueryReceipt nullability and algorithm migration are explicit.
- `R1`: exactly 25 relation candidates receive one finite disposition.
- `R2`: every retained relation has a behavior-changing planned witness.
- `B1`: closed research evidence remains read-only; ontology creation and execution are excluded.

## View 2 — Components

| Component | Responsibility | Output |
| --- | --- | --- |
| `TerminalContract` | Map success/failure paths and select primary abstention code. | Query decision plus subordinate gaps. |
| `QueryReceiptInvariant` | Validate success/null and abstention/non-null constraints. | Pass/fail validation finding. |
| `RelationWitnessRegistry` | Store one 25-row disposition and witness design per relation. | Retained, merged, deferred, or killed set. |
| `MutationHarnessPlan` | Define baseline and single-mutant comparison without executing it. | Expected delta and failure assertion. |
| `MigrationRule` | Version repaired behavior without rewriting history. | New `algorithm_version` and immutable old receipts. |

## View 3 — Data contracts

### Query contract

```text
TerminalCase {
  path_id
  input_constraints
  selected_ids
  primary_abstention_code
  subordinate_gaps[]
  clearing_criterion
  algorithm_version
}
```

On success, `selected_ids` is non-empty and `primary_abstention_code` is null. On abstention, the primary code is declared and non-null.

### Relation witness row

```text
RelationWitness {
  relation_id
  relation_name
  source_fixture
  target_fixture
  consumer
  baseline_output
  mutation
  expected_mutant_delta
  failure_assertion
  disposition: RETAIN | MERGE | DEFER | KILL
  witness_status: planned
  execution_status: planned_not_executed
}
```

`RETAIN` requires every behavioral field. `MERGE` requires a canonicalization or equality-validation decision. `DEFER` requires a named missing behavior contract. `KILL` requires a recorded absence-of-necessity rationale.

## View 4 — Behavior

1. Resolve and validate exact version context.
2. Evaluate compatibility and evidence gaps.
3. If success is possible, select one or more candidates and emit a null abstention code.
4. Otherwise select the highest-priority primary code and preserve other failures as subordinate gaps.
5. For relation admission, compare planned baseline output to the one-edge/property mutant.
6. Retain only when the expected observable delta is discriminating; otherwise merge, defer, or kill.

## View 5 — Validation

- Query matrix: eight terminal paths and eight planned fixtures.
- Relation matrix: 25 unique IDs; expected counts 17/5/3/0.
- Static gates: no undeclared query code; no retained row without a finite consumer delta; no non-retained row represented as admitted.
- Later dynamic gates: execute all fixtures and compare actual baseline/mutant outputs. These are explicitly outside this run.

## View 6 — Ownership and operations

- Refine owns this definition/design/plan evidence only.
- A later confirmed task owner may materialize candidate validators and fixtures.
- Ontology Vault remains the appropriate later owner for selecting/admitting the repaired ontology contract.
- Publication or promotion requires separate owner receipts and is not implied by candidate validation.

## Decisions and risks

- Decision: vocabulary minimization beats adding an ambiguous-choice synonym.
- Decision: only 17 relations proceed as retained candidates.
- Risk: merge decisions may alter downstream serialization shape; preserve a migration note.
- Risk: planned deltas may fail at runtime; route failures back to design rather than weakening assertions.
- Risk: adding ontology bytes before fixture execution would inflate evidence; prohibit that sequence.
