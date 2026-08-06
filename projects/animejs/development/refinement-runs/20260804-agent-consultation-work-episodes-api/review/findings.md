# Design Review Findings

Verdict: `FIX`

The review dispatch is resolved because both requested attacks completed with finite repairs. The reviewed draft remains blocked until Stage 08 incorporates them.

## Ordered repair set

| Priority | Repair |
| --- | --- |
| 1 | Close a neutral-projection allowlist and compiler manifest; expose only safe opaque handles and approved fields. |
| 2 | Hard-bind separate route/credential audiences before parsing bodies; mixed or read grants cannot select append effects. |
| 3 | Bind every episode to principal, workspace/tenant, vault, Task, VersionContext, capability audience, and optional host-issued delegation. |
| 4 | Dereference Task and VersionContext once at open; store immutable canonical snapshots/digests; reject reserved inline fields. |
| 5 | Keep episode material in an isolated rebuildable overlay with closed episode-owned kinds/relations/effects and namespace separation. |
| 6 | Keep only `open_episode` with optional `supersedes_episode_id`; add overlay-only cycle-checked supersession and never emit canonical `AKV-REL-022`. |
| 7 | Bind evidence to its producer episode/attempt/task/version/criterion/class/scope; attach before outcome only and reject rebinding. |
| 8 | Freeze the episode's opening graph digest and define later source changes as applicability overlays. |
| 9 | Close outer status, diagnostic code, receipt recovery, reducer-version, snapshot-key, projection pending/failure/corruption, and quarantine contracts. |
| 10 | Every append/read result declares `semantic_effect=none`, `task_state_unchanged=true`, and `truth_status=not_assessed`; closing creates zero Lessons. |

## Boundary

No fixture executed, no source or vault bytes changed, and no implementation, deployment, promotion, release, or production evidence exists.
