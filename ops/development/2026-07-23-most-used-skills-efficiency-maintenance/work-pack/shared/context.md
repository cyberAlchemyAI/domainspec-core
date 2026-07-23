# Shared Context

## Authority order

1. live canonical lifecycle source and explicit private owner source;
2. accepted review findings;
3. this Define/Design/Plan package;
4. generated runtimes and Inventory as read models only.

## Required sources

- `../../DEFINE.md`
- `../../DESIGN.md`
- `../../../2026-07-22-most-used-skills-efficiency-review/findings.md`
- `../../../2026-07-22-most-used-skills-efficiency-review/attacks.md`
- current exact source anchors named by each task

## Global constraints

- one selected SWU at a time;
- no private prose in public Arcanum;
- canonical source before generated surface;
- no approval bypasses validation;
- no validation implies promotion;
- preserve unrelated dirty-worktree changes;
- generated execution-time context belongs under session evidence, not beside
  this canonical plan.

## Closure receipt shape

```yaml
swu_id: SWU-WFE-xxx
result: pass | flag | block | interrupted
capability_ref: lifecycle owner
receipt_kind: native-stage | subagent | local-fallback | blocked
receipt_artifact: path | none
files_touched: []
validation: []
blockers: []
residue: []
reroute: owner | none
handoff_note: string
```
