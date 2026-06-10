---
title: Vultr for PageMotor
description: Benchmarks, plan picker, region picker, and the bootstrap to get PageMotor 0.8.3b running on a fresh Vultr VPS.
sidebar:
  order: 1
---

A practical guide to running PageMotor on a VPS. Benchmarks, pricing comparisons, and the exact bootstrap we use to get PageMotor 0.8.3b live on a fresh box in about 30 minutes of hands-on work.

Published by [ElmsPark Studio](https://elmspark.com). Updated April 2026.

## Why a VPS, not shared hosting

Shared hosts cap PHP execution time, usually between 30 and 60 seconds, and will not lift it. For a brochure site, that is fine. For PageMotor with AI plugins, ecommerce, or a busy contact form, the cap becomes a ceiling the plugin keeps hitting.

A plugin that waits on an AI API response can easily spend more than a minute on a single request. Shared hosting kills the process halfway through. On a VPS the timeouts are yours to set.

## Why Vultr, specifically

In April 2026 we set up a three-way test rig across Vultr (New Jersey), DigitalOcean (New York) and Linode (Newark). Same PageMotor version, same plugins, same scenario on each. Measured disk, CPU, database, API latency, and end-to-end pipeline time.

In this run, Vultr led on every metric we measured, and on price.

| What | Vultr | DigitalOcean | Linode |
|---|---|---|---|
| Sequential disk write | **2,930 MB/s** | 1,223 MB/s | 587 MB/s |
| Random 4K IOPS | **139,264** | 68,894 | 94,856 |
| PHP benchmark | **0.076s** | 0.211s | 0.154s |
| 500 DB inserts | **1,484ms** | 5,445ms | 4,233ms |
| Anthropic API latency (network distance, see note) | **23.8ms** | 45.5ms | 35.8ms |
| Full pipeline time | **7m 17s** | 10m 38s | 7m 58s |
| Monthly cost | **$60** | $63 | $72 |

Fastest and cheapest of the three providers we tested, in this run. That is a good result, but read it as directional rather than a benchmark suite: it was a single April 2026 run on comparable mid-tier plans in the regions above. The Anthropic API latency row is dominated by network distance from each data centre to Anthropic's endpoint, not by the VPS itself, so treat it as a region and routing signal rather than host performance. Other low-cost hosts (for example Hetzner) were out of scope.

For PageMotor specifically, three of those numbers matter more than the rest. DB inserts matter because the admin is database-heavy. Disk IOPS matter because the page cache, CSS compiler and uploads all hit the disk constantly. API latency matters because AI plugins round-trip to Anthropic dozens of times per session.

## The $60 test rig pick

For the test rig we picked **Vultr VX1 (General Purpose), 2 vCPU, 8 GB RAM, 50 GB NVMe, $60/mo, in New Jersey**.

Three reasons:

1. **Dedicated vCPU.** No noisy neighbours. When ten customer sites all hit the box at lunchtime, nobody waits on nobody.
2. **Sized for 100 sites.** Vultr's measured range is 50 to 80 light-traffic PageMotor sites on this tier. We added headroom to cover a USA-wide audience without having to split the fleet later.
3. **New Jersey location.** Covers both US coasts at acceptable latency and had the lowest round-trip to Anthropic's API of the three hosts tested.

VX1 is Vultr's current-generation compute line, with dedicated CPU and NVMe storage, and is the successor to Vultr's older Optimized Cloud Compute tier. The 2 vCPU / 8 GB plan (`voc-g-2c-8gb-50s`) comes with 50 GB of local NVMe and bills at $0.089 an hour, about $60 a month. That 50 GB is comfortable for a fleet of light brochure and business sites. If you host image-heavy or media-heavy sites, add Vultr Block Storage and point your `user-content` uploads at it, so storage grows independently of the server.

## Pick a plan for your size

Vultr charges the same USD price in every data centre, so location does not change the bill. Only the plan does. Three profiles below, with pricing verified on vultr.com/pricing/ in April 2026.

### Solo owner with 1 or 2 PageMotor sites

**Cloud Compute, High Performance, 1 vCPU, 2 GB RAM, 50 GB NVMe — $12/mo.**

A genuinely capable box for a couple of brochure sites, a contact form, EP Email, EP Newsletter, and a Stripe-backed ecommerce setup. AI plugins will run, though heavy generations may hit the 2 GB RAM ceiling. For that workload, step up to High Performance 2 vCPU / 4 GB / 100 GB NVMe at $24/mo.

Auto Backups add $2.40/mo.

### SME with one main site and real traffic

**Cloud Compute, High Performance, 2 vCPU, 4 GB RAM, 100 GB NVMe — $24/mo.**

The sweet spot for a business running one serious site. Consultancy, small ecommerce shop, service business with booking and contact forms running all day. 100 GB NVMe is enough headroom for years of images, invoices and database growth. AI plugins run without drama. If sustained daily traffic regularly exceeds a few thousand visitors, step up to 4 vCPU / 8 GB / 180 GB NVMe at $48/mo.

Auto Backups add $4.80/mo.

### Service provider or agency reselling PageMotor hosting

**VX1 (General Purpose), 2 vCPU, 8 GB RAM, 50 GB NVMe — $60/mo.**

Dedicated vCPU is the critical difference. Expect 50 to 100 sites per box depending on traffic. For agencies past about 60 active sites, step up to VX1 4 vCPU / 16 GB / 80 GB NVMe at $120/mo, which roughly doubles the ceiling.

On a shared agency box, enable Auto Backups. $12/mo (20 per cent of the plan) is cheap insurance against one customer's mistake becoming every customer's problem.

### Quick reference

| Profile | Plan | Specs | Price | Capacity |
|---|---|---|---|---|
| Solo, 1-2 sites | High Performance | 1 vCPU / 2 GB / 50 GB NVMe | $12/mo | 1-2 PM sites |
| Solo with AI plugins | High Performance | 2 vCPU / 4 GB / 100 GB NVMe | $24/mo | 2-4 PM sites |
| SME, one busy site | High Performance | 2 vCPU / 4 GB / 100 GB NVMe | $24/mo | 1 busy site + ecommerce |
| SME, heavy traffic | High Performance | 4 vCPU / 8 GB / 180 GB NVMe | $48/mo | 1 busy site + AI plugins |
| Agency, 50-100 sites | VX1 | 2 vCPU / 8 GB / 50 GB NVMe | $60/mo | Our test rig pick |
| Agency, 100-200 sites | VX1 | 4 vCPU / 16 GB / 80 GB NVMe | $120/mo | Next step up |

Auto Backups add 20 per cent to whichever plan you pick. On production, enable them.

## Which region to pick

Same price everywhere. Latency is the only thing that changes. Pick the closest Vultr data centre to your visitors, not yourself.

### UK and Europe

London (UK), Frankfurt (Germany), Paris (France), Amsterdam (Netherlands), Madrid (Spain), Stockholm (Sweden), Warsaw (Poland).

For most UK and Irish users, London is the obvious pick. Frankfurt fits if you have significant German-speaking traffic or want a central-European footprint that reaches Berlin, Vienna and Prague at similar latency.

### USA

New Jersey, Miami, Atlanta, Chicago, Dallas, Seattle, Silicon Valley, Los Angeles.

New Jersey (our test rig choice) covers the whole of the eastern US at low latency and reaches the west coast at around 70 ms, which is fine for browsing. For a heavily west-coast audience, pick Silicon Valley or Los Angeles. Dallas is the sensible middle ground for genuinely coast-to-coast traffic.

### Rest of the world

Toronto, Mexico City, São Paulo, Santiago, Tokyo, Osaka, Seoul, Singapore, Mumbai, Delhi, Bangalore, Sydney, Melbourne, Johannesburg.

Vultr has regions across every populated continent (32 at the time of writing, April 2026). Almost always one within 100 ms of your audience.

## What to tick on the Vultr signup screen

| Setting | Pick | Why |
|---|---|---|
| Server type | Cloud Compute | Bare Metal, Kubernetes and Managed Databases are wrong shape for a PageMotor host. |
| CPU & Storage | Dedicated CPU, NVMe | Dedicated vCPUs avoid noisy-neighbour latency that PageMotor's admin feels. |
| Location | Closest to visitors | Same price in every region. Pick by audience latency. |
| Image | Ubuntu 24.04 LTS x64 | Security updates until 2029, ships PHP 8.3, all tooling is first-class. |
| Plan | Match to size | $12 solo / $24 SME / $60 agency / $120 scale. |
| Auto Backups | Enable for production | 20 per cent on top of the plan. Skip for a pure test rig only. |
| IPv6 Networking | Enabled (free) | Future-proofs the box at zero cost. |
| SSH Keys | ed25519, upload before first boot | Most important security click on the page. |
| Hostname | Descriptive, eg `pm-prod-01` | Readable in logs and dashboard. |
| Everything else | Default | No startup script, no VPC, no DDoS add-on at this scale. |

Generate an ed25519 key on your Mac with `ssh-keygen -t ed25519` if you do not already have one, and paste the public key (`~/.ssh/id_ed25519.pub`) into Vultr's SSH Keys section before launching.

## Let Claude Code do the heavy lifting

This guide recommends a complete, Claude-Code-driven stack: **Vultr** for the server, **Cloudflare** for DNS, and **Mailgun** for email. Three surfaces, one workflow. You say what you want; Claude Code provisions the box over SSH, manages the DNS through Cloudflare's API, and configures email delivery through the EP Mailgun plugins.

| Layer | Recommendation | What Claude Code does |
|---|---|---|
| Compute | Vultr VPS (Ubuntu 24.04) | SSHes in, bootstraps nginx + PHP + MariaDB + SSL |
| DNS | Cloudflare (free DNS, wholesale domains) | Points the domain and adds records via the Cloudflare API |
| Email | Mailgun (EU region for GDPR) | Configures the EP Mailgun plugins, adds the sending DNS records |

If "bash commands" and "edit the Nginx vhost" made your eyes glaze over, you are the reason this section exists. [Claude Code](https://claude.com/claude-code) is a command-line tool from Anthropic that will SSH into your Vultr box, run every command in this guide, and explain each step in plain English as it goes.

You do not need to understand what any of the commands do. You need to understand what you want: PageMotor 0.8.3b running at your domain, with SSL, on a fresh Vultr box. Tell Claude Code that, and it handles the rest.

### What Claude Code does for you

- Runs every `apt install`, config edit, `chmod` and `systemctl` command
- Shows you each command before running it, so you can watch it happen
- Checks the output of each step, stops on errors, asks before retrying
- Reads this guide as the reference, so the box matches what is documented
- Never deletes anything without asking first
- Uses British English and plain language when talking to you

### What Claude Code will NOT do automatically

- Create your Vultr account (you sign up as a human)
- Provision the VPS (you click through Vultr's signup screen)
- Point DNS at the new VPS IP (you edit your domain's DNS)
- Create your admin account (you register at `/admin/` on first visit)
- Install EP plugins in the same unattended run (it is a quick second prompt once your admin is registered, same tool)

The first four cross a human-authorisation line: money, identity, DNS ownership, admin rights. The rest, Claude Code does.

## Before Claude Code takes over: 7 manual steps

These are the things you do by hand first. Each is a one-time thing. After step 7, paste the prompt in the next section and Claude Code handles everything else.

**1. Buy a domain if you do not already have one.** Any registrar works (Namecheap, GoDaddy, Porkbun), but **we recommend Cloudflare**: DNS is free, domains renew at wholesale cost with no markup, and Claude Code can manage the DNS for you through Cloudflare's API (see step 6). Full setup, including letting Claude Code manage your records, is in the [Cloudflare DNS guide](/hosting/cloudflare/). You need to be able to edit the DNS A record, which every registrar supports.

**2. Install Claude Code on your Mac.** Download from [claude.com/claude-code](https://claude.com/claude-code). Free to install. You pay only for Anthropic API usage, which for this setup costs a few pence at most.

**3. Generate an SSH key on your Mac, one time ever.** Open Terminal and run:

```bash
ssh-keygen -t ed25519
```

Press Enter three times to accept the defaults. Your public key is now at `~/.ssh/id_ed25519.pub`. If you already did this years ago, skip to step 4.

**4. Sign up for Vultr and provision the VPS.** Sign up through our referral link: [vultr.com/?ref=9892518-9J](https://www.vultr.com/?ref=9892518-9J). That gives you **$300 of free Vultr credit** to test the platform, at no extra cost to you. Then provision a VPS using the choices in "What to tick on the Vultr signup screen" above. Paste your SSH public key from step 3 into the SSH Keys field during signup. This is the most important security click on the page.

To copy your public key to the clipboard:

```bash
cat ~/.ssh/id_ed25519.pub | pbcopy
```

Then paste into Vultr's SSH Keys field.

:::note[What the $300 credit covers]
On the $12 solo plan that is roughly 25 months of hosting. On the $24 SME plan, about 12 months. On the $60 agency box, about 5 months. You need to link a valid card or PayPal to activate the credit, and the unused portion expires 30 days after signup, so pick the plan you actually intend to run.
:::

:::tip[Full disclosure]
If you stay on Vultr past 30 days and spend at least $100, we earn a $100 referral credit from Vultr. It costs you nothing and does not change the price you pay. You still get the same $300 credit whether you click our link or Vultr's generic signup, so we would rather you use the link and help fund the next round of PageMotor hosting tests.
:::

**5. Note the VPS IP address.** Once the VPS finishes provisioning (30 to 60 seconds), Vultr's dashboard shows the public IP. Copy it. You need it for step 6 and for the prompt.

**6. Point your domain's A record at the VPS IP.** Log in to your registrar and edit the A record for your root domain to point at the VPS IP from step 5. Propagation takes anywhere from a few minutes to an hour.

If your DNS is on Cloudflare, you can hand this to Claude Code instead of editing it by hand: once it has Cloudflare API access for your account, give it the VPS IP and it sets the A record and confirms propagation for you. Set the record to **DNS only (grey cloud, proxy off)** so the A record resolves straight to the Vultr box; this is the simplest path and lets certbot issue your SSL cert in step 7 without obstruction. See the [Cloudflare DNS guide](/hosting/cloudflare/) for moving your DNS over and creating the scoped token.

Quick check it worked: `dig yoursite.com +short` in Terminal should return the VPS IP.

**7. Download the PageMotor 0.8.3b core files.** Grab the official PageMotor 0.8.3b core ZIP from the forum download area and unzip it somewhere easy to find, like `~/Downloads/pagemotor-0.8.3b/`. Note the path. You need it in the prompt.

The folder should contain `pagemotor.php`, `index.php`, `lib/`, `config-sample.php` and `license.txt`.

## The prompt (copy, paste, edit three lines)

Open Claude Code in Terminal, paste the prompt below, edit the three bracketed placeholders to match your setup, then hit Enter and watch it run.

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
3. Run mysql_secure_installation (set root auth, remove anonymous users
   and the test database, disallow remote root) and confirm MariaDB
   listens only on localhost
4. Configure MariaDB to default to utf8mb4
5. At an interactive mariadb prompt (never put the DB password on the
   shell command line), create the database and a dedicated DB user
   scoped to it
6. Upload my PageMotor 0.8.3b core to /var/www/mysite on the VPS,
   create user-content subfolders, set ownership to www-data,
   755 directories / 644 files (no 777 or 775; www-data owns the tree)
7. Write config.php with my four database constants:
   DB_NAME, DB_USER, DB_PASSWORD and DB_HOST (localhost). Leave the rest blank.
8. Create the Nginx vhost with fastcgi_read_timeout 600,
   client_max_body_size 64M, and the /lib/ php denial rule
9. Set PHP max_execution_time to 300 and memory_limit to 256M
10. Run certbot --nginx for SSL, then verify renewal with
    certbot renew --dry-run and confirm the certbot timer is active
11. Verify the Nginx config is valid and services are running
12. Hit the homepage once with curl to trigger PageMotor's first-load
    table creation
13. Confirm the tables exist in the database

Stop after step 13. Do NOT register an admin account. Do NOT install
EP plugins. I will register via /admin/ in a browser, then ask you to
install plugins as a separate next task.

Rules:
- Tell me what you are about to do before doing it
- Show me the output of each step
- Stop on any error and ask me before continuing
- British English (organise, behaviour, colour)
- No em dashes in any file you write. Use commas or full stops.
- Ask before anything destructive
```

**What to edit:**

1. `[VPS_IP_FROM_VULTR]` with your VPS IP (eg `149.28.47.148`)
2. `[yoursite.com]` with your actual domain (appears twice)
3. `[~/Downloads/pagemotor-0.8.3b/]` with the actual path where you unzipped the core

### After the prompt finishes

Claude Code stops at the last step and tells you the site is ready to register. Now the manual bit:

1. Open `https://yoursite.com/admin/` in your browser
2. Register your first account. Whoever registers first becomes the administrator.
3. Come back to Claude Code and say:

```
Please install EP Email, EP Newsletter, EP Email Mailgun, EP Newsletter Mailgun,
EP GDPR, EP Password Reset, EP Diagnostics and EP Assistant on yoursite.com.
Then configure EP Email to send through Mailgun: set the Email Transport to
Mailgun EU (api.eu.mailgun.net, GDPR-clean routing) using my Mailgun sending
key [paste-sending-key] and sending domain mg.yoursite.com.
```

**One thing the prompt does not cover yet:** email delivery. Once the plugins are in, you will need a Mailgun account (the free plan is 100 emails/day, no card) and a verified sending subdomain (`mg.yoursite.com`) with its SPF and DKIM DNS records added. Mailgun sends over its HTTPS API, so Vultr's outbound port-25 block does not get in the way. See the **Email: Mailgun (recommended)** section below, or follow the dedicated Mailgun walkthrough.

## Email: Mailgun (recommended)

Vultr gives you the box, not email. And Vultr blocks outbound port 25, so traditional SMTP is not an option anyway. Mailgun is the production recommendation across both EP Email (transactional: contact-form notifications, password resets, opt-in confirmations) and EP Newsletter (campaigns), via the **EP Email Mailgun** and **EP Newsletter Mailgun** driver plugins.

- **The port-25 block does not matter.** The EP Mailgun drivers POST to Mailgun's HTTPS API on port 443, not SMTP, so Vultr's blocked port 25 never comes into it.
- **EU region for GDPR.** Pick the **Mailgun EU** transport (`api.eu.mailgun.net`) for EU and UK audiences. The region is locked per domain for life, so choose it when you create the domain. North-American audiences pick **Mailgun US** (`api.mailgun.net`).
- **Free to start.** Mailgun's free plan is 100 emails a day with one verified custom sending domain, no credit card.

### Use a sending subdomain, not your root domain

Verify `mg.yourdomain.com` in Mailgun, never `yourdomain.com` itself. Sending from a subdomain keeps Mailgun's DNS and your sending reputation separate from your existing mailbox.

:::caution[Never put Mailgun's MX records on your root domain]
Mailgun's MX records are for inbound mail only. On your apex domain they hijack delivery away from your existing mailbox (Google Workspace, Microsoft 365, your host) and incoming mail silently stops. Sending needs only the SPF and DKIM records on `mg.`.
:::

### What to add in Cloudflare

For the `mg.yourdomain.com` subdomain, all set **DNS only (grey cloud)**, never the orange proxy, which would break email authentication:

- One **SPF** TXT record at `mg.yourdomain.com`
- Two **DKIM** CNAME records at `pdk1._domainkey.mg…` and `pdk2._domainkey.mg…`
- One **tracking** CNAME at `email.mg…` (for open and click tracking)
- The two **MX** records only if you want Mailgun to *receive* mail (you usually do not, and never on the apex)

Copy the exact values from your Mailgun domain settings page. If your DNS is on Cloudflare, Claude Code can add these for you with a Cloudflare API token, in the same session it points the A record (see the [Cloudflare DNS guide](/hosting/cloudflare/)).

For the full end-to-end walkthrough (signup, region choice, DNS, DKIM activation, sending key, and inbox-placement verification), follow the dedicated Mailgun setup guide.

> **Fallback:** if you cannot use Mailgun (no card-free option in your region, or an account-review hold), Brevo's free tier (300 emails a day) is a workable second choice via the EP Brevo drivers, with a deliverability trade-off. **SendGrid is now legacy** for new setups: Twilio stopped offering permanent free plans to new SendGrid accounts on 25 March 2025 (new accounts get a 60-day trial only). The EP Newsletter SendGrid plugin still works for existing users but is no longer the recommended path.

## From empty box to live PageMotor (what Claude Code does under the hood)

If you are using the Claude Code prompt above, you can skip this section. It documents the exact sequence Claude Code runs for you, kept here for transparency and for anyone who prefers to do it by hand.

About 30 minutes of hands-on work once your DNS has propagated. Allow longer on a first run.

### 1. Bootstrap the server

SSH in as root using your ed25519 key.

```bash
apt update && apt upgrade -y
apt install -y nginx php8.3-fpm php8.3-mysql php8.3-curl php8.3-gd \
  php8.3-mbstring php8.3-xml php8.3-zip php8.3-intl php8.3-bcmath \
  php8.3-opcache mariadb-server certbot python3-certbot-nginx \
  fail2ban ufw unattended-upgrades unzip

# Confirm PageMotor's required PHP extensions are present
php -m | grep -iE 'mysqli|mbstring|curl|zip|fileinfo|openssl'
# (fileinfo and openssl ship inside php8.3-common; gd is optional, for image
#  plugins, not a PageMotor core dependency.)

# Turn on automatic security updates
dpkg-reconfigure -plow unattended-upgrades

ufw allow OpenSSH        # opens port 22
ufw allow 'Nginx Full'   # opens ports 80 and 443
ufw enable
```

This leaves only ports 22, 80 and 443 open.

Fail2ban installs inactive, so enable an SSH jail:

```bash
cat > /etc/fail2ban/jail.local <<'EOF'
[sshd]
enabled = true
maxretry = 5
bantime = 1h
EOF
systemctl enable --now fail2ban
fail2ban-client status sshd   # confirm the jail is actually running
```

### 2. Make MariaDB speak utf8mb4 by default

Without this, emojis land in the database as `?`. Create `/etc/mysql/conf.d/utf8mb4.cnf`:

```ini
[mysqld]
character-set-server = utf8mb4
collation-server = utf8mb4_unicode_ci

[client]
default-character-set = utf8mb4
```

Then `systemctl restart mariadb`.

### 3. Harden MariaDB, then create the database

Lock down the defaults first:

```bash
mysql_secure_installation
```

Accept the prompts: set or confirm the root authentication, remove anonymous users, disallow remote root login, and drop the `test` database. MariaDB on Ubuntu 24.04 already listens only on localhost by default (`bind-address = 127.0.0.1` in `/etc/mysql/mariadb.conf.d/50-server.cnf`), which is what you want.

Now create the database and a scoped user. Use an interactive prompt so the password never lands in your shell history:

```bash
mariadb -u root -p
```

At the `MariaDB>` prompt:

```sql
CREATE DATABASE mysite_pm CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
CREATE USER 'mysite_db'@'localhost' IDENTIFIED BY 'your-strong-password';
GRANT ALL ON mysite_pm.* TO 'mysite_db'@'localhost';
FLUSH PRIVILEGES;
EXIT;
```

Use a dedicated user scoped to this database only. Never put root credentials in `config.php`.

### 4. Drop PageMotor 0.8.3b into place

```bash
mkdir -p /var/www/mysite
cd /var/www/mysite
# Copy pagemotor.php, index.php and lib/ from your local 0.8.3b core
mkdir -p user-content/{themes,plugins,images,uploads,css,tmp,logs}
```

Copy `config-sample.php` to `config.php` and fill in the four database constants: `DB_NAME`, `DB_USER`, `DB_PASSWORD` and `DB_HOST` (which stays `localhost`). Leave `DB_CHARSET`, `DB_COLLATE`, `DB_TABLE_PREFIX` (defaults to `pm_`), `PM_INSTALL_LOCATION`, `PM_ADMIN_SLUG` and `PM_HTML_CHARSET` at their defaults. PageMotor uses utf8mb4 automatically, so the charset and collation lines stay blank.

```bash
chown -R www-data:www-data /var/www/mysite
find /var/www/mysite -type d -exec chmod 755 {} \;
find /var/www/mysite -type f -exec chmod 644 {} \;
# www-data owns the tree, so 755 directories already let PHP write to
# user-content. No 775 or 777 needed. Add setgid so files created later
# keep the www-data group:
find /var/www/mysite/user-content -type d -exec chmod g+s {} \;
```

### 5. The Nginx vhost

Create `/etc/nginx/sites-available/mysite`:

```nginx
server {
    listen 80;
    server_name yoursite.com;
    root /var/www/mysite;
    index index.php index.html;

    fastcgi_read_timeout 600;
    proxy_read_timeout 600;
    send_timeout 600;
    client_max_body_size 64M;

    add_header X-Content-Type-Options nosniff;
    add_header X-Frame-Options SAMEORIGIN;

    location / {
        try_files $uri $uri/ /index.php?$query_string;
    }
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

Enable it:

```bash
ln -s /etc/nginx/sites-available/mysite /etc/nginx/sites-enabled/
nginx -t && systemctl reload nginx
```

`fastcgi_read_timeout 600` is the critical line. Nginx defaults to 60 seconds, which any AI plugin will blow through on a heavy call.

### 6. PHP settings that match Nginx

Edit `/etc/php/8.3/fpm/php.ini`:

```ini
max_execution_time = 300
memory_limit = 256M
upload_max_filesize = 64M
post_max_size = 64M
```

`systemctl reload php8.3-fpm`. PHP timeout shorter than Nginx means surprise 504s. PHP longer than Nginx means processes running past when Nginx gave up. Keep them aligned.

On the $12 / 2 GB plan these values are fine, but a few concurrent 300-second AI calls can exhaust RAM. On that plan, cap php-fpm `pm.max_children` in `/etc/php/8.3/fpm/pool.d/www.conf` and add a small swap file so a burst cannot take the box down.

### 7. SSL with Certbot

Point your domain's A record at the Vultr IP, wait for DNS to propagate, then:

```bash
certbot --nginx -d yoursite.com
```

Adds the 443 block, redirects 80 to 443, and installs a renewal timer. The nginx plugin reloads nginx automatically when it renews. Confirm both the timer and the renewal path before you walk away:

```bash
systemctl list-timers | grep certbot   # the renewal timer is active
certbot renew --dry-run                 # the renewal actually works
```

:::caution[If you put Cloudflare's proxy in front of the box]
**Issue the SSL cert first with the record DNS-only (grey cloud).** That points the hostname straight at the Vultr IP, so certbot's HTTP-01 challenge reaches nginx and a real Let's Encrypt cert is issued. With the orange-cloud proxy on, the challenge hits Cloudflare instead of your server and issuance breaks. DNS-only also means PageMotor sees a true HTTPS connection and emits correct `https://` links.

Only turn the proxy on **after** the cert is live, for CDN and DDoS protection. When you do, set the SSL/TLS mode to **Full (strict)** so Cloudflare validates your real Let's Encrypt cert. **Never use Flexible:** it talks to your origin over plain HTTP, which makes PageMotor read the request as insecure, emit `http://` links, and risk an infinite redirect loop. If you need to stay proxied during renewals, switch certbot to the DNS-01 challenge with a Cloudflare API token instead of HTTP-01.
:::

### 8. First page load creates the tables

Load your domain in a browser. PageMotor's first front-end request auto-creates its database tables, so there is no SQL file to import. The docroot must be writable by `www-data` at this point, which the ownership step in section 4 already ensures. Then visit `/admin/` to reach the Admin Registration screen. The first account you register becomes the administrator.

If you ever get a blank page here, PageMotor 0.8.3b deliberately keeps PHP errors off the screen and writes them to `/var/www/mysite/user-content/logs/php-errors.log`. Read that file rather than turning `display_errors` on; PageMotor forces it off on every boot. A genuine "Unknown collation 'utf8mb4_unicode_520_ci'" there only happens on a very old database server (MariaDB 10.1 or earlier); Ubuntu 24.04's MariaDB 10.11 ships that collation, so this should not occur on the stack above.

### 9. Install essential plugins

Through the admin, install and activate: EP Email, EP Newsletter, EP Email Mailgun, EP Newsletter Mailgun, EP GDPR, EP Password Reset, EP Diagnostics and EP Assistant.

Configure EP Email to send through Mailgun. Mailgun delivers over its HTTPS API rather than SMTP, which sidesteps Vultr's outbound port-25 block entirely. Pick the **Mailgun EU** transport (`api.eu.mailgun.net`) for GDPR-clean routing if your audience is in the EU or UK, or **Mailgun US** otherwise. See the **Email: Mailgun (recommended)** section for the DNS records and the `mg.` subdomain caution.

## Settings people forget (and later regret)

- **`fastcgi_read_timeout` must be 600 or higher.** Default 60 kills AI plugins mid-call.
- **`max_execution_time = 300`.** Match PHP to Nginx or expect 504s.
- **MariaDB `character-set-server = utf8mb4`.** Without this, emojis corrupt silently.
- **UFW before anything else.** A new server gets scanned within minutes. Close the doors first.
- **Run `mysql_secure_installation`.** A default MariaDB install leaves an open `test` database and anonymous users until you do.
- **Enable the fail2ban [sshd] jail.** The package installs inactive; without a `jail.local` nothing is banning anyone.
- **ed25519 SSH keys, then harden login.** Once keys work, set `PasswordAuthentication no` and `PermitRootLogin prohibit-password` in `/etc/ssh/sshd_config`, then `systemctl reload ssh`. For a multi-admin box, create a non-root sudo user and disable root login entirely.
- **`unattended-upgrades` on.** A one-time `apt upgrade` at provisioning is not enough for a box that lives for years.
- **opcache on.** Default on Ubuntu 24.04 but verify with `php -m | grep -i opcache`. 3 to 5 times the page speed for free.

## The cost side

The $60 Vultr box was sized for 100 PageMotor sites, based on the measured range of 50 to 80 light-traffic sites per box plus headroom for a USA-wide audience. At 100 sites that works out at roughly 50p each per month. Even at the more cautious 50-site figure, about £1 each. Compare to shared hosting at £5 to £15 per site per month, where AI plugins still cannot run reliably.

Important caveat for single-site owners: the $12 High Performance plan is the right answer for one or two sites, not the $60 one. The VX1 plan only pays off past roughly five sites.

## Summary

| Question | Answer |
|---|---|
| Which host? | Vultr |
| Which DNS / registrar? | Cloudflare (free DNS, wholesale domains, Claude-Code-manageable) |
| Which email? | Mailgun (HTTPS API, EU region for GDPR, free 100/day) |
| Which region? | Closest to your visitors (same price everywhere) |
| Which plan? | $12 solo / $24 SME / $60 agency / $120 scale |
| Which OS? | Ubuntu 24.04 LTS |
| Which stack? | Nginx + PHP 8.3 FPM + MariaDB + Certbot |
| Security baseline? | UFW, ed25519 keys, Fail2ban jail, password + root login hardened, automatic security updates |
| Critical timeouts? | PHP 300s, Nginx 600s, matched |
| Time to live? | About 30 minutes from empty box |

## Feedback and corrections

Spotted a mistake, an outdated price, or a step that no longer works? [Open an issue on GitHub](https://github.com/ElmsPark-Studio/documentation/issues). Pricing especially shifts, every figure here was verified in April 2026, but Vultr changes plans and prices regularly, so always cross-check vultr.com/pricing/ before signing up.
