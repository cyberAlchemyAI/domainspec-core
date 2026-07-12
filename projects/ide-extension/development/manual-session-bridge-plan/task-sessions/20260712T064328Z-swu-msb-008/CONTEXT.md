# Context Pack: SWU-MSB-008

- Task/SWU: `TASK-HUMAN-WORKBENCH / SWU-MSB-008`
- Dependencies: 006 one-shot protocol and 007 truthful workbench complete
- Sources: approved UX state model, Human Workbench task contract, current
  bridge APIs/projector, workbench UI and focused tests
- Runtime: local Codex; no delegation

## Boundaries And Decisions

- Browser controls only operator-owned ready, unready, reject/revoke, and
  release/requeue transitions; claim, interrupt, and result remain session-owned.
- Queue and detail status follow envelope typestate, not authorization state.
- The singleton ready target is visible globally and never silently replaced.
- Claims are explicitly unattested and attempt/session handles remain inspectable.
- Release requires a human-entered reason and returns to approved; a fresh ready
  action is required.
- Terminal result, validation, evidence references, and execution receipt remain
  visible beside the authorization receipt.

## Gate

- Kernel singleton/recovery actor tests: pass.
- Workbench truthfulness and session protocol: pass.
- Decisions/blockers: none.
- Gate verdict: PASS.
