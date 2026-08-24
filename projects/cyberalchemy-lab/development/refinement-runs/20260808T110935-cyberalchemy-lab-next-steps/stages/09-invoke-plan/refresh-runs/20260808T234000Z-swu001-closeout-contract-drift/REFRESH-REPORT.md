## Outcome Brief

Invoke Refresh compared the passing SWU-CAL-001 terminal receipt with the exact closeout sources. It found that the task and Work Pack still require a retired fixed receipt path, while the accepted admission contract requires the new immutable attempt-specific path. The closeout cannot safely advance to SWU-CAL-002 until that source disagreement is repaired and approved.

- Objective: synchronize the passed SWU-CAL-001 execution into its one-unit successor projection.
- Result: blocked before staging or applying a closeout package.
- Why it matters: the retained fixed path is historical blocking evidence and must not be overwritten or treated as the fresh passing receipt.

## Boundary and Next Decision

- Changed: a strict Context Builder handoff and this blocked refresh report.
- Unchanged: the SWU-CAL-001 product files, its immutable passing terminal receipt, all closeout targets, execution entry, authority, publication, deployment, and Git state.
- Open questions: none about the evidence; the plan sources disagree.
- User decision: approve a new exact repair that changes the conflicting task/Work Pack receipt references (and any other stale fixed-path references) to the immutable attempt template, then revalidate the affected plan sources.
- Next action: Invoke Refresh repair proposal and owner acceptance; after it passes, rerun SWU-CAL-001 closeout from the frozen terminal receipt.

## Invoke Result

- Mode: refresh
- Phase status: block
- Handoff readiness: blocked
- Source signals: one high-confidence `artifact_drift`
- Material package: not staged; the contradiction blocks apply-approved packaging.
- Target artifact: WP-CAL-TEN-L0 closeout, owned by Invoke Refresh.
- Next route: `invoke:refresh:repair-terminal-receipt-prose`
