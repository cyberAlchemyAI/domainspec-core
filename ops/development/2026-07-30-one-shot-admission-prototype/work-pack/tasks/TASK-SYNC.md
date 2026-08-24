# TASK-SYNC

## SWU-OAP-007 — Sync WPRA generated package

- Primary behavior: regenerate and sync only `work-pack-readiness-audit`.
- Dependencies: OAP-002 and OAP-006.
- Write scope: `.agents/skills/work-pack-readiness-audit/**` and
  `.claude/skills/work-pack-readiness-audit/**`.
- Command:
  `arcanum/tools/sync-generated-skill-package.sh --target . --spell work-pack-readiness-audit --profiles repo-codex,claude --apply`
- Done: staged comparison and post-sync parity pass.

## SWU-OAP-008 — Sync chain generated package

- Primary behavior: regenerate and sync only `task-session-until-blocker`.
- Dependencies: OAP-005 and OAP-006.
- Write scope: `.agents/skills/task-session-until-blocker/**` and
  `.claude/skills/task-session-until-blocker/**`.
- Command:
  `arcanum/tools/sync-generated-skill-package.sh --target . --spell task-session-until-blocker --profiles repo-codex,claude --apply`
- Done: staged comparison and post-sync parity pass.

Never run partial repository bootstrap with `repo-codex`.
