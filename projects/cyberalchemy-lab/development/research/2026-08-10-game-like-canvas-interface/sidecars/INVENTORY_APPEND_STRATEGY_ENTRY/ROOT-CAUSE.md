# Inventory Append Strategy Entry Sidecar Diagnosis

Authority: none. This is a candidate-local governance diagnosis and does not apply Inventory projections or alter dispatch authority.

## Root Cause

The failed command passed `inventoryRoot: ".arcanum/inventory"` to `runAppendDryRun`. The runtime successfully used that relative path for direct reads. `runValidator`, however, constructed the validator argument as `.arcanum/inventory/scripts/validate_projection_conformance.py` and also launched Python with `cwd: .arcanum/inventory`. The child therefore resolved a doubled path under `.arcanum/inventory/.arcanum/inventory/scripts/`. Python produced no JSON report, so the runtime substituted `validatorFailureReport()` with one `validator_execution` failure and zero warnings. That synthetic report cannot satisfy `isExactPendingSourceGap`, producing `baseline-blocked` / `baseline-not-ready`.

The actual live validator reports exactly one source-coverage gap for `entries/cyberalchemy-game-like-canvas-interface-research-strategy-result-synthesis.md`, no other errors, and 150 inherited tag warnings. With absolute `inventoryRoot` and `recordPath`, the unchanged runtime returns `dry-run-ready`: baseline failure count 1, candidate disposition `added`, and candidate lookup readiness `ready`, with no write attempted.

## Affected Invariant

Repository-relative and absolute representations of the same Inventory root must resolve to the same validator bytes and validation outcome. A validator launch-path error must not masquerade as an unrelated baseline-conformance defect.

## Immediate Safe Invocation

No live runtime repair is required to unblock this append. Resolve both paths before calling the API:

```sh
node -e 'const path=require("node:path"); const t=require("./.arcanum/inventory/lib/inventory-update.cjs"); const r=t.runAppendDryRun({inventoryRoot:path.resolve(".arcanum/inventory"),recordPath:path.resolve(".arcanum/inventory/tmp/cyberalchemy-game-like-canvas-interface-research-strategy-result-synthesis.record.json"),timestampInput:"2026-08-10T20:20:00Z"}); console.log(r.bytes); process.exitCode=r.exitCode'
```

Expected dry-run receipt status: `dry-run-ready`. This command performs no Inventory write.

After binding the returned candidate digests and rechecking the live baseline, the corresponding apply call may use `runAppendApply` with the same absolute paths. Apply authority remains with the parent owner and is not granted by this sidecar.

## Permanent Repair Proposal

Normalize `inventoryRoot`, `indexPath`, and optional `sourceInventoryRoot` with `path.resolve` inside the exported `runValidator` boundary before constructing arguments or child `cwd`. The candidate patch is `candidate/inventory-update-relative-root.patch`.

Add the permanent regression `tests/test-relative-root-admission.cjs`: it proves the current synthetic failure, applies the candidate transformation only inside an isolated fixture, proves `dry-run-ready`, and verifies zero byte mutation.

## Acceptance And Revalidation

The safe absolute-path re-invocation changes no accepted source, record, strategy, dispatch, or runtime bytes; renewed strategy-owner acceptance is not required. A later live runtime patch would be a new maintenance candidate requiring its own runtime-owner review and revalidation, but it would not change the admitted dispatch-sheet digest or require strategy reconfirmation.

Required before any apply:

1. Re-run the absolute-path dry-run and bind its current baseline and candidate digests.
2. Run projection conformance directly and confirm the only baseline error is the exact pending source row.
3. Confirm candidate lookup readiness is `ready`, write attempted is `false`, and live `index.json` / `index.md` digests are unchanged.
4. Only under separate parent apply authority, run `runAppendApply` with absolute paths.
5. Re-run projection conformance and verify the human and machine indexes both represent the exact entry.

For the optional runtime repair, additionally run the existing pending-source, split-root staging, append/apply, operation-receipt, and installed-consumer suites plus the new relative-root regression.
