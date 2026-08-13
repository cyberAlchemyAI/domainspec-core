#!/usr/bin/env sh
set -eu
umask 077

# Connection defaults are inherited from Body War's secret-blind VPS route.
SSH_CMD="${SSH_CMD:-ssh -o BatchMode=yes -o StrictHostKeyChecking=yes root@187.77.248.154}"
SCP_CMD="${SCP_CMD:-scp -o BatchMode=yes -o StrictHostKeyChecking=yes}"
REMOTE_DIR="${REMOTE_DIR:-/srv/co-op-engine}"
REMOTE_COPY_TARGET="${REMOTE_COPY_TARGET:-root@187.77.248.154:$REMOTE_DIR}"

PUBLIC_HOST="${PUBLIC_HOST:-cyberalchemize.com}"
EDGE_NETWORK="${EDGE_NETWORK:-troqar_edge}"
TRAEFIK_ENTRYPOINT="${TRAEFIK_ENTRYPOINT:-websecure}"
TRAEFIK_CERT_RESOLVER="${TRAEFIK_CERT_RESOLVER:-letsencrypt}"
DOMAINSPEC_AUTH_USERNAME="${DOMAINSPEC_AUTH_USERNAME:-domainspec-guide}"
DOMAINSPEC_AUTH_PASSWORD_FILE="${DOMAINSPEC_AUTH_PASSWORD_FILE:-}"
DEPLOY_SCOPE="${DEPLOY_SCOPE:-full}"
DRY_RUN="${DRY_RUN:-0}"

SCRIPT_DIR="$(CDPATH= cd -- "$(dirname -- "$0")" && pwd)"
SITE_FILE="$SCRIPT_DIR/../index.html"
CRAFT_SITE_FILE="$SCRIPT_DIR/../../../arcanum/development/user-guide/craft-augmented-physics.html"
BELLA_SITE_FILE="${BELLA_SITE_FILE:-$SCRIPT_DIR/../../../../direito-romano/learning-graph/FAST-TOWER-GRAPH.html}"
DOMAINSPEC_GUIDE_DIR="${DOMAINSPEC_GUIDE_DIR:-$SCRIPT_DIR/../../domainspec-v2}"
DOMAINSPEC_HTML_FILE="$DOMAINSPEC_GUIDE_DIR/COMPLETE-GUIDE.html"
DOMAINSPEC_MARKDOWN_FILE="$DOMAINSPEC_GUIDE_DIR/COMPLETE-GUIDE.md"
DOMAINSPEC_LANES_FILE="$DOMAINSPEC_GUIDE_DIR/COMPLETE-GUIDE.lanes.json"
DOMAINSPEC_SCHEMA_FILE="$DOMAINSPEC_GUIDE_DIR/COMPLETE-GUIDE.schema.json"
COMPOSE_FILE="$SCRIPT_DIR/docker-compose.yml"
NGINX_FILE="$SCRIPT_DIR/nginx.conf"
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

rollback_remote() {
  echo "rolling back the static site release" >&2
  remote "set -eu; cd '$REMOTE_DIR'; if [ -d site.previous ]; then rm -rf site.failed && if [ -d site ]; then mv site site.failed; fi && mv site.previous site; fi; if [ -f docker-compose.yml.previous ]; then mv docker-compose.yml.previous docker-compose.yml; fi; if [ -f nginx.conf.previous ]; then mv nginx.conf.previous nginx.conf; fi; if [ -f .env.previous ]; then mv .env.previous .env; fi; if [ -f .domainspec.htpasswd.previous ]; then mv .domainspec.htpasswd.previous .domainspec.htpasswd; else rm -f .domainspec.htpasswd; fi; docker compose --env-file .env -f docker-compose.yml up -d --force-recreate site"
}

fail_with_rollback() {
  message="$1"
  echo "$message" >&2
  if ! rollback_remote; then
    echo "automatic rollback failed; inspect $REMOTE_DIR before retrying" >&2
  fi
  exit 1
}

verify_live_release() {
  canonical_status="$(curl -sS --max-time 15 -o /dev/null -w '%{http_code}' "https://$PUBLIC_HOST/domainspec")" || return 1
  [ "$canonical_status" = "308" ] || return 1

  for protected_path in \
    "/domainspec/" \
    "/domainspec/COMPLETE-GUIDE.html" \
    "/domainspec/COMPLETE-GUIDE.md" \
    "/domainspec/COMPLETE-GUIDE.lanes.json" \
    "/domainspec/COMPLETE-GUIDE.schema.json" \
    "/domainspec/impl/not-deployed"
  do
    anonymous_status="$(curl -sS --max-time 15 -o /dev/null -w '%{http_code}' "https://$PUBLIC_HOST$protected_path")" || return 1
    wrong_auth_status="$(curl -sS --max-time 15 -u 'invalid-domainspec-user:invalid-password' -o /dev/null -w '%{http_code}' "https://$PUBLIC_HOST$protected_path")" || return 1
    [ "$anonymous_status" = "401" ] || return 1
    [ "$wrong_auth_status" = "401" ] || return 1
  done

  curl -sSI --max-time 15 "https://$PUBLIC_HOST/domainspec/" |
    grep -Fi 'www-authenticate: Basic realm="DomainSpec guide"' >/dev/null || return 1

  [ "$(curl -fsS --max-time 15 "https://$PUBLIC_HOST/" | sha256sum | awk '{print $1}')" = "$SITE_SOURCE_SHA256" ] || return 1
  [ "$(curl -fsS --max-time 15 "https://$PUBLIC_HOST/craft" | sha256sum | awk '{print $1}')" = "$CRAFT_SOURCE_SHA256" ] || return 1
  [ "$(curl -fsS --max-time 15 "https://$PUBLIC_HOST/bella" | sha256sum | awk '{print $1}')" = "$BELLA_SOURCE_SHA256" ] || return 1

  [ "$(curl -fsS --netrc-file "$NETRC_FILE" --max-time 15 "https://$PUBLIC_HOST/domainspec/" | sha256sum | awk '{print $1}')" = "$DOMAINSPEC_HTML_SHA256" ] || return 1
  [ "$(curl -fsS --netrc-file "$NETRC_FILE" --max-time 15 "https://$PUBLIC_HOST/domainspec/COMPLETE-GUIDE.html" | sha256sum | awk '{print $1}')" = "$DOMAINSPEC_HTML_SHA256" ] || return 1
  [ "$(curl -fsS --netrc-file "$NETRC_FILE" --max-time 15 "https://$PUBLIC_HOST/domainspec/COMPLETE-GUIDE.md" | sha256sum | awk '{print $1}')" = "$DOMAINSPEC_MARKDOWN_SHA256" ] || return 1
  [ "$(curl -fsS --netrc-file "$NETRC_FILE" --max-time 15 "https://$PUBLIC_HOST/domainspec/COMPLETE-GUIDE.lanes.json" | sha256sum | awk '{print $1}')" = "$DOMAINSPEC_LANES_SHA256" ] || return 1
  [ "$(curl -fsS --netrc-file "$NETRC_FILE" --max-time 15 "https://$PUBLIC_HOST/domainspec/COMPLETE-GUIDE.schema.json" | sha256sum | awk '{print $1}')" = "$DOMAINSPEC_SCHEMA_SHA256" ] || return 1

  private_source_status="$(curl -sS --netrc-file "$NETRC_FILE" --max-time 15 -o /dev/null -w '%{http_code}' "https://$PUBLIC_HOST/domainspec/impl/not-deployed")" || return 1
  [ "$private_source_status" = "404" ] || return 1

  curl -fsS --netrc-file "$NETRC_FILE" --max-time 15 -D "$DOMAIN_HEADERS_FILE" -o /dev/null "https://$PUBLIC_HOST/domainspec/" || return 1
  grep -Fi 'content-security-policy:' "$DOMAIN_HEADERS_FILE" >/dev/null || return 1
  grep -Fi "connect-src 'none'" "$DOMAIN_HEADERS_FILE" >/dev/null || return 1
  grep -Fi 'referrer-policy: no-referrer' "$DOMAIN_HEADERS_FILE" >/dev/null || return 1
  grep -Fi 'x-content-type-options: nosniff' "$DOMAIN_HEADERS_FILE" >/dev/null || return 1
  grep -Fi 'x-frame-options: DENY' "$DOMAIN_HEADERS_FILE" >/dev/null || return 1
  grep -Fi 'permissions-policy: camera=(), microphone=(), geolocation=()' "$DOMAIN_HEADERS_FILE" >/dev/null || return 1
  grep -Fi 'cache-control: private, no-store, max-age=0' "$DOMAIN_HEADERS_FILE" >/dev/null || return 1
  grep -Fi 'vary: Authorization' "$DOMAIN_HEADERS_FILE" >/dev/null || return 1
  grep -Fi 'x-robots-tag: noindex, nofollow, noarchive' "$DOMAIN_HEADERS_FILE" >/dev/null || return 1
}

case "$PUBLIC_HOST" in
  "" | *[!A-Za-z0-9.-]* | .* | *..* | *.)
    echo "invalid PUBLIC_HOST: $PUBLIC_HOST" >&2
    exit 2
    ;;
esac

case "$PUBLIC_HOST" in
  troqarapp.com | time-capsule.cyberalchemize.com)
    echo "refusing to replace an existing product host: $PUBLIC_HOST" >&2
    exit 2
    ;;
esac

case "$DOMAINSPEC_AUTH_USERNAME" in
  "" | *[!A-Za-z0-9._-]*)
    echo "invalid DOMAINSPEC_AUTH_USERNAME" >&2
    exit 2
    ;;
esac

case "$DEPLOY_SCOPE" in
  full | domainspec)
    ;;
  *)
    echo "invalid DEPLOY_SCOPE: $DEPLOY_SCOPE" >&2
    exit 2
    ;;
esac

if [ -z "$DOMAINSPEC_AUTH_PASSWORD_FILE" ]; then
  echo "DOMAINSPEC_AUTH_PASSWORD_FILE is required" >&2
  exit 2
fi

if [ ! -r "$DOMAINSPEC_AUTH_PASSWORD_FILE" ]; then
  echo "DomainSpec password file is not readable: $DOMAINSPEC_AUTH_PASSWORD_FILE" >&2
  exit 1
fi

PASSWORD_LINE_COUNT="$(awk 'END {print NR}' "$DOMAINSPEC_AUTH_PASSWORD_FILE")"
PASSWORD_CHAR_COUNT="$(tr -d '\r\n' < "$DOMAINSPEC_AUTH_PASSWORD_FILE" | wc -c | tr -d ' ')"
if [ "$PASSWORD_LINE_COUNT" -ne 1 ] || [ "$PASSWORD_CHAR_COUNT" -lt 16 ]; then
  echo "DomainSpec password file must contain one line with at least 16 characters" >&2
  exit 2
fi

for required_path in \
  "$DOMAINSPEC_HTML_FILE" \
  "$DOMAINSPEC_MARKDOWN_FILE" \
  "$DOMAINSPEC_LANES_FILE" \
  "$DOMAINSPEC_SCHEMA_FILE" \
  "$COMPOSE_FILE" \
  "$NGINX_FILE"
do
  if [ ! -f "$required_path" ]; then
    echo "missing required deploy input: $required_path" >&2
    exit 1
  fi
done

if [ "$DEPLOY_SCOPE" = "full" ]; then
  for required_path in "$SITE_FILE" "$CRAFT_SITE_FILE" "$BELLA_SITE_FILE"
  do
    if [ ! -f "$required_path" ]; then
      echo "missing required deploy input: $required_path" >&2
      exit 1
    fi
  done
fi

SITE_DEPLOY_FILE="$SITE_FILE"
CRAFT_DEPLOY_FILE="$CRAFT_SITE_FILE"
BELLA_DEPLOY_FILE="$BELLA_SITE_FILE"

if [ "$DEPLOY_SCOPE" = "domainspec" ]; then
  CURRENT_PUBLIC_STAGE="$TMP_DIR/current-public"
  mkdir -p "$CURRENT_PUBLIC_STAGE"
  SITE_DEPLOY_FILE="$CURRENT_PUBLIC_STAGE/index.html"
  CRAFT_DEPLOY_FILE="$CURRENT_PUBLIC_STAGE/craft.html"
  BELLA_DEPLOY_FILE="$CURRENT_PUBLIC_STAGE/bella.html"

  echo "capturing the current public pages for a DomainSpec-only release"
  curl -fsS --max-time 30 "https://$PUBLIC_HOST/" -o "$SITE_DEPLOY_FILE"
  curl -fsS --max-time 30 "https://$PUBLIC_HOST/craft" -o "$CRAFT_DEPLOY_FILE"
  curl -fsS --max-time 30 "https://$PUBLIC_HOST/bella" -o "$BELLA_DEPLOY_FILE"
fi

SITE_SOURCE_SHA256="$(sha256sum "$SITE_DEPLOY_FILE" | awk '{print $1}')"
CRAFT_SOURCE_SHA256="$(sha256sum "$CRAFT_DEPLOY_FILE" | awk '{print $1}')"
BELLA_SOURCE_SHA256="$(sha256sum "$BELLA_DEPLOY_FILE" | awk '{print $1}')"
DOMAINSPEC_HTML_SHA256="$(sha256sum "$DOMAINSPEC_HTML_FILE" | awk '{print $1}')"
DOMAINSPEC_MARKDOWN_SHA256="$(sha256sum "$DOMAINSPEC_MARKDOWN_FILE" | awk '{print $1}')"
DOMAINSPEC_LANES_SHA256="$(sha256sum "$DOMAINSPEC_LANES_FILE" | awk '{print $1}')"
DOMAINSPEC_SCHEMA_SHA256="$(sha256sum "$DOMAINSPEC_SCHEMA_FILE" | awk '{print $1}')"

SITE_BUNDLE="$TMP_DIR/co-op-engine-site.tar.gz"
ENV_FILE="$TMP_DIR/co-op-engine.env"
SITE_STAGE="$TMP_DIR/site"
HTPASSWD_FILE="$TMP_DIR/domainspec.htpasswd"
NETRC_FILE="$TMP_DIR/domainspec.netrc"
DOMAIN_HEADERS_FILE="$TMP_DIR/domainspec.headers"

mkdir -p "$SITE_STAGE/craft" "$SITE_STAGE/bella" "$SITE_STAGE/domainspec"
cp "$SITE_DEPLOY_FILE" "$SITE_STAGE/index.html"
cp "$CRAFT_DEPLOY_FILE" "$SITE_STAGE/craft/index.html"
cp "$BELLA_DEPLOY_FILE" "$SITE_STAGE/bella/index.html"
cp "$DOMAINSPEC_HTML_FILE" "$SITE_STAGE/domainspec/index.html"
cp "$DOMAINSPEC_HTML_FILE" "$SITE_STAGE/domainspec/COMPLETE-GUIDE.html"
cp "$DOMAINSPEC_MARKDOWN_FILE" "$SITE_STAGE/domainspec/COMPLETE-GUIDE.md"
cp "$DOMAINSPEC_LANES_FILE" "$SITE_STAGE/domainspec/COMPLETE-GUIDE.lanes.json"
cp "$DOMAINSPEC_SCHEMA_FILE" "$SITE_STAGE/domainspec/COMPLETE-GUIDE.schema.json"

DOMAIN_PASSWORD="$(tr -d '\r\n' < "$DOMAINSPEC_AUTH_PASSWORD_FILE")"
DOMAIN_PASSWORD_HASH="$(printf '%s' "$DOMAIN_PASSWORD" | openssl passwd -apr1 -stdin)"
printf '%s:%s\n' "$DOMAINSPEC_AUTH_USERNAME" "$DOMAIN_PASSWORD_HASH" > "$HTPASSWD_FILE"
printf 'machine %s\nlogin %s\npassword %s\n' \
  "$PUBLIC_HOST" \
  "$DOMAINSPEC_AUTH_USERNAME" \
  "$DOMAIN_PASSWORD" \
  > "$NETRC_FILE"
chmod 600 "$HTPASSWD_FILE" "$NETRC_FILE"
unset DOMAIN_PASSWORD DOMAIN_PASSWORD_HASH

test "$(sha256sum "$SITE_STAGE/index.html" | awk '{print $1}')" = "$SITE_SOURCE_SHA256"
test "$(sha256sum "$SITE_STAGE/craft/index.html" | awk '{print $1}')" = "$CRAFT_SOURCE_SHA256"
test "$(sha256sum "$SITE_STAGE/bella/index.html" | awk '{print $1}')" = "$BELLA_SOURCE_SHA256"
test "$(sha256sum "$SITE_STAGE/domainspec/index.html" | awk '{print $1}')" = "$DOMAINSPEC_HTML_SHA256"
test "$(sha256sum "$SITE_STAGE/domainspec/COMPLETE-GUIDE.html" | awk '{print $1}')" = "$DOMAINSPEC_HTML_SHA256"
test "$(sha256sum "$SITE_STAGE/domainspec/COMPLETE-GUIDE.md" | awk '{print $1}')" = "$DOMAINSPEC_MARKDOWN_SHA256"
test "$(sha256sum "$SITE_STAGE/domainspec/COMPLETE-GUIDE.lanes.json" | awk '{print $1}')" = "$DOMAINSPEC_LANES_SHA256"
test "$(sha256sum "$SITE_STAGE/domainspec/COMPLETE-GUIDE.schema.json" | awk '{print $1}')" = "$DOMAINSPEC_SCHEMA_SHA256"
test "$(find "$SITE_STAGE" -type f | wc -l | tr -d ' ')" = "8"
tar -C "$SITE_STAGE" -czf "$SITE_BUNDLE" .

printf '%s\n' \
  "PUBLIC_HOST=$PUBLIC_HOST" \
  "EDGE_NETWORK=$EDGE_NETWORK" \
  "TRAEFIK_ENTRYPOINT=$TRAEFIK_ENTRYPOINT" \
  "TRAEFIK_CERT_RESOLVER=$TRAEFIK_CERT_RESOLVER" \
  > "$ENV_FILE"

echo "checking isolated remote directory: $REMOTE_DIR"
remote "if [ -e '$REMOTE_DIR' ] && [ ! -f '$REMOTE_DIR/.coop-engine-deployment' ]; then echo 'refusing unexpected existing remote directory: $REMOTE_DIR' >&2; exit 1; fi; mkdir -p '$REMOTE_DIR'; touch '$REMOTE_DIR/.coop-engine-deployment'"

echo "uploading the static pages and protected DomainSpec routing files"
upload "$SITE_BUNDLE" "site.tar.gz.next"
upload "$COMPOSE_FILE" "docker-compose.yml.next"
upload "$NGINX_FILE" "nginx.conf.next"
upload "$ENV_FILE" ".env.next"
upload "$HTPASSWD_FILE" ".domainspec.htpasswd.next"

echo "validating the staged site release"
if ! remote "set -eu; cd '$REMOTE_DIR'; rm -rf site.next; mkdir site.next; tar -xzf site.tar.gz.next -C site.next; test -f site.next/index.html; test -f site.next/craft/index.html; test -f site.next/bella/index.html; test -f site.next/domainspec/index.html; test -f site.next/domainspec/COMPLETE-GUIDE.html; test -f site.next/domainspec/COMPLETE-GUIDE.md; test -f site.next/domainspec/COMPLETE-GUIDE.lanes.json; test -f site.next/domainspec/COMPLETE-GUIDE.schema.json; test \"\$(sha256sum site.next/index.html | awk '{print \$1}')\" = '$SITE_SOURCE_SHA256'; test \"\$(sha256sum site.next/craft/index.html | awk '{print \$1}')\" = '$CRAFT_SOURCE_SHA256'; test \"\$(sha256sum site.next/bella/index.html | awk '{print \$1}')\" = '$BELLA_SOURCE_SHA256'; test \"\$(sha256sum site.next/domainspec/index.html | awk '{print \$1}')\" = '$DOMAINSPEC_HTML_SHA256'; test \"\$(sha256sum site.next/domainspec/COMPLETE-GUIDE.html | awk '{print \$1}')\" = '$DOMAINSPEC_HTML_SHA256'; test \"\$(sha256sum site.next/domainspec/COMPLETE-GUIDE.md | awk '{print \$1}')\" = '$DOMAINSPEC_MARKDOWN_SHA256'; test \"\$(sha256sum site.next/domainspec/COMPLETE-GUIDE.lanes.json | awk '{print \$1}')\" = '$DOMAINSPEC_LANES_SHA256'; test \"\$(sha256sum site.next/domainspec/COMPLETE-GUIDE.schema.json | awk '{print \$1}')\" = '$DOMAINSPEC_SCHEMA_SHA256'; docker compose --env-file .env.next -f docker-compose.yml.next config -q; docker run --rm --network none --entrypoint nginx -v '$REMOTE_DIR/site.next:/usr/share/nginx/html:ro' -v '$REMOTE_DIR/nginx.conf.next:/etc/nginx/conf.d/default.conf:ro' -v '$REMOTE_DIR/.domainspec.htpasswd.next:/etc/nginx/domainspec.htpasswd:ro' nginx:1.27-alpine -t"
then
  echo "candidate release validation failed; current release was not switched" >&2
  exit 1
fi

echo "switching to the validated site release"
if ! remote "set -eu; cd '$REMOTE_DIR'; cp -p docker-compose.yml docker-compose.yml.previous; cp -p nginx.conf nginx.conf.previous; cp -p .env .env.previous; if [ -f .domainspec.htpasswd ]; then cp -p .domainspec.htpasswd .domainspec.htpasswd.previous; else rm -f .domainspec.htpasswd.previous; fi; rm -rf site.previous site.failed; if [ -d site ]; then mv site site.previous; fi; mv site.next site; mv docker-compose.yml.next docker-compose.yml; mv nginx.conf.next nginx.conf; mv .env.next .env; install -o 101 -g 101 -m 0600 .domainspec.htpasswd.next .domainspec.htpasswd; rm -f .domainspec.htpasswd.next site.tar.gz.next"
then
  fail_with_rollback "release switch failed"
fi

echo "starting the isolated static container"
if ! remote "cd '$REMOTE_DIR' && docker compose --env-file .env -f docker-compose.yml up -d --pull always --force-recreate site"
then
  fail_with_rollback "container startup failed"
fi

echo "checking the container directly"
if ! remote "cd '$REMOTE_DIR' && docker compose --env-file .env -f docker-compose.yml exec -T site wget -qO- http://127.0.0.1/healthz"
then
  fail_with_rollback "container health check failed"
fi

if [ "$DRY_RUN" = "1" ]; then
  echo "dry run complete"
  exit 0
fi

echo "checking the public HTTPS route"
attempt=1
while [ "$attempt" -le 18 ]; do
  if verify_live_release; then
    echo "public HTTPS: pass"
    echo "existing route SHA-256 checks: pass"
    echo "DomainSpec anonymous access: 401"
    echo "DomainSpec authenticated HTML SHA-256: $DOMAINSPEC_HTML_SHA256"
    echo "DomainSpec private source tree: unavailable"
    echo "deploy complete: https://$PUBLIC_HOST/, https://$PUBLIC_HOST/craft, https://$PUBLIC_HOST/bella, and protected https://$PUBLIC_HOST/domainspec/"
    exit 0
  fi

  echo "public HTTPS not ready ($attempt/18)"
  sleep 5
  attempt=$((attempt + 1))
done

fail_with_rollback "public HTTPS validation failed"
