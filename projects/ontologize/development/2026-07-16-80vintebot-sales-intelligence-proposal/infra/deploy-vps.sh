#!/usr/bin/env sh
set -eu

SSH_TARGET="${SSH_TARGET:-root@187.77.248.154}"
REMOTE_DIR="${REMOTE_DIR:-/srv/80vinte}"
PUBLIC_HOST="${PUBLIC_HOST:-80vinte.cyberalchemize.com}"
EDGE_NETWORK="${EDGE_NETWORK:-troqar_edge}"
TRAEFIK_ENTRYPOINT="${TRAEFIK_ENTRYPOINT:-websecure}"
TRAEFIK_CERT_RESOLVER="${TRAEFIK_CERT_RESOLVER:-letsencrypt}"
COMPOSE_PROJECT="${COMPOSE_PROJECT:-eightyvinte}"
DRY_RUN="${DRY_RUN:-0}"

SCRIPT_DIR="$(CDPATH= cd -- "$(dirname -- "$0")" && pwd)"
PROPOSAL_DIR="$(CDPATH= cd -- "$SCRIPT_DIR/.." && pwd)"
SOURCE_HTML="$PROPOSAL_DIR/proposal-blueprint.html"
COMPOSE_FILE="$SCRIPT_DIR/docker-compose.yml"
NGINX_FILE="$SCRIPT_DIR/nginx.conf"
DEPLOY_ID="$(date -u +%Y%m%dT%H%M%SZ)"
INCOMING_DIR="$REMOTE_DIR/.incoming-$DEPLOY_ID"
PUBLIC_URL="https://$PUBLIC_HOST"
PUBLIC_RESPONSE_FILE="$(mktemp)"

cleanup() {
  rm -f "$PUBLIC_RESPONSE_FILE"
}
trap cleanup EXIT INT TERM

for required_file in "$SOURCE_HTML" "$COMPOSE_FILE" "$NGINX_FILE"; do
  if [ ! -r "$required_file" ]; then
    echo "missing deploy input: $required_file" >&2
    exit 1
  fi
done

if ! grep -q '<title>Ontologize para o 80VinteBot</title>' "$SOURCE_HTML"; then
  echo "proposal identity check failed: expected HTML title was not found" >&2
  exit 1
fi

remote() {
  if [ "$DRY_RUN" = "1" ]; then
    printf '[dry-run ssh] %s %s\n' "$SSH_TARGET" "$1"
    return 0
  fi

  ssh -o BatchMode=yes "$SSH_TARGET" "$1"
}

upload() {
  source_file="$1"
  remote_name="$2"

  if [ "$DRY_RUN" = "1" ]; then
    printf '[dry-run scp] %s %s:%s/%s\n' "$source_file" "$SSH_TARGET" "$INCOMING_DIR" "$remote_name"
    return 0
  fi

  scp -q "$source_file" "$SSH_TARGET:$INCOMING_DIR/$remote_name"
}

compose_env="PUBLIC_HOST='$PUBLIC_HOST' EDGE_NETWORK='$EDGE_NETWORK' TRAEFIK_ENTRYPOINT='$TRAEFIK_ENTRYPOINT' TRAEFIK_CERT_RESOLVER='$TRAEFIK_CERT_RESOLVER'"
compose_cmd="$compose_env docker compose -p '$COMPOSE_PROJECT' -f '$REMOTE_DIR/docker-compose.yml'"

echo "preparing isolated release on $SSH_TARGET"
remote "mkdir -p '$INCOMING_DIR' '$REMOTE_DIR/receipts'"

echo "uploading proposal and deployment configuration"
upload "$SOURCE_HTML" index.html
upload "$COMPOSE_FILE" docker-compose.yml
upload "$NGINX_FILE" nginx.conf

echo "validating routing prerequisites"
remote "docker network inspect '$EDGE_NETWORK' >/dev/null"
remote "mkdir -p '$INCOMING_DIR/site' && mv '$INCOMING_DIR/index.html' '$INCOMING_DIR/site/index.html' && $compose_env docker compose -p '$COMPOSE_PROJECT' -f '$INCOMING_DIR/docker-compose.yml' config -q"

echo "promoting release $DEPLOY_ID"
remote "cd '$REMOTE_DIR' && rm -rf site.previous && if [ -d site ]; then mv site site.previous; fi && mv '$INCOMING_DIR/site' site && mv '$INCOMING_DIR/docker-compose.yml' docker-compose.yml && mv '$INCOMING_DIR/nginx.conf' nginx.conf && rmdir '$INCOMING_DIR' && $compose_cmd up -d"

if [ "$DRY_RUN" = "1" ]; then
  echo "dry run: pass"
  echo "url: $PUBLIC_URL/"
  exit 0
fi

echo "waiting for container health"
attempt=1
while [ "$attempt" -le 30 ]; do
  health="$(remote "docker inspect 80vinte-proposal-site --format '{{if .State.Health}}{{.State.Health.Status}}{{else}}{{.State.Status}}{{end}}'" 2>/dev/null || true)"
  if [ "$health" = "healthy" ]; then
    break
  fi
  if [ "$health" = "unhealthy" ] || [ "$health" = "exited" ]; then
    echo "container health failed: $health" >&2
    exit 1
  fi
  sleep 2
  attempt=$((attempt + 1))
done

if [ "${health:-}" != "healthy" ]; then
  echo "container did not become healthy" >&2
  exit 1
fi

echo "checking public HTTPS route"
attempt=1
while [ "$attempt" -le 30 ]; do
  if curl -fsS --connect-timeout 5 --max-time 15 -o "$PUBLIC_RESPONSE_FILE" "$PUBLIC_URL/" \
    && grep -q '<title>Ontologize para o 80VinteBot</title>' "$PUBLIC_RESPONSE_FILE"; then
    break
  fi
  sleep 2
  attempt=$((attempt + 1))
done

if [ "$attempt" -gt 30 ]; then
  echo "public HTTPS route did not return the expected proposal" >&2
  exit 1
fi

remote "printf '%s\n' '# 80Vinte Proposal Deployment Receipt' '' '- Timestamp: $DEPLOY_ID' '- Domain: $PUBLIC_HOST' '- Container health: pass' '- HTTPS identity check: pass' '- Source: proposal-blueprint.html' > '$REMOTE_DIR/receipts/deploy-$DEPLOY_ID.md'"
remote "cd '$REMOTE_DIR' && find . -maxdepth 1 -type d -name '.incoming-*' -mtime +1 -exec rm -rf {} +"

echo "deploy: pass"
echo "url: $PUBLIC_URL/"
echo "remote receipt: $REMOTE_DIR/receipts/deploy-$DEPLOY_ID.md"
