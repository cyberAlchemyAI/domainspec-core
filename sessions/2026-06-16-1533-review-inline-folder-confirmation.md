---
tags: [subagents-dispatch, review, working-folder, constitution, governance]
node_type: constitution
is_session: true
layer: architecture, governance
nature: procedural, technical
status: active
created: 2026-06-16
timestamp: 2026-06-16T15:33:38-03:00
expires: 2026-08-15
conversation_id: 2026-06-16-review-inline-folder-confirmation
decisions_made: true
contradictions_found: false
specs_updated: [internal_tools/subagents-dispatch-hooks/constitution/subagents-strategy-constitution-proposal.md, internal_tools/subagents-dispatch-hooks/skills/review/SKILL.md, internal_tools/subagents-dispatch-hooks/skills/register-dispatch/SKILL.md, internal_tools/subagents-dispatch-hooks/skills/register-dispatch/append-dispatch.cjs, internal_tools/subagents-dispatch-hooks/skills/domainspec-subagents-strategy/SKILL.md]
promoted_candidates: []
expected_importance: 6
importance_rationale: "Changes review's output contract and adds a universal artifact-destination gate across constitution, appender code, and the dispatch skill chain."
---

# Review goes inline + universal folder confirmation (v0.6.2)

## Summary

Owner decision to make `dispatch_type: review` inline by default — its cited change-request report is delivered in chat, the mandated `attacks.md`/`findings.md` pair removed, and `working_folder` made optional for review. Coupled with a universal rule that any dispatch saving artifacts must confirm the `working_folder` (or inline) with the human at the P2 gate. Landed full-chain: appender (`WORKING_FOLDER_TYPES = {research, experiment}`, review stays LIVE), the three SKILLs, constitution §5 + new §13 (doc 0.6.1→0.6.2, wire schema stays 0.6.0), and regression tests 10j/10k — battery 83/0. Discovered `.claude/skills` had drifted ahead of the `internal_tools/` source; reconciled by porting `.claude` into source, then ran the installer as a verified no-op.

## Next Steps

- Commit the working tree submodule-aware (run `make bump-check`); nothing committed yet.
- Decide whether the submodule vendored copy `implementation/domainspec/internal_tools/subagents-dispatch-hooks/` should track the parent hooks package (still on old behavior).
- Restart Claude Code sessions to pick up the reinstalled global hooks/skill.

## Open Questions

- The `install.cjs` "single source of truth" model is stale — `.claude/` was ahead of source. Should the source→generated flow be fixed or formally reversed? (see `internal_tools/subagents-dispatch-hooks/install.cjs`)
- Does `register-dispatch` runtime use the project `.claude` copy (`$CLAUDE_PROJECT_DIR`) or the global `~/.claude` copy (`$HOME`)? The two diverge on the appender path.

## Files touched

- internal_tools/subagents-dispatch-hooks/constitution/subagents-strategy-constitution-proposal.md
- internal_tools/subagents-dispatch-hooks/skills/register-dispatch/append-dispatch.cjs
- internal_tools/subagents-dispatch-hooks/skills/register-dispatch/SKILL.md
- internal_tools/subagents-dispatch-hooks/skills/review/SKILL.md
- internal_tools/subagents-dispatch-hooks/skills/domainspec-subagents-strategy/SKILL.md
- internal_tools/subagents-dispatch-hooks/skills/{research,experiment,check-tension}/SKILL.md
- internal_tools/subagents-dispatch-hooks/skills/robot-talks/README.md
- internal_tools/subagents-dispatch-hooks/tests/test-append-dispatch.cjs
- .claude/skills/{review,domainspec-subagents-strategy,register-dispatch}/ (synced)
