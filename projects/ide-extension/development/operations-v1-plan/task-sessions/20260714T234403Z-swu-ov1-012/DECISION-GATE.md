# Decision Gate: Durable Automatic Pruning Completion

```yaml
decision_id: DEC-IDEEXT-OV1-PRUNING-COMPLETION
status: selected
blocking: false
scope: SWU-OV1-012
selected_option: 1
selected_at: 2026-07-15T00:24:31Z
source: user reply "1"
```

## Decision

How should automatic retention durably close an active grace request when
temporary/orphan cleanup alone brings storage below soft and no revision was
pruned?

## Option 1: Add `canvas.pruning_completed` To V4 - Recommended

Add a seventh V4 event through an explicit migration. The event binds the
active pruning request, automatic trigger, reclaimed orphan/temporary bytes,
final total bytes, and completion timestamp. The projector accepts it only when
the request is active and final bytes are below that request's soft limit, then
sets `state: normal` and `active_request: null`.

This tells the truth about what happened, replays deterministically, supports
orphan-only recovery, and keeps revision tombstones reserved for actual
revision pruning. It requires contract, projector, replay, and migration tests.

## Option 2: Make `canvas.revision_pruned` A Completion Union

Allow the existing event name to carry either a revision tombstone or a
cleanup-only completion record. This avoids a seventh name but turns one exact
event shape into a discriminated union and makes “revision pruned” false when
only an orphan was deleted.

This is more confusing and changes more of the existing replay contract than a
new additive event.

## Option 3: Keep The Request Sticky And Derive Normal From Disk

Leave `active_request` durable forever and let diagnostics display Normal when
physical bytes are below soft. This avoids an event migration, but restart still
replays the expired request and the next threshold crossing skips a fresh grace
window. It violates durable-state truth and is not recommended.

## Option 4: Narrow SWU-012 And Exclude Orphan-Only Convergence

Only auto-prune when at least one historical revision is eligible. This keeps
the six-name vocabulary but fails the planned orphan-only recovery edge and the
selected orphan-first algorithm.

## Recommendation

Select Option 1. It is the smallest honest additive transition and preserves
the exact meaning of every existing V4 event.

## Selection

The user selected Option 1. SWU-OV1-012 may resume under an explicit additive
V4 migration. No blockers remain in this Decision Gate.

## Decision Gate Result

- Result: PASS
- Decisions resolved: 1
- Blockers remaining: 0
- Selected option: Add `canvas.pruning_completed` to V4
- Migration evidence: `../20260715T002431Z-swu-ov1-012-resume/EVENT-V4-MIGRATION.md`
- Next step: resume SWU-OV1-012
