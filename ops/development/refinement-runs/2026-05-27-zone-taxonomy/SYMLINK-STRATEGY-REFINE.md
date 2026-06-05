# Symlink Strategy Refinement

Date: 2026-05-27
Target: clean runtime surface without copies and copies
Status: FLAG

## Question

Will the runtime-surface policy give the cleanest surface without repeated copies? Should we use symbolic links?

## Short Answer

Yes, but with a mixed model:

- Use symlinks for repo-local discovery surfaces when the consumer and canonical source live in the same checkout and the runtime supports symlink traversal.
- Use generated snapshots for machine-global Codex, cross-repository installs, Windows/WSL boundary cases, and distributable runtime adapters.
- Use manifests to make every snapshot auditable and refreshable.
- Do not preserve unmanaged copies.

The cleanest surface is not "symlink everything." It is:

```text
canonical source
  -> symlink when local and stable
  -> generated snapshot when crossing runtime/repo/machine boundaries
  -> generated state ignored or untracked
```

## Evidence

Current good pattern:

- `arcanum/.agents/skills/*` already uses symlinks into canonical Arcanum capability folders.
- `arcanum/README.md` explicitly says `.agents/skills/` uses symlinked skill folders so tiered Arcanum folders remain canonical while Codex can discover them.

Current copy-heavy patterns:

- `/mnt/c/Users/vlad_/.codex/skills/arcanum-*` are machine-global snapshot directories, not symlinks.
- `/mnt/c/Users/vlad_/.codex/commands/*.md` are machine-global command snapshots.
- `implementation/domainspec/.codex/commands/*.md` are submodule-local command snapshots.
- `projects/body-war/.codex/commands/*.md` are untracked project-local command snapshots.
- `projects/sonar-loop/.github/skills/arcanum-*` are project-local GitHub Copilot skill snapshots.

Important warning:

- `arcanum/.arcanum/codex-home*` contains symlinks to private Codex home state such as auth/config/model cache. That is not the model to copy. Private runtime state must be ignored and never preserved as source.

## Recommended Model

### 1. Repo-Local Development Surface: Prefer Symlinks

Use symlinks when:

- source and target are inside the same repository checkout,
- the target is a discovery facade, not a distribution artifact,
- the runtime follows symlinks reliably,
- the symlink points from a flat discovery folder to canonical source.

Good example:

```text
arcanum/.agents/skills/context-builder -> ../../transmutations/context-builder
```

Recommended future shape:

```text
.agents/skills/arcanum-context-builder -> ../arcanum/transmutations/context-builder
.agents/skills/arcanum-inventory -> ../arcanum/arcana/inventory
```

Only do this if root-level Codex actually reads `.agents/skills` from the parent checkout and follows links correctly.

### 2. Machine-Global Codex Surface: Prefer Managed Snapshots

Use snapshots for:

- `/mnt/c/Users/vlad_/.codex/skills/*`
- `/mnt/c/Users/vlad_/.codex/commands/*`

Reason:

- This is outside the repo.
- It crosses Windows/WSL boundaries.
- The user previously chose global availability by copying.
- Global installs should not break when a repo moves, branch changes, submodule is absent, or WSL path resolution changes.

Cleanliness rule:

- Snapshots must carry provenance and refresh metadata.
- They should be refreshed by an installer, not edited manually.

### 3. GitHub Copilot / Other Runtime Surface: Prefer Managed Snapshots

Use snapshots for:

- `.github/skills/*`
- runtime-specific install packages,
- project-local exported capability bundles.

Reason:

- Many external runtimes do not reliably follow symlinks or preserve them through UI upload, repository archive, marketplace packaging, or cross-platform checkout.
- Runtime surfaces should be reproducible from canonical source.

### 4. Command Adapter Surface: Prefer Generated Files

Command files under `.codex/commands` are not canonical behavior. They are adapter files.

Use generated snapshots because:

- the command body often embeds a canonical source snapshot,
- slash-command surfaces expect files in a specific folder,
- command adapters may include runtime-specific wrappers.

Cleanliness rule:

- generated command files must be synchronized from canonical source or explicitly marked stale.
- they should never become the source of truth.

### 5. Generated Runtime State: Never Symlink As Source

Do not use symlinks to preserve:

- auth/config/model cache,
- Codex home state,
- runtime run folders,
- telemetry JSONL,
- SQLite projections,
- temporary plugin/cache folders.

These should be ignored, untracked, or stored as explicit evidence snapshots only when deliberately promoted.

## Policy Matrix

| Surface | Best mechanism | Why |
| --- | --- | --- |
| `arcanum/.agents/skills/*` | symlink | same repo, discovery facade, canonical source nearby |
| root `.agents/skills/arcanum-*` | symlink candidate | clean if Codex reads root `.agents` reliably |
| root `.codex/commands/*` | generated snapshot | command adapter surface, not canonical source |
| global `/mnt/c/Users/vlad_/.codex/skills/*` | managed snapshot | machine-global, Windows/WSL boundary, survives repo movement |
| global `/mnt/c/Users/vlad_/.codex/commands/*` | managed snapshot | slash-command compatibility and desktop surface |
| `implementation/domainspec/copilot/skills/*` | canonical source | DomainSpec owns these |
| `implementation/domainspec/.github/skills/*` | generated/install target or DomainSpec-owned snapshot | submodule-local, do not parent-edit |
| `projects/*/.github/skills/arcanum-*` | generated snapshot or delete | project-local runtime install, needs manifest |
| `projects/*/.codex/commands/*` | generated snapshot or delete | project-local runtime install, needs manifest |
| `.arcanum/observability/*` | generated state | ignore/untrack unless evidence |
| `.arcanum/runtime/config.json` | tracked config possible | safe non-secret runtime selection metadata |
| `.arcanum/runtime/private/*` | local private state | never track |

## Cleanest Target Surface

The cleanest target for this repo is:

```text
arcanum/                         # canonical Arcanum source
  arcana/
  transmutations/
  formulae/
  spells/
  .agents/skills/*               # symlinks for Arcanum repo-local discovery

.agents/skills/                  # optional parent repo symlink facade
  arcanum-<capability> -> ../arcanum/<tier>/<capability>

.codex/commands/                 # optional generated adapter snapshots only
  MANIFEST.yaml                  # source, generated_by, last_verified

.github/skills/                  # only root-owned skills or generated runtime snapshots with manifest

.arcanum/
  runtime/config.json            # safe config
  runtime/private/               # ignored
  observability/                 # generated unless explicit evidence
```

Then remove:

- obsolete `sigils-library/`,
- unmanaged project-local `.codex/commands` copies,
- duplicate Arcanum GitHub skills unless admitted as fixtures,
- tracked generated telemetry/database files unless promoted.

## Guardrails

1. Do not symlink from tracked repo files to machine-private paths.
2. Do not symlink across Windows/WSL boundaries for global Codex install by default.
3. Do not use symlinks for packaged/distributed runtime surfaces unless that runtime explicitly supports them.
4. Do not edit generated snapshots manually.
5. Every non-symlink install surface needs a manifest.
6. Every symlink facade needs a validation check that links resolve.

## Validation Checks

Symlink health:

```bash
find .agents arcanum/.agents -type l -print -exec test -e {} \; -print
```

No private symlink leakage:

```bash
find . -type l -lname '*auth.json' -o -lname '*config.toml' -o -lname '*models_cache.json'
```

Runtime surface manifest coverage:

```bash
find . -path './.git' -prune -o \( -path '*/.codex/commands' -o -path '*/.github/skills' -o -path '*/.agents/skills' -o -path '*/.arcanum/runtime' \) -type d -print
```

Generated state tracking:

```bash
git ls-files '.data/*' '*.sqlite' '*.sqlite-shm' '*.sqlite-wal' '.arcanum/observability/*.jsonl'
```

## Final Synthesis

This will give the cleanest surface only if the runtime policy explicitly distinguishes symlink facades from generated snapshots.

Recommended rule:

- **Symlink inside the same repo for discovery.**
- **Snapshot across repo, runtime, machine, or distribution boundaries.**
- **Manifest every snapshot.**
- **Ignore/untrack generated state.**

This keeps Arcanum canonical in one place while preserving robust global Codex and GitHub Copilot surfaces.

