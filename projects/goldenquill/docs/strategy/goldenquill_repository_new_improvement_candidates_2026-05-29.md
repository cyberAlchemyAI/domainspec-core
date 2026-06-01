---
title: GoldenQuill Net-New Improvement Candidates
date: 2026-05-29
dispatch: goldenquill-repository-research-20260529
status: tournament-output
---

# Net-New Improvement Candidates

## Tournament Result

| Candidate | Status | Duplicate Check | Evidence | Validation |
| --- | --- | --- | --- | --- |
| Current-truth refresh pack | partial-overlap / net-new detail | Existing docs call for front-door truth, but row 292/key-rotation stale state is newly identified in this run. | `PROJECT_STATUS.md`, `RUNTIME_MATURITY_MATRIX.md`, `ACTIVE_BLUEPRINT_INDEX.md`, `lock_history.v1.jsonl`, `vault_shared/cards/publisher_pubkey.signed.yaml` | Diff front-door claims against ledger max row and current key asset. |
| Product surface index | net-new | Not found as a single existing artifact. | `docs/FRONTEND_BOUNDARY.md`, `apps/`, `landing/`, `docs/whitepapers/` | Create docs-only table; no source edits. |
| Implementation-status matrix | net-new | Not found as a single existing artifact. | `skills/`, `pipeline/cli/`, modules, tests, maturity matrix | Build crosswalk and sample-verify entries. |
| Wheel packaging smoke for substrate | net-new | Related CI hardening exists, but substrate import omission is newly specific. | `pyproject.toml`, `golden_quill_substrate/`, CI wheel smoke | Add failing/passing install smoke in temp venv. |
| Unified local verification wrapper | partial-overlap | Existing `run_tests.sh` and `run_lint.sh`; no single wrapper found. | `scripts/`, `.github/workflows/` | Wrapper returns nonzero on any failed check. |
| Whitepaper format hygiene | net-new | No explicit whitepaper format issue found. | `docs/whitepapers/*` | `file` output and canonicality review. |

## Rejected Or Deferred

- Direct Cedar runtime integration: important, but already a known v0.2/governed substrate decision.
- FD broker SCM_RIGHTS/bind-mount namespace work: important, but security architecture work requiring deeper Gate 2 prioritization.
- Landing page rebuild: useful, but depends on Josh decisions about customer-facing language and current design direction.
- Direct implementation against stale front-door docs: blocked until current-truth refresh lands.

## Candidate Rules

Any candidate marked net-new must keep:

- concrete path evidence,
- prior-art check,
- owner surface,
- validation path,
- next route.
