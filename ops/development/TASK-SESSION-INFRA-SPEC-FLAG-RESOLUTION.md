# Task Session: Resolve Infra-Spec Coverage-Gap & Hygiene Flags

Date: 2026-06-08 · Branch: `codex/infra-spec`
Task: resolve the flags raised by the infra-spec strategy execution (next-step "clear the coverage gap" + repo hygiene).
Result: **PASS**

## Scope (one bounded task)

Resolve F1–F4 + parent-owned hygiene from `infra-spec-next-route-handoff.md` / `…-validation-ledger.md`. No infra-spec package creation; no schema authoring (those remain separate next routes).

## Decisions (3, all gated before mutation)

| Decision | Chosen | Owner-boundary note |
| --- | --- | --- |
| F1 domainspec broken pin | repoint gitlink to origin/main + populate | gitlink is superproject (parent) metadata; the pinned commit was gone upstream, so only the parent can restore a valid pin |
| F2/F3 | init poker-team + remove stray gitlink | poker-team recorded commit present on remote; stray gitlink had no `.gitmodules` mapping |
| Hygiene | untrack DB + fix CI | `.data/` and root `.github`/`tools` are parent-owned |

## Execution + validation

| Flag | Action | Validation |
| --- | --- | --- |
| F1 | gitlink `970dab5`→`6f26de2`; worktree populated (52 entries) | `git submodule status` clean; `INFRA-SETUP.md` present |
| F2 | init `validation/poker-team` @ `486f39a` | 28 entries; in sync |
| F3 | removed stray `validation/sigil-spell-sandbox` gitlink + dir | gone from index |
| SQLite | untracked `.data/*.sqlite{,-shm,-wal}` + `.gitignore` | `git check-ignore` confirms ignored; no longer tracked |
| drift CI | guarded pnpm step + script skips-with-warning when submodules absent | `bash tools/check_github_drift.sh` → `PASS` exit 0 |

Precondition unchanged: `infra-spec-research-strategy.dispatch.json` still `VALIDATION=pass`.

## Finding surfaced

The strategy's L3 starting path `implementation/domainspec/infra/` is **stale** — domainspec `main` has no `infra/` dir; infra knowledge lives in `INFRA-SETUP.md` + `domainspec-infra-*` skills/agents. Recommend updating the strategy's L3 known-paths on the next refine, and re-running L3/L6 against the now-present submodules.

## Files updated (staged/working-tree; not committed)

- repointed: `implementation/domainspec` gitlink (→6f26de2)
- initialized: `validation/poker-team`
- removed: `validation/sigil-spell-sandbox` gitlink, `.data/*.sqlite{,-shm,-wal}` (untracked)
- edited: `.gitignore`, `.github/workflows/drift-check.yml`, `tools/check_github_drift.sh`
- updated: `ops/development/infra-spec-validation-ledger.md` (flag-resolution section)

## Owner boundary

All edits parent-owned (superproject gitlinks, root `.github`/`tools`, `.data`, `.gitignore`, `ops/`). Submodule *contents* not modified. arcanum pointer untouched.

## Follow-up (not in this task)

- Re-run lanes L3 + L6 against now-present submodules (child dispatches CD-L3-A, CD-L6-1) to close F4's evidence gap.
- Update the strategy `.md` L3 known-paths (stale `infra/` path).
- Fixture-first MVP infra-spec schema design (separate route).
