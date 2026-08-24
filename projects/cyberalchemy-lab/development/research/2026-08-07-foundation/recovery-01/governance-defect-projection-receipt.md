# Governance Defect Sidecar Receipt: Recovery Material Projection

- Date: 2026-08-08
- Classification: governance-only, mechanical projection-integrity defect
- Authority ceiling: diagnosis and separately staged repair candidate only
- Confirmed dispatch-sheet SHA-256: `1fc661acb630215700a19abaf9baec00d25c4dbe3bfb4dfd6ceb190c108a795c`
- Result: repair candidate proven equivalent; canonical adoption remains parent-owned

## Root cause

`material-strategy-projection.json` contains the unchanged confirmed material, but its declared `material_sha256` is stale or incorrectly calculated. It declares `b3b746469a27b695ab1d15cccfd3d16cb5b940e5bd338279083269debc87a2e8`; the projection owner computes `f3b4d4eb8400b96362fea3948c654843dc3b27705d5465e36fc53f1a9a1ee7c0` from both the stored material content and the current confirmed sheet.

The material content in the defective projection and a fresh projection of the confirmed sheet is canonically identical. No semantic or material-strategy difference was found.

## Affected invariant

The preserved projection must be internally self-consistent before it can prove material equivalence: its declared digest must equal the SHA-256 of the projection owner's stable canonical material JSON. Because that invariant failed, `--compare` correctly returned exit `1` and `MATERIAL_EQUIVALENCE=unknown`.

## Minimal repair proposal

Adopt `material-strategy-projection.repaired.candidate.json` as the replacement for the defective projection. The candidate changes exactly one value: `material_sha256` from `b3b746...` to owner-computed `f3b4d4...`. Do not change `dispatch-sheet.json`.

This sidecar did not adopt or apply the candidate.

## Proof

- Original failing comparison: exit `1`, `MATERIAL_EQUIVALENCE=unknown`, `material_sha256 does not match projection content`.
- Confirmed sheet remains SHA-256 `1fc661acb630215700a19abaf9baec00d25c4dbe3bfb4dfd6ceb190c108a795c`.
- Stored declared material digest: `b3b746469a27b695ab1d15cccfd3d16cb5b940e5bd338279083269debc87a2e8`.
- Stored actual canonical material digest: `f3b4d4eb8400b96362fea3948c654843dc3b27705d5465e36fc53f1a9a1ee7c0`.
- Fresh sheet projection material digest: `f3b4d4eb8400b96362fea3948c654843dc3b27705d5465e36fc53f1a9a1ee7c0`.
- Canonical material-content comparison: `true`.
- Candidate-to-sheet `--compare`: exit `0`, `equivalence: same`, both material digests `f3b4d4...`.

## Changed-byte inventory

- Added `material-strategy-projection.repaired.candidate.json`: 6,552 bytes; file SHA-256 `18eaed104efd8771181006cbae60f90209a789e2db41acdebe043a406853daa2`; one-value repair relative to the defective projection.
- Added this receipt.
- Unchanged: `dispatch-sheet.json` and `material-strategy-projection.json`.
- No ledger, registration, research, findings, product, ontology, Inventory, Arcanum-source, Git, or external-effect mutation occurred.

## Required revalidation after parent adoption

1. Verify the sheet still hashes to `1fc661acb630215700a19abaf9baec00d25c4dbe3bfb4dfd6ceb190c108a795c`.
2. Run the projection owner's `--compare` against the adopted projection and unchanged sheet; require exit `0`, `equivalence: same`, and material digest `f3b4d4...` on both sides.
3. Rerun live `--validate-sheet` readiness before registration and require `SHEET_VALIDATION=pass`, schema `0.8.0`, the same sheet digest, and `LEDGER_MUTATION=none`.
4. Preserve the already admitted tension evidence only if its handles remain bound to this exact unchanged sheet digest. Any sheet-byte change requires fresh readiness and both tension checks.

## Renewed owner acceptance

No renewed owner acceptance is required for this exact repair. Human confirmation binds the reviewed material strategy; the confirmed sheet bytes are unchanged, and deterministic comparison proves the repair candidate's material equivalent. Parent adoption of the candidate and the required live revalidation remain necessary before registration.

## Permanent workflow regression fix

Generate projection bytes only from `material-strategy.cjs --project`, stage them atomically, and immediately run `--compare <staged-projection> <sheet>` before presenting the human gate. Add a regression fixture with correct material plus a stale declared digest and require the pre-confirmation workflow to fail with exit `1` before confirmation can be requested. Preserve each command's exit status so a later readiness success cannot mask projection-integrity failure.
