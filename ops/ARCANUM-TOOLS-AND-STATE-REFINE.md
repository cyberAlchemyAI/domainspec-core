# Arcanum Tools And State Refine

Date: 2026-05-29
Status: flag
Target: `tools/arcanum`, `.arcanum` artifacts, repo-local vs global runtime behavior

## Short Answer

Yes, we still need `tools/arcanum`, but not as the default model execution engine.

`tools/arcanum` should become the deterministic Arcanum utility surface:

- resolve canonical capabilities,
- validate dispatch and install manifests,
- list runtime adapters,
- generate runtime/install surfaces,
- produce handoff prompts and receipt requirements,
- run deterministic smoke checks,
- keep legacy `codex-exec` available only by explicit opt-in.

It should not be the default way to run model-backed stages through nested `codex exec`.

## Role Split

| Layer | Owner | What It Does | What It Must Not Do |
| --- | --- | --- | --- |
| Canonical source | `arcanum/arcana`, `arcanum/spells`, `arcanum/formulae`, DomainSpec source | Defines behavior | Become copied runtime state |
| Native runtime skills | Codex skills, Claude skills, Copilot skills/instructions | Execute or guide model-backed work in the host runtime | Become canonical source |
| `tools/arcanum` | repository or installed tool bundle | Deterministic resolution, validation, manifests, compatibility | Default to nested model CLI |
| `.arcanum` | target repository runtime/state folder | Runtime manifests, generated adapters, observability, local state | Hide canonical source or unclassified generated state |

## Do We Need `tools/arcanum`?

### Keep It

Keep `tools/arcanum` for repository-local installs such as `domainspec-core`.

It is still useful when a repo needs:

- `--resolve <capability>` checks,
- adapter listing and default adapter inspection,
- dispatch-spec validation wrappers,
- runtime install generation for Codex/Claude/Copilot,
- `.arcanum` runtime manifest maintenance,
- deterministic smoke tests,
- compatibility with older scripts and evidence.

### Shrink Its Authority

The migration should remove this assumption:

```text
tools/arcanum --exec == run the model-backed workflow
```

Replace it with:

```text
tools/arcanum validates/resolves/prepares
native runtime skills/subagents execute
stage receipts prove what happened
```

`tools/arcanum --exec` may remain, but the default adapter should become `local-skill` or `native-skill`, producing a handoff/receipt contract rather than launching nested Codex. `codex-exec` should be explicit legacy opt-in.

## What Happens To `.arcanum`?

`.arcanum` should remain as a target-repository runtime/state namespace, but every subpath needs a class.

| Path Class | Examples | Policy |
| --- | --- | --- |
| Runtime manifest/config | `.arcanum/runtime/*`, future `.arcanum/runtime/config.json` | Keep only manifest/config needed to describe installed surfaces. |
| Runtime adapters/install outputs | `.arcanum/runtimes/github-copilot/*`, `.arcanum/runtimes/codex/*` | Keep only when generated from canonical source and tracked intentionally. |
| Legacy command adapters | `.arcanum/runtimes/codex/commands/*` | Delete or avoid by default; keep only for explicit compatibility. |
| Observability durable config | `.arcanum/observability/README.md`, `config.json`, `.gitkeep` structure | Keep if this repo uses Arcanum observability. |
| Observability ledgers | `.arcanum/observability/signals/*.jsonl`, `by-sigil/*.jsonl`, reflection state | Track only if accepted as durable evidence; otherwise append-only local/generated. |
| Generated run state | `.arcanum/observability/runs/*`, hooks output, reflections | Ignore/untrack by default. |
| Local private state | `.arcanum/codex-home*`, auth/cache/runtime homes | Never track. |
| Knowledge/runtime indexes | `.arcanum/necronomicon/*` | Keep only if intentionally used as repository durable index. |

## In `domainspec-core`

`domainspec-core` is a governed multi-family workspace, so it can keep a repo-local Arcanum utility surface:

- keep `tools/arcanum`,
- keep `tools/audit_codex_skill_surface.sh`,
- keep `tools/classify_root_github_skills.sh`,
- keep selected `.arcanum/observability` config/evidence if intentionally durable,
- keep `.arcanum/runtimes/github-copilot` only if root `.github/skills` is confirmed as a distribution surface,
- delete `.arcanum/runtimes/codex/commands/*` as legacy command adapters unless explicitly needed.

The root repo should not rely on `.arcanum` as the canonical source for Arcanum behavior. Canonical source remains under `arcanum/`.

## When Running From Global Codex

Global Codex means the operator is using:

```text
/mnt/c/Users/vlad_/.codex/skills
```

In that mode:

- the global skill is the entrypoint,
- the target repository is discovered from the current working directory,
- outputs and run evidence should be written into the target repository when the task is repo-scoped,
- machine-global state should stay minimal and should not absorb repo evidence,
- `tools/arcanum` is optional unless the target repo has a local Arcanum tool install or the skill needs deterministic repo-local validation.

Global skills should not silently create `.arcanum` in every repo. They should create or update `.arcanum` only when the user runs an install/setup/observability task or when a workflow explicitly needs repo-local runtime state.

## New Repository / New User Behavior

For a new user or a new repository, installation should be profile-based.

| Profile | Writes | Does Not Write |
| --- | --- | --- |
| `personal-codex` | user Codex home skills/aliases | repo `.codex/commands` |
| `repo-local` | `tools/arcanum`, `.arcanum/runtime/config`, selected docs/manifests | model-backed command wrappers by default |
| `github-copilot` | `.github/skills` or `.github/instructions` generated from canonical source | personal Codex home |
| `claude` | `.claude/skills`, `.claude/agents`, `CLAUDE.md` | Codex commands |
| `observability` | `.arcanum/observability` config and durable ledgers | local/private run cache |
| `all` | selected explicit profiles | unclassified generated state |
| `none` | no install, source-only usage | runtime state |

This avoids "copies and copies" while still making Arcanum usable across runtimes.

## Answer To The Current Question

You still need `tools/arcanum` in repositories where you want deterministic Arcanum repo-local behavior, install generation, adapter metadata, validation, or compatibility.

You do not need `tools/arcanum` as the universal execution path for model-backed orchestration.

`.arcanum` should become a classified repo-local runtime namespace. Some parts can be tracked, some parts should be generated/local, and private/global state should not be tracked.

## Remaining Required Work

1. Update `tools/arcanum` adapter model so `local-skill` or `native-skill` is the orchestration default.
2. Update bootstrap/install scripts to use profiles and stop generating command files by default.
3. Classify current `.arcanum` tracked files into durable config, distribution adapters, evidence, generated state, and delete candidates.
4. Add ignore rules or untracking tasks for generated `.arcanum` run/reflection/local-private state.
5. Decide whether `.arcanum/runtimes/github-copilot` is the generator source for root `.github/skills` or just stale install output.
6. Update Refine so it stops requiring command-backed model stage dispatch and instead records parent-owned dispatch plus native receipts.

## Refine Result

- Target: `tools/arcanum` and `.arcanum` handling across repo-local and global runtime modes
- Status: flag
- Preset: compact
- Research: no-research
- Run manifest: `ops/ARCANUM-TOOLS-AND-STATE-REFINE.md`
- Evidence index: `ops/RUNTIME-SURFACE-CONVERGENCE-REFINE.md`, `ops/SKILLS-FIRST-RUNTIME-POLICY.md`, `ops/CODEX-SKILL-SURFACE-POLICY.md`, current `.arcanum` scan
- Seed proposal: keep `tools/arcanum` as deterministic utility, classify `.arcanum` by state role, use global Codex skills as entrypoints without absorbing repo evidence
- Dispatch route: local synthesis; command-backed refine not run because this is a design-policy refinement
- Runtime handoff: none
- Stage evidence:
  - Context Builder evidence baseline: pass
  - Invoke Define: n/a
  - Interrogation refine-review: n/a
  - Research decision: pass
  - Distill: pass
  - Invoke Redefine / Design: n/a
  - Interrogation refine-design-review: n/a
  - Distill Repair: n/a
  - Invoke Plan: n/a
  - Final Interrogation and Synthesis: pass
- Final synthesis: keep `tools/arcanum` as deterministic repo utility, not default nested executor; keep `.arcanum` only as classified runtime/state/evidence namespace
- Recommended next routes: TASK-ORCH-004 for adapter metadata, TASK-ORCH-006 for active surface inventory, then a `.arcanum` classification task-session
