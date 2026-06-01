#!/usr/bin/env bash
# Tilth Pipeline — single-shot organism pass.
#
# Usage:
#   bash skills/tilth-pipeline/run.sh [client_slug]
#
# Chains Scout live-API discovery into the pipeline scorer + DB write-back.
# Fail-closed on Scout failure — pipeline still runs on whatever Scout saved
# so the organism records the partial pass.
#
# Law 3: one client slug per invocation.
set -u

CLIENT_SLUG="${1:-mycosymbiotics_inc}"

# resolve workspace root relative to this script
HERE="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
ROOT="$(cd "$HERE/../.." && pwd)"
cd "$ROOT"

STAMP="$(date -u +%Y-%m-%dT%H:%M:%SZ)"
echo "── Tilth Pipeline ─────────────────────────────────────────────"
echo "  client:    ${CLIENT_SLUG}"
echo "  workspace: ${ROOT}"
echo "  started:   ${STAMP}"
echo "───────────────────────────────────────────────────────────────"

SCOUT_RC=0
echo "[1/2] Scout live-API pass..."
python3 pipeline/tilth/scout_live.py --client "${CLIENT_SLUG}" || SCOUT_RC=$?

if [ "$SCOUT_RC" -ne 0 ]; then
  echo "!! Scout exited with code ${SCOUT_RC} — continuing pipeline on last saved radar."
fi

echo "[2/2] Tilth pipeline scoring + DB write-back..."
python3 pipeline/tilth/tilth_pipeline.py --client "${CLIENT_SLUG}"
PIPE_RC=$?

FINISHED="$(date -u +%Y-%m-%dT%H:%M:%SZ)"
echo "───────────────────────────────────────────────────────────────"
echo "  finished:  ${FINISHED}"
echo "  scout_rc:  ${SCOUT_RC}"
echo "  pipe_rc:   ${PIPE_RC}"
echo "───────────────────────────────────────────────────────────────"
exit "$PIPE_RC"
