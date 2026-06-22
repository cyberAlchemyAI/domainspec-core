#!/usr/bin/env sh
set -eu

cd "$(dirname "$0")/.."

if [ ! -d node_modules ]; then
  echo "node_modules missing; run npm install in projects/auth-user-management" >&2
  exit 2
fi

npm run build
npm test

if find src tests -name '*.py' -print | grep -q .; then
  echo "Python files are not allowed in auth-user-management runtime/tests" >&2
  find src tests -name '*.py' -print >&2
  exit 1
fi
