# Repository Development Artifact Cleanup Findings

Dispatch ID: `2026-06-30-repository-development-artifact-cleanup-research`
Date: 2026-06-30
Status: draft findings pending auditor

## Verdict

The recommended path is **build-from-owned**.

The repository already has strong cleanup precedent: classify before mutation,
preserve historical/open development evidence, respect owner boundaries, run
preservation diffs before deletion, and route destructive work through bounded
execution. The missing piece is a reusable dry-run lifecycle that makes those
rules operational directory by directory. That gap can justify a future
`development-artifact-cleanup` sigil only if it is built from existing
discipline, constitution, artifact, and task-session owners rather than as a
clean-room deletion tool.

The immediate VS Code problem should be handled separately as editor relief:
add workspace watcher/search excludes for large generated trees. This is not
cleanup proof and does not authorize deletion.

## Evidence Base

The file-pressure lane found about `435,524` files and `40,632` directories
outside `.git`, with about `397,224` files covered by generated/runtime
exclusion candidates. The largest classes are `.lake` (`248,344` files),
`node_modules` (`110,997` files), virtual environments (`24,846` files), and
`.claude/worktrees` (`12,183` files). High-pressure examples include
`research/projects/mars/papers/triton-top2-backward-kernel/formal/.lake`,
`domainspec-lean-formalization/lean-engineer/.lake`,
`validation/poker-team/node_modules`,
`projects/savvy_legal-studio-ai/frontend/savvy-legal-studio/node_modules`,
`research/triton-top2-backward-kernel/.venv`, and
`implementation/domainspec/node_modules`. The machine already has
`fs.inotify.max_user_watches=524288`, so the first practical relief is
workspace exclusion, not a system knob change. See [research.md](research.md),
Agent 1.

The governance lane found existing owner-boundary and cleanup rules:
parent cleanup may classify child-owned paths but must not mutate
`arcanum/`, `implementation/domainspec/`, `projects/*`, or `validation/*`
unless that owner scope is explicitly selected. Canonical source is protected;
generated/local state is ignored or untracked only when explicit policy allows;
public/private boundaries must not leak private parent evidence into public
`arcanum`. See [research.md](research.md), Agent 2, plus
`ops/SURFACE-OWNER-BOUNDARIES.md`,
`ops/REPOSITORY-ORGANIZATION-DESIGN.md`, and
`ops/ARCANUM-STATE-CLASSIFICATION.md`.

The lifecycle lane proposed a dry-run-first Arcana workflow that classifies
artifacts, proves successors, preserves open packets, and emits owner-routed
cleanup candidates. See [research.md](research.md), Agent 3.

The runtime reviewer gates were incorporated into this synthesis as operator
review notes rather than as separate durable artifacts:

- Precedent: `build-from-owned`, not `precedent-clean`.
- Non-vacuity: pass, but final output must carry concrete path classes,
  commands/checks, states, ledger shape, examples, and non-examples.
- Definitional soundness: pass, if cleanup means **classification plus proposed
  disposition**, not deletion. Apply/delete must remain a later scoped
  `task-session`.

## Immediate VS Code Relief

Add workspace-level `files.watcherExclude` and `search.exclude` entries to
`vscode-workspaces/domainspec-core.code-workspace` for generated/runtime paths.
This is safe as editor relief because it does not mutate source, git state, or
development packets.

Two caveats from the filesystem evidence matter:

- exclude `.claude/worktrees` only when not actively editing those nested
  worktrees;
- broad `build`, `target`, and `out` patterns can hide tracked benchmark or
  evidence artifacts from search, so they must stay editor-relief settings, not
  deletion evidence.

Recommended initial patterns:

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

Validation after this change:

```bash
cat /proc/sys/fs/inotify/max_user_watches
cat /proc/sys/fs/inotify/max_user_instances
find . -path './.git' -prune -o -path '*/.git' -prune -o -type f | wc -l
```

Then reload VS Code and inspect Output: `Log (File Watcher)`. If the repository
is opened directly instead of through `vscode-workspaces/domainspec-core.code-workspace`,
these workspace settings will not apply.

## Cleanup Taxonomy

Use a normalized state vocabulary for dry-run rows:

| State | Meaning | Default action |
| --- | --- | --- |
| `canonical-source` | Current owner source or authority surface. | Keep. |
| `open-development-packet` | Work is not closed, promoted, superseded, or owner-approved for archival. | Keep in place. |
| `promoted` | Durable content moved into an owner surface with citation/backlink or promotion record. | Archive/delete candidate only after preservation diff. |
| `superseded` | Newer canonical successor exists. | Diff, then archive/delete only after approval. |
| `generated` | Runtime output, projection, telemetry, cache, dependency tree, generated package, build artifact. | Ignore, untrack, or regenerate only with provenance and approval. |
| `local-private` | Auth, machine-local runtime home, private cache, local worktree state. | Never track; preserve locally; do not parent-edit. |
| `archive` | Closed historical evidence intentionally retained for audit. | Keep or move only with owner approval. |
| `blocked` | Owner, successor, public/private, or unique-content risk unresolved. | Stop. |

Classification overlays:

| Overlay | Meaning | Rule |
| --- | --- | --- |
| `owner-boundary` | `arcanum/`, `implementation/domainspec/`, `projects/*`, `validation/*`, nested repos, or submodules. | Parent cleanup may classify and hand off, not mutate. |
| `cleanup-candidate` | Potential action lacks enough proof. | Flag/block until owner, successor, and preservation evidence exist. |

## Retention Rules

Preserve a development packet in place when any of these are true:

- status is `OPEN`, `flag`, `block`, `defer`, or `review-required`;
- it has unresolved `Open Questions`;
- it names a next route that has not executed;
- it lacks a canonical successor;
- the successor does not carry the packet's durable claims;
- owner scope or public/private status is unclear.

Closed packets are not automatically deletable. They need a canonical successor
or archive signal such as `RESULT.md`, `RUN-MANIFEST.md`, `RUNTIME-HANDOFF.md`,
source maps, promotion records, generated provenance, or frontmatter
`canonical_source`, followed by preservation diff.

## Dry-Run Algorithm

For each target root:

1. Select exactly one directory root and owner scope.
2. Read applicable owner rules for that scope.
3. Inventory tracked, untracked, ignored, generated, and nested-repo state.
4. Classify each item using the normalized state vocabulary and overlays.
5. Partition development content into packets: run folder, task-session folder,
   handoff packet, research packet, generated output, runtime surface, or
   docs/source.
6. Preserve open packets in place.
7. For non-open packets, identify canonical successor or owner archive path.
8. Run preservation diff before any archive/delete/untrack proposal.
9. Emit a dry-run ledger only.
10. Route blockers, owner conflicts, or destructive actions before any apply
    mode.

Minimum checks:

```bash
git status --short --ignored <target-root>
git ls-files <target-root>
git submodule status --recursive
rg -n "OPEN|Open Questions|flag|block|defer|review-required|next route|RUNTIME-HANDOFF|RUN-MANIFEST|RESULT.md|canonical_source" <target-root>
find <target-root> -path '*/node_modules' -o -path '*/.lake' -o -path '*/.venv' -o -path '*/build' -o -path '*/dist'
```

Preservation diff should compare candidate packet content against successor or
archive content and classify the result as `equivalent`, `unique-content`,
`successor-missing`, `not-needed`, or `not-run`.

## Dry-Run Ledger Contract

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
  regenerate_candidates: <n>
  handoffs: <n>
  blocked: <n>
rows:
  - path: <path>
    artifact_state: canonical-source | open-development-packet | promoted | superseded | generated | local-private | archive | blocked
    overlays:
      - owner-boundary | cleanup-candidate
    lifecycle_status: open | pass | flag | block | defer | executed | unknown
    owner_scope: <scope>
    git_state: tracked | untracked | ignored | nested-repo | submodule | mixed
    canonical_successor: <path|null>
    generated_provenance: <path|null>
    diff_result: equivalent | unique-content | successor-missing | not-needed | not-run
    proposed_action: keep | archive-candidate | delete-candidate | untrack-candidate | regenerate-candidate | handoff | block
    evidence_refs:
      - <path:line or manifest ref>
    gate: pass | flag | block
```

## Examples And Non-Examples

Examples:

- Add watcher/search excludes for `.lake`, `node_modules`, `.venv`, caches, and
  build outputs as immediate editor relief.
- Treat `.lake` and `node_modules` as generated/runtime pressure classes for
  exclusion and later owner-scoped cleanup review.
- Treat `sigils-library/` as a cleanup candidate only after preservation diff
  against its successor.
- Emit a handoff for `implementation/domainspec/` rather than parent-editing it.

Non-examples:

- Treating VS Code excludes or `.gitignore` entries as proof that deletion is
  safe.
- Parent cleanup mutating `arcanum/`, `implementation/domainspec/`,
  `projects/*`, or `validation/*` without explicit owner scope.
- Deleting packets with `OPEN`, `flag`, `block`, unresolved questions, or no
  successor.
- Deleting broad `build`, `target`, or `out` paths because they are excluded
  from search.
- Promoting cleanup output into authority, glossary, ontology, sigil, or spell
  contracts without the owning lifecycle.

## Governance Route

1. Use `discipline-governance` with target catalog `private-parent`, mode
   `scan/formalize`, and route `build-from-owned`. Adjacent anchors to inspect
   or extend are `submodule-orchestration`, `asset-ownership-propagation`,
   public `runtime-boundary`, and `development-package-promotion-gate`. The
   discipline should name the recurring practice and hardening route only; it
   must not mutate artifacts.
2. Use `constitution-governance` for modular enforceable rules. Candidate rule
   targets:
   - owner classification before cleanup: `hybrid`, with validator impact
     `required` for owner-scope detection;
   - preservation diff before deletion/archive/untrack: `hybrid`, validator
     impact `required` for dry-run ledger/diff checks;
   - generated provenance before regeneration/untracking: `hybrid`,
     validator impact `required` for provenance-field detection;
   - public/private scrub before public derivatives: `hybrid`, validator
     impact `required` or existing public-boundary scan integration;
   - open-packet retention: `review`, with future deterministic support from
     status/open-question/next-route scans;
   - promotion-patch requirements: `review` or `hybrid`, depending on whether
     successor/backlink checks become scriptable.
3. Use `sigil-development` only if the owned governance extensions still leave
   the distinct reusable lifecycle gap: dry-run ledgers, successor diffs,
   owner-scoped handoffs, observability, and reflection.
4. Use `decision-gate` for contested owner, public/private, naming, deletion,
   archive, or successor decisions.
5. Use `task-session` only for bounded apply/delete/archive/untrack work after
   dry-run and owner gates pass.

## Sigil-Development Substrate

Candidate name: `development-artifact-cleanup`.

Candidate tier: Arcana.

Core definition: a preservation-led cleanup gate that performs classification
plus proposed disposition. It does not delete by default.

Initial modes:

- `scan`: count and classify pressure/artifact classes without action.
- `dry-run`: emit ledger rows and gates for one selected root.
- `handoff`: produce owner-scoped handoffs for child-owned surfaces.
- `apply`: later only, after dry-run, preservation diff, and owner approval.
- `observe`: record outcomes, false positives, blocked gates, and corrections.

Quality bar:

- no apply without dry-run ledger;
- no deletion without successor and preservation diff;
- no open-packet removal;
- no parent mutation across owner boundaries;
- no provenance-free generated cleanup;
- no public/private ambiguity;
- no authority promotion from cleanup output.

Open questions before sigil creation:

- Should workspace excludes be applied now to `vscode-workspaces/domainspec-core.code-workspace`?
- Which owner approves stale `.claude/worktrees`, and should their cleanup use
  git worktree lifecycle commands only?
- Which `projects/*` and research sandboxes are private-parent retention zones
  versus cleanup candidates?
- What is sufficient canonical successor evidence for old development packets:
  exact migration, summarized claim migration, backlink plus diff, or owner
  archive?
- Should the future sigil start private-parent and only later be publicized
  after examples are scrubbed?
- Which checks can become deterministic validators rather than review-only
  constitution rules?

## Next Route

Recommended next route: `discipline-governance` scan/formalize for the
private-parent recurring practice, then `constitution-governance` rule selection
or composition, then `sigil-development` only for the remaining reusable dry-run
lifecycle gap.
