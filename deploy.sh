#!/bin/bash
# documentation.elmspark.com — Deploy Script
#
# Builds the Astro Starlight site and pushes dist/ to the live VPS.
# Backs up the live site before rsyncing, then reloads nginx.
#
# Usage: bash deploy.sh

set -e

HERE="$(cd "$(dirname "$0")" && pwd)"
SERVER="root@88.208.226.236"
REMOTE="/var/www/documentation.elmspark.com"

echo "Building..."
cd "$HERE"
npm run build

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
