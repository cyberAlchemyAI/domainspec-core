#!/bin/bash
export PATH=/Users/goldenquill/.npm-global/bin:/opt/homebrew/opt/node/bin:$PATH

echo "=== GATEWAY CLI SURFACE ==="
openclaw gateway --help 2>&1 | head -25
echo "---"
openclaw daemon --help 2>&1 | head -20

echo ""
echo "=== SMOKE TEST 1: LOCAL EXECUTION (bypasses daemon cache) ==="
openclaw infer model run --local --model editor --prompt "Reply with exactly: OK" 2>&1 | head -20

echo ""
echo "=== SMOKE TEST 2: GATEWAY EXECUTION (hits daemon cache) ==="
openclaw infer model run --gateway --model editor --prompt "Reply with exactly: OK" 2>&1 | head -20

echo ""
echo "=== SMOKE TEST 3: NO FLAG (default path) ==="
openclaw infer model run --model editor --prompt "Reply with exactly: OK" 2>&1 | head -20
