# Arcanum Add-on Invoke Distill Review Findings

## Parent Verdict

- Review dispatch: `2026-07-30-arcanum-addon-invoke-distill-review`
- Runtime dispatch: `arcanum-addon-invoke-distill-validation-v1`
- Exact confirmed sheet:
  `f3ada9f189c26482029cebcd2aa14633db915b4596c4cbe8e065082837df72d5`
- Both agents: spawned once, joined, closed, and read-only
- Native gate: `gate_block`
- Artifact verdict: `FIX`
- Dispatch close disposition: `resolved` once this verified change-request list
  is accepted; FIX is the review deliverable, not implementation readiness.

## Surviving Findings

| # | File | Evidence | Severity | Proposed fix |
| --- | --- | --- | --- | --- |
| F-001 | `plan/work-pack/waves/W1.md`, `W2.md`, TASK-1, TASK-2 | L0 named a continuation decision but W2 had no durable owner receipt dependency. | MAJOR | Add L0-DECISION-001 and require its exact current `continue` disposition for APPROVAL-001/W2. |
| F-002 | `plan/work-pack/waves/W4.md`, TASK-4, closeout sync | W4 serialized uninstall before rollback although both require different copies of the disabled candidate. | MAJOR | Branch uninstall and rollback from isolated copies of one accepted disabled snapshot; join both receipts. |
| F-003 | `design/VALIDATION-CONTRACTS.md`, `PLANNED-WITNESSES.json` | Uninstall, rollback failure, compatibility drift, and owner loss lacked exact planned witnesses. | MAJOR | Add digest-bound fixtures, forbidden-mutation counters, recovery rules, and a lifecycle-branch validator. |
| F-004 | TASK-4 and Work Pack | L3 promised degraded-mode proof without a scheduled compatibility-drift/owner-loss SWU. | MAJOR | Add DEGRADE-001 with zero-start, honest projection, history preservation, and explicit recovery acceptance. |
| F-005 | `plan/WORK-PACK.md` and TASK-0 | Aggregate atomicity omitted BOOT-002, PROPOSAL-UI-001, and RUN-UI-001; BOOT-002 had no partial-apply contract. | MAJOR | Enumerate every non-exempt SWU and require atomic staged apply/restoration or pre-execution split for BOOT-002. |
| F-006 | TASK-0 and Work Pack | GOV-001 could leave issue, Project, owners, and retention partially synchronized. | MINOR | Require one digest-bound complete authority receipt; partial synchronization is non-pass. |

Artifact verdict: **FIX**.

## Reconciliation

| Finding | Disposition | Reconciliation |
| --- | --- | --- |
| P-001 / F-001 | accept and revise | Added `SWU-ARC-L0-DECISION-001`, owner receipt contract, closeout row, and W2/APPROVAL dependency. |
| P-002 + BAL-001 / F-002 | accept and revise | Replaced linear W4 with isolated uninstall/rollback branches and a required join. |
| BAL-002 + P-003 / F-003/F-004 | accept and revise | Added DEGRADE-001, four planned fixtures, three planned witnesses, V-LIFECYCLE-BRANCHES, branch counters, and recovery rules. |
| P-004 + BAL-003 / F-005 | accept and revise | Expanded aggregate atomicity to every non-exempt SWU and made BOOT-002 conditional on staged atomic apply/restoration or a split. |
| BAL-004 / F-006 | accept and revise | Strengthened GOV-001 to one exact, digest-bound, complete owner receipt; partial state authorizes no successor. |

No finding was rejected or softened. The parent verified the changed planning
contracts, but the original agents' blocking validation receipts remain literal.
Therefore B-DESIGN-001 and the native gate remain block until separately
authorized independent revalidation closes the repaired bytes.

## Refuted or Dropped Findings

None. Both reviewers explicitly reported that the current contracts materially
cover stale approval, replay, partial-child isolation, reload/Unknown,
independent result actions, disable rejection, secret/path redaction,
absent-owner no-substitution, and planned-witness claim ceilings.

## Ordered Change Requests

1. Keep the newly authored L0 decision receipt as a mandatory W2 dependency.
2. Preserve lifecycle branch isolation and require both branch receipts.
3. Materialize and execute degradation/uninstall/rollback fixtures only in
   their future owner SWUs; do not count them as current evidence.
4. Split BOOT-002 before execution if Bootstrap cannot prove atomic staged
   apply or exact restoration.
5. Require the atomic governance receipt before any successor becomes eligible.
6. Retain B-DESIGN-001 until independent revalidation of the reconciled bytes.

## Claim Ceiling

The Invoke Design/Plan package is materially stronger and navigable, but its
Distill gate is still block. No SWU is selected. No product implementation,
runtime execution, browser witness, readiness, promotion, or release is proven
or authorized.
