#!/usr/bin/env bash
set -euo pipefail

runtime_dir="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
fixture_dir="$runtime_dir/tests/fixtures"

if rg -n 'socket|urllib|requests|curl|wget|git[[:space:]]+clone|npm[[:space:]]+ci|node-gyp|arcanum/(arcana|development)/craft' \
  "$fixture_dir/fixture_driver.py" "$fixture_dir/cases.json"; then
  printf 'FIXTURE_STATIC_EFFECT_SCAN=block\n' >&2
  exit 1
fi

python3 "$fixture_dir/fixture_driver.py" \
  --validator "$runtime_dir/validate_source_build.py" \
  --schema "$runtime_dir/source-build-receipt.schema.json" \
  --cases "$fixture_dir/cases.json"

printf 'FIXTURE_STATIC_EFFECT_SCAN=pass\n'

