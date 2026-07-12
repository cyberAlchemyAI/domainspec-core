# Context Pack: SWU-MSB-007

- Task/SWU: `TASK-HUMAN-WORKBENCH / SWU-MSB-007`
- Dependency: W1 result admission complete; 006 protocol complete in parallel lane
- Sources: approved UX copy/state matrix, current dense Approval Desk HTML/CSS/JS,
  proposal/evidence APIs, workbench tests, responsive conventions
- Runtime: local Codex; no delegation

## Boundaries And Decisions

- Keep the existing operational three-panel workbench and accessible selectors.
- Task becomes visibly labeled, empty by default, required, nonblank, and focused
  with an inline error before any request is sent.
- A skill-bearing form submits the exact bridge grant profile; no skill remains
  the legacy dry-run path.
- Approval labels/confirmation distinguish `Approve request` from legacy dry run
  and never claim execution.
- Receipt rows visibly name legacy, authorization, or execution kind and expose
  only the evidence links supplied by the server.
- Target/claim/recovery controls remain 008; no early UI action is added here.

## Gate

- API and 86-test baseline: pass.
- Decisions/blockers: none.
- Required proof: static semantic selectors, required/empty task, no fallback
  default, bridge grants, truthful approval copy, receipt kind/status/evidence,
  long text/narrow layout safeguards, and legacy behavior regression.
- Gate verdict: PASS.
