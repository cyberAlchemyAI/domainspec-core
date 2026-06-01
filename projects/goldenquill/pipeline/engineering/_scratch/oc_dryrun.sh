#!/bin/bash
export PATH=/Users/goldenquill/.npm-global/bin:/opt/homebrew/opt/node/bin:$PATH

BATCH=/Users/goldenquill/Downloads/GoldenQuill/pipeline/engineering/_scratch/openclaw_cross_family_allowlist_batch.json

echo "=== D.1 DRY-RUN ==="
echo "--- Batch file content ---"
cat "$BATCH"
echo
echo "--- Dry-run ---"
openclaw config set --batch-file "$BATCH" --dry-run --strict-json 2>&1
echo "--- Validate pre-change ---"
openclaw config validate --json 2>&1 | head -10
