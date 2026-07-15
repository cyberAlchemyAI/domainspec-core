# Task Contract: Degraded Behavior And Accepted Copy Round Trip

## Control

| Field | Value |
| --- | --- |
| Task ID | `TASK-RDL-ROUNDTRIP` |
| Objective | Prove failures preserve evidence, then close one genuinely accepted presentation-copy change. |
| Layer / slice / wave | L2/S-004/W3 and L3/S-005/W4 |
| Dependencies | SWU-RDL-010; SWU-RDL-012 additionally needs SWU-RDL-013 and owner acceptance |
| Blockers | Real owner acceptance is mandatory for SWU-012. |
| Execution | 011 before trial; 012 after the real trial/acceptance gate. |

## Sources

- [RDL-O04 applied copy flow](../../ARCHITECTURE-BUNDLE.md#rdl-o04-apply-one-accepted-presentation-copy-change)
- [Error principles](../../UX-PLAN.md#accessibility-and-error-principles)
- [L2/L3 boundaries](../../IMPLEMENTATION-LAYERING.md#layer-decision-table)

## SWU-RDL-011 — Negative and degraded-mode proof

- **Objective:** Demonstrate that the complete route fails closed and preserves
  user work/original evidence.
- **Dependencies:** SWU-RDL-010.
- **Write scope:** focused visibility/IDE tests and only minimal fixes inside
  already owned template/focused-mode files. No auth, snapshot, remote, or
  generic hardening subsystem.
- **Rules:** test invalid/oversized payload, disconnected API, retry, duplicate,
  stale revision/fingerprint/original, removed field, unsupported/protected
  class, absent owner evidence, restart, and unrelated current Canvas surface;
  drafts survive retryable failure and originals survive every disposition.
- **Done:** every expected failure has a visible state, no direct effect, and no
  false stored/accepted/applied acknowledgment.
- **Acceptance evidence:** failure matrix, browser artifacts, regression output,
  and owner-boundary code review.
- **Validation:** focused negative Node/Playwright suites plus existing Canvas
  contracts/replay/publish/interactions.
- **Owner:** `local-fallback`.
- **Handoff:** W3 passes only if all authority-critical negatives pass; then 013
  may run.

## SWU-RDL-012 — Accepted presentation-copy application

- **Objective:** Close one real accepted proposal from evidence to new published
  revision.
- **Dependencies:** SWU-RDL-011 and SWU-RDL-013 pass; concrete presentation-owner
  acceptance for a non-stale proposal.
- **Write scope:** only the accepted field in `visibility/roadmap-copy.json`,
  regenerated visibility outputs, required evidence under this work-pack, and
  Task Session/status synchronization. No graph/manifest/Craft mutation.
- **Rules:** verify owner/evidence and current original/fingerprint; apply exact
  accepted wording; run full visibility tests and generated check; publish new
  complete Canvas revision; capture before/after, old/new fingerprints and
  revisions; project applied only after all proof passes.
- **Stop cases:** proposal class is not presentation copy, acceptance missing,
  proposal stale, broader edits required, tests fail, publish fails, or current
  worktree ownership is unresolved.
- **Done:** one accepted copy proposal has a complete auditable chain and the UI
  shows `applied-with-evidence` without widening claims.
- **Acceptance evidence:** original event, owner receipt, exact source diff,
  validation output, generated diff, publish response, browser before/after,
  and disposition evidence reference.
- **Validation:** full visibility unittest suite/build check; focused Canvas
  publish/replay/interactions; Roadmap Lab Playwright before/after witness.
- **Owner:** `manual` through the presentation owner and Task Session.
- **Handoff:** enable SWU-RDL-014 only after the entire chain is retained.

## Synchronization And Completion

If Victor's proposal is valuable but not accepted or not copy-targeted, retain
the successful trial and return SWU-012 blocked-human-owner. Do not manufacture
an acceptance merely to close the plan.

