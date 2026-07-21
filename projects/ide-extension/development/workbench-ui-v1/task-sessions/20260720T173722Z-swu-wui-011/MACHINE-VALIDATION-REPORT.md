# WUI V1 Machine Validation Report

```yaml
swu_id: SWU-WUI-011
machine_result: pass
human_usefulness_verdict: pending
promotion_result: blocked_on_human
validated_at: 2026-07-20
```

## Machine Matrix

- Integrated Workbench UI and Operations desktop/mobile browser matrix: **16/16
  passed**.
- Desktop Work, Canvas, and Inspector shell geometry: **1/1 passed**.
- Mobile Work, Canvas, and Evidence navigation: **1/1 passed**.
- Scoped bridge and L0 Node regression suite: **68/68 passed**.
- WUI-010 retained receipt Inspector witness: **2/2 passed**.
- WUI-009 Craft selection and no-write witness: **2/2 passed**.
- Scoped `git diff --check`: **pass**.
- Craft ledger/index YAML, JSON, and digest projection: **pass**.

## Behaviors Covered

- Explicit Agent task and Dry run modes remain distinct.
- Craft selection seeds Task and Context without changing Craft state.
- Canvas output remains primary, retains revision identity, and preserves the
  last good frame after failed navigation.
- Lifecycle stages and legal actions remain truthful through terminal receipt.
- Authorization and execution receipts remain distinct and attributable to one
  envelope, run, and approval.
- Ready-only polling remains opaque before claim.
- Desktop and mobile views remain reachable without overlap or horizontal
  overflow.

## Retained Evidence

- [Canvas desktop/mobile](../20260720T165903Z-swu-wui-008/TASK-SESSION-RESULT.md)
- [Craft desktop/mobile](../20260720T170841Z-swu-wui-009/TASK-SESSION-RESULT.md)
- [Inspector desktop/mobile](../20260720T172635Z-swu-wui-010/TASK-SESSION-RESULT.md)
- [Prior lifecycle/action and shell evidence](../20260720T164437Z-swu-wui-007/TASK-SESSION-RESULT.md)

## Blocker

The machine evidence does not answer whether the composed Workbench UI V1 is
useful enough to become the default screen. `TASK-WUI-005` explicitly requires
an operator usefulness verdict and prohibits self-approval from green tests.
V1 remains unpromoted and the Work Pack remains open until that verdict is
recorded.

## Boundary

This report does not claim provider execution, browser control, worker wake-up,
VSCodium embedding, or an autonomous IDE agent. Those remain separate gaps and
are outside the V1 validation gate.
