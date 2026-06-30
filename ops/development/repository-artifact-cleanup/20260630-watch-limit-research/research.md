# Repository Development Artifact Cleanup Research

Dispatch ID: `2026-06-30-repository-development-artifact-cleanup-research`
Date: 2026-06-30
Status: collected explorer returns

This file collects the explorer returns for the governed research dispatch on
VS Code file-watcher pressure and future development-artifact cleanup in
`domainspec-core`. It is evidence for synthesis only; it does not authorize
cleanup or promotion.

## Agent 1 - Robertson, Sam - Filesystem Pressure And VS Code Relief

Runtime nickname: Hume

No files edited.

Commands used included `find ... -printf`, `du -sk/-sh --exclude=.git`,
`cat /proc/sys/fs/inotify/*`, and workspace reads.

Current live counts outside `.git`:

| Class | Files | Dirs | Size signal |
| --- | ---: | ---: | ---: |
| `.lake` | 248,344 | 8,909 | about 12.9 GiB file content |
| `node_modules` | 110,997 | 13,083 | about 1.6 GiB file content |
| `.venv` / `venv` | 24,846 | 1,975 | about 1.1 GiB file content |
| `.claude/worktrees` | 12,183 | 3,569 | about 244 MiB file content |
| build/dist/out/etc. | 561 | 95 | small now |
| `__pycache__` / Python caches | 180 | 74 | small now |
| `.formal-tools` | 113 | 69 | about 202 MiB disk usage |

Total live pressure was about `435,524` files, `40,632` directories, and
`18G` disk usage. Candidate exclusions cover about `397,224` files and
`27,774` directories, leaving about `38,300` files and `12,858` directories
visible to broad workspace watching and search.

Top individual pressure paths:

```text
119,937 files  7.3G  research/projects/mars/papers/triton-top2-backward-kernel/formal/.lake
119,616 files  7.1G  domainspec-lean-formalization/lean-engineer/.lake
46,863 files   566M  validation/poker-team/node_modules
40,484 files   766M  projects/savvy_legal-studio-ai/frontend/savvy-legal-studio/node_modules
17,867 files   854M  research/triton-top2-backward-kernel/.venv
13,443 files   154M  implementation/domainspec/node_modules
12,190 files   285M  .claude/worktrees
8,791 files    700M  domainspec-lean-formalization/lean-formalization/files/.lake
6,979 files    353M  research/agentic-music-studio/build/.venv
```

Kernel values verified:

```text
fs.inotify.max_user_watches=524288
fs.inotify.max_user_instances=128
```

The file count is high enough for VS Code's large-workspace warning even though
directory count is below the watch limit; multiple windows or extensions can
still pressure instances.

The likely target workspace
`vscode-workspaces/domainspec-core.code-workspace` currently has no
`files.watcherExclude` or `search.exclude` settings. An existing example lives
at `validation/poker-team/domainspec-unified.code-workspace`.

Suggested workspace settings candidates:

```json
"files.watcherExclude": {
  "**/node_modules/**": true,
  "**/.lake/**": true,
  "**/.venv/**": true,
  "**/venv/**": true,
  "**/__pycache__/**": true,
  "**/.pytest_cache/**": true,
  "**/.mypy_cache/**": true,
  "**/.ruff_cache/**": true,
  "**/.formal-tools/**": true,
  "**/.claude/worktrees/**": true,
  "**/dist/**": true,
  "**/build/**": true,
  "**/coverage/**": true,
  "**/target/**": true,
  "**/.next/**": true,
  "**/.nuxt/**": true,
  "**/.svelte-kit/**": true,
  "**/out/**": true
},
"search.exclude": {
  "**/node_modules": true,
  "**/.lake": true,
  "**/.venv": true,
  "**/venv": true,
  "**/__pycache__": true,
  "**/.pytest_cache": true,
  "**/.mypy_cache": true,
  "**/.ruff_cache": true,
  "**/.formal-tools": true,
  "**/.claude/worktrees": true,
  "**/dist": true,
  "**/build": true,
  "**/coverage": true,
  "**/target": true,
  "**/.next": true,
  "**/.nuxt": true,
  "**/.svelte-kit": true,
  "**/out": true
}
```

Editor-exclude now: `.lake`, `node_modules`, `.venv`, Python caches,
build/dist/coverage outputs, `.formal-tools`, and `.claude/worktrees` if not
actively editing nested worktrees.

Clean later only with intent: duplicate Lean `.lake` trees, reinstallable
`node_modules`, research virtualenvs, generated build artifacts, and stale
`.claude/worktrees`. Treat `.claude/worktrees` through worktree lifecycle, not
blind deletion.

Risks and checks:

- Broad `**/build/**`, `**/target/**`, and `**/out/**` can hide tracked
  benchmark or evidence artifacts from search; keep them as search/watch relief,
  not cleanup proof.
- If the folder is opened directly instead of the `.code-workspace`, workspace
  settings will not apply.
- Validate by reloading VS Code, checking whether the warning disappears,
  inspecting Output: `Log (File Watcher)`, and rerunning the count commands
  after any setting changes.

## Agent 2 - Mac Lane, Saunders - Governance And Owner Boundaries

Runtime nickname: Confucius

Read-only pass completed. No files edited.

Cleanup rules:

- Classify before deleting, regenerating, untracking, or treating runtime
  artifacts as source. Parent cleanup must classify owner scope first, then only
  mutate explicitly named scopes. Evidence:
  `ops/SURFACE-OWNER-BOUNDARIES.md` and
  `ops/ARCANUM-STATE-CLASSIFICATION.md`.
- Canonical source is protected. `implementation/`, `research/`, `validation/`,
  and `arcanum/` are canonical source zones; canonical paths are kept and
  protected before cleanup decisions. Evidence:
  `ops/REPOSITORY-ORGANIZATION-DESIGN.md`.
- Public/private boundary is hard: `arcanum/` is public; private parent,
  implementation, validation, sessions, telemetry, and owner-only residue must
  not leak into public derivatives. Evidence: `SUBMODULE-DISCIPLINE.md` and
  `cyberAlchemy-v2/authority/constitutions/STABLE-REPOSITORY-CONSTITUTION.md`.
- Historical/open development evidence is preserved unless a cleanup task
  explicitly owns it. Development artifacts are evidence/proposal surfaces, not
  authority, and should be distilled through promotion patches rather than bulk
  copied or deleted casually. Evidence:
  `docs/decisions/surface-cleanup-blocker-decisions.md` and
  `arcanum/framework/DEVELOPMENT-TO-CANONICAL-PROMOTION.md`.

Parent cleanup may classify but not mutate these owner scopes:

- `arcanum/`: Arcanum-owned public source/runtime state; no parent sweep.
- `implementation/domainspec/`: DomainSpec-owned; parent may record handoff only.
- `projects/*`: project-owned sandboxes; do not move/delete/normalize in root
  cleanup.
- `validation/*`: fixture-owned; mutate only through validation tasks with
  fixture expectations.
- Machine-global Codex home: explicit `personal-codex` only, never silent repo
  cleanup mutation.
- Submodules require submodule-first, parent-last; parent gitlink bumps are
  deliberate, never automatic.

Generated versus canonical:

- Source artifacts are versioned by default; generated artifacts are ignored
  unless explicitly promoted to durable evidence; local runtime artifacts must
  never become versioned source. Evidence:
  `arcanum/framework/ARTIFACT-CONSTITUTION.md`.
- Skills are the default runtime surface; command files are legacy
  compatibility, not canonical source, and should not be regenerated by default.
  Evidence: `ops/SKILLS-FIRST-RUNTIME-POLICY.md`.
- Generated native packages must record canonical source/provenance and be
  regenerated from canonical source rather than manually evolved. Evidence:
  `ops/CODEX-SKILL-SURFACE-POLICY.md`.
- Inventory/ontology/read models reduce search and preserve evidence, but
  cannot promote authority by themselves. Evidence:
  `cyberAlchemy-v2/authority/constitutions/STABLE-REPOSITORY-CONSTITUTION.md`
  and `cyberAlchemy-v2/authority/AUTHORITY-MODEL.md`.

Deletion gates:

- No migration/deletion before classification and preservation review; obsolete
  paths require preservation diff, then approval. Evidence:
  `ops/REPOSITORY-ORGANIZATION-DESIGN.md`.
- A preservation diff proves unique content was migrated, retained, or
  intentionally discarded before deletion.
- `sigils-library/` is a deletion candidate only after targeted preservation
  diff; `cyberAlchemy/`, `projects/body-war/`, and
  `research/projects/hermes-agent/repo` are decision-gated.
- Duplicate skill pruning is gated by owner/runtime confirmation, even for exact
  duplicates across owner boundaries. Evidence:
  `ops/DUPLICATE-SKILL-PRUNING-PLAN.md`.

Governance implications:

- For `discipline-governance`: cleanup/owner-boundary work should stay in the
  private umbrella discipline layer unless generalized. A discipline can name a
  recurring practice and route hardening, but cannot promote/delete/mutate owned
  content directly.
- Existing discipline anchors already cover much of this: `submodule-orchestration`,
  `asset-ownership-propagation`, public `runtime-boundary`, and
  `development-package-promotion-gate`.
- For `constitution-governance`: enforceable cleanup should become scoped
  constitution rules/validators: owner classification, preservation diff,
  public/private scrub, generated traceability, and promotion-patch
  requirements. Constitution rules should remain modular and route contested
  owner/public/private choices through `decision-gate`.

## Agent 3 - Turing, Alan - Cleanup-Sigil Lifecycle Design

Runtime nickname: James

Read-only research pass. Proposed working name: `development-artifact-cleanup`.

Problem:

`domainspec-core` mixes canonical source, generated runtime/install surfaces,
local/private state, historical evidence, and active development packets. A
cleanup sigil must reduce active `development/` clutter directory by directory
while preserving open packets and proving that anything removed, archived,
untracked, or regenerated has a canonical successor, owner approval, or no
source value.

Tier guess: Arcana. This is not a one-off cleanup helper; it needs
owner-boundary governance, preservation diffs, dry-run ledgers, observability,
reflection, and promotion readiness. That matches `sigil-development`
lifecycle ownership for reusable sigils and its requirement for experiment
harness evidence before promotion readiness.

Directory process:

1. Select one directory root and owner scope.
2. Read local owner rules: root, `arcanum/`, `implementation/domainspec/`,
   `projects/*`, `validation/*`.
3. Inventory tracked, untracked, ignored, generated, and nested-repo state for
   that directory.
4. Classify the directory using the repo zone/runtimes policy: canonical
   source, runtime surface, generated/local state, superseded name, project
   incubator, validation fixture, etc. The key repo rule is that useful files
   are not canonical unless they have a current owner, current name, and no
   newer canonical successor.
5. Partition artifacts into packets: run folder, task-session folder, handoff
   packet, research packet, generated output, runtime surface, docs/source.
6. Mark open packets. Preserve in place if status is `OPEN`, `flag`, `block`,
   `defer`, `review-required`, has unresolved `Open Questions`, has a next
   route not executed, or lacks a promoted successor.
7. For non-open packets, find canonical successor or owner archive: `RESULT.md`,
   `RUN-MANIFEST.md`, `RUNTIME-HANDOFF.md`, promotion records, source maps,
   generated provenance, frontmatter `canonical_source`, or root policy tables.
8. Run preservation diff before any proposed deletion/archive/untrack.
9. Emit a dry-run ledger with proposed actions only.
10. Route blockers, owner conflicts, or destructive actions to the proper owner
    before any apply mode.

Artifact states:

| State | Meaning | Default action |
| --- | --- | --- |
| `canonical-source` | Current owner source or authority surface. | Keep; never delete by cleanup. |
| `open-development-packet` | Work is not closed, promoted, or superseded. | Keep in place. |
| `promoted` | Durable content moved into owner surface with citation/backlink. | Archive/delete candidate only after preservation diff. |
| `superseded` | Newer canonical successor exists. | Diff, then archive/delete with approval. |
| `generated` | Runtime output, projection, telemetry, cache, generated package. | Ignore/untrack/regenerate unless explicitly promoted as evidence. |
| `local-private` | Auth, machine-local runtime homes, private cache. | Never track; preserve locally; do not parent-edit. |
| `owner-boundary` | Child/submodule/project/validation-owned. | Classify only; emit handoff. |
| `archive` | Closed historical evidence retained for audit. | Move/record only with owner approval. |
| `cleanup-candidate` | No owner/successor proven yet. | Flag or block; do not delete. |
| `blocked` | Owner, public/private, successor, or unique-content risk unresolved. | Stop. |

CyberAlchemy lifecycle vocabulary separates `source-evidence`,
`review-candidate`, `active`, `drift-flagged`, `superseded`, and
`deprecated`. Its gate vocabulary is `pass`, `flag`, `block`, `defer`.

Diff and classification algorithm row:

```yaml
path:
owner_scope:
git_state:
artifact_kind:
lifecycle_state:
status_markers:
canonical_successors:
generated_provenance:
unique_content:
proposed_action:
gate:
```

Classification rules:

1. If path is canonical source, keep.
2. If path is child-owned, classify and hand off. Parent cleanup may classify
   child paths but must not mutate them without explicit owner scope.
3. If generated package, require `canonical_source`, runtime, generator, alias
   status, and mutation policy before keeping or regenerating.
4. If superseded name, tree-diff against successor and block on unique content.
5. If development packet, compare final claims/outputs to canonical successors.
   If successor lacks durable claims, mark `open-development-packet` or
   `archive`, not delete.
6. If generated/local state, untrack only after explicit approval; `.arcanum`
   already has a split where durable config stays and ledgers/state are
   generated by default.
7. If owner/successor/public-private status is unclear, block or decision-gate.

Dry-run ledger contract:

```yaml
run_id: <timestamp-slug>
mode: dry-run
target_root: <path>
owner_scope: root | arcanum | domainspec | project | validation
status: pass | flag | block
summary:
  keep_open: <n>
  archive_candidates: <n>
  delete_candidates: <n>
  untrack_candidates: <n>
  blocked: <n>
rows:
  - path: <path>
    artifact_state: open-development-packet | promoted | superseded | generated | local-private | archive | blocked
    lifecycle_status: open | pass | flag | block | defer | executed | unknown
    owner_scope: <scope>
    canonical_successor: <path|null>
    diff_result: equivalent | unique-content | successor-missing | not-needed | not-run
    proposed_action: keep | archive-candidate | delete-candidate | untrack-candidate | regenerate-candidate | handoff | block
    evidence_refs:
      - <path:line or manifest ref>
    gate: pass | flag | block
```

Safety gates:

- No apply mode without prior dry-run ledger.
- No parent mutation of `arcanum/`, `implementation/domainspec/`,
  `projects/*`, or `validation/*` unless that owner scope is explicitly selected.
- No deletion without canonical successor plus preservation diff.
- No generated package cleanup without provenance/regeneration path.
- No removal of open packets.
- No public/private boundary ambiguity.
- No cleanup if the action would hide unresolved questions, next routes, or
  handoff obligations.
- No schema/authority promotion from cleanup output; cleanup can propose, not
  promote.

Routing:

- Route to `sigil-development` when creating the reusable cleanup sigil, adding
  observability, writing its experiment harness, defining quality
  bar/anti-patterns, or deciding promotion readiness.
- Route to `discipline-governance` if the recurring practice itself needs a
  discipline card, catalog row, steward, maturity status, and hardening route.
- Route to `constitution-governance` when a cleanup rule should constrain future
  artifacts, such as status declarations, preservation diffs, generated
  projection provenance, or owner-boundary classify-only behavior.
- Route to `decision-gate` for contested owner, public/private, naming,
  deletion, archive, or successor decisions.
- Route to `task-session` only for bounded cleanup execution after dry-run and
  owner gates pass.

Net: this future sigil should be a dry-run-first Arcana cleanup lifecycle that
classifies, proves successors, preserves open packets, and emits owner-routed
cleanup candidates. The sharp edge is useful: it should make deletion boring,
auditable, and deliberately difficult.
