#!/usr/bin/env sh
set -eu

# Edit these lines for the Hostinger VPS.
SSH_CMD="${SSH_CMD:-ssh root@187.77.248.154}"
SCP_CMD="${SCP_CMD:-scp}"
REMOTE_DIR="${REMOTE_DIR:-/srv/troqar}"
REMOTE_COPY_TARGET="${REMOTE_COPY_TARGET:-root@187.77.248.154:$REMOTE_DIR}"

# Edit these defaults once you know the production host and Traefik names.
BODY_WAR_DOMAIN="${BODY_WAR_DOMAIN:-troqarapp.com}"
BODY_WAR_APP_IMAGE="${BODY_WAR_APP_IMAGE:-troqar-body-war-app}"
BODY_WAR_EDGE_NETWORK="${BODY_WAR_EDGE_NETWORK:-troqar_edge}"
TRAEFIK_ENTRYPOINT="${TRAEFIK_ENTRYPOINT:-websecure}"
TRAEFIK_CERT_RESOLVER="${TRAEFIK_CERT_RESOLVER:-letsencrypt}"
DRY_RUN="${DRY_RUN:-0}"

SCRIPT_DIR="$(CDPATH= cd -- "$(dirname -- "$0")" && pwd)"
REPO_ROOT="$(CDPATH= cd -- "$SCRIPT_DIR/../../../.." && pwd)"
COMPOSE_FILE="$REPO_ROOT/projects/body-war/infra/docker-compose.direct.yml"
TMP_DIR="$(mktemp -d)"

cleanup() {
  rm -rf "$TMP_DIR"
}
trap cleanup EXIT INT TERM

remote() {
  if [ "$DRY_RUN" = "1" ]; then
    printf '[dry-run ssh] %s %s\n' "$SSH_CMD" "$1"
    return 0
  fi

  $SSH_CMD "$1"
}

upload() {
  source_file="$1"
  remote_name="$2"

  if [ "$DRY_RUN" = "1" ]; then
    printf '[dry-run scp] %s %s %s/%s\n' "$SCP_CMD" "$source_file" "$REMOTE_COPY_TARGET" "$remote_name"
    return 0
  fi

  $SCP_CMD "$source_file" "$REMOTE_COPY_TARGET/$remote_name"
}

require_file() {
  if [ ! -e "$1" ]; then
    echo "missing required deploy input: $1" >&2
    exit 1
  fi
}

for required_path in \
  "$COMPOSE_FILE" \
  "$REPO_ROOT/projects/auth-user-management/package.json" \
  "$REPO_ROOT/projects/auth-user-management/package-lock.json" \
  "$REPO_ROOT/projects/auth-user-management/tsconfig.json" \
  "$REPO_ROOT/projects/auth-user-management/src" \
  "$REPO_ROOT/projects/auth-user-management/drizzle" \
  "$REPO_ROOT/projects/body-war/app/package.json" \
  "$REPO_ROOT/projects/body-war/app/package-lock.json" \
  "$REPO_ROOT/projects/body-war/app/tsconfig.json" \
  "$REPO_ROOT/projects/body-war/app/server.ts" \
  "$REPO_ROOT/projects/body-war/app/src" \
  "$REPO_ROOT/projects/body-war/app/static" \
  "$REPO_ROOT/projects/body-war/app/drizzle" \
  "$REPO_ROOT/projects/body-war/app/Dockerfile" \
  "$REPO_ROOT/projects/body-war/app/Dockerfile.dockerignore"
do
  require_file "$required_path"
done

BUNDLE_FILE="$TMP_DIR/troqar-source.tar.gz"
ENV_TEMPLATE_FILE="$TMP_DIR/troqar.env.initial"
TRAEFIK_ROUTING_CHECK_FILE="$TMP_DIR/check-traefik-routing.sh"
APP_HEALTH_CHECK_FILE="$TMP_DIR/wait-app-health.sh"

tar -C "$REPO_ROOT" -czf "$BUNDLE_FILE" \
  projects/auth-user-management/package.json \
  projects/auth-user-management/package-lock.json \
  projects/auth-user-management/tsconfig.json \
  projects/auth-user-management/src \
  projects/auth-user-management/drizzle \
  projects/body-war/app/package.json \
  projects/body-war/app/package-lock.json \
  projects/body-war/app/tsconfig.json \
  projects/body-war/app/server.ts \
  projects/body-war/app/src \
  projects/body-war/app/static \
  projects/body-war/app/drizzle \
  projects/body-war/app/Dockerfile \
  projects/body-war/app/Dockerfile.dockerignore

cat > "$ENV_TEMPLATE_FILE" <<ENV_EOF
# TROQAR / Body War production env.
# This file is created on the VPS only. Replace every CHANGE_ME value there.

BODY_WAR_DOMAIN=$BODY_WAR_DOMAIN
BODY_WAR_APP_IMAGE=$BODY_WAR_APP_IMAGE

BODY_WAR_PUBLIC_BASE_URL=https://$BODY_WAR_DOMAIN
BODY_WAR_ALLOWED_ORIGINS=https://$BODY_WAR_DOMAIN
BODY_WAR_SECURE_COOKIES=1

BODY_WAR_SESSION_SECRET=CHANGE_ME_GENERATE_WITH_OPENSSL_RAND_HEX_32
BODY_WAR_TOKEN_PROTECTION_SECRET=CHANGE_ME_GENERATE_WITH_OPENSSL_RAND_HEX_32

STRAVA_CLIENT_ID=CHANGE_ME_STRAVA_CLIENT_ID
STRAVA_CLIENT_SECRET=CHANGE_ME_STRAVA_CLIENT_SECRET
STRAVA_REDIRECT_URI=https://$BODY_WAR_DOMAIN/api/auth/strava/callback

POSTGRES_USER=body_war
POSTGRES_PASSWORD=CHANGE_ME_GENERATE_WITH_OPENSSL_RAND_HEX_32
POSTGRES_DB=body_war

BODY_WAR_EDGE_NETWORK=$BODY_WAR_EDGE_NETWORK
TRAEFIK_ENTRYPOINT=$TRAEFIK_ENTRYPOINT
TRAEFIK_CERT_RESOLVER=$TRAEFIK_CERT_RESOLVER
TRAEFIK_ROUTER_NAME=troqar
TRAEFIK_SERVICE_NAME=troqar
ENV_EOF

cat > "$TRAEFIK_ROUTING_CHECK_FILE" <<'CHECK_EOF'
#!/usr/bin/env sh
set -eu

ENV_FILE="${1:-.env}"
EDGE_NETWORK_VALUE="$(awk -F= '/^BODY_WAR_EDGE_NETWORK=/{print $2; exit}' "$ENV_FILE")"

if [ "$EDGE_NETWORK_VALUE" = "" ]; then
  echo "BODY_WAR_EDGE_NETWORK is missing from $ENV_FILE"
  exit 1
fi

echo "Body War edge network: $EDGE_NETWORK_VALUE"
if docker network inspect "$EDGE_NETWORK_VALUE" >/dev/null 2>&1; then
  echo "Edge network already exists."
else
  echo "Edge network will be created by docker compose."
fi

echo
echo "Traefik containers and attached networks:"
if docker ps --format '{{.Names}} {{.Image}}' | grep -qi traefik; then
  docker ps --format '{{.Names}} {{.Image}}' \
    | awk 'tolower($0) ~ /traefik/ {print $1}' \
    | while IFS= read -r container
      do
        printf '  - %s: ' "$container"
        docker inspect "$container" \
          --format '{{range $name, $_ := .NetworkSettings.Networks}}{{printf "%s " $name}}{{end}}'
        printf '\n'
      done
else
  echo "  - none detected by container name or image"
fi
echo
echo "If Traefik is attached to host, the direct deploy path does not need a pre-existing Traefik Docker network."
CHECK_EOF

cat > "$APP_HEALTH_CHECK_FILE" <<'CHECK_EOF'
#!/usr/bin/env sh
set -eu

ENV_FILE="${1:-.env}"
ATTEMPTS="${2:-45}"
SLEEP_SECONDS="${3:-2}"
COMPOSE_FILE="${COMPOSE_FILE:-docker-compose.direct.yml}"

attempt=1
while [ "$attempt" -le "$ATTEMPTS" ]; do
  if docker compose --env-file "$ENV_FILE" -f "$COMPOSE_FILE" exec -T app \
    node -e "fetch('http://127.0.0.1:5174/api/status').then((r)=>{if(!r.ok) process.exit(1); return r.text();}).then((body)=>{console.log(body);}).catch(()=>process.exit(1));" >/tmp/troqar-health.out 2>/tmp/troqar-health.err
  then
    cat /tmp/troqar-health.out
    echo "app health: pass"
    rm -f /tmp/troqar-health.out /tmp/troqar-health.err
    exit 0
  fi

  echo "app health not ready ($attempt/$ATTEMPTS)"
  sleep "$SLEEP_SECONDS"
  attempt=$((attempt + 1))
done

echo
echo "app health: fail"
echo
echo "last health error:"
cat /tmp/troqar-health.err 2>/dev/null || true
rm -f /tmp/troqar-health.out /tmp/troqar-health.err
echo
echo "compose services:"
docker compose --env-file "$ENV_FILE" -f "$COMPOSE_FILE" ps
echo
echo "recent app logs:"
docker compose --env-file "$ENV_FILE" -f "$COMPOSE_FILE" logs --tail=120 app
exit 1
CHECK_EOF

echo "creating remote deploy directory: $REMOTE_DIR"
remote "mkdir -p '$REMOTE_DIR'"

echo "uploading source bundle and compose file"
upload "$BUNDLE_FILE" "troqar-source.tar.gz"
upload "$COMPOSE_FILE" "docker-compose.direct.yml"
upload "$ENV_TEMPLATE_FILE" ".env.initial"
upload "$TRAEFIK_ROUTING_CHECK_FILE" "check-traefik-routing.sh"
upload "$APP_HEALTH_CHECK_FILE" "wait-app-health.sh"

echo "preparing remote source tree and env file"
remote "cd '$REMOTE_DIR' && rm -rf source && mkdir -p source receipts && tar -xzf troqar-source.tar.gz -C source && if [ ! -f .env ]; then mv .env.initial .env && chmod 600 .env && echo 'created .env from template'; else rm -f .env.initial && echo 'kept existing .env'; fi && if ! grep -q '^BODY_WAR_EDGE_NETWORK=' .env; then printf '\nBODY_WAR_EDGE_NETWORK=%s\n' '$BODY_WAR_EDGE_NETWORK' >> .env && echo 'added BODY_WAR_EDGE_NETWORK to existing .env'; fi"

echo "checking remote .env placeholders"
if ! remote "cd '$REMOTE_DIR' && if grep -Eq '^[A-Za-z_][A-Za-z0-9_]*=.*(CHANGE_ME|your-vps-ip|troqar\\.example\\.com|example\\.com)' .env; then echo 'Placeholder/default values still present in .env:'; grep -E '^[A-Za-z_][A-Za-z0-9_]*=.*(CHANGE_ME|your-vps-ip|troqar\\.example\\.com|example\\.com)' .env | sed 's/=.*//' | sed 's/^/  - /'; exit 1; fi"; then
  echo
  echo "Remote .env still has placeholders. Edit it on the VPS, then rerun this script:"
  echo "  $SSH_CMD \"nano $REMOTE_DIR/.env\""
  echo
  echo "Generate private values on the VPS with:"
  echo "  openssl rand -hex 32"
  exit 3
fi

echo "checking remote Traefik routing mode"
if ! remote "cd '$REMOTE_DIR' && sh check-traefik-routing.sh .env"; then
  echo
  echo "Fix the routing values in the remote env file, then rerun this script:"
  echo "  $SSH_CMD \"nano $REMOTE_DIR/.env\""
  exit 4
fi

echo "building and starting TROQAR on the VPS"
remote "cd '$REMOTE_DIR' && docker compose --env-file .env -f docker-compose.direct.yml up -d --build postgres"
remote "cd '$REMOTE_DIR' && docker compose --env-file .env -f docker-compose.direct.yml run --rm --build app node dist/src/infrastructure/postgres/migrate-cli.js"
remote "cd '$REMOTE_DIR' && docker compose --env-file .env -f docker-compose.direct.yml up -d --build app"

echo "checking app health inside the container"
remote "cd '$REMOTE_DIR' && sh wait-app-health.sh .env 45 2"

echo "deploy complete. Open https://$BODY_WAR_DOMAIN"
