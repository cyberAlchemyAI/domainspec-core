# Interface Workbench Rework Invoke Run

- Run ID: `20260727T192427Z-interface-workbench-rework`
- Target: UI Prototyping Studio local governed workbench
- Route: Invoke Define → Design → Plan
- Status: Plan Distill BLOCK; verified remediation required
- Prior implementation chain: receipt-complete, terminal, and not reopened
- Selected SWU: `none`
- Implementation authority: `none`

This run turns the verified 2026-07-27 interface audit into a new bounded
authoring package. It does not modify Studio source, select an implementation
unit, reopen the completed GSP chain, or grant human-study, accessibility,
release, deployment, or production-readiness claims.

The reviewed candidate contains 19 mutation SWUs plus a closure-only VERIFY
task. Its mutation, acceptance, and closeout candidates are in
`SWU-SCOPE-INVENTORY.json`, `SWU-ACCEPTANCE-MATRIX.json`, and
`CLOSEOUT-SYNC-INVENTORY.json`. Fresh governed Plan Distill returned BLOCK:
SWU-016, SWU-017, and SWU-019 require splits, and closeout/W5 is not yet
executable. The verified changes are in
`plan-redistill-review/findings.md`.
