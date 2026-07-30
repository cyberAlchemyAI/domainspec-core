# Arcanum Add-on Repair Revalidation Findings

## Parent Verdict

- Dispatch: `2026-07-30-arcanum-addon-repair-revalidation`
- Run: `arcanum-addon-repair-revalidation-a850483e`
- Confirmed sheet SHA-256:
  `a850483e486e6d09f6baab804628ea2fd89244ee6fd69bd4115c96ef1c7ca6a1`
- Admitted corpus SHA-256:
  `5b5e79f5632b2e29e7a20e7ac4d9e92addef6f707e9525c71e7266c24349e4b0`
- Source commit:
  `80dcd79677ad73b21dbaded12e0e9cd47aace82b`
- Agent lifecycle: both agents spawned once, joined, and closed
- Native gate: `gate_block`
- Artifact verdict: **FIX**

The first repair closed seven of the eight reviewed findings. It did not close
`NEW-001` at the machine-route level. The Proposer accepted the prose re-entry
condition as sufficient; the Balancer tested scheduler reachability and found
that no executable step consumes a selection binding. The literal dependency
graph therefore wins the disagreement. `B-DESIGN-001` remains open.

## Finding Closure

| Finding | Proposer | Balancer | Parent disposition |
| --- | --- | --- | --- |
| F-001 durable L0 continuation decision | closed | closed | closed in current bytes |
| F-002 isolated uninstall/rollback branches | closed | closed | closed in current bytes |
| F-003 lifecycle witnesses and counters | closed | closed | closed in current bytes |
| F-004 degradation SWU and acceptance | closed | closed | closed in current bytes |
| F-005 complete atomicity and BOOT-002 transactionality | closed | closed | closed in current bytes |
| F-006 atomic governance receipt | closed | closed | closed in current bytes |
| NEW-001 implementation dispatch bypass | closed | block | **MAJOR survives** |
| NEW-BAL-001 lifecycle baseline conflation | closed | closed | closed in current bytes |

## Surviving Finding

### NEW-001 — MAJOR — Per-SWU operator re-entry is not machine-enforced

`plan/DISPATCH.json` declares a static `mode: sequence` route and names
`g-swu-reentry`, but the gate is only an unattached condition. Mechanical
inspection found no step with a selection-bound input.

The current graph admits this counter-example:

1. `s03-catalog-001` consumes `receipts/W0-COMPLETE.json`.
2. `s04-status-001` consumes `receipts/CATALOG-001.json` and
   `receipts/BOOT-001.json`.
3. `s05-proposal-001` consumes `receipts/STATUS-001.json`.
4. None consumes a fresh owner/operator selection receipt or binds the selected
   SWU ID.
5. The same pattern repeats through later waves.

A conforming dependency scheduler can therefore run successive SWUs without
returning to Task Session selection. Exact receipt producers and complete joins
prevent omitted work, but they do not enforce one explicitly selected SWU per
session.

Required repair: give every exact SWU a fresh source-bound operator-selection
receipt/input whose selected SWU ID must literally match the admitted step, or
compile the corpus as separately selected one-shot routes. The machine route,
validation contract, work-pack prose, and closeout sync must agree.

## Parent Verification

The parent independently:

- recomputed the admitted 75-file corpus digest;
- verified target `HEAD` and `origin/dev` equal the admitted commit;
- parsed all 25 JSON artifacts and ran the existing repair validator;
- ran the repository docs checks and obtained 224/224 documentation tests;
- mechanically inspected the exact step inputs and found zero selection-bound
  steps while `g-swu-reentry` remains unattached;
- confirmed the target worktree still has only its pre-existing untracked
  `development/` package;
- admitted both normalized receipts to the deterministic Orchestrate reducer,
  which returned `gate_block` with zero next actions; and
- validated all 14 native lifecycle events with zero causal-order errors.

The zero-finding red flag does not apply to the parent result: a concrete MAJOR
counter-example survived. The Proposer's zero-finding claim is retained as
disagreement evidence, not accepted as the gate decision.

## Ordered Change Request

1. Machine-bind a fresh selected-SWU receipt to every exact SWU admission.
2. Validate literal selected SWU equality and reject missing, stale, replayed,
   or mismatched selections with zero task starts.
3. Preserve exact SWU producers, full wave joins, typed lifecycle joins,
   `selectedSWU: none`, and all independent execution blockers.
4. Refresh the affected Invoke Plan artifacts as one coherent corpus.
5. Repeat exact-byte independent revalidation before Task Session selects any
   implementation SWU.

## Claim Ceiling

This review proves only that seven findings are closed and one planning defect
survives. It does not close `B-DESIGN-001`, select an SWU, implement the
add-on, refresh Bootstrap packages, run a browser, or establish readiness,
promotion, deployment, or release.
