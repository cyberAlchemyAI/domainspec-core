# TASK-COOP-L0-CONTRACT

## Objective

Implement `SWU-COOP-001`: one deterministic decision that either admits a
candidate `ProjectRecord` under the current Co-Op policy or returns stable
typed diagnostics.

## Mapping

- Layer: L0
- Slice: `S-L0-ADMISSION`
- Wave: W1
- Dependency: validated W0 strict packs
- Blockers: none

## Source Contracts

- [Shared execution context](../shared/context.md)
- [Approved specification](../../SPEC.md)
- [Architecture bundle](../../ARCHITECTURE-BUNDLE.md)
- [Implementation layering](../../IMPLEMENTATION-LAYERING.md)
- [SWU manifest](../../SWU-MANIFEST.json)
- [Closeout contract](../../CLOSEOUT-SYNC-CONTRACT.json)

## Smallest Working Unit: SWU-COOP-001

### Primary behavior

Decide whether one candidate project record is admitted under the approved
policy.

### Independent acceptance boundary

At fixed `asOf=2026-07-26T00:00:00Z`, the normalized Poker record returns
`admitted: true`. Four independently mutated candidates return
`admitted: false` and contain the exact intended diagnostic without changing
the input.

### Split analysis

Candidate children:

- structural required-field validation;
- policy/freshness validation;
- visibility-class validation.

Retain one unit because partial success cannot produce a safe admitted record.
The single externally meaningful decision is admission. Collaboration
transitions, browser projections, and observable-surface leakage are excluded
because they do have independent acceptance boundaries.

### Write scope

- `projects/co-op-engine/package.json`
- `projects/co-op-engine/src/contracts/project-record.ts`
- `projects/co-op-engine/test/fixtures/poker-record.ts`
- `projects/co-op-engine/test/project-record.test.ts`

No other file may be created or changed.

### Data model

Use erasable TypeScript only.

```text
VisibilityClass =
  public | meeting_visible | assigned_collaborator |
  participant_private | owner_private

ProjectRecord =
  schemaVersion
  policyVersion
  project { id, displayName, domain, owner, verifiedAt, expiresAt }
  truth { problem, currentWitness, limitation, claimCeiling,
          sourceRefs[], forbiddenClaims[] }
  experiment { uncertainty, contributionOptions[], skillAsk,
               recruitmentAsk, effortCeiling, stopRule, expectedWitness,
               ownerResponseSlaHours, checkIn }
  eligibility
  fieldVisibility { requiredFieldPath -> VisibilityClass }

AdmissionResult =
  { admitted: true, record }
  | { admitted: false, diagnostics[] }
```

Diagnostics contain `code`, `path`, and `message`. Expected validation failures
are values, not thrown exceptions.

### Algorithm

```text
admitProjectRecord(candidate, asOf):
  diagnostics = []
  validate schemaVersion and policyVersion
  for each required string:
    add REQUIRED_FIELD when blank or absent
  require at least one sourceRef, forbiddenClaim, and contributionOption
  require ownerResponseSlaHours == 72
  parse verifiedAt and expiresAt as valid instants
  require expiresAt - verifiedAt == 30 calendar days
  require asOf <= expiresAt
  require candidate eligibility == eligible
  for each required field path:
    require an entry in fieldVisibility
    require its value is one of the five visibility classes
  sort diagnostics by code, then path
  if diagnostics non-empty:
    return rejected result
  return admitted result carrying an immutable copy or readonly record
```

The function must not read the wall clock, filesystem, network, environment,
or browser state.

### Fixture contract

Positive fixture:

- project `poker-agent-arena`;
- claim ceiling “runnable Kuhn-poker bot harness”;
- bounded two-seat contribution and hidden-state stop rule;
- verification `2026-07-02T00:00:00Z`;
- expiry `2026-08-01T00:00:00Z`;
- 72-hour SLA;
- all required paths classified.

Negative mutations:

1. set SLA to the research-era 48 hours → `SLA_POLICY_MISMATCH`;
2. set `asOf` after expiry → `STALE_RECORD`;
3. blank `truth.currentWitness` → `REQUIRED_FIELD`;
4. delete one required visibility path → `UNCLASSIFIED_FIELD`;
5. set a required path to an unknown class through an untyped copy →
   `UNKNOWN_VISIBILITY_CLASS`.

Each test asserts the intended code/path and that the original positive fixture
still returns a byte-equivalent result after the mutation test.

### Package contract

`package.json` is private, ESM, dependency-free, and provides:

```json
{
  "scripts": {
    "test:contract": "node --experimental-strip-types --test test/project-record.test.ts"
  }
}
```

No install step is required.

### Done criteria

- exact write scope only;
- positive and five negative cases pass;
- diagnostic ordering is deterministic;
- input fixture remains unchanged;
- no dependency or lockfile is introduced;
- scoped whitespace check passes.

### Validation

```bash
npm --prefix projects/co-op-engine run test:contract
git diff --check -- projects/co-op-engine
```

### Execution owner and result

- Recommendation: `local-fallback`
- Capability: native goal/Task Session
- Expected result shape: exact shape in `SWU-MANIFEST.json`
- Stop on: missing strict source, unsupported Node behavior, write-scope
  conflict, contradictory policy, or failure that cannot be tied to one seeded
  violation.

## Synchronization

On terminal execution, emit the source receipt, validate the exact closeout
contract, apply only declared status/evidence deltas through
`invoke:refresh:apply-approved`, emit the closeout receipt, and stop. L1 is not
an automatic successor.
