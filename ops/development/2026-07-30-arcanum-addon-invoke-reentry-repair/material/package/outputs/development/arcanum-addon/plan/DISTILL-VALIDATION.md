# Plan Distill Validation

## Current Result

- Target: Arcanum add-on high-complexity split Plan
- Mode: Validate
- Dispatch: `arcanum-addon-invoke-distill-validation-v1`
- Run: `run-20260730-f3ada9f1`
- Proposer receipt: [`distill/PROPOSER.md`](distill/PROPOSER.md), joined and
  closed, validation `block`
- Balancer receipt: [`distill/BALANCER.md`](distill/BALANCER.md), joined and
  closed, validation `block`
- Native gate: `gate_block`; zero next actions
- Parent reconciliation: complete for the first-review list and the two
  second-revalidation findings
- Verdict: block pending fresh exact-byte independent revalidation of the
  current repaired bytes

## Authored Precheck

| Check | Result | Evidence/gap |
| --- | --- | --- |
| Smallest coherent unit | pass-reconciled-authored | L0 adds a durable continuation decision before approval/run work |
| SWU atomicity | pass-reconciled-authored | complete non-exempt set mapped; BOOT-002 must split if staged atomic apply/restoration cannot be proven |
| First-unit narrowness | pass-authored | governance, then no-write compatibility, then catalog mutation |
| Recomposition | pass-reconciled-authored | W4 now joins isolated uninstall/rollback branches from one accepted disabled baseline |
| Hidden gaps | block-revalidation-required | degradation and lifecycle witness gaps were repaired in authored contracts, not independently revalidated |
| Deferred complexity | pass-authored | real adapters, lifecycle execution, browser, and release remain layer-gated |
| Navigation | pass-reconciled-authored | TASK-0/GOV-001 remains start-here; selectedSWU remains none |

## Objection Reconciliation

| Objection | Disposition | Result |
| --- | --- | --- |
| P-001 durable L0 decision | accept/revise | Added L0-DECISION-001 and exact W2/APPROVAL dependency. |
| P-002 + BAL-001 lifecycle order | accept/revise | Added isolated post-disable uninstall/rollback branches and join. |
| P-003 + BAL-002 missing degradation/lifecycle witnesses | accept/revise | Added DEGRADE-001, explicit fixtures/witnesses, counters, and recovery rules. |
| P-004 + BAL-003 incomplete atomicity/BOOT-002 | accept/revise | Enumerated all non-exempt SWUs; staged atomic apply/restoration or split is mandatory. |
| BAL-004 GOV-001 coupling | accept/revise | Added one digest-bound complete authority receipt; partial synchronization fails closed. |

No objection was rejected or softened. The current block is deliberate: the
parent verified the authored repair, but parent review does not replace the two
independent validation verdicts. Governance, Bootstrap, owner, adapter, and
retention blockers also remain unaffected.

## Second Revalidation Reconciliation

The confirmed second review
`cc655251c83bb1fba988921680870be78bcad5644fc43c77729aafa286905646`
admitted source commit
`80dcd79677ad73b21dbaded12e0e9cd47aace82b` and pre-repair corpus digest
`bb0a6f31cf1142902693d30c53ecc2ee08b6747e14ea12f7dff5b81d08d64b14`.
It closed F-001 through F-006 and returned two new MAJOR findings:

The exact aggregate algorithm used an absolute `addon_root` and a sorted
NUL-delimited path stream:

```bash
find "$addon_root/define" "$addon_root/design" "$addon_root/plan" \
  -type f -print0 |
  sort -z |
  xargs -0 sha256sum |
  sha256sum
```

| Finding | Disposition | Current authored result |
| --- | --- | --- |
| `NEW-001` generic layer receipts bypass complete wave closure | accept/revise | `DISPATCH.json` now uses one exact node/receipt per SWU, explicit closeout re-entry, W0-W4 receipt-set joins, sibling uninstall/rollback branches, and `VERIFY-001` consuming `W4-COMPLETE.json`. |
| `NEW-BAL-001` enabled and disabled lifecycle baselines conflated | accept/revise | Design and TASK-4 now type degradation, disabled lifecycle branches, and their security join separately. |

Historical review receipts remain unchanged because they describe the bytes
they reviewed. The current repaired corpus still requires fresh independent
exact-byte revalidation; no SWU is selected and all unrelated blockers remain.

## Repair Revalidation And Machine Admission Repair

- Confirmed sheet:
  `a850483e486e6d09f6baab804628ea2fd89244ee6fd69bd4115c96ef1c7ca6a1`
- Admitted pre-repair corpus:
  `5b5e79f5632b2e29e7a20e7ac4d9e92addef6f707e9525c71e7266c24349e4b0`
- Verdict: seven findings closed; `NEW-001` remained MAJOR because
  `g-swu-reentry` was not consumed by executable steps.
- Current authored repair: every exact SWU consumes a fresh
  `receipts/selections/{session_id}/SWU-ARC-<ID>.json` decision. The input contract
  literally binds dispatch, step, SWU, source, work-pack, expiry, and a
  single-use nonce; invalid selection yields zero starts.
- Claim ceiling: authored repair only. `B-DESIGN-001`, work-pack block, and
  `selectedSWU: none` remain until fresh exact-byte independent validation.
