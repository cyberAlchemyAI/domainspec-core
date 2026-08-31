# W0 Live-Byte Baseline Inventory

Date: 2026-08-26

Canonical repository: `arcanum`

Baseline HEAD: `b07a03d95e4c8bd4d98c05a8eb2916ad7f8341d9`

Tracked Invoke diff digest: `76cee727ebb25d249e88d8156ec346447923f6278f6595f519095348231a5793`

Isolated candidate: `/tmp/invoke-igd-candidate.sGNnyPrI/arcanum`

## Adopted tracked changes

The isolated candidate mechanically adopts, without claiming authorship, the exact
current tracked changes to:

- `README.md`
- `development/PLAN-ARTIFACT-BOUNDARIES.md`
- `development/preacceptance-closure/real_consumer_rehearsal.py`
- `development/preacceptance-closure/test_preacceptance_closure.py`
- `development/run-preacceptance-closure-fixtures.sh`
- `plan.md`
- `preacceptance-closure.md`
- `schemas/preacceptance-closure-manifest-v1.schema.json`
- `scripts/preacceptance_closure.py`

The live and isolated tracked diffs have the same digest above. These bytes are
treated as prerequisite work in progress and may be extended only in the isolated
candidate. They must not be overwritten in the live worktree.

## Adopted untracked prerequisites

- `PLAN-ARTIFACT-BOUNDARIES.md`
- `development/preacceptance-closure/test_execution_entry_negative_cases.py`
- `development/preacceptance-closure/test_live_entry_rehearsal_budget.py`
- `schemas/execution-entry-consumer-rehearsal-v1.schema.json`
- `schemas/owner-acceptance-response-v1.schema.json`
- `schemas/pre-execution-block-owner-receipt-v1.schema.json`
- `schemas/preacceptance-live-entry-rehearsal-budget-v1.schema.json`
- `schemas/request-emission-eligibility-receipt-v1.schema.json`
- `scripts/handle_pre_execution_block.py`
- `scripts/rehearse_execution_entry_consumers.py`
- `scripts/validate_owner_acceptance_response.py`

All were copied byte-for-byte into the isolated candidate before repair authoring.
They remain unattributed concurrent work; final candidate inventory and independent
review must enumerate their exact postimage hashes.

## Collision decision

Material v1 schemas are clean and stay unchanged. New material and preacceptance
contracts use parallel v2 schema files. Necessary runner, fixture, and documentation
changes extend the adopted dirty bytes only in isolation. No production Task Session
source is in repair write scope; downstream behavior is exercised from Invoke-owned
compatibility tests.

If any live source byte changes after this freeze, canonical application must stop
and rebase the reviewed candidate against a fresh baseline instead of overwriting it.
