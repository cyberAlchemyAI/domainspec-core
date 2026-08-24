#!/usr/bin/env sh
set -eu

SSH_TARGET="${SSH_TARGET:-root@187.77.248.154}"
REMOTE_DIR="${REMOTE_DIR:-/srv/augmentor-ontology}"
PUBLIC_HOST="${PUBLIC_HOST:-resonant-alchemy.com}"
PUBLIC_PATH="${PUBLIC_PATH:-/augmentor}"
EDGE_NETWORK="${EDGE_NETWORK:-troqar_edge}"
TRAEFIK_ENTRYPOINT="${TRAEFIK_ENTRYPOINT:-websecure}"
TRAEFIK_CERT_RESOLVER="${TRAEFIK_CERT_RESOLVER:-letsencrypt}"
AUTH_USERNAME="${AUTH_USERNAME:-augmentor}"
AUTH_PASSWORD="${AUTH_PASSWORD:-}"
DRY_RUN="${DRY_RUN:-0}"

SCRIPT_DIR="$(CDPATH= cd -- "$(dirname -- "$0")" && pwd)"
CONSUMER_ROOT="${CONSUMER_ROOT:-$(CDPATH= cd -- "$SCRIPT_DIR/../../../../../../workspace-resonant/2.0.0-alpha" 2>/dev/null && pwd || true)}"
PACKAGE_DIR="$(CDPATH= cd -- "$SCRIPT_DIR/.." && pwd)"
SITE_FILE="$PACKAGE_DIR/ontology-visualization.html"
COMPOSE_FILE="$SCRIPT_DIR/docker-compose.yml"
NGINX_FILE="$SCRIPT_DIR/nginx.conf"
TMP_DIR="$(mktemp -d)"
RELEASE_DIR="$TMP_DIR/release"
SITE_DIR="$RELEASE_DIR/site"
API_DIR="$RELEASE_DIR/api"
RELEASE_BUNDLE="$TMP_DIR/augmentor-ontology-release.tar.gz"
ENV_FILE="$RELEASE_DIR/.env"
HTPASSWD_FILE="$RELEASE_DIR/.htpasswd"
NETRC_FILE="$TMP_DIR/curl.netrc"
LIVE_FILE="$TMP_DIR/live.html"

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

rollback_remote() {
  remote "set -eu; cd '$REMOTE_DIR'; test -L previous; prior=\$(readlink previous); ln -sfn \"\$prior\" current.next; mv -Tf current.next current; docker compose -p augmentor-ontology --env-file current/.env -f current/docker-compose.yml up -d --force-recreate --remove-orphans"
}

case "$PUBLIC_HOST" in
  "" | *[!A-Za-z0-9.-]* | .* | *..* | *.)
    echo "invalid PUBLIC_HOST: $PUBLIC_HOST" >&2
    exit 2
    ;;
esac

if [ "$PUBLIC_PATH" != "/augmentor" ]; then
  echo "refusing unexpected PUBLIC_PATH: $PUBLIC_PATH" >&2
  exit 2
fi

case "$AUTH_USERNAME" in
  "" | *[!A-Za-z0-9._-]*)
    echo "invalid AUTH_USERNAME" >&2
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

if [ -z "$CONSUMER_ROOT" ] || [ ! -d "$CONSUMER_ROOT/browser-first/host" ]; then
  echo "CONSUMER_ROOT must select the ResonantOS 2.0.0-alpha checkout" >&2
  exit 2
fi

PROJECTION_DIR="$PACKAGE_DIR/development/consultation-api/generated/consumer"
for required_path in \
  "$CONSUMER_ROOT/browser-first/host/run-augmentor-consultation-deployment.mjs" \
  "$CONSUMER_ROOT/browser-first/host/augmentor-consultation-answer-policy.mjs" \
  "$CONSUMER_ROOT/browser-first/host/augmentor-consultation-cache.mjs" \
  "$CONSUMER_ROOT/browser-first/host/augmentor-consultation-contract.mjs" \
  "$CONSUMER_ROOT/browser-first/host/augmentor-consultation-service.mjs" \
  "$PROJECTION_DIR/projection.json" \
  "$PROJECTION_DIR/projection-manifest.json" \
  "$PROJECTION_DIR/glossary.json" \
  "$PROJECTION_DIR/schemas/projection.schema.json" \
  "$PROJECTION_DIR/schemas/projection-manifest.schema.json" \
  "$PROJECTION_DIR/schemas/glossary.schema.json" \
  "$PROJECTION_DIR/schemas/explanation-support.schema.json" \
  "$PROJECTION_DIR/anatomy-focus-map.json" \
  "$PROJECTION_DIR/schemas/anatomy-focus-map.schema.json"
do
  if [ ! -f "$required_path" ]; then
    echo "missing consultation API deploy input: $required_path" >&2
    exit 1
  fi
done

mkdir -p "$SITE_DIR"
mkdir -p "$API_DIR/projection/schemas"
cp "$SITE_FILE" "$SITE_DIR/index.html"
cp "$COMPOSE_FILE" "$RELEASE_DIR/docker-compose.yml"
cp "$NGINX_FILE" "$RELEASE_DIR/nginx.conf"
cp "$CONSUMER_ROOT/browser-first/host/run-augmentor-consultation-deployment.mjs" "$API_DIR/"
cp "$CONSUMER_ROOT/browser-first/host/augmentor-consultation-answer-policy.mjs" "$API_DIR/"
cp "$CONSUMER_ROOT/browser-first/host/augmentor-consultation-cache.mjs" "$API_DIR/"
cp "$CONSUMER_ROOT/browser-first/host/augmentor-consultation-contract.mjs" "$API_DIR/"
cp "$CONSUMER_ROOT/browser-first/host/augmentor-consultation-service.mjs" "$API_DIR/"
cp "$PROJECTION_DIR/projection.json" "$API_DIR/projection/"
cp "$PROJECTION_DIR/projection-manifest.json" "$API_DIR/projection/"
cp "$PROJECTION_DIR/glossary.json" "$API_DIR/projection/"
cp "$PROJECTION_DIR/anatomy-focus-map.json" "$API_DIR/projection/"
cp "$PROJECTION_DIR/schemas/projection.schema.json" "$API_DIR/projection/schemas/"
cp "$PROJECTION_DIR/schemas/projection-manifest.schema.json" "$API_DIR/projection/schemas/"
cp "$PROJECTION_DIR/schemas/glossary.schema.json" "$API_DIR/projection/schemas/"
cp "$PROJECTION_DIR/schemas/explanation-support.schema.json" "$API_DIR/projection/schemas/"
cp "$PROJECTION_DIR/schemas/anatomy-focus-map.schema.json" "$API_DIR/projection/schemas/"

printf '%s\n' \
  "PUBLIC_HOST=$PUBLIC_HOST" \
  "PUBLIC_PATH=$PUBLIC_PATH" \
  "EDGE_NETWORK=$EDGE_NETWORK" \
  "TRAEFIK_ENTRYPOINT=$TRAEFIK_ENTRYPOINT" \
  "TRAEFIK_CERT_RESOLVER=$TRAEFIK_CERT_RESOLVER" \
  "AUTH_USERNAME=$AUTH_USERNAME" \
  > "$ENV_FILE"

if [ -n "$AUTH_PASSWORD" ]; then
  AUTH_HASH="$(printf '%s\n' "$AUTH_PASSWORD" | openssl passwd -apr1 -stdin)"
  printf '%s:%s\n' "$AUTH_USERNAME" "$AUTH_HASH" > "$HTPASSWD_FILE"
  chmod 600 "$HTPASSWD_FILE"
fi

RELEASE_ID="$(sha256sum "$SITE_FILE" | awk '{print substr($1, 1, 16)}')-$(date -u +%Y%m%d%H%M%S)"
tar -C "$RELEASE_DIR" -czf "$RELEASE_BUNDLE" .

if [ -n "$AUTH_PASSWORD" ]; then
  printf 'machine %s login %s password %s\n' "$PUBLIC_HOST" "$AUTH_USERNAME" "$AUTH_PASSWORD" > "$NETRC_FILE"
  chmod 600 "$NETRC_FILE"
fi

echo "checking isolated remote directory: $REMOTE_DIR"
remote "if [ -e '$REMOTE_DIR' ] && [ ! -f '$REMOTE_DIR/.augmentor-ontology-deployment' ]; then echo 'refusing unexpected existing remote directory: $REMOTE_DIR' >&2; exit 1; fi; mkdir -p '$REMOTE_DIR/releases'; touch '$REMOTE_DIR/.augmentor-ontology-deployment'"

echo "uploading the protected static page and routing files"
upload "$RELEASE_BUNDLE" "release-$RELEASE_ID.tar.gz"

echo "installing the release with one-generation rollback"
remote "set -eu; cd '$REMOTE_DIR'; next='releases/$RELEASE_ID.next'; final='releases/$RELEASE_ID'; rm -rf \"\$next\"; mkdir -p \"\$next\"; tar -xzf 'release-$RELEASE_ID.tar.gz' -C \"\$next\"; test -f \"\$next/site/index.html\"; test -f \"\$next/api/run-augmentor-consultation-deployment.mjs\"; test -f \"\$next/api/projection/projection.json\"; test -f \"\$next/api/projection/projection-manifest.json\"; test -f \"\$next/api/projection/glossary.json\"; test -f \"\$next/api/projection/anatomy-focus-map.json\"; test -f \"\$next/api/projection/schemas/projection.schema.json\"; test -f \"\$next/api/projection/schemas/projection-manifest.schema.json\"; test -f \"\$next/api/projection/schemas/glossary.schema.json\"; test -f \"\$next/api/projection/schemas/explanation-support.schema.json\"; test -f \"\$next/api/projection/schemas/anatomy-focus-map.schema.json\"; if [ ! -f \"\$next/.htpasswd\" ]; then test -L current; cp -p current/.htpasswd \"\$next/.htpasswd\"; fi; test \"\$(cut -d: -f1 \"\$next/.htpasswd\")\" = '$AUTH_USERNAME'; chown 101:101 \"\$next/.htpasswd\"; chmod 600 \"\$next/.htpasswd\"; docker compose -p augmentor-ontology --env-file \"\$next/.env\" -f \"\$next/docker-compose.yml\" config -q; rm -rf \"\$final\"; mv \"\$next\" \"\$final\"; old=; if [ -L current ]; then old=\$(readlink current); fi; ln -sfn \"\$final\" current.next; mv -Tf current.next current; if [ -n \"\$old\" ]; then ln -sfn \"\$old\" previous.next; mv -Tf previous.next previous; fi; rm -f 'release-$RELEASE_ID.tar.gz'"

echo "starting the isolated protected container"
if ! remote "cd '$REMOTE_DIR' && docker compose -p augmentor-ontology --env-file current/.env -f current/docker-compose.yml up -d --pull always --force-recreate api site"
then
  echo "start failed; restoring the previous complete release" >&2
  rollback_remote
  exit 1
fi

echo "checking the container directly"
if ! remote "cd '$REMOTE_DIR' && docker compose -p augmentor-ontology --env-file current/.env -f current/docker-compose.yml exec -T site wget -qO- http://127.0.0.1/healthz && docker compose -p augmentor-ontology --env-file current/.env -f current/docker-compose.yml exec -T api node -e \"fetch('http://127.0.0.1:8787/healthz').then(async r=>{if(!r.ok)process.exit(1);const v=await r.json();if(v.service!=='augmentor-consultation')process.exit(1)})\" && docker compose -p augmentor-ontology --env-file current/.env -f current/docker-compose.yml exec -T api node -e \"const q={schemaVersion:'augmentor.consultation.query@1.1.0',requestId:'deploy-general-smoke',questionId:'deploy-general-smoke',operation:'search',query:{text:'saved conversation'},scope:{viewIds:['experience']},limits:{maxCandidates:100,maxRecords:10,maxSources:20,maxBytes:32768,maxTokens:4096,maxMillis:1000}};fetch('http://127.0.0.1:8787/augmentor/consultation',{method:'POST',headers:{'content-type':'application/json','x-resonantos-consultation-principal':'$AUTH_USERNAME'},body:JSON.stringify(q)}).then(async r=>{const v=await r.json();const supported=['ok','partial'].includes(v.consultation?.status)&&['answer','qualify'].includes(v.answerPolicy?.action);if(!r.ok||!supported||(v.consultation?.result?.statements?.length??0)<1)process.exit(1)})\" && docker compose -p augmentor-ontology --env-file current/.env -f current/docker-compose.yml exec -T api node -e \"const q={schemaVersion:'augmentor.consultation.query@1.2.0',requestId:'deploy-work-spine-smoke',questionId:'deploy-work-spine-smoke',operation:'search',query:{text:'How do a work plan, approval, one running task, and the final completion check fit together?'},focus:{kind:'anatomy-region',id:'work-spine'},scope:{viewIds:['experience']},limits:{maxCandidates:100,maxRecords:10,maxSources:20,maxBytes:32768,maxTokens:4096,maxMillis:1000}};fetch('http://127.0.0.1:8787/augmentor/consultation',{method:'POST',headers:{'content-type':'application/json','x-resonantos-consultation-principal':'$AUTH_USERNAME'},body:JSON.stringify(q)}).then(async r=>{const v=await r.json();const supported=['ok','partial'].includes(v.consultation?.status)&&['answer','qualify'].includes(v.answerPolicy?.action);if(!r.ok||!supported||v.consultation?.schemaVersion!=='augmentor.consultation.result@1.2.0'||v.consultation?.resolvedFocus?.id!=='work-spine'||(v.consultation?.result?.statements?.length??0)<1)process.exit(1)})\""
then
  echo "health check failed; restoring the previous complete release" >&2
  rollback_remote
  exit 1
fi

if [ "$DRY_RUN" = "1" ]; then
  echo "dry run complete"
  exit 0
fi

echo "checking anonymous denial, fixed-hash authentication when available, and unchanged homepage"
attempt=1
while [ "$attempt" -le 12 ]; do
  anonymous_status="$(curl -sS -o /dev/null -w '%{http_code}' --max-time 15 "https://$PUBLIC_HOST$PUBLIC_PATH/")"
  auth_ok=1
  if [ -n "$AUTH_PASSWORD" ]; then
    auth_ok=0
    if curl -fsS --netrc-file "$NETRC_FILE" --max-time 15 "https://$PUBLIC_HOST$PUBLIC_PATH/" -o "$LIVE_FILE" && cmp -s "$SITE_FILE" "$LIVE_FILE"; then auth_ok=1; fi
  fi
  if [ "$anonymous_status" = "401" ] && [ "$auth_ok" = "1" ] && \
     curl -fsS --max-time 15 "https://$PUBLIC_HOST/" | grep -F '<title>The Creative Exchange</title>' >/dev/null
  then
    echo "anonymous HTTPS: 401"
    if [ -n "$AUTH_PASSWORD" ]; then echo "authenticated HTML digest: $(sha256sum "$LIVE_FILE" | awk '{print $1}')"; else echo "fixed password hash: preserved from previous release"; fi
    echo "existing homepage: pass"
    echo "deploy complete: https://$PUBLIC_HOST$PUBLIC_PATH/"
    exit 0
  fi

  echo "public HTTPS not ready ($attempt/12; anonymous status $anonymous_status)"
  sleep 5
  attempt=$((attempt + 1))
done

echo "public HTTPS validation failed" >&2
rollback_remote
exit 1
