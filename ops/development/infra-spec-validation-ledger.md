# Infra-Spec Research Validation Ledger

Dispatch step: `validate-research-coverage` · Owner: dispatch-spec (coverage) + task-session (gate)
Date: 2026-06-08

## Coverage checks (from strategy "Validation" + `validate-research-coverage` stop-conditions)

| # | Coverage criterion | Result | Evidence |
| --- | --- | --- | --- |
| C1 | Every top-level zone classified or explicitly deferred | **pass** | `infra-spec-zone-classification-ledger.md` (38 zones); `implementation/domainspec` + `validation/poker-team` explicitly deferred |
| C2 | Every candidate concept has evidence or residue status | **pass** | `infra-spec-candidate-dag.md` (N1–N12 each: status + source/residue) |
| C3 | Every lane returned a receipt | **pass** | `infra-spec-fanout-receipts.md` (7/7, all path-cited, no-block) |
| C4 | Every child-dispatch proposal has bounded scope | **pass (held)** | 12 proposals across lane ledgers; each carries `parent_dispatch_id` + scope/roles/inputs/artifacts/stop/join/validation; **none executed** |
| C5 | No research output claims infra-spec authority | **pass** | brief, DAG, tournament all marked candidate-only; promotion_guardrails honored |
| C6 | Future schemas are YAML-first + validator-backed | **pass (deferred to next route)** | no schema created here; `infra-spec-next-route-handoff.md` specifies fixture-first `.schema.yml` |
| C7 | All 13 expected artifacts produced | **pass** | 11 written by lanes/synthesis + this ledger + next-route-handoff = 13 |
| C8 | Strategy dispatch precondition still valid | **pass** | `validate-dispatch.py` on `infra-spec-research-strategy.dispatch.json` → `VALIDATION=pass` |

## Flagged coverage gaps (honest, not silently passed)

| Flag | Detail | Disposition |
| --- | --- | --- |
| F1 | `implementation/domainspec/` submodule broken (pinned `+6f26de2` / `970dab5` not on remote) — its `infra/` is the strategy's top L3 path | **deferred**; unblock = fix upstream pointer then `git submodule update --init`; routed to child dispatches CD-L3-A, CDP-L5-1, L1-CD1 |
| F2 | `validation/poker-team/` uninitialized — canonical `ghcr.io/poker-team/backend` exemplar not inspected | **deferred**; unblock = `git submodule update --init validation/poker-team` |
| F3 | `validation/sigil-spell-sandbox` has no `.gitmodules` mapping | **flag**; repo-hygiene finding (L7 G1); owner = repo maintainer |
| F4 | Evidence layer (receipts/drift) partially blocked on real runtime instances (only goldenquill produces them) | **expected**; MVP ships operational-contract spine first (candidate DAG critical path) |

## Owner-boundary verdict

- All writes confined to `ops/development/infra-spec-*` (parent-owned). No child surface mutated. `arcanum/` submodule initialized for read-only research; pointer not committed.

## Validation verdict

**pass with flags** — research coverage is complete for the in-checkout scope; two submodule zones are explicitly deferred (not silently skipped). No output overclaims infra-spec authority. Ready for next-route handoff.

## Flag Resolution (follow-up task-session, 2026-06-08)

Operator authorized resolution via decision gate (repoint pin / init poker-team + remove stray / untrack DB + fix CI).

| Flag | Prior status | Now | Action taken |
| --- | --- | --- | --- |
| F1 implementation/domainspec broken pin | deferred | **resolved** | superproject gitlink repointed `970dab5`→`6f26de2` (origin/main, the only valid tip); working tree populated (52 entries, incl. `INFRA-SETUP.md`). Submodule now in sync + initable. NB: domainspec main has **no `infra/` dir** — infra knowledge lives in `INFRA-SETUP.md` + `.github/skills/domainspec-infra-*` + agents; the strategy's literal L3 path `implementation/domainspec/infra/` is stale. |
| F2 validation/poker-team uninitialized | deferred | **resolved** | `git submodule update --init validation/poker-team` (recorded commit `486f39a` present on remote); 28 entries. Canonical `ghcr.io/poker-team/backend` exemplar now inspectable. |
| F3 validation/sigil-spell-sandbox stray gitlink | flag | **resolved** | orphaned gitlink removed from index (`git rm --cached`) + empty dir removed; no `.gitmodules` entry existed. |
| Hygiene: committed SQLite/WAL | flag | **resolved** | `.data/*.sqlite{,-shm,-wal}` untracked (`git rm --cached`, local copy kept) + added to `.gitignore`. |
| Hygiene: drift CI coupling | flag | **resolved** | `drift-check.yml` code-tags step guarded on `implementation/domainspec/package.json`; `tools/check_github_drift.sh` now skips-with-warning (exit 0) instead of hard `exit 2` when submodules absent. With pins now valid, `bash tools/check_github_drift.sh` → PASS (exit 0). |
| F4 evidence layer blocked on instances | expected | **still open (by design)** | MVP ships operational-contract spine first; re-running L3/L6 against now-present submodules is the recommended follow-up. |

All changes are staged/working-tree only (not committed). Submodule status is now clean (arcanum, implementation/domainspec, validation/poker-team all in sync).
