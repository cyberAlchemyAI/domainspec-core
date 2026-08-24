# Runtime Handoff — Awaiting Strategy Permission

- Dispatch: `REFINE-DISPATCH.json`
- Runtime objective: execute the canonical ten-stage Refine loop for the UOVARR-003 reference/digest contradiction
- Authorization: `requires_user_permission`
- Runtime status: blocked before native stages and subagent spawning
- Proposed subagents: two bounded read-only analysts
- Join policy: all; every spawned agent must return a receipt and reach terminal join and close state
- External research: local-first; a named gap requires separate confirmation
- Product mutation: forbidden

No adapter or runtime-backed capability has been dispatched. On confirmation, Refine must record permission, identify each native capability handle and expected receipt, then run the stages in the validated order.

