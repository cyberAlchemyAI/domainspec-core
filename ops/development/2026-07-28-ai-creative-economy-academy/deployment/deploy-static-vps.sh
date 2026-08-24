#!/usr/bin/env sh
set -eu

SSH_TARGET="${SSH_TARGET:-root@187.77.248.154}"
REMOTE_DIR="${REMOTE_DIR:-/srv/creative-economy-academy}"
PUBLIC_HOST="${PUBLIC_HOST:-resonant-alchemy.com}"
EDGE_NETWORK="${EDGE_NETWORK:-troqar_edge}"
TRAEFIK_ENTRYPOINT="${TRAEFIK_ENTRYPOINT:-websecure}"
TRAEFIK_CERT_RESOLVER="${TRAEFIK_CERT_RESOLVER:-letsencrypt}"
DRY_RUN="${DRY_RUN:-0}"

SCRIPT_DIR="$(CDPATH= cd -- "$(dirname -- "$0")" && pwd)"
PACKAGE_DIR="$(CDPATH= cd -- "$SCRIPT_DIR/.." && pwd)"
SITE_FILE="$PACKAGE_DIR/creative-economy-session.html"
COMPOSE_FILE="$SCRIPT_DIR/docker-compose.yml"
NGINX_FILE="$SCRIPT_DIR/nginx.conf"
TMP_DIR="$(mktemp -d)"
SITE_DIR="$TMP_DIR/site"
SITE_BUNDLE="$TMP_DIR/creative-economy-academy-site.tar.gz"
ENV_FILE="$TMP_DIR/creative-economy-academy.env"

cleanup() {
  rm -rf "$TMP_DIR"
}
trap cleanup EXIT INT TERM

remote() {
  if [ "$DRY_RUN" = "1" ]; then
    printf '[dry-run ssh] %s %s\n' "$SSH_TARGET" "$1"
    return 0
  fi

  ssh -o BatchMode=yes -o StrictHostKeyChecking=yes "$SSH_TARGET" "$1"
}

upload() {
  source_file="$1"
  remote_name="$2"

  if [ "$DRY_RUN" = "1" ]; then
    printf '[dry-run scp] %s %s:%s/%s\n' "$source_file" "$SSH_TARGET" "$REMOTE_DIR" "$remote_name"
    return 0
  fi

  scp -o BatchMode=yes -o StrictHostKeyChecking=yes "$source_file" "$SSH_TARGET:$REMOTE_DIR/$remote_name"
}

case "$PUBLIC_HOST" in
  "" | *[!A-Za-z0-9.-]* | .* | *..* | *.)
    echo "invalid PUBLIC_HOST: $PUBLIC_HOST" >&2
    exit 2
    ;;
esac

for required_path in "$SITE_FILE" "$COMPOSE_FILE" "$NGINX_FILE"
do
  if [ ! -f "$required_path" ]; then
    echo "missing required deploy input: $required_path" >&2
    exit 1
  fi
done

mkdir -p "$SITE_DIR"
cp "$SITE_FILE" "$SITE_DIR/index.html"
tar -C "$SITE_DIR" -czf "$SITE_BUNDLE" index.html

printf '%s\n' \
  "PUBLIC_HOST=$PUBLIC_HOST" \
  "EDGE_NETWORK=$EDGE_NETWORK" \
  "TRAEFIK_ENTRYPOINT=$TRAEFIK_ENTRYPOINT" \
  "TRAEFIK_CERT_RESOLVER=$TRAEFIK_CERT_RESOLVER" \
  > "$ENV_FILE"

echo "checking isolated remote directory: $REMOTE_DIR"
remote "if [ -e '$REMOTE_DIR' ] && [ ! -f '$REMOTE_DIR/.creative-economy-academy-deployment' ]; then echo 'refusing unexpected existing remote directory: $REMOTE_DIR' >&2; exit 1; fi; mkdir -p '$REMOTE_DIR'; touch '$REMOTE_DIR/.creative-economy-academy-deployment'"

echo "uploading the static page and public routing files"
upload "$SITE_BUNDLE" "site.tar.gz"
upload "$COMPOSE_FILE" "docker-compose.yml"
upload "$NGINX_FILE" "nginx.conf"
upload "$ENV_FILE" ".env.next"

echo "installing the release with one-generation rollback"
remote "cd '$REMOTE_DIR' && rm -rf site.next && mkdir site.next && tar -xzf site.tar.gz -C site.next && test -f site.next/index.html && rm -rf site.previous && if [ -d site ]; then mv site site.previous; fi && mv site.next site && mv .env.next .env"

echo "starting the isolated static container"
remote "cd '$REMOTE_DIR' && docker compose --env-file .env -f docker-compose.yml up -d --pull always --force-recreate site"

echo "checking the container directly"
remote "cd '$REMOTE_DIR' && docker compose --env-file .env -f docker-compose.yml exec -T site wget -qO- http://127.0.0.1/healthz"

if [ "$DRY_RUN" = "1" ]; then
  echo "dry run complete"
  exit 0
fi

echo "checking the public HTTPS route"
attempt=1
while [ "$attempt" -le 12 ]; do
  if curl -fsS --max-time 15 "https://$PUBLIC_HOST/" | grep -F '<title>The Creative Exchange</title>' >/dev/null
  then
    echo "public HTTPS: pass"
    echo "deploy complete: https://$PUBLIC_HOST/"
    exit 0
  fi

  echo "public HTTPS not ready ($attempt/12)"
  sleep 5
  attempt=$((attempt + 1))
done

echo "public HTTPS validation failed" >&2
exit 1
