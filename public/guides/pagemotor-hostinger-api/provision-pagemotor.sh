#!/usr/bin/env bash
# provision-pagemotor.sh
# On-box setup script: run this via SSH after the Hostinger VPS is provisioned.
# It creates the CloudPanel site + database, deploys PageMotor, and issues the SSL cert.
#
# USAGE (Claude Code will run this for you):
#   ssh root@VPS_IP 'bash -s' < provision-pagemotor.sh DOMAIN SITE_SLUG DB_PASS PM_ZIP_DEST
#
# Or tell Claude Code:
#   "SSH into [IP] and run provision-pagemotor.sh for [domain]"
#
# ARGUMENTS:
#   $1  DOMAIN    e.g. mysite.com
#   $2  SITE_SLUG short slug used as site user and in db names  e.g. mysite
#   $3  DB_PASS   a strong random password for the database user
#   $4  PM_ZIP    path to the PageMotor zip already on the server  e.g. /tmp/pagemotor.zip

set -euo pipefail

DOMAIN="${1:?Arg 1 required: domain (e.g. mysite.com)}"
SLUG="${2:?Arg 2 required: site slug (e.g. mysite)}"
DB_PASS="${3:?Arg 3 required: database password}"
PM_ZIP="${4:-/tmp/pagemotor.zip}"

DB_NAME="${SLUG}-db"
DB_USER="${SLUG}-user"
SITE_PASS="$(openssl rand -base64 18 | tr -d '=/+' | head -c 20)"

PINE="\033[32m"; YELL="\033[33m"; OFF="\033[0m"
log()  { echo -e "${PINE}▶ $*${OFF}"; }
warn() { echo -e "${YELL}⚠ $*${OFF}"; }

# -- Step 1: CloudPanel site --
log "Creating PHP 8.3 site: $DOMAIN (user: $SLUG)"
clpctl site:add:php \
  --domainName="$DOMAIN" \
  --phpVersion=8.3 \
  --vhostTemplate="Generic" \
  --siteUser="$SLUG" \
  --siteUserPassword="$SITE_PASS"

# -- Step 2: Database --
log "Creating database: $DB_NAME"
clpctl db:add \
  --domainName="$DOMAIN" \
  --databaseName="$DB_NAME" \
  --databaseUserName="$DB_USER" \
  --databaseUserPassword="$DB_PASS"

# -- Step 3: Deploy PageMotor --
WEBROOT="/home/$SLUG/htdocs/$DOMAIN"
log "Deploying PageMotor from $PM_ZIP to $WEBROOT"

[[ -f "$PM_ZIP" ]] || { warn "PageMotor zip not at $PM_ZIP — upload it first"; exit 1; }

TMPDIR="/tmp/pm-deploy-$$"
mkdir -p "$TMPDIR"
unzip -q "$PM_ZIP" -d "$TMPDIR"

# Find the folder containing index.php (handles pagemotor-X.X.Xb/ wrapper)
PMDIR=$(find "$TMPDIR" -name "index.php" -maxdepth 2 | head -1 | xargs dirname)
[[ -n "$PMDIR" ]] || { warn "Could not find index.php in zip"; exit 1; }

cp -a "$PMDIR/." "$WEBROOT/"
rm -rf "$TMPDIR"

# -- Step 4: config.php --
log "Writing config.php"
cat > "$WEBROOT/config.php" << CONF
<?php
define( 'DB_NAME',         '$DB_NAME' );
define( 'DB_USER',         '$DB_USER' );
define( 'DB_PASSWORD',     '$DB_PASS' );
define( 'DB_HOST',         '127.0.0.1' );
define( 'DB_CHARSET',      'utf8mb4' );
define( 'DB_COLLATE',      'utf8mb4_unicode_ci' );
define( 'DB_TABLE_PREFIX', 'pm_' );
define( 'DB_FLAGS',        0 );
define( 'PM_HTML_CHARSET',     'UTF-8' );
define( 'PM_INSTALL_LOCATION', '/' );
define( 'PM_ADMIN_SLUG',   'admin' );
define( 'PM_API_SLUG',     'api' );
define( 'PM_MCP_SLUG',     'mcp' );
define( 'PM_ERROR_LOGS',   true );
CONF

# -- Step 5: Ownership --
log "Setting file ownership"
chown -R "$SLUG:www-data" "$WEBROOT/"
find "$WEBROOT" -type d -exec chmod 755 {} \;
find "$WEBROOT" -type f -exec chmod 644 {} \;

# -- Step 6: Wait for DNS, then SSL --
log "Checking DNS for $DOMAIN..."
VPS_IP=$(hostname -I | awk '{print $1}')
for i in $(seq 1 18); do
  RESOLVED=$(dig +short "$DOMAIN" 2>/dev/null | head -1 || true)
  [[ "$RESOLVED" == "$VPS_IP" ]] && break
  warn "  DNS not yet resolved (attempt $i/18, waiting 20s)..."
  sleep 20
done

if [[ "$RESOLVED" == "$VPS_IP" ]]; then
  log "DNS resolved. Requesting Let's Encrypt certificate..."
  clpctl lets-encrypt:install:certificate --domainName="$DOMAIN" \
    && log "SSL certificate installed" \
    || warn "SSL failed — retry with: clpctl lets-encrypt:install:certificate --domainName=$DOMAIN"
else
  warn "DNS still not resolved. Set an A record for $DOMAIN → $VPS_IP then retry SSL."
  warn "Retry: clpctl lets-encrypt:install:certificate --domainName=$DOMAIN"
fi

# -- Done --
echo ""
echo -e "${PINE}=== PageMotor deployed ===${OFF}"
echo "  Site root: $WEBROOT"
echo "  DB name:   $DB_NAME"
echo "  DB user:   $DB_USER"
echo "  DB pass:   $DB_PASS"
echo "  Admin:     https://$DOMAIN/admin/"
echo ""
echo "Visit https://$DOMAIN/ — if it loads, create your admin account at /admin/ right away."
