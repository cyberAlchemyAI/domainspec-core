# TASK-BWOI-ONTOLOGY

## Objective

Implement T-ONTOLOGY-001: validate the local Body War ontology meaning of CT-2
without loading DomainSpec or application code.

## Mapping

- Layer: L0
- Slice: S-001
- Wave: W0
- SWU: SWU-BWOI-001
- Dependency: none

## Source Contracts

- [SPEC test contract](../../SPEC.md#t-ontology-001)
- Body War `operations.md`, `CreateSuggestedTrack` CT-2 through CT-4
- Body War `states.md`, `none -> needs_evidence`
- CyberAlchemy `ontology/README.md`, candidate-entry rule

## SWU-BWOI-001

### Primary behavior

Accept one coherent CT-2 ontology entry set and reject an illegal direct
`needs_evidence -> source_backed` transition.

### Inputs

- entry schema;
- `SuggestedTrack`, `CreateSuggestedTrack`, and `needs_evidence` entries;
- legal transition fixture;
- invalid-transition fixture.

### Outputs

- deterministic ontology validation receipt;
- typed diagnostics for invalid entry, missing edge, illegal transition, and
  missing governance metadata.

### Algorithm

```text
load entry set
validate closed schema
index entries by stable id; reject duplicates
require evidence, confidence, status, next gate and contradiction path
resolve every edge endpoint
require CreateSuggestedTrack -> produces -> SuggestedTrack
require CreateSuggestedTrack -> establishes -> needs_evidence
validate declared transitions against the allowed set
canonicalize entries and compute per-entry and set digests
emit status=pass with authority_effect=none
run invalid-transition fixture and require ONTOLOGY_TRANSITION_FORBIDDEN
```

### Edge cases and failure modes

- duplicate ID;
- missing referenced entry;
- candidate status hidden or omitted;
- an entry containing `body.logic` or executable DS-SFOL AST;
- direct transition to `source_backed`;
- nondeterministic array or map ordering.

### Split analysis

Schema, entries, and tests are plausible child edits, but none yields an
independently meaningful semantic verdict. The retained unit is one ontology
admission behavior with positive and negative polarity.

### Write scope

- `projects/body-war/proofs/suggested-track-ontology-domainspec/ontology/`
- `projects/body-war/proofs/suggested-track-ontology-domainspec/src/ontology-validator.ts`
- `projects/body-war/proofs/suggested-track-ontology-domainspec/tests/ontology.test.ts`
- `projects/body-war/proofs/suggested-track-ontology-domainspec/receipts/ontology-receipt.json`

Forbidden:

- `cyberAlchemy/ontology/`
- `projects/domainspec-v2/`
- Body War app runtime sources
- ontology promotion fields outside the local fixture

### Done criteria

- positive entry set passes;
- illegal transition rejects with the exact diagnostic;
- receipt is byte-identical across two runs;
- receipt says candidate-local, `authority_effect: none`, and no release claim.

### Validation

```bash
(cd projects/domainspec-v2/impl && node --import tsx --test \
  ../../body-war/proofs/suggested-track-ontology-domainspec/tests/ontology.test.ts)
git diff --check -- projects/body-war
```

### Acceptance evidence

- `receipts/ontology-receipt.json`;
- Task Session result at the exact closeout path in `WORK-PACK.md`;
- passing command output.

### Execution owner

`local-fallback`. No subagent dispatch is required; the write scope is one
consumer-local proof package.

### Handoff note

At execution time, Context Builder must include this task, SPEC T-ONTOLOGY-001,
the Body War CT-2 sources, CyberAlchemy candidate-entry rules, and the exact
write/forbidden scopes.

## Synchronization

Invoke Refresh may update only the task/work-pack evidence and BWOI-scoped
Craft route state after the terminal receipt passes. The unique successor is
SWU-BWOI-002.

## Execution Evidence

- Status: completed
- Task Session:
  `projects/body-war/development/task-sessions/SWU-BWOI-001/TASK-SESSION-RESULT.md`
- Ontology receipt:
  `projects/body-war/proofs/suggested-track-ontology-domainspec/receipts/ontology-receipt.json`
- Validation: ontology tests 4/4 twice; Body War application tests 3/3;
  deterministic receipt SHA-256
  `071e397041e3dfe9c0777c92dff20fa92ea63af61990b51ec1b13d2bf878dc88`;
  scoped diff check pass.
- Claim ceiling: candidate-local experimental ontology witness;
  `authority_effect: none`; release admission not granted.
- Next route: Task Session to `SWU-BWOI-002`; not executed by this closeout.
