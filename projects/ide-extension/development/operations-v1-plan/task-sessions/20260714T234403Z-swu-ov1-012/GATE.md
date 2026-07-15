# Task Gate: SWU-OV1-012

```yaml
swu_id: SWU-OV1-012
verdict: block
blocking_decisions:
  - DEC-IDEEXT-OV1-PRUNING-COMPLETION
dependency: SWU-OV1-011 pass
runtime: local
```

## Blocking Condition

Automatic orphan-only cleanup can converge below soft without emitting a
revision tombstone. The current V4 contract has no event that can close the
active pruning request in that case.

## Stop Conditions Applied

- Do not fabricate a revision tombstone when no revision was pruned.
- Do not clear durable projection state through filesystem-derived mutation.
- Do not report Normal while replay still projects Grace/Reclaiming.
- Do not expand the human-confirmed six-name V4 vocabulary without a recorded
  migration decision.
