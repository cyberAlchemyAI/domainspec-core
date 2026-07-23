# Execution Pack

This file schedules owner-bound work. `WORK-PACK.md` and task files remain the
source of truth for tasks and SWUs.

| Wave | Layer | Question | Included tasks | Entry gate | Exit evidence |
| --- | --- | --- | --- | --- | --- |
| [W0](work-pack/waves/W0.md) | L0 | do known forbidden/false-ready states fail early? | 001-004 | dispatch and Distill pass; one selected SWU | DSS/TS/Invoke red-green receipts and conformant Inventory index |
| [W1](work-pack/waves/W1.md) | L1 | can evidence cross boundaries without ambient authority? | 005-007 | W0 closed; INV-1 and DSS-1 receipts available | readiness, option/override, sheet/overlay receipts |
| [W2](work-pack/waves/W2.md) | L2 | do runtime/read-model/status projections stay synchronized? | 008-010 | W1 closed; INT-1 conformant | Whisper parity, Inventory projection, Invoke status receipts |
| [W3](work-pack/waves/W3.md) | L3 | do all ten changes recompose without regression? | VERIFY | all task receipts | final audit and lifecycle-owner closeout |

Parallelization: none by default. A later owner may prove two validation-only
checks have disjoint writes, but this package never authorizes parallel
mutation.

For every stage:

1. owner accepts one task/SWU;
2. Context Builder creates execution-time evidence;
3. red fixture demonstrates the current bad state;
4. owner applies the bounded mutation;
5. focused and positive regressions run;
6. generated/read-model surfaces synchronize from their owner;
7. closure receipt updates the work-pack;
8. stop before the next SWU unless it is explicitly selected.
