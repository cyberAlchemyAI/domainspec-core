---
module: ide-extension-open-poll-bridge
version: current
status: planned
updatedAt: 2026-07-16
docType: plan-transport
---

# Plan Transport

## Task Session Entry

Use this handoff when starting execution:

```text
Execute SWU-OPB-001 from projects/ide-extension/development/open-poll-bridge-plan/WORK-PACK.md.
Keep the active layer at L0. Do not add a queue, background poller, lease,
worker registry, provider adapter, mutation executor, or IDE/browser control.
Return a structured Task Session result and update only the selected SWU status.
```

## Core Acceptance Claim

The work is done only when the bridge proves:

```text
ready is open availability; claim binds identity; result preserves stored claim identity.
```

## Current First SWU

- ID: `SWU-OPB-001`
- Parent: `TASK-CONTRACT-IDENTITY`
- Goal: add schema fixtures for open ready and claim-bound `agent_ref`.
- Validation: schema validation plus focused contract assertions.
