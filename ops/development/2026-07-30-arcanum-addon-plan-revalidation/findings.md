# Arcanum Add-on Plan Revalidation Findings

## Parent Verdict

- Dispatch: `2026-07-30-arcanum-addon-plan-revalidation`
- Run: `arcanum-addon-plan-revalidation-cc655251`
- Confirmed sheet SHA-256:
  `cc655251c83bb1fba988921680870be78bcad5644fc43c77729aafa286905646`
- Admitted corpus SHA-256:
  `bb0a6f31cf1142902693d30c53ecc2ee08b6747e14ea12f7dff5b81d08d64b14`
- Source commit:
  `80dcd79677ad73b21dbaded12e0e9cd47aace82b`
- Agent lifecycle: both agents spawned once, joined, and closed
- Native gate: `gate_block`
- Artifact verdict: **FIX**

Both fresh reviewers found that all six findings from the first Distill review
are closed in the current literal corpus. The revalidation still blocks because
each reviewer independently found a different new MAJOR defect. Therefore
`B-DESIGN-001` remains open.

## Prior-Finding Closure

| Prior finding | Proposer | Balancer | Parent disposition |
| --- | --- | --- | --- |
| F-001 durable L0 continuation decision | closed | closed | closed in current bytes |
| F-002 isolated uninstall/rollback branches | closed | closed | closed in current bytes |
| F-003 lifecycle witnesses and counters | closed | closed | closed in current bytes |
| F-004 degradation SWU and acceptance | closed | closed | closed in current bytes |
| F-005 complete atomicity and BOOT-002 transactionality | closed | closed | closed in current bytes |
| F-006 atomic governance receipt | closed | closed | closed in current bytes |

Closure of these six defects does not satisfy the gate while new MAJOR defects
survive.

## Surviving Findings

### NEW-001 — MAJOR — Implementation dispatch bypasses complete wave closure

The work-pack requires full intra-wave sequences and receipt-set joins, but
`plan/DISPATCH.json` compresses each layer into one generic selected-SWU
receipt:

- `DISPATCH.json:118-147` emits one `L0-selected-swu` receipt;
- `DISPATCH.json:152-224` advances through L1 and L2 using one generic prior
  layer receipt;
- `DISPATCH.json:228-281` reaches verification after one generic L3 receipt.

That route conflicts with the complete W1-W4 sequences and joins in
`WORK-PACK.md:67-93`, `W1.md:6-13`, `W2.md:5-12`, `W3.md:5-15`,
`W4.md:5-15`, and `TASK-5-VERIFY-DECIDE.md:25-28`.

Failure consequence: a conforming route runner can cross a layer boundary
before every required SWU and wave receipt exists. A later verification stop
condition detects missing evidence too late; it does not repair the dependency
graph.

Required repair: replace generic per-layer edges with explicit per-SWU
re-entry/loop gates and complete wave-receipt joins. Bind verification to the
complete W4 bundle, not `L3-selected-swu.json`.

### NEW-BAL-001 — MAJOR — Lifecycle validator conflates enabled and disabled baselines

`design/VALIDATION-CONTRACTS.md:18-19` and
`TASK-4-LIFECYCLE-ACCEPTANCE.md:25-37` define degradation from an
enabled/running accepted candidate. Yet
`design/VALIDATION-CONTRACTS.md:33` gives the aggregate
`V-LIFECYCLE-BRANCHES` validator one accepted binding: the same disabled
snapshot digest for degradation, uninstall, and rollback.

The disabled snapshot correctly belongs only to the uninstall/rollback branches
(`TASK-4-LIFECYCLE-ACCEPTANCE.md:49-72,81-83`).

Failure consequence: a literal validator must either reject correct degradation
evidence for lacking a disabled-snapshot digest or falsely relabel degradation
as starting disabled. Either result makes SECURITY-001 recomposition ambiguous.

Required repair: type and join two binding classes:

1. DEGRADE-001: accepted enabled/running candidate plus compatibility and owner
   baseline digests.
2. UNINSTALL/ROLLBACK: one shared accepted disabled-snapshot digest plus
   isolated branch IDs and counters.

SECURITY-001 must require both binding classes explicitly.

## Parent Verification

The parent independently:

- recomputed the exact aggregate digest using the sorted absolute-path
  `sha256sum` stream over all `define/`, `design/`, and `plan/` files;
- verified target `HEAD` and `origin/dev` both equal the admitted commit;
- inspected the literal route, wave, lifecycle, validator, and security
  contracts supporting both new findings;
- confirmed the target worktree still has only its pre-existing untracked
  `development/` planning package;
- admitted both normalized receipts to the deterministic Orchestrate reducer;
- obtained `gate_block` with zero next actions; and
- validated all 14 native lifecycle events with zero causal-order errors.

## Ordered Change Requests

1. Repair the implementation dispatch so every layer transition requires the
   full prior-wave receipt set and branch join.
2. Split `V-LIFECYCLE-BRANCHES` into typed degradation and disabled-lifecycle
   baseline bindings, then join both at SECURITY-001.
3. Document the corpus aggregate algorithm beside the digest so future
   reviewers can reproduce it without caller assistance.
4. Preserve `selectedSWU: none` and all independent execution blockers.
5. Run a new exact-byte independent revalidation after the two planning repairs.

## Claim Ceiling

This review proves that F-001 through F-006 are closed and that the current
planning corpus remains owner-preserving at the architectural level. It does
not pass Distill, close `B-DESIGN-001`, select an SWU, implement the add-on,
refresh Bootstrap packages, run a browser, or establish readiness, promotion,
deployment, or release.
