#!/usr/bin/env sh
set -eu

APP_DIR="${TROQAR_APP_DIR:-/srv/troqar}"
ENV_FILE="${TROQAR_ENV_FILE:-$APP_DIR/.env}"
COMPOSE_FILE="${TROQAR_COMPOSE_FILE:-$APP_DIR/docker-compose.traefik.yml}"
RECEIPT_DIR="${TROQAR_RECEIPT_DIR:-$APP_DIR/receipts}"

usage() {
  echo "usage: troqar-deploy-agent <image-tag>" >&2
}

IMAGE_TAG="${1:-}"
if [ "$IMAGE_TAG" = "" ]; then
  usage
  exit 2
fi

case "$IMAGE_TAG" in
  *[!A-Za-z0-9_.-]* | "." | "..")
    echo "invalid image tag" >&2
    exit 2
    ;;
esac

if [ ! -r "$ENV_FILE" ]; then
  echo "missing env file: $ENV_FILE" >&2
  exit 1
fi

if [ ! -r "$COMPOSE_FILE" ]; then
  echo "missing compose file: $COMPOSE_FILE" >&2
  exit 1
fi

mkdir -p "$RECEIPT_DIR"
RECEIPT_FILE="$RECEIPT_DIR/deploy-$(date -u +%Y%m%dT%H%M%SZ).md"

{
  echo "# TROQAR Deploy Receipt"
  echo
  echo "- Timestamp: $(date -u +%Y-%m-%dT%H:%M:%SZ)"
  echo "- Image tag: $IMAGE_TAG"
  echo "- Compose file: $COMPOSE_FILE"
  echo "- Env file: server-owned, not printed"
  echo
} > "$RECEIPT_FILE"

echo "deploying image tag $IMAGE_TAG"

IMAGE_TAG="$IMAGE_TAG" docker compose --env-file "$ENV_FILE" -f "$COMPOSE_FILE" pull app
IMAGE_TAG="$IMAGE_TAG" docker compose --env-file "$ENV_FILE" -f "$COMPOSE_FILE" up -d postgres
IMAGE_TAG="$IMAGE_TAG" docker compose --env-file "$ENV_FILE" -f "$COMPOSE_FILE" run --rm app \
  node dist/src/infrastructure/postgres/migrate-cli.js
IMAGE_TAG="$IMAGE_TAG" docker compose --env-file "$ENV_FILE" -f "$COMPOSE_FILE" up -d app

PUBLIC_BASE_URL="$(awk -F= '/^BODY_WAR_PUBLIC_BASE_URL=/{print $2; exit}' "$ENV_FILE")"
STATUS_URL="${PUBLIC_BASE_URL%/}/api/status"

if curl -fsS "$STATUS_URL" >/dev/null; then
  echo "- Health: pass" >> "$RECEIPT_FILE"
  echo "health: pass"
else
  echo "- Health: fail" >> "$RECEIPT_FILE"
  echo "health: fail" >&2
  exit 1
fi

echo "- Result: pass" >> "$RECEIPT_FILE"
echo "receipt: $RECEIPT_FILE"
