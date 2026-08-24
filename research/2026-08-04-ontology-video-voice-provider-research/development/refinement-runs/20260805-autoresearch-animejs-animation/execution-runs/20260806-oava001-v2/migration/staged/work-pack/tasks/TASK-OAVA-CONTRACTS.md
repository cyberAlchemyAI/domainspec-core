# TASK-OAVA-CONTRACTS — Source and Candidate Trust

## Task objective

Provide a deterministic, dependency-free boundary that proves an animation-hypothesis candidate is structurally closed, bound to the exact Sequence 6 source snapshot, below the current proof ceiling, contradiction-aware, and semantically equivalent in standard and reduced-motion terminal states.

Layer: L0. Slice: OAVA contract foundation. Current captured SWU: `SWU-OAVA-001` only.

## Source contracts

- `contracts/animation-hypothesis-candidate.schema.json` — candidate schema source.
- `stages/06-design.md` — S6 selection, semantic invariants, proof states, and source zero-delta rule.
- `VALIDATION-CONTRACTS.md` — standard/reduced terminal equivalence and causal mutant obligations.
- `2026-08-03-ontology-authority-agent-context-presentation/educational-video-production-script.md` — Sequence 6 `04:29–04:39`, “Rule — enforces → Operation”.
- `2026-08-03-ontology-authority-agent-context-presentation/educational-video-captions.vtt` — immutable caption source.
- `2026-08-03-ontology-authority-agent-context-presentation/images/03-arrow-is-a-contract.png` — immutable image reference.

## SWU-OAVA-001

### Primary behavior and acceptance boundary

Implement the staged candidate schema, frozen source snapshot, validator, one valid candidate, and five one-cause mutants. This is one atomic behavior because every output participates in the same pure validation decision and one test command proves the whole contract. Splitting schema, source identity, or semantic checks would create intermediate states that could accept inflated or stale candidates; runtime, consultation, browser, review, and episode work are independently testable and remain outside this SWU.

### Dependencies and blockers

No runtime dependency. B-001, B-002, and B-003 do not block this contract-only SWU. The exact current source bytes and the plan-once admission chain are mandatory inputs.

### Inputs

- Exact source paths, SHA-256 digests, sizes, and aggregate snapshot digest from `work-pack/execution-contract.json#/source_snapshot`.
- Closed schema source at `contracts/animation-hypothesis-candidate.schema.json`.
- Current evidence ceiling `planned_motion`.
- Execution binding, selection receipt, material package/receipt, strict context pack, mutation admission, and closeout-preflight receipt for the same attempt.

### Exact material writes

The ten paths in `work-pack/execution-contract.json#/execution_binding/material_writes`; no directory glob is authorized.

### Algorithm and failure precedence

1. Load JSON and validate the supported Draft 2020-12 schema keywords recursively: `type`, `required`, `properties`, `additionalProperties`, `const`, `enum`, `pattern`, `minLength`, numeric bounds, item/property minima, and array items.
2. Return the first deterministic schema error as `SCHEMA_INVALID` with its JSON path; unknown fields are therefore rejected before semantic checks.
3. Canonicalize and hash the source snapshot, compare it with the candidate aggregate and per-artifact bindings, then hash the live source files. Any mismatch returns exactly `SOURCE_DRIFT`.
4. Reject any proof state above `planned_motion` as exactly `PROOF_INFLATION`.
5. Require the contradiction object and its falsifier/reproposal fields through the schema; absence returns exactly `SCHEMA_INVALID` at `$.contradiction`.
6. Compare the final standard semantic state with the final reduced-motion state. A mismatch returns exactly `REDUCED_MOTION_MISMATCH`.
7. Otherwise return `VALID` without implying execution, visual quality, runtime conformance, or owner approval.

### Edge cases and causal fixtures

- Source drift mutates only one digest and expects `SOURCE_DRIFT`.
- Unknown field adds only one closed-schema property and expects `SCHEMA_INVALID`.
- Proof inflation changes only one proof state to `executed_witness` and expects `PROOF_INFLATION`.
- Missing contradiction deletes only `contradiction` and expects `SCHEMA_INVALID`.
- Reduced-motion mismatch changes only the final reduced state and expects `REDUCED_MOTION_MISMATCH`.
- File read, parse, or schema-load failures return a stable non-success result and never fall through to `VALID`.

### Expected result shape

```json
{
  "valid": true,
  "code": "VALID",
  "path": "$",
  "message": "candidate satisfies the OAVA-001 contract"
}
```

Negative results set `valid` to `false`, use one stable code, identify one JSON path, and provide a bounded message.

### Validation and acceptance evidence

Run from the refinement-run root:

```text
node --test prototype/test/candidate.test.mjs
```

Acceptance requires one positive pass, five exact negative-code passes, no network or external process dependency, staged/applied byte equality, and zero byte delta in the three source artifacts plus the AutoAds and canonical Anime.js vault boundaries.

### Execution owner and handoff

Task Session owns the single-use governed executor. `invoke:refresh:apply-approved` owns closeout synchronization. The terminal handoff may name `SWU-OAVA-002` but must set `successor_executed=false`.

## Later portfolio task

`SWU-OAVA-002` remains defined by the existing portfolio plan but is not a member of this Work Pack and is not authorized by this task session.
