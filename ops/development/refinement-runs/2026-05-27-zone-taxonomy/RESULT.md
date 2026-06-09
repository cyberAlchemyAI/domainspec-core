# Refine Result: Repository Zone Taxonomy

Date: 2026-05-27
Target: repository zone taxonomy and best repository shape
Status: FLAG
Preset: standard
Research: research-if-gap-appears; no external research run

## Final Synthesis

The best shape for `domainspec-core` is not a pure research repository anymore. It should be treated as a governed workspace with a small stable core and a few explicit satellite zones.

Update after deletion-candidate pass:

- `sigils-library/` should not be preserved as an independent canonical zone. User clarification says it was the first name of Arcanum, so it is now a `superseded-name` deletion candidate.
- The previous `capability-library` zone should be removed unless a future root-local capability library is deliberately created under a current name.
- The taxonomy should include a cleanup gate before zone-contract implementation.

Update after runtime-surface invoke pass:

- Runtime surfaces need their own layer. Codex global commands, Arcanum repo commands, DomainSpec repo-local commands, GitHub Copilot skill installs, `.arcanum` runtime state, and project-local installed copies should not be treated as ordinary source folders.
- Add `runtime-surface` policy before cleanup execution so canonical source, installed surface, generated runtime state, and local/private state are separated.

Recommended shape:

```text
domainspec-core/
  README.md
  docs/                         # root orientation, glossary, registry, shared governance notes
  ops/                          # repository organization, ownership, drift policy, work-packs
  tools/                        # root governance and drift checks
  vscode-workspaces/            # operator entrypoints

  implementation/               # implementation source references and submodules
    domainspec/
    mars/

  research/                     # self-contained research programs
    projects/
    shared/
    registry/

  validation/                   # validation harnesses and runtime case studies
    poker-team/
    sigil-spell-sandbox/

  arcanum/                      # canonical Arcanum upstream or working submodule

  projects/                     # local product/domain project incubator
    <project-id>/

  cyberAlchemy/                 # decision-gated legacy or knowledge workspace until classified

  .github/ .githooks/ .codex/ .agents/ .planning/
                                # operator and automation surfaces, governed by runtime-surface policy
  .arcanum/ .data/ output/      # runtime/generated/local state, source-like only by explicit exception
```

This shape preserves the original three-lane DomainSpec model as the core lane:

- `implementation/`
- `research/`
- `validation/`

It also acknowledges the actual current workspace:

- Arcanum lifecycle work exists and deserves its own lane.
- Reusable sigil/spell capability work exists and should not be hidden inside research.
- Product/domain projects exist and should not be silently promoted to research projects.
- Generated runtime state exists and needs an explicit policy.

## Best Taxonomy

| Zone | Paths | Status | Owner model | Admission rule |
| --- | --- | --- | --- | --- |
| `root-orientation` | `README.md`, `docs/`, `robot-talks-complete-guide.md` | canonical plus one legacy top-level doc | repo root | Human/operator navigation, glossary, registry, and cross-zone explanation only. Feature or project detail belongs in its owning zone. |
| `ops-governance` | `ops/`, `tools/`, `.githooks/` | canonical | repo root | Repository policy, validation, drift checks, and non-product automation. |
| `operator-surfaces` | `.github/`, `.codex/`, `.agents/`, `vscode-workspaces/`, `.planning/` | canonical with generated/local exceptions | repo root or capability owner | Entry points, commands, agents, workspace launchers, and planning state. Must point to canonical owning assets rather than duplicate them silently. |
| `runtime-surface` | `.codex/commands`, `.github/skills`, `.agents/skills`, `.arcanum/runtimes`, machine Codex home, project-local installs | install/generated/source-fixture by declaration | source owner or installing runtime | Must declare whether it is canonical source, installed surface, generated runtime state, local private state, or fixture. |
| `implementation-sources` | `implementation/*` | canonical submodule/source-reference lane | owning implementation repo | Framework or implementation source of truth, pinned by submodule or explicit version. |
| `research-programs` | `research/projects/*`, `research/shared/`, `research/registry/` | canonical | project owner plus research registry | Self-contained research programs with `PROJECT.yaml`, dependencies, exports, claims/protocols/results, and no internal cross-project reads. |
| `validation-harnesses` | `validation/*` | canonical | validation repo or harness owner | Runtime evidence, test harnesses, and case studies. Reusable outputs must be exported or referenced explicitly. |
| `arcanum-lifecycle` | `arcanum/` | canonical submodule/workspace lane | Arcanum lifecycle owner | Spells, sigils, formulae, registries, and lifecycle development that belongs to Arcanum. |
| `superseded-name` | `sigils-library/` | deletion candidate | Arcanum successor owner | Old Arcanum name. Delete after preserving or intentionally discarding any unique content. |
| `project-incubator` | `projects/*` | canonical if admitted, otherwise local candidate | project owner | Product/domain pilots and app ideas. Must declare whether they are tracked project, scratch, future repo, or future research program. |
| `knowledge-candidate` | `cyberAlchemy/` | decision-gated | unresolved | Keep as candidate/legacy knowledge workspace until classified as project, Arcanum capability, research source, or archive. |
| `runtime-generated` | `.arcanum/observability/*`, `.data/`, `output/` | generated/local by default | producing tool | Append-only or generated state. Track only source-like policy/config by explicit exception. |
| `vcs-internal` | `.git/`, `.gitmodules` | system | git | VCS metadata only. Submodule declarations must match nested git paths. |

## Shape Decisions

Keep:

- `implementation/`, `research/`, and `validation/` as the DomainSpec core triangle.
- `arcanum/` as an explicit lifecycle lane, not a hidden implementation or research folder.
- `sigils-library/` only as a temporary deletion-candidate path until preservation review is complete.
- `projects/` as a project incubator, not research by default.

Change:

- Update the root README to say this is a governed multi-family workspace, with the DomainSpec three-lane model as the central lane.
- Update `ops/REPOSITORY-ORGANIZATION-PLAN.md` from a research-only organization plan into a zone contract plus research containment section.
- Add admission metadata for `projects/*` so each folder declares `tracked-project`, `scratch`, `future-repo`, `future-research`, or `archive`.

Decision-gate:

- `cyberAlchemy/`: classify before any movement.
- `research/projects/hermes-agent/repo`: repair nested git/submodule status before any migration.
- `projects/body-war/`: decide whether it is tracked, ignored local work, a future repo, or a research candidate.

## Rejected Shapes

Rejected: collapse everything into `research/`.

- Reason: Arcanum lifecycle work, local product projects, and implementation submodules are not research programs.

Rejected: split every top-level family into separate repositories now.

- Reason: too much migration risk while ownership and submodule state are unresolved.

Rejected: keep `sigils-library/` as a current independent zone.

- Reason: user clarified it was the first name of Arcanum. The right action is preservation review followed by deletion, not zone promotion.

Rejected: keep the old "unified 3-project workspace" as the whole root model.

- Reason: it no longer describes the current repository shape.

## Admission Rules

Research project:

- Belongs under `research/projects/<id>/`.
- Requires `PROJECT.yaml`, `README.md`, `claims/`, `protocols/`, `deps/`, `exports/`, `registry/`, and validation gates.
- May consume another project only through declared dependencies and exports.

Product/domain incubator project:

- Belongs under `projects/<id>/`.
- Requires a small admission file before promotion, for example `PROJECT-STATUS.md` or `PROJECT.yaml`.
- Must declare one of: tracked project, scratch/local, future standalone repo, future research program, archived candidate.

Arcanum lifecycle asset:

- Belongs in `arcanum/` when it is part of Arcanum's lifecycle source.
- Does not belong in `sigils-library/` unless a preservation review proves unique content that should be migrated first.
- Belongs in `.codex/commands` only as an installed command surface or adapter snapshot.

Generated/runtime state:

- Belongs in `.arcanum/observability`, `.data`, `output`, or tool-owned generated folders.
- Should be ignored or append-only unless explicitly promoted to source-like evidence.

Runtime surface:

- Canonical Arcanum definitions belong in `arcanum/`.
- Canonical DomainSpec skills belong in `implementation/domainspec/copilot/skills/`.
- Machine-global Codex defaults under `/mnt/c/Users/vlad_/.codex` are audit-only from this repo.
- Repo-local and project-local `.codex`, `.github/skills`, `.agents`, `.arcanum`, and `.Codex` folders require a manifest or admission decision before cleanup.

Root documentation:

- Belongs in `docs/` unless it is the root README or a short operational entrypoint.
- Long top-level guide files should either move to `docs/` or be admitted as root orientation exceptions.

## Execution Plan

L0: freeze taxonomy before moving files.

- Run deletion-candidate audit before writing the final zone contract.
- Run runtime-surface inventory before deleting or untracking installed command/skill/runtime folders.
- Create a formal zone contract in `ops/REPOSITORY-ZONE-CONTRACT.md`.
- Add a current top-level classification table.
- Record dirty git/submodule risks.

L1: align human-facing docs.

- Refresh `README.md`.
- Refresh `ops/REPOSITORY-ORGANIZATION-PLAN.md`.
- Add project incubator admission rule.

L2: add checks.

- Add or extend a root organization check to flag unclassified top-level paths.
- Flag nested repos under `research/projects/*` unless declared.
- Flag tracked generated state unless explicitly allowed.
- Flag runtime surfaces with no manifest or owner classification.

L3: perform approved migrations only.

- Move or reclassify `robot-talks-complete-guide.md`.
- Delete approved retired paths such as `sigils-library/` after preservation review.
- Resolve `cyberAlchemy/`.
- Resolve `projects/body-war/`.
- Repair `research/projects/hermes-agent/repo` submodule/nested git status.

## Final Verdict

FLAG, usable for planning.

The refined taxonomy is strong enough to guide the next artifact, but not safe enough for automatic migration. The first execution route should be `task-session` for the zone contract, followed by `decision-gate` for the three unresolved path families.

## Recommended Next Routes

1. `task-session`: create `ops/REPOSITORY-ZONE-CONTRACT.md` from this synthesis.
2. `decision-gate`: classify `cyberAlchemy/`, `projects/body-war/`, and `research/projects/hermes-agent/repo`.
3. `invoke refresh`: update `ops/REPOSITORY-ORGANIZATION-INVOKE-PLAN.md` after the zone contract is accepted.
4. `task-session`: create `ops/RUNTIME-SURFACE-POLICY.md` from `RUNTIME-SURFACE-INVOKE.md`.
