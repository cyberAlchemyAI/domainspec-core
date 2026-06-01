# Git Workflow

Commit conventions and branching strategy for the Golden Quill / Tilth repository.

## Branching Model: Trunk-Based

Development happens on `main`. No long-lived feature branches. Short-lived working branches are acceptable for multi-session work but merge back to `main` within days, not weeks.

Why trunk-based: solo operator, single pipeline, linear dependency chain. Branch complexity doesn't add value — it adds merge debt.

## Commit Discipline

### Atomic commits

Each commit represents one logical change. A commit should be independently understandable — someone reading `git log --oneline` should know what changed without opening the diff.

### Size target: ~100 lines per commit

This is a guideline, not a hard rule. The intent is commits small enough to review in one pass. A 300-line commit that's all test functions for one module is fine. A 100-line commit that touches five unrelated files is not.

### Commit as save point

Commit early, commit often. A commit is a save point, not a publication. You can always squash before pushing if the intermediate states aren't useful to preserve.

### Commit message format

```
<scope>: <imperative description>

<optional body — what and why, not how>
```

**Scope** is the pipeline section or component:

- `§1` through `§10` for blueprint sections
- `arch` for architecture documents
- `logician` for validation gates
- `scout`, `scribe`, `editor`, `judge` for council seats
- `pipeline` for orchestration (Section 5)
- `tests` for test-only changes
- `docs` for documentation
- `infra` for build/CI/tooling

**Examples:**

```
§5: add rate_limiter module with token bucket + Groq tier awareness

logician: implement F-AMDT-12 daily_log_lock_block_missing gate

§3: land Scout Round 9 verify_stage — 142 tests, 1065 LOC

docs: add architecture overview for repo init

tests: add adversarial coverage for vault compound transactions
```

## Tags for LOCKs

When a section or component is LOCKED (passed its audit rounds and is considered frozen), tag the commit:

```
git tag -a lock/§1-sovereignty-v5 -m "§1 Sovereignty Envelope LOCKED — Round J capstone, 214 tests"
git tag -a lock/arch-v7 -m "Architecture v7 LOCKED — A1-A12, two audit rounds"
```

Tag naming convention: `lock/<section>-<version>`

Tags are the audit trail in git. They correspond to rows in `pipeline/engineering/lock_history.v1.jsonl`.

## What Gets Committed

**Always commit:**

- Source code under `pipeline/`, `logician/`
- Test files under `tests/`
- Architecture and blueprint documents
- Lock history (`pipeline/engineering/lock_history.v1.jsonl`)
- `router.yaml` (model bindings)
- Documentation (`docs/`)
- `pyproject.toml`, `scripts/`

**Never commit:**

- `.env` or any file containing API keys
- `orgs/*/vault/` (client data — Law 3)
- `orgs/*/PROJECT_CONTEXT.md` (client-specific data)
- Session metrics (`pipeline/metrics/session_log.jsonl`)
- `daily_logs/` (operational, not architectural)
- `memory/` (session-specific working memory)
- `.venv/`, `__pycache__/`, `.pytest_cache/`
- Machine-specific calibration artifacts

## Pull Request Discipline

If working with collaborators (future state — v0.1 is solo):

- Every PR gets a cross-family code review (the reviewer's model family differs from the author's, per L-003)
- Tests must pass before merge
- AST lint must pass
- No PR merges with `[NEEDED]` placeholders in committed files

## Initial Commit Strategy

The initial push includes:

1. Public documentation (README, docs/)
2. `.gitignore`
3. Core pipeline code and tests
4. Architecture and blueprint documents
5. Lock history (audit trail)
6. `router.yaml`

Client org data, daily logs, memory files, and session metrics are excluded per `.gitignore`.
