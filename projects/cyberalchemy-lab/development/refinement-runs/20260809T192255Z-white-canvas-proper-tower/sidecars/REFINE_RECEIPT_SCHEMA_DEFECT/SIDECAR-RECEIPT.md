# Refine Receipt Schema Defect Sidecar Receipt

- Sidecar: `REFINE_RECEIPT_SCHEMA_DEFECT`
- Classification: governance-only
- Live target: `projects/cyberalchemy-lab/development/refinement-runs/20260809T192255Z-white-canvas-proper-tower/REFINE-DISPATCH.json`
- Live mutation: none
- Product or design decision: none
- Authority effect: none
- Candidate: `CANDIDATE.patch`

## Failing command and preserved evidence

```sh
python3 arcanum/formulae/dispatch-spec/scripts/validate-dispatch.py \
  projects/cyberalchemy-lab/development/refinement-runs/20260809T192255Z-white-canvas-proper-tower/REFINE-DISPATCH.json
```

Observed result: `VALIDATION=block`, exit `1`, with 62 blocker records:

| Blocker class | Count | Exact defect |
|---|---:|---|
| Native receipt schema | 20 | Each of 10 receipts lacks `capability_ref` and `receipt_kind`. |
| Lifecycle enum schema | 4 | Both agents use `pass` for `spawn_status` and `join_status`; the schema requires `spawned` and terminal `completed`. |
| Capability-bound lifecycle bindings | 10 | Each agent lacks `capability_ref`, `capability_target`, `capability_mode`, `wave_id`, and `write_scope`. |
| Successful lifecycle assertions | 4 | Each agent consequently fails the successful-spawn and completed-join assertions. |
| Role cardinality | 2 | Each role resolves to zero conforming closed agent records instead of one. |
| Role output binding | 2 | The `s03-review` receipt does not include either declared reviewer output. |
| Native receipt semantic checks | 20 | Each receipt has no matching capability and uses singular `artifact`, so no accepted `artifacts` or `validation` evidence is present. |

## Root cause

Closeout data was projected through a summary shape instead of the Dispatch Spec closeout contract. An action result value (`pass`) was reused where lifecycle transition enums were required, the role binding fields were dropped, and native receipts used a singular `artifact` convenience field rather than the schema's `artifacts` evidence list. The lifecycle's generic `receipt` path also pointed to the Orchestrate machine receipt, while the validator requires `receipt_artifact` to equal the role's declared semantic output reference.

This is confined to receipt normalization. The accepted white-tower design, reviewer findings, role assignments, execution history, and product boundary are unchanged.

## Affected invariant

A capability-bound dispatch may close with `subagent_lifecycle.status=pass` only when:

1. every declared role has exactly its configured number of `spawned` / `completed` / closed agents;
2. every agent record repeats the role's capability, target, mode, wave, and exact write scope;
3. `receipt_artifact` binds a declared role output;
4. every native stage receipt identifies its step capability and receipt kind and carries artifacts or validation; and
5. the passing receipt for a delegated step contains every declared role output.

## Minimal exact repair

`CANDIDATE.patch` makes only the following contract repairs:

- adds `receipt_kind` to the strategy's receipt requirements;
- replaces lifecycle `pass` values with `spawned` and `completed`;
- adds the five missing capability-bound fields to both lifecycle records;
- binds each `receipt_artifact` to its declared reviewer output while preserving the normalized Orchestrate receipt as `runtime_receipt_artifact`;
- replaces each singular `artifact` with `artifacts`, adds the step-matching `capability_ref`, and adds an allowed `receipt_kind`; and
- includes both reviewer outputs in the `s03-review` receipt.

No status, design conclusion, reviewer finding, product scope, authority statement, or execution result is changed.

## Isolated validation

Patch applicability:

```sh
git apply --check \
  projects/cyberalchemy-lab/development/refinement-runs/20260809T192255Z-white-canvas-proper-tower/sidecars/REFINE_RECEIPT_SCHEMA_DEFECT/CANDIDATE.patch
```

Observed: exit `0`.

Validator against an in-memory patched copy, without mutating the live target:

```sh
python3 arcanum/formulae/dispatch-spec/scripts/validate-dispatch.py \
  <(patch --silent --output=- \
    projects/cyberalchemy-lab/development/refinement-runs/20260809T192255Z-white-canvas-proper-tower/REFINE-DISPATCH.json \
    projects/cyberalchemy-lab/development/refinement-runs/20260809T192255Z-white-canvas-proper-tower/sidecars/REFINE_RECEIPT_SCHEMA_DEFECT/CANDIDATE.patch)
```

Observed: `VALIDATION=pass`, exit `0`, target `/dev/fd/63`.

## Changed-byte inventory

| Path | Change | Evidence |
|---|---|---|
| `sidecars/REFINE_RECEIPT_SCHEMA_DEFECT/CANDIDATE.patch` | New candidate only; 29 insertions and 17 deletions if applied to the live dispatch | 5,956 bytes; SHA-256 `d3fb66d62255c0839933d447a75057d09930de7720b0595701f085a15e652926` |
| `sidecars/REFINE_RECEIPT_SCHEMA_DEFECT/SIDECAR-RECEIPT.md` | New sidecar evidence | This receipt only; no live target bytes |

Forbidden scopes remain untouched: product files, tests, Arcanum canonical or generated sources, telemetry ledger, authority, promotion, publication, deployment, Git history, and external transports.

## Required revalidation after any authorized apply

1. Re-run `git apply --check` immediately before apply to detect concurrent target drift.
2. Apply only `CANDIDATE.patch` to the named `REFINE-DISPATCH.json`.
3. Run `jq empty` on the live dispatch.
4. Run the exact Dispatch Spec validator command above against the live dispatch and require exit `0` plus `VALIDATION=pass`.
5. Re-run the Orchestrate run-evidence validator for `subagents/orchestrate/run-001` and require a passing terminal reduction.
6. Recompute the live dispatch digest and any acceptance inventory bound to it.
7. Verify the changed-file inventory contains no product, Arcanum, telemetry, authority, publication, deployment, or Git-history mutation.

## Renewed acceptance

No renewed semantic or product-design decision is required. Renewed owner acceptance of the exact repaired dispatch bytes **is required before apply** if the live dispatch has already been frozen or acceptance-bound; the patch changes closeout evidence and an older digest cannot cover those bytes. The parent must inspect this receipt and own that gate.

## Permanent regression recommendation

Add a Dispatch Spec closeout fixture/test that constructs the same capability-bound two-reviewer shape and fails before acceptance unless:

- lifecycle statuses use schema enums rather than generic result statuses;
- all capability-bound lifecycle fields are present and match their role and wave;
- `receipt_artifact` is one of the role's `output_refs`;
- every native receipt uses `capability_ref`, `receipt_kind`, and `artifacts` or `validation`; and
- the delegated step receipt includes all role outputs.

The validator should also compare every actual native receipt against the strategy's declared `receipt_requirements`. Today that declaration includes fields such as `observer_status`, `blockers`, `residue`, and `handoff_note`, but the native receipt validator does not enforce their presence. Closing that coverage gap will prevent a schema-valid but contract-incomplete receipt from reaching the next acceptance request.
