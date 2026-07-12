# Execution Pack: V0 Canvas Repair

## Choreography

```text
W0 policy contract
  -> W1 canonical admission
  -> W2 adversarial regression
  -> W3 integrated closeout
```

The path task cannot start before the policy task closes because adding an
approval subsystem would contradict the selected trusted-local repair.

## Wave Map

| Wave | Layer | Tasks | SWUs | Entry gate | Exit evidence |
| --- | --- | --- | --- | --- | --- |
| W0 | L0 | Canvas policy | 001 | Accepted review and design refs exist. | Policy clauses agree and no runtime files change. |
| W1 | L1 | Path admission | 002 | 001 pass. | Helper and server mappings reject external canonical targets. |
| W2 | L2 | Path admission | 003 | 002 pass. | Adversarial and compatibility tests pass. |
| W3 | L3 | Verify | 004 | 003 pass. | Integrated evidence and work-pack state synchronize. |

## Parallelism

None. The work is intentionally sequential and small. Each Task Session owns
one SWU and returns the standard result shape from `WORK-PACK.md`.

## Execution Receipt Handoff

Each SWU result must include:

- exact files touched;
- commands and counts/results;
- whether any unrelated worktree changes intersected write scope;
- blocker or residue;
- next ready SWU;
- evidence path for status synchronization.

## Stop Conditions

- Stop if policy cannot distinguish preview/display from protected effects.
- Stop if the implementation admits an external canonical target.
- Stop if a fix requires changing V0 request schema or surface identity.
- Stop if tests can pass only by weakening path normalization.
- Stop before any Operations V1 implementation.
