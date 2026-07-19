---
module: ide-extension-open-poll-bridge
version: current
status: planned
updatedAt: 2026-07-16
docType: invoke-plan-index
---

# Open Poll Bridge Plan

This package turns the refresh finding into an executable L0 work-pack.

The plan preserves the existing manual session bridge shape, but changes the
availability model:

- `ready` is caller-neutral availability, not a Codex-targeted selector.
- `claim` binds the real `agent_ref`.
- `result` and receipts derive identity from the stored claim, not from a
  default or caller-supplied terminal field.
- the workbench and CLI stop teaching operators that "polling type" selects who
  can see work.

## Artifacts

- [IMPLEMENTATION-LAYERING.md](IMPLEMENTATION-LAYERING.md)
- [WORK-PACK.md](WORK-PACK.md)
- [EXECUTION-PACK.md](EXECUTION-PACK.md)
- [PLAN-TRANSPORT.md](PLAN-TRANSPORT.md)
- [DISTILL-VALIDATION.md](DISTILL-VALIDATION.md)
- [open-poll-bridge-plan.dispatch.json](open-poll-bridge-plan.dispatch.json)
- [INVOKE-RESULT.md](INVOKE-RESULT.md)

Start execution with `SWU-OPB-001`.
