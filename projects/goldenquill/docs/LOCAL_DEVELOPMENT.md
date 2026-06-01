---
title: Local Development — the real setup path
filed: 2026-05-17
audience: technical collaborator cloning the repo from cold; future-Josh after a venv rebuild
companion_docs: docs/COLLABORATOR_HANDOFF.md · docs/AGENT_CONTEXT_INDEX.md · docs/TECHNICAL_BACKLOG.md
orientation: AGENTS.md (wake-up sequence) · pipeline/SESSION_BOOTSTRAP.md (project universe)
---

# Local Development

A working setup that gets you to a green test run without guessing. If
something here is wrong because the codebase moved, fix the doc in the
same PR that surfaces the gap — that's one of the safe-first-tasks
listed in `docs/TECHNICAL_BACKLOG.md`.

## Prerequisites

- macOS on Apple Silicon (M1/M2/M3 family) or Linux. Windows is not
  currently supported for local dev; collaborators on Windows should
  use WSL2 or a Linux VM.
- **Python ≥ 3.11.** The repo's `pyproject.toml` declares
  `requires-python = ">=3.11"` and `scripts/run_tests.sh` enforces that
  floor via the venv interpreter — it does not enforce a specific
  point release. Three concrete numbers to keep straight:
  - **3.14 is Josh's local pin.** Operator-side venv is 3.14; that's
    the version this doc's setup steps create.
  - **3.11 and 3.12 are CI-supported.** The matrix at
    `.github/workflows/ci.yml` runs `quality-gate` and
    `wheel-install-smoke` against both. A PR that breaks on either CI
    Python won't merge.
  - **macOS system `python3` is 3.9 and is rejected.** It cannot even
    *collect* `@dataclass(frozen=True, kw_only=True)` modules. The
    test runner refuses to use it.

  If you have 3.11 or 3.12 instead of 3.14 locally, you can work — just
  point the venv-create step at whatever 3.11+ interpreter you have.
- `git`.
- Approximately 5 GB of disk for the venv plus model weights for the
  spaCy NER dependency.
- A working `/opt/homebrew/bin/python3.14` (Apple Silicon Homebrew path).
  If you installed Python 3.14 via `python.org` or `pyenv`, point your
  venv creation at that interpreter; the script error message has the
  expected paths.

## Setup

```bash
# 1. Clone the repo
git clone <your-fork-or-the-main-repo-url> GoldenQuill
cd GoldenQuill

# 2. Create the pinned venv (Python 3.14)
/opt/homebrew/bin/python3.14 -m venv .venv

# 3. Activate
source .venv/bin/activate

# 4. Install the package in editable mode with dev extras
.venv/bin/pip install --upgrade pip wheel
.venv/bin/pip install -e '.[dev]'

# 5. Download the spaCy NER model (required for F-LOGICIAN-FABRICATED-ORG gate)
.venv/bin/python -m spacy download en_core_web_sm
```

The install command — `pip install -e '.[dev]'` — is the canonical form;
it reads `pyproject.toml` for the dependency set (cryptography, pyyaml,
feedparser, idna, spacy, rapidfuzz, python-docx, pypdf, openpyxl,
weasyprint, plus the dev extras). There is no `requirements.txt` — the
project ships its dependencies through `pyproject.toml`.

## Verification

Two scripts, both should exit clean:

```bash
# Tests — pins the interpreter to .venv/bin/python3 (3.14)
scripts/run_tests.sh

# AST lint — same interpreter pin
scripts/run_lint.sh pipeline
```

Both scripts will error with a clear message if the venv is missing or
points at the wrong Python. Do not work around the error by calling
`pytest` directly with system Python — you will see 8 collection errors
that look like real test failures but are actually a 3.9-vs-3.10+
incompatibility (per the CLAUDE.md "Running tests — PINNED INTERPRETER"
section).

## Expected pass counts at 2026-05-17

The numbers below are from the §4 v2.x.6 runtime companion landing
session on 2026-05-17 (see `daily_logs/2026-05-17.md` for the full
write-up). Numbers will drift as the codebase evolves; treat these as
the calibration point for "is my local setup green."

- `scripts/run_tests.sh tests/orchestrator/` → **66 passed** in ~0.5s.
- `scripts/run_tests.sh tests/linting/` → **267 passed** in ~6.5s.
- `scripts/run_tests.sh tests/seats/` → **3004 passed / 3 failed**.
  The 3 failures are *pre-existing capstone-hash drift* surfaced by the
  §4 v2.x.6 daily-log entry, not regressions — they live in the 163-file
  WIP touching `pipeline/seats/red_team/{provider_groq,seat,types}.py`
  (capstone §10 LOCKed-set pin) plus the
  `section_07_scribe.md BLUEPRINT_DEPS` pin in the judge `__init__`.
  Surface, do not paper over.
- `scripts/run_lint.sh pipeline` → exit 0 (no AST-lint violations).

Earlier focused-suite numbers from the lock-and-clear packet (e.g., the
2026-05-11 v0.1 smoke suite at 339 tests passed) are historical; the
PR #4 merge commit body records `10,584 passed / 3 skipped / 1 xfailed`
as the canonical CI-green baseline for the broader matrix.

## Common local failures

1. **Wrong Python version.** The macOS-default `python3` is 3.9; calling
   `python3 -m pytest` directly will produce 8 collection errors before
   any test runs. The fix is always to use `scripts/run_tests.sh` (which
   pins the venv interpreter) or to call `.venv/bin/python3 -m pytest`
   directly.

2. **`.venv/bin/python3.14` symlink broken in a Cowork sandbox.** In
   some Cowork sandbox environments the venv created by a previous
   session has a stale symlink. If `.venv/bin/python3 --version` errors
   out, rebuild: `rm -rf .venv && /opt/homebrew/bin/python3.14 -m venv
   .venv && .venv/bin/pip install -e '.[dev]'`.

3. **Logfire bootstrap order.** Logfire is disabled-by-default at v0.1
   (CC-008 in the QA/QC remediation pack) and must not be imported
   before the env-bootstrap step. The AST-lint rule
   `R-INTAKE-NO-LOGFIRE-IMPORT-BEFORE-ENV` catches the static case; a
   runtime "Logfire token missing" or "telemetry already initialized"
   error means the bootstrap order is wrong. The Intake module is the
   canonical example — see `pipeline/orchestrator/seats/intake.py`
   (orchestrator seat) and `pipeline/cli/tilth_intake.py` (CLI entry
   point), plus the lint rule at
   `pipeline/linting/r_intake_no_logfire_import_before_env.py`.

4. **Missing system libs for weasyprint.** On Linux, weasyprint needs
   `libpango-1.0-0`, `libpangoft2-1.0-0`, `libcairo2`, `libgdk-pixbuf-2.0-0`
   (the CI workflow installs these via `apt-get`). On macOS the Homebrew
   `cairo` and `pango` formulas cover this. If your test run errors out
   in the §17 WPFA path, this is usually why.

5. **spaCy model not downloaded.** Step 5 of setup is non-optional. The
   gate at `pipeline/logician/gates/f_logician_fabricated_org.py` has
   lazy imports and returns FAIL with reason `spacy_unavailable` if the
   model isn't present; the test suite will surface this as a clean
   failure with a clear message.

## What CI proves that local Mac tests may not

Local Mac tests on 3.14 are necessary but not sufficient. CI proves:

- **Cross-Python-version matrix.** `quality-gate (3.11)` and
  `quality-gate (3.12)` exercise both supported lower bounds; some
  syntax and stdlib differences (e.g., the 3.11 `tomllib` stdlib
  addition, 3.12 type-parameter syntax) won't surface on 3.14.
- **Wheel-smoke.** `wheel-install-smoke (3.11)` and
  `wheel-install-smoke (3.12)` build the wheel and import the CLI from
  the installed package, catching the class of "works in editable
  install but not after a real install" bugs that `pip install -e .`
  hides.
- **AST-lint over the full pipeline tree.** CI runs
  `scripts/run_lint.sh pipeline` on every PR; a violation introduced
  outside the tree you happened to touch locally still blocks merge.
- **Serial pytest under the canonical CI runner.** CI runs the suite in
  `--tb=short` form on Ubuntu; some macOS-only path or filesystem
  assumptions will fail on Linux that pass locally.

The four required checks at branch protection are
`quality-gate (3.11)`, `quality-gate (3.12)`,
`wheel-install-smoke (3.11)`, `wheel-install-smoke (3.12)`. "Green on
my Mac" is not "green on CI" by default. Wait for the matrix.

## Where to go when stuck

The wake-up sequence in `AGENTS.md` (`SOUL.md` → `USER.md` →
`router.yaml` → last two daily logs → `lessons.md` → `MEMORY.md`) is
the canonical orientation. After that:

- **`pipeline/SESSION_BOOTSTRAP.md`** — compresses the project universe
  for fast context-load.
- **`lessons.md`** — institutional memory. If you hit a problem that
  looks like a known pattern, search here first. L-001 through L-023
  are the live entries as of 2026-05-16.
- **`docs/tilth_full_audit_prompt_v1_1.md`** — systematic-diagnosis
  audit playbook. Walk it section by section when something is broken
  and you can't tell why.
- **`docs/AGENT_CONTEXT_INDEX.md`** — the per-file map of the root
  wake-up files (what each is for, who reads it).
- **`daily_logs/`** — the narrative thread. The most recent two are
  always worth reading on session-start; for deeper history, search the
  log dated nearest the system you're working on.

If you discover a setup step this doc missed, fix the doc in the same
PR that surfaces the gap. The cleanup plan v1.1 explicitly lists
README polish and LOCAL_DEVELOPMENT.md improvements as collaborator
safe-first-tasks.
