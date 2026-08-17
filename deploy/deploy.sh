#!/usr/bin/env bash
#
# Ship whatever is on the current branch to the server.
#
#   ./deploy/deploy.sh
#   DEPLOY_HOST=other-server ./deploy/deploy.sh
#
# Expects an ssh alias (see ~/.ssh/config) that can reach the box as root.

set -euo pipefail

HOST="${DEPLOY_HOST:-mikrus}"
APP_DIR=/opt/weather-accuracy
WEB_ROOT=/var/www/weather-accuracy
REPO_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"

cd "$REPO_ROOT"

step() { printf '\n\033[1m==> %s\033[0m\n' "$1"; }

step "Checking the working tree is clean"
if [ -n "$(git status --porcelain)" ]; then
    echo "Uncommitted changes. The server pulls from git, so commit and push first."
    git status --short
    exit 1
fi

if [ "${DEPLOY_SKIP_PUSH:-}" = "1" ]; then
    step "Skipping push (DEPLOY_SKIP_PUSH=1)"
else
    step "Pushing to origin"
    git push
fi

step "Running checks"
pnpm web:check
(cd apps/api && uv run poe check)

step "Building the frontend"
pnpm web:build

step "Uploading static files"
rsync -az --delete "apps/web/dist/" "$HOST:$WEB_ROOT/"

step "Updating the backend"
ssh "$HOST" "
    set -e
    sudo -u weather git -C $APP_DIR pull --ff-only
    cd $APP_DIR/apps/api
    sudo -u weather env PATH=/usr/local/bin:\$PATH HOME=/home/weather uv sync --no-dev
    sudo -u weather env PATH=/usr/local/bin:\$PATH HOME=/home/weather uv run alembic upgrade head
    systemctl restart weather-api
"

step "Smoke test"
sleep 3
ssh "$HOST" '
    set -e
    code=$(curl -s -o /dev/null -w "%{http_code}" "http://127.0.0.1/api/analytics?metric=temp_max")
    [ "$code" = "200" ] || { echo "API returned $code"; journalctl -u weather-api -n 20 --no-pager; exit 1; }
    code=$(curl -s -o /dev/null -w "%{http_code}" http://127.0.0.1/)
    [ "$code" = "200" ] || { echo "Site returned $code"; exit 1; }
    echo "API and site both answered 200"
'

step "Done"

