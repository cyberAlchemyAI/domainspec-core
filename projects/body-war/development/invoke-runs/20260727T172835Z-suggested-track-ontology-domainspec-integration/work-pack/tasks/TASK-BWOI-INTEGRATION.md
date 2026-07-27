# TASK-BWOI-INTEGRATION

## Objective

Implement T-INTEGRATION-001: validate a sidecar bridge that binds exact local
ontology meaning to exact canonical DomainSpec CT-2 logic before reusing the
accepted behavior case.

## Mapping

- Layer: L2
- Slice: S-003
- Wave: W2
- SWU: SWU-BWOI-003
- Dependencies: SWU-BWOI-001 and SWU-BWOI-002 receipts

## Source Contracts

- [SPEC test contract](../../SPEC.md#t-integration-001)
- [Bridge model](../../ARCHITECTURE.md#bridge-manifest)
- ontology and DomainSpec receipt contracts from the two parent tasks

## SWU-BWOI-003

### Primary behavior

Admit integration only when every ontology, node, module, clause, build and
bridge digest is current and the observed ontology state satisfies the
experimental profile.

### Inputs

- ontology standalone receipt;
- DomainSpec standalone receipt;
- bridge manifest;
- experimental integration profile requiring `candidate`;
- negative bridge fixtures.

### Outputs

- bridge admission receipt;
- integrated CT-2 proof receipt;
- typed stale-digest and insufficient-state diagnostics.

### Algorithm

```text
load and schema-check both standalone receipts
recompute each receipt digest and reject stale inputs
load bridge and reject executable logic fields
resolve every ontology entry id against the ontology receipt
resolve node, module and clause ids against the DomainSpec receipt
recompute and compare every entry/node/module/clause/build digest
compare observed ontology state with required state under the named profile
if admitted, reuse the exact DomainSpec case and backend observation path
emit integration receipt linking both parent receipt digests and bridge digest
mutate one ontology digest; require BRIDGE_STALE_ONTOLOGY_DIGEST
require promoted while observing candidate; require BRIDGE_ONTOLOGY_STATE_INSUFFICIENT
```

State ordering is explicit:

```text
candidate < promoted
```

The validator reads this order from the integration profile. It never writes
the observed state.

### Edge cases and failure modes

- bridge copies a DS-SFOL expression;
- unknown ontology entry, node, module or clause;
- stale parent receipt;
- current parent receipt with stale nested digest;
- candidate accepted under a promoted-only profile;
- a bridge admits release or authority effect;
- integration reruns a different case set than the standalone DS receipt.

### Split analysis

Digest checks and state checks can have internal unit cases, but their
independent results do not authorize integration. The retained unit owns one
fail-closed composition admission and one linked receipt.

### Write scope

- `projects/body-war/proofs/suggested-track-ontology-domainspec/bridge/`
- `projects/body-war/proofs/suggested-track-ontology-domainspec/src/bridge-validator.ts`
- `projects/body-war/proofs/suggested-track-ontology-domainspec/src/integration-runner.ts`
- `projects/body-war/proofs/suggested-track-ontology-domainspec/tests/integration.test.ts`
- `projects/body-war/proofs/suggested-track-ontology-domainspec/receipts/integration-receipt.json`

Read-only:

- the two standalone proof packages and receipts;
- DomainSpec and Body War adapter sources already bound by the DomainSpec
  receipt.

Forbidden:

- `cyberAlchemy/ontology/`;
- `projects/domainspec-v2/`;
- changing ontology promotion state;
- adding executable CT-2 logic to the bridge.

### Done criteria

- exact bridge passes and reuses the same CT-2 case;
- stale digest rejects;
- promoted-required/candidate-observed rejects;
- executable duplication rejects;
- receipt links both parent receipts and preserves claim ceilings.

### Validation

```bash
(cd projects/domainspec-v2/impl && node --import tsx --test \
  ../../body-war/proofs/suggested-track-ontology-domainspec/tests/integration.test.ts)
(cd projects/domainspec-v2/impl && node --import tsx --test \
  ../../body-war/proofs/suggested-track-ontology-domainspec/tests/*.test.ts)
npm --prefix projects/body-war/app test
git diff --check -- projects/body-war
```

### Acceptance evidence

- `receipts/integration-receipt.json`;
- exact diagnostic assertions for both mandatory negative controls;
- parent-receipt and bridge digest chain.

### Execution owner

`local-fallback`. Route contract changes to the Body War integration owner;
route generic compiler limitations to the DomainSpec engine owner.

### Handoff note

Context Builder must select this task, both prior receipts, the bridge section
of Architecture, and the exact negative-control requirements. It must not load
the entire CyberAlchemy ontology corpus.

## Synchronization

Refresh can route only to TASK-BWOI-VERIFY after all three tests pass. It
cannot infer ontology promotion or release from the integration receipt.

## Execution Evidence

- Status: completed
- Task Session result:
  `projects/body-war/development/task-sessions/SWU-BWOI-003/TASK-SESSION-RESULT.md`
- Integration receipt:
  `projects/body-war/proofs/suggested-track-ontology-domainspec/receipts/integration-receipt.json`
- Bridge admission receipt:
  `projects/body-war/proofs/suggested-track-ontology-domainspec/bridge/receipts/bridge-admission-receipt.json`
- Validation: integration 4/4, full proof suite 11/11, Body War application
  3/3, and scoped diff check pass.
- Negative controls: stale ontology digest, insufficient ontology state, and
  executable bridge logic all reject with typed diagnostics.
- Claim ceiling: authority effect none; release admission not granted.

## Closeout

Invoke Refresh synchronized the W2 execution evidence. The unique next route
is `task-session:execute TASK-BWOI-VERIFY`; this closeout did not execute it,
promote ontology, release DomainSpec, publish, or deploy.
