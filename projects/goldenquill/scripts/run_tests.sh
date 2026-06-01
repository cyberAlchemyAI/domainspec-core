#!/usr/bin/env bash
# Pinned test runner.
#
# Pins the interpreter to .venv/bin/python3 (Python 3.14) to avoid the
# silent failure mode where the system `python3` on macOS (3.9) cannot
# collect `@dataclass(frozen=True, kw_only=True)` modules and reports
# 8 collection errors that look like real test failures.
#
# Usage:
#   scripts/run_tests.sh                    # full suite
#   scripts/run_tests.sh tests/gpp          # subset
#   scripts/run_tests.sh -k manifest        # keyword filter
#
# The pinned venv is built from Python 3.14 (pyproject requires >=3.11);
# system Python 3.9 is rejected by this script with a clear error.

set -euo pipefail

REPO_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
VENV_PY="$REPO_ROOT/.venv/bin/python3"

if [[ ! -x "$VENV_PY" ]]; then
    echo "error: $VENV_PY not found — rebuild the venv:" >&2
    echo "  /opt/homebrew/bin/python3.14 -m venv .venv" >&2
    echo "  .venv/bin/pip install -e '.[dev]'" >&2
    exit 2
fi

PY_VERSION="$("$VENV_PY" -c 'import sys; print(f"{sys.version_info.major}.{sys.version_info.minor}")')"
PY_MAJOR="${PY_VERSION%%.*}"
PY_MINOR="${PY_VERSION##*.}"
if [[ "$PY_MAJOR" -lt 3 || ( "$PY_MAJOR" -eq 3 && "$PY_MINOR" -lt 11 ) ]]; then
    echo "error: .venv/bin/python3 is $PY_VERSION; pyproject requires >=3.11" >&2
    echo "  rebuild with: /opt/homebrew/bin/python3.14 -m venv .venv" >&2
    exit 2
fi

cd "$REPO_ROOT"
exec "$VENV_PY" -m pytest "$@"
