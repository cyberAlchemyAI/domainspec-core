# Events: Capital Logic Library

## RulePackMarkedStale

Announces that a registered rule pack has aged past its `next_review_due` and now
requires re-review. Decay is computed, not asserted — this event makes the ONGOING
maintenance marker auditable.

**Produced by:** [RegisterRulePack](operations.md#registerrulepack)
**Triggers transition:** [RulePackLifecycle](states.md#rulepacklifecycle)

### Payload

| Field           | Type           | Description                              |
| --------------- | -------------- | ---------------------------------------- |
| rule_pack_id    | string         | The pack that went stale                 |
| next_review_due | date           | The due date that elapsed                |
| computed_at     | date           | The `now` value used by StalenessComputation |
| maintainer_role | string         | Who owns the re-review                   |

### Consumed By

| Consumer                          | Action                                            |
| --------------------------------- | ------------------------------------------------- |
| Capital Logic Library maintainer  | Schedule re-review of the funder/program RFA       |
| Logician (deterministic gates)    | Treat stale pack's requirements as needing refresh |
