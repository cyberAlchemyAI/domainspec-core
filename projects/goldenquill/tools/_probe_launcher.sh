#!/bin/bash
# Launcher for code_review_probe — backgrounds the probe and disowns it
# so we can poll for completion without blocking osascript.
# Portable: derive workspace root from this script's location.
# Override via QUILL_WORKSPACE env var if needed.
# Pinned interpreter policy (CLAUDE.md): use .venv/bin/python3, never system python3.
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
WORKSPACE="${QUILL_WORKSPACE:-$(dirname "$SCRIPT_DIR")}"
cd "$WORKSPACE" || exit 1
PYBIN="${WORKSPACE}/.venv/bin/python3"
if [ ! -x "$PYBIN" ]; then
  echo "ERROR: pinned interpreter not found at $PYBIN" >&2
  exit 1
fi
nohup "$PYBIN" tools/code_review_probe.py > /tmp/quill_probe_rerun.log 2>&1 &
PROBE_PID=$!
echo "$PROBE_PID" > /tmp/quill_probe_rerun.pid
disown
echo "PID:$PROBE_PID"
