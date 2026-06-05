# Repository Organization Invoke Plan

Date: 2026-05-27
Status: FLAG
Mode: distill -> invoke plan

## Distill Result

- Target context: `domainspec-core` as a multi-family workspace containing research programs, implementation/submodule references, validation harnesses, Arcanum lifecycle assets, reusable sigil/spell libraries, product/domain project folders, operational policy, and generated runtime state.
- Objective and output artifact: organize the repository through a governed invoke-plan artifact that can route into bounded execution without losing existing repository history.
- Mode and budget: Standard; one proposal track, Proposer/Balancer role simulation, two recursive rounds, reconciliation.
- Proposal tracks: one track, "Repository Zone Contract first".
- Recursive rounds: 2 / 2.
- Verdict: FLAG because the existing organization plan predates current top-level families and the working tree has unresolved git/submodule state.

## Discovery Baseline

Source refs:

- `README.md`: declares the original three-project operating model and canonical-path policy.
- `ops/REPOSITORY-ORGANIZATION-PLAN.md`: defines self-contained research projects, explicit dependencies, exports, and governance checks.
- `ops/ASSET-OWNERSHIP-POLICY.md`: defines Type A/B/C automation ownership and no-compatibility-alias policy.
- `.gitmodules`: currently declares `implementation/domainspec`, `validation/poker-team`, and `arcanum`.
- Current top-level scan: repo now includes `arcanum/`, `sigils-library/`, `cyberAlchemy/`, `docs/`, `projects/`, `research/`, `implementation/`, `validation/`, `ops/`, `tools/`, `.arcanum/`, `.codex/`, `.planning/`, `.data/`, and generated `output/`.
- Current git signal: modified `arcanum`, modified nested `implementation/domainspec`, untracked `projects/body-war/`, and a submodule status error for `research/projects/hermes-agent/repo` with no `.gitmodules` mapping.

Assumptions:

- The repo should keep canonical paths only; compatibility aliases are not a default solution.
- Existing project content should be classified before move/delete decisions.
- Arcanum assets are not merely research artifacts; they need their own capability/lifecycle zone.
- Product/domain project folders under `projects/` are first-class local project workspaces, not necessarily research projects.

## Role Conversation Trace

Proposer claim:

- The smallest coherent organizing unit is a repository zone contract, not a full file migration.
- Evidence: existing plans already define research containment, but newer top-level families are unclassified.

Balancer objection:

- Category: boundary ambiguity.
- The phrase "organize repository" could invite broad migration before deciding whether `projects/*`, `arcanum/`, `sigils-library/`, and `cyberAlchemy/` are source, research, validation, or runtime state.

Reconciliation:

- Accept objection.
- First execution layer creates a zone contract and admission checklist before moving files.
- Migration comes only after classification and owner decisions are recorded.

Proposer claim:

- The first actionable plan should classify zones, not normalize every folder.

Balancer objection:

- Category: hidden state risk.
- Existing dirty submodules and an unmapped nested repo can make mechanical migration unsafe.

Reconciliation:

- Accept objection.
- Add an L0 inventory and git-state task before any write-scope migration task.

## Current Smallest Coherent Unit

Unit name: Repository Zone Contract.

Responsibility:

- Define the canonical repository zones, admission rules, ownership model, generated-state policy, and migration decision checklist for every top-level family.

Inputs:

- Existing organization plan, asset ownership policy, README operating model, current tree inventory, `.gitmodules`, and git/submodule status.

Outputs:

- Updated organization plan or companion zone contract.
- Classification table for top-level directories.
- Gap ledger for unclassified or unsafe paths.
- Work-pack tasks for follow-on migrations.

## Optimization Point

The zone contract is the best size because it is small enough to complete without risky file movement, but large enough to recompose upward into the full repository organization model. Smaller units, such as "move `projects/body-war`" or "fix submodule mapping", do not carry the repository-level meaning. Larger units, such as "reorganize everything", smuggle migration before governance.

## Concept Layer Map

1. Repository operating model: why this workspace exists and how humans/agents enter it.
2. Repository zones: which families own source, research, validation, lifecycle assets, runtime state, and local projects.
3. Zone contract: rules for admission, ownership, dependency declaration, generated-state handling, and exits.
4. Directory classification table: current path -> zone -> owner -> action.
5. Migration tasks: bounded, reversible changes after classification.

## Technique Pack Trace

- abstraction-level guard: ran; selected repository-zone level instead of folder-by-folder cleanup.
- recomposition proof: ran; zone contract feeds README, ops policy, checks, and migration tasks.
- evolution profile: ran; repo is evolving from three-project workspace to multi-family lifecycle workspace.
- frame-expiry note: ran; plan expires if `arcanum`, `sigils-library`, or `projects/*` ownership changes.
- navigable result check: ran; next route is `task-session` on `SWU-ORG-001`.
- cognitive load check: triggered; current top-level shape is too broad for one migration batch.
- requisite variety check: triggered; research, product project, lifecycle capability, and runtime-state families need different rules.
- boundary-object check: triggered; zone contract is the shared object across README, ops, and execution.
- premortem pass: triggered; likely failure is moving files before resolving ownership and dirty submodule state.

## Closure And Recomposition Proof

Closure:

- The zone contract closes when every top-level path has a zone, owner, allowed dependencies, generated-state policy, and next action.

Recomposition:

- The contract updates `ops/REPOSITORY-ORGANIZATION-PLAN.md`.
- It refines `README.md` repository structure language.
- It extends `ops/ASSET-OWNERSHIP-POLICY.md` only where automation/lifecycle asset ownership is involved.
- It drives checks in `tools/check_research_structure.sh` or a new organization check only after classification is accepted.

## Evolution Profile

Expected evolution:

- More local product/domain projects under `projects/*`.
- More Arcanum lifecycle artifacts under `arcanum/`, `sigils-library/`, and `.arcanum/`.
- More research programs under `research/projects/*`.
- More generated observability and output state.

Smallest extension boundary:

- Add a top-level `zone_kind` taxonomy and `PROJECT.yaml`-style admission record for each first-class project family.
- Defer a full registry generator until the classification table stabilizes.

## Deferred Complexity

- No immediate file moves.
- No compatibility aliases.
- No automatic promotion of `projects/*` into `research/projects/*`.
- No cleanup of dirty submodules until a git-state decision is made.
- No generated-state untracking unless explicitly approved.

## Tension Ledger

Resolved:

- Organizing around zones beats organizing around a one-time migration.
- Research projects and product/domain projects need separate admission rules.
- Runtime/generated state must not be mixed with source-like artifacts.

Unresolved:

- Whether `cyberAlchemy/` is a local product/domain project, source archive, ontology workspace, or candidate Arcanum capability.
- Whether `sigils-library/` remains root-local or should be absorbed into `arcanum/`.
- Whether `projects/body-war/` should be admitted as a tracked project, ignored local scratch, or migrated into a separate repo.
- How to repair or remove `research/projects/hermes-agent/repo` from submodule expectations.

## Premortem

Likely failure reason:

- A broad cleanup moves files before ownership decisions are made, breaking hidden references or preserving the wrong source of truth.

Guardrail:

- Require the L0 classification table and git/submodule audit before migration writes.

## Frame-Expiry Note

This optimization point expires if the user decides that `domainspec-core` should become only an Arcanum workspace, only a research hub, or only a parent repository for submodules. Any of those changes would replace the zone contract with a narrower root purpose.

## Invoke Result

- Mode: plan.
- Spell: invoke.
- Phase status: FLAG.
- Mode contract: `arcanum/spells/invoke/plan.md`.
- Outputs: this file, `ops/REPOSITORY-ORGANIZATION-INVOKE-PLAN.md`.
- Implementation layering: inline L0-L3 below.
- Work-pack: single-file plan; split work-pack can be generated after L0 classification.
- Complexity: medium.
- Per-layer planning: L0, L1, L2, L3.
- Implementation detail: inline for each task.
- Smallest working units: complete for L0 and L1; later-layer SWUs are gated by classification outcome.
- Target artifact: repository organization plan and governance checks.
- Decisions: use Repository Zone Contract as the first coherent unit.
- Unresolved gaps: ownership decisions for `cyberAlchemy/`, `sigils-library/`, `projects/body-war/`, and `research/projects/hermes-agent/repo`.
- Next route: task-session.

## Implementation Layering

### L0: Classification Proof

Layer question:

- Can the repository be classified without moving files?

Promotion evidence:

- A classification table exists for every top-level directory.
- Dirty git and submodule risks are recorded.
- Unclassified paths are routed to explicit decisions.

Tasks:

- `TASK-ORG-001`: create repository zone contract and classification table.
- `TASK-ORG-002`: audit git/submodule state and classify unsafe migration blockers.

### L1: Policy Alignment

Layer question:

- Can the existing README, organization plan, and asset policy agree on the same zones?

Promotion evidence:

- `README.md`, `ops/REPOSITORY-ORGANIZATION-PLAN.md`, and `ops/ASSET-OWNERSHIP-POLICY.md` no longer contradict current repo shape.

Tasks:

- `TASK-ORG-003`: refresh operating-model docs from the accepted zone contract.
- `TASK-ORG-004`: add admission rules for `research/projects/*`, `projects/*`, `arcanum/`, `sigils-library/`, and generated state.

### L2: Governance Checks

Layer question:

- Can the repo detect future organization drift?

Promotion evidence:

- A check reports unclassified top-level paths, invalid project admission records, and generated-state leakage.

Tasks:

- `TASK-ORG-005`: extend or add organization validation.
- `TASK-ORG-006`: document check commands and expected failures.

### L3: Migration And Rollout

Layer question:

- Can classified paths be migrated, ignored, or promoted safely?

Promotion evidence:

- Each migration has an owner decision, write scope, verification command, and rollback note.

Tasks:

- `TASK-ORG-007`: execute approved path migrations or tracking changes.
- `TASK-ORG-008`: update workspace files and final navigation docs.

## Work-Pack

### SWU Manifest

| SWU | Parent task | Goal | Write scope | Verification |
| --- | --- | --- | --- | --- |
| `SWU-ORG-001` | `TASK-ORG-001` | Draft zone taxonomy and current top-level classification table | `ops/REPOSITORY-ORGANIZATION-PLAN.md` or companion under `ops/` | Review table against `find . -maxdepth 2 -type d` |
| `SWU-ORG-002` | `TASK-ORG-002` | Record dirty git/submodule blockers and repair options | companion under `ops/` | `git status --short`; `git submodule status` |
| `SWU-ORG-003` | `TASK-ORG-003` | Align README structure with accepted zones | `README.md` | Markdown link check where applicable |
| `SWU-ORG-004` | `TASK-ORG-004` | Add admission rules for new project/capability families | `ops/REPOSITORY-ORGANIZATION-PLAN.md`, `ops/ASSET-OWNERSHIP-POLICY.md` | Manual review against path examples |
| `SWU-ORG-005` | `TASK-ORG-005` | Add validation for unclassified top-level paths | `tools/` and/or existing check scripts | Run new or extended check |
| `SWU-ORG-006` | `TASK-ORG-006` | Document validation commands and known current failures | `README.md`, `ops/` | Commands copied from runnable scripts |
| `SWU-ORG-007` | `TASK-ORG-007` | Apply approved moves or tracking changes | approved paths only | `git status --short`; relevant checks |
| `SWU-ORG-008` | `TASK-ORG-008` | Finalize navigation and workspace entrypoints | `vscode-workspaces/`, `README.md`, `ops/` | Open workspace files or static review |

### Task Details

#### TASK-ORG-001: Repository Zone Contract

Objective:

- Define canonical zones for current repo families.

Suggested initial zones:

- `root-docs`: `README.md`, `docs/`, `.planning/`.
- `ops-governance`: `ops/`, `tools/`, `.githooks/`, `.github/`.
- `research-programs`: `research/projects/*`, `research/shared/`, `research/registry/`.
- `implementation-sources`: `implementation/*`.
- `validation-harnesses`: `validation/*`.
- `arcanum-lifecycle`: `arcanum/`, `.arcanum/`, `.codex/commands`.
- `reusable-capability-library`: `sigils-library/`.
- `local-product-projects`: `projects/*`.
- `legacy-or-candidate-workspace`: `cyberAlchemy/` until owner decision.
- `generated-runtime-state`: `.data/`, `output/`, `.arcanum/observability/*` where generated.

Done criteria:

- Every top-level path is classified or explicitly marked unresolved.

#### TASK-ORG-002: Git And Submodule Audit

Objective:

- Prevent organization work from trampling unresolved submodule or user changes.

Current known blockers:

- `arcanum` modified.
- `implementation/domainspec` modified inside nested checkout.
- `projects/body-war/` untracked.
- `research/projects/hermes-agent/repo` appears as nested git state without `.gitmodules` mapping.

Done criteria:

- Each blocker has one of: preserve, ignore, repair mapping, remove from index, migrate, or ask user.

#### TASK-ORG-003: README Alignment

Objective:

- Update the root README from "unified 3-project workspace" to the accepted current zone model while preserving the historical three-project model as a core lane, not the whole repo.

Done criteria:

- README gives a newcomer a correct first-screen map of the repo.

#### TASK-ORG-004: Admission Rules

Objective:

- Add rules for when a folder belongs under `research/projects/*`, `projects/*`, `arcanum/`, `sigils-library/`, or `implementation/*`.

Done criteria:

- A new project can be admitted without guessing where it belongs.

#### TASK-ORG-005: Organization Check

Objective:

- Make the classification auditable.

Check behavior:

- fail on unclassified top-level paths,
- flag project folders without required admission metadata,
- flag generated-state paths that are tracked without policy,
- flag research project nested repos unless explicitly declared.

Done criteria:

- A command gives PASS/FLAG/BLOCK output.

#### TASK-ORG-006: Validation Documentation

Objective:

- Document how to run organization checks and how to interpret expected current failures.

Done criteria:

- README or ops docs include the command and known failure explanation.

#### TASK-ORG-007: Approved Migration

Objective:

- Execute only migrations approved after L0-L2.

Done criteria:

- No move occurs without owner, source path, target path, verification, and rollback note.

#### TASK-ORG-008: Navigation Closeout

Objective:

- Make workspaces and navigation docs reflect the accepted zone model.

Done criteria:

- Workspace files and quick links route users to the right zone.

## Validation Strategy

L0:

- `find . -maxdepth 2 -type d | sort`
- `git status --short`
- `git submodule status`

L1:

- `tools/check_markdown_links.sh` against edited markdown files, one file at a time.

L2:

- New or extended organization check command.
- Existing drift checks where relevant: `tools/check_github_drift.sh`.

L3:

- `git status --short`
- targeted checks for moved/edited areas.

## Navigation Guide

Start here:

- Run `SWU-ORG-001` as the first task-session unit.

Do not start with:

- Moving files.
- Cleaning generated state.
- Repairing submodules.
- Updating README prose before the classification table exists.

Use this result as:

- the planning baseline for a `task-session` run,
- the replacement candidate for the stale parts of `ops/REPOSITORY-ORGANIZATION-PLAN.md`,
- the decision map for repository organization gates.

