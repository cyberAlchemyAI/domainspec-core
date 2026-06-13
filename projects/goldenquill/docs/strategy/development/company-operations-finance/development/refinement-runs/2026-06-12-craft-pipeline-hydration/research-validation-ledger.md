# Research Validation Ledger - Company operations and finance

Dispatch: `gq-research-strategy-company-operations-finance-2026-06-12` · Run: `2026-06-12-craft-pipeline-hydration`
Gate rg05 (claim-evidence): each claim → source class → concrete path/handle → validation question → owner-boundary check.
Source classes: WB = workbook handoff · LED = Craft ledger · CON = Golden Quill project constraints · PREP = run-dir prep artifact.

| # | Claim | Source class | Concrete path / handle | Validation question | External state | Owner-boundary | Verdict |
| --- | --- | --- | --- | --- | --- | --- | --- |
| C1 | This node owns the four ops gaps mapped to Workstream G rows 77-80 | WB + LED | `docs/golden-quill-task-role-breakdown-handoff.md` §1 rows 77-80; `.craft/ledger.yml` gaps[0..3] | Do all four ledger gaps trace to a distinct G row? | local-only | planning evidence only | PASS |
| C2 | Entity hygiene needs an operating checklist (banking/bookkeeping/filing/insurance) | WB + LED | handoff row 77; `.craft/ledger.yml` GAP-COF-ENTITY-HYGIENE | Does any local artifact already contain the checklist? (No → authoring gap) | EXT-COF-01 DEFERRED | planning only | PASS (gap real) |
| C3 | Support triage needs explicit "support absorbs vs engineering sees" routing rules + issue-log schema | WB + LED | handoff row 78; `.craft/ledger.yml` GAP-COF-SUPPORT-TRIAGE (severity block) | Are routing rules / channel / log schema present locally? (No → authoring gap) | EXT-COF-02 DEFERRED | planning only | PASS (gap real, block) |
| C4 | Node Care ops cadence is authorable from local evidence (updates, source-index, quarterly check-ins, vault care) | WB + LED | handoff row 79; `.craft/ledger.yml` GAP-COF-NODE-CARE-OPS | Are the Node Care activities enumerated locally? (Yes) | none needed | planning only | PASS |
| C5 | Validation packet contents are named locally (data room, unit economics, support-load, renewal, channel plan), QA-owned | WB | handoff §2 After Acceleration "Next financing" row; handoff row 80 (Founder + QA) | Are packet contents + owner named locally? (Yes) | none needed | planning only | PASS |
| C6 | Bookkeeper and Customer Success are fractional/trigger-staffed, not staffed today | WB | handoff §3 Roles & Gaps: Bookkeeper "few hrs/month at first revenue"; Customer Success "part-time contract as deployments stack" | Does authoring need to encode trigger conditions vs assume staffed? (Yes — trigger) | local-only | planning only | PASS |
| C7 | Validation packet has a cross-node dependency on the C-node claims register; not an external need | WB + CON | handoff §1 Workstream C "Claims register: every external claim mapped to evidence"; row 80 | Is the packet's QA evidence produced in this node or consumed from C? (Consumed → cross-node, not scope merge) | local-only | planning only | PASS (residue) |

## Gate checks

- **rg02 local-first:** PASS — every claim cites a local path/handle; no external source activated.
- **rg03 external-approval:** PASS (DEFERRED) — two bounded external requests named (EXT-COF-01, EXT-COF-02), neither run; awaiting Josh.
- **rg04 org-isolation:** PASS — only Golden Quill PROJECT evidence used; no `orgs/` client PROJECT_CONTEXT read. FIT Farms Commons / Golden Quill business itself is in scope for this ops node.
- **rg05 claim-evidence:** PASS — 7/7 claims carry source class + concrete path + validation question.
- **rg06 owner-boundary:** PASS — only the two RUN_DIR output files written; `.craft/ledger.yml` and canonical/lifecycle artifacts untouched.

## Overall verdict

**PASS.** Local evidence is sufficient to enter local-first authoring for all four gaps. Two gaps (NODE-CARE-OPS, VALIDATION-PACKET) need no external pass. Two gaps (ENTITY-HYGIENE, SUPPORT-TRIAGE) are authorable now with optional approval-gated external hardening (EXT-COF-01 / EXT-COF-02, both DEFERRED). No claim depends on unapproved external evidence. One residue: cross-node claims-register dependency for the validation packet.
