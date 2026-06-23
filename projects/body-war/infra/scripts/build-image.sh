#!/usr/bin/env sh
set -eu

if [ "${1:-}" = "" ]; then
  echo "usage: $0 <image-tag> [image-repository]" >&2
  exit 2
fi

IMAGE_TAG="$1"
IMAGE_REPOSITORY="${2:-ghcr.io/domainspec/body-war-app}"
SCRIPT_DIR="$(CDPATH= cd -- "$(dirname -- "$0")" && pwd)"
REPO_ROOT="$(CDPATH= cd -- "$SCRIPT_DIR/../../../.." && pwd)"

case "$IMAGE_TAG" in
  *[!A-Za-z0-9_.-]* | "" | "." | "..")
    echo "invalid image tag" >&2
    exit 2
    ;;
esac

docker build \
  --file "$REPO_ROOT/projects/body-war/app/Dockerfile" \
  --tag "$IMAGE_REPOSITORY:$IMAGE_TAG" \
  "$REPO_ROOT"
