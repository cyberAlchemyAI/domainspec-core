# TASK-BWOI-VERIFY

## Objective

Reproduce and audit the ontology, DomainSpec, and integration witnesses without
changing their source contracts.

## Mapping

- Layer: L3
- Slice: S-004
- Wave: W3
- Dependencies: all three SWU receipts
- SWU exemption: permitted closure-only `VERIFY` task

## Checks

1. Run the full proof suite twice from unchanged bytes.
2. Require identical ontology, DomainSpec, bridge and integration receipt
   digests.
3. Search fixtures for expected-value or verdict oracles.
4. Confirm integration case IDs equal the standalone DomainSpec case IDs.
5. Confirm `authority_effect: none` and
   `release_admission: not-granted` in every terminal receipt.
6. Confirm this task introduces no changes under `cyberAlchemy/ontology` or
   `projects/domainspec-v2` relative to its captured preflight baseline.
7. Run the existing Body War app tests and scoped diff check.
8. Prepare Refresh synchronization for Work Pack and Body War Craft links;
   do not apply promotion, release, deployment, or unrelated project state.

## Write Scope

Task Session may create or update only:

- `projects/body-war/development/task-sessions/TASK-BWOI-VERIFY/VERIFICATION-REPORT.md`;
- `projects/body-war/development/task-sessions/TASK-BWOI-VERIFY/RECEIPT-DIGESTS.json`;
- `projects/body-war/development/task-sessions/TASK-BWOI-VERIFY/RESIDUE.md`;
- `projects/body-war/development/task-sessions/TASK-BWOI-VERIFY/TASK-SESSION-RESULT.md`.

Read-only:

- `projects/body-war/proofs/suggested-track-ontology-domainspec/`;
- `cyberAlchemy/ontology/`;
- `projects/domainspec-v2/`;
- the work pack, task contracts, prior Task Session results, and prior owner
  receipts.

Forbidden:

- changing proof sources, fixtures, standalone or integration receipts;
- changing ontology or DomainSpec sources;
- changing application behavior;
- changing Work Pack, Craft, or continuity state from inside Task Session;
- promotion, release, deployment, or wider SuggestedTrack claims.

## Done Criteria

- both full-suite runs pass from unchanged source bytes;
- the two receipt-digest tables are byte-identical;
- all eight checks above pass;
- every terminal receipt retains the experimental authority and release
  ceilings;
- the Task Session result names files, commands, verdict, blockers, and
  residue;
- no write occurs outside the four declared Task Session paths;
- any failure produces a blocker and residue instead of partial closeout.

## Validation

```bash
(cd projects/domainspec-v2/impl && node --import tsx --test \
  ../../body-war/proofs/suggested-track-ontology-domainspec/tests/*.test.ts)
npm --prefix projects/body-war/app test
git diff --check -- projects/body-war
```

The full proof-suite command runs twice. The verification report records both
run identities, source baselines, receipt digests, and the equality verdict.

## Closeout Contract

- Lifecycle owner route: `invoke:refresh:apply-approved`.
- Terminal source receipt:
  `projects/body-war/development/task-sessions/TASK-BWOI-VERIFY/TASK-SESSION-RESULT.md`.
- Exact synchronization targets:
  - `projects/body-war/development/invoke-runs/20260727T172835Z-suggested-track-ontology-domainspec-integration/WORK-PACK.md`;
  - `projects/body-war/development/invoke-runs/20260727T172835Z-suggested-track-ontology-domainspec-integration/work-pack/tasks/TASK-BWOI-VERIFY.md`;
  - `projects/body-war/.craft/ledger.yml`;
  - `projects/body-war/CRAFT.md`.
- Baseline: digest every synchronization target at Task Session preflight and
  reject post-start drift.
- Allowed closeout deltas: `evidence-added`, `status-changed`, BWOI blocker
  opened/resolved, and `route-changed`.
- Owner validation: full proof suite twice with identical receipt digests;
  Body War app tests; scoped diff check; Craft ledger/index/view checks.
- Expected owner receipt:
  `projects/body-war/development/task-sessions/TASK-BWOI-VERIFY/closeout/INVOKE-REFRESH-RECEIPT.md`.
- Successor: none. A pass closes the current experiment.

The terminal Task Session result and expected Invoke owner receipt are
different artifacts and must not alias or replace one another.

## Completion Evidence

- `projects/body-war/development/task-sessions/TASK-BWOI-VERIFY/VERIFICATION-REPORT.md`;
- `projects/body-war/development/task-sessions/TASK-BWOI-VERIFY/RECEIPT-DIGESTS.json`;
- `projects/body-war/development/task-sessions/TASK-BWOI-VERIFY/RESIDUE.md`;
- `projects/body-war/development/task-sessions/TASK-BWOI-VERIFY/TASK-SESSION-RESULT.md`;
- the distinct Invoke Refresh receipt declared above.

## Execution Owner

`local-fallback`. Task Session executes verification; Invoke owns planning and
Craft synchronization; ontology, DomainSpec, promotion, and release owners
retain their existing authority.

## Terminal Route

No successor is authorized. After a passing closeout, any promotion, release,
deployment, or wider SuggestedTrack formalization requires a new bounded plan.

## Exit Claim

Only the experimental CT-2 integration claim in `SPEC.md` may pass. Any wider
claim is a verification failure.

