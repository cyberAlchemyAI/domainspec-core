---
taskId: TASK-OCA-05
swuId: SWU-OCA-005
status: planned
layer: L1
wave: W5
---

# Generated Orchestrate parity

## Objective and boundary

Regenerate the supported Codex, repository-local, and Claude Orchestrate
packages from canonical Arcanum after all canonical SWUs pass. Generated files
are projections, never authoring authority.

Primary behavior: manifest-declared generated source/support bytes reproduce
canonical capacity behavior.

Independent acceptance boundary: generation in an isolated temporary target
followed by exact-directory comparison proves parity without replacing the
repository skill surface.

## Exact future write scope

- `.agents/skills/orchestrate/**`
- `.arcanum/runtime/orchestrate/**`
- `.claude/skills/orchestrate/**`

Inputs are canonical `arcanum/runtime/orchestrate/**` and the Arcanum bootstrap
manifest. Tests/caches are not copied unless the manifest explicitly owns them.

## Implementation detail

1. Create an isolated temporary target.
2. Run `arcanum/tools/bootstrap_arcanum.sh` there with profiles
   `repo-codex,repo-local,claude` and the minimum required sigil selector.
3. Review source-to-target manifests and diffs.
4. Sync only the three exact Orchestrate package directories.
5. Prove byte parity of declared support files and absence of test/cache leaks.

Never run a partial `bootstrap_arcanum.sh --force --target .` into this working
repository and never hand-edit projections to make tests pass.

## Done and evidence

- bootstrap-generation test passes;
- all three generated package manifests match canonical inputs;
- no unrelated generated package changes;
- canonical and generated boundary scans pass.

Dependencies: OCA-001 through OCA-004. Owner: Arcanum generation owner.
Closeout uses the `SWU-OCA-005` row and may hand off to read-only verification,
but cannot claim publication or release.
