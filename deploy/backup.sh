#!/usr/bin/env bash
#
# Snapshot the database and keep the last two weeks of them.
#
# Uses sqlite's own backup API rather than cp, because a plain copy of a live
# database can catch it mid-write. The sqlite3 CLI is not installed here, so
# this goes through Python, which ships with the same engine.

set -euo pipefail

DB=/var/lib/weather-accuracy/weather.db
DEST=/var/backups/weather-accuracy
KEEP=14

mkdir -p "$DEST"
OUT="$DEST/weather-$(date +%Y%m%d).db"

python3 - "$DB" "$OUT" <<'PY'
import sqlite3, sys
src, dst = sqlite3.connect(sys.argv[1]), sqlite3.connect(sys.argv[2])
with dst:
    src.backup(dst)
src.close(); dst.close()
PY

gzip -f "$OUT"

# Oldest first past the keep count, then delete.
ls -1t "$DEST"/weather-*.db.gz 2>/dev/null | tail -n +$((KEEP + 1)) | xargs -r rm -f

echo "backup: $OUT.gz ($(du -h "$OUT.gz" | cut -f1)), $(ls -1 "$DEST"/weather-*.db.gz | wc -l) kept"
