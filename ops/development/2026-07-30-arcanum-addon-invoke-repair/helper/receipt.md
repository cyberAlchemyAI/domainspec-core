# Bounded background helper receipt

- Route: Route 2 / Invoke refresh
- Helper: `/root/invoke_repair_check`
- Mode: read-only, delegated, proposal-only
- Status: pass
- Mutation: none
- Joined/closed: yes

## Result

The helper independently confirmed the smallest exact repair:

1. Replace generic `L0`-`L3` selected-SWU receipts with one exact receipt
   producer per SWU, explicit closeout/re-entry, complete W0-W4 receipt-set
   joins, sibling uninstall/rollback branches, and VERIFY consuming
   `W4-COMPLETE`.
2. Split the lifecycle validator into:
   `V-DEGRADATION-BASELINE`,
   `V-DISABLED-LIFECYCLE-BRANCHES`, and
   `V-SECURITY-LIFECYCLE-JOIN`.
3. Synchronize the nine target artifacts in the Invoke material package while
   retaining `block`, `selectedSWU: none`, and every independent blocker.

The helper reviewed and recommended no semantic delta to `EXECUTION-PACK.md`,
`W4.md`, `W5.md`, or `TASK-5-VERIFY-DECIDE.md`; their existing complete-wave
contracts are satisfied by the repaired dispatch.

## Residue

- The helper did not inspect or execute product runtime, browser, GitHub,
  public Arcanum, or release work.
- Fresh independent exact-byte revalidation remains audit-owned.
