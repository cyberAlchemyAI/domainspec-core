# Invoke Refresh Report — SWU-BWAA-001 Material Admission

## Outcome

- Phase status: `pass`
- Activation source: `direct-user`
- Mutation mode: `apply-approved`
- Handoff status: `ready`
- Task Session admission probe: `admit`
- Mutation ready: `true`
- Live product mutation: not started

The missing producer-material blocker is resolved for the exact current
`SWU-BWAA-001` controls. Invoke authored three staged post-images, a
schema-valid package and producer receipt, a ready Refresh handoff, a strict
Context Builder pack, and the closeout-owner contract. The canonical Task
Session 1.2 verifier admits the resulting request with no reasons.

## Staged material

The staged projection now:

- derives 13 directed lens-flow groups in catalog lens order;
- assigns all 109 portal relation IDs exactly once;
- preserves reciprocal directions as separate groups;
- binds each ID to the canonical portal set;
- rejects unknown lenses/relations, same-lens portals, duplicates, count
  drift, and partition drift;
- exposes immutable flow rows with exact relation counts.

The staged validator records the exact 13-row summary and verifies the full
109-ID set. The staged test suite has 8 passing tests, including the flow
contract and fail-closed cases.

## Material evidence

- Package ID:
  `body-war-bwaa-swu-001-material-admission-20260730T090724Z`
- Canonical package digest:
  `905e2b76c704f0ed114b5601ae230e7fc8f3e812c68851bcd8b8164313e49e13`
- Package file: `material/MATERIAL-PACKAGE.json`
- Producer receipt: `material/MATERIAL-RECEIPT.json`
- Refresh handoff: `material/REFRESH-HANDOFF-RESULT.json`
- Task Session probe: `TASK-SESSION-ADMISSION-PROBE-RECEIPT.json`
- Task Session handoff: `TASK-SESSION-HANDOFF.json`
- Closeout contract: `CLOSEOUT-OWNER-CONTRACT.json`

Package verdict, dependency, owner, publication, schema, path, validation, and
handoff checks all pass. Receipt reasons are empty.

## Boundaries

The live three target files retain their preflight hashes. Invoke did not:

- apply the staged implementation to the product tree;
- execute or complete SWU-BWAA-001;
- write the coverage or terminal closeout receipts;
- select SWU-BWAA-002;
- change ontology nodes, relations, lifecycle policy, authority, or release
  posture.

`authority_effect: none` and `release_admission: not-granted` remain fixed.

## Next route

Run one Task Session for `SWU-BWAA-001` using
`TASK-SESSION-HANDOFF.json`. Task Session must recheck current bytes, apply the
three staged outputs, run the exact validation commands, write the coverage
and terminal receipts, and stop without selecting the successor.
