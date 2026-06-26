#!/usr/bin/env bash
# provision-pagemotor.sh
# On-box setup script for CloudPanel + PageMotor.
# Run this via SSH after the VPS is provisioned (by Claude Code via the Hostinger MCP or API).
#
# USAGE:
#   ssh root@VPS_IP 'bash -s' -- << 'EOF' < provision-pagemotor.sh DOMAIN SLUG DB_PASS PM_ZIP_PATH
#
# Or tell Claude Code:
#   "SSH into [IP] as root using ~/.ssh/id_ed25519 and run provision-pagemotor.sh
#    for domain mysite.com, slug mysite. The PageMotor zip is at /tmp/pagemotor.zip."
#
# ARGUMENTS:
#   $1  DOMAIN    e.g. mysite.com
#   $2  SLUG      short identifier used as site user + in db name  e.g. mysite
#   $3  DB_PASS   strong random password for the database user
#   $4  PM_ZIP    path to the PageMotor zip already on the server  default: /tmp/pagemotor.zip

set -euo pipefail

DOMAIN="${1:?Arg 1 required: domain (e.g. mysite.com)}"
SLUG="${2:?Arg 2 required: site slug (e.g. mysite)}"
DB_PASS="${3:?Arg 3 required: database password}"
PM_ZIP="${4:-/tmp/pagemotor.zip}"

# CloudPanel requires hyphens, not underscores, in db names and usernames
DB_NAME="${SLUG}-db"
DB_USER="${SLUG}-user"
SITE_PASS="$(openssl rand -base64 18 | tr -d '=/+' | head -c 20)"
WEBROOT="/home/$SLUG/htdocs/$DOMAIN"

PINE="\033[32m"; YELL="\033[33m"; OFF="\033[0m"
log()  { echo -e "${PINE}▶ $*${OFF}"; }
warn() { echo -e "${YELL}⚠ $*${OFF}"; }

# ── Step 1: Create CloudPanel site ──────────────────────────────────────────
log "Creating PHP 8.3 site for $DOMAIN (user: $SLUG)"
# PHP must be 8.3 — CloudPanel may default to 8.5; PageMotor needs ≥8.2 (8.3 is proven)
clpctl site:add:php \
  --domainName="$DOMAIN" \
  --phpVersion=8.3 \
  --vhostTemplate="Generic" \
  --siteUser="$SLUG" \
  --siteUserPassword="$SITE_PASS"

# ── Step 2: Create database ─────────────────────────────────────────────────
log "Creating database $DB_NAME (user: $DB_USER)"
# CloudPanel rejects underscores in DB name/username — use hyphens
clpctl db:add \
  --domainName="$DOMAIN" \
  --databaseName="$DB_NAME" \
  --databaseUserName="$DB_USER" \
  --databaseUserPassword="$DB_PASS"

# ── Step 3: Deploy PageMotor ────────────────────────────────────────────────
log "Deploying PageMotor from $PM_ZIP to $WEBROOT"
[[ -f "$PM_ZIP" ]] || { warn "PageMotor zip not found at $PM_ZIP — upload it first"; exit 1; }

TMPDIR="/tmp/pm-deploy-$$"
mkdir -p "$TMPDIR"
unzip -q "$PM_ZIP" -d "$TMPDIR"

# Handle wrapper folder (e.g. pagemotor-0.9.4b/) — find the dir containing index.php
PMDIR=$(find "$TMPDIR" -name "index.php" -maxdepth 2 | head -1 | xargs dirname)
[[ -n "$PMDIR" ]] || { warn "Could not find index.php inside the zip"; exit 1; }

# Deploy straight into site root (no subfolder = no web root change needed)
cp -a "$PMDIR/." "$WEBROOT/"
rm -rf "$TMPDIR"

# ── Step 4: Write config.php ────────────────────────────────────────────────
log "Writing config.php"
cat > "$WEBROOT/config.php" << CONF
<?php
define( 'DB_NAME',         '${DB_NAME}' );
define( 'DB_USER',         '${DB_USER}' );
define( 'DB_PASSWORD',     '${DB_PASS}' );
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

# ── Step 5: Fix ownership ───────────────────────────────────────────────────
log "Setting ownership and permissions"
chown -R "$SLUG:www-data" "$WEBROOT/"
find "$WEBROOT" -type d -exec chmod 755 {} \;
find "$WEBROOT" -type f -exec chmod 644 {} \;

# ── Step 6: Wait for DNS, then SSL cert ─────────────────────────────────────
log "Checking DNS for $DOMAIN..."
VPS_IP=$(hostname -I | awk '{print $1}')
RESOLVED=""
for i in $(seq 1 18); do
  RESOLVED=$(dig +short "$DOMAIN" 2>/dev/null | grep -F "$VPS_IP" || true)
  [[ -n "$RESOLVED" ]] && break
  warn "  DNS not yet pointing here (check $i/18, waiting 20s)..."
  sleep 20
done

if [[ -n "$RESOLVED" ]]; then
  log "DNS confirmed. Requesting Let's Encrypt certificate..."
  clpctl lets-encrypt:install:certificate --domainName="$DOMAIN" \
    && log "SSL certificate installed" \
    || warn "SSL failed — retry: clpctl lets-encrypt:install:certificate --domainName=$DOMAIN"
else
  warn "DNS still not resolved after 6 min. Add an A record for $DOMAIN → $VPS_IP"
  warn "Then retry: clpctl lets-encrypt:install:certificate --domainName=$DOMAIN"
fi

# ── Done ─────────────────────────────────────────────────────────────────────
echo ""
echo -e "${PINE}=== PageMotor deployed ===${OFF}"
echo "  URL:       https://$DOMAIN/"
echo "  Admin:     https://$DOMAIN/admin/  ← register here first"
echo "  Site root: $WEBROOT"
echo "  DB name:   $DB_NAME"
echo "  DB user:   $DB_USER"
echo "  DB pass:   $DB_PASS"
echo ""
echo -e "${YELL}Save the DB password — it is not stored anywhere else.${OFF}"
