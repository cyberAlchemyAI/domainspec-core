# Refined Synthesis: Surface Blockers And Gaps

Date: 2026-05-31
Status: pass

## Refined Target

The cleanup is no longer blocked by the native-first contract or by whether personal Codex may be updated. Those are resolved:

- Native runtime skills/packages are primary.
- `tools/arcanum` is deterministic support.
- Personal Codex refresh is approved as stage, compare, then promote.

The remaining blocker space is not one large repository-organization question. It is five decision groups with different scopes.

## Blocker Decisions

1. Personal Codex promotion safety: how to preserve rollback evidence before replacing active Arcanum skill packages.
2. GitHub/Copilot runtime cache fate: keep, delete, or untrack `.arcanum/runtimes/github-copilot` after `.github/skills/arcanum-*` is self-provenanced.
3. Root `.github/skills` duplicate fate: what to do with DomainSpec/GSD duplicate skill packages classified as `gate-delete`.
4. Root `.arcanum` generated state policy: whether generated observability ledgers and reflection state should stay local/ignored, be selectively promoted, or be tracked by default.
5. Repository organization legacy path fate: how to handle `cyberAlchemy/`, `projects/body-war/`, `research/projects/hermes-agent/repo`, and legacy `sigils-library` remnants before broad cleanup.

## Deferrable Gaps

- Exact separate provenance manifest file shape, because current generated frontmatter fields already provide a minimum promotion contract.
- Root `.agents/skills/arcanum-*` symlink facade, because it is not needed for the immediate native runtime package route.
- Full runtime-surface inventory JSON, because current markdown inventories are sufficient for the next task-session.
- Organization validation script, because it can follow after decisions stabilize.
- README refresh, because it should happen after zone and surface decisions are accepted.
- DomainSpec-owned runtime helper migration, because parent cleanup must not mutate submodule-owned surfaces.

## Assumptions For Next Work

- Staging can be repository-local or temporary, but promotion must touch only generated Arcanum personal skill packages and aliases.
- Historical development evidence that mentions command-backed execution is preserved unless a cleanup task explicitly owns it.
- Root command adapter deletions remain valid unless a compatibility task reopens them.
- DomainSpec, GSD, nested Arcanum, and project-owned surfaces are protected from broad parent cleanup.
- `sigils-library` is a legacy Arcanum name, not a second canonical source.

## Recommended Route

The five blocker decision groups were resolved by the recommended set:

- 1A: back up replaced personal Codex Arcanum skill packages before promotion.
- 2B: untrack and regenerate `.arcanum/runtimes/github-copilot` on demand after `.github/skills` is self-provenanced.
- 3A: keep root duplicate GitHub skills until runtime confirmation.
- 4A: ignore generated observability ledgers by default and promote selectively.
- 5C: treat legacy Arcanum names as delete candidates after targeted diff.

Proceed to `task-session` for `TASK-SURFACE-002 / SWU-SURFACE-002`.
