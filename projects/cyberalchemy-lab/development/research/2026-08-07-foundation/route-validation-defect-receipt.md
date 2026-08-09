# Dispatch Route Validation Defect Receipt

- Classification: governance-only Dispatch Spec projection defect
- Status: repaired candidate validates `pass`
- Dispatch ID: `2026-08-07-cyberalchemy-lab-foundation`
- Authority ceiling: no registration, execution, promotion, implementation, publication, or deployment
- Accepted dispatch sheet: SHA-256 `943728666e768d5fee502e8eec00ad35368443bb0d91bc9d03dd39593b4fda64`
- Accepted material strategy: SHA-256 `39ee52dd90d9f10d035690009c0136068532cbffbce7c2420c6d268b2cfcb836`
- Confirmation receipt: `user-confirmation-943728666e76-20260807T232938Z`

## Root cause

The route projection used intent-level labels and receipt fields where the Dispatch Spec validator requires canonical schema vocabulary. It also conflated the writer's product artifact with the capability-bound role's receipt-only `output_refs`. The affected projection was not schema-valid; the confirmed research strategy and domain behavior were not disputed.

## Affected invariant

A confirmed strategy may cross into registration or execution only through a Dispatch Spec projection that validates `pass`, uses schema-owned evidence and gate fields, declares the complete native receipt contract, and limits capability-bound role `output_refs` to receipt outputs. The original projection remains unchanged and must not be registered or executed.

## Minimal repair and exact changed-field inventory

Created `DISPATCH-ROUTE.repaired.json` from the original projection with only these semantic field changes:

- `/boundary_evidence/boundaries/3/kind`: `authority_split` -> `capability_handoff`; owners, applied steps, contract, and `on_violation` are unchanged.
- `/boundary_evidence/receipts/0..4/required_fields`: removed unsupported `wave_id`, `role`, and `agent_id`; all supported fields, producers, stores, and missing-receipt actions are unchanged.
- `/gates/0/kind`: `human` -> `human_approval`; the confirmation condition and owner are unchanged.
- `/steps/6/expected_evidence`: renamed to `/steps/6/evidence_artifact`; value remains `orchestrate/run-001/evidence/witness-mutants.json`.
- `/steps/9/expected_evidence`: renamed to `/steps/9/evidence_artifact`; value remains `orchestrate/run-001/receipts/wave-05-auditor/findings-auditor.json`.
- `/subagent_strategy/receipt_requirements`: added `observer_status` and `handoff_note`.
- `/subagent_strategy/roles/7/output_refs`: removed `projects/cyberalchemy-lab/development/research/2026-08-07-foundation/findings.md`; the artifact remains the `s9` artifact output, writer `write_scope` and capability target, and `s10` artifact input. The writer receipt remains the role output and the only receipt required by `g-findings`.

Changed-byte inventory:

- Created `DISPATCH-ROUTE.repaired.json`: 31,938 bytes; SHA-256 `22d602fc1aea43dda93161fe9a5fe8388ab1e459ff66ab0bc7d7dde77dccf3d7`.
- Created this receipt.
- `DISPATCH-ROUTE.json` was not altered: 32,128 bytes; SHA-256 `6d665c0575df76db54514e0f051b5ac649b85fb2391480924f1e4247d5635cef`.
- No accepted sheet, material-strategy projection, confirmation, ledger, telemetry, Inventory, Arcanum, product, IDE, ontology, research output, or Git state was changed.

## Revalidation

Required command against the actual repaired bytes:

```text
python3 .agents/skills/dispatch-spec/scripts/validate-dispatch.py projects/cyberalchemy-lab/development/research/2026-08-07-foundation/DISPATCH-ROUTE.repaired.json --json
```

Observed result: process exit `0`; `validation: pass`; `blocks: []`; `flags: []`.

Before any registration or execution edge, the parent must inspect this receipt, recheck the repaired candidate digest, rerun the validator against that exact candidate, and bind any downstream route record to the repaired digest rather than the invalid original.

## Owner acceptance

Renewed confirmation of the material strategy is not required: the confirmation remains bound to the unchanged accepted dispatch-sheet and material-strategy digests. The repaired route is nevertheless a new projection candidate and requires explicit parent adoption after receipt inspection; the older confirmation must not be represented as exact-byte acceptance of this repaired file.

## Permanent regression check proposal

Add a Dispatch Spec projection fixture and validator-suite assertion that exercises this route shape before confirmation or registration. The fixture should fail on `authority_split`, `human`, `expected_evidence`, unsupported boundary-receipt fields, missing `observer_status` or `handoff_note`, and artifact paths in capability-bound role `output_refs`; its canonical form should pass only with supported enums, `evidence_artifact`, complete native receipt requirements, and receipt-only role outputs. The workflow must validate the actual staged or newly created route bytes and preserve the validator's nonzero exit status so later cleanup cannot mask a projection failure.
