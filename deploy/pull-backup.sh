#!/usr/bin/env bash
#
# Copy the newest server snapshot down to this machine.
#
# The daily timer on the server protects against mistakes. This protects
# against losing the server. Run it every so often.
#
#   ./deploy/pull-backup.sh [destination-dir]

set -euo pipefail

HOST="${DEPLOY_HOST:-mikrus}"
DEST="${1:-$HOME/Backups/weather-accuracy}"

mkdir -p "$DEST"

latest=$(ssh "$HOST" 'ls -1t /var/backups/weather-accuracy/weather-*.db.gz | head -1')
[ -n "$latest" ] || { echo "No backups on the server yet."; exit 1; }

scp "$HOST:$latest" "$DEST/"
name=$(basename "$latest")

gzip -t "$DEST/$name"
echo "Pulled $name to $DEST ($(du -h "$DEST/$name" | cut -f1)), archive intact"
