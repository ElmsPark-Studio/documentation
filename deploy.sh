#!/bin/bash
# documentation.elmspark.com — Deploy Script
#
# Builds the Astro Starlight site and pushes dist/ to the live VPS.
# Backs up the live site before rsyncing, then reloads nginx.
#
# Usage: bash deploy.sh

set -e

HERE="$(cd "$(dirname "$0")" && pwd)"
SERVER="ionos-ts"   # Tailscale SSH alias (User root, s2l key). Public port 22 closed 2026-05-27.
REMOTE="/var/www/documentation.elmspark.com"

echo "Building..."
cd "$HERE"
npm run build

echo ""
echo "Completeness gate (no JS-only content in guides)..."
# A guide that renders blank without JS would look broken to an AI, a no-JS browser or a PDF reader.
# Refuse to deploy if any guide has content that only exists in JS/JSON/data-attributes.
GATE="$HOME/Developer/elmspark/tools/verify-deliverable.py"
if [ -f "$GATE" ]; then
  GFAIL=0
  while IFS= read -r f; do
    python3 "$GATE" "$f" >/dev/null 2>&1 || { echo "  MISSING-CHUNK in: ${f#$HERE/dist/}"; python3 "$GATE" "$f" | sed -n '2,7p'; GFAIL=1; }
  done < <(find "$HERE/dist/guides" -name "index.html" 2>/dev/null)
  [ "$GFAIL" = 0 ] || { echo "ABORT: a guide has JS-only content. Not deploying a guide with a missing chunk."; exit 1; }
  echo "  completeness OK"
else
  echo "  (gate script not found at $GATE — skipping; install it to enforce)"
fi

echo ""
echo "Backing up live site..."
STAMP=$(date +%Y%m%d-%H%M%S)
ssh "$SERVER" "cp -a $REMOTE ${REMOTE}.bak.$STAMP"
echo "Backup: ${REMOTE}.bak.$STAMP"

echo ""
echo "Rsyncing dist/..."
rsync -av --delete "$HERE/dist/" "$SERVER:$REMOTE/"

echo ""
echo "Fixing ownership and reloading nginx..."
ssh "$SERVER" "chown -R www-data:www-data $REMOTE && nginx -t && systemctl reload nginx"

echo ""
echo "Verifying..."
CODE=$(curl -s -o /dev/null -w "%{http_code}" https://documentation.elmspark.com/)
echo "HTTP $CODE on https://documentation.elmspark.com/"

echo ""
echo "Done."
