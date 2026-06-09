# Personal Codex Skill Refresh Decision

Date: 2026-05-31
Status: accepted
Decision source: `decision-gate` before `TASK-SURFACE-002 / SWU-SURFACE-002`

## Blocked Work

`TASK-SURFACE-002` refreshes the machine-global Codex skill surface at:

```text
/mnt/c/Users/vlad_/.codex/skills/*
```

This is consequential because it changes the active Codex skill surface outside the repository checkout. The accepted install profile contract requires `personal-codex` to be explicit and never included in repository-local `all`.

## Decision Question

How should this run handle the personal Codex skill refresh?

## Options

### Option 1: Stage Only

Generate the `personal-codex` output into a repository-local or temporary staging folder, compare it against the active personal skills, and stop before mutating `/mnt/c/Users/vlad_/.codex/skills`.

Benefit: safest review path; no global runtime mutation.

Cost or risk: active Codex skills remain stale until a later approval.

Choose when: the priority is auditability and avoiding machine-global changes in this task session.

Downstream impact: `TASK-SURFACE-002` can produce a diff/report, but promotion remains blocked.

### Option 2: Stage Then Promote

Generate the `personal-codex` output into staging, compare it, then replace the active personal Arcanum skill packages and aliases in `/mnt/c/Users/vlad_/.codex/skills`.

Benefit: finishes the actual active Codex surface cleanup now.

Cost or risk: mutates machine-global Codex state; a bad generated package would affect later Codex sessions until corrected.

Choose when: the current canonical generator is trusted enough and the user wants the active runtime updated in this run.

Downstream impact: `TASK-SURFACE-002` may continue through promotion and validation.

### Option 3: Do Not Touch Personal Codex

Skip `TASK-SURFACE-002` for now and move to repository-local GitHub/Copilot or `.arcanum` cleanup.

Benefit: avoids global mutation and avoids spending time on a surface that may need broader runtime packaging decisions.

Cost or risk: personal Codex stays known-stale, so native-first behavior remains only documented, not fully reflected in the active user runtime.

Choose when: the next priority is repo shape rather than active personal Codex behavior.

Downstream impact: `TASK-SURFACE-002` remains blocked; next task should be `TASK-SURFACE-003` or `TASK-SURFACE-004`.

## Selected Option

Option 2: Stage Then Promote.

## Rationale

The user explicitly selected option 2 in the follow-up request:

```text
[$invoke] refresh 2
```

This authorizes `TASK-SURFACE-002` to stage the generated `personal-codex` skill packages, compare them against the active personal Codex skill surface, and then promote the reviewed generated Arcanum packages and aliases into `/mnt/c/Users/vlad_/.codex/skills`.

## Remaining Blockers

None for starting `TASK-SURFACE-002`.

## Deferred Decisions

- Whether to archive superseded personal skill packages after promotion.

## Assumptions

- Repository-local staging is allowed.
- Active personal Codex mutation is allowed for this task session after staging and review.
- Promotion should be limited to Arcanum-generated skill packages and aliases; unrelated personal or system skills remain out of scope.
