# Task Contract: Victor Trial And Pilot Readiness

## Control

| Field | Value |
| --- | --- |
| Task ID | `TASK-RDL-VERIFY` |
| Objective | Obtain real newcomer evidence and close only the pilot-readiness claim supported by it. |
| Layer / slice / wave | L3 / S-005 / W4 |
| Dependencies | SWU-RDL-011 for trial; SWU-RDL-012 and 013 for closeout |
| Blockers | Real Victor availability and owner acceptance round trip. |
| Execution | Manual human gate; never delegate or simulate participant evidence. |

## Sources

- [UX comprehension gate](../../UX-PLAN.md#comprehension-gate)
- [L3 boundary](../../IMPLEMENTATION-LAYERING.md#layer-decision-table)
- [Traceability](../shared/traceability.md)

## SWU-RDL-013 — Real Victor comprehension/usefulness trial

- **Objective:** Test whether a total newcomer can understand and improve the
  roadmap without repository coaching.
- **Dependencies:** SWU-RDL-011; available real Victor; stable published revision.
- **Write scope:** W4 protocol, time-stamped trial report, sanitized browser/event
  evidence, and Task Session receipt only. No product-source fixes during the
  timed trial.
- **Protocol:** collect self-declared label/consent; start timer; let Victor use
  the focused route; ask the five comprehension questions; require one proposal;
  record time, answers, confusion, abandoned actions, facilitator help, payload,
  and participant usefulness judgment; separate product failure from facilitator
  explanation after the measurement.
- **Pass:** within 30 minutes, substantially correct answers to all five boundary/
  roadmap questions and one actionable, correctly targeted proposal with reason.
  A valuable failing result remains evidence but does not pass.
- **Acceptance evidence:** complete report, exact published bindings, stored
  proposal event, facilitator interventions, and verdict rationale.
- **Validation:** manual two-person review against the protocol and event/schema
  contract; verify no answer was backfilled after coaching.
- **Owner:** `manual` — Victor plus facilitator/reviewer.
- **Handoff:** route the actual proposal. If presentation copy is accepted it may
  feed 012; otherwise record why a separate accepted copy proposal is required.

## SWU-RDL-014 — Pilot readiness and no-overclaim audit

- **Objective:** Reconcile all evidence and state exactly what the pilot proves
  and what production work remains.
- **Dependencies:** SWU-RDL-012 and SWU-RDL-013 pass.
- **Write scope:** work-pack status, traceability/gap synchronization, evidence
  index, and final readiness report only. No feature mutation.
- **Rules:** verify every accepted outcome has a receipt; check design/plan/code/
  evidence links; rerun or cite current planned suites; confirm no private/public
  leak and no submission/acceptance/application collapse; list deferred identity,
  collaboration, authorization, lifecycle automation, scale, and support work;
  recommend next route based on evidence.
- **Done:** package is navigable, statuses agree, pilot claim is bounded, gaps
  have owners/routes, and no required evidence is missing.
- **Acceptance evidence:** closeout matrix, link/status audit, validation summary,
  and explicit verdict: pilot-ready, narrow/redesign, or blocked.
- **Validation:** deterministic link/status checks, `git diff --check` on package,
  evidence review, and exact command/results table from preceding SWUs.
- **Owner:** `manual` coordinator/reviewer.
- **Handoff:** if pilot-ready, invoke a separate productionization/hardening
  design; this work-pack never self-promotes to general production.

## Synchronization And Completion

Human evidence is immutable source material for the verdict. Fixes discovered
during the trial become new planned work; they do not silently rewrite the
measured session.

