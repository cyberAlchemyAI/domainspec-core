#!/usr/bin/env bash
# Pinned AST-lint runner (ARCH-04).
#
# Pins the interpreter to .venv/bin/python3 for the same reason as
# scripts/run_tests.sh — system Python 3.9 cannot collect the module.
#
# Usage:
#   scripts/run_lint.sh                      # lint the live pipeline/ tree
#   scripts/run_lint.sh path/to/subtree      # lint a narrower root
#
# Exit codes:
#   0 — zero violations
#   1 — one or more violations (printed to stderr, one per line)
#   2 — environment/setup error (wrong venv, missing interpreter)
#
# Output format (stderr, per violation):
#   <file>:<line>:<col>: <RULE_NAME> [<reason_tag>] <message>

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
exec "$VENV_PY" -m pipeline.linting.ast_lint "$@"
