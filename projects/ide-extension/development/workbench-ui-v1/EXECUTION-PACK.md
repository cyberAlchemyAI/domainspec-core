# Workbench UI V1 Execution Pack

Execute one SWU per Task Session in this order:

```text
SWU-WUI-001 -> SWU-WUI-002 -> SWU-WUI-003 -> SWU-WUI-004
  -> SWU-WUI-005 -> SWU-WUI-006 -> SWU-WUI-007
  -> SWU-WUI-008 -> SWU-WUI-009 -> SWU-WUI-010 -> SWU-WUI-011
```

`SWU-WUI-006` and `SWU-WUI-007` may run in parallel after `SWU-WUI-005` only
when their exact write scopes are disjoint or a merge owner is named. The
default route remains sequential.

Each result must report the SWU id, files touched, validation, blockers,
residue, and next route. Synchronize `WORK-PACK.md` and the owning Craft context
after every pass, flag, block, or interruption. Preserve unrelated worktree
changes and do not execute a dependent SWU before its predecessor passes.
