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
#
# REPAIR MODE (for a site this script already built, or one built by hand):
#   bash provision-pagemotor.sh --fix-wellknown mysite.com
#   Re-applies only the /.well-known/ vhost fix. Safe to run repeatedly. Run it
#   again after anything that re-renders the vhost (a certificate reinstall, a
#   PHP version change), if you did not let this script do that step for you.

set -euo pipefail

PINE="\033[32m"; YELL="\033[33m"; OFF="\033[0m"
log()  { echo -e "${PINE}▶ $*${OFF}"; }
warn() { echo -e "${YELL}⚠ $*${OFF}"; }

# ── /.well-known/ vhost fix ──────────────────────────────────────────────────
# Why this exists: PageMotor serves its OAuth discovery documents
# (/.well-known/oauth-protected-resource, /.well-known/oauth-authorization-server,
# /.well-known/api-catalog) as DYNAMIC routes, not as files on disk. CloudPanel's
# stock vhost ships `location ~ /.well-known { auth_basic off; allow all; }`, which
# hands the whole namespace to the filesystem. Nothing is there, so an MCP client
# fetching discovery gets a 404 and sign-in fails before it starts.
#
# On current CloudPanel that block sits in the FRONT server (80/443, TLS
# termination, proxy to a backend on 127.0.0.1:8080), which has no PHP handler at
# all — so the php-fpm-style `try_files … /index.php` fix routes nowhere there.
# The front server must PROXY the namespace to the backend instead.
#
# We proxy the whole /.well-known/ namespace rather than enumerating the three
# discovery paths, because PageMotor already publishes a third document
# (/.well-known/api-catalog, RFC 9727) and an enumerated fix goes stale the day a
# fourth appears.
#
# The acme-challenge location must be PRESENT, and must keep `auth_basic off;
# allow all;` and `try_files $uri =404;`. Its POSITION is irrelevant: among
# prefix locations nginx takes the longest match, and file order does not come
# into it. What matters is that it exists at all. Proxy the whole namespace with
# no acme-challenge location anywhere in the vhost and Let's Encrypt's HTTP-01
# challenge goes to PageMotor, which cannot answer it. Nothing appears to break
# on the day you make the change; the certificate stops renewing ~90 days later.
#
# How load-bearing the block is depends on the vhost shape. On a single-server
# vhost proxying to a backend with no filesystem root, it is the only thing
# answering the challenge and its absence breaks renewal outright. On
# CloudPanel's two-server layout the backend carries its own root plus
# try_files, so a real challenge file is found on disk before anything reaches
# index.php. We emit it either way: it costs nothing, it documents intent, and
# it makes the vhost correct on both layouts. We emit it first because that
# reads clearly, not because order changes behaviour.
#
# See section 6d of https://documentation.elmspark.com/guides/pagemotor-mcp-troubleshooting/
#
# We patch the PER-SITE vhost, not the vhost template. Templates are rows in
# CloudPanel's SQLite database (/home/clp/htdocs/app/data/db.sq3, table
# `vhost_template`), they are shared by every site the box will ever create, and
# CloudPanel refreshes them from its upstream GitHub repo nightly — a template
# patch would silently revert and would change sites this script never touched.
# A per-site edit is what the CloudPanel Vhost tab writes, and it survives
# certificate renewal.

fix_wellknown() {
  local DOMAIN="$1"
  local VHOST="/etc/nginx/sites-enabled/${DOMAIN}.conf"
  local CLPDB="/home/clp/htdocs/app/data/db.sq3"
  local STAMP; STAMP="$(date +%Y%m%d-%H%M%S)"

  [[ -f "$VHOST" ]] || { warn "No vhost at $VHOST — skipping the /.well-known/ fix"; return 1; }

  log "Patching /.well-known/ in $VHOST (PageMotor OAuth discovery)"
  cp -a "$VHOST" "${VHOST}.pm-bak-${STAMP}"

  local PY="/tmp/pm-wellknown-$$.py"
  cat > "$PY" <<'PMPY'
import re, sys

path = sys.argv[1]
src  = open(path, encoding='utf-8').read()

MARK_A = "# >>> PageMotor OAuth discovery (provision-pagemotor.sh) >>>"
MARK_B = "# <<< PageMotor OAuth discovery (provision-pagemotor.sh) <<<"

def mask(text):
    """Blank out comments and quoted strings so brace counting is safe."""
    out = list(text); i = 0; n = len(text)
    while i < n:
        c = text[i]
        if c == '#':
            while i < n and text[i] != '\n':
                out[i] = ' '; i += 1
        elif c in '"\'':
            q = c; out[i] = ' '; i += 1
            while i < n and text[i] != q:
                if text[i] == '\\':
                    out[i] = ' '; i += 1
                if i < n:
                    out[i] = ' '; i += 1
            if i < n:
                out[i] = ' '; i += 1
        else:
            i += 1
    return ''.join(out)

def close_brace(m, open_idx, end=None):
    """Index just past the '}' that closes the '{' at open_idx."""
    end = len(m) if end is None else end
    depth = 0; j = open_idx
    while j < end:
        if m[j] == '{':
            depth += 1
        elif m[j] == '}':
            depth -= 1
            if depth == 0:
                return j + 1
        j += 1
    return -1

m = mask(src)

# Top-level `server { ... }` blocks.
servers = []
for mo in re.finditer(r'(?m)^[ \t]*server[ \t]*\{', m):
    o = mo.end() - 1
    e = close_brace(m, o)
    if e > 0:
        servers.append((mo.start(), e))
if not servers:
    sys.exit("no server block found")

# Front = the server listening on 80/443. Backend = any other server block that
# carries the PHP handler. Deliberately NOT keyed on port 8080: the guide's rule
# is to read the port off the config rather than assume it.
front = None; others = []
for sp in servers:
    body = m[sp[0]:sp[1]]
    is_edge = re.search(r'(?m)^[ \t]*listen[ \t]+(\[::\]:)?(80|443)\b', body)
    if is_edge and front is None and re.search(r'(?m)^[ \t]*(root|location)\b', body):
        front = sp
    else:
        others.append(sp)
if front is None:
    front, others = servers[0], servers[1:]

backend = None
for sp in others:
    if re.search(r'fastcgi_pass|try_files', m[sp[0]:sp[1]]):
        backend = sp
        break

fb = src[front[0]:front[1]]

# 1. Drop any previous run of ours, remembering exactly where it sat so a
#    re-run lands in the same place and produces a byte-identical file.
anchor = None; indent = None
mk = re.search(re.escape(MARK_A) + r'[\s\S]*?' + re.escape(MARK_B) + r'[ \t]*\n?', fb)
if mk:
    line_start = fb.rfind('\n', 0, mk.start()) + 1
    indent = fb[line_start:mk.start()]
    if indent.strip():
        indent = None
    anchor = line_start
    fb = fb[:line_start] + fb[mk.end():]

# 2. Drop every remaining .well-known location in the front server, remembering
#    where the first one sat so the replacement lands in the same place.
def wellknown_spans(text):
    mm = mask(text); spans = []
    for mo in re.finditer(r'(?m)^[ \t]*location\b([^{]*)\{', mm):
        sel = mo.group(1)
        if 'well-known' not in sel and 'well_known' not in sel:
            continue
        o = mo.end() - 1
        e = close_brace(mm, o)
        if e > 0:
            spans.append((mo.start(), e))
    # keep only outermost, in order
    out = []
    for s in sorted(spans):
        if not out or s[0] >= out[-1][1]:
            out.append(s)
    return out

spans = wellknown_spans(fb)
if spans:
    if anchor is None:
        anchor = spans[0][0]
        indent = re.match(r'[ \t]*', fb[spans[0][0]:]).group(0)
    for s, e in reversed(spans):
        tail = e
        while tail < len(fb) and fb[tail] in ' \t':
            tail += 1
        if tail < len(fb) and fb[tail] == '\n':
            tail += 1
        fb = fb[:s] + fb[tail:]
        if anchor is not None and s < anchor:
            anchor -= (tail - s)

# 3. Work out where to proxy to — read it off the front server's own
#    `location /`, never assume the port.
# If the PHP handler lives in the front server itself, try_files is the right
# fix there (hand-rolled nginx, the Vultr guide, older single-server CloudPanel).
# Only proxy when the front has no PHP to hand anything to.
front_has_php = re.search(r'fastcgi_pass', m[front[0]:front[1]]) is not None
mode   = 'proxy' if (backend and not front_has_php) else 'php'
target = 'http://127.0.0.1:8080'
if mode == 'proxy':
    mo = re.search(r'(?m)^[ \t]*proxy_pass[ \t]+(https?://[^\s;]+)[ \t]*;', mask(fb))
    if mo:
        target = re.search(r'(https?://[^\s;]+)', fb[mo.start(1):mo.end(1)]).group(1).rstrip('/')

# 4. Pick an insertion point if there was no existing block to replace.
if anchor is None:
    mo = re.search(r'(?m)^[ \t]*location\b[^{]*\{', mask(fb))
    if mo:
        anchor = mo.start()
        indent = re.match(r'[ \t]*', fb[mo.start():]).group(0)
    else:
        anchor = fb.rfind('}')
        indent = '  '
if indent is None:
    indent = '  '

I = indent
B = I + "  "
block = [
    I + MARK_A,
    I + "# Let's Encrypt HTTP-01, answered from disk. Keep this block. Its position",
    I + "# is irrelevant (nginx takes the longest prefix match, not the first one);",
    I + "# what matters is that it exists. Remove it on a vhost whose backend has no",
    I + "# filesystem root and renewal silently stops working about 90 days later.",
    I + "location ^~ /.well-known/acme-challenge/ {",
    B + "auth_basic off;",
    B + "allow all;",
    B + "try_files $uri =404;",
    I + "}",
    "",
    I + "# PageMotor serves OAuth discovery as dynamic routes, not files on disk.",
]
if mode == 'proxy':
    block += [
        I + "# This front server has no PHP handler, so hand the namespace to the backend.",
        I + "location ^~ /.well-known/ {",
        B + "auth_basic off;",
        B + "allow all;",
        B + "proxy_pass " + target + ";",
        B + "proxy_set_header Host $host;",
        B + "proxy_set_header X-Forwarded-Host $host;",
        B + "proxy_set_header X-Real-IP $remote_addr;",
        B + "proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;",
        I + "}",
    ]
else:
    block += [
        I + "location ^~ /.well-known/ {",
        B + "auth_basic off;",
        B + "allow all;",
        B + "try_files $uri $uri/ /index.php?$args;",
        I + "}",
    ]
block.append(I + MARK_B)

fb = fb[:anchor] + "\n".join(block) + "\n\n" + fb[anchor:]

# Collapse the blank lines our deletions leave behind, so re-running this on a
# renewal produces a byte-identical file rather than slowly growing one.
fb = re.sub(r'\n(?:[ \t]*\n){2,}', '\n\n', fb)

out = src[:front[0]] + fb + src[front[1]:]
open(path, 'w', encoding='utf-8').write(out)
print("MODE=%s TARGET=%s" % (mode, target if mode == 'proxy' else '-'))
PMPY

  local RESULT=""
  if ! RESULT="$(python3 "$PY" "$VHOST")"; then
    warn "Could not parse the vhost — restoring ${VHOST}.pm-bak-${STAMP} and leaving it alone"
    cp -a "${VHOST}.pm-bak-${STAMP}" "$VHOST"
    rm -f "$PY"
    return 1
  fi
  rm -f "$PY"
  log "  $RESULT"

  if ! nginx -t 2>/dev/null; then
    warn "nginx -t FAILED after the /.well-known/ patch — rolling back"
    cp -a "${VHOST}.pm-bak-${STAMP}" "$VHOST"
    nginx -t || true
    return 1
  fi
  systemctl reload nginx
  log "  nginx reloaded"

  # Mirror the patched vhost into CloudPanel's own store so a later re-render
  # (certificate reinstall, PHP version change) does not quietly revert it.
  # Best effort: we only ever overwrite a column that already holds THIS site's
  # vhost text, and we back the database up first.
  if [[ -f "$CLPDB" ]]; then
    cp -a "$CLPDB" "${CLPDB}.pm-bak-${STAMP}"
    local PYDB="/tmp/pm-clpdb-$$.py"
    cat > "$PYDB" <<'PMDB'
import sqlite3, sys

db, domain, vhost_path = sys.argv[1], sys.argv[2], sys.argv[3]
text = open(vhost_path, encoding='utf-8').read()

con = sqlite3.connect(db, timeout=20)
con.execute("PRAGMA busy_timeout=20000")
cur = con.cursor()

tables = [r[0] for r in cur.execute(
    "SELECT name FROM sqlite_master WHERE type='table'").fetchall()]
if 'site' not in tables:
    sys.exit("no `site` table")

cols = [r[1] for r in cur.execute("PRAGMA table_info(site)").fetchall()]

# Which column holds the domain? The one where exactly this site matches.
domcol = None
for c in cols:
    try:
        n = cur.execute('SELECT COUNT(*) FROM site WHERE "%s" = ?' % c, (domain,)).fetchone()[0]
    except sqlite3.Error:
        continue
    if n == 1:
        domcol = c
        break
if domcol is None:
    sys.exit("could not identify the domain column for %s" % domain)

row = cur.execute('SELECT * FROM site WHERE "%s" = ?' % domcol, (domain,)).fetchone()
names = [d[0] for d in cur.description]

# Which column holds the rendered vhost? The one that already looks like one.
vhcol = None
for name, val in zip(names, row):
    if isinstance(val, str) and 'server' in val and '{' in val and 'listen' in val:
        vhcol = name
        break
if vhcol is None:
    sys.exit("no column on this row holds a rendered vhost — file patched, database left alone")

cur.execute('UPDATE site SET "%s" = ? WHERE "%s" = ?' % (vhcol, domcol), (text, domain))
con.commit()
con.close()
print("synced site.%s for %s (matched on %s)" % (vhcol, domain, domcol))
PMDB
    local DBOUT
    if DBOUT="$(python3 "$PYDB" "$CLPDB" "$DOMAIN" "$VHOST" 2>&1)"; then
      log "  CloudPanel database: $DBOUT"
    else
      warn "  CloudPanel database not updated: $DBOUT"
      warn "  The live vhost IS fixed. If CloudPanel later re-renders it, re-run:"
      warn "    bash provision-pagemotor.sh --fix-wellknown $DOMAIN"
    fi
    rm -f "$PYDB"
  fi

  # ── Self-test, from this box, against the front server ────────────────────
  local ROOT PROBE
  ROOT="$(awk '/^[[:space:]]*root[[:space:]]/ {print $2; exit}' "$VHOST" | tr -d ';')"

  # 1. acme-challenge must still be answered from disk.
  if [[ -n "$ROOT" && -d "$ROOT" ]]; then
    mkdir -p "$ROOT/.well-known/acme-challenge"
    PROBE="pm-provision-probe-$$"
    echo "pm-acme-probe" > "$ROOT/.well-known/acme-challenge/$PROBE"
    chmod 755 "$ROOT/.well-known" "$ROOT/.well-known/acme-challenge"
    chmod 644 "$ROOT/.well-known/acme-challenge/$PROBE"
    local ACME
    ACME="$(curl -sk --max-time 15 --resolve "${DOMAIN}:443:127.0.0.1" \
      "https://${DOMAIN}/.well-known/acme-challenge/${PROBE}" 2>/dev/null || true)"
    rm -f "$ROOT/.well-known/acme-challenge/$PROBE"
    if [[ "$ACME" == "pm-acme-probe" ]]; then
      log "  acme-challenge still served from disk ✓ (Let's Encrypt renewal safe)"
    else
      warn "  acme-challenge did NOT return the file from disk — got: ${ACME:0:80}"
      warn "  Certificate renewal will fail in ~90 days. Check the vhost before going live."
    fi
  fi

  # 2. OAuth discovery must reach PageMotor, not the filesystem.
  local HDRS CODE CT
  HDRS="$(curl -sk --max-time 15 -D - -o /dev/null --resolve "${DOMAIN}:443:127.0.0.1" \
    "https://${DOMAIN}/.well-known/oauth-protected-resource" 2>/dev/null || true)"
  CODE="$(printf '%s' "$HDRS" | awk 'NR==1 {print $2}')"
  CT="$(printf '%s' "$HDRS" | awk 'tolower($1)=="content-type:" {print $2}' | tr -d '\r')"
  if [[ "$CT" == application/json* ]]; then
    log "  OAuth discovery: HTTP $CODE $CT — PageMotor is answering ✓"
  elif printf '%s' "$HDRS" | grep -qi '^accept-ranges:'; then
    warn "  OAuth discovery: HTTP $CODE $CT, served from DISK (accept-ranges present)."
    warn "  Delete any hand-made .well-known files under $ROOT and re-run --fix-wellknown."
  else
    warn "  OAuth discovery: HTTP $CODE ${CT:-no content-type} — not JSON yet."
    warn "  Expected before PageMotor's setup wizard has been completed. Re-check with:"
    warn "    curl -sI https://${DOMAIN}/.well-known/oauth-protected-resource"
  fi
}

# ── Repair mode ──────────────────────────────────────────────────────────────
if [[ "${1:-}" == "--fix-wellknown" ]]; then
  fix_wellknown "${2:?Arg 2 required: domain (e.g. mysite.com)}"
  exit 0
fi

DOMAIN="${1:?Arg 1 required: domain (e.g. mysite.com)}"
SLUG="${2:?Arg 2 required: site slug (e.g. mysite)}"
DB_PASS="${3:?Arg 3 required: database password}"
PM_ZIP="${4:-/tmp/pagemotor.zip}"

# CloudPanel requires hyphens, not underscores, in db names and usernames
DB_NAME="${SLUG}-db"
DB_USER="${SLUG}-user"
SITE_PASS="$(openssl rand -base64 18 | tr -d '=/+' | head -c 20)"
WEBROOT="/home/$SLUG/htdocs/$DOMAIN"

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

# ── Step 7: PageMotor OAuth discovery (/.well-known/) ───────────────────────
# Runs AFTER the certificate step on purpose: installing a certificate re-renders
# the vhost, which would throw this patch away if we applied it first.
fix_wellknown "$DOMAIN" || warn "The /.well-known/ fix did not apply — see section 6d: https://documentation.elmspark.com/guides/pagemotor-mcp-troubleshooting/"

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
echo "  After finishing setup at /admin/, confirm MCP sign-in will work:"
echo "    curl -sI https://$DOMAIN/.well-known/oauth-protected-resource"
echo "  It must say 200 and content-type: application/json."
echo ""
echo -e "${YELL}Save the DB password — it is not stored anywhere else.${OFF}"
