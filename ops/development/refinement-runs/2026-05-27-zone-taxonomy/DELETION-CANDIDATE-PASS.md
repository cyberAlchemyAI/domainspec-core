# Deletion Candidate Pass

Date: 2026-05-27
Target: repository organization cleanup candidates
Status: review-required

## Purpose

This pass corrects the prior zone taxonomy after user clarification that `sigils-library/` was the first name of Arcanum. The repository shape should not preserve obsolete names as independent zones when their content is superseded by a canonical home.

No files were deleted in this pass.

## Deletion Classes

| Class | Meaning | Default action |
| --- | --- | --- |
| `superseded-name` | Old name for a now-canonical folder or concept. | Delete after verifying unique content is preserved or intentionally abandoned. |
| `generated-state` | Runtime output, telemetry, caches, databases, or generated projections. | Untrack or ignore unless explicitly promoted to evidence/source. |
| `duplicate-install` | Installed copy of a capability whose canonical source is elsewhere. | Keep only if it is the intended install target; otherwise regenerate from source. |
| `one-off-output` | Presentation/export/demo artifact without current source ownership. | Move to owner folder or delete after preservation review. |
| `nested-repo-drift` | Embedded git repo or submodule-like path without declaration. | Repair mapping, promote to submodule, or remove from tracked tree. |

## High-Confidence Retirement Candidates

### `sigils-library/`

Verdict: delete candidate after preservation review.

Reason:

- User clarified it was the first name of Arcanum.
- It contains only 8 tracked files.
- Its current concept taxonomy (`formulae`, `transmutations`, `arcana`) now exists canonically under `arcanum/`.
- Root references are limited and can be updated: `vscode-workspaces/sigils-library.code-workspace`, `vscode-workspaces/README.md`, and the prior organization artifacts from this refinement pass.

Preservation check:

- `sigils-library/arcana/robot-talks/SKILL.md` has a canonical counterpart at `arcanum/arcana/robot-talks/SKILL.md`.
- `sigils-library/transmutations/implementation-layering/templates/implementation-layering.md` has a canonical counterpart at `arcanum/transmutations/implementation-layering/templates/implementation-layering.md`.
- `sigils-library/transmutations/implementation-layering/SKILL.md` differs from `arcanum/transmutations/implementation-layering/SKILL.md`, so review before deletion.
- `sigils-library/README.md` references missing files such as `REGISTRY.md`, `spells/`, `QUALITY-BAR.md`, and `ANTI-PATTERNS.md`; this supports retirement rather than active ownership.

Recommended action:

1. Diff the differing implementation-layering skill.
2. If no unique value remains, delete `sigils-library/`.
3. Delete `vscode-workspaces/sigils-library.code-workspace`.
4. Remove the Sigils Library row from `vscode-workspaces/README.md`.
5. Rewrite organization artifacts to say Arcanum is the canonical successor.

## Medium-Confidence Cleanup Candidates

### `.data/`

Verdict: untrack candidate.

Reason:

- Contains tracked SQLite projection files: `.sqlite`, `.sqlite-shm`, `.sqlite-wal`.
- These are generated runtime/data artifacts, not source-like repository policy.

Recommended action:

- Preserve locally.
- Add ignore rule.
- Use `git rm --cached` only after explicit approval.

### `output/`

Verdict: ignore/generated candidate.

Reason:

- No tracked files found in the current pass.
- It is an output folder by name and should stay untracked unless a specific artifact is intentionally published.

Recommended action:

- Add ignore rule if not already covered.

### `.arcanum/observability/*`

Verdict: split policy needed.

Reason:

- The root `.arcanum/` contains both source-like install/config artifacts and append-only/generated telemetry.
- Tracked JSONL and reflection state under observability are generated state unless promoted as evidence.

Recommended action:

- Keep source-like README/config/schema/placeholder files where needed.
- Untrack generated JSONL/state files after explicit approval.

### `projects/*/.arcanum/` and `projects/*/.github/skills/`

Verdict: duplicate-install review.

Reason:

- `projects/sonar-loop/` tracks many installed Arcanum runtime and GitHub Copilot skill copies.
- These may be intentional per-project fixtures, but they look like generated/install output from the canonical Arcanum package.

Recommended action:

- Add project admission metadata that states whether installed runtime files are source, fixture, or generated install output.
- If generated install output, untrack and regenerate when needed.

## Decision-Gated Candidates

### `cyberAlchemy/`

Verdict: do not delete without a separate decision.

Reason:

- Contains 56 tracked files including source-like ontology docs, HTML presentations, assets, and PDF output.
- Memory and local docs suggest it has been used as a pilot and knowledge workspace.

Recommended action:

- Classify as one of:
  - `knowledge-project`,
  - `presentation/archive bundle`,
  - `Arcanum ontology pilot source`,
  - `external repo candidate`,
  - `delete/archive`.

### `research/projects/hermes-agent/repo`

Verdict: repair before cleanup.

Reason:

- `git submodule status` reports: no submodule mapping found in `.gitmodules` for this path.
- It is a nested repo-like path under a research project.

Recommended action:

- Decide whether it is:
  - a declared submodule,
  - vendored source,
  - research source snapshot,
  - local scratch that should not be tracked.

### `projects/body-war/`

Verdict: untracked project admission decision.

Reason:

- It is currently untracked.
- It may be valid incubator work, but should not become part of repository shape accidentally.

Recommended action:

- Decide `tracked-project`, `scratch/local`, `future-repo`, `future-research`, or `archive/delete`.

### `robot-talks-complete-guide.md`

Verdict: root-doc cleanup candidate.

Reason:

- It is a tracked top-level guide, while root docs should generally live under `docs/` or the owning capability.
- It may belong under `arcanum/arcana/robot-talks/`, `docs/`, or be retired if superseded.

Recommended action:

- Compare with `arcanum/arcana/robot-talks/` docs before moving or deleting.

## Revised Best Repository Shape

The best shape should be stricter than the previous synthesis:

```text
domainspec-core/
  README.md
  docs/
  ops/
  tools/
  vscode-workspaces/

  implementation/
  research/
  validation/

  arcanum/                       # canonical Arcanum successor to sigils-library
  projects/                      # admitted incubator projects only
  cyberAlchemy/                  # decision-gated until classified

  .github/ .codex/ .agents/ .planning/
  .arcanum/                      # install/config plus local generated state by policy
```

Removed as independent canonical zones:

- `sigils-library/`
- generic `capability-library`

New rule:

- A top-level folder is not canonical just because it is meaningful. It must be current, named correctly, and have no newer canonical successor.

## Proposed Immediate Work-Pack Update

1. Add `TASK-ORG-000`: deletion-candidate audit before zone contract.
2. Update `TASK-ORG-001` so `sigils-library/` is classified as `superseded-name`, not `capability-library`.
3. Add `TASK-ORG-009`: remove approved retired paths and workspace references.
4. Add `TASK-ORG-010`: untrack approved generated/runtime state while preserving local files.

