#!/usr/bin/env bash
# MEMORY.md auto-consolidation trigger — wake-up sequence preflight.
#
# Invokes the `tilth memory auto-trigger` CLI to check whether MEMORY.md
# has grown past the early-warning threshold (default 200 lines / 12 KiB).
# Intended to be called from the wake-up sequence (per AGENTS.md step 6)
# or from a scheduled task. Defaults are conservative; override via env
# vars or CLI flags.
#
# Exit codes (matches the CLI):
#   0  — under threshold; no action needed
#   10 — trigger fired; agent should invoke the `consolidate-memory`
#        skill OR re-run with --run to consolidate inline
#   1  — error
#
# Env vars:
#   MEMORY_TRIGGER_LINES  — int line threshold (default 200)
#   MEMORY_TRIGGER_BYTES  — int byte threshold (default 12288)
#   MEMORY_PATH           — path to MEMORY.md (default $REPO_ROOT/MEMORY.md)
#   MEMORY_TRIGGER_LOG    — JSONL log path (default
#                           $REPO_ROOT/pipeline/institutional_memory/
#                           memory_consolidation_log.jsonl)
#
# Usage:
#   scripts/memory_size_check.sh                  # signal-only check
#   scripts/memory_size_check.sh --run            # consolidate inline
#   scripts/memory_size_check.sh --json-output    # machine-readable
#   scripts/memory_size_check.sh --threshold-lines 250

set -euo pipefail

REPO_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
VENV_PY="$REPO_ROOT/.venv/bin/python3"

if [[ -x "$VENV_PY" ]]; then
    PY="$VENV_PY"
else
    PY="python3"
fi

cd "$REPO_ROOT"

exec "$PY" -m pipeline.cli.tilth_memory auto-trigger "$@"
