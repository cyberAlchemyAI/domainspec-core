# Design Distill Validation

## Status

- Mode: Validate
- Runtime path: independent Proposer and Balancer roles
- Dispatch: `arcanum-addon-invoke-distill-validation-v1`
- Run: `run-20260730-f3ada9f1`
- Proposer: spawned once, joined, closed, validation `block`
- Balancer: spawned once, joined, closed, validation `block`
- Native gate: `gate_block`
- Current verdict: block after second independent revalidation and bounded
  parent reconciliation
- Design selection validator: pass
- Architecture authoring: complete

## Why This Is Separate

The deterministic Design selector proves total concern coverage and a stable
output set. It does not independently challenge whether the architecture is the
smallest coherent unit, whether a hidden owner transfer remains, or whether the
significant scenario recomposes without hidden glue.

## Joined Read-only Roles

| Role | Review target | Required receipt |
| --- | --- | --- |
| Proposer | smallest coherent integration, six-view closure, recomposition into the expected end state | [`../plan/distill/PROPOSER.md`](../plan/distill/PROPOSER.md) |
| Balancer | owner collapse, hidden runtime, state/replay/secret/rollback gaps, planned-witness inflation | [`../plan/distill/BALANCER.md`](../plan/distill/BALANCER.md) |

Join policy `all` completed. Both agents were read-only. Invoke remains the
synthesis owner.

## Reconciliation

- Accepted: add a durable L0 continuation receipt.
- Accepted: treat uninstall and rollback as isolated branches from copies of
  one accepted disabled snapshot.
- Accepted: add explicit degradation, uninstall-preservation, and rollback
  success/failure witnesses.
- Accepted: require complete SWU atomicity coverage and a BOOT-002 partial-apply
  contract.
- Accepted: make the governance packet fail closed on partial synchronization.

The Design witness contracts were revised, but the original independent
receipts correctly remain blocking evidence over the bytes they reviewed. A
second independently authorized validation is required to move this verdict to
pass. Design may inform blocked planning; it does not authorize mutation.

## Second Revalidation And Current Reconciliation

- Confirmed review sheet:
  `cc655251c83bb1fba988921680870be78bcad5644fc43c77729aafa286905646`
- Admitted pre-repair corpus digest:
  `bb0a6f31cf1142902693d30c53ecc2ee08b6747e14ea12f7dff5b81d08d64b14`
- Source commit:
  `80dcd79677ad73b21dbaded12e0e9cd47aace82b`
- Result: F-001 through F-006 closed; `NEW-001` and `NEW-BAL-001` blocked.

The admitted digest was computed from an absolute `addon_root` so the
`sha256sum` records also bind absolute paths:

```bash
find "$addon_root/define" "$addon_root/design" "$addon_root/plan" \
  -type f -print0 |
  sort -z |
  xargs -0 sha256sum |
  sha256sum
```

The current Invoke refresh splits the lifecycle validator into
`V-DEGRADATION-BASELINE`, `V-DISABLED-LIFECYCLE-BRANCHES`, and
`V-SECURITY-LIFECYCLE-JOIN`. Degradation remains bound to an accepted
enabled/running candidate plus compatibility and owner baselines. Uninstall and
rollback remain isolated branches over one later accepted disabled snapshot.
Security must join both typed classes without equating their baseline digests.

This reconciliation is authored evidence only. A fresh independent review must
bind the exact repaired corpus before this verdict or `B-DESIGN-001` can change.

## Repair Revalidation And Machine Admission Repair

- Confirmed sheet:
  `a850483e486e6d09f6baab804628ea2fd89244ee6fd69bd4115c96ef1c7ca6a1`
- Admitted pre-repair corpus:
  `5b5e79f5632b2e29e7a20e7ac4d9e92addef6f707e9525c71e7266c24349e4b0`
- Verdict: seven findings closed; `NEW-001` remained MAJOR because
  `g-swu-reentry` was not consumed by executable steps.
- Current authored repair: every exact SWU consumes a fresh
  `receipts/selections/SWU-ARC-<ID>.json` decision. The input contract
  literally binds dispatch, step, SWU, source, work-pack, expiry, and a
  single-use nonce; invalid selection yields zero starts.
- Claim ceiling: authored repair only. `B-DESIGN-001`, work-pack block, and
  `selectedSWU: none` remain until fresh exact-byte independent validation.
