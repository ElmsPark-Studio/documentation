# Hosting PageMotor on Vultr — LLM Prompt

> **How to use this file:** Paste the entire contents into Claude, ChatGPT, Gemini, or any LLM as your opening message. It primes the model with the full guide so it can walk you through the VPS setup step by step, ask where you're up to, and help you troubleshoot anything that goes wrong. You don't need to read the guide yourself first — just paste and ask.
>
> *Source: [documentation.elmspark.com/guides/vultr-hosting](https://documentation.elmspark.com/guides/vultr-hosting/)*

---

You are helping me set up PageMotor on a Vultr VPS. Use this guide as your reference. Walk me through each step, ask me what I've completed, and help me troubleshoot anything. If I want to use Claude Code to automate the server setup, give me the ready-to-use prompt. If I'm doing it by hand, walk me through each command.

## Context

**Time:** ~30 minutes hands-on  
**Cost:** From $12/month  
**Stack:** Ubuntu 24.04 + Nginx + PHP 8.3 FPM + MariaDB + Certbot  
**Can be automated:** Yes — Claude Code can do the entire server build via SSH

**Why a VPS instead of shared hosting:** Shared hosts cap PHP execution time (usually 30–60 seconds) and won't lift it. PageMotor with AI plugins, ecommerce, or a busy contact form will hit that ceiling. A VPS means the timeouts are yours to set. Also, Vultr blocks outbound port 25 — email goes through Mailgun's HTTPS API instead (covered in the Email section).

### April 2026 benchmark results (Vultr vs DigitalOcean vs Linode)

| What | Vultr | DigitalOcean | Linode |
|---|---|---|---|
| Sequential disk write | 2,930 MB/s | 1,223 MB/s | 587 MB/s |
| Random 4K IOPS | 139,264 | 68,894 | 94,856 |
| PHP benchmark | 0.076s | 0.211s | 0.154s |
| 500 DB inserts | 1,484ms | 5,445ms | 4,233ms |
| Monthly cost | $60 | $63 | $72 |

---

## Plan Selection

| Profile | Plan | Specs | Price |
|---|---|---|---|
| Solo, 1-2 sites | High Performance | 1 vCPU / 2 GB / 50 GB | $12/mo |
| Solo with AI plugins | High Performance | 2 vCPU / 4 GB / 100 GB | $24/mo |
| SME, one busy site | High Performance | 2 vCPU / 4 GB / 100 GB | $24/mo |
| SME, heavy traffic | High Performance | 4 vCPU / 8 GB / 180 GB | $48/mo |
| Agency, 50-100 sites | VX1 | 2 vCPU / 8 GB / 50 GB | $60/mo |
| Agency, 100-200 sites | VX1 | 4 vCPU / 16 GB / 80 GB | $120/mo |

Auto Backups add 20% to the plan price. Enable them on production. Pricing verified April 2026.

**Agency cost per site example:** 100 sites on a VX1 ($60/mo) = $0.60 per site per month. Shared hosting charges $5–15 per site and AI plugins won't run on it.

---

## Vultr Sign-Up Settings

| Setting | Pick | Why |
|---|---|---|
| Server type | Shared CPU | Right shape for PageMotor at all but the very largest scale |
| Location | Closest to visitors | Same price everywhere. Pick by audience latency. |
| Plan | vc2-1c-2gb ($10/mo) to start | Handles a typical PageMotor site; resize up later without reinstalling |
| Image | Ubuntu, latest LTS | Long-term support, ships PHP 8.3 |
| Auto Backups | Enable for production | 20% on top of plan price |
| SSH Keys | ed25519, before first boot | Most important security click on the page |
| Hostname | Descriptive (e.g. pm-prod-01) | Readable in logs and dashboard |
| Everything else | Default | No startup script, no VPC, no DDoS add-on at this scale |

**Region guide:**
- UK & Europe: London, Frankfurt, Paris, Amsterdam, Madrid, Stockholm, Warsaw. London for most UK/Irish users; Frankfurt for central-European footprint.
- USA: pick by audience location

**No SSH key yet?** Generate one: `ssh-keygen -t ed25519`, press Enter three times. Public key is at `~/.ssh/id_ed25519.pub`. Copy it with: `cat ~/.ssh/id_ed25519.pub | pbcopy`

---

## Option A — The Claude Code Way (Recommended)

Claude Code is a command-line tool from Anthropic that SSHes into your Vultr box, runs every command, and explains each step in plain English. You don't need to understand the commands.

### 7 manual steps before Claude Code takes over

1. **Buy a domain** if you don't have one. Cloudflare is recommended (free DNS, wholesale renewals, Claude-Code-manageable).
2. **Install Claude Code** on your Mac from [claude.com/claude-code](https://claude.com/claude-code)
3. **Generate an SSH key** (one time): `ssh-keygen -t ed25519`, press Enter three times
4. **Sign up for Vultr and provision the VPS** using the settings above. Paste your SSH public key into the SSH Keys field during signup.
5. **Note the VPS IP address** once provisioning finishes (30–60 seconds)
6. **Point your domain's A record at the VPS IP.** Set DNS Only (grey cloud) if on Cloudflare. Check: `dig yoursite.com +short` should return the VPS IP.
7. **Download the PageMotor 0.8.3b core ZIP**, unzip to somewhere easy like `~/Downloads/pagemotor-0.8.3b/`. Should contain: `pagemotor.php`, `index.php`, `lib/`, `config-sample.php`, `license.txt`.

### The Claude Code prompt (copy, paste, edit 3 lines, hit Enter)

```
I have a fresh Ubuntu 24.04 VPS at [VPS_IP_FROM_VULTR].
I can SSH as root using my ed25519 key at ~/.ssh/id_ed25519.

My domain is [yoursite.com]. The A record already points at the VPS IP.

My PageMotor 0.8.3b core files are in [~/Downloads/pagemotor-0.8.3b/].
The folder contains pagemotor.php, index.php, lib/, config-sample.php, license.txt.

Please follow the "From empty box to live PageMotor" procedure at
https://documentation.elmspark.com/hosting/vultr/

Do this end-to-end:
1. Bootstrap the server (nginx, PHP 8.3 FPM with required extensions,
   MariaDB, certbot, fail2ban, UFW allowing only 22/80/443, and
   unattended-upgrades for automatic security patches)
2. Configure a fail2ban [sshd] jail and confirm it is active
3. Run mysql_secure_installation and confirm MariaDB listens only on localhost
4. Configure MariaDB to default to utf8mb4
5. At an interactive mariadb prompt, create the database and a dedicated DB user
6. Upload my PageMotor 0.8.3b core to /var/www/mysite, set ownership to www-data,
   755 directories / 644 files (no 777 or 775)
7. Write config.php with DB_NAME, DB_USER, DB_PASSWORD and DB_HOST (localhost)
8. Create the Nginx vhost with fastcgi_read_timeout 600, client_max_body_size 64M
9. Set PHP max_execution_time to 300 and memory_limit to 256M
10. Run certbot --nginx for SSL, verify renewal, confirm certbot timer is active
11. Verify Nginx config is valid and services are running
12. Hit the homepage once with curl to trigger PageMotor's first-load table creation
13. Confirm the tables exist in the database

Stop after step 13. Do NOT register an admin account. Do NOT install EP plugins.
I will register via /admin/ in a browser, then ask you to install plugins separately.

Rules:
- Tell me what you are about to do before doing it
- Show me the output of each step
- Stop on any error and ask me before continuing
- British English (organise, behaviour, colour)
- Ask before anything destructive
```

**Edit before running:** `[VPS_IP_FROM_VULTR]` → your VPS IP; `[yoursite.com]` → your domain (appears twice); `[~/Downloads/pagemotor-0.8.3b/]` → your path.

### After the prompt finishes

1. Open `https://yoursite.com/admin/` in your browser
2. Register your first account — whoever registers first becomes administrator
3. Come back to Claude Code and paste the plugins prompt:

```
Please install EP Email, EP Newsletter, EP Email Mailgun, EP Newsletter Mailgun,
EP GDPR, EP Password Reset, EP Diagnostics and EP Assistant on yoursite.com.
Then configure EP Email to send through Mailgun: set the Email Transport to
Mailgun EU (api.eu.mailgun.net, GDPR-clean routing) using my Mailgun sending
key [paste-sending-key] and sending domain mg.yoursite.com.
```

---

## Option B — By Hand (~30 minutes)

### 1. Bootstrap the server

SSH in as root, then:

```bash
apt update && apt upgrade -y
apt install -y nginx php8.3-fpm php8.3-mysql php8.3-curl php8.3-gd \
  php8.3-mbstring php8.3-xml php8.3-zip php8.3-intl php8.3-bcmath \
  php8.3-opcache mariadb-server certbot python3-certbot-nginx \
  fail2ban ufw unattended-upgrades unzip

php -m | grep -iE 'mysqli|mbstring|curl|zip|fileinfo|openssl'
dpkg-reconfigure -plow unattended-upgrades

ufw allow OpenSSH
ufw allow 'Nginx Full'
ufw enable
```

Enable fail2ban SSH jail:

```bash
cat > /etc/fail2ban/jail.local <<'EOF'
[sshd]
enabled = true
maxretry = 5
bantime = 1h
EOF
systemctl enable --now fail2ban
fail2ban-client status sshd
```

### 2. Make MariaDB use utf8mb4

Create `/etc/mysql/conf.d/utf8mb4.cnf`:

```ini
[mysqld]
character-set-server = utf8mb4
collation-server = utf8mb4_unicode_ci

[client]
default-character-set = utf8mb4
```

Then `systemctl restart mariadb`.

### 3. Harden MariaDB and create the database

Run `mysql_secure_installation`, then create a scoped database and user:

```sql
-- At an interactive mariadb prompt (never put the DB password on the shell command line)
mariadb -u root -p

CREATE DATABASE mysite_pm CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
CREATE USER 'mysite_db'@'localhost' IDENTIFIED BY 'your-strong-password';
GRANT ALL ON mysite_pm.* TO 'mysite_db'@'localhost';
FLUSH PRIVILEGES;
EXIT;
```

### 4. Drop PageMotor into place

```bash
mkdir -p /var/www/mysite
cd /var/www/mysite
# Copy pagemotor.php, index.php and lib/ from your local core
mkdir -p user-content/{themes,plugins,images,uploads,css,tmp,logs}
# Copy config-sample.php to config.php and fill in DB_NAME, DB_USER, DB_PASSWORD, DB_HOST=localhost
chown -R www-data:www-data /var/www/mysite
find /var/www/mysite -type d -exec chmod 755 {} \;
find /var/www/mysite -type f -exec chmod 644 {} \;
find /var/www/mysite/user-content -type d -exec chmod g+s {} \;
```

### 5. Nginx vhost

Create `/etc/nginx/sites-available/mysite`:

```nginx
server {
    listen 80;
    server_name yoursite.com;
    root /var/www/mysite;
    index index.php index.html;

    fastcgi_read_timeout 600;    # Critical: default 60s kills AI plugins mid-call
    proxy_read_timeout 600;
    send_timeout 600;
    client_max_body_size 64M;

    add_header X-Content-Type-Options nosniff;
    add_header X-Frame-Options SAMEORIGIN;

    location / { try_files $uri $uri/ /index.php?$query_string; }
    location ~ \.php$ {
        include snippets/fastcgi-php.conf;
        fastcgi_pass unix:/run/php/php8.3-fpm.sock;
        fastcgi_read_timeout 600;
    }
    location ~ ^/lib/.*\.(js|css|woff|woff2|ttf|eot|svg|png|jpg|gif)$ {
        try_files $uri =404;
    }
    location ~ ^/lib/.*\.php$ { deny all; }
    location ~ /\.(ht|git|env) { deny all; }
}
```

```bash
ln -s /etc/nginx/sites-available/mysite /etc/nginx/sites-enabled/
nginx -t && systemctl reload nginx
```

### 6. PHP settings

Edit `/etc/php/8.3/fpm/php.ini`:

```ini
max_execution_time = 300
memory_limit = 256M
upload_max_filesize = 64M
post_max_size = 64M
```

`systemctl reload php8.3-fpm`

### 7. SSL

```bash
certbot --nginx -d yoursite.com
systemctl list-timers | grep certbot
certbot renew --dry-run
```

**If using Cloudflare proxy:** issue the cert first with DNS Only (grey cloud) so certbot's HTTP-01 challenge reaches Nginx. After the cert is live, you can enable the orange proxy — but set SSL/TLS mode to **Full (strict)**. Never use Flexible: it sends traffic to your origin over plain HTTP.

### 8. First page load creates the tables

Visit your domain in a browser. PageMotor's first request auto-creates its database tables — no SQL file to import. Then visit `/admin/` to register your first admin account.

Blank page? PageMotor writes errors to `/var/www/mysite/user-content/logs/php-errors.log`. Read that file first.

---

## Settings People Forget (and Later Regret)

- **`fastcgi_read_timeout 600` or higher.** Default 60s kills AI plugins mid-call.
- **`max_execution_time = 300`.** Match PHP to Nginx or expect 504 errors.
- **MariaDB `character-set-server = utf8mb4`.** Without it, emojis corrupt silently.
- **UFW before anything else.** A new server gets scanned within minutes.
- **Run `mysql_secure_installation`.** Default install leaves open test database and anonymous users.
- **Enable the fail2ban [sshd] jail.** The package installs inactive.
- **ed25519 keys, then harden SSH.** Set `PasswordAuthentication no` and `PermitRootLogin prohibit-password`.
- **`unattended-upgrades` on.** A one-time `apt upgrade` is not enough for a box that runs for years.
- **Opcache on.** Default on Ubuntu 24.04. Verify with `php -m | grep -i opcache`. 3–5x page speed for free.

---

## Email: Mailgun

Vultr blocks outbound port 25 — traditional SMTP is out anyway. Use Mailgun via EP Email Mailgun and EP Newsletter Mailgun plugins, which POST to Mailgun's HTTPS API on port 443.

- **EU region for GDPR.** Use `api.eu.mailgun.net` for UK/EU audiences. Region is locked per domain — choose it when creating the sending domain.
- **Free to start.** 100 emails/day with one verified sending domain, no card.
- **Never put Mailgun's MX records on your root domain.** Verify `mg.yourdomain.com`, never `yourdomain.com` itself. Mailgun's MX records on your apex will silently hijack your incoming email.

For the full walkthrough, use the [Mailgun LLM prompt](https://documentation.elmspark.com/guides/mailgun-email/) from the same download location, or follow the guide at [documentation.elmspark.com/guides/mailgun-email/](https://documentation.elmspark.com/guides/mailgun-email/).

---

*Source: ElmsPark documentation — documentation.elmspark.com/guides/vultr-hosting/*  
*Benchmarks and pricing: April 2026. Cross-check vultr.com/pricing/ before signing up.*
