# TASK-BWOI-DOMAINSPEC

## Objective

Implement T-DOMAINSPEC-001: derive CT-2 from canonical Body War
`body.logic`, execute the current memory repository, and detect a mutated
backend observation without loading ontology.

## Mapping

- Layer: L1
- Slice: S-002
- Wave: W1
- SWU: SWU-BWOI-002
- Ordering dependency: SWU-BWOI-001 closeout
- Semantic dependency on ontology: none

## Source Contracts

- [SPEC test contract](../../SPEC.md#t-domainspec-001)
- [Architecture low-level view](../../ARCHITECTURE.md#3-low-level-component-view)
- `projects/domainspec-v2/impl/tools/tests/sfol-profile-engine.test.ts`
- `projects/domainspec-v2/impl/test-derivation-engine/src/sfol/`
- `projects/body-war/app/src/auth/memory-repository.ts#createMemoryBodyWarAuthRepository`

## SWU-BWOI-002

### Primary behavior

Prove that the canonical CT-2 function produces the same normalized creation
result as the current Body War memory repository and that a backend mutation
is detected.

### Inputs

- Body War minted project with Rule, Operation, and Event nodes;
- Operation `body.logic` function clause `body-war.CT-2`;
- input-only creation fixture: name, place, city, optional distance and note;
- pure-function binding to a consumer-local adapter.

### Outputs

- deterministic graph, source manifest, build receipt and logic projection;
- generated CT-2 case;
- normalized backend observation;
- standalone DomainSpec proof receipt.

### Algorithm

```text
load the current DomainSpec development profile by exact digest
compile the Body War minted project twice
require byte-identical graph, source manifest and build receipt
project only body-war.CreateSuggestedTrack body.logic
decode and typecheck the projected module
select clause body-war.CT-2; reject any expected value in the fixture
derive the expected return record from the function clause
create an in-memory Body War repository
invoke createSuggestedTrack with generated input
normalize random id/timestamps out of the observation
compare status, geometryAuthority and prohibited stronger claims
emit a receipt bound to node/module/clause and adapter-source digests
rerun through a mutated adapter observation and require proof failure
```

The CT-2 clause is a DS-SFOL `function` returning a named record. This is a
bounded functional specification inside an Operation node; it does not claim
the entire stateful creation workflow is formalized.

### Edge cases and failure modes

- unsupported profile or stale profile/schema digest;
- `body.logic` on an unsupported kind;
- source identity not matching the containing node;
- fixture containing expected output;
- missing required creation input;
- random IDs/timestamps leaking into deterministic receipt material;
- backend returning `source_backed`, `pilot_ready`, or a different status;
- accidental import of ontology or bridge data.

### Split analysis

Canonical build and adapter comparison can be unit-tested separately, but
neither independently proves CT-2 behavior. The retained boundary owns one
source-derived expectation versus observed-backend decision.

### Write scope

- `projects/body-war/proofs/suggested-track-ontology-domainspec/domainspec/`
- `projects/body-war/proofs/suggested-track-ontology-domainspec/src/domainspec-ct2-runner.ts`
- `projects/body-war/proofs/suggested-track-ontology-domainspec/tests/domainspec.test.ts`
- `projects/body-war/proofs/suggested-track-ontology-domainspec/receipts/domainspec-receipt.json`

Read-only dependencies:

- `projects/domainspec-v2/impl/`
- `projects/body-war/app/src/auth/`

Forbidden:

- copying `run-financial-settlement-sfol.ts`;
- modifying DomainSpec v2 or Body War app source;
- reading ontology or bridge inputs.

### Done criteria

- build/projection/decode/case/evaluate/observe stages use the same case set;
- positive CT-2 proof passes;
- mutated backend observation fails;
- no expected-value oracle exists in fixtures;
- receipt is stable across two unchanged runs.

### Validation

```bash
(cd projects/domainspec-v2/impl && node --import tsx --test \
  ../../body-war/proofs/suggested-track-ontology-domainspec/tests/domainspec.test.ts)
npm --prefix projects/body-war/app test
git diff --check -- projects/body-war
```

### Acceptance evidence

- `receipts/domainspec-receipt.json`;
- mutation detection recorded in the test result;
- exact node, module, clause, profile and adapter-source digests.

### Execution owner

`local-fallback`. Escalate to the DomainSpec engine owner only if the generic
compiler, projection, case, evaluator, or proof APIs are not consumer-usable.

### Handoff note

Context Builder must include this task, the current profile/schema, the generic
SFOL profile test, CT-2 sources, and the memory repository symbol. Financial
Settlement runner business code is excluded.

## Synchronization

Refresh recorded the standalone proof without changing the preceding receipt.
SWU-BWOI-002 is complete. The unique selected successor is SWU-BWOI-003; it
was not executed by this Task Session.

## Execution Evidence

- Status: completed
- Task Session:
  `projects/body-war/development/task-sessions/SWU-BWOI-002/TASK-SESSION-RESULT.md`
- Standalone receipt:
  `projects/body-war/proofs/suggested-track-ontology-domainspec/receipts/domainspec-receipt.json`
- Receipt SHA-256:
  `d1484bb6d8ee6a637e3eba4ee4b38336582b36fbf9ef901d087946415f46f756`
- Validation: DomainSpec 3/3 twice, byte-stable receipt, Body War app 3/3,
  scoped diff check pass
- Claim ceiling: one experimental CT-2 seam; authority effect none; release
  admission not granted
