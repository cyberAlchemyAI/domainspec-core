---
module: keystone-lift
task: TASK-AUDIT
docType: work-pack-task
updatedAt: 2026-06-14
---

# TASK-AUDIT — Moat-leak + sanitization gate (B-KSL-2)

Layer: L2 · Wave: W2 (and re-run whole-diff before W3 push) · Gate: ready-after-impl
**Smallest Working Unit Exemption:** task ID contains `AUDIT` (closure task).

## Objective
Guarantee no moat content reaches public arcanum. This is the safety gate that flips `workPackGateStatus` from block to pass. It runs on the **staged arcanum diff**, not the whole repo.

## Checklist (all must pass)
1. `git -C arcanum diff --staged` piped to each grep returns **0 hits**:
   - moat IDs: `DS-C3|DS-D9|DS-COR-1|DS-F1|DS-F5|DS-F6|DS-M13`
   - ambiguous (private by default): `DS-D4|DS-D5|DS-D6`
   - stale/PT strings: `ZefraHub|veracidade|convic`
   - hardcoded DS CI names: `validate-governance-chain|validate-signals|domainspec-tuning`
   - private paths: `implementation/domainspec|\.arcanum/`
2. arcanum markdown-linking constitution + definitions-index + link checker: **green**.
3. Proposed ~38-edge extension absent; only the 25-type/29-edge profile present.
4. Collision terms (`schema`/`contract`) carry boundary notes; `DEF-ARC-*` unchanged.

## Failure policy
Any hit ⇒ **BLOCK** the push; remediate the offending file; re-run. No override without explicit operator approval recorded here.

## Evidence
Record the grep outputs + validator results in a `AUDIT-REPORT.md` alongside this task before any push.
