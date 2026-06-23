#!/usr/bin/env sh
set -eu

BASE_URL="${1:-${BODY_WAR_PUBLIC_BASE_URL:-}}"
if [ "$BASE_URL" = "" ]; then
  echo "usage: $0 https://troqar.example.com" >&2
  exit 2
fi

BASE_URL="${BASE_URL%/}"

echo "checking $BASE_URL/api/status"
curl -fsS "$BASE_URL/api/status" >/dev/null

echo "checking first page"
curl -fsS "$BASE_URL/" | grep -q "Bora correr"

echo "checking no obvious secret terms on first page"
if curl -fsS "$BASE_URL/" | grep -Eiq "access_token|refresh_token|client_secret|oauth code"; then
  echo "secret-like term rendered on first page" >&2
  exit 1
fi

echo "online smoke: pass"
