#!/usr/bin/env sh
set -eu

cd "$(dirname "$0")/.."

COMPOSE_FILE="docker-compose.e2e.yml"
export COMPOSE_PROJECT_NAME="body-war-v2-validation-$$"
SERVICE_NAME="body-war-postgres"
export BODY_WAR_DATABASE_URL="postgres://body_war_e2e:body_war_e2e_password@127.0.0.1:${BODY_WAR_E2E_POSTGRES_PORT:-55483}/body_war_e2e"
export BODY_WAR_AUTH_BACKEND="postgres"
export BODY_WAR_STRAVA_FAKE="1"

compose() {
  docker compose -f "$COMPOSE_FILE" "$@"
}

require_docker() {
  if ! docker info >/dev/null 2>&1; then
    echo "Docker is not available. Start Docker, then rerun the E2E command." >&2
    exit 2
  fi
}

up() {
  require_docker
  if ! compose up -d --wait; then
    echo "BodyWar PostgreSQL E2E container failed to become healthy." >&2
    compose ps >&2 || true
    compose logs "$SERVICE_NAME" >&2 || true
    exit 1
  fi
}

down() {
  require_docker
  compose down -v --remove-orphans
}

run() {
  npm run e2e
}

all() {
  status=0
  up || status=$?

  if [ "$status" -eq 0 ]; then
    run || status=$?
  fi

  down || {
    down_status=$?
    if [ "$status" -eq 0 ]; then
      status=$down_status
    fi
  }

  exit "$status"
}

case "${1:-all}" in
  up)
    up
    ;;
  down)
    down
    ;;
  run)
    run
    ;;
  all)
    all
    ;;
  *)
    echo "Usage: $0 [up|down|run|all]" >&2
    exit 2
    ;;
esac
