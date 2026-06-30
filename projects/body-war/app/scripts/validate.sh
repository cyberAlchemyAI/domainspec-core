#!/usr/bin/env sh
set -eu

cd "$(dirname "$0")/.."

fail() {
  echo "FAIL: $*" >&2
  exit 1
}

npm run build
npm test
npm run db:generate

if find server.ts src tests e2e -name '*.py' -type f -print | grep -q .; then
  find server.ts src tests e2e -name '*.py' -type f -print >&2
  fail "BodyWar app runtime and tests must stay TypeScript"
fi

if rg -n 'CREATE TABLE "?auth_' drizzle src tests e2e; then
  fail "BodyWar app must not hand-write or generate auth package tables"
fi

for table in body_war_runner_profiles body_war_oauth_states body_war_provider_accounts body_war_provider_tokens body_war_suggested_tracks body_war_activity_evidence_candidates; do
  if ! rg -n "$table" drizzle >/dev/null; then
    fail "missing Drizzle-generated BodyWar table in migrations: $table"
  fi
done

if rg -n 'sk_live_|xox[baprs]-|AKIA[0-9A-Z]{16}|-----BEGIN (RSA |EC |OPENSSH )?PRIVATE KEY-----' \
  server.ts src tests e2e drizzle README.md \
  --glob '!**/node_modules/**' \
  --glob '!**/dist/**' \
  --glob '!**/dist-test/**' \
  --glob '!**/.runtime/**'; then
  fail "possible real secret material found in tracked BodyWar app artifacts"
fi

echo "BodyWar app validation passed."
